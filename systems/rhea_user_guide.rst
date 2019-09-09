*********************
Rhea User Guide
*********************

Overview
=========

Rhea is a 521-node commodity-type linux cluster. The primary purpose of
rhea is to provide a conduit for large-scale scientific discovery via
pre/post processing and analysis of simulation data generated on Summit.
Users with accounts on Summit will automatically be given access to rhea.

Compute nodes
-------------

.. include:: includes/rhea-compute-nodes.txt

Login nodes
-----------

Rhea features (4) login nodes which are identical to the compute nodes,
but with 64gb of ram. The login nodes provide an environment for
editing, compiling, and launching codes onto the compute nodes. All rhea
users will access the system through these same login nodes, and as
such, any cpu- or memory-intensive tasks on these nodes could interrupt
service to other users. As a courtesy, we ask that you refrain from
doing any analysis or visualization tasks on the login nodes.

--------------

File systems
------------

The olcf's center-wide lustre\ :sup:`®` file system, named
`spider <../file-systems/#spider-the-centerwide-lustre-file-system>`_,
is available on rhea for computational work. With over 26,000 clients
and (32) pb of disk space, it is one of the largest-scale
lustre\ :sup:`®` file systems in the world. A nfs-based file system
provides `user home storage
areas <../file-systems/#user-home-directories-nfs>`__ and `project home
storage areas <../file-systems/#project-home-directories-nfs>`__.
additionally, the olcf's `high performance storage
system <../file-systems/#hpss-high-performance-storage-system>`__ (hpss)
provides archival spaces.

Compiling
=========

Compiling code on rhea is typical of commodity or beowulf-style hpc
linux clusters.

Available compilers
-------------------

The following compilers are available on rhea:

- `intel <https://www.olcf.ornl.gov/software_package/intel/>`__, intel composer xe (default)
- `pgi <https://www.olcf.ornl.gov/software_package/pgi/>`__, the portland group compiler suite
- `gcc <https://www.olcf.ornl.gov/software_package/gcc/>`__, the gnu compiler collection

Upon login, default versions of the intel compiler and openmpi (message
passing interface) libraries are automatically added to each user's
environment. Users do not need to make any environment changes to use
the default version of intel and openmpi.

--------------

Changing compilers
------------------

If a different compiler is required, it is important to use the correct
environment for each compiler. To aid users in pairing the correct
compiler and environment, the module system on rhea automatically pulls
in libraries compiled with a given compiler when changing compilers. The
compiler modules will load the correct pairing of compiler version,
message passing libraries, and other items required to build and run
code. To change the default loaded intel environment to the gcc
environment for example, use:

.. code::

    $ module load gcc

This will automatically unload the current compiler and system libraries
associated with it, load the new compiler environment and automatically
load associated system libraries as well.

Changing versions of the same compiler
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To use a specific compiler *version*, you must first ensure the
compiler's module is loaded, and *then* swap to the correct compiler
version. For example, the following will configure the environment to
use the gcc compilers, then load a non-default gcc compiler version:

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

These wrapper programs are cognizant of your currently loaded modules,
and will ensure that your code links against our openmpi installation.
more information about using openmpi at our center can be found in our
`software documentation <https://www.olcf.ornl.gov/software_package/openmpi/>`__.

Compiling threaded codes
------------------------

When building threaded codes, compiler-specific flags must be included
to ensure a proper build.

Openmp
^^^^^^

For pgi, add "-mp" to the build line.

.. code::

    $ mpicc -mp test.c -o test.x
    $ export omp_num_threads=2

For gnu, add "-fopenmp" to the build line.

.. code::

    $ mpicc -fopenmp test.c -o test.x
    $ export omp_num_threads=2

For intel, add "-qopenmp" to the build line.

.. code::

    $ mpicc -qopenmp test.c -o test.x
    $ export omp_num_threads=2

For information on *running threaded codes*, please see the  :ref:`thread-layout`
subsection of the :ref:`rhea-running-jobs` section in
this user guide.

Shell and programming environments
==================================

OLCF systems provide hundreds of software packages and scientific
libraries pre-installed at the system-level for users to take advantage
of. To facilitate this, environment management tools are employed to
handle necessary changes to the shell dynamically. The sections below
provide information about using the management tools at the OLCF.

--------------

Default shell
-------------

A user's default shell is selected when completing the user account
request form. The chosen shell is set across all OLCF resources.
Currently, supported shells include:

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

The *modules* software package allows you to dynamically modify your
user environment by using pre-written *modulefiles*. environment modules
are provided through `Lmod <https://lmod.readthedocs.io/en/latest/>`__,
a Lua-based module system for dynamically altering shell environments.
by managing changes to the shell’s environment variables (such as
``path``, ``ld_library_path``, and ``pkg_config_path``), Lmod allows you
to alter the software available in your shell environment without the
risk of creating package and version combinations that cannot coexist in
a single environment.

Lmod is a recursive environment module system, meaning it is aware of
module compatibility and actively alters the environment to protect
against conflicts. Messages to stderr are issued upon Lmod implicitly
altering the environment. Environment modules are structured
hierarchically by compiler family such that packages built with a given
compiler will only be accessible if the compiler family is first present
in the environment.

    **note:** Lmod can interpret both Lua modulefiles and legacy Tcl
    modulefiles. However, long and logic-heavy Tcl modulefiles may require
    porting to Lua.

General usage
^^^^^^^^^^^^^

Typical use of Lmod is very similar to that of interacting with
modulefiles on other OLCF systems. The interface to Lmod is provided by
the ``module`` command:

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

    **Note:** Modules are changed recursively. Some commands, such as
    ``module swap``, are available to maintain compatibility with scripts
    using Tcl Environment Modules, but are not necessary since Lmod
    recursively processes loaded modules and automatically resolves
    conflicts.

Searching for modules
^^^^^^^^^^^^^^^^^^^^^

Modules with dependencies are only available when the underlying
dependencies, such as compiler families, are loaded. Thus,
``module avail`` will only display modules that are compatible with the
current state of the environment. To search the entire hierarchy across
all possible dependencies, the ``spider`` sub-command can be used as
summarized in the following table.

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

Lmod supports caching commonly used collections of environment modules
on a per-user basis in ``$home/.lmod.d``. to create a collection called
"NAME" from the currently loaded modules, simply call
``module save NAME``. omitting "NAME" will set the user’s default
collection. Saved collections can be recalled and examined with the
commands summarized in the following table.

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

    **Note:** You should use unique names when creating collections to
    specify the application (and possibly branch) you are working on. For
    example, \`app1-development\`, \`app1-production\`, and
    \`app2-production\`.

    **Note:** In order to avoid conflicts between user-defined collections
    on multiple compute systems that share a home file system (e.g.
    /ccs/home/[userid]), lmod appends the hostname of each system to the
    files saved in in your ~/.lmod.d directory (using the environment
    variable lmod\_system\_name). This ensures that only collections
    appended with the name of the current system are visible.

The following screencast shows an example of setting up user-defined
module collections on Summit. https://vimeo.com/293582400

--------------

Installed Software
------------------

The OLCF provides hundreds of pre-installed software packages and
scientific libraries for your use, in addition to taking `software
installation requests <https://www.olcf.ornl.gov/support/software/software-request/>`__. See the
`software <https://www.olcf.ornl.gov/for-users/software/>`__ page for complete details on
existing installs.

.. _rhea-running-jobs:

Running jobs
============

In high performance computing (hpc), computational work is performed by
*jobs*. individual jobs produce data that lend relevant insight into
grand challenges in science and engineering. As such, the timely,
efficient execution of jobs is the primary concern in the operation of
any hpc system. A job on a commodity cluster typically comprises a few
different components:

-  a batch submission script.
-  a binary executable.
-  a set of input files for the executable.
-  a set of output files created by the executable.

And the process for running a job, in general, is to:

#. prepare executables and input files.
#. write a batch script.
#. submit the batch script to the batch scheduler.
#. optionally monitor the job before and during execution.

The following sections describe in detail how to create, submit, and
manage jobs for execution on commodity clusters.

--------------

Login vs compute nodes on commodity clusters
--------------------------------------------

Login nodes
^^^^^^^^^^^

When you log into an olcf cluster, you are placed on a *login* node.
login node resources are shared by all users of the system. Because of
this, users should be mindful when performing tasks on a login node.
login nodes should be used for basic tasks such as file editing, code
compilation, data backup, and job submission. Login nodes should *not*
be used for memory- or compute-intensive tasks. Users should also limit
the number of simultaneous tasks performed on the login resources. For
example, a user should not run (10) simultaneous ``tar`` processes on a
login node.

    **warning:** compute-intensive, memory-intensive, or otherwise
    disruptive processes running on login nodes may be killed without
    warning.

Compute nodes
^^^^^^^^^^^^^

.. include:: includes/rhea-compute-nodes.txt

--------------

Writing batch scripts for commodity clusters
--------------------------------------------

Batch scripts, or job submission scripts, are the mechanism by which a
user configures and submits a job for execution. A batch script is
simply a shell script that also includes commands to be interpreted by
the batch scheduling software (e.g. Pbs). batch scripts are submitted to
the batch scheduler, where they are then parsed for the scheduling
configuration options. The batch scheduler then places the script in the
appropriate queue, where it is designated as a batch job. Once the batch
jobs makes its way through the queue, the script will be executed on the
primary compute node of the allocated resources.

Components of a batch script
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Batch scripts are parsed into the following (3) sections:

Interpreter line
""""""""""""""""

The first line of a script can be used to specify the script’s
interpreter; this line is optional. If not used, the submitter’s default
shell will be used. The line uses the *hash-bang* syntax, i.e.,
``#!/path/to/shell``.

Pbs submission options
""""""""""""""""""""""

The pbs submission options are preceded by the string ``#pbs``, making
them appear as comments to a shell. Pbs will look for ``#pbs`` options
in a batch script from the script’s first line through the first
non-comment line. A comment line begins with ``#``. ``#pbs`` options
entered after the first non-comment line will not be read by pbs.

Shell commands
""""""""""""""

The shell commands follow the last ``#pbs`` option and represent the
executable content of the batch job. If any ``#pbs`` lines follow
executable statements, they will be treated as comments only. The
execution section of a script will be interpreted by a shell and can
contain multiple lines of executables, shell commands, and comments.
when the job's queue wait time is finished, commands within this section
will be executed on the primary compute node of the job's allocated
resources. Under normal circumstances, the batch job will exit the queue
after the last line of the script is executed.

Example batch script
^^^^^^^^^^^^^^^^^^^^

.. code::

      1: #!/bin/bash
      2: #pbs -a xxxyyy
      3: #pbs -n test
      4: #pbs -j oe
      5: #pbs -l walltime=1:00:00,nodes=2
      6:
      7: cd $pbs_o_workdir
      8: date
      9: mpirun -n 8 ./a.out

This batch script shows examples of the three sections outlined above:

Interpreter line
""""""""""""""""

1: this line is optional and can be used to specify a shell to interpret
the script. In this example, the bash shell will be used.

Pbs options
"""""""""""

2: the job will be charged to the “xxxyyy” project. 3: the job will be
named ``test``. 4: the job's standard output and error will be combined
into one file. 5: the job will request (2) nodes for (1) hour.

Shell commands
""""""""""""""

6: this line is left blank, so it will be ignored. 7: this command will
change the current directory to the directory from where the script was
submitted. 8: this command will run the ``date`` command. 9: this
command will run (8) mpi instances of the executable ``a.out`` on the
compute nodes allocated by the batch system. Batch scripts can be
submitted for execution using the ``qsub`` command. For example, the
following will submit the batch script named ``test.pbs``:

.. code::

      qsub test.pbs

If successfully submitted, a pbs job id will be returned. This id can be
used to track the job. It is also helpful in troubleshooting a failed
job; make a note of the job id for each of your jobs in case you must
contact the `olcf user assistance
center </for-users/user-assistance/>`__ for support.

--------------

Interactive batch jobs on commodity clusters
--------------------------------------------

Batch scripts are useful when one has a pre-determined group of commands
to execute, the results of which can be viewed at a later time. However,
it is often necessary to run tasks on compute resources interactively.
users are not allowed to access cluster compute nodes directly from a
login node. Instead, users must use an *interactive batch job* to
allocate and gain access to compute resources. This is done by using the
``-i`` option to ``qsub``. other pbs options are passed to ``qsub`` on
the command line as well:

.. code::

      $ qsub -i -a abc123 -q qname -v -l nodes=4 -l walltime=00:30:00

This request will:

+----------------------------+----------------------------------------------------------------+
| ``-i``                     | start an interactive session                                   |
+----------------------------+----------------------------------------------------------------+
| ``-a``                     | charge to the ``abc123`` project                               |
+----------------------------+----------------------------------------------------------------+
| ``-q qname``               | run in the ``qname`` queue                                     |
+----------------------------+----------------------------------------------------------------+
| ``-v``                     | export the user's shell environment to the job's environment   |
+----------------------------+----------------------------------------------------------------+
| ``-l nodes=4``             | request (4) nodes...                                           |
+----------------------------+----------------------------------------------------------------+
| ``-l walltime=00:30:00``   | ...for (30) minutes                                            |
+----------------------------+----------------------------------------------------------------+

After running this command, the job will wait until enough compute nodes
are available, just as any other batch job must. However, once the job
starts, the user will be given an interactive prompt on the primary
compute node within the allocated resource pool. Commands may then be
executed directly (instead of through a batch script).

Using to debug
^^^^^^^^^^^^^^

A common use of interactive batch is to aid in debugging efforts.
interactive access to compute resources allows the ability to run a
process to the point of failure; however, unlike a batch job, the
process can be restarted after brief changes are made without losing the
compute resource pool; thus speeding up the debugging effort.

Choosing a job size
^^^^^^^^^^^^^^^^^^^

Because interactive jobs must sit in the queue until enough resources
become available to allocate, it is useful to choose a job size based on
the number of currently unallocated nodes (to shorten the queue wait
time). use the ``showbf`` command (i.e. "show backfill") to see resource
limits that would allow your job to be immediately backfilled (and thus
started) by the scheduler. For example, the snapshot below shows that
(8) nodes are currently free.

.. code::

      $ showbf

      partition   tasks  nodes  startoffset   duration   startdate
      ---------   -----  -----  ------------  ---------  --------------
      rhea        4744   8      infinity      00:00:00   hh:mm:ss_mm/dd

See the output of the ``showbf –help`` command for additional options.

--------------

Common batch options to pbs
---------------------------

The following table summarizes frequently-used options to pbs:

+----------+----------------------------------------+-------------------------------------------------------------------------------------+
| option   | use                                    | description                                                                         |
+==========+========================================+=====================================================================================+
| ``-a``   | ``#pbs -a <account>``                  | causes the job time to be                                                           |
|          |                                        | charged to ``<account>``. the account string, e.g. ``pjt000``, is typically         |
|          |                                        | composed of three letters followed by three digits and optionally followed by a     |
|          |                                        | subproject identifier. The utility ``showproj`` can be used to list your valid      |
|          |                                        | assigned project id(s). this option is required by all jobs.                        |
+----------+----------------------------------------+-------------------------------------------------------------------------------------+
| ``-l``   | ``#PBS -l nodes=<value>``              | Maximum number of compute nodes. Jobs cannot request partial nodes.                 |
+----------+----------------------------------------+-------------------------------------------------------------------------------------+
|          | ``#PBS -l walltime=<time>``            | Maximum wall-clock time. ``<time>`` is in the format HH:MM:SS.                      |
+----------+----------------------------------------+-------------------------------------------------------------------------------------+
|          | ``#PBS -l partition=<partition_name>`` | Allocates resources on specified partition.                                         |
+----------+----------------------------------------+-------------------------------------------------------------------------------------+
| ``-o``   | ``#PBS -o <filename>``                 | Writes standard output to                                                           |
|          |                                        | ``<name>`` instead of ``<job script>.o$PBS_JOBID``. ``$PBS_JOBID`` is an            |
|          |                                        | environment variable created by PBS that contains the PBS job identifier.           |
+----------+----------------------------------------+-------------------------------------------------------------------------------------+
| ``-e``   | ``#PBS -e <filename>``                 | Writes standard error to ``<name>`` instead of ``<job script>.e$PBS_JOBID.``        |
+----------+----------------------------------------+-------------------------------------------------------------------------------------+
| ``-j``   | ``#PBS -j {oe,eo}``                    | Combines standard output                                                            |
|          |                                        | and standard error into the standard error file (``eo``) or the standard out        |
|          |                                        | file (``oe``).                                                                      |
+----------+----------------------------------------+-------------------------------------------------------------------------------------+
| ``-m``   | ``#PBS -m a``                          | Sends email to the submitter when the job aborts.                                   |
+----------+----------------------------------------+-------------------------------------------------------------------------------------+
|          | ``#PBS -m b``                          | Sends email to the submitter when the job begins.                                   |
+----------+----------------------------------------+-------------------------------------------------------------------------------------+
|          | ``#PBS -m e``                          | Sends email to the submitter when the job ends.                                     |
+----------+----------------------------------------+-------------------------------------------------------------------------------------+
| ``-M``   | ``#PBS -M <address>``                  | Specifies email address to use for ``-m`` options.                                  |
+----------+----------------------------------------+-------------------------------------------------------------------------------------+
| ``-N``   | ``#PBS -N <name>``                     | Sets the job name to ``<name>`` instead of the name of the job script.              |
+----------+----------------------------------------+-------------------------------------------------------------------------------------+
| ``-S``   | ``#PBS -S <shell>``                    | Sets the shell to interpret the job script.                                         |
+----------+----------------------------------------+-------------------------------------------------------------------------------------+
| ``-q``   | ``#PBS -q <queue>``                    | Directs the job to the                                                              |
|          |                                        | specified queue.This option is not required to run in the default queue on any      |
|          |                                        | given system.                                                                       |
+----------+----------------------------------------+-------------------------------------------------------------------------------------+
| ``-V``   | ``#PBS -V``                            | Exports all environment                                                             |
|          |                                        | variables from the submitting shell into the batch job shell. Since the login       |
|          |                                        | nodes differ from the service nodes, using the '-V' option is **not recommended**.  |
|          |                                        | Users should create the needed environment within the batch job.                    |
+----------+----------------------------------------+-------------------------------------------------------------------------------------+
| ``-X``   | ``#PBS -X``                            | Enables X11 forwarding.                                                             |
|          |                                        | The -X PBS option should be used to tunnel a GUI from an interactive batch job.     |
+----------+----------------------------------------+-------------------------------------------------------------------------------------+

    **Note:** Because the login nodes differ from the service nodes, using
    the '-V' option is not recommended. Users should create the needed
    environment within the batch job.

Further details and other PBS options may be found through the ``qsub``
man page.

--------------

Batch Environment Variables
---------------------------

PBS sets multiple environment variables at submission time. The
following PBS variables are useful within batch scripts:

+----------------------+----------------------------------------------------------------------------------+
| Variable             | Description                                                                      |
+======================+==================================================================================+
| ``$PBS_O_WORKDIR``   | The directory from which the batch job was                                       |
|                      | *submitted*. By default, a new job starts in your home directory. You can get    |
|                      | back to the directory of job submission with ``cd $PBS_O_WORKDIR``. Note that    |
|                      | this is not necessarily the same directory in which the batch script resides.    |
+----------------------+----------------------------------------------------------------------------------+
| ``$PBS_JOBID``       | The job’s full identifier. A common use for                                      |
|                      | ``PBS_JOBID`` is to append the job’s ID to the standard output and error files.  |
+----------------------+----------------------------------------------------------------------------------+
| ``$PBS_NUM_NODES``   | The number of nodes requested.                                                   |
+----------------------+----------------------------------------------------------------------------------+
| ``$PBS_JOBNAME``     | The job name supplied by the user.                                               |
+----------------------+----------------------------------------------------------------------------------+
| ``$PBS_NODEFILE``    | The name of the file containing the list of nodes                                |
|                      | assigned to the job. Used sometimes on non-Cray clusters.                        |
+----------------------+----------------------------------------------------------------------------------+

--------------

Modifying Batch Jobs
--------------------

The batch scheduler provides a number of utility commands for managing
submitted jobs. See each utilities' man page for more information.

Removing and Holding Jobs
^^^^^^^^^^^^^^^^^^^^^^^^^

``qdel``


Jobs in the queue in any state can be stopped and removed from the queue
using the command ``qdel``.

.. code::

    $ qdel 1234

``qhold``


Jobs in the queue in a non-running state may be placed on hold using the
``qhold`` command. Jobs placed on hold will not be removed from the
queue, but they will not be eligible for execution.

.. code::

    $ qhold 1234

``qrls``


Once on hold the job will not be eligible to run until it is released to
return to a queued state. The ``qrls`` command can be used to remove a
job from the held state.

.. code::

    $ qrls 1234

Modifying Job Attributes
^^^^^^^^^^^^^^^^^^^^^^^^

``qalter``


Non-running jobs in the queue can be modified with the PBS ``qalter``
command. The ``qalter`` utility can be used to do the following (among
others): Modify the job’s name:

.. code::

    $ qalter -N newname 130494

Modify the number of requested cores:

.. code::

    $ qalter -l nodes=12 130494

Modify the job’s walltime:

.. code::

    $ qalter -l walltime=01:00:00 130494

..

    **Note:** Once a batch job moves into a running state, the job's
    walltime can not be increased.

--------------

Monitoring Batch Jobs
---------------------

PBS and Moab provide multiple tools to view queue, system, and job
status. Below are the most common and useful of these tools.

Job Monitoring Commands
^^^^^^^^^^^^^^^^^^^^^^^

``showq``
"""""""""

The Moab utility ``showq`` can be used to view a more detailed
description of the queue. The utility will display the queue in the
following states:


+----------+-------------------------------------------------------------------------------+
| State    | Description                                                                   |
+==========+===============================================================================+
| Active   | These jobs are currently running.                                             |
+----------+-------------------------------------------------------------------------------+
| Eligible | These jobs are currently queued awaiting resources. Eligible jobs are         |
|          | shown in the order in which the scheduler will consider them for allocation.  |
+----------+-------------------------------------------------------------------------------+
| Blocked  | These jobs are currently queued but are not eligible to run. A job may        |
|          | be in this state because the user has more jobs that are "eligible to         |
|          | run" than the system's queue policy allows.                                   |
+----------+-------------------------------------------------------------------------------+

To see all jobs currently in the queue:

.. code::

    $ showq

To see all jobs owned by userA currently in the queue:

.. code::

    $ showq -u userA

To see all jobs submitted to partitionA:

.. code::

    $ showq -p partitionA

To see all completed jobs:

.. code::

    $ showq -c

..

    **Note:** To increase response time, the MOAB utilities (*showstart*,
    *checkjob*) will display a cached result. The cache updates every 30
    seconds. But, because the cached result is displayed, you may see the
    following message:

::

    --------------------------------------------------------------------
    NOTE: The following information has been cached by the remote server
          and may be slightly out of date.
    --------------------------------------------------------------------


``checkjob``
""""""""""""

The Moab utility ``checkjob`` can be used to view details of a job in
the queue. For example, if job 736 is a job currently in the queue in a
blocked state, the following can be used to view why the job is in a
blocked state:

.. code::

    $ checkjob 736

The return may contain a line similar to the following:

.. code::

    BlockMsg: job 736 violates idle HARD MAXJOB limit of X for user (Req: 1 InUse: X)

This line indicates the job is in the blocked state because the owning
user has reached the limit for jobs in the "eligible to run" state.

``qstat``
"""""""""

The PBS utility ``qstat`` will poll PBS (Torque) for job information.
However, ``qstat`` does not know of Moab's blocked and eligible states.
Because of this, the ``showq`` Moab utility (see above) will provide a
more accurate batch queue state. To show show all queued jobs:

.. code::

    $ qstat -a

To show details about job 1234:

.. code::

    $ qstat -f 1234

To show all currently queued jobs owned by userA:

.. code::

    $ qstat -u userA

.. _batch-queues-on-rhea:

Batch Queues on Rhea
--------------------

The compute nodes on Rhea are separated into two partitions
(`rhea </for-users/system-user-guides/rhea/system-overview/#rhea-partition>`__
and
`gpu </for-users/system-user-guides/rhea/system-overview/#gpu-partition>`__)
and are available through a single batch queue: ``batch``. The
scheduling policies for the individual partitions are as follows:

Rhea Partition Policy (default)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Jobs that do not specify a partition will run in the 512 node `rhea
partition </for-users/system-user-guides/rhea/system-overview/#rhea-partition>`__.


+-----+----------------+------------+-------------------------------------------+
| Bin | Node Count     | Duration   | Policy                                    |
+=====+================+============+===========================================+
| A   | 1 - 16 Nodes   | 0 - 48 hr  |                                           |
+-----+----------------+------------+ | max 4 jobs running and 4 jobs eligible  |
| B   | 17 - 64 Nodes  | 0 - 36 hr  | | **per user**                            |
+-----+----------------+------------+ | in bins A, B, and C                     |
| C   | 65 - 384 Nodes | 0 - 3 hr   |                                           |
+-----+----------------+------------+-------------------------------------------+


GPU Partition Policy
^^^^^^^^^^^^^^^^^^^^

To access the 9 node `gpu
partition </for-users/system-user-guides/rhea/system-overview/#gpu-partition>`__,
batch job submissions should request ``-lpartition=gpu``

+------------+-------------+--------------------------+
| Node Count |  Duration   |  Policy                  |
+============+=============+==========================+
| 1-2 Nodes  |  0 - 48 hrs |    | max 1 job running   |
|            |             |    | **per user**        |
+------------+-------------+--------------------------+

    **Note:** The queue structure was designed based on user feedback and
    analysis of batch jobs over the recent years. However, we understand that
    the structure may not meet the needs of all users. **If this structure
    limits your use of the system, please let us know.** We want Rhea to be a
    useful OLCF resource and will work with you providing exceptions or even
    changing the queue structure if necessary.

Users wishing to submit jobs that fall outside the queue structure are
encouraged to request a reservation via the `Special Request
Form </for-users/getting-started/special-request-form/>`__.

Allocation Overuse Policy
^^^^^^^^^^^^^^^^^^^^^^^^^

Projects that overrun their allocation are still allowed to run on OLCF
systems, although at a reduced priority. Like the adjustment for the
number of processors requested above, this is an adjustment to the
apparent submit time of the job. However, this adjustment has the effect
of making jobs appear much younger than jobs submitted under projects
that have not exceeded their allocation. In addition to the priority
change, these jobs are also limited in the amount of wall time that can
be used. For example, consider that ``job1`` is submitted at the same
time as ``job2``. The project associated with ``job1`` is over its
allocation, while the project for ``job2`` is not. The batch system will
consider ``job2`` to have been waiting for a longer time than ``job1``.
Also projects that are at 125% of their allocated time will be limited
to only one running job at a time. The adjustment to the apparent submit
time depends upon the percentage that the project is over its
allocation, as shown in the table below:

+------------------------+----------------------+--------------------------+------------------+
| % Of Allocation Used   | Priority Reduction   | number eligible-to-run   | number running   |
+========================+======================+==========================+==================+
| < 100%                 | 0 days               | 4 jobs                   | unlimited jobs   |
+------------------------+----------------------+--------------------------+------------------+
| 100% to 125%           | 30 days              | 4 jobs                   | unlimited jobs   |
+------------------------+----------------------+--------------------------+------------------+
| > 125%                 | 365 days             | 4 jobs                   | 1 job            |
+------------------------+----------------------+--------------------------+------------------+

--------------

Job Execution on Commodity Clusters
-----------------------------------

Once resources have been allocated through the batch system, users have
the option of running commands on the allocated resources' primary
compute node (a serial job) and/or running an MPI/OpenMP executable
across all the resources in the allocated resource pool simultaneously
(a parallel job).

Serial Job Execution on Commodity Clusters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The executable portion of batch scripts is interpreted by the shell
specified on the first line of the script. If a shell is not specified,
the submitting user’s default shell will be used. The serial portion of
the batch script may contain comments, shell commands, executable
scripts, and compiled executables. These can be used in combination to,
for example, navigate file systems, set up job execution, run serial
executables, and even submit other batch jobs.

Parallel Job Execution on Commodity Clusters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using ``mpirun``
"""""""""""""""""

By default, commands will be executed on the job's primary compute node,
sometimes referred to as the job's *head node*. The ``mpirun`` command
is used to execute an MPI executable on one or more compute nodes in
parallel. ``mpirun`` accepts the following common options:

+----------------------------------+-------------------------------------------------------+
| ``--npernode``                   | Number of ranks per node                              |
+----------------------------------+-------------------------------------------------------+
| ``-n``                           | Total number of MPI ranks                             |
+----------------------------------+-------------------------------------------------------+
| ``--bind-to none``               | Allow code to control thread affinity                 |
+----------------------------------+-------------------------------------------------------+
| ``--map-by ppr:N:node:pe=T``     | Place N tasks per node leaving space for T threads    |
+----------------------------------+-------------------------------------------------------+
| ``--map-by ppr:N:socket:pe=T``   | Place N tasks per socket leaving space for T threads  |
+----------------------------------+-------------------------------------------------------+
| ``--map-by ppr:N:socket``        | Assign tasks by socket placing N tasks on each socket |
+----------------------------------+-------------------------------------------------------+
| ``--report-bindings``            | Have MPI explain which ranks have been assigned to    |
|                                  | which nodes / physical cores                          |
+----------------------------------+-------------------------------------------------------+

    **Note:** If you do not specify the number of MPI tasks to ``mpirun``
    via ``-n``, the system will default to all available cores allocated to
    the job.

MPI Task Layout
"""""""""""""""""

Each compute node on Rhea contains two sockets each with 8 cores.
Depending on your job, it may be useful to control task layout within
and across nodes.

**Default Layout: Sequential**

The following will run a copy of a.out on two cores each on the same
node:

.. code::

    $ mpirun -np 2 ./a.out

+-----------------------------------------------------------------------------------------------------------------------------------------------+
|                                                                 Compute Node                                                                  |
+-----------------------------------------------------------------------+-----------------------------------------------------------------------+
|                             Socket 0                                  |                             Socket 1                                  |
+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| Core 0 | Core 1 | Core 2 | Core 3 | Core 4 | Core 5 | Core 6 | Core 7 | Core 0 | Core 1 | Core 2 | Core 3 | Core 4 | Core 5 | Core 6 | Core 7 |
+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| rank 0 | rank 1 |        |        |        |        |        |        |        |        |        |        |        |        |        |        |
+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+

**4 cores, 2 cores per socket, 1 node**

The following will run a.out on 4 cores, 2 cores per socket, 1 node:

.. code::

    $ mpirun -np 4 --map-by ppr:2:socket ./a.out

+-----------------------------------------------------------------------------------------------------------------------------------------------+
|                                                                 Compute Node                                                                  |
+-----------------------------------------------------------------------+-----------------------------------------------------------------------+
|                             Socket 0                                  |                             Socket 1                                  |
+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| Core 0 | Core 1 | Core 2 | Core 3 | Core 4 | Core 5 | Core 6 | Core 7 | Core 0 | Core 1 | Core 2 | Core 3 | Core 4 | Core 5 | Core 6 | Core 7 |
+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| rank 0 | rank 1 |        |        |        |        |        |        | rank 2 | rank 3 |        |        |        |        |        |        |
+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+

**4 cores, 1 core per socket, 2 nodes**

The following will run a.out on 4 cores, 1 core per socket, 2 nodes.
This can be useful if you need to spread your batch job over multiple
nodes to allow each task access to more memory.

.. code::

    $ mpirun -np 4 --map-by ppr:1:socket ./a.out

+-----------------------------------------------------------------------------------------------------------------------------------------------+
|                                                                 Compute Node 0                                                                |
+-----------------------------------------------------------------------+-----------------------------------------------------------------------+
|                             Socket 0                                  |                             Socket 1                                  |
+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| Core 0 | Core 1 | Core 2 | Core 3 | Core 4 | Core 5 | Core 6 | Core 7 | Core 0 | Core 1 | Core 2 | Core 3 | Core 4 | Core 5 | Core 6 | Core 7 |
+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| rank 0 |        |        |        |        |        |        |        | rank 1 |        |        |        |        |        |        |        |
+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
|                                                                 Compute Node 1                                                                |
+-----------------------------------------------------------------------+-----------------------------------------------------------------------+
|                             Socket 0                                  |                             Socket 1                                  |
+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| Core 0 | Core 1 | Core 2 | Core 3 | Core 4 | Core 5 | Core 6 | Core 7 | Core 0 | Core 1 | Core 2 | Core 3 | Core 4 | Core 5 | Core 6 | Core 7 |
+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| rank 2 |        |        |        |        |        |        |        | rank 3 |        |        |        |        |        |        |        |
+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+

The ``--report-bindings`` flag can be used to report task layout:

.. code::

    $ mpirun -np 4 --map-by ppr:1:socket --report-bindings hostname
    [rhea2:47176] MCW rank 0 bound to socket 0[core 0[hwt 0-1]]: [BB/../../../../../../..][../../../../../../../..]
    [rhea2:47176] MCW rank 1 bound to socket 1[core 8[hwt 0-1]]: [../../../../../../../..][BB/../../../../../../..]
    [rhea4:104150] MCW rank 2 bound to socket 0[core 0[hwt 0-1]]: [BB/../../../../../../..][../../../../../../../..]
    [rhea4:104150] MCW rank 3 bound to socket 1[core 8[hwt 0-1]]: [../../../../../../../..][BB/../../../../../../..]
    $

.. _thread-layout:

Thread Layout
"""""""""""""""""

    **Warning:** Without controlling affinity, threads may be placed on the
    same core.

**2 MPI tasks, 1 tasks per node, 16 threads per task, 2 nodes**


.. code::

    $ setenv OMP_NUM_THREADS 16
    $ mpirun -np 2 --map-by ppr:1:node:pe=16 ./a.out

+-----------------------------------------------------------------------------------------------------------------------------------------------+
|                                                                 Compute Node 0                                                                |
+-----------------------------------------------------------------------+-----------------------------------------------------------------------+
|                             Socket 0                                  |                             Socket 1                                  |
+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| Core 0 | Core 1 | Core 2 | Core 3 | Core 4 | Core 5 | Core 6 | Core 7 | Core 0 | Core 1 | Core 2 | Core 3 | Core 4 | Core 5 | Core 6 | Core 7 |
+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| rank 0 | thd. 1 | thd. 2 | thd. 3 | thd. 4 | thd. 5 | thd. 6 | thd. 7 | thd. 8 | thd. 9 | thd. 10| thd. 11| thd. 12| thd. 13| thd. 14| thd. 15|
| thd. 0 |        |        |        |        |        |        |        |        |        |        |        |        |        |        |        |
+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
|                                                                 Compute Node 1                                                                |
+-----------------------------------------------------------------------+-----------------------------------------------------------------------+
|                             Socket 0                                  |                             Socket 1                                  |
+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| Core 0 | Core 1 | Core 2 | Core 3 | Core 4 | Core 5 | Core 6 | Core 7 | Core 0 | Core 1 | Core 2 | Core 3 | Core 4 | Core 5 | Core 6 | Core 7 |
+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| rank 1 | thd. 1 | thd. 2 | thd. 3 | thd. 4 | thd. 5 | thd. 6 | thd. 7 | thd. 8 | thd. 9 | thd. 10| thd. 11| thd. 12| thd. 13| thd. 14| thd. 15|
| thd. 0 |        |        |        |        |        |        |        |        |        |        |        |        |        |        |        |
+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+

**2 MPI tasks, 1 tasks per socket, 4 threads per task, 1 node**

+-----------------------------------------------------------------------------------------------------------------------------------------------+
|                                                                 Compute Node                                                                  |
+-----------------------------------------------------------------------+-----------------------------------------------------------------------+
|                             Socket 0                                  |                             Socket 1                                  |
+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| Core 0 | Core 1 | Core 2 | Core 3 | Core 4 | Core 5 | Core 6 | Core 7 | Core 0 | Core 1 | Core 2 | Core 3 | Core 4 | Core 5 | Core 6 | Core 7 |
+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| rank 0 | thd. 1 | thd. 2 | thd. 3 |        |        |        |        | rank 1 | thd. 1 | thd. 2 | thd. 3 |        |        |        |        |
| thd. 0 |        |        |        |        |        |        |        | thd. 0 |        |        |        |        |        |        |        |
+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+


.. code::

    $ setenv OMP_NUM_THREADS 4
    $ mpirun -np 2 --map-by ppr:1:socket:pe=4 ./a.out

Resource Sharing on Commodity Clusters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Jobs on OLCF clusters are scheduled in full node increments; a node's
cores cannot be allocated to multiple jobs. Because the OLCF charges
based on what a job makes *unavailable* to other users, a job is charged
for an entire node even if it uses only one core on a node. To simplify
the process, users are given a multiples of entire nodes through PBS.

    **Note:** Users are given a multiples of entire nodes through PBS, and
    associated allocations are reduced by the number of nodes requested,
    regardless of actual CPU utilization.

In general, the cluster may move MPI tasks between cores within a node.
To help prevent a job’s tasks from being moved between cores each idle
cycle the ``mpi_yield_when_idle`` OpenMPI option may be used. For
example:

.. code::

      $ mpirun -n 8 -mca mpi_yield_when_idle 0 a.out

This will help prevent the core from being given to other waiting tasks.
This only affects MPI processes when they are blocking in MPI library
calls. By default OpenMPI will set this variable based on whether it
believes the node is over-allocated or under-allocated. If
over-allocated, ``mpi_yield_when_idle``, will be set to a value other
than (1), allowing the core to be given to other waiting tasks when
idle. If under-allocated, ``mpi_yield_when_idle``, will be set to (0).
If more tasks are running on a node than are cores, the OS will swap all
tasks between cores on the node. The ``mpi_yield_when_idle`` option only
helps to slow this down; it will not fully prevent the swaps.

--------------

Job Accounting on Rhea
----------------------

Jobs on Rhea are scheduled in full node increments; a node's cores
cannot be allocated to multiple jobs. Because the OLCF charges based on
what a job makes *unavailable* to other users, a job is charged for an
entire node even if it uses only one core on a node. To simplify the
process, users are given a multiples of entire nodes through PBS.

Viewing Allocation Utilization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Projects are allocated time on Rhea in units of *node-hours*. This is
separate from a project's Titan or Eos allocation, and usage of Rhea
does not count against that allocation. This page describes how such
units are calculated, and how users can access more detailed information
on their relevant allocations.

Node-Hour Calculation
^^^^^^^^^^^^^^^^^^^^^

The *node-hour* charge for each batch job will be calculated as follows:

.. code::

    node-hours = nodes requested * ( batch job endtime - batch job starttime )

Where *batch job starttime* is the time the job moves into a running
state, and *batch job endtime* is the time the job exits a running
state. A batch job's usage is calculated solely on requested nodes and
the batch job's start and end time. The number of cores actually used
within any particular node within the batch job is not used in the
calculation. For example, if a job requests (6) nodes through the batch
script, runs for (1) hour, uses only (2) CPU cores per node, the job
will still be charged for 6 nodes \* 1 hour = *6 node-hours*.

Viewing Usage
^^^^^^^^^^^^^

Utilization is calculated daily using batch jobs which complete between
00:00 and 23:59 of the previous day. For example, if a job moves into a
run state on Tuesday and completes Wednesday, the job's utilization will
be recorded Thursday. Only batch jobs which write an end record are used
to calculate utilization. Batch jobs which do not write end records due
to system failure or other reasons are not used when calculating
utilization. Each user may view usage for projects on which they are
members from the command line tool ``showusage`` and the `My OLCF
site <https://users.nccs.gov>`__.

On the Command Line via ``showusage``


The ``showusage`` utility can be used to view your usage from January 01
through midnight of the previous day. For example:

.. code::

      $ showusage
        Usage:
                                 Project Totals
        Project             Allocation      Usage      Remaining     Usage
        _________________|______________|___________|____________|______________
        abc123           |  20000       |   126.3   |  19873.7   |   1560.80

The ``-h`` option will list more usage details.

On the Web via My OLCF


More detailed metrics may be found on each project's usage section of
the `My OLCF site <https://users.nccs.gov>`__. The following information
is available for each project:

-  YTD usage by system, subproject, and project member
-  Monthly usage by system, subproject, and project member
-  YTD usage by job size groupings for each system, subproject, and
   project member
-  Weekly usage by job size groupings for each system, and subproject
-  Batch system priorities by project and subproject
-  Project members

The My OLCF site is provided to aid in the utilization and management of
OLCF allocations. If you have any questions or have a request for
additional data, please contact the OLCF User Assistance Center.

--------------

Enabling Workflows through Cross-System Batch Submission
--------------------------------------------------------

The OLCF now supports submitting jobs between OLCF systems via batch
scripts. This can be useful for automatically triggering analysis and
storage of large data sets after a successful simulation job has ended,
or for launching a simulation job automatically once the input deck has
been retrieved from HPSS and pre-processed.

.. image:: /images/Cross-Submission-Workflow-544x300.png
   :class: size-medium wp-image-4468
   :width: 544px
   :height: 300px

Cross-Submission allows jobs on one OLCF resource to submit new jobs to other
OLCF resources. The key to remote job submission is the command ``qsub -q host
script.pbs`` which will submit the file ``script.pbs`` to the batch queue on
the specified host. This command can be inserted at the end of an existing
batch script in order to automatically trigger work on another OLCF resource.
This feature is supported on the following hosts:

+------------------------------+--------------------------------------+
| Host                         | Remote Submission Command            |
+==============================+======================================+
| Rhea                         | ``qsub -q rhea visualization.pbs``   |
+------------------------------+--------------------------------------+
| Eos                          | ``qsub -q eos visualization.pbs``    |
+------------------------------+--------------------------------------+
| Titan                        | ``qsub -q titan compute.pbs``        |
+------------------------------+--------------------------------------+
| Data Transfer Nodes (DTNs)   | ``qsub -q dtn retrieve_data.pbs``    |
+------------------------------+--------------------------------------+

Example Workflow 1: Automatic Post-Processing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The simplest example of a remote submission workflow would be
automatically triggering an analysis task on Rhea at the completion of a
compute job on Titan. This workflow would require two batch scripts, one
to be submitted on Titan, and a second to be submitted automatically to
Rhea. Visually, this workflow may look something like the following:

.. image:: /images/remote_submission.stage-compute-e1392655934134.png

The batch scripts for such a workflow could be implemented as follows:
**Batch-script-1.pbs**

.. code::

    #PBS -l walltime=0:30:00
    #PBS -l nodes=4096
    #PBS -A PRJ123
    #PBS -l gres=atlas1%atlas2

    # run compute job on titan
    cd $MEMBERWORK/prj123
    aprun -n 65536 ./run_simulation.exe

    # Submit visualization processing job to Rhea
    qsub -q rhea Batch-script-2.pbs

**Batch-script-2.pbs**

.. code::

    #PBS -l walltime=2:00:00
    #PBS -l nodes=10
    #PBS -A PRJ123
    #PBS -l gres=atlas1%atlas2

    # Launch exectuable
    cd $MEMBERWORK/prj123
    mpirun -n 10 ./post_process_job.exe

The key to this workflow is the
``qsub -q batch@rhea-batch Batch-script-2.pbs`` command, which tells
``qsub`` to submit the file ``Batch-script-2.pbs`` to the batch queue on
Rhea.

Initializing the Workflow


We can initialize this workflow in one of two ways:

-  Log into ``titan.ccs.ornl.gov`` and run ``qsub Batch-script-1.pbs``
   OR
-  From Titan or Rhea, run ``qsub -q titan Batch-script-1.pbs``

Example Workflow 2: Data Staging, Compute, and Archival
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now we give another example of a linear workflow. This example shows how
to use the Data Transfer Nodes (DTNs) to retrieve data from HPSS and
stage it to your project's scratch area before beginning. Once the
computation is done, we will automatically archive the output.

.. image:: /images/remote_submission.stage-compute-archive-e1392655850482.png

**Batch-script-1.pbs**

.. code::

    #PBS -l walltime=0:30:00
    #PBS -l nodes=1
    #PBS -A PRJ123
    #PBS -l gres=atlas1%atlas2

    # Retrieve Data from HPSS
    cd $MEMBERWORK/prj123
    htar -xf /proj/prj123/input_data.htar input_data/

    # Launch compute job
    qsub -q titan Batch-script-2.pbs

**Batch-script-2.pbs**

.. code::

    #PBS -l walltime=6:00:00
    #PBS -l nodes=4096
    #PBS -A PRJ123
    #PBS -l gres=atlas1%atlas2

    # Launch exectuable
    cd $MEMBERWORK/prj123
    aprun -n 65536 ./analysis-task.exe

    # Submit data archival job to DTNs
    qsub -q dtn Batch-script-3.pbs

**Batch-script-3.pbs**

.. code::

    #PBS -l walltime=0:30:00
    #PBS -l nodes=1
    #PBS -A PRJ123
    #PBS -l gres=atlas1%atlas2

    # Launch exectuable
    cd $MEMBERWORK/prj123
    htar -cf /proj/prj123/viz_output.htar viz_output/
    htar -cf /proj/prj123/compute_data.htar compute_data/

Initializing the Workflow


We can initialize this workflow in one of two ways:

-  Log into ``dtn.ccs.ornl.gov`` and run ``qsub Batch-script-1.pbs`` OR
-  From Titan or Rhea, run ``qsub -q dtn Batch-script-1.pbs``

Example Workflow 3: Data Staging, Compute, Visualization, and Archival
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is an example of a "branching" workflow. What we will do is first
use Rhea to prepare a mesh for our simulation on Titan. We will then
launch the compute task on Titan, and once this has completed, our
workflow will branch into two separate paths: one to archive the
simulation output data, and one to visualize it. After the
visualizations have finished, we will transfer them to a remote
institution.

.. image:: /images/remote_submission.stag-compute-archive-vis-transfer-e1392822417662.png

**Step-1.prepare-data.pbs**

.. code::

    #PBS -l walltime=0:30:00
    #PBS -l nodes=10
    #PBS -A PRJ123
    #PBS -l gres=atlas1%atlas2

    # Prepare Mesh for Simulation
    mpirun -n 160 ./prepare-mesh.exe

    # Launch compute job
    qsub -q titan Step-2.compute.pbs

**Step-2.compute.pbs**

.. code::

    #PBS -l walltime=6:00:00
    #PBS -l nodes=4096
    #PBS -A PRJ123
    #PBS -l gres=atlas1%atlas2

    # Launch exectuable
    cd $MEMBERWORK/prj123
    aprun -n 65536 ./analysis-task.exe

    # Workflow branches at this stage, launching 2 separate jobs

    # - Launch Archival task on DTNs
    qsub -q dtn@dtn-batch Step-3.archive-compute-data.pbs

    # - Launch Visualization task on Rhea
    qsub -q rhea Step-4.visualize-compute-data.pbs

**Step-3.archive-compute-data.pbs**

.. code::

    #PBS -l walltime=0:30:00
    #PBS -l nodes=1
    #PBS -A PRJ123
    #PBS -l gres=atlas1%atlas2

    # Archive compute data in HPSS
    cd $MEMBERWORK/prj123
    htar -cf /proj/prj123/compute_data.htar compute_data/

**Step-4.visualize-compute-data.pbs**

.. code::

    #PBS -l walltime=2:00:00
    #PBS -l nodes=64
    #PBS -A PRJ123
    #PBS -l gres=atlas1%atlas2

    # Visualize Compute data
    cd $MEMBERWORK/prj123
    mpirun -n 768 ./visualization-task.py

    # Launch transfer task
    qsub -q dtn Step-5.transfer-visualizations-to-campus.pbs

**Step-5.transfer-visualizations-to-campus.pbs**

.. code::

    #PBS -l walltime=2:00:00
    #PBS -l nodes=1
    #PBS -A PRJ123
    #PBS -l gres=atlas1%atlas2

    # Transfer visualizations to storage area at home institution
    cd $MEMBERWORK/prj123
    SOURCE=gsiftp://dtn03.ccs.ornl.gov/$MEMBERWORK/visualization.mpg
    DEST=gsiftp://dtn.university-name.edu/userid/visualization.mpg
    globus-url-copy -tcp-bs 12M -bs 12M -p 4 $SOURCE $DEST

Initializing the Workflow


We can initialize this workflow in one of two ways:

-  Log into ``rhea.ccs.ornl.gov`` and run
   ``qsub Step-1.prepare-data.pbs`` OR
-  From Titan or the DTNs, run ``qsub -q rhea Step-1.prepare-data.pbs``

Checking Job Status
^^^^^^^^^^^^^^^^^^^

+------------------------------+-----------------------------+--------------------------------+
| Host                         | Remote qstat                | Remote showq                   |
+==============================+=============================+================================+
| Rhea                         | ``qstat -a @rhea-batch``    | ``showq --host=rhea-batch``    |
+------------------------------+-----------------------------+--------------------------------+
| Eos                          | ``qstat -a @eos-batch``     | ``showq --host=eos-batch``     |
+------------------------------+-----------------------------+--------------------------------+
| Titan                        | ``qstat -a @titan-batch``   | ``showq --host=titan-batch``   |
+------------------------------+-----------------------------+--------------------------------+
| Data Transfer Nodes (DTNs)   | ``qstat -a @dtn-batch``     | ``showq --host=dtn-batch``     |
+------------------------------+-----------------------------+--------------------------------+

Deleting Remote Jobs
^^^^^^^^^^^^^^^^^^^^

In order to delete a job (say, job number 18688) from a remote queue,
you can do the following

+------------------------------+------------------------------+
| Host                         | Remote qdel                  |
+==============================+==============================+
| Rhea                         | ``qdel 18688@rhea-batch``    |
+------------------------------+------------------------------+
| Eos                          | ``qdel 18688@eos-batch``     |
+------------------------------+------------------------------+
| Titan                        | ``qdel 18688@titan-batch``   |
+------------------------------+------------------------------+
| Data Transfer Nodes (DTNs)   | ``qdel 18688@dtn-batch``     |
+------------------------------+------------------------------+

Potential Pitfalls
^^^^^^^^^^^^^^^^^^

The OLCF advises users to keep their remote submission workflows simple,
short, and mostly linear. Workflows that contain many layers of
branches, or that trigger many jobs at once, may prove difficult to
maintain and debug. Workflows that contain loops or recursion (jobs that
can submit themselves again) may inadvertently waste allocation hours if
a suitable exit condition is not reached.

    **Warning:** Recursive workflows which do not exit will drain your
    project's allocation. Refunds will not be granted. Please be extremely
    cautious when designing workflows that cause jobs to re-submit themselves.


.. image:: /images/remote_submission.circular-e1392656023400.png

As always, users on multiple projects are strongly advised to double
check that the ``#PBS -A <PROJECTID>`` field is set to the correct
project prior to submission. This will ensure that resource usage is
associated with the intended project.

--------------

Analysis tools
==============

ParaView
--------

`ParaView <http://paraview.org>`__ is an open-source, multi-platform
data analysis and visualization application. ParaView users can quickly
build visualizations to analyze their data using qualitative and
quantitative techniques. The data exploration can be done interactively
in 3D or programmatically using ParaView’s batch processing
capabilities. ParaView was developed to analyze extremely large datasets
using distributed memory computing resources. The OLCF provides ParaView
server installs on Rhea to facilitate large scale distributed
visualizations. The ParaView server running on Rhea may be used in a
headless batch processing mode or be used to drive a ParaView GUI client
running on your local machine.

ParaView client
^^^^^^^^^^^^^^^

A ParaView client instance is not available on Rhea. Interactive mode
requires that your local machine have a version matched ParaView client
installation and batch mode can benefit from a local installation as
well to aid in script generation. Precompiled ParaView binaries for
Windows, Macintosh, and Linux can be downloaded from
`Kitware <http://paraview.org/paraview/resources/software.php>`__.

Interactive mode
^^^^^^^^^^^^^^^^

Although in a single machine setup both the ParaView client and server
run on the same host, this need not be the case. It is possible to run a
local ParaView client to display and interact with your data while the
ParaView server runs in a Rhea batch job, allowing interactive analysis
of very large data sets.

    **Warning:** In interactive mode your local ParaView version number must
    match the ParaView version number available on Rhea. Please check the
    available ParaView versions using Rhea's `modules system
    </for-users/system-user-guides/rhea/shell-and-programming-environments/#using-modules>`__.

Interactive Example
"""""""""""""""""""

The following provides an example of launching the ParaView server on
Rhea and connecting to it from a locally running ParaView client.
Although several methods may be used the one described should work in
most cases.

    **Warning:** For Macintosh clients, it is necessary to install `XQuartz
    (X11) <https://support.apple.com/en-us/HT201341>`__ to get a command prompt
    in which you will securely enter your OLCF credentials.

    **Warning:** For Windows clients, it is necessary to install PuTTY to
    create an ssh connection in step 2.

**Step 1: Launch ParaView on your Desktop and fetch a connection script for Rhea**

Start ParaView and then select ``File/Connect`` to begin.

.. image:: /images/paraview_step1a.png
   :width: 700px

Next Select ``Fetch Servers``

.. image:: /images/paraview1.2.png
   :width: 600px

Next select the connection to Rhea for either windows or Mac/Linux and hit the
“Import Selected” button.

.. image:: /images//paraview_step1c.png
   :width: 600px

You may now quit and restart ParaView in order to save connection setup in your
preferences. **Step 2: Establish a connection to Rhea** Once restarted, and
henceforth, simply select Rhea from the File->Connect dialog and click the
“Connect” button.

.. image:: /images/paraview_step2a.png
   :width: 600px

A dialog box follows, in which you must enter in your username and project
allocation, the number of nodes to reserve and a duration to reserve them for.

.. image:: /images/paraview_step2b.png
   :width: 500px

When you click OK, a windows command prompt or ``xterm`` pops up. In this
window enter your credentials at the OLCF login prompt.

.. image:: /images/paraview_step2c.png
   :width: 700px

When your job reaches the top of the queue, the ``RenderView1`` view window
will return. At this point you are connected to Rhea and can open files that
reside there and visualize them interactively.

VisIt
-----

VisIt is a interactive, parallel analysis and visualization tool for
scientific data. VisIt contains a rich set of visualization features so
you can view your data in a variety of ways. It can be used to visualize
scalar and vector fields defined on two- and three-dimensional (2D and
3D) structured and unstructured meshes.

Installing and Setting Up Visit
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

VisIt uses a client-server architecture. You will obtain the best
performance by running the VisIt client on your local computer and
running the server on OLCF resources. VisIt for your local computer can
be obtained here: `VisIt Installation <http://visit.llnl.gov>`__. The
first time you launch VisIt (after installing), you will be prompted for
a remote host preference. Make sure you select ORNL. You will then be
prompted to exit and re-launch VisIt for the host preferences to become
available. In order to finish setting up VisIt on your local machine:

-  Go to "Options→Host profiles" and choose "ORNL\_Rhea".
-  Make sure "Username" is set to your OLCF username.
-  Click on the "Launch Profiles" tab and then click on the "Parallel"
   button. Here, you can set up the parallel launch configuration.
   Default values will be filled in, but you will need to enter your
   project ID in the "Bank/Account" section. When finished, click Apply
   and close the "Host profiles" window.
-  To ensure these settings are saved, go to "Options→Save Settings".

Usage
^^^^^

Once you have VisIt installed and set up on your local computer:

-  Open VisIt on your local computer.
-  Go to: "File→Open file" or click the "Open" button on the GUI.
-  Click the "Host" dropdown menu on the "File open" window that popped
   up and choose "ORNL\_Rhea".
-  This will prompt you for your OLCF password, and connect you to Rhea.
-  Navigate to the appropriate file.
-  Once you choose a file, you will be prompted for the number of nodes
   and processors you would like to use (remember that each node of Rhea
   contains 16 processors) and the Project ID, which VisIt calls a
   "Bank" as shown below.
-  Once specified, the server side of VisIt will be launched, and you
   can interact with your data.

Please do not run VisIt's client from an OLCF machine. You will get much
better performance if you install a client on your workstation and
launch locally. You can directly connect to OLCF machines from inside
VisIt and access your data remotely. For additional resources, please
see the `VisIt Wiki <http://www.visitusers.org>`__.

Troubleshooting
^^^^^^^^^^^^^^^

VisIt keeps asking for your password.
"""""""""""""""""""""""""""""""""""""

If VisIt keeps asking for your "Password" in the dialog box below, and
you are entering your correct PIN + RSA token code, you might need to
select "Change username" and then enter your OLCF username when
prompted.

.. image:: /images/Screen-Shot-2016-01-06-at-11.10.19-AM.png
   :width: 330px
   :height: 125px

This will give you a new opportunity to enter your PIN + token code and
your username will appear in login request box as shown below. If you
want you OLCF username to be filled in by default, go to "Options→Host
profiles" and enter it under "Username". See the `Modifying Host
Profiles </for-users/system-user-guides/rhea/analysis-tools/#modifying-host-profiles>`__
section below for more details.

.. image:: /images/Screen-Shot-2016-01-06-at-11.06.25-AM1.png
   :width: 360px
   :height: 125px

VisIt will not connect when you try to draw an image.
"""""""""""""""""""""""""""""""""""""""""""""""""""""

If VisIt will not connect to Rhea when you try to draw an image, you
should login to Rhea and enter "qstat" from the command line. Your VisIt
job should appear in the queue. If you see it in a state marked "Q" you
should wait a bit longer to see if it will start. If you do not see your
job listed in the queue, check to make sure your project ID is entered
in your VisIt host profile. See the `Modifying Host
Profiles </for-users/system-user-guides/rhea/analysis-tools/#modifying-host-profiles>`__
section below for instructions.

Modifying Host Profiles
^^^^^^^^^^^^^^^^^^^^^^^

To make changes to an exiting host profile, do the following:

-  Go to "Options→Host Profiles".
-  The window will display the known hosts on the left, with the
   settings for that host shown on the right in the "Host Settings" tab.
-  You can modify settings relevant to this host machine. For example,
   you can change the "Username" field if your OLCF username differs
   from your local computer username.
-  Once you have made your changes, press the "Apply" button, and then
   save the settings (Options/Save Settings).

Each host can have several launch profiles. A launch profile specifies
VisIt can be run on a given host computer. To make changes to a host's
launch profile, do the following:

-  Go to "Options→Host Profiles".
-  Select the host in the left side of the window.
-  Select the "Launch Profiles" tab in the right side of the window.
   This will display the known launch profiles for this host.
-  Select a "Launch Profile" and the settings are displayed in the tabs
   below.
-  You can set your Project ID in the "Default Bank/Account" field in
   the "Parallel" tab.
-  You can change the queue used by modifying the "Partition/Pool/Queue"
   field in the "Parallel" tab.
-  Once you have made your changes, press the "Apply" button, and then
   save the settings (Options/Save Settings).

Remote Visualization using VNC (non-GPU)
----------------------------------------

In addition to the instructions below, `Benjamin
Hernandez </directory/staff-member/benjamin-hernandez/>`__ of the `OLCF
Advanced Data and Workflows
Group </about-olcf/olcf-groups/advanced-data-and-workflows/>`__
presented a related talk, `GPU Rendering in Rhea and
Titan </wp-content/uploads/2016/01/GPURenderingRheaTitan-1.pdf>`__,
during the 2016 OLCF User Meeting.

step 1 (local system)
^^^^^^^^^^^^^^^^^^^^^

Install a vncviewer (turbovnc, tigervnc, etc.) on your local machine.
When running vncviewer for the first time, it will ask to set a password
for this and future vnc sessions.

step 2 (terminal 1)
^^^^^^^^^^^^^^^^^^^

From a Rhea connection launch a batch job and execute the below
matlab-vnc.sh script to start the vncserver and run matlab within:

#. localsytem: ssh -X @rhea.ccs.ornl.gov
#. rhea: qsub -I -A abc123 -X -l nodes=1,walltime=01:00:00
#. rhea: ./matlab-vnc.sh

.. code::

    ./matlab-vnc.sh
    New 'rhea6:1 (userA)' desktop is rhea6:1

    Starting applications specified in /ccs/home/userA/.vnc/xstartup
    Log file is /ccs/home/userA/.vnc/rhea6:1.log

    **************************************************************************
    Instructions

    In a new terminal, open a tunneling connection with rhea6 and port 5901
    example:
             userid@rhea.ccs.ornl.gov -L 5901:rhea6:5901
     **************************************************************************

    MATLAB is selecting SOFTWARE OPENGL rendering.

step 3 (terminal 2)
^^^^^^^^^^^^^^^^^^^

In a second terminal on your local system open a tunneling connection
following the instructions given by the vnc start-up script:

-  localsystem: ssh @rhea.ccs.ornl.gov -L 5901:rhea99:5901

step 4 (local system)
^^^^^^^^^^^^^^^^^^^^^

Launch the vncviewer. When you launch the vncviewer that you downloaded
you will need to specify ‘localhost:5901’. You will also set a passoword
for the initial connection or enter the created password for subsequent
connections.

matlab-vnc.sh (non-GPU rendering)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code::

    #!/bin/sh

    what()
    {
        hostname
    }
    echo "Starting vncserver"

    vncserver :1 -geometry 1920x1080  -depth 24

    echo
    echo
    echo "**************************************************************************"
    echo "Instructions"
    echo
    echo "In a new terminal, open a tunneling connection with $(what) and port 5901"
    echo "example:"
    echo  "         userid@rhea.ccs.ornl.gov -L 5901:$(what):5901 "
    echo
    echo "**************************************************************************"
    echo
    echo
    export DISPLAY=:1
    . /sw/rhea/environment-modules/3.2.10/rhel6.7_gnu4.4.7/init/sh
    module load matlab/R2016b
    matlab
    vncserver -kill :1

Remote Visualization using VNC (GPU nodes)
------------------------------------------

step 1 (local system)
^^^^^^^^^^^^^^^^^^^^^

Install a vncviewer (turbovnc, tigervnc, etc.) on your local machine.
When running vncviewer for the first time, it will ask to set a password
for this and future vnc sessions.

step 2 (terminal 1)
^^^^^^^^^^^^^^^^^^^

From a Rhea connection launch a batch job and execute the below
matlab-vnc.sh script to start the vncserver and run matlab within:

#. localsytem: ssh -X @rhea.ccs.ornl.gov
#. rhea: qsub -I -A abc123 -X -l nodes=1,walltime=01:00:00
   -lpartition=gpu
#. rhea: ./matlab-vnc.sh

.. code::

    ./matlab-vnc.sh
    New 'rhea6:1 (userA)' desktop is rhea6:1

    Starting applications specified in /ccs/home/userA/.vnc/xstartup
    Log file is /ccs/home/userA/.vnc/rhea6:1.log

    **************************************************************************
    Instructions

    In a new terminal, open a tunneling connection with rhea6 and port 5901
    example:
             userid@rhea.ccs.ornl.gov -L 5901:rhea6:5901
     **************************************************************************

    MATLAB is selecting SOFTWARE OPENGL rendering.

step 3 (terminal 2)
^^^^^^^^^^^^^^^^^^^

In a second terminal on your local system open a tunneling connection
following the instructions given by the vnc start-up script:

-  localsystem: ssh @rhea.ccs.ornl.gov -L 5901:rhea99:5901

step 4 (local system)
^^^^^^^^^^^^^^^^^^^^^

Launch the vncviewer. When you launch the vncviewer that you downloaded
you will need to specify ‘localhost:5901’. You will also set a passoword
for the initial connection or enter the created password for subsequent
connections.

vmd-vgl.sh (GPU rendering)
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code::

    #!/bin/sh

    what()
    {
        hostname
    }
    echo
    echo "Starting X"
    xinit &
    sleep 5
    echo "Starting vncserver"

    vncserver :1 -geometry 1920x1080  -depth 24

    echo
    echo
    echo "**************************************************************************"
    echo "Instructions"
    echo
    echo "In a new terminal, open a tunneling connection with $(what) and port 5901"
    echo "example:"
    echo  "         userid@rhea.ccs.ornl.gov -L 5901:$(what):5901 "
    echo
    echo "**************************************************************************"
    echo
    echo
    export DISPLAY=:1
    module load vmd/1.9.3
    vglrun vmd
    vncserver -kill :1

Remote Visualization using Nice DCV (GPU nodes only)
----------------------------------------------------

step 1 (terminal 1)
^^^^^^^^^^^^^^^^^^^

Launch an interactive job:

.. code::

     qsub -I -A projectID   -l nodes=1 -l walltime=00:30:00 -l partition=gpu

As of April 29, the dcv feature will be required:
.. code::

     qsub -I -A projectID   -l nodes=1 -l walltime=00:30:00 -l partition=gpu -l feature=dcv

Run the following commands:

.. code::

    xinit &
    export DISPLAY=:0
    dcv create-session --gl-display :0 mySessionName
    hostname  // will be used to open a tunneling connection with this node

step 1 (terminal 2)
^^^^^^^^^^^^^^^^^^^

Open a tunneling connection with gpu node ``N``, given by hostname:

.. code::

    ssh user@rhea.ccs.ornl.gov -L 8443:rhea-gpuN:8443

Open your web browser using the following link and use your credentials
to access OLCF systems: ``https://localhost:8443`` When finished, kill
the dcv session in first terminal:

.. code::

    dcv close-session mySessionName
    kill %1

