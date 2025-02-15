from firepit.query import (
    Query,
    Projection,
    Table,
    Filter,
    Predicate,
    Count,
    Unique,
    Join,
)
from collections import OrderedDict
from kestrel.codegen.relations import all_entity_types, stix_2_0_identical_mapping
from kestrel.exceptions import KestrelInternalError


def gen_variable_summary(var_name, var_struct):
    """Generate summary dictionary for a variable.

    Args:

        variable (kestrel.symboltable.VarStruct): The target variable.

    Returns:

        dict: ``str`` to ``str`` dict on the variable summary.

    """
    summary = OrderedDict()
    footnote = "*Number of related records cached."

    summary["VARIABLE"] = var_name
    summary["TYPE"] = var_struct.type
    summary["#(ENTITIES)"] = len(var_struct)
    summary["#(RECORDS)"] = var_struct.records_count

    query_ids = _get_variable_query_ids(var_struct)

    for table in var_struct.store.tables():

        if table in all_entity_types:
            count = 0

            if query_ids:
                query_ids_filter = Filter([Predicate("query_id", "IN", query_ids)])
                query = Query()
                query.append(Table(table))
                query.append(Join("__queries", "id", "=", "sco_id"))
                query.append(query_ids_filter)
                query.append(Count())
                result = var_struct.store.run_query(query).fetchall()
                count = result[0]["count"]
                if table == var_struct.type and count:
                    count = count - len(var_struct)
                    if count < 0:
                        raise KestrelInternalError(
                            f"impossible count regarding variable {var_name} and table {table}"
                        )

            summary[f"{table}*"] = count

    return summary, footnote


def _get_variable_query_ids(variable):
    if variable.entity_table:
        query = Query()
        query.append(Table("__queries"))
        query.append(Join("__membership", "sco_id", "=", "sco_id"))
        query.append(Filter([Predicate("var", "=", variable.entity_table)]))
        query.append(Projection(["query_id"]))
        query.append(Unique())
        rows = variable.store.run_query(query).fetchall()
        query_ids = [r["query_id"] for r in rows]
    else:
        query_ids = []
    return query_ids


def get_variable_entity_count(variable):
    if variable.entity_table:
        query = Query()
        query.append(Table(variable.entity_table))
        cols = (
            stix_2_0_identical_mapping[variable.type]
            if variable.type in stix_2_0_identical_mapping
            else ["id"]
        )
        query.append(Projection(cols))
        query.append(Unique())
        query.append(Count())
        rows = variable.store.run_query(query).fetchall()
        entity_count = rows[0]["count"] if rows else 0
    else:
        entity_count = 0
    return entity_count
