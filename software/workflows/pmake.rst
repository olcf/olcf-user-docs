.. _workflows-pmake:

*****
pmake
*****


Overview
========

`pmake <https://code.ornl.gov/99R/pmake>`_ is a parallel
make developed for use within batch jobs.  A ``rules.yaml``
file specifies extended make-rules with:

 * multiple input and multiple output files

 * a resource-set specification

 * a multi-line shell script that can use variable
   substitution (e.g. ``{mpirun}`` expands to
   ``{jsrun -g -c ...}`` on summit).

Full documentation and examples are available
in `<https://code.ornl.gov/99R/pmake>`_.


Prerequisites
================

pmake is a standard python package.  It is recommended
to install it in a virtual environment.  One easy
way to create a virtual environment is to load an available
python module, and then put a new environment into ``/ccs/proj/<projid>/<systemname>``.  This way, the project can share environments, and each system
gets its own install location.


.. code-block:: console

   $ module load python/3.8-anaconda3
   $ python -m venv /path/to/new-venv
   $ source /path/to/new-venv/bin/activate

On subsequent logins, remember to load the same python module
and run the ``source /path/to/new-venv/bin/activate`` command
again.


Once you have entered the virtual environment, pmake can be installed
with:

.. code-block:: console

    $ python -m pip install git+https://code.ornl.gov/99R/pmake.git@latest

Run the following command to verify that pmake is available:

.. code-block:: console

    $ pmake --help


Hello world!
============

To run a pmake demo on Summit, you will create a ``pmake-example``
directory with its preferred file layout, then submit
a batch job to LSF from a Summit login node.

First, create the directories,

.. code-block:: console

   $ mkdir -p pmake-example/simulation


Next, create pmake's two configuration files, ``rules.yaml``
and ``targets.yaml``:

.. code-block:: yaml

    # pmake-example/targets.yaml

    simulation:
      dirname: simulation # request simulation/run.log to be created
      out:
        - run.log

    #... additional directories here

.. code-block:: yaml

    # pmake-example/rules.yaml
  
    simulate:
       resource:
          cpu: 1 # number of CPUs per resource set
          gpu: 0 # number of GPUs per resource set
          nrs: 1 # number of resource sets to request
          time: 3 # minutes
       inp: [] # empty list of input files - no inputs required
       # Declare a list of output files, (same as "out: [run.log]").
       out:
         - run.log
       # The | character here creates a multi-line string.
       script: |
         {mpirun} seq 4 >run.log

    #... additional rules here

To check the syntax of your files, cd into the ``pmake-example``
directory and run ``pmake --test``.
It should show the commands that would
be run if pmake were being executed inside a job-script.


Finally, create an LSF batch script called ``pmake.lsf``,
fix the python module and virtual environment path to match
your installation above, and change
``abc123`` to match your own project identifier:

.. code-block:: bash

    #BSUB -P abc123
    #BSUB -W 10
    #BSUB -nnodes 1

    #BSUB -J pmake_demo
    #BSUB -o pmake.o%J
    #BSUB -e pmake.e%J

    module load python/3.8-anaconda3
    source /path/to/new-venv/bin/activate

    pmake rules.yaml targets.yaml 8
    # Note the 8 here is a time-limit on launching new rules
    # to 8 minutes.  This prevents launching job steps
    # that are not likely to complete before the job time-limit.
    # (Note: this example -W 10 requests 10 minutes total)

Finally, submit the batch job to LSF by executing the
following command from a login node:

.. code-block:: console

    $ bsub pmake.lsf

When the job completes, you will
see pmake explain what rules it launched, completed, or errored
in pmake.oNNN, where NNN is your job ID.

Inside the simulation directory, you should see 3 new files,
``simulate.sh``, which contains the shell script pmake built
from the ``simulate`` rule, ``simulate.log``, containing the
log output from running ``simulate.sh``, and ``run.log``,
the file written during rule execution.

Extending pmake using your own rules is straightforward.
pmake acts like make, running rules to create output
files (that do not yet exist) from input files
(that must exist before the rule is run).

Unlike make, pmake does not run a rule unless its
output is requested by some target.
