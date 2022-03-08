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

To learn more about FireWorks, refer to its extensive online `documentation <https://materialsproject.github.io/fireworks/>`_.


FireWorks on Summit
===================

In order to use FireWorks on Summit, use the FireWorks module as shown below:

.. code-block:: console

    $ module load workflows
    $ module load fireworks/2.0.2

Now, FireWorks should be available to use. Run the following command as a quick verification:

.. code-block:: console

    $ rlaunch -v

