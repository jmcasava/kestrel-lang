===============================
Kestrel Threat Hunting Language
===============================

.. image:: https://img.shields.io/pypi/pyversions/kestrel-lang
        :target: https://pypi.python.org/pypi/kestrel-lang/

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
        :target: https://github.com/psf/black

.. image:: https://img.shields.io/pypi/v/kestrel-lang
        :target: https://pypi.python.org/pypi/kestrel-lang/

.. image:: https://img.shields.io/pypi/dm/kestrel-lang
        :target: https://pypi.python.org/pypi/kestrel-lang/

.. image:: https://readthedocs.org/projects/kestrel/badge/?version=latest
        :target: https://kestrel.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

|

What is Kestrel? Why we need it? How to hunt with XDR support? What is the
science behind it?

You can find all the answers at `Kestrel documentation hub`_. A quick primer is below.

Overview
========

Kestrel threat hunting language provides an abstraction for threat hunters to
focus on *what to hunt* instead of *how to hunt*. The abstraction makes it
possible to codify resuable hunting knowledge in a composable and sharable
manner. And Kestrel runtime figures out *how to hunt* for hunters to make cyber
threat hunting less tedious and more efficient.

.. image:: docs/images/overview.png
   :width: 100%
   :alt: Kestrel overview.

- **Kestrel language**: a threat hunting language for a human to express *what to
  hunt*.

  - expressing the knowledge of *what* in patterns, analytics, and hunt flows.
  - composing reusable hunting flows from individual hunting steps.
  - reasoning with human-friendly entity-based data representation abstraction.
  - thinking across heterogeneous data and threat intelligence sources.
  - applying existing public and proprietary detection logic as analytics.
  - reusing and sharing individual hunting steps and entire hunt books.

- **Kestrel runtime**: a machine interpreter that deals with *how to hunt*.

  - compiling the *what* against specific hunting platform instructions.
  - executing the compiled code locally and remotely.
  - assembling raw logs and records into entities for entity-based reasoning.
  - caching intermediate data and related records for fast response.
  - prefetching related logs and records for link construction between entities.
  - defining extensible interfaces for data sources and analytics execution.

Installation
============

Kestrel requires Python 3.x to run. Check `Python installation guide`_ if you
do not have Python. It is preferred to install Kestrel runtime using `pip`_,
and it is preferred to install Kestrel runtime in a `Python virtual
environment`_.

0. Update Python installer.

.. code-block:: console

    $ pip install --upgrade pip setuptools wheel

1. Install Kestrel runtime.

.. code-block:: console

    $ pip install kestrel-lang

2. Install Kestrel Jupyter kernel if you use `Jupyter Notebook`_ to hunt.

.. code-block:: console

    $ pip install kestrel-jupyter
    $ python -m kestrel_jupyter_kernel.setup

3. (Optional) download Kestrel analytics examples for the ``APPLY`` hunt steps.

.. code-block:: console

    $ git clone https://github.com/IBM/kestrel-analytics.git

Hello World Hunt
================

1. Copy the following 3-step hunt flow into your favorite text editor:

.. code-block::

    # create four process entities in Kestrel and store them in the variable `proclist`
    proclist = NEW process [ {"name": "cmd.exe", "pid": "123"}
                           , {"name": "explorer.exe", "pid": "99"}
                           , {"name": "firefox.exe", "pid": "201"}
                           , {"name": "chrome.exe", "pid": "205"}
                           ]

    # match a pattern of browser processes, and put the matched entities in variable `browsers`
    browsers = GET process FROM proclist WHERE [process:name IN ('firefox.exe', 'chrome.exe')]

    # display the information (attributes name, pid) of the entities in variable `browsers`
    DISP browsers ATTR name, pid

2. Save to a file ``helloworld.hf``.

3. Execute the hunt flow in a terminal (in Python venv if virtual environment is used):

.. code-block:: console

    $ kestrel helloworld.hf

Now you captured browser processes in a Kestrel variable ``browsers`` from all processes created:

::
    
           name pid
     chrome.exe 205
    firefox.exe 201

    [SUMMARY] block executed in 1 seconds
    VARIABLE    TYPE  #(ENTITIES)  #(RECORDS)  process*
    proclist process            4           4         0
    browsers process            2           2         0
    *Number of related records cached.

Hunting In The Real World
=========================

#. How to develop hunts interactively in Jupyter Notebook?
#. How to connect to one and more real-world data sources?
#. How to write and match a TTP pattern?
#. How to find child processes of a process?
#. How to find network traffic from a process?
#. How to apply pre-built analytics?
#. How to fork and merge hunt flows?

Find more at `Kestrel documentation hub`_.

Connecting With The Community
=============================

Quick questions? Like to meet other users? Want to contribute? Join our `Kestrel slack workspace`_.

.. _Kestrel documentation hub: https://kestrel.readthedocs.io/
.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/
.. _Python virtual environment: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
.. _Jupyter Notebook: https://jupyter.org/
.. _Kestrel slack workspace: https://kestrel-lang.slack.com/
