.. _workflows-entk:

***********************
Ensemble Toolkit (EnTK)
***********************


Overview
========

The Ensemble Toolkit (EnTK) is a Python library developed by the RADICAL
Research Group at Rutgers University for developing and executing large-scale
ensemble-based workflows. This tutorial shows how to get up and running with
EnTK 1.13.0 on Summit specifically. For in-depth information about EnTK itself,
please refer to its
`documentation <https://radicalentk.readthedocs.io/en/stable/>`_.


Prerequisites
=============

Before using EnTK itself, you will need `MongoDB <https://www.mongodb.com/>`_
and `RabbitMQ <https://www.rabbitmq.com/>`_ services running on
:ref:`Slate<slate>`. There are tutorials for MongoDB in this documentation,
but the tutorial for RabbitMQ is forthcoming.

You will need to know the connection information for both MongoDB and RabbitMQ
so that EnTK can be configured to connect to the services.

Then, to use EnTK on Summit, load the module as shown below:

.. code-block:: console

    $ module load entk/1.80.0

Run the following command to verify that EnTK is available:

.. code-block:: console

    $ radical-utils-version
    5d086a

Hello world!
============

To run EnTK on Frontier, you will create two files and then execute two commands
from a login node. Currently, EnTK must be run from a login node,
rather than within a batch job.

First, create a setup file ``setup.bash`` that will load the correct modules and
define environment variables.

.. code-block:: bash

    module load entk/1.80.0

    export RADICAL_PILOT_DBURL="mongodb://admin:password@apps.marble.ccs.ornl.gov:32767/test"
    export RMQ_HOSTNAME="apps.marble.ccs.ornl.gov"
    export RMQ_PORT="30256"
    export RMQ_USERNAME="admin"
    export RMQ_PASSWORD="password"

Replace, without renaming, the ``RADICAL_PILOT_DBURL`` environment variable in
``setup.bash`` with the MongoDB connection string that corresponds to your own
service running on Slate. EnTK uses this environment variable directly.

Then, replace the ``RMQ_`` variables in ``setup.bash`` with the corresponding
values for your RabbitMQ service on Slate. These variables can be renamed,
because their only use is in the following example Python program.

Now, create a ``demo.py3`` file with the following lines:

.. code-block:: python

    import os
    from radical.entk import AppManager, Pipeline, Stage, Task

    # Create objects.

    appman = AppManager(
        hostname=os.environ["RMQ_HOSTNAME"],
        port=int(os.environ["RMQ_PORT"]),
        username=os.environ["RMQ_USERNAME"],
        password=os.environ["RMQ_PASSWORD"])

    p = Pipeline()

    s = Stage()

    t = Task()

    # Use the objects to model the workflow.

    appman.resource_desc = {
        "resource": "ornl.frontier",
        "walltime": 10,
        "cpus":     1,
        "project":  "abc123" # replace with your own project identifier
    }

    t.name = "mytask"
    t.executable = "/bin/echo"
    t.arguments = ["Hello world!"]

    s.add_tasks(t)

    p.add_stages(s)

    appman.workflow = set([p])

    # Execute the workflow.

    appman.run()

In ``demo.py3``, only one line needs to be changed, so that EnTK knows which
project identifier to use when submitting batch jobs to Summit.

Finally, run the demo program by executing the following commands from a Summit
login node:

.. code-block:: console

    $ source setup.bash
    $ python3 demo.py3

Congratulations! You should now see interactive output from EnTK while it
launches and monitors your job on Frontier.


