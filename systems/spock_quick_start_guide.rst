.. _spock-quick-start-guide:

***********************
Spock Quick-Start Guide
***********************

.. _spock-system-overview:

System Overview
===============

Spock is an NCCS moderate-security system that contains similar hardware and
software as the upcoming Frontier system. It is used as an early-access testbed
for Center for Accelerated Application Readiness (CAAR) and Exascale Computing
Project (ECP) teams as well as NCCS staff and our vendor partners. The system
has 3 cabinets, each containing 12 compute nodes, for a total of 36 compute
nodes.

.. _spock-compute-nodes:

Spock Compute Nodes
-------------------

Each Spock node consists of [1x] 64-core AMD EPYC 7662 "Rome" CPU (with 2
hardware threads per physical core) with access to 256 GB of DDR4 memory and
connected to [4x] AMD MI100 GPUs. The CPU is connected to all GPUs via PCIe
Gen4, allowing peak host-to-device (H2D) and device-to-host (D2H) data
transfers of 32+32 GB/s. The GPUs are connected in an all-to-all arrangement
via Infinity Fabric (xGMI), allowing for a peak device-to-device bandwidth of
46+46 GB/s. 

.. note::
    The X+X GB/s values for bandwidths above represent bi-directional bandwidths. So, for example, the Infinity Fabric connecting any two GPUs allows peak data transfers of 46 GB/s *in both directions simultaneously*.

.. image:: /images/Spock_Node.jpg
   :align: center
   :width: 100%
   :alt: Spock node architecture diagram

System Interconnect
-------------------

The Spock nodes are connected with Slingshot-10 providing a node injection
bandwidth of 12.5 GB/s.

File Systems
------------

Spock is connected to an IBM Spectrum Scale™ filesystem providing 250 PB of
storage capacity with a peak write speed of 2.5 TB/s. Spock also has access to
the center-wide NFS-based filesystem (which provides user and project home
areas). While Spock does not have *direct* access to the center’s High
Performance Storage System (HPSS) - for user and project archival storage -
users can log in to the :ref:`dtn-user-guide` to move data to/from HPSS.

GPUs
----

Spock contains a total of 144 AMD MI100 GPUs. The AMD MI100 GPU has a peak
performance of up to 11.5 TFLOPS in double-precision for modeling & simulation
and up to 184.6 TFLOPS in half-precision for machine learning and data
analytics. Each GPU contains 120 compute units (7680 stream processors) and 32
GB of high-bandwidth memory (HBM2) which can be accessed at speeds of up to 1.2
TB/s.

----

Connecting
==========

To connect to Spock, ``ssh`` to ``spock.olcf.ornl.gov``. For example:

.. code-block:: bash

    $ ssh username@spock.olcf.ornl.gov

For more information on connecting to OLCF resources, see :ref:`connecting-to-olcf`.

----

Data and Storage
================

For more detailed information about center-wide file systems and data archiving
available on Spock, please refer to the pages on
:ref:`data-storage-and-transfers`, but the two subsections below give a quick
overview of NFS and GPFS storage spaces.

NFS
---

+---------------------+---------------------------------------------+----------------+-------------+--------+---------+---------+------------+------------------+
| Area                | Path                                        | Type           | Permissions |  Quota | Backups | Purged  | Retention  | On Compute Nodes |
+=====================+=============================================+================+=============+========+=========+=========+============+==================+
| User Home           | ``/ccs/home/[userid]``                      | NFS            | User set    |  50 GB | Yes     | No      | 90 days    | Read-only        |
+---------------------+---------------------------------------------+----------------+-------------+--------+---------+---------+------------+------------------+
| Project Home        | ``/ccs/proj/[projid]``                      | NFS            | 770         |  50 GB | Yes     | No      | 90 days    | Read-only        |
+---------------------+---------------------------------------------+----------------+-------------+--------+---------+---------+------------+------------------+

GPFS
----

+---------------------+---------------------------------------------+----------------+-------------+--------+---------+---------+------------+------------------+
| Area                | Path                                        | Type           | Permissions |  Quota | Backups | Purged  | Retention  | On Compute Nodes |
+=====================+=============================================+================+=============+========+=========+=========+============+==================+
| Member Work         | ``/gpfs/alpine/[projid]/scratch/[userid]``  | Spectrum Scale | 700         |  50 TB | No      | 90 days | N/A        | Yes              |
+---------------------+---------------------------------------------+----------------+-------------+--------+---------+---------+------------+------------------+
| Project Work        | ``/gpfs/alpine/[projid]/proj-shared``       | Spectrum Scale | 770         |  50 TB | No      | 90 days | N/A        | Yes              |
+---------------------+---------------------------------------------+----------------+-------------+--------+---------+---------+------------+------------------+
| World Work          | ``/gpfs/alpine/[projid]/world-shared``      | Spectrum Scale | 775         |  50 TB | No      | 90 days | N/A        | Yes              |
+---------------------+---------------------------------------------+----------------+-------------+--------+---------+---------+------------+------------------+

----

Programming Environment
=======================

OLCF provides Spock users many pre-installed software packages and scientific
libraries. To facilitate this, environment management tools are used to handle
necessary changes to the shell.

Environment Modules (Lmod)
--------------------------

Environment modules are provided through `Lmod
<https://lmod.readthedocs.io/en/latest/>`__, a Lua-based module system for
dynamically altering shell environments. By managing changes to the shell’s
environment variables (such as ``PATH``, ``LD_LIBRARY_PATH``, and
``PKG_CONFIG_PATH``), Lmod allows you to alter the software available in your
shell environment without the risk of creating package and version combinations
that cannot coexist in a single environment.

General Usage
^^^^^^^^^^^^^

The interface to Lmod is provided by the ``module`` command:

+------------------------------------+-------------------------------------------------------------------------+
| Command                            | Description                                                             |
+====================================+=========================================================================+
| ``module -t list``                 | Shows a terse list of the currently loaded modules                      |
+------------------------------------+-------------------------------------------------------------------------+
| ``module avail``                   | Shows a table of the currently available modules                        |
+------------------------------------+-------------------------------------------------------------------------+
| ``module help <modulename>``       | Shows help information about ``<modulename>``                           |
+------------------------------------+-------------------------------------------------------------------------+
| ``module show <modulename>``       | Shows the environment changes made by the ``<modulename>`` modulefile   |
+------------------------------------+-------------------------------------------------------------------------+
| ``module spider <string>``         | Searches all possible modules according to ``<string>``                 |
+------------------------------------+-------------------------------------------------------------------------+
| ``module load <modulename> [...]`` | Loads the given ``<modulename>``\(s) into the current environment       |
+------------------------------------+-------------------------------------------------------------------------+
| ``module use <path>``              | Adds ``<path>`` to the modulefile search cache and ``MODULESPATH``      |
+------------------------------------+-------------------------------------------------------------------------+
| ``module unuse <path>``            | Removes ``<path>`` from the modulefile search cache and ``MODULESPATH`` |
+------------------------------------+-------------------------------------------------------------------------+
| ``module purge``                   | Unloads all modules                                                     |
+------------------------------------+-------------------------------------------------------------------------+
| ``module reset``                   | Resets loaded modules to system defaults                                |
+------------------------------------+-------------------------------------------------------------------------+
| ``module update``                  | Reloads all currently loaded modules                                    |
+------------------------------------+-------------------------------------------------------------------------+

Searching for Modules
^^^^^^^^^^^^^^^^^^^^^

Modules with dependencies are only available when the underlying dependencies,
such as compiler families, are loaded. Thus, module avail will only display
modules that are compatible with the current state of the environment. To
search the entire hierarchy across all possible dependencies, the ``spider``
sub-command can be used as summarized in the following table.

+------------------------------------------+--------------------------------------------------------------------------------------+
| Command                                  | Description                                                                          |
+==========================================+======================================================================================+
| ``module spider``                        | Shows the entire possible graph of modules                                           |
+------------------------------------------+--------------------------------------------------------------------------------------+
| ``module spider <modulename>``           | Searches for modules named ``<modulename>`` in the graph of possible modules         |
+------------------------------------------+--------------------------------------------------------------------------------------+
| ``module spider <modulename>/<version>`` | Searches for a specific version of ``<modulename>`` in the graph of possible modules |
+------------------------------------------+--------------------------------------------------------------------------------------+
| ``module spider <string>``               | Searches for modulefiles containing ``<string>``                                     |
+------------------------------------------+--------------------------------------------------------------------------------------+

Compilers
---------

Cray, AMD, and GCC compilers are provided through modules on Spock. The Cray
and AMD compilers are both based on LLVM/Clang. There are also system/OS
versions of both Clang and GCC available in ``/usr/bin``. The table below lists
details about each of the module-provided compilers.

.. note::

    It is highly recommended to use the Cray compiler wrappers (``cc``, ``CC``, and ``ftn``) whenever possible. See the next section for more details.


+--------+-------------------------+-----------------+----------+-------------------+---------------------------------+
| Vendor | Programming Environment | Compiler Module | Language | Compiler Wrapper  | Compiler                        |
+========+=========================+=================+==========+===================+=================================+ 
| Cray   | ``PrgEnv-cray``         | ``cce``         | C        | ``cc``            | ``craycc``                      |
|        |                         |                 +----------+-------------------+---------------------------------+
|        |                         |                 | C++      | ``CC``            | ``craycxx`` or ``crayCC``       |
|        |                         |                 +----------+-------------------+---------------------------------+
|        |                         |                 | Fortran  | ``ftn``           | ``crayftn``                     |
+--------+-------------------------+-----------------+----------+-------------------+---------------------------------+
| AMD    | Not yet available       | ``rocm``        | C        | Not yet available | ``$ROCM_PATH/llvm/bin/clang``   |
|        |                         |                 +----------+-------------------+---------------------------------+
|        |                         |                 | C++      | Not yet available | ``$ROCM_PATH/llvm/bin/clang++`` |
|        |                         |                 +----------+-------------------+---------------------------------+
|        |                         |                 | Fortran  | Not yet available | ``$ROCM_PATH/llvm/bin/flang``   |
+--------+-------------------------+-----------------+----------+-------------------+---------------------------------+
| GCC    | ``PrgEnv-gnu``          | ``gcc``         | C        | ``cc``            | ``$GCC_PATH/bin/gcc``           |
|        |                         |                 +----------+-------------------+---------------------------------+
|        |                         |                 | C++      | ``CC``            | ``$GCC_PATH/bin/g++``           |
|        |                         |                 +----------+-------------------+---------------------------------+
|        |                         |                 | Fortran  | ``ftn``           | ``$GCC_PATH/bin/gfortran``      |
+--------+-------------------------+-----------------+----------+-------------------+---------------------------------+


Cray Programming Environment and Compiler Wrappers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Cray provides ``PrgEnv-<compiler>`` modules (e.g., ``PrgEnv-cray``) that load
compatible components of a specific compiler toolchain. The components include
the specified compiler as well as MPI, LibSci, and other libraries. Loading the
``PrgEnv-<compiler>`` modules also defines a set of compiler wrappers for that
compiler toolchain that automatically add include paths and link in libraries
for Cray software. Compiler wrappers are provided for C (``cc``), C++ (``CC``),
and Fortran (``ftn``).

.. note::
   Use the ``-craype-verbose`` flag to display the full include and link information used by the Cray compiler wrappers. This must be called on a file to see the full output (e.g., ``CC -craype-verbose test.cpp``).

MPI
---

The MPI implementation available on Spock is Cray's MPICH, which is "GPU-aware"
so GPU buffers can be passed directly to MPI calls.

----

Compiling
=========

This section covers how to compile for different programming models using the
different compilers covered in the previous section.

MPI
---

+----------------+----------------+-----------------------------------------------------+-------------------------------------------------------------------------------+
| Implementation | Module         | Compiler                                            | Header Files & Linking                                                        | 
+================+================+=====================================================+===============================================================================+
| Cray MPICH     | ``cray-mpich`` | ``cc``, ``CC``, ``ftn`` (Cray compiler wrappers)    | MPI header files and linking is built into the Cray compiler wrappers         |
|                |                +-----------------------------------------------------+-------------------------------------------------------------------------------+
|                |                | ``hipcc``                                           | | ``-L$(MPICH_DIR)/lib -lmpi``                                                |
|                |                |                                                     | | ``-I$(MPICH_DIR)/include``                                                  |
+----------------+----------------+-----------------------------------------------------+-------------------------------------------------------------------------------+


GPU-Aware MPI
^^^^^^^^^^^^^

To use GPU-aware Cray MPICH, there are currently some extra steps needed in addition to the table above, which depend on the compiler that is used.

1. Compiling with the Cray compiler wrappers, ``cc`` or ``CC``
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

To use GPU-aware Cray MPICH with the Cray compiler wrappers, users must load specific modules, set some environment variables, and include appropriate headers and libraries. The following modules and environment variables must be set:

.. code:: bash

    module load craype-accel-amd-gfx908
    module load PrgEnv-cray
    module load rocm

    ## These must be set before compiling so the executable picks up GTL
    export PE_MPICH_GTL_DIR_amd_gfx908="-L/opt/cray/pe/mpich/8.1.4/gtl/lib"
    export PE_MPICH_GTL_LIBS_amd_gfx908="-lmpi_gtl_hsa"

    ## These must be set before running
    export MPIR_CVAR_GPU_EAGER_DEVICE_MEM=0
    export MPICH_GPU_SUPPORT_ENABLED=1

In addition, the following header files and libraries must be included:

.. code:: bash

    -I${ROCM_PATH}/include
    -L${ROCM_PATH}/lib -lamdhip64 -lhsa-runtime64

where the include path implies that ``#include <hip/hip_runtime.h>`` is included in the source file.

2. Compiling with ``hipcc``
"""""""""""""""""""""""""""

To use GPU-aware Cray MPICH with ``hipcc``, users must load specific modules, set some environment variables, and include appropriate headers and libraries. The following modules and environment variables must be set:

.. code:: bash

    module load craype-accel-amd-gfx908
    module load PrgEnv-cray
    module load rocm

    ## These must be set before running
    export MPIR_CVAR_GPU_EAGER_DEVICE_MEM=0
    export MPICH_GPU_SUPPORT_ENABLED=1

In addition, the following header files and libraries must be included:

.. code:: bash

    -I${MPICH_DIR}/include
    -L${MPICH_DIR}/lib -lmpi -L/opt/cray/pe/mpich/8.1.4/gtl/lib -lmpi_gtl_hsa
    
OpenMP
------

This section shows how to compile with OpenMP using the different compilers
covered above.

+--------+----------+-----------+-------------------------------------------+-------------------------------------+
| Vendor | Module   | Language  | Compiler                                  | OpenMP flag (CPU thread)            |
+========+==========+===========+===========================================+=====================================+
| Cray   | ``cce``  | C, C\+\+  | | ``cc``                                  | ``-fopenmp``                        |
|        |          |           | | ``CC``                                  |                                     |
|        |          +-----------+-------------------------------------------+-------------------------------------+
|        |          | Fortran   | ``ftn``                                   | | ``-homp``                         | 
|        |          |           |                                           | | ``-fopenmp`` (alias)              |
+--------+----------+-----------+-------------------------------------------+-------------------------------------+
| AMD    | ``rocm`` | | C       | | ``$ROCM_PATH/llvm/bin/clang``           | ``-fopenmp``                        |
|        |          | | C++     | | ``$ROCM_PATH/llvm/bin/clang++``         |                                     |
|        |          | | Fortran | | ``ROCM_PATH/llvm/bin/flang``            |                                     |
+--------+----------+-----------+-------------------------------------------+-------------------------------------+
| GCC    | ``gcc``  | | C       | | ``$GCC_PATH/bin/gcc``                   | ``-fopenmp``                        |
|        |          | | C++     | | ``$GCC_PATH/bin/g++``                   |                                     |
|        |          | | Fortran | | ``$GCC_PATH/bin/gfortran``              |                                     |
+--------+----------+-----------+-------------------------------------------+-------------------------------------+

OpenMP GPU Offload
------------------

This section shows how to compile with OpenMP Offload using the different compilers covered above. 

.. note::

    Make sure the ``craype-accel-amd-gfx908`` module is loaded when using OpenMP offload.

+--------+----------+-----------+-------------------------------------------+----------------------------------------------+
| Vendor | Module   | Language  | Compiler                                  | OpenMP flag (GPU)                            |
+========+==========+===========+===========================================+==============================================+
| Cray   | ``cce``  | C         | | ``cc``                                  | ``-fopenmp``                                 |
|        |          | C\+\+     | | ``CC``                                  |                                              |
|        |          +-----------+-------------------------------------------+----------------------------------------------+
|        |          | Fortran   | ``ftn``                                   | | ``-homp``                                  |
|        |          |           |                                           | | ``-fopenmp`` (alias)                       |
+--------+----------+-----------+-------------------------------------------+----------------------------------------------+
| AMD    | ``rocm`` | | C       | | ``$ROCM_PATH/llvm/bin/clang``           | | ``-fopenmp -target x86_64-pc-linux-gnu \`` |
|        |          | | C\+\+   | | ``$ROCM_PATH/llvm/bin/clang++``         | | ``-fopenmp-targets=amdgcn-amd-amdhsa   \`` |
|        |          | | Fortran | | ``ROCM_PATH/llvm/bin/flang``            | | ``-Xopenmp-target=amdgcn-amd-amdhsa    \`` |
|        |          |           | | ``hipcc``                               | | ``-march=gfx908``                          |
+--------+----------+-----------+-------------------------------------------+----------------------------------------------+
| GCC    | ``gcc``  | | C       | | ``$GCC_PATH/bin/gcc``                   | ``-fopenmp``                                 |
|        |          | | C++     | | ``$GCC_PATH/bin/g++``                   |                                              |
|        |          | | Fortran | | ``$GCC_PATH/bin/gfortran``              |                                              |
+--------+----------+-----------+-------------------------------------------+----------------------------------------------+

HIP
---

This section shows how to compile HIP codes using the Cray compiler wrappers and ``hipcc`` compiler driver.

.. note::

    Make sure the ``craype-accel-amd-gfx908`` module is loaded when using HIP.

+-----------+--------------------------------------------------------------------------------------------------------------------------+
| Compiler  | Compile/Link Flags, Header Files, and Libraries                                                                          |
+===========+==========================================================================================================================+
| ``CC``    | | ``CFLAGS = -std=c++11 -D__HIP_ROCclr__ -D__HIP_ARCH_GFX908__=1 --rocm-path=${ROCM_PATH} --offload-arch=gfx908 -x hip`` |
|           | | ``LFLAGS = -std=c++11 -D__HIP_ROCclr__ --rocm-path=${ROCM_PATH}``                                                      |
|           | | ``-I${HIP_PATH}/include``                                                                                              |
|           | | ``-L${HIP_PATH}/lib -lamdhip64``                                                                                       |
+-----------+--------------------------------------------------------------------------------------------------------------------------+
| ``hipcc`` | | Can be used directly to compile HIP source files.                                                                      |
|           | | To see what is being invoked within this compiler driver, issue the command, ``hipcc --verbose``                       |
+-----------+--------------------------------------------------------------------------------------------------------------------------+

----

Running Jobs
============

This section describes how to run programs on the Spock compute nodes,
including a brief overview of Slurm and also how to map processes and threads
to CPU cores and GPUs.

Slurm Workload Manager
----------------------

`Slurm <https://slurm.schedmd.com/>`__ is the workload manager used to interact
with the compute nodes on Spock. In the following subsections, the most
commonly used Slurm commands for submitting, running, and monitoring jobs will
be covered, but users are encouraged to visit the official documentation and
man pages for more information.

Batch Scheduler and Job Launcher
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Slurm provides 3 ways of submitting and launching jobs on Spock's compute
nodes: batch  scripts, interactive, and single-command. The Slurm commands
associated with these methods are shown in the table below and examples of
their use can be found in the related subsections.

+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``sbatch`` | | Used to submit a batch script to allocate a Slurm job allocation. The script contains options preceded with ``#SBATCH``.                                                   |
|            | | (see Batch Scripts section below)                                                                                                                                          |
+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``salloc`` | | Used to allocate an interactive Slurm job allocation, where one or more job steps (i.e., ``srun`` commands) can then be launched on the allocated resources (i.e., nodes). |
|            | | (see Interactive Jobs section below)                                                                                                                                       |
+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``srun``   | | Used to run a parallel job (job step) on the resources allocated with sbatch or ``salloc``.                                                                                |
|            | | If necessary, srun will first create a resource allocation in which to run the parallel job(s).                                                                            |
|            | | (see Single Command section below)                                                                                                                                         |
+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+ 

Batch Scripts
"""""""""""""

A batch script can be used to submit a job to run on the compute nodes at a
later time. In this case, stdout and stderr will be written to a file(s) that
can be opened after the job completes. Here is an example of a simple batch
script:

.. code-block:: bash
   :linenos:

   #!/bin/bash
   #SBATCH -A <project_id>
   #SBATCH -J <job_name>
   #SBATCH -o %x-%j.out
   #SBATCH -t 00:05:00
   #SBATCH -p <partition> 
   #SBATCH -N 2
 
   srun -n4 --ntasks-per-node=2 ./a.out 

The Slurm submission options are preceded by ``#SBATCH``, making them appear as
comments to a shell (since comments begin with ``#``). Slurm will look for
submission options from the first line through the first non-comment line.
Options encountered after the first non-comment line will not be read by Slurm.
In the example script, the lines are:

+------+-------------------------------------------------------------------------------+
| Line | Description                                                                   |
+======+===============================================================================+ 
| 1    | [Optional] shell interpreter line                                             |
+------+-------------------------------------------------------------------------------+ 
| 2    | OLCF project to charge                                                        |
+------+-------------------------------------------------------------------------------+ 
| 3    | Job name                                                                      |
+------+-------------------------------------------------------------------------------+ 
| 4    | stdout file name ( ``%x`` represents job name, ``%j`` represents job id)      |
+------+-------------------------------------------------------------------------------+ 
| 5    | Walltime requested (``HH:MM:SS``)                                             |
+------+-------------------------------------------------------------------------------+ 
| 6    | Batch queue                                                                   |
+------+-------------------------------------------------------------------------------+ 
| 7    | Number of compute nodes requested                                             |
+------+-------------------------------------------------------------------------------+ 
| 8    | Blank line                                                                    |
+------+-------------------------------------------------------------------------------+
| 9    | ``srun`` command to launch parallel job (requesting 4 processes - 2 per node) | 
+------+-------------------------------------------------------------------------------+

.. _interactive:

Interactive Jobs
""""""""""""""""

To request an interactive job where multiple job steps (i.e., multiple srun
commands) can be launched on the allocated compute node(s), the ``salloc``
command can be used:

.. code-block:: bash
   
   $ salloc -A <project_id> -J <job_name> -t 00:05:00 -p <partition> -N 2
   salloc: Granted job allocation 4258
   salloc: Waiting for resource configuration
   salloc: Nodes spock[10-11] are ready for job
 
   $ srun -n 4 --ntasks-per-node=2 ./a.out
   <output printed to terminal>
 
   $ srun -n 2 --ntasks-per-node=1 ./a.out
   <output printed to terminal>
   
Here, ``salloc`` is used to request an allocation of 2 MI100 compute nodes for
5 minutes. Once the resources become available, the user is granted access to
the compute nodes (``spock10`` and ``spock11`` in this case) and can launch job
steps on them using srun. 

.. _single-command:

Single Command (non-interactive)
""""""""""""""""""""""""""""""""

.. code-block:: bash

   $ srun -A <project_id> -t 00:05:00 -p <partition> -N 2 -n 4 --ntasks-per-node=2 ./a.out
   <output printed to terminal>

The job name and output options have been removed since stdout/stderr are
typically desired in the terminal window in this usage mode.

Common Slurm Submission Options
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The table below summarizes commonly-used Slurm job submission options:

+--------------------------+--------------------------------+
| ``A <project_id>``       | Project ID to charge           |
+--------------------------+--------------------------------+
| ``-J <job_name>``        | Name of job                    |
+--------------------------+--------------------------------+
| ``-p <partition>``       | Partition / batch queue        |
+--------------------------+--------------------------------+
| ``-t <time>``            | Wall clock time <``HH:MM:SS``> |
+--------------------------+--------------------------------+
| ``-N <number_of_nodes>`` | Number of compute nodes        |
+--------------------------+--------------------------------+
| ``-o <file_name>``       | Standard output file name      |
+--------------------------+--------------------------------+
| ``-e <file_name>``       | Standard error file name       |
+--------------------------+--------------------------------+

For more information about these and/or other options, please see the
``sbatch`` man page.

Other Common Slurm Commands
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The table below summarizes commonly-used Slurm commands:

+--------------+---------------------------------------------------------------------------------------------------------------------------------+
| ``sinfo``    | | Used to view partition and node information.                                                                                  |
|              | | E.g., to view user-defined details about the caar queue:                                                                      |
|              | | ``sinfo -p caar -o "%15N %10D %10P %10a %10c %10z"``                                                                          | 
+--------------+---------------------------------------------------------------------------------------------------------------------------------+
| ``squeue``   | | Used to view job and job step information for jobs in the scheduling queue.                                                   |
|              | | E.g., to see all jobs from a specific user:                                                                                   |
|              | | ``squeue -l -u <user_id>``                                                                                                    |
+--------------+---------------------------------------------------------------------------------------------------------------------------------+
| ``sacct``    | | Used to view accounting data for jobs and job steps in the job accounting log (currently in the queue or recently completed). |
|              | | E.g., to see a list of specified information about all jobs submitted/run by a users since 1 PM on January 4, 2021:           |
|              | | ``sacct -u <username> -S 2021-01-04T13:00:00 -o "jobid%5,jobname%25,user%15,nodelist%20" -X``                                 |
+--------------+---------------------------------------------------------------------------------------------------------------------------------+
| ``scancel``  | | Used to signal or cancel jobs or job steps.                                                                                   |
|              | | E.g., to cancel a job:                                                                                                        |
|              | | ``scancel <jobid>``                                                                                                           | 
+--------------+---------------------------------------------------------------------------------------------------------------------------------+
| ``scontrol`` | | Used to view or modify job configuration.                                                                                     |
|              | | E.g., to place a job on hold:                                                                                                 |
|              | | ``scontrol hold <jobid>``                                                                                                     |  
+--------------+---------------------------------------------------------------------------------------------------------------------------------+

----

Slurm Compute Node Partitions
-----------------------------

Spock's compute nodes are separated into 2 Slurm partitions (queues): 1 for
CAAR projects and 1 for ECP projects. Please see the tables below for details.

.. note::
    If CAAR or ECP teams require a temporary exception to this policy, please
    email help@olcf.ornl.gov with your request and it will be given to the OLCF
    Resource Utilization Council (RUC) for review.

CAAR Partition
^^^^^^^^^^^^^^

The CAAR partition consists of 24 total compute nodes. On a per-project basis,
each user can have 1 running and 1 eligible job at a time, with no limit on the
number of jobs submitted.

+-----------------+--------------+
| Number of Nodes | Max Walltime |
+=================+==============+
| 1 - 4           | 3 hours      |
+-----------------+--------------+
| 5 - 16          | 1 hour       |
+-----------------+--------------+


ECP Partition
^^^^^^^^^^^^^

The ECP partition consists of 12 total compute nodes. On a per-project basis,
each user can have 1 running and 1 eligible job at a time, with up to 5 jobs
submitted.

+-----------------+--------------+
| Number of Nodes | Max Walltime |
+=================+==============+
| 1 - 4           | 3 hours      |
+-----------------+--------------+

Process and Thread Mapping
--------------------------

This section describes how to map processes (e.g., MPI ranks) and process threads (e.g., OpenMP threads) to the CPUs and GPUs on Spock. The :ref:`spock-compute-nodes` diagram will be helpful when reading this section to understand which hardware threads your processes and threads run on. 

CPU Mapping
^^^^^^^^^^^

In this sub-section, a simple MPI+OpenMP "Hello, World" program (`hello_mpi_omp <https://code.ornl.gov/olcf/hello_mpi_omp>`__) will be used to clarify the mappings. Slurm's :ref:`interactive` method was used to request an allocation of 1 compute node for these examples: ``salloc -A <project_id> -t 30 -p <parition> -N 1``

The ``srun`` options used in this section are (see ``man srun`` for more information):

+----------------------------------+-------------------------------------------------------------------------------------------------------+
| ``-c, --cpus-per-task=<ncpus>``  | | Request that ``ncpus`` be allocated per process (default is 1).                                     |
|                                  | | (``ncpus`` refers to hardware threads)                                                              |
+----------------------------------+-------------------------------------------------------------------------------------------------------+
| ``--threads-per-core=<threads>`` | | In task layout, use the specified maximum number of threads per core                                |
|                                  | | (default is 1; there are 2 hardware threads per physical CPU core).                                 |
+----------------------------------+-------------------------------------------------------------------------------------------------------+
|  ``--cpu-bind=threads``          | | Bind tasks to CPUs.                                                                                 |
|                                  | | ``threads`` - Automatically generate masks binding tasks to threads.                                |
|                                  | | (Although this option is not explicitly used in these examples, it is the default CPU binding.)     |
+----------------------------------+-------------------------------------------------------------------------------------------------------+

.. note::

    In the ``srun`` man page (and so the table above), threads refers to hardware threads.

2 MPI ranks - each with 2 OpenMP threads
""""""""""""""""""""""""""""""""""""""""

In this example, the intent is to launch 2 MPI ranks, each of which spawn 2 OpenMP threads, and have all of the 4 OpenMP threads run on different physical CPU cores.

**First (INCORRECT) attempt**

To set the number of OpenMP threads spawned per MPI rank, the ``OMP_NUM_THREADS`` environment variable can be used. To set the number of MPI ranks launched, the ``srun`` flag ``-n`` can be used.

.. code-block:: bash

    $ export OMP_NUM_THREADS=2
    $ srun -n2 ./hello_mpi_omp | sort

    WARNING: Requested total thread count and/or thread affinity may result in
    oversubscription of available CPU resources!  Performance may be degraded.
    Explicitly set OMP_WAIT_POLICY=PASSIVE or ACTIVE to suppress this message.
    Set CRAY_OMP_CHECK_AFFINITY=TRUE to print detailed thread-affinity messages.
    WARNING: Requested total thread count and/or thread affinity may result in
    oversubscription of available CPU resources!  Performance may be degraded.
    Explicitly set OMP_WAIT_POLICY=PASSIVE or ACTIVE to suppress this message.
    Set CRAY_OMP_CHECK_AFFINITY=TRUE to print detailed thread-affinity messages.

    MPI 000 - OMP 000 - HWT 000 - Node spock01
    MPI 000 - OMP 001 - HWT 000 - Node spock01
    MPI 001 - OMP 000 - HWT 016 - Node spock01
    MPI 001 - OMP 001 - HWT 016 - Node spock01

The first thing to notice here is the ``WARNING`` about oversubscribing the available CPU cores. Also, the output shows each MPI rank did spawn 2 OpenMP threads, but both OpenMP threads ran on the same hardware thread (for a given MPI rank). This was not the intended behavior; each OpenMP thread was meant to run on its own physical CPU core.

**Second (CORRECT) attempt**

By default, each MPI rank is allocated only 1 hardware thread, so both OpenMP threads only have that 1 hardware thread to run on - hence the WARNING and undesired behavior. In order for each OpenMP thread to run on its own physical CPU core, each MPI rank should be given 2 hardware thread (``-c 2``) - since, by default, only 1 hardware thread per physical CPU core is enabled (this would need to be ``-c 4`` if ``--threads-per-core=2`` instead of the default of ``1``. The OpenMP threads will be mapped to unique physical CPU cores unless there are not enough physical CPU cores available, in which case the remaining OpenMP threads will share hardware threads and a WARNING will be issued as shown in the previous example.

.. code-block:: bash

    $ export OMP_NUM_THREADS=2
    $ srun -n2 -c2 ./hello_mpi_omp | sort

    MPI 000 - OMP 000 - HWT 000 - Node spock13
    MPI 000 - OMP 001 - HWT 001 - Node spock13
    MPI 001 - OMP 000 - HWT 016 - Node spock13
    MPI 001 - OMP 001 - HWT 017 - Node spock13


Now the output shows that each OpenMP thread ran on (one of the hardware threads of) its own physical CPU cores. More specifically (see the Spock Compute Node diagram), OpenMP thread 000 of MPI rank 000 ran on hardware thread 000 (i.e., physical CPU core 00), OpenMP thread 001 of MPI rank 000 ran on hardware thread 001 (i.e., physical CPU core 01), OpenMP thread 000 of MPI rank 001 ran on hardware thread 016 (i.e., physical CPU core 16), and OpenMP thread 001 of MPI rank 001 ran on hardware thread 017 (i.e., physical CPU core 17) - as expected.

.. note::

    There are many different ways users might choose to perform these mappings, so users are encouraged to clone the ``hello_mpi_omp`` program and test whether or not processes and threads are running where intended.

GPU Mapping
^^^^^^^^^^^

In this sub-section, an MPI+OpenMP+CUDA "Hello, World" program (`hello_jobstep <https://code.ornl.gov/olcf/hello_jobstep>`__) will be used to clarify the GPU mappings. Again, Slurm's :ref:`interactive` method was used to request an allocation of 1 compute node for these examples: ``salloc -A <project_id> -t 30 -p <parition> -N 1``

There are many combinations of ``srun`` options that could be used to map MPI ranks to GPUs, but only the ones listed in the table below will be used in these examples. See ``man srun`` for more information.

+-------------------------------+---------------------------------------------------------------------------------------------+
| ``--ntasks-per-gpu=<ntasks>`` | Request that there are ntasks tasks invoked for every GPU.                                  |
+-------------------------------+---------------------------------------------------------------------------------------------+
| ``--gpu-bind=map_gpu:<list>`` | Bind tasks to specific GPUs by setting GPU masks on tasks (or ranks) as specified where     |
|                               | ``<list>`` is ``<gpu_id_for_task_0>,<gpu_id_for_task_1>,...``. If the number of tasks (or   |
|                               | ranks) exceeds the number of elements in this list, elements in the list will be reused as  |
|                               | needed starting from the beginning of the list. To simplify support for large task          |
|                               | counts, the lists may follow a map with an asterisk and repetition count. (For example      |
|                               | ``map_gpu:0*4,1*4``)                                                                        |
+-------------------------------+---------------------------------------------------------------------------------------------+

4 MPI ranks - each with 2 OpenMP threads and 1 GPU
""""""""""""""""""""""""""""""""""""""""""""""""""

In this example, the intent is to launch 4 MPI ranks, each of which spawn 2 OpenMP threads, and have all of the 8 OpenMP threads run on different physical CPU cores. In addition, each MPI rank (and its 2 OpenMP threads) should have access to only 1 GPU.

The CPU mapping part of this example is very similar to the example used above in the CPU Mapping sub-section, so the focus here is on the GPU mapping part. The GPU mapping can, of course, be done in different ways. For example, an application might map MPI ranks to GPUs programmatically within the code using, say, ``hipSetDevice``. In this case, since all GPUs on a node are available to all MPI ranks on that node by default, there might not be a need to map to GPUs using Slurm (just do it in the code). However, in another application, there might be a reason to make only a subset of GPUs available to the MPI ranks on a node. It is this latter case that the following examples refer to.

Similar to the CPU Mapping example, this example uses 4 MPI ranks (``-n 4``), each with 2 physical CPU cores (``-c 2``, again, since by default, only 1 of the 2 hardware threads per physical CPU core is enabled) to launch 2 OpenMP threads (``OMP_NUM_THREADS=2``) on. There are multiple combinations of ``srun`` options that could be used to map MPI ranks to a single GPU, but only the ``--ntasks-per-gpu`` and ``--gpu-bind=map_gpu`` options will be used here. Without additional flags, all MPI ranks would have access to all GPUs (which is the default behavior).

**Example 1: Map 1 task per GPU**

.. code-block:: bash

    $ export OMP_NUM_THREADS=2
    $ srun -n4 -c2 --ntasks-per-gpu=1 ./hello_jobstep | sort

    MPI 000 - OMP 000 - HWT 000 - Node spock13 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 000 - OMP 001 - HWT 001 - Node spock13 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 001 - OMP 000 - HWT 016 - Node spock13 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 001 - OMP 001 - HWT 017 - Node spock13 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 002 - OMP 000 - HWT 032 - Node spock13 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID 48
    MPI 002 - OMP 001 - HWT 033 - Node spock13 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID 48
    MPI 003 - OMP 000 - HWT 048 - Node spock13 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID 09
    MPI 003 - OMP 001 - HWT 049 - Node spock13 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID 09

The output contains different IDs associated with the GPUs so it is important to describe these IDs before moving on. ``GPU_ID`` is the node-level (or global) GPU ID, which is labeled as one might expect from looking at a node diagram: 0, 1, 2, 3. ``RT_GPU_ID`` is the HIP runtime GPU ID, which can be thought of as each MPI rank's local GPU ID numbering (with zero-based indexing). So in the output above, each MPI rank has access to 1 unique GPU - where MPI 000 has access to GPU 0, MPI 001 has access to GPU 1, etc., but all MPI ranks show a HIP runtime GPU ID of 0. The reason is that each MPI rank only "sees" one GPU and so the HIP runtime labels it as "0", even though it might be global GPU ID 0, 1, 2, or 3. The GPU's bus ID is included to definitively show that different GPUs are being used. 

The different GPU IDs reported by the example program are:

* ``GPU_ID`` is the node-level (or global) GPU ID read from ``ROCR_VISIBLE_DEVICES``. If this environment variable is not set (either by the user or by Slurm), the value of ``GPU_ID`` will be set to N/A.
* ``RT_GPU_ID`` is the HIP runtime GPU ID (as reported from, say ``hipGetDevice``).
* ``Bus_ID`` is the physical bus ID associated with the GPUs. Comparing the bus IDs is meant to definitively show that different GPUs are being used.

**Example 2: Map 1 task to a specific GPU**

It is also possible to map MPI ranks to specific GPUs using the ``--gpu-bind=map_gpu`` option. The following job step would give the same results as Example 1 above:

.. code:: bash

    $ export OMP_NUM_THREADS=2
    $ srun -n4 -c2 --ntasks-per-gpu=1 --gpu-bind=map_gpu:0,1,2,3 ./hello_jobstep | sort

    MPI 000 - OMP 000 - HWT 000 - Node spock13 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 000 - OMP 001 - HWT 001 - Node spock13 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 001 - OMP 000 - HWT 016 - Node spock13 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 001 - OMP 001 - HWT 017 - Node spock13 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 002 - OMP 000 - HWT 032 - Node spock13 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID 48
    MPI 002 - OMP 001 - HWT 033 - Node spock13 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID 48
    MPI 003 - OMP 000 - HWT 048 - Node spock13 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID 09
    MPI 003 - OMP 001 - HWT 049 - Node spock13 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID 09

In the ``--gpu_bind=map_gpu`` option, the comma-separated list of GPU IDs specifies how the MPI ranks are mapped to GPUs. In this case, MPI ranks would be mapped as MPI 000 to GPU 0, MPI 001 to GPU 1, MPI 002 to GPU 2, MPI 003 to GPU 3. 

.. note::

    If there were 8 MPI ranks instead of 4, then the additional MPI ranks would wrap back around to map MPI 004 to GPU 0, MPI 005 to GPU 1, MPI 006 to GPU 2, and MPI 007 to GPU 3. However ``--ntasks-per-gpu=2`` would be needed since there would be 2 MPI ranks assigned to each GPU.

The ordering of the GPU mapping can also be changed with ``--gpu-bind=map_gpu`` to give results that could not be accomplished with ``--ntasks-per-gpu`` alone. For example:

.. code:: bash

    $ export OMP_NUM_THREADS=2
    $ srun -n4 -c2 --ntasks-per-gpu=1 --gpu-bind=map_gpu:3,2,1,0 ./hello_jobstep | sort

    MPI 000 - OMP 000 - HWT 000 - Node spock13 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID 09
    MPI 000 - OMP 001 - HWT 001 - Node spock13 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID 09
    MPI 001 - OMP 000 - HWT 016 - Node spock13 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID 48
    MPI 001 - OMP 001 - HWT 017 - Node spock13 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID 48
    MPI 002 - OMP 000 - HWT 032 - Node spock13 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 002 - OMP 001 - HWT 033 - Node spock13 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 003 - OMP 000 - HWT 048 - Node spock13 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 003 - OMP 001 - HWT 049 - Node spock13 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9


Here, notice that MPI 000 now maps to GPU 3, MPI 001 maps to GPU 2, etc.

Mapping multiple MPI ranks to a GPU
"""""""""""""""""""""""""""""""""""

It is also possible to use the ``--ntasks-per-gpu`` and the ``--gpu-bind=map_gpu`` options to map multiple MPI ranks to a single GPU.

.. code:: bash

    $ export OMP_NUM_THREADS=2
    $ srun -n4 -c2 --ntasks-per-gpu=2 --gpu-bind=map_gpu:0*2,1*2 ./hello_jobstep | sort

    MPI 000 - OMP 000 - HWT 000 - Node spock13 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 000 - OMP 001 - HWT 001 - Node spock13 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 001 - OMP 000 - HWT 016 - Node spock13 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 001 - OMP 001 - HWT 017 - Node spock13 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 002 - OMP 000 - HWT 032 - Node spock13 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 002 - OMP 001 - HWT 033 - Node spock13 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 003 - OMP 000 - HWT 048 - Node spock13 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 003 - OMP 001 - HWT 049 - Node spock13 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87


Here, the option ``--gpu-bind=map_gpu:0*2,1*2`` specifies that GPU 0 should be assigned to the first two MPI ranks and GPU 1 should be assigned to the next two MPI ranks.

If 8 MPI ranks are used instead, the next 2 MPI ranks would wrap back around to use GPU 0, and so on (and ``--ntasks-per-gpu`` would need to be set to ``4``):

.. code:: bash

    $ export OMP_NUM_THREADS=2
    $ srun -n8 -c2 --ntasks-per-gpu=4 --gpu-bind=map_gpu:0*2,1*2 ./hello_jobstep | sort

    MPI 000 - OMP 000 - HWT 000 - Node spock13 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 000 - OMP 001 - HWT 001 - Node spock13 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 001 - OMP 000 - HWT 016 - Node spock13 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 001 - OMP 001 - HWT 017 - Node spock13 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 002 - OMP 000 - HWT 032 - Node spock13 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 002 - OMP 001 - HWT 033 - Node spock13 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 003 - OMP 000 - HWT 048 - Node spock13 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 003 - OMP 001 - HWT 049 - Node spock13 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 004 - OMP 000 - HWT 002 - Node spock13 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 004 - OMP 001 - HWT 003 - Node spock13 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 005 - OMP 000 - HWT 018 - Node spock13 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 005 - OMP 001 - HWT 019 - Node spock13 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 006 - OMP 000 - HWT 034 - Node spock13 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 006 - OMP 001 - HWT 035 - Node spock13 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 007 - OMP 000 - HWT 050 - Node spock13 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 007 - OMP 001 - HWT 051 - Node spock13 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87


.. note::

    On AMD's MI100 GPUs, multi-process service (MPS) is not needed since multiple MPI ranks per GPU is supported natively.

Multiple GPUs per MPI rank
""""""""""""""""""""""""""

As mentioned previously, all GPUs are accessible by all MPI ranks by default, so it is possible to *programatically* map any combination of MPI ranks to GPUs. However, there is currently no way to use Slurm to map multiple GPUs to a single MPI rank. If this functionality is needed for an application, please submit a ticket by emailing help@olcf.ornl.gov.


.. note::

    There are many different ways users might choose to perform these mappings, so users are encouraged to clone the ``hello_jobstep`` program and test whether or not processes and threads are running where intended.

----

Getting Help
============

If you have problems or need helping running on Spock, please submit a ticket
by emailing help@olcf.ornl.gov.

----


Known Issues
============

.. JIRA_CONTENT_HERE
