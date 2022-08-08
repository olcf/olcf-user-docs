.. _workflows-fireworks:

*********
FireWorks
*********


Overview
========

FireWorks is a free, open-source tool for defining, managing, and executing
workflows. Complex workflows can be defined using Python, JSON, or YAML, are
stored using MongoDB, and can be monitored through a built-in web interface.
Workflow execution can be automated over arbitrary computing resources,
including those that have a queueing system. FireWorks has been used to run
millions of workflows encompassing tens of millions of CPU-hours across diverse
application areas and in long-term production projects over the span of
multiple years.

To learn more about FireWorks, please refer to its extensive online
`documentation <https://materialsproject.github.io/fireworks/>`__.


Prerequisites
================

Before using FireWorks itself, you will need a MongoDB service running
on :ref:`Slate<slate>`. A tutorial to deploy MongoDB is available in the
Slate `documentation <https://docs.olcf.ornl.gov/services_and_applications/slate/use_cases/mongodb_service.html>`__.

You will need to know the connection information for both MongoDB so that
FireWorks can be configured to connect to it.

Then, to use FireWorks on Summit, load the module as shown below:

.. code-block:: console

    $ module load workflows
    $ module load fireworks/2.0.2

Run the following command to verify that FireWorks is available:

.. code-block:: console

    $ rlaunch -v
    rlaunch v2.0.2


Hello world!
============

To run this FireWorks demo on Summit, you will create a Python file and then
submit it as a batch job to LSF from a Summit node.

The contents for ``demo.py`` follow:

.. code-block:: python

    import os
  
    from fireworks import Firework, Workflow, LaunchPad, ScriptTask
    from fireworks.core.rocket_launcher import rapidfire

    # Set up and reset the LaunchPad using MongoDB URI string.
    launchpad = LaunchPad(host = os.getenv("MONGODB_URI"), uri_mode = True)
    launchpad.reset('', require_password=False)

    # Create the individual FireWorks and Workflow.
    fw1 = Firework(ScriptTask.from_str('echo "hello"'), name = "hello")
    fw2 = Firework(ScriptTask.from_str('echo "goodbye"'), name = "goodbye")
    wf = Workflow([fw1, fw2], {fw1: fw2}, name = "test workflow")

    # Store workflow and launch it locally.
    launchpad.add_wf(wf)
    rapidfire(launchpad)


Finally, create an LSF batch script called ``fireworks_demo.lsf``, and
change ``abc123`` to match your own project identifier:

.. code-block:: bash

    #BSUB -P abc123
    #BSUB -W 10
    #BSUB -nnodes 1

    #BSUB -J fireworks_demo
    #BSUB -o fireworks_demo.o%J
    #BSUB -e fireworks_demo.e%J

    module load workflows
    module load fireworks/2.0.2

    # Edit the following line to match your own MongoDB connection string.
    export MONGODB_URI="mongodb://admin:password@apps.marble.ccs.ornl.gov:32767/test"

    jsrun -n 1 python3 demo.py


Finally, submit the batch job to LSF by executing the following command from a
Summit login node:

.. code-block:: console

    $ bsub fireworks_demo.lsf

Congratulations! Once the batch job completes, you will find new directories
beginning with ``launcher_`` and containing ``FW.json`` files that detail
exactly what happened.


