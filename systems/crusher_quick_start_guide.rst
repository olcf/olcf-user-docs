.. _crusher-quick-start-guide:

*************************
Crusher Quick-Start Guide
*************************

.. _crusher-system-overview:

System Overview
===============

Crusher is an National Center for Computational Sciences (NCCS) moderate-security system that contains identical hardware and similar software as the upcoming Frontier system. It is used as an early-access testbed for Center for Accelerated Application Readiness (CAAR) and Exascale Computing Project (ECP) teams as well as NCCS staff and our vendor partners. The system has 2 cabinets, the first with 128 compute nodes and the second with 64 compute nodes, for a total of 192 compute nodes.

.. _crusher-compute-nodes:

Crusher Compute Nodes
---------------------

Each Crusher compute node consists of [1x] 64-core AMD EPYC 7A53 "Optimized 3rd Gen EPYC" CPU (with 2 hardware threads per physical core) with access to 512 GB of DDR4 memory. Each node also contains [4x] AMD MI250X, each with 2 Graphics Compute Dies (GCDs) for a total of 8 GCDs per node. The programmer can think of the 8 GCDs as 8 separate GPUs, each having 64 GB of high-bandwidth memory (HBM2E). The CPU is connected to each GCD via Infinity Fabric CPU-GPU, allowing a peak host-to-device (H2D) and device-to-host (D2H) bandwidth of 36+36 GB/s. The 2 GCDs on the same MI250X are connected with Infinity Fabric GPU-GPU with a peak bandwidth of 200 GB/s. The GCDs on different MI250X are connected with Infinity Fabric GPU-GPU in the arrangement shown in the Crusher Node Diagram below, where the peak bandwidth ranges from 50-100 GB/s based on the number of Infinity Fabric connections between individual GCDs.

.. note::

    **TERMINOLOGY:**

    The 8 GCDs contained in the 4 MI250X will show as 8 separate GPUs according to Slurm, ``ROCR_VISIBLE_DEVICES``, and the ROCr runtime, so from this point forward in the quick-start guide, we will simply refer to the GCDs as GPUs.

.. image:: /images/Crusher_Node_Diagram.jpg
   :align: center
   :width: 100%
   :alt: Crusher node architecture diagram

.. note::
    There are [4x] NUMA domains per node and [2x] L3 cache regions per NUMA for a total of [8x] L3 cache regions. The 8 GPUs are each associated with one of the L3 regions as follows:

    NUMA 0:

    * hardware threads 000-007, 064-071 | GPU 4
    * hardware threads 008-015, 072-079 | GPU 5
    
    NUMA 1:

    * hardware threads 016-023, 080-087 | GPU 2
    * hardware threads 024-031, 088-095 | GPU 3

    NUMA 2:

    * hardware threads 032-039, 096-103 | GPU 6
    * hardware threads 040-047, 104-111 | GPU 7

    NUMA 3:

    * hardware threads 048-055, 112-119 | GPU 0
    * hardware threads 056-063, 120-127 | GPU 1


System Interconnect
-------------------

The Crusher nodes are connected with [4x] HPE Slingshot 200 Gbps (25 GB/s) NICs providing a node-injection bandwidth of 800 Gbps (100 GB/s).

File Systems
------------

Crusher is connected to the center-wide IBM Spectrum Scale™ filesystem providing 250 PB of storage capacity with a peak write speed of 2.5 TB/s. Crusher also has access to the center-wide NFS-based filesystem (which provides user and project home areas). While Crusher does not have *direct* access to the center’s High Performance Storage System (HPSS) - for user and project archival storage - users can log in to the :ref:`dtn-user-guide` to move data to/from HPSS. 

GPUs
----

Crusher contains a total of 1536 AMD MI250X. The AMD MI250X has a peak performance of 52 TFLOPS in double-precision for modeling and simulation. Each MI250X contains 2 GPUs, where each GPU has a peak performance of 26 TFLOPS (double-precision), 110 compute units, and 64 GB of high-bandwidth memory (HBM2) which can be accessed at a peak of 1.6 TB/s. The 2 GPUs on an MI250X are connected with Infinity Fabric with a bandwidth of 200 GB/s (in both directions simultaneously).

----

Connecting
==========

To connect to Crusher, ``ssh`` to ``crusher.olcf.ornl.gov``. For example:

.. code-block:: bash

    $ ssh <username>@crusher.olcf.ornl.gov

For more information on connecting to OLCF resources, see :ref:`connecting-to-olcf`.

----

Data and Storage
================

For more detailed information about center-wide file systems and data archiving available on Crusher, please refer to the pages on :ref:`data-storage-and-transfers`, but the two subsections below give a quick overview of NFS and GPFS storage spaces.

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

Crusher users are provided with many pre-installed software packages and scientific libraries. To facilitate this, environment management tools are used to handle necessary changes to the shell.

Environment Modules (Lmod)
--------------------------

Environment modules are provided through `Lmod <https://lmod.readthedocs.io/en/latest/>`__, a Lua-based module system for dynamically altering shell environments. By managing changes to the shell’s environment variables (such as ``PATH``, ``LD_LIBRARY_PATH``, and ``PKG_CONFIG_PATH``), Lmod allows you to alter the software available in your shell environment without the risk of creating package and version combinations that cannot coexist in a single environment.

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

Modules with dependencies are only available when the underlying dependencies, such as compiler families, are loaded. Thus, module avail will only display modules that are compatible with the current state of the environment. To search the entire hierarchy across all possible dependencies, the ``spider`` sub-command can be used as summarized in the following table.

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

Cray, AMD, and GCC compilers are provided through modules on Crusher. The Cray and AMD compilers are both based on LLVM/Clang. There is also a system/OS versions of GCC available in ``/usr/bin``. The table below lists details about each of the module-provided compilers.

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
| AMD    | ``PrgEnv-amd``          | ``rocm``        | C        | ``cc``            | ``amdclang``                    |
|        |                         |                 +----------+-------------------+---------------------------------+
|        |                         |                 | C++      | ``CC``            | ``amdclang++``                  |
|        |                         |                 +----------+-------------------+---------------------------------+
|        |                         |                 | Fortran  | ``ftn``           | ``amdflang``                    |
+--------+-------------------------+-----------------+----------+-------------------+---------------------------------+
| GCC    | ``PrgEnv-gnu``          | ``gcc``         | C        | ``cc``            | ``${GCC_PATH}/bin/gcc``         |
|        |                         |                 +----------+-------------------+---------------------------------+
|        |                         |                 | C++      | ``CC``            | ``${GCC_PATH}/bin/g++``         |
|        |                         |                 +----------+-------------------+---------------------------------+
|        |                         |                 | Fortran  | ``ftn``           | ``${GCC_PATH}/bin/gfortran``    |
+--------+-------------------------+-----------------+----------+-------------------+---------------------------------+


Cray Programming Environment and Compiler Wrappers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Cray provides ``PrgEnv-<compiler>`` modules (e.g., ``PrgEnv-cray``) that load compatible components of a specific compiler toolchain. The components include the specified compiler as well as MPI, LibSci, and other libraries. Loading the ``PrgEnv-<compiler>`` modules also defines a set of compiler wrappers for that compiler toolchain that automatically add include paths and link in libraries for Cray software. Compiler wrappers are provided for C (``cc``), C++ (``CC``), and Fortran (``ftn``).

.. note::
   Use the ``-craype-verbose`` flag to display the full include and link information used by the Cray compiler wrappers. This must be called on a file to see the full output (e.g., ``CC -craype-verbose test.cpp``).

MPI
---

The MPI implementation available on Crusher is Cray's MPICH, which is "GPU-aware" so GPU buffers can be passed directly to MPI calls.

----

Compiling
=========

This section covers how to compile for different programming models using the different compilers covered in the previous section.

MPI
---

+----------------+----------------+-----------------------------------------------------+-------------------------------------------------------------------------------+
| Implementation | Module         | Compiler                                            | Header Files & Linking                                                        |
+================+================+=====================================================+===============================================================================+
| Cray MPICH     | ``cray-mpich`` | ``cc``, ``CC``, ``ftn`` (Cray compiler wrappers)    | MPI header files and linking is built into the Cray compiler wrappers         |
|                |                +-----------------------------------------------------+-------------------------------------------------------------------------------+
|                |                | ``hipcc``                                           | | ``-L${MPICH_DIR}/lib -lmpi``                                                |
|                |                |                                                     | | ``-I${MPICH_DIR}/include``                                                  |
+----------------+----------------+-----------------------------------------------------+-------------------------------------------------------------------------------+

GPU-Aware MPI
^^^^^^^^^^^^^

To use GPU-aware Cray MPICH, users must set the following modules and environment variables:

.. code:: bash
    
    module load craype-accel-amd-gfx90a
    module load rocm

    export MPICH_GPU_SUPPORT_ENABLED=1

.. note::

    There are extra steps needed to enable GPU-aware MPI on Crusher, which depend on the compiler that is used (see 1. and 2. below).
    

1. Compiling with the Cray compiler wrappers, ``cc`` or ``CC``
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

To use GPU-aware Cray MPICH with the Cray compiler wrappers, the following environment variables must be set before compiling. These variables are automatically set by the ``cray-mpich`` modulefile:

.. code:: bash

    ## These must be set before compiling so the executable picks up GTL
    PE_MPICH_GTL_DIR_amd_gfx90a="-L${CRAY_MPICH_ROOTDIR}/gtl/lib"
    PE_MPICH_GTL_LIBS_amd_gfx90a="-lmpi_gtl_hsa"

In addition, the following header files and libraries must be included:

.. code:: bash

    -I${ROCM_PATH}/include
    -L${ROCM_PATH}/lib -lamdhip64

where the include path implies that ``#include <hip/hip_runtime.h>`` is included in the source file.

2. Compiling with ``hipcc``
"""""""""""""""""""""""""""

To use GPU-aware Cray MPICH with ``hipcc``, users must include appropriate headers, libraries, and flags:

.. code:: bash

    -I${MPICH_DIR}/include
    -L${MPICH_DIR}/lib -lmpi -L${CRAY_MPICH_ROOTDIR}/gtl/lib -lmpi_gtl_hsa

    HIPFLAGS = --amdgpu-target=gfx90a

OpenMP
------

This section shows how to compile with OpenMP using the different compilers covered above.

+--------+----------+-----------+----------------------------------------------+-------------------------------------+
| Vendor | Module   | Language  | Compiler                                     | OpenMP flag (CPU thread)            |
+========+==========+===========+==============================================+=====================================+
| Cray   | ``cce``  | C, C\+\+  | | ``cc`` (wraps ``craycc``)                  | ``-fopenmp``                        |
|        |          |           | | ``CC`` (wraps ``crayCC``)                  |                                     |
|        |          +-----------+----------------------------------------------+-------------------------------------+
|        |          | Fortran   | ``ftn`` (wraps ``crayftn``)                  | | ``-homp``                         |
|        |          |           |                                              | | ``-fopenmp`` (alias)              |
+--------+----------+-----------+----------------------------------------------+-------------------------------------+
| AMD    | ``rocm`` | | C       | | ``cc`` (wraps ``amdclang``)                | ``-fopenmp``                        |
|        |          | | C++     | | ``CC`` (wraps ``amdclang++``)              |                                     |
|        |          | | Fortran | | ``ftn`` (wraps ``amdflang``)               |                                     |
+--------+----------+-----------+----------------------------------------------+-------------------------------------+
| GCC    | ``gcc``  | | C       | | ``cc`` (wraps ``$GCC_PATH/bin/gcc``)       | ``-fopenmp``                        |
|        |          | | C++     | | ``CC`` (wraps ``$GCC_PATH/bin/g++``)       |                                     |
|        |          | | Fortran | | ``ftn`` (wraps ``$GCC_PATH/bin/gfortran``) |                                     |
+--------+----------+-----------+----------------------------------------------+-------------------------------------+

OpenMP GPU Offload
------------------

This section shows how to compile with OpenMP Offload using the different compilers covered above.

.. note::

    Make sure the ``craype-accel-amd-gfx90a`` module is loaded when using OpenMP offload.

+--------+----------+-----------+----------------------------------------------+----------------------------------------------+
| Vendor | Module   | Language  | Compiler                                     | OpenMP flag (GPU)                            |
+========+==========+===========+==============================================+==============================================+
| Cray   | ``cce``  | C         | | ``cc`` (wraps ``craycc``)                  | ``-fopenmp``                                 |
|        |          | C\+\+     | | ``CC`` (wraps ``crayCC``)                  |                                              |
|        |          +-----------+----------------------------------------------+----------------------------------------------+
|        |          | Fortran   | ``ftn`` (wraps ``crayftn``)                  | | ``-homp``                                  |
|        |          |           |                                              | | ``-fopenmp`` (alias)                       |
+--------+----------+-----------+----------------------------------------------+----------------------------------------------+
| AMD    | ``rocm`` | | C       | | ``cc`` (wraps ``amdclang``)                | ``-fopenmp``                                 |
|        |          | | C\+\+   | | ``CC`` (wraps ``amdclang++``)              |                                              |
|        |          | | Fortran | | ``ftn`` (wraps ``amdflang``)               |                                              |
|        |          |           | | ``hipcc`` (requires flags below)           |                                              |
+--------+----------+-----------+----------------------------------------------+----------------------------------------------+

.. note::

    If invoking ``amdclang``, ``amdclang++``, or ``amdflang`` directly, or using ``hipcc`` you will need to add:
    ``-fopenmp -target x86_64-pc-linux-gnu -fopenmp-targets=amdgcn-amd-amdhsa -Xopenmp-target=amdgcn-amd-amdhsa -march=gfx90a``.

HIP
---

This section shows how to compile HIP codes using the Cray compiler wrappers and ``hipcc`` compiler driver.

.. note::

    Make sure the ``craype-accel-amd-gfx90a`` module is loaded when using HIP.

+-----------+--------------------------------------------------------------------------------------------------------------------------+
| Compiler  | Compile/Link Flags, Header Files, and Libraries                                                                          |
+===========+==========================================================================================================================+
| ``CC``    | | ``CFLAGS = -std=c++11 -D__HIP_ROCclr__ -D__HIP_ARCH_GFX90A__=1 --rocm-path=${ROCM_PATH} --offload-arch=gfx90a -x hip`` |
|           | | ``LFLAGS = --rocm-path=${ROCM_PATH}``                                                                                  |
|           | | ``-L${ROCM_PATH}/lib -lamdhip64``                                                                                      |
+-----------+--------------------------------------------------------------------------------------------------------------------------+
| ``hipcc`` | | Can be used directly to compile HIP source files.                                                                      |
|           | | To see what is being invoked within this compiler driver, issue the command, ``hipcc --verbose``                       |
+-----------+--------------------------------------------------------------------------------------------------------------------------+

----

Running Jobs
============

This section describes how to run programs on the Crusher compute nodes, including a brief overview of Slurm and also how to map processes and threads to CPU cores and GPUs.

Slurm Workload Manager
----------------------

`Slurm <https://slurm.schedmd.com/>`__ is the workload manager used to interact with the compute nodes on Crusher. In the following subsections, the most commonly used Slurm commands for submitting, running, and monitoring jobs will be covered, but users are encouraged to visit the official documentation and man pages for more information.

Batch Scheduler and Job Launcher
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Slurm provides 3 ways of submitting and launching jobs on Crusher's compute nodes: batch scripts, interactive, and single-command. The Slurm commands associated with these methods are shown in the table below and examples of their use can be found in the related subsections. Please note that regardless of the submission method used, the job will launch on compute nodes, with the first compute in the allocation serving as head-node.

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

A batch script can be used to submit a job to run on the compute nodes at a later time. In this case, stdout and stderr will be written to a file(s) that can be opened after the job completes. Here is an example of a simple batch script:

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

The Slurm submission options are preceded by ``#SBATCH``, making them appear as comments to a shell (since comments begin with ``#``). Slurm will look for submission options from the first line through the first non-comment line. Options encountered after the first non-comment line will not be read by Slurm. In the example script, the lines are:

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

Interactive Jobs
""""""""""""""""

To request an interactive job where multiple job steps (i.e., multiple ``srun`` commands) can be launched on the allocated compute node(s), the ``salloc`` command can be used:

.. code-block:: bash

   $ salloc -A <project_id> -J <job_name> -t 00:05:00 -p <partition> -N 2
   salloc: Granted job allocation 4258
   salloc: Waiting for resource configuration
   salloc: Nodes crusher[010-011] are ready for job

   $ srun -n 4 --ntasks-per-node=2 ./a.out
   <output printed to terminal>

   $ srun -n 2 --ntasks-per-node=1 ./a.out
   <output printed to terminal>

Here, ``salloc`` is used to request an allocation of 2 compute nodes for 5 minutes. Once the resources become available, the user is granted access to the compute nodes (``crusher010`` and ``crusher011`` in this case) and can launch job steps on them using ``srun``.

.. _single-command:

Single Command (non-interactive)
""""""""""""""""""""""""""""""""

.. code-block:: bash

   $ srun -A <project_id> -t 00:05:00 -p <partition> -N 2 -n 4 --ntasks-per-node=2 ./a.out
   <output printed to terminal>

The job name and output options have been removed since stdout/stderr are typically desired in the terminal window in this usage mode.

Common Slurm Submission Options
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The table below summarizes commonly-used Slurm job submission options:

+--------------------------+--------------------------------+
| ``-A <project_id>``       | Project ID to charge           |
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

For more information about these and/or other options, please see the ``sbatch`` man page.

Other Common Slurm Commands
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The table below summarizes commonly-used Slurm commands:

+--------------+---------------------------------------------------------------------------------------------------------------------------------+
| ``sinfo``    | | Used to view partition and node information.                                                                                  |
|              | | E.g., to view user-defined details about the batch queue:                                                                     |
|              | | ``sinfo -p batch -o "%15N %10D %10P %10a %10c %10z"``                                                                         |
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

Crusher's compute nodes are contained within a single Slurm partition (queue) for both CAAR and ECP projects. Please see the table below for details.


Partition
^^^^^^^^^^^^^^

The CAAR and ECP "batch" partition consists of 192 total compute nodes. On a per-project basis, each user can have 2 running and 2 eligible jobs at a time, with up to 20 jobs submitted.

+-----------------+--------------+
| Number of Nodes | Max Walltime |
+=================+==============+
| 1 - 8           | 8 hours      |
+-----------------+--------------+
| 9 - 64          | 6 hours      |
+-----------------+--------------+
| 65 - 160        | 2 hours      |
+-----------------+--------------+

.. note::
    If CAAR or ECP teams require a temporary exception to this policy, please email help@olcf.ornl.gov with your request and it will be given to the OLCF Resource Utilization Council (RUC) for review.

Process and Thread Mapping
--------------------------

This section describes how to map processes (e.g., MPI ranks) and process threads (e.g., OpenMP threads) to the CPUs and GPUs on Crusher. The :ref:`crusher-compute-nodes` diagram will be helpful when reading this section to understand which physical CPU cores (and hardware threads) your processes and threads run on. 

.. note::

    Users are highly encouraged to use the CPU- and GPU-mapping programs used in the following sections to check their understanding of the job steps (i.e., ``srun`` commands) the intend to use in their actual jobs.

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
    $ srun -N1 -n2 ./hello_mpi_omp | sort

    WARNING: Requested total thread count and/or thread affinity may result in
    oversubscription of available CPU resources!  Performance may be degraded.
    Explicitly set OMP_WAIT_POLICY=PASSIVE or ACTIVE to suppress this message.
    Set CRAY_OMP_CHECK_AFFINITY=TRUE to print detailed thread-affinity messages.
    WARNING: Requested total thread count and/or thread affinity may result in
    oversubscription of available CPU resources!  Performance may be degraded.
    Explicitly set OMP_WAIT_POLICY=PASSIVE or ACTIVE to suppress this message.
    Set CRAY_OMP_CHECK_AFFINITY=TRUE to print detailed thread-affinity messages.

    MPI 000 - OMP 000 - HWT 000 - Node crusher001
    MPI 000 - OMP 001 - HWT 000 - Node crusher001
    MPI 001 - OMP 000 - HWT 008 - Node crusher001
    MPI 001 - OMP 001 - HWT 008 - Node crusher001

The first thing to notice here is the ``WARNING`` about oversubscribing the available CPU cores. Also, the output shows each MPI rank did spawn 2 OpenMP threads, but both OpenMP threads ran on the same hardware thread (for a given MPI rank). This was not the intended behavior; each OpenMP thread was meant to run on its own physical CPU core.

The problem here arises from two default settings; 1) each MPI rank is only allocated 1 physical CPU core (``-c 1``) and, 2) only 1 hardware thread per physical CPU core is enabled (``--threads-per-core=1``). So in this case, each MPI rank only has 1 physical core (with 1 hardware thread) to run on - including any threads the process spawns - hence the WARNING and undesired behavior.

**Second (CORRECT) attempt**

In order for each OpenMP thread to run on its own physical CPU core, each MPI rank should be given 2 physical CPU cores (``-c 2``). Now the OpenMP threads will be mapped to unique hardware threads on separate physical CPU cores.

.. code-block:: bash

    $ srun -N1 -n2 -c2 ./hello_mpi_omp | sort
    MPI 000 - OMP 000 - HWT 000 - Node crusher001
    MPI 000 - OMP 001 - HWT 001 - Node crusher001
    MPI 001 - OMP 000 - HWT 008 - Node crusher001
    MPI 001 - OMP 001 - HWT 009 - Node crusher001

Now the output shows that each OpenMP thread ran on (one of the hardware threads of) its own physical CPU core. More specifically (see the Crusher Compute Node diagram), OpenMP thread 000 of MPI rank 000 ran on hardware thread 000 (i.e., physical CPU core 00), OpenMP thread 001 of MPI rank 000 ran on hardware thread 001 (i.e., physical CPU core 01), OpenMP thread 000 of MPI rank 001 ran on hardware thread 008 (i.e., physical CPU core 08), and OpenMP thread 001 of MPI rank 001 ran on hardware thread 009 (i.e., physical CPU core 09) - as intended.

.. note::

    There are many different ways users might choose to perform these mappings, so users are encouraged to clone the ``hello_mpi_omp`` program and test whether or not processes and threads are running where intended.

GPU Mapping
^^^^^^^^^^^

In this sub-section, an MPI+OpenMP+HIP "Hello, World" program (`hello_jobstep <https://code.ornl.gov/olcf/hello_jobstep>`__) will be used to clarify the GPU mappings. Again, Slurm's :ref:`interactive` method was used to request an allocation of 2 compute node for these examples: ``salloc -A <project_id> -t 30 -p <parition> -N 2``. The CPU mapping part of this example is very similar to the example used above in the CPU Mapping sub-section, so the focus here will be on the GPU mapping part.

The following ``srun`` options will be used in the examples below. See ``man srun`` for a complete list of options and more information.

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
| ``--distribution=<value>[:<value>][:<value>]`` | Specifies the distribution of MPI ranks across compute nodes, sockets (L3 regions on Crusher), and cores,    |
|                                                | respectively. The default values are ``block:cyclic:cyclic``                                                 |
+------------------------------------------------+--------------------------------------------------------------------------------------------------------------+

.. note::
    In general, GPU mapping can be accomplished in different ways. For example, an application might map MPI ranks to GPUs programmatically within the code using, say, ``hipSetDevice``. In this case, since all GPUs on a node are available to all MPI ranks on that node by default, there might not be a need to map to GPUs using Slurm (just do it in the code). However, in another application, there might be a reason to make only a subset of GPUs available to the MPI ranks on a node. It is this latter case that the following examples refer to.

Mapping 1 task per GPU
""""""""""""""""""""""

In the following examples, each MPI rank (and its OpenMP threads) will be mapped to a single GPU.

**Example 1: 8 MPI ranks - each with 2 OpenMP threads and 1 GPU (single-node)**

This example launches 8 MPI ranks (``-n8``), each with 2 physical CPU cores (``-c2``) to launch 2 OpenMP threads (``OMP_NUM_THREADS=2``) on. In addition, each MPI rank (and its 2 OpenMP threads) should have access to only 1 GPU. To accomplish the GPU mapping, two new ``srun`` options will be used:

* ``--gpus-per-task`` specifies the number of GPUs required for the job on each task
* ``--gpu-bind=closest`` binds each task to the GPU which is closest.

.. note::
    Without these additional flags, all MPI ranks would have access to all GPUs (which is the default behavior).

.. code-block:: bash

    $ export OMP_NUM_THREADS=2
    $ srun -n8 -c2 --gpus-per-task=1 --gpu-bind=closest ./hello_jobstep | sort

    MPI 000 - OMP 000 - HWT 000 - Node crusher001 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 000 - OMP 001 - HWT 001 - Node crusher001 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 001 - OMP 000 - HWT 008 - Node crusher001 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 001 - OMP 001 - HWT 009 - Node crusher001 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 002 - OMP 000 - HWT 016 - Node crusher001 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 002 - OMP 001 - HWT 017 - Node crusher001 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 003 - OMP 000 - HWT 024 - Node crusher001 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 003 - OMP 001 - HWT 025 - Node crusher001 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 004 - OMP 000 - HWT 032 - Node crusher001 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 004 - OMP 001 - HWT 033 - Node crusher001 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 005 - OMP 000 - HWT 040 - Node crusher001 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 005 - OMP 001 - HWT 041 - Node crusher001 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 006 - OMP 000 - HWT 048 - Node crusher001 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 006 - OMP 001 - HWT 049 - Node crusher001 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 007 - OMP 000 - HWT 056 - Node crusher001 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6
    MPI 007 - OMP 001 - HWT 057 - Node crusher001 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6

The output from the program contains a lot of information, so let's unpack it. First, there are different IDs associated with the GPUs so it is important to describe them before moving on. ``GPU_ID`` is the node-level (or global) GPU ID, which is labeled as one might expect from looking at the Crusher Node Diagram: 0, 1, 2, 3, 4, 5, 6, 7. ``RT_GPU_ID`` is the HIP runtime GPU ID, which can be though of as each MPI rank's local GPU ID number (with zero-based indexing). So in the output above, each MPI rank has access to only 1 unique GPU - where MPI 000 has access to "global" GPU 4, MPI 001 has access to "global" GPU 5, etc., but all MPI ranks show a HIP runtime GPU ID of 0. The reason is that each MPI rank only "sees" one GPU and so the HIP runtime labels it as "0", even though it might be global GPU ID 0, 1, 2, 3, 4, 5, 6, or 7. The GPU's bus ID is included to definitively show that different GPUs are being used.

Here is a summary of the different GPU IDs reported by the example program:

* ``GPU_ID`` is the node-level (or global) GPU ID read from ``ROCR_VISIBLE_DEVICES``. If this environment variable is not set (either by the user or by Slurm), the value of ``GPU_ID`` will be set to ``N/A`` by this program.
* ``RT_GPU_ID`` is the HIP runtime GPU ID (as reported from, say ``hipGetDevice``).
* ``Bus_ID`` is the physical bus ID associated with the GPUs. Comparing the bus IDs is meant to definitively show that different GPUs are being used.

So the job step (i.e., ``srun`` command) used above gave the desired output. Each MPI rank spawned 2 OpenMP threads and had access to a unique GPU. The ``--gpus-per-task=1`` allocated 1 GPU for each MPI rank and the ``--gpu-bind=closest`` ensured that the closest GPU to each rank was the one used.

.. note::

    This example shows an important peculiarity of the Crusher nodes; the "closest" GPUs to each MPI rank are not in sequential order. For example, MPI rank 000 and its two OpenMP threads ran on hardware threads 000 and 001. As can be seen in the Crusher node diagram, these two hardware threads reside in the same L3 cache region, and that L3 region is connected via Infinity Fabric (blue line in the diagram) to GPU 4. This is an important distinction that can affect performance if not considered carefully. 

**Example 2: 16 MPI ranks - each with 2 OpenMP threads and 1 GPU (multi-node)**

This example will extend Example 1 to run on 2 nodes. As the output shows, it is a very straightforward exercise of changing the number of nodes to 2 (``-N2``) and the number of MPI ranks to 16 (``-n16``).

.. code-block:: bash

    $ export OMP_NUM_THREADS=2
    $ srun -N2 -n16 -c2 --gpus-per-task=1 --gpu-bind=closest ./hello_jobstep | sort

    MPI 000 - OMP 000 - HWT 000 - Node crusher001 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 000 - OMP 001 - HWT 001 - Node crusher001 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 001 - OMP 000 - HWT 008 - Node crusher001 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 001 - OMP 001 - HWT 009 - Node crusher001 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 002 - OMP 000 - HWT 016 - Node crusher001 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 002 - OMP 001 - HWT 017 - Node crusher001 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 003 - OMP 000 - HWT 024 - Node crusher001 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 003 - OMP 001 - HWT 025 - Node crusher001 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 004 - OMP 000 - HWT 032 - Node crusher001 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 004 - OMP 001 - HWT 033 - Node crusher001 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 005 - OMP 000 - HWT 040 - Node crusher001 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 005 - OMP 001 - HWT 041 - Node crusher001 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 006 - OMP 000 - HWT 048 - Node crusher001 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 006 - OMP 001 - HWT 049 - Node crusher001 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 007 - OMP 000 - HWT 056 - Node crusher001 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6
    MPI 007 - OMP 001 - HWT 057 - Node crusher001 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6
    MPI 008 - OMP 000 - HWT 000 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 008 - OMP 001 - HWT 001 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 009 - OMP 000 - HWT 008 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 009 - OMP 001 - HWT 009 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 010 - OMP 000 - HWT 016 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 010 - OMP 001 - HWT 017 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 011 - OMP 000 - HWT 024 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 011 - OMP 001 - HWT 025 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 012 - OMP 000 - HWT 032 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 012 - OMP 001 - HWT 033 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 013 - OMP 000 - HWT 040 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 013 - OMP 001 - HWT 041 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 014 - OMP 000 - HWT 048 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 014 - OMP 001 - HWT 049 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 015 - OMP 000 - HWT 056 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6
    MPI 015 - OMP 001 - HWT 057 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6

**Example 3: 8 MPI ranks - each with 2 OpenMP threads and 1 *specific* GPU (single-node)**

This example will be very similar to Example 1, but instead of using ``--gpu-bind=closest`` to map each MPI rank to the closest GPU, ``--gpu-bind=map_gpu`` will be used to map each MPI rank to a *specific* GPU. The ``map_gpu`` option takes a comma-separated list of GPU IDs to specify how the MPI ranks are mapped to GPUs, where the form of the comma-separated list is ``<gpu_id_for_task_0>, <gpu_id_for_task_1>,...``.

.. code:: bash

    $ export OMP_NUM_THREADS=2
    $ srun -N1 -n8 -c2 --gpus-per-task=1 --gpu-bind=map_gpu:4,5,2,3,6,7,0,1 ./hello_jobstep | sort

    MPI 000 - OMP 000 - HWT 000 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 000 - OMP 001 - HWT 001 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 001 - OMP 000 - HWT 008 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 001 - OMP 001 - HWT 009 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 002 - OMP 000 - HWT 016 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 002 - OMP 001 - HWT 017 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 003 - OMP 000 - HWT 024 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 003 - OMP 001 - HWT 025 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 004 - OMP 000 - HWT 032 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 004 - OMP 001 - HWT 033 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 005 - OMP 000 - HWT 040 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 005 - OMP 001 - HWT 041 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 006 - OMP 000 - HWT 048 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 006 - OMP 001 - HWT 049 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 007 - OMP 000 - HWT 056 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6
    MPI 007 - OMP 001 - HWT 057 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6

Here, the output is the same as the results from Example 1. This is because the 8 GPU IDs in the comma-separated list happen to specify the GPUs within the same L3 cache region that the MPI ranks are in. So MPI 000 is mapped to GPU 4, MPI 001 is mapped to GPU 5, etc.

While this level of control over mapping MPI ranks to GPUs might be useful for some applications, it is always important to consider the implication of the mapping. For example, if the order of the GPU IDs in the ``map_gpu`` option is reversed, the MPI ranks and the GPUs they are mapped to would be in different L3 cache regions, which could potentially lead to poorer performance.

**Example 4: 16 MPI ranks - each with 2 OpenMP threads and 1 *specific* GPU (multi-node)**

Extending Examples 2 and 3 to run on 2 nodes is also a straightforward exercise by changing the number of nodes to 2 (``-N2``) and the number of MPI ranks to 16 (``-n16``).

.. code:: bash

    $ export OMP_NUM_THREADS=2
    $ srun -N2 -n16 -c2 --gpus-per-task=1 --gpu-bind=map_gpu:4,5,2,3,6,7,0,1 ./hello_jobstep | sort
    
    MPI 000 - OMP 000 - HWT 000 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 000 - OMP 001 - HWT 001 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 001 - OMP 000 - HWT 008 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 001 - OMP 001 - HWT 009 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 002 - OMP 000 - HWT 016 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 002 - OMP 001 - HWT 017 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 003 - OMP 000 - HWT 024 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 003 - OMP 001 - HWT 025 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 004 - OMP 000 - HWT 032 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 004 - OMP 001 - HWT 033 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 005 - OMP 000 - HWT 040 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 005 - OMP 001 - HWT 041 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 006 - OMP 000 - HWT 048 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 006 - OMP 001 - HWT 049 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 007 - OMP 000 - HWT 056 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6
    MPI 007 - OMP 001 - HWT 057 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6
    MPI 008 - OMP 000 - HWT 000 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 008 - OMP 001 - HWT 001 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 009 - OMP 000 - HWT 008 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 009 - OMP 001 - HWT 009 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 010 - OMP 000 - HWT 016 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 010 - OMP 001 - HWT 017 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 011 - OMP 000 - HWT 024 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 011 - OMP 001 - HWT 025 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 012 - OMP 000 - HWT 032 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 012 - OMP 001 - HWT 033 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 013 - OMP 000 - HWT 040 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 013 - OMP 001 - HWT 041 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 014 - OMP 000 - HWT 048 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 014 - OMP 001 - HWT 049 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 015 - OMP 000 - HWT 056 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6
    MPI 015 - OMP 001 - HWT 057 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6

Mapping multiple MPI ranks to a single GPU
""""""""""""""""""""""""""""""""""""""""""

In the following examples, 2 MPI ranks will be mapped to 1 GPU. For the sake of brevity, ``OMP_NUM_THREADS`` will be set to ``1``, so ``-c1`` will be used unless otherwise specified.

.. note::

    On AMD's MI250X, multi-process service (MPS) is not needed since multiple MPI ranks per GPU is supported natively.

**Example 5: 16 MPI ranks - where 2 ranks share a GPU (round-robin, single-node)**

This example launches 16 MPI ranks (``-n16``), each with 1 physical CPU core (``-c1``) to launch 1 OpenMP thread (``OMP_NUM_THREADS=1``) on. The MPI ranks will be assigned to GPUs in a round-robin fashion so that each of the 8 GPUs on the node are shared by 2 MPI ranks. To accomplish this GPU mapping, a new ``srun`` option will be used:

* ``--ntasks-per-gpu`` specifies the number of MPI ranks that will share access to a GPU.

.. code:: bash

    $ export OMP_NUM_THREADS=1
    $ srun -N1 -n16 -c1 --ntasks-per-gpu=2 --gpu-bind=closest ./hello_jobstep | sort

    MPI 000 - OMP 000 - HWT 000 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 001 - OMP 000 - HWT 008 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 002 - OMP 000 - HWT 016 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 003 - OMP 000 - HWT 024 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 004 - OMP 000 - HWT 032 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 005 - OMP 000 - HWT 040 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 006 - OMP 000 - HWT 048 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 007 - OMP 000 - HWT 056 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6
    MPI 008 - OMP 000 - HWT 001 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 009 - OMP 000 - HWT 009 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 010 - OMP 000 - HWT 017 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 011 - OMP 000 - HWT 025 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 012 - OMP 000 - HWT 033 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 013 - OMP 000 - HWT 041 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 014 - OMP 000 - HWT 049 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 015 - OMP 000 - HWT 057 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6


The output shows the round-robin (``cyclic``) distribution of MPI ranks to GPUs. In fact, it is a round-robin distribution of MPI ranks *to L3 cache regions* (the default distribution). The GPU mapping is a consequence of where the MPI ranks are distributed; ``--gpu-bind=closest`` simply maps the GPU in an L3 cache region to the MPI ranks in the same L3 region.

**Example 6: 32 MPI ranks - where 2 ranks share a GPU (round-robin, multi-node)**

This example is an extension of Example 5 to run on 2 nodes.

.. warning::

    This example requires a workaround to run as expected. ``--ntasks-per-gpu=2`` does not force MPI ranks 008-015 to run on the second node, so the number of physical CPU cores per MPI rank is increased to 4 (``-c4``) to force the desired behavior due to the constraint of the number of physical CPU cores (64) on a node.

.. code:: bash

    $ export OMP_NUM_THREADS=1
    $ srun -N2 -n32 -c4 --ntasks-per-gpu=2 --gpu-bind=closest ./hello_jobstep | sort

    MPI 000 - OMP 000 - HWT 000 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 001 - OMP 000 - HWT 008 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 002 - OMP 000 - HWT 016 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 003 - OMP 000 - HWT 024 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 004 - OMP 000 - HWT 032 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 005 - OMP 000 - HWT 040 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 006 - OMP 000 - HWT 048 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 007 - OMP 000 - HWT 056 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6
    MPI 008 - OMP 000 - HWT 004 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 009 - OMP 000 - HWT 012 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 010 - OMP 000 - HWT 020 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 011 - OMP 000 - HWT 028 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 012 - OMP 000 - HWT 036 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 013 - OMP 000 - HWT 044 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 014 - OMP 000 - HWT 052 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 015 - OMP 000 - HWT 060 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6
    MPI 016 - OMP 000 - HWT 000 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 017 - OMP 000 - HWT 008 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 018 - OMP 000 - HWT 016 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 019 - OMP 000 - HWT 024 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 020 - OMP 000 - HWT 034 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 021 - OMP 000 - HWT 041 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 022 - OMP 000 - HWT 048 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 023 - OMP 000 - HWT 056 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6
    MPI 024 - OMP 000 - HWT 006 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 025 - OMP 000 - HWT 012 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 026 - OMP 000 - HWT 021 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 027 - OMP 000 - HWT 028 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 028 - OMP 000 - HWT 036 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 029 - OMP 000 - HWT 044 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 030 - OMP 000 - HWT 052 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 031 - OMP 000 - HWT 060 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6


**Example 7: 16 MPI ranks - where 2 ranks share a GPU (packed, single-node)**

This example launches 16 MPI ranks (``-n16``), each with 4 physical CPU cores (``-c4``) to launch 1 OpenMP thread (``OMP_NUM_THREADS=1``) on. The MPI ranks will be assigned to GPUs in a packed fashion so that each of the 8 GPUs on the node are shared by 2 MPI ranks. Similar to Example 5, ``-ntasks-per-gpu=2`` will be used, but a new ``srun`` flag will be used to change the default round-robin (``cyclic``) distribution of MPI ranks across NUMA domains:

* ``--distribution=<value>:[<value>]:[<value>]`` specifies the distribution of MPI ranks across compute nodes, sockets (L3 cache regions on Crusher), and cores, respectively. The default values are ``block:cyclic:cyclic``, which is where the ``cyclic`` assignment comes from in the previous examples.

.. note::

    In the job step for this example, ``--distribution=*:block`` is used, where ``*`` represents the default value of ``block`` for the distribution of MPI ranks across compute nodes and the distribution of MPI ranks across L3 cache regions has been changed to ``block`` from its default value of ``cyclic``.

.. note::

    Because the distribution across L3 cache regions has been changed to a "packed" (``block``) configuration, caution must be taken to ensure MPI ranks end up in the L3 cache regions where the GPUs they intend to be mapped to are located. To accomplish this, the number of physical CPU cores assigned to an MPI rank was increased - in this case to 4. Doing so ensures that only 2 MPI ranks can fit into a single L3 cache region. If the value of ``-c`` was left at ``1``, all 8 MPI ranks would be "packed" into the first L3 region, where the "closest" GPU would be GPU 4 - the only GPU in that L3 region.

    Notice that this is not a workaround like in Example 6, but a requirement due to the ``block`` distribution of MPI ranks across NUMA domains.

.. code:: bash

    $ export OMP_NUM_THREADS=1
    $ srun -N1 -n16 -c4 --ntasks-per-gpu=2 --gpu-bind=closest --distribution=*:block ./hello_jobstep | sort
    
    MPI 000 - OMP 000 - HWT 000 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 001 - OMP 000 - HWT 004 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 002 - OMP 000 - HWT 008 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 003 - OMP 000 - HWT 012 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 004 - OMP 000 - HWT 016 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 005 - OMP 000 - HWT 020 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 006 - OMP 000 - HWT 024 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 007 - OMP 000 - HWT 028 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 008 - OMP 000 - HWT 032 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 009 - OMP 000 - HWT 036 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 010 - OMP 000 - HWT 040 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 011 - OMP 000 - HWT 044 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 012 - OMP 000 - HWT 048 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 013 - OMP 000 - HWT 052 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 014 - OMP 000 - HWT 056 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6
    MPI 015 - OMP 000 - HWT 060 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6

The overall effect of using ``--distribution=*:block`` and increasing the number of physical CPU cores available to each MPI rank is to place the first two MPI ranks in the first L2 cache region with GPU 4, the next two MPI ranks in the second L3 cache region with GPU 5, and so on.

**Example 8: 32 MPI ranks - where 2 ranks share a GPU (packed, multi-node)**

This example is an extension of Example 7 to use 2 compute nodes. With the appropriate changes put in place in Example 7, it is a straightforward exercise to change to using 2 nodes (``-N2``) and 32 MPI ranks (``-n32``).

.. code:: bash

    $ export OMP_NUM_THREADS=1
    $ srun -N2 -n32 -c4 --ntasks-per-gpu=2 --gpu-bind=closest --distribution=*:block ./hello_jobstep | sort
    
    MPI 000 - OMP 000 - HWT 000 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 001 - OMP 000 - HWT 004 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 002 - OMP 000 - HWT 010 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 003 - OMP 000 - HWT 012 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 004 - OMP 000 - HWT 016 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 005 - OMP 000 - HWT 021 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 006 - OMP 000 - HWT 024 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 007 - OMP 000 - HWT 028 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 008 - OMP 000 - HWT 032 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 009 - OMP 000 - HWT 037 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 010 - OMP 000 - HWT 041 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 011 - OMP 000 - HWT 044 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 012 - OMP 000 - HWT 049 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 013 - OMP 000 - HWT 052 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 014 - OMP 000 - HWT 056 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6
    MPI 015 - OMP 000 - HWT 060 - Node crusher002 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6
    MPI 016 - OMP 000 - HWT 000 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 017 - OMP 000 - HWT 004 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 018 - OMP 000 - HWT 008 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 019 - OMP 000 - HWT 013 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 020 - OMP 000 - HWT 016 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 021 - OMP 000 - HWT 020 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 022 - OMP 000 - HWT 024 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 023 - OMP 000 - HWT 028 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 024 - OMP 000 - HWT 034 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 025 - OMP 000 - HWT 036 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 026 - OMP 000 - HWT 040 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 027 - OMP 000 - HWT 044 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 028 - OMP 000 - HWT 048 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 029 - OMP 000 - HWT 052 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 030 - OMP 000 - HWT 056 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6
    MPI 031 - OMP 000 - HWT 060 - Node crusher004 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6

Multiple GPUs per MPI rank
""""""""""""""""""""""""""

As mentioned previously, all GPUs are accessible by all MPI ranks by default, so it is possible to *programatically* map any combination of MPI ranks to GPUs. 

..
    However, there is currently no way to use Slurm to map multiple GPUs to a single MPI rank. If this functionality is needed for an application, please submit a ticket by emailing help@olcf.ornl.gov.


.. note::

    There are many different ways users might choose to perform these mappings, so users are encouraged to clone the ``hello_jobstep`` program and test whether or not processes and threads are running where intended.


NVMe Usage
----------

Each Crusher compute node has [2x] 1.92 TB NVMe devices (SSDs) with a peak sequential performance of 5500 MB/s (read) and 2000 MB/s (write). To use the NVMe, users must request access during job allocation using the ``-C nvme`` option to ``sbatch``, ``salloc``, or ``srun``. Once the devices have been granted to a job, users can access them at ``/mnt/bb/<userid>``. Users are responsible for moving data to/from the NVMe before/after their jobs. Here is a simple example script:

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
    Fri Oct 8 12:28:18 EDT 2021

    *****ORIGINAL FILE*****
    This is my file. There are many like it but this one is mine.
    ***********************

    *****UPDATED FILE******
    This is my file. There are many like it but this one is mine.
    crusher025
    ***********************

----

Getting Help
============

If you have problems or need helping running on Crusher, please submit a ticket
by emailing help@olcf.ornl.gov.

Known Issues
============

.. JIRA_CONTENT_HERE



