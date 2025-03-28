.. _defiant-quick-start-guide:

*************************
Defiant Quick-Start Guide
*************************

.. _defiant-system-decommission:

Defiant System Decommission
===========================

.. warning::
        The OLCF test resource, Defiant, and its scratch filesystem, Polis, will be **decommissioned at 8:00am on April 21, 2025**.  Data remaining on Polis will be **permanently deleted** following the decommission.  Data owners are responsible for retrieving needed data prior to decommission, so we recommend that this is completed as soon as possible.  The replacement for Defiant is anticipated to enter service in June.  Please contact help@olcf.ornl.gov with any questions.


.. _defiant-system-overview:

System Overview
===============

Defiant is an NCCS open access system that contains similar hardware and
software as the Frontier system. It is one of the Advanced Computing
Ecosystem (ACE) testbeds and provides a sandbox for testing advances in
IRI workflows and patterns, emerging compute architectures and techniques for
HPC, emerging storage architectures and techniques for HPC, emerging network
architectures and techniques, cloudification of traditional HPC architectures.
The system has 3 cabinets, each containing 12 compute nodes, for a total of 36
compute nodes.

.. _defiant-compute-nodes:

Defiant Compute Nodes
---------------------

Each Defiant compute node consists of [1x] 64-core AMD EPYC 7662 "Rome" CPU (with
2 hardware threads per physical core) with access to 256 GB of DDR4 memory and
connected to [4x] AMD MI100 GPUs. The CPU is connected to all GPUs via PCIe
Gen4, allowing peak host-to-device (H2D) and device-to-host (D2H) data
transfers of 32+32 GB/s. The GPUs are connected in an all-to-all arrangement
via Infinity Fabric (xGMI), allowing for a peak device-to-device bandwidth of
46+46 GB/s. Each compute node also has [2x] 3.2 TB NVMe devices (SSDs) with
sequential read and write speeds of 6900 MB/s and 4200 MB/s, respectively.

.. note::
    The X+X GB/s values for bandwidths above represent bi-directional bandwidths.
    So, for example, the Infinity Fabric connecting any two GPUs allows peak data
    transfers of 46 GB/s *in both directions simultaneously*.

.. image:: /images/Defiant_Node.jpg
   :align: center
   :width: 100%
   :alt: Defiant node architecture diagram

.. note::
    There are 4 NUMA domains per node, that are defined as follows:

    * NUMA 0: hardware threads 000-015, 064-079 | GPU 0
    * NUMA 1: hardware threads 016-031, 080-095 | GPU 1
    * NUMA 2: hardware threads 032-047, 096-111 | GPU 2
    * NUMA 3: hardware threads 048-063, 112-127 | GPU 3

System Interconnect
-------------------

The Defiant nodes are connected with Slingshot-10 providing a node injection
bandwidth of 12.5 GB/s.

File Systems
------------

Defiant is connected to the Lustre Polis filesystem providing ~1.6 PB of usable
namespace (``/lustre/polis/``). 

Defiant also has access to
the center-wide NFS-based filesystem (which provides user and project home
areas) in ``/ccsopen/home/<username>``

..
  While Defiant does not have *direct* access to the center’s High
  Performance Storage System (HPSS) - for user and project archival storage -
  users can log in to the :ref:`dtn-user-guide` to move data to/from HPSS.

GPUs
----

Defiant contains a total of 144 AMD MI100 GPUs. The AMD MI100 GPU has a peak
performance of up to 11.5 TFLOPS in double-precision for modeling & simulation
and up to 184.6 TFLOPS in half-precision for machine learning and data
analytics. Each GPU contains 120 compute units (7680 stream processors) and 32
GB of high-bandwidth memory (HBM2) which can be accessed at speeds of up to 1.2
TB/s.

----

Connecting
==========

To connect to Defiant, first ``ssh`` to the jump server: ``flux.op.ccs.ornl.gov`` and then to the load balancer: ``defiant-login.ccs.ornl.gov``. For example:

.. code-block:: bash

    $ ssh username@flux.op.ccs.ornl.gov
    $ ssh username@defiant-login.ccs.ornl.gov

If the load balancer is unavailable, explicity define a login node with ``defiant-login[1-2].ccs.ornl.gov``. 
For more information on connecting to OLCF resources, see :ref:`connecting-to-olcf`.

----

Data and Storage
================

For more detailed information about center-wide file systems and data archiving
available on Defiant, please refer to the pages on
:ref:`data-storage-and-transfers`, but the two subsections below give a quick
overview of NFS and GPFS storage spaces.

NFS Filesystem
--------------

.. list-table:: NFS Filesystem
   :header-rows: 1

   * - Area
     - Path
     - Type
     - Permissions
     - Quota
     - Backups
     - Purge
     - Retention
     - On Compute Nodes
   * - User Home
     - ``/ccsopen/home/[userid]``
     - NFS
     - User set
     - 50 GB
     - Yes
     - No
     - 90 days
     - yes


.. note::
   Please not that this ``/ccsopen`` location is not the same NFS filesystem as
   found in other Open enclave systems like Odo. So files created on Defiant will not be available on
   on Odo.

Lustre Filesystem (Polis)
-------------------------

.. list-table:: Polis
   :header-rows: 1

   * - Area
     - Path
     - Type
     - Permissions
     - Quota
     - Backups
     - Purge
     - Retention
     - On Compute Nodes
   * - Member Work
     - ``/lustre/polis/[projid]/scratch/[userid]``
     - Lustre HPE ClusterStor
     - 700
     - 50 TB
     - No
     - 90 days
     - N/A
     - yes
   * - Project Work
     - ``/lustre/polis/[projid]/proj-shared``
     - Lustre HPE ClusterStor
     - 770
     - 50 TB
     - No
     - 90 days
     - N/A
     - yes
   * - World Work
     - ``/lustre/polis/[projid]/world-shared``
     - Lustre HPE ClusterStor
     - 770
     - 50 TB
     - No
     - 90 days
     - N/A
     - yes


Programming Environment
=======================

OLCF provides Defiant users many pre-installed software packages and scientific
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

Cray, AMD, and GCC compilers are provided through modules on Defiant. The Cray
and AMD compilers are both based on LLVM/Clang. The system GCC (version 7.5.0) compiler is also located in
``/usr/bin``. The table below lists details about each of the module-provided compilers.

.. note::

    It is highly recommended to use the Cray compiler wrappers (``cc``, ``CC``, and ``ftn``) whenever possible. See the next section for more details.


+--------+-------------------------+-----------------+----------+-------------------+------------------------------------+
| Vendor | Programming Environment | Compiler Module | Language | Compiler Wrapper  | Compiler                           |
+========+=========================+=================+==========+===================+====================================+ 
| Cray   | ``PrgEnv-cray``         | ``cce``         | C        | ``cc``            | ``craycc``                         |
|        |                         |                 +----------+-------------------+------------------------------------+
|        |                         |                 | C++      | ``CC``            | ``craycxx`` or ``crayCC``          |
|        |                         |                 +----------+-------------------+------------------------------------+
|        |                         |                 | Fortran  | ``ftn``           | ``crayftn``                        |
+--------+-------------------------+-----------------+----------+-------------------+------------------------------------+
| AMD    | ``PrgEnv-amd``          | ``amd``         | C        | ``cc``            | ``amdclang``                       |
|        |                         |                 +----------+-------------------+------------------------------------+
|        |                         |                 | C++      | ``CC``            | ``amdclang++``                     |
|        |                         |                 +----------+-------------------+------------------------------------+
|        |                         |                 | Fortran  | ``ftn``           | ``amdflang``                       |
+--------+-------------------------+-----------------+----------+-------------------+------------------------------------+
| GCC    | ``PrgEnv-gnu``          | ``gcc``         | C        | ``cc``            | ``$GCC_PATH/bin/gcc``              |
|        |                         |                 +----------+-------------------+------------------------------------+
|        |                         |                 | C++      | ``CC``            | ``$GCC_PATH/bin/g++``              |
|        |                         |                 +----------+-------------------+------------------------------------+
|        |                         |                 | Fortran  | ``ftn``           | ``$GCC_PATH/bin/gfortran``         |
+--------+-------------------------+-----------------+----------+-------------------+------------------------------------+


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
   Use the ``-craype-verbose`` flag to display the full include and link information
   used by the Cray compiler wrappers. This must be called on a file to see the full
   output (e.g., ``CC -craype-verbose test.cpp``).

MPI
---

The MPI implementation available on Defiant is Cray's MPICH, which is "GPU-aware"
so GPU buffers can be passed directly to MPI calls. Currently, Defiant has MPICH
versions 8.1.27 as default and 8.1.26 as an additional module.

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

.. warning::
  GPU Aware MPI is currently not working on Defiant. Your code should stage data on main
  memory before sending/receiving data via MPI. We are working on a fix.

To use GPU-aware Cray MPICH, there are currently some extra steps needed in
addition to the table above, which depend on the compiler that is used.

1. Compiling with the Cray compiler wrappers, ``cc`` or ``CC``
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

To use GPU-aware Cray MPICH with the Cray compiler wrappers, users must load
specific modules, set some environment variables, and include appropriate headers
and libraries. The following modules and environment variables must be set:

.. code:: bash

    module load craype-accel-amd-gfx908
    module load PrgEnv-cray
    module load amd-mixed

    ## These must be set before running
    export MPIR_CVAR_GPU_EAGER_DEVICE_MEM=0
    export MPICH_GPU_SUPPORT_ENABLED=1

In addition, the following header files and libraries must be included:

.. code:: bash

    -I${ROCM_PATH}/include
    -L${ROCM_PATH}/lib -lamdhip64 -lhsa-runtime64

where the include path implies that ``#include <hip/hip_runtime.h>`` is
included in the source file.

2. Compiling with ``hipcc``
"""""""""""""""""""""""""""

To use GPU-aware Cray MPICH with ``hipcc``, users must load specific modules,
set some environment variables, and include appropriate headers and libraries.
The following modules and environment variables must be set:

.. code:: bash

    module load craype-accel-amd-gfx908
    module load PrgEnv-cray
    module load amd

    ## These must be set before running
    export MPIR_CVAR_GPU_EAGER_DEVICE_MEM=0
    export MPICH_GPU_SUPPORT_ENABLED=1
    export MPICH_SMP_SINGLE_COPY_MODE=CMA

In addition, the following header files and libraries must be included:

.. code:: bash

    -I${MPICH_DIR}/include
    -L${MPICH_DIR}/lib -lmpi -L${CRAY_MPICH_ROOTDIR}/gtl/lib -lmpi_gtl_hsa


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
| AMD    | ``amd``  | | C       | | ``amdclang``                            | ``-fopenmp``                        |
|        |          | | C++     | | ``amdclang++``                          |                                     |
|        |          | | Fortran | | ``amdflang``                            |                                     |
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
| AMD    | ``amd``  | | C       | | ``amdclang``                            | | ``-fopenmp --target=x86_64-pc-linux-gnu \``|
|        |          | | C\+\+   | | ``amdclang++``                          | | ``-fopenmp-targets=amdgcn-amd-amdhsa   \`` |
|        |          | | Fortran | | ``amdflang``                            | | ``-Xopenmp-target=amdgcn-amd-amdhsa    \`` |
|        |          |           | | ``hipcc``                               | | ``-march=gfx908``                          |
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

This section describes how to run programs on the Defiant compute nodes,
including a brief overview of Slurm and also how to map processes and threads
to CPU cores and GPUs.

Slurm Workload Manager
----------------------

`Slurm <https://slurm.schedmd.com/>`__ is the workload manager used to interact
with the compute nodes on Defiant. In the following subsections, the most
commonly used Slurm commands for submitting, running, and monitoring jobs will
be covered, but users are encouraged to visit the official documentation and
man pages for more information.

Batch Scheduler and Job Launcher
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Slurm provides 3 ways of submitting and launching jobs on Defiant's compute
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
   salloc: Nodes defiant[10-11] are ready for job
 
   $ srun -n 4 --ntasks-per-node=2 ./a.out
   <output printed to terminal>
 
   $ srun -n 2 --ntasks-per-node=1 ./a.out
   <output printed to terminal>

Here, ``salloc`` is used to request an allocation of 2 MI100 compute nodes for
5 minutes. Once the resources become available, the user is granted access to
the compute nodes (``defiant10`` and ``defiant11`` in this case) and can launch job
steps on them using srun. 

.. _single-command-defiant:

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

Defiant's compute nodes are separated into 2 Slurm partitions (queues): 1 for
CPU jobs and 1 for GPU. Please see the tables below for details.

.. note::
   Hold for partition info.

Process and Thread Mapping
--------------------------

This section describes how to map processes (e.g., MPI ranks) and process 
threads (e.g., OpenMP threads) to the CPUs and GPUs on Defiant. The 
:ref:`defiant-compute-nodes` diagram will be helpful when reading this section
to understand which hardware threads your processes and threads run on. 

CPU Mapping
^^^^^^^^^^^

In this sub-section, a simple MPI+OpenMP "Hello, World" program 
(`hello_mpi_omp <https://code.ornl.gov/olcf/hello_mpi_omp>`__) will be used to
clarify the mappings. Slurm's :ref:`interactive` method was used to request an
allocation of 1 compute node for these examples: 
``salloc -A <project_id> -t 30 -p <parition> -N 1``

The ``srun`` options used in this section are (see ``man srun`` for more 
information):

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

    In the ``srun`` man page (and so the table above), threads refers 
    to hardware threads.

2 MPI ranks - each with 2 OpenMP threads
""""""""""""""""""""""""""""""""""""""""

In this example, the intent is to launch 2 MPI ranks, each of which spawn 
2 OpenMP threads, and have all of the 4 OpenMP threads run on different 
physical CPU cores.

**First (INCORRECT) attempt**

To set the number of OpenMP threads spawned per MPI rank, the 
``OMP_NUM_THREADS`` environment variable can be used. To set the number 
of MPI ranks launched, the ``srun`` flag ``-n`` can be used.

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

    MPI 000 - OMP 000 - HWT 000 - Node defiant01
    MPI 000 - OMP 001 - HWT 000 - Node defiant01
    MPI 001 - OMP 000 - HWT 016 - Node defiant01
    MPI 001 - OMP 001 - HWT 016 - Node defiant01

The first thing to notice here is the ``WARNING`` about oversubscribing the 
available CPU cores. Also, the output shows each MPI rank did spawn 2 OpenMP
threads, but both OpenMP threads ran on the same hardware thread (for a given
MPI rank). This was not the intended behavior; each OpenMP thread was meant
to run on its own physical CPU core.

**Second (CORRECT) attempt**

By default, each MPI rank is allocated only 1 hardware thread, so both OpenMP
threads only have that 1 hardware thread to run on - hence the WARNING and 
undesired behavior. In order for each OpenMP thread to run on its own physical
CPU core, each MPI rank should be given 2 hardware thread (``-c 2``) - since,
by default, only 1 hardware thread per physical CPU core is enabled (this would
need to be ``-c 4`` if ``--threads-per-core=2`` instead of the default of ``1``.
The OpenMP threads will be mapped to unique physical CPU cores unless there are
not enough physical CPU cores available, in which case the remaining OpenMP
threads will share hardware threads and a WARNING will be issued as shown in
the previous example.

.. code-block:: bash

    $ export OMP_NUM_THREADS=2
    $ srun -n2 -c2 ./hello_mpi_omp | sort

    MPI 000 - OMP 000 - HWT 000 - Node defiant13
    MPI 000 - OMP 001 - HWT 001 - Node defiant13
    MPI 001 - OMP 000 - HWT 016 - Node defiant13
    MPI 001 - OMP 001 - HWT 017 - Node defiant13


Now the output shows that each OpenMP thread ran on (one of the hardware
threads of) its own physical CPU cores. More specifically (see the Defiant
Compute Node diagram), OpenMP thread 000 of MPI rank 000 ran on hardware thread
000 (i.e., physical CPU core 00), OpenMP thread 001 of MPI rank 000 ran on
hardware thread 001 (i.e., physical CPU core 01), OpenMP thread 000 of MPI
rank 001 ran on hardware thread 016 (i.e., physical CPU core 16), and OpenMP
thread 001 of MPI rank 001 ran on hardware thread 017 (i.e., physical CPU core
17) - as expected.

.. note::

    There are many different ways users might choose to perform these mappings,
    so users are encouraged to clone the ``hello_mpi_omp`` program and test
    whether or not processes and threads are running where intended.

GPU Mapping
^^^^^^^^^^^

In this sub-section, an MPI+OpenMP+HIP "Hello, World" program
(`hello_jobstep <https://code.ornl.gov/olcf/hello_jobstep>`__) will be used to
clarify the GPU mappings. Again, Slurm's :ref:`interactive` method was used to
request an allocation of 2 compute node for these examples:
``salloc -A <project_id> -t 30 -p <parition> -N 2``. The CPU mapping part of
this example is very similar to the example used above in the CPU Mapping 
sub-section, so the focus here will be on the GPU mapping part.

The following ``srun`` options will be used in the examples below. See 
``man srun`` for a complete list of options and more information.

+------------------------------------------------+--------------------------------------------------------------------------------------------------------------+
| ``--gpus-per-task``                            | Specify the number of GPUs required for the job on each task to be spawned in the job's resource allocation. |
+------------------------------------------------+--------------------------------------------------------------------------------------------------------------+
| ``--gpu-bind=closest``                         | Binds each task to the GPU which is on the same NUMA domain as the CPU core the MPI rank is running on.      |
+------------------------------------------------+--------------------------------------------------------------------------------------------------------------+
| ``--gpu-bind=map_gpu:<list>``                  | Bind tasks to specific GPUs by setting GPU masks on tasks (or ranks) as specified where                      |
|                                                | ``<list>`` is ``<gpu_id_for_task_0>,<gpu_id_for_task_1>,...``. If the number of tasks (or                    |
|                                                | ranks) exceeds the number of elements in this list, elements in the list will be reused as                   |
|                                                | needed starting from the beginning of the list. To simplify support for large task                           |
|                                                | counts, the lists may follow a map with an asterisk and repetition count. (For example                       |
|                                                | ``map_gpu:0*4,1*4``)                                                                                         |
+------------------------------------------------+--------------------------------------------------------------------------------------------------------------+
| ``--ntasks-per-gpu=<ntasks>``                  | Request that there are ntasks tasks invoked for every GPU.                                                   |
+------------------------------------------------+--------------------------------------------------------------------------------------------------------------+
| ``--distribution=<value>[:<value>][:<value>]`` | Specifies the distribution of MPI ranks across compute nodes, sockets (NUMA domains on Defiant), and cores,  |
|                                                | respectively. The default values are ``block:cyclic:cyclic``                                                 |
+------------------------------------------------+--------------------------------------------------------------------------------------------------------------+

.. note::
    In general, GPU mapping can be accomplished in different ways. For example, an
    application might map MPI ranks to GPUs programmatically within the code using, 
    say, ``hipSetDevice``. In this case, since all GPUs on a node are available to 
    all MPI ranks on that node by default, there might not be a need to map to GPUs 
    using Slurm (just do it in the code). However, in another application, there 
    might be a reason to make only a subset of GPUs available to the MPI ranks on a
    node. It is this latter case that the following examples refer to.

Mapping 1 task per GPU
""""""""""""""""""""""

In the following examples, each MPI rank (and its OpenMP threads) will be mapped
to a single GPU.

**Example 1: 4 MPI ranks - each with 2 OpenMP threads and 1 GPU (single-node)**

This example launches 4 MPI ranks (``-n4``), each with 2 physical CPU cores
(``-c2``) to launch 2 OpenMP threads (``OMP_NUM_THREADS=2``) on. In addition,
each MPI rank (and its 2 OpenMP threads) should have access to only 1 GPU. To 
accomplish the GPU mapping, two new ``srun`` options will be used:

* ``--gpus-per-task`` specifies the number of GPUs required for the job on each task
* ``--gpu-bind=closest`` binds each task to the GPU which is closest.

.. note::
    To further clarify, ``--gpus-per-task`` does not actually bind GPUs to MPI ranks.
    It allocates GPUs to the job step. The ``--gpu-bind=closest`` is what actually 
    maps a specific GPU to each rank; namely, the "closest" one, which is the GPU on 
    the same NUMA domain as the CPU core the MPI rank is running on 
    (see the :ref:`defiant-compute-nodes` section).

.. note::
    Without these additional flags, all MPI ranks would have access to all GPUs 
    (which is the default behavior).

.. code-block:: bash

    $ export OMP_NUM_THREADS=2
    $ srun -N1 -n4 -c2 --gpus-per-task=1 --gpu-bind=closest ./hello_jobstep | sort

    MPI 000 - OMP 000 - HWT 000 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 000 - OMP 001 - HWT 001 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 001 - OMP 000 - HWT 016 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 001 - OMP 001 - HWT 017 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 002 - OMP 000 - HWT 032 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID 48
    MPI 002 - OMP 001 - HWT 033 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID 48
    MPI 003 - OMP 000 - HWT 048 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID 09
    MPI 003 - OMP 001 - HWT 049 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID 09

The output contains different IDs associated with the GPUs so it is important to
first describe these IDs before moving on. ``GPU_ID`` is the node-level (or global)
GPU ID, which is labeled as one might expect from looking at a node diagram:
0, 1, 2, 3. ``RT_GPU_ID`` is the HIP runtime GPU ID, which can be thought of as
each MPI rank's local GPU ID numbering (with zero-based indexing). So in the output
above, each MPI rank has access to 1 unique GPU - where MPI 000 has access to GPU 0,
MPI 001 has access to GPU 1, etc., but all MPI ranks show a HIP runtime GPU ID of 0.
The reason is that each MPI rank only "sees" one GPU and so the HIP runtime labels
it as "0", even though it might be global GPU ID 0, 1, 2, or 3. The GPU's bus ID
is included to definitively show that different GPUs are being used. 

Here is a summary of the different GPU IDs reported by the example program:

* ``GPU_ID`` is the node-level (or global) GPU ID read from ``ROCR_VISIBLE_DEVICES``. If this environment variable is not set (either by the user or by Slurm), the value of ``GPU_ID`` will be set to ``N/A``.
* ``RT_GPU_ID`` is the HIP runtime GPU ID (as reported from, say ``hipGetDevice``).
* ``Bus_ID`` is the physical bus ID associated with the GPUs. Comparing the bus IDs is meant to definitively show that different GPUs are being used.

So the job step (i.e., ``srun`` command) used above gave the desired output. Each
MPI rank spawned 2 OpenMP threads and had access to a unique GPU. The 
``--gpus-per-task=1`` allocated 1 GPU for each MPI rank and the ``--gpu-bind=closest``
ensured that the closest GPU to each rank was the one used.

**Example 2: 8 MPI ranks - each with 2 OpenMP threads and 1 GPU (multi-node)**

This example will extend Example 1 to run on 2 nodes. As the output shows, it is a
very straightforward exercise of changing the number of nodes to 2 (``-N2``) and 
the number of MPI ranks to 8 (``-n8``).

.. code-block:: bash

    $ export OMP_NUM_THREADS=2
    $ srun -N2 -n8 -c2 --gpus-per-task=1 --gpu-bind=closest ./hello_jobstep | sort

    MPI 000 - OMP 000 - HWT 000 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 000 - OMP 001 - HWT 001 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 001 - OMP 000 - HWT 016 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 001 - OMP 001 - HWT 017 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 002 - OMP 000 - HWT 032 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID 48
    MPI 002 - OMP 001 - HWT 033 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID 48
    MPI 003 - OMP 000 - HWT 048 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID 09
    MPI 003 - OMP 001 - HWT 049 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID 09
    MPI 004 - OMP 000 - HWT 000 - Node defiant14 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 004 - OMP 001 - HWT 001 - Node defiant14 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 005 - OMP 000 - HWT 016 - Node defiant14 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 005 - OMP 001 - HWT 017 - Node defiant14 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 006 - OMP 000 - HWT 032 - Node defiant14 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID 48
    MPI 006 - OMP 001 - HWT 033 - Node defiant14 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID 48
    MPI 007 - OMP 000 - HWT 048 - Node defiant14 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID 09
    MPI 007 - OMP 001 - HWT 049 - Node defiant14 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID 09

**Example 3: 4 MPI ranks - each with 2 OpenMP threads and 1 *specific* GPU (single-node)**

This example will be very similar to Example 1, but instead of using
``--gpu-bind=closest`` to map each MPI rank to the closest GPU, ``--gpu-bind=map_gpu``
will be used to map each MPI rank to a *specific* GPU. The ``map_gpu`` option takes a
comma-separated list of GPU IDs to specify how the MPI ranks are mapped to GPUs, where
the form of the comma-separated list is ``<gpu_id_for_task_0>, <gpu_id_for_task_1>,...``.

.. code:: bash

    $ export OMP_NUM_THREADS=2
    $ srun -N1 -n4 -c2 --gpus-per-task=1 --gpu-bind=map_gpu:0,1,2,3 ./hello_jobstep | sort

    MPI 000 - OMP 000 - HWT 000 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 000 - OMP 001 - HWT 001 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 001 - OMP 000 - HWT 016 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 001 - OMP 001 - HWT 017 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 002 - OMP 000 - HWT 032 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID 48
    MPI 002 - OMP 001 - HWT 033 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID 48
    MPI 003 - OMP 000 - HWT 048 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID 09
    MPI 003 - OMP 001 - HWT 049 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID 09


Here, the output is the same as the results from Example 1. This is because the 4 GPU
IDs in the comma-separated list happen to specify the GPUs within the same NUMA domains
that the MPI ranks are in. So MPI 000 is mapped to GPU 0, MPI 001 is mapped to GPU 1,
etc.

While this level of control over mapping MPI ranks to GPUs might be useful for some
applications, it is always important to consider the implication of the mapping. For
example, if the order of the GPU IDs in the ``map_gpu`` option is reversed, the MPI
ranks and the GPUs they are mapped to would be in different NUMA domains, which
could potentially lead to poorer performance.

.. code:: bash

    $ export OMP_NUM_THREADS=2
    $ srun -N1 -n4 -c2 --gpus-per-task=1 --gpu-bind=map_gpu:3,2,1,0 ./hello_jobstep | sort

    MPI 000 - OMP 000 - HWT 000 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID 09
    MPI 000 - OMP 001 - HWT 001 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID 09
    MPI 001 - OMP 000 - HWT 016 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID 48
    MPI 001 - OMP 001 - HWT 017 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID 48
    MPI 002 - OMP 000 - HWT 032 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 002 - OMP 001 - HWT 033 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 003 - OMP 000 - HWT 048 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 003 - OMP 001 - HWT 049 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9

Here, notice that MPI 000 now maps to GPU 3, MPI 001 maps to GPU 2, etc., so the MPI
ranks are not in the same NUMA domains as the GPUs they are mapped to.

.. note::
    Again, this particular example would NOT be a very good mapping of GPUs to MPI ranks though. E.g., notice that MPI rank 000 is running on NUMA node 0, whereas GPU 3 is on NUMA node 3. Again, see the :ref:`defiant-compute-nodes` section for NUMA descriptions.

**Example 4: 8 MPI ranks - each with 2 OpenMP threads and 1 *specific* GPU (multi-node)**

Extending Examples 2 and 3 to run on 2 nodes is also a straightforward exercise by
changing the number of nodes to 2 (``-N2``) and the number of MPI ranks to 8 (``-n8``).

.. code:: bash

    $ export OMP_NUM_THREADS=2
    $ srun -N2 -n8 -c2 --gpus-per-task=1 --gpu-bind=map_gpu:0,1,2,3 ./hello_jobstep | sort

    MPI 000 - OMP 000 - HWT 000 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 000 - OMP 001 - HWT 001 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 001 - OMP 000 - HWT 016 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 001 - OMP 001 - HWT 017 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 002 - OMP 000 - HWT 032 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID 48
    MPI 002 - OMP 001 - HWT 033 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID 48
    MPI 003 - OMP 000 - HWT 048 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID 09
    MPI 003 - OMP 001 - HWT 049 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID 09
    MPI 004 - OMP 000 - HWT 000 - Node defiant14 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 004 - OMP 001 - HWT 001 - Node defiant14 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 005 - OMP 000 - HWT 016 - Node defiant14 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 005 - OMP 001 - HWT 017 - Node defiant14 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 006 - OMP 000 - HWT 032 - Node defiant14 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID 48
    MPI 006 - OMP 001 - HWT 033 - Node defiant14 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID 48
    MPI 007 - OMP 000 - HWT 048 - Node defiant14 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID 09
    MPI 007 - OMP 001 - HWT 049 - Node defiant14 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID 09

Mapping multiple MPI ranks to a single GPU
""""""""""""""""""""""""""""""""""""""""""

In the following examples, 2 MPI ranks will be mapped to 1 GPU. For the sake of brevity,
``OMP_NUM_THREADS`` will be set to ``1``, so ``-c1`` will be used unless otherwise specified.

.. note::

    On AMD's MI100 GPUs, multi-process service (MPS) is not needed since multiple MPI ranks per GPU is supported natively.

**Example 5: 8 MPI ranks - where 2 ranks share a GPU (round-robin, single-node)**

This example launches 8 MPI ranks (``-n8``), each with 1 physical CPU core (``-c1``)
to launch 1 OpenMP thread (``OMP_NUM_THREADS=1``) on. The MPI ranks will be assigned
to GPUs in a round-robin fashion so that each of the 4 GPUs on the node are shared
by 2 MPI ranks. To accomplish this GPU mapping, a new ``srun`` option will be used:

* ``--ntasks-per-gpu`` specifies the number of MPI ranks that will share access to a GPU.

.. code:: bash

    $ export OMP_NUM_THREADS=1
    $ srun -N1 -n8 -c1 --ntasks-per-gpu=2 --gpu-bind=closest ./hello_jobstep | sort

    MPI 000 - OMP 000 - HWT 000 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 001 - OMP 000 - HWT 016 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 002 - OMP 000 - HWT 032 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID 48
    MPI 003 - OMP 000 - HWT 048 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID 09
    MPI 004 - OMP 000 - HWT 001 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 005 - OMP 000 - HWT 017 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 006 - OMP 000 - HWT 033 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID 48
    MPI 007 - OMP 000 - HWT 049 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID 09

The output shows the round-robin (``cyclic``) distribution of MPI ranks to GPUs.
In fact, it is a round-robin distribution of MPI ranks *to NUMA domains* 
(the default distribution). The GPU mapping is a consequence of where the MPI ranks
are distributed; ``--gpu-bind=closest`` simply maps the GPU in a NUMA domain to the 
MPI ranks in the same NUMA domain.

**Example 6: 16 MPI ranks - where 2 ranks share a GPU (round-robin, multi-node)**

This example is an extension of Example 5 to run on 2 nodes.

.. warning::

    This example requires a workaround to run as expected. ``--ntasks-per-gpu=2`` does not force MPI ranks 008-015 to run on the second node, so the number of physical CPU cores per MPI rank is increased to 8 (``-c8``) to force the desired behavior due to the constraint of the number of physical CPU cores (64) on a node.

.. code:: bash

    $ export OMP_NUM_THREADS=1
    $ srun -N2 -n16 -c8 --ntasks-per-gpu=2 --gpu-bind=closest ./hello_jobstep | sort

    MPI 000 - OMP 000 - HWT 005 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 001 - OMP 000 - HWT 018 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 002 - OMP 000 - HWT 032 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID 48
    MPI 003 - OMP 000 - HWT 050 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID 09
    MPI 004 - OMP 000 - HWT 010 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 005 - OMP 000 - HWT 026 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 006 - OMP 000 - HWT 040 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID 48
    MPI 007 - OMP 000 - HWT 059 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID 09
    MPI 008 - OMP 000 - HWT 003 - Node defiant14 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 009 - OMP 000 - HWT 016 - Node defiant14 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 010 - OMP 000 - HWT 032 - Node defiant14 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID 48
    MPI 011 - OMP 000 - HWT 048 - Node defiant14 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID 09
    MPI 012 - OMP 000 - HWT 008 - Node defiant14 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 013 - OMP 000 - HWT 024 - Node defiant14 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 014 - OMP 000 - HWT 042 - Node defiant14 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID 48
    MPI 015 - OMP 000 - HWT 056 - Node defiant14 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID 09

**Example 7: 8 MPI ranks - where 2 ranks share a GPU (packed, single-node)**

This example launches 8 MPI ranks (``-n8``), each with 8 physical CPU cores (``-c8``)
to launch 1 OpenMP thread (``OMP_NUM_THREADS=1``) on. The MPI ranks will be assigned
to GPUs in a packed fashion so that each of the 4 GPUs on the node are shared by 2 
MPI ranks. Similar to Example 5, ``-ntasks-per-gpu=2`` will be used, but a new ``srun``
flag will be used to change the default round-robin (``cyclic``) distribution of MPI 
ranks across NUMA domains:

* ``--distribution=<value>:[<value>]:[<value>]`` specifies the distribution of MPI ranks across compute nodes, sockets (NUMA domains on Defiant), and cores, respectively. The default values are ``block:cyclic:cyclic``, which is where the ``cyclic`` assignment comes from in the previous examples.

.. note::

    In the job step for this example, ``--distribution=*:block`` is used, where ``*`` represents the default value of ``block`` for the distribution of MPI ranks across compute nodes and the distribution of MPI ranks across NUMA domains has been changed to ``block`` from its default value of ``cyclic``.

.. note:: 

    Because the distribution across NUMA domains has been changed to a "packed" (``block``) configuration, caution must be taken to ensure MPI ranks end up in the NUMA domains where the GPUs they intend to be mapped to are located. To accomplish this, the number of physical CPU cores assigned to an MPI rank was increased - in this case to 8. Doing so ensures that only 2 MPI ranks can fit into a single NUMA domain. If the value of ``-c`` was left at ``1``, all 8 MPI ranks would be "packed" into the first NUMA domain, where the "closest" GPU would be GPU 0 - the only GPU in that NUMA domain. 

    Notice that this is not a workaround like in Example 6, but a requirement due to the ``block`` distribution of MPI ranks across NUMA domains.

.. code:: bash

    $ export OMP_NUM_THREADS=1
    $ srun -N1 -n8 -c8 --ntasks-per-gpu=2 --gpu-bind=closest --distribution=*:block ./hello_jobstep | sort

    MPI 000 - OMP 000 - HWT 001 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 001 - OMP 000 - HWT 008 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 002 - OMP 000 - HWT 016 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 003 - OMP 000 - HWT 024 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 004 - OMP 000 - HWT 035 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID 48
    MPI 005 - OMP 000 - HWT 043 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID 48
    MPI 006 - OMP 000 - HWT 049 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID 09
    MPI 007 - OMP 000 - HWT 057 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID 09

The overall effect of using ``--distribution=*:block`` and increasing the number of 
physical CPU cores available to each MPI rank is to place the first two MPI ranks in 
NUMA 0 with GPU 0, the next two MPI ranks in NUMA 1 with GPU 1, and so on.

**Example 8: 16 MPI ranks - where 2 ranks share a GPU (packed, multi-node)**

This example is an extension of Example 7 to use 2 compute nodes. With the appropriate 
changes put in place in Example 7, it is a straightforward exercise to change to using
2 nodes (``-N2``) and 16 MPI ranks (``-n16``).

.. code:: bash

    $ export OMP_NUM_THREADS=1
    $ srun -N2 -n16 -c8 --ntasks-per-gpu=2 --gpu-bind=closest --distribution=*:block ./hello_jobstep | sort

    MPI 000 - OMP 000 - HWT 005 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 001 - OMP 000 - HWT 008 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 002 - OMP 000 - HWT 017 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 003 - OMP 000 - HWT 026 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 004 - OMP 000 - HWT 033 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID 48
    MPI 005 - OMP 000 - HWT 041 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID 48
    MPI 006 - OMP 000 - HWT 048 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID 09
    MPI 007 - OMP 000 - HWT 057 - Node defiant13 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID 09
    MPI 008 - OMP 000 - HWT 002 - Node defiant14 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 009 - OMP 000 - HWT 011 - Node defiant14 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9
    MPI 010 - OMP 000 - HWT 016 - Node defiant14 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 011 - OMP 000 - HWT 026 - Node defiant14 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
    MPI 012 - OMP 000 - HWT 033 - Node defiant14 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID 48
    MPI 013 - OMP 000 - HWT 041 - Node defiant14 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID 48
    MPI 014 - OMP 000 - HWT 054 - Node defiant14 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID 09
    MPI 015 - OMP 000 - HWT 063 - Node defiant14 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID 09

Multiple GPUs per MPI rank
""""""""""""""""""""""""""

As mentioned previously, all GPUs are accessible by all MPI ranks by default, so it 
is possible to *programatically* map any combination of MPI ranks to GPUs. However,
there is currently no way to use Slurm to map multiple GPUs to a single MPI rank. If 
this functionality is needed for an application, please submit a ticket by 
emailing help@olcf.ornl.gov.


.. note::

    There are many different ways users might choose to perform these mappings, so users are encouraged to clone the ``hello_jobstep`` program and test whether or not processes and threads are running where intended.

NVMe Usage
----------

Each Defiant compute node has [2x] 3.2 TB NVMe devices (SSDs) with a peak sequential 
performance of 6900 MB/s (read) and 4200 MB/s (write). To use the NVMe, users must 
request access during job allocation using the ``-C nvme`` option to 
``sbatch``, ``salloc``, or ``srun``. Once the devices have been granted to a job, 
users can access them at ``/mnt/bb/<userid>``. Users are responsible for moving data 
to/from the NVMe before/after their jobs. Here is a simple example script:

.. code:: bash

    #!/bin/bash
    #SBATCH -A <projid>
    #SBATCH -J nvme_test
    #SBATCH -o %x-%j.out
    #SBATCH -t 00:05:00
    #SBATCH -p batch
    #SBATCH -N 1
    #SBATCH -C nvme
    
    date
    
    # Change directory to user scratch space (GPFS)
    cd /gpfs/alpine/<projid>/scratch/<userid>
    
    echo " "
    echo "*****ORIGINAL FILE*****"
    cat test.txt
    echo "***********************"
    
    # Move file from GPFS to SSD
    mv test.txt /mnt/bb/<userid>
    
    # Edit file from compute node
    srun -n1 hostname >> /mnt/bb/<userid>/test.txt
    
    # Move file from SSD back to GPFS
    mv /mnt/bb/<userid>/test.txt .
    
    echo " "
    echo "*****UPDATED FILE******"
    cat test.txt
    echo "***********************"

And here is the output from the script:

.. code:: bash

    $ cat nvme_test-<jobid>.out
    Mon May 17 12:28:18 EDT 2021
    
    *****ORIGINAL FILE*****
    This is my file. There are many like it but this one is mine.
    ***********************
    
    *****UPDATED FILE******
    This is my file. There are many like it but this one is mine.
    defiant25
    ***********************

----


Container Usage
===============


Defiant provides Apptainer v1.2.5 installed for building and running containers. Defiant
also provides Podman to build container images if you only have the Dockerfile formats and can't convert
to the Apptainer format. Currently the containers that can be built with Podman is very limited, so it is
recommended that you convert your Dockerfiles to the Apptainer Definition format. See documentation for that
`here <https://apptainer.org/docs/user/main/definition_files.html>`_ . 

.. note::
   The container docs will continue to evolve and change as we identify better practices and more user friendly
   methods for using containers on Defiant to best suit the needs of the users.
   If something you're trying no longer works, be sure to come back and check
   the docs to see if anything has changed.

..
   Notes on things to do
   - building with Podman and running with Apptainer
   - building and running MPI program
   - building and running MPI with GPU program
   - building and running gpu aware mpi program
   - Best practices for building a container with apptainer and building with Podman
   - multi stage builds
   - other best practices

Setup before Building
---------------------

Users will need to set up a file in their home directory
``/ccsopen/home/<username>/.config/containers/storage.conf`` with the following content:
::

   [storage]
   driver = "overlay"
   graphroot = "/tmp/containers/<user>"
   
   [storage.options]
   additionalimagestores = [
   ]
   
   [storage.options.overlay]
   ignore_chown_errors = "true"
   mount_program = "/usr/bin/fuse-overlayfs"
   mountopt = "nodev,metacopy=on"
   
   [storage.options.thinpool]

``<user>`` in the ``graphroot = "/tmp/containers/<user>"`` in the above file should be
replaced with your username. This will ensure that Podman will use the NVMe mounted in ``/tmp/containers`` for storage during container image builds.


Build and Run Workflow
-----------------------

As an example, let's build and run a very simple container image to demonstrate the workflow.

Building a Simple Image
^^^^^^^^^^^^^^^^^^^^^^^

- Create a directory called ``simplecontainer`` on home or GPFS and ``cd`` into it.
- Create a file named ``simple.def`` with the following contents.
  ::

     Bootstrap: docker
     From: opensuse/leap:15.4

     %post
     zypper install -y wget sudo git gzip gcc-c++ openssh hostname



- Build the container image with ``apptainer build simple.sif simple.def``.

  * Apptainer builds the container image in the SIF file format. Unlike Podman, Apptainer gives you a single file for your image that you can later run as your container.

.. note::
   Using opensuse as your ``From`` image is preferred as it does not run into issues when installing packages with the ``zypper`` (until we get to a point where all users have mappings in the ``/etc/subuid`` files which is currently a work in progress).


Running a Simple Container in a Batch Job
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As a simple example, we will run ``hostname`` with the Apptainer container.

- Create a file submit.sl with the contents below.
  ::

     #!/bin/bash
     #SBATCH -t00:10:00
     #SBATCH -A csc266
     #SBATCH -N2
     #BATCH -P batch
     #SBATCH -J simple_container_job
     #SBATCH -o %x_%j.out
     #SBATCH -e %x_%j.out
     
     
     srun  -N2 --tasks-per-node=1 apptainer exec  simple.sif hostname

- Submit the job with ``sbatch submit.sl``. This should produce an output that looks like:
  ::

     defiant14
     defiant12


Note that if you are running multiple tasks per node, for example with
``srun -N1 --tasks-per-node=2 apptainer exec simple.sif hostname``, Apptainer is running
an instance of the runtime for each task i.e. the same running container is NOT shared
between multiple tasks running on the same node.


Running an MPI program with an MPI image
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For running a program that uses MPI, you will need to build your container image
with MPICH 3.4.2 installed (and also install ROCm if you need GPU
functionality). We have a prebuilt image with with MPICH 3.4.2 and ROCm 5.3.3 in /lustre/polis/stf007/world-shared/containers/opensusempich342rocm533.sif.
The definition files that are used to build this image can be found on `this code.ornl.gov repo <https://code.ornl.gov/olcfcontainers/olcfbaseimages/-/tree/master/defiant>`_ .
Let's look at an example where we build a container that runs an MPI example
based on this image.

- Create a new directory ``mpiexample``.
- Create a file ``mpiexample.c`` with the following contents.
  ::

     #include <stdio.h>
     #include <mpi.h>

     int main (int argc, char *argv[])
     {
     int rank, size;
     MPI_Comm comm;

     comm = MPI_COMM_WORLD;
     MPI_Init (&argc, &argv);
     MPI_Comm_rank (comm, &rank);
     MPI_Comm_size (comm, &size);

     printf("Hello from rank %d\n", rank);

     MPI_Barrier(comm);
     MPI_Finalize();
     }

 - Create a file named ``mpiexample.def`` with the following contents
   ::

      Bootstrap: localimage
      From: /lustre/polis/stf007/world-shared/containers/opensusempich342rocm533.sif

      %files
      mpiexample.c /app/mpiexample.c


      %post
      cd /app && mpicc -o mpiexample mpiexample.c

- Build the container image with ``apptainer build mpiexample.sif mpiexample.def``.
- Create a submit script ``submit.sl`` with the following contents. The submit script will launch four apptainer tasks across two nodes with MPI running, and prints their rank id the same as if the program was running on bare metal.
  ::

     #!/bin/bash
     #SBATCH -t00:10:00
     #SBATCH -A csc266
     #SBATCH -N2
     #SBATCH -J mpiexample
     #SBATCH -o %x_%j.out
     #SBATCH -e %x_%j.out

     module  load amd-mixed
     module load craype-accel-amd-gfx908
     module load cray-mpich-abi
     
     export MPICH_SMP_SINGLE_COPY_MODE=NONE
     
     export APPTAINERENV_LD_LIBRARY_PATH="$CRAY_MPICH_DIR/lib-abi-mpich:$CRAY_MPICH_ROOTDIR/gtl/lib:/opt/rocm/lib:/opt/rocm/lib64:$CRAY_LD_LIBRARY_PATH:$LD_LIBRARY_PATH:/opt/cray/pe/lib64:/usr/lib64/libibverbs"
     export APPTAINER_CONTAINLIBS="/usr/lib64/libjansson.so.4,/usr/lib64/libcxi.so.1,/usr/lib64/libjson-c.so.3,/usr/lib64/libdrm_amdgpu.so.1,/usr/lib64/libdrm.so.2,/lib64/libtinfo.so.6,/usr/lib64/libnl-3.so.200,/usr/lib64/librdmacm.so.1,/usr/lib64/libibverbs.so.1,/usr/lib64/libibverbs/libmlx5-rdmav34.so,/usr/lib64/libnl-route-3.so.200"
     export APPTAINERENV_LD_PRELOAD=$CRAY_MPICH_ROOTDIR/gtl/lib/libmpi_gtl_hsa.so.0:
     export APPTAINER_BIND=/usr/share/libdrm,/var/spool/slurm,/opt/cray,${PWD},/etc/libibverbs.d,/usr/lib64/libibverbs/



     srun  -N2 -n4 --tasks-per-node 2 apptainer exec  --workdir `pwd` mpiexample.sif /app/mpiexample

- You should get output that looks like
  ::

     <several INFO messages. Can be ignored>
     ...
     Hello from rank 1
     Hello from rank 0
     Hello from rank 2
     Hello from rank 3


You can view the definition files used to build the base image at the `code.ornl.gov
repository <https://code.ornl.gov/olcfcontainers/olcfbaseimages>`_ in the
``defiant`` directory. You can build these yourself (if you want slightly modify
it) by cloning the repository and running ``./build`` in the individual
directories in the repository.


.. note::

   GPU aware MPI is currently buggy on Defiant due to issues with the MI210 with the Slingshot-10 network.
   We have a ticket open with HPE to address the issue. This will affect GPU aware MPI in the containers as well.
   Once that is fixed, we will add documentation on how to use GPU aware MPI with containers on Defiant.



..
  tabling gpu aware MPI till after we get it working on defiant
  Running a GPU aware MPI program with OLCF MPI base image
  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

----------

Getting Help
============

If you have problems or need helping running on Defiant, please submit a ticket
by emailing help@olcf.ornl.gov.

----


Known Issues
============

- GPU aware MPI is currently not working on MPI. Your code should stage GPU data through main memory for MPI operations.

.. JIRA_CONTENT_HERE
