******
Andes
******

System Overview
===============

Andes is a replacement for the Rhea system. Andes has 8 login nodes, 704
compute nodes and 9 GPU nodes. The primary purpose of Andes is to provide a
conduit for large-scale scientific discovery via pre/post processing and
analysis of simulation data generated on Summit.  Users with accounts on Summit
will automatically be given access to Andes.

.. _andes-compute-nodes:

Compute nodes
-------------

Andes contains 704 compute nodes and 9 GPU nodes. Andes has two partitions:

+-------------+-------------+---------+-------------------+------------------------------------+
| Partition   | Node Count  | Memory  | GPU               | CPU                                |
+=============+=============+=========+===================+====================================+
| andes       | 704         | 256 GB  | N/A               | [2x] AMD EPYC 7302 16Core Processor|
| (default)   |             |         |                   | 3.0 GHz                            |   
|             |             |         |                   | (total 32 cores *per node*)        |
+-------------+-------------+---------+-------------------+------------------------------------+
| gpu         | 9           | 1 TB    | [2x]              | [2x] Intel\ |R| Xeon\ |R| E5-2695  |
|             |             |         | NVIDIA\ |R|       | @2.3 GHz - 14 cores, 28 HT         |
|             |             |         | K80               | (total 28 cores, 56 HT *per node*) |
+-------------+-------------+---------+-------------------+------------------------------------+

**Andes Partition**

The first 704 nodes make up the *andes* partition, where each node contains two
16-core 3.0 GHz AMD EPYC 7302 processors and 256GB of main memory.  Each CPU in
this partition features 16 physical cores, for a total of 32 physical cores per
node.

**GPU Partition**

Andes also has 9 large memory/GPU nodes, which make up the *gpu* partition.
These nodes each have 1TB of main memory and two NVIDIA K80 GPUs in addition to
two 14-core 2.30 GHz Intel Xeon processors with HT Technology. Each CPU in this
partition features 14 physical cores, for a total of 28 physical cores per
node.  With Hyper-Threading enabled, these nodes have 56 logical cores that can
execute 56 hardware threads for increased parallelism.

.. note::
    To access the gpu partition, batch job submissions should request ``-p gpu``.

Please see the :ref:`batch-queues-on-andes` section to learn about the queuing
policies for these two partitions. Both compute partitions are accessible
through the same batch queue from Andes’s :ref:`andes-login-nodes`.

Andes features a S8500 Series HDR Infiniband interconnect, with a maximum theoretical
transfer rate of 200 Gb/s.

.. _andes-login-nodes:

Login nodes
-----------

Andes features 8 login nodes which are identical to the *andes* partition
compute nodes.  The login nodes provide an environment for editing, compiling,
and launching codes onto the compute nodes. All Andes users will access the
system through these same login nodes, and as such, any CPU- or
memory-intensive tasks on these nodes could interrupt service to other users.
As a courtesy, we ask that you refrain from doing any analysis or visualization
tasks on the login nodes.

To connect to Andes, ssh to andes.ccs.ornl.gov 
::

        ssh username@andes.ccs.ornl.gov

For more information on connecting to OLCF resources, see :ref:`connecting-to-olcf`.

--------------

File systems
------------

The OLCF's center-wide :ref:`alpine-ibm-spectrum-scale-filesystem` name Alpine
is available on Andes for computational work.  An NFS-based file system provides
:ref:`user-home-directories-nfs` and :ref:`project-home-directories-nfs`.
Additionally, the OLCF's :ref:`hpss` provides archival spaces.

Shell and programming environments
==================================

OLCF systems provide hundreds of software packages and scientific libraries
pre-installed at the system-level for users to take advantage of. To facilitate
this, environment management tools are employed to handle necessary changes to
the shell dynamically. The sections below provide information about using the
management tools at the OLCF.

--------------

Default shell
-------------

A user's default shell is selected when completing the user account request
form. The chosen shell is set across all OLCF resources.  Currently, supported
shells include:

-  bash
-  tsch
-  csh
-  ksh

If you would like to have your default shell changed, please contact the
`OLCF user assistance center <https://www.olcf.ornl.gov/for-users/user-assistance/>`__ at
help@olcf.ornl.gov.

--------------

Environment management with lmod
--------------------------------

The *modules* software package allows you to dynamically modify your user
environment by using pre-written *modulefiles*. environment modules are provided
through `Lmod <https://lmod.readthedocs.io/en/latest/>`__, a Lua-based module
system for dynamically altering shell environments.  by managing changes to the
shell’s environment variables (such as ``path``, ``ld_library_path``, and
``pkg_config_path``), Lmod allows you to alter the software available in your
shell environment without the risk of creating package and version combinations
that cannot coexist in a single environment.

Lmod is a recursive environment module system, meaning it is aware of module
compatibility and actively alters the environment to protect against conflicts.
Messages to stderr are issued upon Lmod implicitly altering the environment.
Environment modules are structured hierarchically by compiler family such that
packages built with a given compiler will only be accessible if the compiler
family is first present in the environment.

    **note:** Lmod can interpret both Lua modulefiles and legacy Tcl
    modulefiles. However, long and logic-heavy Tcl modulefiles may require
    porting to Lua.


General usage
^^^^^^^^^^^^^

Typical use of Lmod is very similar to that of interacting with modulefiles on
other OLCF systems. The interface to Lmod is provided by the ``module`` command:

+----------------------------------+-----------------------------------------------------------------------+
| Command                          | Description                                                           |
+==================================+=======================================================================+
| module -t list                   | Shows a terse list of the currently loaded modules.                   |
+----------------------------------+-----------------------------------------------------------------------+
| module avail                     | Shows a table of the currently available modules                      |
+----------------------------------+-----------------------------------------------------------------------+
| module help <modulename>         | Shows help information about <modulename>                             |
+----------------------------------+-----------------------------------------------------------------------+
| module show <modulename>         | Shows the environment changes made by the <modulename> modulefile     |
+----------------------------------+-----------------------------------------------------------------------+
| module spider <string>           | Searches all possible modules according to <string>                   |
+----------------------------------+-----------------------------------------------------------------------+
| module load <modulename> [...]   | Loads the given <modulename>(s) into the current environment          |
+----------------------------------+-----------------------------------------------------------------------+
| module use <path>                | Adds <path> to the modulefile search cache and ``MODULESPATH``        |
+----------------------------------+-----------------------------------------------------------------------+
| module unuse <path>              | Removes <path> from the modulefile search cache and ``MODULESPATH``   |
+----------------------------------+-----------------------------------------------------------------------+
| module purge                     | Unloads all modules                                                   |
+----------------------------------+-----------------------------------------------------------------------+
| module reset                     | Resets loaded modules to system defaults                              |
+----------------------------------+-----------------------------------------------------------------------+
| module update                    | Reloads all currently loaded modules                                  |
+----------------------------------+-----------------------------------------------------------------------+

.. note::
    Modules are changed recursively. Some commands, such as
    ``module swap``, are available to maintain compatibility with scripts
    using Tcl Environment Modules, but are not necessary since Lmod
    recursively processes loaded modules and automatically resolves
    conflicts.

Searching for modules
^^^^^^^^^^^^^^^^^^^^^

Modules with dependencies are only available when the underlying dependencies,
such as compiler families, are loaded. Thus, ``module avail`` will only display
modules that are compatible with the current state of the environment. To search
the entire hierarchy across all possible dependencies, the ``spider``
sub-command can be used as summarized in the following table.

+----------------------------------------+------------------------------------------------------------------------------------+
| Command                                | Description                                                                        |
+========================================+====================================================================================+
| module spider                          | Shows the entire possible graph of modules                                         |
+----------------------------------------+------------------------------------------------------------------------------------+
| module spider <modulename>             | Searches for modules named <modulename> in the graph of possible modules           |
+----------------------------------------+------------------------------------------------------------------------------------+
| module spider <modulename>/<version>   | Searches for a specific version of <modulename> in the graph of possible modules   |
+----------------------------------------+------------------------------------------------------------------------------------+
| module spider <string>                 | Searches for modulefiles containing <string>                                       |
+----------------------------------------+------------------------------------------------------------------------------------+

 
Defining custom module collections
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Lmod supports caching commonly used collections of environment modules on a
per-user basis in ``$home/.lmod.d``. to create a collection called "NAME" from
the currently loaded modules, simply call ``module save NAME``. omitting "NAME"
will set the user’s default collection. Saved collections can be recalled and
examined with the commands summarized in the following table.

+-------------------------+----------------------------------------------------------+
| Command                 | Description                                              |
+=========================+==========================================================+
| module restore NAME     | Recalls a specific saved user collection titled "NAME"   |
+-------------------------+----------------------------------------------------------+
| module restore          | Recalls the user-defined defaults                        |
+-------------------------+----------------------------------------------------------+
| module reset            | Resets loaded modules to system defaults                 |
+-------------------------+----------------------------------------------------------+
| module restore system   | Recalls the system defaults                              |
+-------------------------+----------------------------------------------------------+
| module savelist         | Shows the list user-defined saved collections            |
+-------------------------+----------------------------------------------------------+

.. note::
    You should use unique names when creating collections to
    specify the application (and possibly branch) you are working on. For
    example, ``app1-development``, ``app1-production``, and
    ``app2-production``.

.. note::
    In order to avoid conflicts between user-defined collections
    on multiple compute systems that share a home file system (e.g.
    ``/ccs/home/[username]``), lmod appends the hostname of each system to the
    files saved in in your ``~/.lmod.d`` directory (using the environment
    variable ``lmod_system_name``). This ensures that only collections
    appended with the name of the current system are visible.

The following screencast shows an example of setting up user-defined module
collections on Summit. https://vimeo.com/293582400

--------------

Installed Software
------------------

The OLCF provides hundreds of pre-installed software packages and scientific
libraries for your use, in addition to taking `software installation requests
<https://www.olcf.ornl.gov/support/software/software-request/>`__. See the
`software <https://www.olcf.ornl.gov/for-users/software/>`__ page for complete
details on existing installs.

Compiling
=========

Compiling code on andes is typical of commodity or beowulf-style hpc linux
clusters.

Available compilers
-------------------

The following compilers are available on andes:

- `intel <https://www.olcf.ornl.gov/software_package/intel/>`__, intel composer xe (default)
- `pgi <https://www.olcf.ornl.gov/software_package/pgi/>`__, the portland group compilar suite
- `gcc <https://www.olcf.ornl.gov/software_package/gcc/>`__, the gnu compiler collection

Upon login, default versions of the intel compiler and openmpi (message passing
interface) libraries are automatically added to each user's environment. Users
do not need to make any environment changes to use the default version of intel
and openmpi.

--------------

Changing compilers
------------------

If a different compiler is required, it is important to use the correct
environment for each compiler. To aid users in pairing the correct compiler and
environment, the module system on andes automatically pulls in libraries compiled
with a given compiler when changing compilers. The compiler modules will load
the correct pairing of compiler version, message passing libraries, and other
items required to build and run code. To change the default loaded intel
environment to the gcc environment for example, use:

.. code::

    $ module load gcc

This will automatically unload the current compiler and system libraries
associated with it, load the new compiler environment and automatically load
associated system libraries as well.

Changing versions of the same compiler
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To use a specific compiler *version*, you must first ensure the compiler's
module is loaded, and *then* swap to the correct compiler version. For example,
the following will configure the environment to use the gcc compilers, then load
a non-default gcc compiler version:

.. code::

    $ module load gcc
    $ module swap gcc gcc/4.7.1

..

    **note: we recommend the following general guidelines for using the
    programming environment modules:**

    -  Do not purge all modules; rather, use the default module environment
       provided at the time of login, and modify it.
    -  Do not swap moab, torque, or mysql modules after loading a
       programming environment modulefile.

--------------

Compiler wrappers
-----------------

Commodity clusters at the olcf can be accessed via the following wrapper
programs:

-  ``mpicc`` to invoke the c compiler
-  ``mpicc``, ``mpicxx``, or ``mpic++`` to invoke the c++ compiler
-  ``mpif77`` or ``mpif90`` to invoke appropriate versions of the
   fortran compiler

These wrapper programs are cognizant of your currently loaded modules, and will
ensure that your code links against our openmpi installation.  more information
about using openmpi at our center can be found in our `software documentation
<https://www.olcf.ornl.gov/software_package/openmpi/>`__.

Compiling threaded codes
------------------------

When building threaded codes, compiler-specific flags must be included to ensure
a proper build.

Openmp
^^^^^^

For pgi, add "-mp" to the build line.

.. code::

    $ mpicc -mp test.c -o test.x
    $ export OMP_NUM_THREADS=2

For gnu, add "-fopenmp" to the build line.

.. code::

    $ mpicc -fopenmp test.c -o test.x
    $ export OMP_NUM_THREADS=2

For intel, add "-qopenmp" to the build line.

.. code::

    $ mpicc -qopenmp test.c -o test.x
    $ export OMP_NUM_THREADS=2

For information on *running threaded codes*, please see the :ref:`andes-thread-layout`
subsection of the :ref:`andes-running-jobs` section in this user guide.

.. _andes-running-jobs:

Running Jobs
============

In High Performance Computing (HPC), computational work is performed by *jobs*.
Individual jobs produce data that lend relevant insight into grand challenges in
science and engineering. As such, the timely, efficient execution of jobs is the
primary concern in the operation of any HPC system.

A job on a commodity cluster typically comprises a few different components:

-  A batch submission script.
-  A binary executable.
-  A set of input files for the executable.
-  A set of output files created by the executable.

And the process for running a job, in general, is to:

#. Prepare executables and input files.
#. Write a batch script.
#. Submit the batch script to the batch scheduler.
#. Optionally monitor the job before and during execution.

The following sections describe in detail how to create, submit, and manage jobs
for execution on commodity clusters.

--------------

Login vs Compute Nodes on Commodity Clusters
--------------------------------------------

Login Nodes
^^^^^^^^^^^

When you log into an OLCF cluster, you are placed on a *login* node.  Login node
resources are shared by all users of the system. Because of this, users should
be mindful when performing tasks on a login node.

Login nodes should be used for basic tasks such as file editing, code
compilation, data backup, and job submission. Login nodes should *not* be used
for memory- or compute-intensive tasks. Users should also limit the number of
simultaneous tasks performed on the login resources. For example, a user should
not run (10) simultaneous ``tar`` processes on a login node.

.. warning::
    Compute-intensive, memory-intensive, or otherwise disruptive processes
    running on login nodes may be killed without warning.



Slurm
-----

Most OLCF resources now use the Slurm batch scheduler. Previously, most OLCF resources
used the Moab scheduler. Summit and other IBM hardware use the LSF scheduler.
Below is a comparison table of useful commands among the three schedulers.

+--------------------------------------------+-----------------------+-------------------+
| Task                                       | LSF (Summit)          | Slurm             |
+============================================+=======================+===================+
| View batch queue                           | ``jobstat``           | ``squeue``        |
+--------------------------------------------+-----------------------+-------------------+
| Submit batch script                        | ``bsub``              | ``sbatch``        |
+--------------------------------------------+-----------------------+-------------------+
| Submit interactive batch job               | ``bsub -Is $SHELL``   | ``salloc``        |
+--------------------------------------------+-----------------------+-------------------+
| Run parallel code within batch job         | ``jsrun``             | ``srun``          |
+--------------------------------------------+-----------------------+-------------------+


Writing Batch Scripts
^^^^^^^^^^^^^^^^^^^^^

Batch scripts, or job submission scripts, are the mechanism by which a user
configures and submits a job for execution. A batch script is simply a shell
script that also includes commands to be interpreted by the batch scheduling
software (e.g. Slurm).

Batch scripts are submitted to the batch scheduler, where they are then parsed
for the scheduling configuration options. The batch scheduler then places the
script in the appropriate queue, where it is designated as a batch job. Once the
batch jobs makes its way through the queue, the script will be executed on the
primary compute node of the allocated resources.

Components of a Batch Script
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Batch scripts are parsed into the following (3) sections:

Interpreter Line
""""""""""""""""

The first line of a script can be used to specify the script’s interpreter; this
line is optional. If not used, the submitter’s default shell will be used. The
line uses the *hash-bang* syntax, i.e., ``#!/path/to/shell``.

Slurm Submission Options
""""""""""""""""""""""""

The Slurm submission options are preceded by the string ``#SBATCH``, making them
appear as comments to a shell. Slurm will look for ``#SBATCH`` options in a
batch script from the script’s first line through the first non-comment line. A
comment line begins with ``#``. ``#SBATCH`` options entered after the first
non-comment line will not be read by Slurm.

Shell Commands
""""""""""""""

The shell commands follow the last ``#SBATCH`` option and represent the
executable content of the batch job. If any ``#SBATCH`` lines follow executable
statements, they will be treated as comments only.

The execution section of a script will be interpreted by a shell and can contain
multiple lines of executables, shell commands, and comments.  when the job's
queue wait time is finished, commands within this section will be executed on
the primary compute node of the job's allocated resources. Under normal
circumstances, the batch job will exit the queue after the last line of the
script is executed.

Example Batch Script
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash
   :linenos:

   #!/bin/bash
   #SBATCH -A XXXYYY
   #SBATCH -J test
   #SBATCH -N 2
   #SBATCH -t 1:00:00

   cd $SLURM_SUBMIT_DIR
   date
   srun -n 8 ./a.out

This batch script shows examples of the three sections outlined above:

Interpreter Line
""""""""""""""""

1: This line is optional and can be used to specify a shell to interpret the
script. In this example, the bash shell will be used.

Slurm Options
"""""""""""""

2: The job will be charged to the “XXXYYY” project.

3: The job will be named test.

4: The job will request (2) nodes.

5: The job will request (1) hour walltime.

Shell Commands
""""""""""""""

6: This line is left blank, so it will be ignored.

7: This command will change the current directory to the directory
from where the script was submitted.

8: This command will run the date command.

9: This command will run (8) MPI instances of the executable a.out
on the compute nodes allocated by the batch system.


Batch scripts can be submitted for execution using the ``sbatch`` command.
For example, the following will submit the batch script named ``test.slurm``:

.. code::

      sbatch test.slurm

If successfully submitted, a Slurm job ID will be returned. This ID can be used
to track the job. It is also helpful in troubleshooting a failed job; make a
note of the job ID for each of your jobs in case you must contact the `OLCF User
Assistance Center for support
<https://www.olcf.ornl.gov/for-users/user-assistance/>`__.



--------------

Interactive Batch Jobs on Commodity Clusters
--------------------------------------------

Batch scripts are useful when one has a pre-determined group of commands to
execute, the results of which can be viewed at a later time. However, it is
often necessary to run tasks on compute resources interactively.

Users are not allowed to access cluster compute nodes directly from a login
node. Instead, users must use an *interactive batch job* to allocate and gain
access to compute resources. This is done by using the Slurm ``salloc`` command.
Other Slurm options are passed to ``salloc`` on the command line as well:

.. code::

      $ salloc -A abc123 -p gpu -N 4 -t 1:00:00

This request will:

+----------------------------+----------------------------------------------------------------+
| ``salloc``                 | Start an interactive session                                   |
+----------------------------+----------------------------------------------------------------+
| ``-A``                     | Charge to the ``abc123`` project                               |
+----------------------------+----------------------------------------------------------------+
| ``-p gpu``                 | Run in the ``gpu`` partition                                   |
+----------------------------+----------------------------------------------------------------+
| ``-N 4``                   | request (4) nodes...                                           |
+----------------------------+----------------------------------------------------------------+
| ``-t 1:00:00``             | ...for (1) hour                                                |
+----------------------------+----------------------------------------------------------------+

After running this command, the job will wait until enough compute nodes are
available, just as any other batch job must. However, once the job starts, the
user will be given an interactive prompt on the primary compute node within the
allocated resource pool. Commands may then be executed directly (instead of
through a batch script).

Debugging
^^^^^^^^^

A common use of interactive batch is to aid in debugging efforts.  interactive
access to compute resources allows the ability to run a process to the point of
failure; however, unlike a batch job, the process can be restarted after brief
changes are made without losing the compute resource pool; thus speeding up the
debugging effort.

Choosing a Job Size
^^^^^^^^^^^^^^^^^^^

Because interactive jobs must sit in the queue until enough resources become
available to allocate, it is useful to know when a job can start.

Use the ``sbatch --test-only`` command to see when a job of a specific size
could be scheduled. For example, the snapshot below shows that a (2) node job
would start at 10:54.

.. code::

    $ sbatch --test-only -N2 -t1:00:00 batch-script.slurm

      sbatch: Job 1375 to start at 2019-08-06T10:54:01 using 64 processors on nodes andes[499-500] in partition batch

.. note::
    The queue is fluid, the given time is an estimate made from the current queue state and load. Future job submissions and job
    completions will alter the estimate.

--------------

Common Batch Options to Slurm
-----------------------------

The following table summarizes frequently-used options to Slurm:

+------------------+-----------------------------------+-----------------------------------------------------------+
| Option           | Use                               | Description                                               |
+==================+===================================+===========================================================+
| -A               | #SBATCH -A <account>              | Causes the job time to be charged to ``<account>``.       |
|                  |                                   | The account string, e.g. ``pjt000`` is typically composed |
|                  |                                   | of three letters followed by three digits and optionally  |
|                  |                                   | followed by a subproject identifier. The utility          |
|                  |                                   | ``showproj`` can be used to list your valid assigned      |
|                  |                                   | project ID(s). This option is required by all jobs.       |
+------------------+-----------------------------------+-----------------------------------------------------------+
| -N               | #SBATCH -N <value>                | Number of compute nodes to allocate.                      |
|                  |                                   | Jobs cannot request partial nodes.                        |
+------------------+-----------------------------------+-----------------------------------------------------------+
|                  | #SBATCH -t <time>                 | Maximum wall-clock time. ``<time>`` is in the             |
|                  |                                   | format HH:MM:SS.                                          |
+------------------+-----------------------------------+-----------------------------------------------------------+
|                  | #SBATCH -p <partition_name>       | Allocates resources on specified partition.               |
+------------------+-----------------------------------+-----------------------------------------------------------+
| -o               | #SBATCH -o <filename>             | Writes standard output to ``<name>`` instead of           |
|                  |                                   | ``<job_script>.o$SLURM_JOB_UID``. ``$SLURM_JOB_UID``      |
|                  |                                   | is an environment variable created by Slurm that          |
|                  |                                   | contains the batch job identifier.                        |
+------------------+-----------------------------------+-----------------------------------------------------------+
| -e               | #SBATCH -e <filename>             | Writes standard error to ``<name>`` instead               |
|                  |                                   | of ``<job_script>.e$SLURM_JOB_UID``.                      |
+------------------+-----------------------------------+-----------------------------------------------------------+
| \\-\\-mail-type  | #SBATCH \\-\\-mail-type=FAIL      | Sends email to the submitter when the job fails.          |
+------------------+-----------------------------------+-----------------------------------------------------------+
|                  | #SBATCH \\-\\-mail-type=BEGIN     | Sends email to the submitter when the job begins.         |
+------------------+-----------------------------------+-----------------------------------------------------------+
|                  | #SBATCH \\-\\-mail-type=END       | Sends email to the submitter when the job ends.           |
+------------------+-----------------------------------+-----------------------------------------------------------+
| \\-\\-mail-user  | #SBATCH \\-\\-mail-user=<address> | Specifies email address to use for                        |
|                  |                                   | ``--mail-type`` options.                                  |
+------------------+-----------------------------------+-----------------------------------------------------------+
| -J               | #SBATCH -J <name>                 | Sets the job name to ``<name>`` instead of the            |
|                  |                                   | name of the job script.                                   |
+------------------+-----------------------------------+-----------------------------------------------------------+
|\\-\\-get-user-env| #SBATCH \\-\\-get-user-env        | Exports all environment variables from the                |
|                  |                                   | submitting shell into the batch job shell.                |
|                  |                                   | Since the login nodes differ from the service             |
|                  |                                   | nodes, using the ``–get-user-env`` option is              |
|                  |                                   | **not recommended**. Users should create the              |
|                  |                                   | needed environment within the batch job.                  |
+------------------+-----------------------------------+-----------------------------------------------------------+
| \\-\\-mem=0      | #SBATCH \\-\\-mem=0               | Declare to use all the available memory of the node       |
+------------------+-----------------------------------+-----------------------------------------------------------+

.. note::
    Because the login nodes differ from the service nodes, using
    the ``–get-user-env`` option is not recommended. Users should create the
    needed environment within the batch job.

Further details and other Slurm options may be found through the ``sbatch`` man
page.

--------------

Batch Environment Variables
---------------------------

Slurm sets multiple environment variables at submission time. The following
Slurm variables are useful within batch scripts:

+--------------------------+-------------------------------------------------------+
| Variable                 | Description                                           |
+==========================+=======================================================+
|                          | The directory from which the batch job was submitted. |
|                          | By default, a new job starts in your home directory.  |
| ``$SLURM_SUBMIT_DIR``    | You can get back to the directory of job submission   |
|                          | with ``cd $SLURM_SUBMIT_DIR``. Note that this is not  |
|                          | necessarily the same directory in which the batch     |
|                          | script resides.                                       |
+--------------------------+-------------------------------------------------------+
|                          | The job’s full identifier. A common use for           |
| ``$SLURM_JOBID``         | ``SLURM_JOBID`` is to append the job’s ID to          |
|                          | the standard output and error files.                  |
+--------------------------+-------------------------------------------------------+
| ``$SLURM_JOB_NUM_NODES`` | The number of nodes requested.                        |
+--------------------------+-------------------------------------------------------+
| ``$SLURM_JOB_NAME``      | The job name supplied by the user.                    |
+--------------------------+-------------------------------------------------------+
| ``$SLURM_NODELIST``      | The list of nodes assigned to the job.                |
+--------------------------+-------------------------------------------------------+

--------------

Modifying Batch Jobs
--------------------

The batch scheduler provides a number of utility commands for managing
submitted jobs. See each utilities' man page for more information.

Removing and Holding Jobs
^^^^^^^^^^^^^^^^^^^^^^^^^

``scancel``


Jobs in the queue in any state can be stopped and removed from the queue
using the command ``scancel``.

.. code::

    $ scancel 1234

``scontrol hold``


Jobs in the queue in a non-running state may be placed on hold using the
``scontrol hold`` command. Jobs placed on hold will not be removed from the
queue, but they will not be eligible for execution.

.. code::

    $ scontrol hold 1234

``scontrol release``


Once on hold the job will not be eligible to run until it is released to
return to a queued state. The ``scontrol release`` command can be used to
remove a job from the held state.

.. code::

    $ scontrol release 1234

--------------

Monitoring Batch Jobs
---------------------

Slurm provides multiple tools to view queue, system, and job status. Below are
the most common and useful of these tools.

Job Monitoring Commands
^^^^^^^^^^^^^^^^^^^^^^^

``squeue``
""""""""""

The Slurm utility ``squeue`` can be used to view the batch queue.

To see all jobs currently in the queue:

.. code::

    $ squeue -l

To see all of your queued jobs:

.. code::

    $ squeue -l -u $USER

``sacct``
"""""""""

The Slurm utility ``sacct`` can be used to view jobs currently in the queue and
those completed within the last few days. The utility can also be used to see
job steps in each batch job.


To see all jobs currently in the queue:

.. code::

    $ sacct -a -X


To see all jobs including steps owned by userA currently in the queue:

.. code::

    $ sacct -u userA

To see all steps submitted to job 123:

.. code::

    $ sacct -j 123

To see all of your jobs that completed on 2019-06-10:

.. code::

    $ sacct -S 2019-06-10T00:00:00 -E 2019-06-10T23:59:59 -o"jobid,user,account%16,cluster,AllocNodes,Submit,Start,End,TimeLimit" -X -P


``scontrol show job <jobid>``
"""""""""""""""""""""""""""

Provides additional details of given job.

``sview``
""""""""""

The ``sview`` tool provide a graphical queue monitoring tool. To use, you will
need an X server running on your local system. You will also need to tunnel X
traffic through your ssh connection:

.. code::

    local-system> ssh -Y username@andes.ccs.ornl.gov
    andes-login> sview

--------------

Job Execution
-------------

Once resources have been allocated through the batch system, users have the
option of running commands on the allocated resources' primary compute node (a
serial job) and/or running an MPI/OpenMP executable across all the resources in
the allocated resource pool simultaneously (a parallel job).

Serial Job Execution
^^^^^^^^^^^^^^^^^^^^

The executable portion of batch scripts is interpreted by the shell specified on
the first line of the script. If a shell is not specified, the submitting user’s
default shell will be used.

The serial portion of the batch script may contain comments, shell commands,
executable scripts, and compiled executables. These can be used in combination
to, for example, navigate file systems, set up job execution, run serial
executables, and even submit other batch jobs.

Andes Compute Node Description
"""""""""""""""""""""""""""""

The following image represents a high level compute node that will be used below
to display layout options.

.. image:: /images/Andes-Node-Description.jpg
   :align: center

.. note::
    0 and 32 are on the same physical core.

Using ``srun``
""""""""""""""

By default, commands will be executed on the job’s primary compute node,
sometimes referred to as the job’s head node. The ``srun`` command is used to
execute an MPI binary on one or more compute nodes in parallel.

``srun`` accepts the following common options:

+----------------------+---------------------------------------+
| ``-N``               | Minimum number of nodes               |
+----------------------+---------------------------------------+
| ``-n``               | Total number of MPI tasks             |
+----------------------+---------------------------------------+
| ``--cpu-bind=no``    | Allow code to control thread affinity |
+----------------------+---------------------------------------+
| ``-c``               | Cores per MPI task                    |
+----------------------+---------------------------------------+
| ``--cpu-bind=cores`` | Bind to cores                         |
+----------------------+---------------------------------------+

.. note::
    If you do not specify the number of MPI tasks to ``srun``
    via ``-n``, the system will default to using only one task per node.


MPI Task Layout
"""""""""""""""""

Each compute node on Rhea contains two sockets each with 8 cores.  Depending on
your job, it may be useful to control task layout within and across nodes.

Physical Core Binding
"""""""""""""""""""""

The following will run four copies of a.out, one per CPU, two per node with
physical core binding

.. image:: /images/Andes-layout-physical-core-1-per-CPU.jpg
   :align: center

Hyper Thread Binding
""""""""""""""""""""
The following will run four copies of a.out, one per hyper-thread, two per node
using a round robin task layout between nodes:

.. image:: /images/Andes-layout-1-per-hyper-thread-cyclic.jpg
   :align: center

.. _andes-thread-layout:

Thread Layout
"""""""""""""
**Thread per Hyper-Thread**

The following will run four copies of a.out. Each task will launch two threads.
The ``-c`` flag will provide room for the threads.

.. image:: /images/Andes-layout-thread-per-hyperthread.jpg
   :align: center

.. warning::
    Not adding enough resources using the ``-c`` flag,
    threads may be placed on the same resource.

Multiple Simultaneous Jobsteps
""""""""""""""""""""""""""""""

Multiple simultaneous sruns can be executed within a batch job by placing each
``srun`` in the background.

.. code-block:: bash
   :linenos:

   #!/bin/bash
   #SBATCH -N 2
   #SBATCH -t 1:00:00
   #SBATCH -A prj123
   #SBATCH -J simultaneous-jobsteps

   srun -n16 -N2 -c1 --cpu-bind=cores --exclusive ./a.out &
   srun -n8 -N2 -c1 --cpu-bind=cores --exclusive ./b.out &
   srun -n4 -N1 -c1 --cpu-bind=threads --exclusive ./c.out &
   wait

.. note::
    The ``wait`` command must be used in a batch script
    to prevent the shell from exiting before all backgrounded
    sruns have completed.

.. warning::
    The ``--exclusive`` flag must be used to prevent
    resource sharing. Without the flag each backgrounded srun
    will likely be placed on the same resources.

.. _batch-queues-on-andes:

