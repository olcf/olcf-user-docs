.. _frontier-user-guide:

*******************
Frontier User Guide
*******************

.. _system_overview:

System Overview
===============

Frontier is a HPE Cray EX supercomputer located at the Oak Ridge Leadership Computing Facility. With a theoretical peak double-precision performance of approximately 2 exaflops (2 quintillion calculations per second), it is the fastest system in the world for a wide range of traditional computational science applications.

.. _frontier-nodes:

Frontier Nodes
--------------

A picture containing a node diagram goes here.

A description of the setup of the nodes. 


Node Types
----------

Describe different nodes: logins, batch, computes, etc.

System Interconnect
-------------------

Describe how nodes are connected.

File Systems
------------

Explain the filesystem.

Operating System
----------------

State the operating system and current version.

Hardware Threads
----------------

A blurb here about hardware thread support.

GPUs
----

Describe the specs and capability of the GPUs in use on the compute nodes.



Connecting
==========

To connect to Frontier, ``ssh`` to ``frontier.olcf.ornl.gov``. For example:

.. code-block:: bash

    $ ssh <username>@frontier.olcf.ornl.gov

For more information on connecting to OLCF resources, see :ref:`connecting-to-olcf`.

----

Data and Storage
================

For more detailed information about center-wide file systems and data archiving available on Frontier, please refer to the pages on :ref:`data-storage-and-transfers`. The subsections below give a quick overview of NFS and GPFS storage spaces as well as the on node NVMe "Burst Buffers" (SSDs).

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

.. note::

    Frontier will be migrating from the Alpine Spectrum Scale filesystem to the Orion Lustre filesystem in the coming months. Details will be added to this section as they become available.

NVMe
----

Each compute node on Frontier has [2x] 1.92TB \ **N**\ on-\ **V**\ olatile **Me**\mory (NVMe) storage devices (SSDs), colloquially known as a "Burst Buffer" with a peak sequential performance of 5500 MB/s (read) and 2000 MB/s (write). The NVMes could be used to reduce the time that applications wait for I/O. Using the two SSD drives per compute node, the burst buffer can be used to transfer data to or from the drive before the application reads a file or after it writes a file. The result will be that the application benefits from native SSD performance for a portion of its I/O requests. Users are not required to use the NVMes. Data can also be written directly to the parallel filesystem.

.. figure:: /images/frontier_nvme_arch.png
   :align: center

   The NVMes on Frontier are local to each node.

NVMe Usage
----------

To use the NVMe, users must request access during job allocation using the ``-C nvme`` option to ``sbatch``, ``salloc``, or ``srun``. Once the devices have been granted to a job, users can access them at ``/mnt/bb/<userid>``. **Users are responsible for moving data to/from the NVMe before/after their jobs**. Here is a simple example script:

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

    *****ORIGINAL FILE*****
    This is my file. There are many like it but this one is mine.
    ***********************

    *****UPDATED FILE******
    This is my file. There are many like it but this one is mine.
    frontier0123
    ***********************

----

AMD GPUs
========

Each Frontier node uses 4 AMD MI200 GPUs.

Compiling
=========

Compilers
---------

Cray, AMD, and GCC compilers are provided through modules on Frontier. The Cray and AMD compilers are both based on LLVM/Clang. There is also a system/OS versions of GCC available in ``/usr/bin``. The table below lists details about each of the module-provided compilers.

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

The MPI implementation available on Frontier is Cray's MPICH, which is "GPU-aware" so GPU buffers can be passed directly to MPI calls.

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

    There are extra steps needed to enable GPU-aware MPI on Frontier, which depend on the compiler that is used (see 1. and 2. below).
    

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

Determining the Compatibility of Cray MPICH and ROCm
""""""""""""""""""""""""""""""""""""""""""""""""""""

Releases of ``cray-mpich`` are each built with a specific version of ROCm, and compatibility across multiple versions is not guaranteed. OLCF will maintain compatible default modules when possible. If using non-default modules, you can determine compatibility by reviewing the *Product and OS Dependencies* section in the ``cray-mpich`` release notes. This can be displayed by running ``module show cray-mpich/<version>``. If the notes indicate compatibility with *AMD ROCM X.Y or later*, only use ``rocm/X.Y.Z`` modules. If using a non-default version of ``cray-mpich``, you must add ``${CRAY_MPICH_ROOTDIR}/gtl/lib`` to either your ``LD_LIBRARY_PATH`` at run time or your executable's rpath at build time.

The compatibility table below was determined by linker testing with all current combinations of ``cray-mpich`` and ``rocm`` modules on Crusher.

+------------+---------------------+
| cray-mpich |        ROCm         |
+============+=====================+
|   8.1.12   |    4.5.2, 4.5.0     |
+------------+---------------------+
|   8.1.14   |    4.5.2, 4.5.0     |
+------------+---------------------+
|   8.1.15   | 5.1.0, 5.0.2, 5.0.0 |
+------------+---------------------+
|   8.1.16   | 5.1.0, 5.0.2, 5.0.0 |
+------------+---------------------+

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

    Make sure the ``craype-accel-amd-gfx90a`` module is loaded when compiling HIP with the Cray compiler wrappers.

+-------------------+--------------------------------------------------------------------------------------------------------------------------+
| Compiler          | Compile/Link Flags, Header Files, and Libraries                                                                          |
+===================+==========================================================================================================================+
| | ``CC``          | | ``CFLAGS = -std=c++11 -D__HIP_ROCclr__ -D__HIP_ARCH_GFX90A__=1 --rocm-path=${ROCM_PATH} --offload-arch=gfx90a -x hip`` |
| | Only with       | | ``LFLAGS = --rocm-path=${ROCM_PATH}``                                                                                  |
| | ``PrgEnv-cray`` | | ``-L${ROCM_PATH}/lib -lamdhip64``                                                                                      |
| | ``PrgEnv-amd``  |                                                                                                                          |
+-------------------+--------------------------------------------------------------------------------------------------------------------------+
| ``hipcc``         | | Can be used directly to compile HIP source files.                                                                      |
|                   | | To see what is being invoked within this compiler driver, issue the command, ``hipcc --verbose``                       |
|                   | | To explicitly target AMD MI250X, use ``--amdgpu-target=gfx90a``                                                        |
+-------------------+--------------------------------------------------------------------------------------------------------------------------+

HIP + OpenMP CPU Threading
--------------------------

This section shows how to compile HIP + OpenMP CPU threading hybrid codes.

.. note::

    Make sure the ``craype-accel-amd-gfx90a`` module is loaded when compiling HIP with the Cray compiler wrappers.

+----------+-----------+-----------------------------------------------------------------------------------------------------------------------------------+
| Vendor   | Compiler  | Compile/Link Flags, Header Files, and Libraries                                                                                   |
+==========+===========+===================================================================================================================================+
| AMD/Cray | ``CC``    | | ``CFLAGS = -std=c++11 -D__HIP_ROCclr__ -D__HIP_ARCH_GFX90A__=1 --rocm-path=${ROCM_PATH} --offload-arch=gfx90a -x hip -fopenmp`` |
|          |           | | ``LFLAGS = --rocm-path=${ROCM_PATH}``                                                                                           |
|          |           | | ``-L${ROCM_PATH}/lib -lamdhip64``                                                                                               |
|          +-----------+-----------------------------------------------------------------------------------------------------------------------------------+
|          | ``hipcc`` | | Can be used to directly compile HIP source files, add ``-fopenmp`` flag to enable OpenMP threading                              |
|          |           | | To explicitly target AMD MI250X, use ``--amdgpu-target=gfx90a``                                                                 |
+----------+-----------+-----------------------------------------------------------------------------------------------------------------------------------+
| GNU      | ``CC``    | | The GNU compilers cannot be used to compile HIP code, so all HIP kernels must be separated from CPU code.                       |
|          |           | | During compilation, all non-HIP files must be compiled with ``CC`` while HIP kernels must be compiled with ``hipcc``.           |
|          |           | | Then linking must be performed with the ``CC`` wrapper.                                                                         |
|          |           | | NOTE: When using ``cmake``, HIP code must currently be compiled using ``amdclang++`` instead of ``hipcc``.                      |
+----------+-----------+-----------------------------------------------------------------------------------------------------------------------------------+


----


Running Jobs
============

Computational work on Frontier is performed by *jobs*. Jobs typically consist of several componenets:

-  A batch submission script 
-  A binary executable
-  A set of input files for the executable
-  A set of output files created by the executable

In general, the process for running a job is to:

#. Prepare executables and input files.
#. Write a batch script.
#. Submit the batch script to the batch scheduler.
#. Optionally monitor the job before and during execution.

The following sections describe in detail how to create, submit, and manage jobs for execution on Frontier. Frontier uses SchedMD's Slurm Workload Manager as the batch scheduling system.


Login vs Compute Nodes
----------------------

Recall from the System Overview that Frontier contains two node types: Login and Compute. When you connect to the system, you are placed on a *login* node. Login nodes are used for tasks such as code editing, compiling, etc. They are shared among all users of the system, so it is not appropriate to run tasks that are long/computationally intensive on login nodes. Users should also limit the number of simultaneous tasks on login nodes (e.g. concurrent tar commands, parallel make 

Compute nodes are the appropriate place for long-running, computationally-intensive tasks. When you start a batch job, your batch script (or interactive shell for batch-interactive jobs) runs on one of your allocated compute nodes.

.. warning::
  Compute-intensive, memory-intensive, or other disruptive processes running on login nodes may be killed without warning.

.. note::
  Unlike Summit and Titan, there are no launch/batch nodes on Frontier. This means your batch script runs on a node allocated to you rather than a shared node. You still must use the job launcher (srun) to run parallel jobs across all of your nodes, but serial tasks need not be launched with srun.


Slurm
-----

Frontier uses SchedMD's Slurm workload manager for scheduling jobs. Proir systems used different schedulers (Summit used IBM's LSF, many others used Moab). While most of these systems provide similar functionality, but with different commands/options. A comparison of a few important commands is below, but SchedMD provides a more complete reference in their `Rosetta Stone of Workload Managers <https://slurm.schedmd.com/rosetta.pdf>`_.

Slurm documentation for each command is available on the system via the ``man`` utility as well as on the web at ` <https://slurm.schedmd.com/man_index.html>`_. Additional documentation is available at ` <https://slurm.schedmd.com/documentation.html>`_.

Some common Slurm commands are summarized in the table below. More complete examples are given in the Monitoring and Modifying Batch Jobs section of this guide.

+--------------+------------------------------------------------+------------------------------------+
| Command      | Action/Task                                    | LSF Equivalent                     |
+==============+================================================+====================================+
| ``squeue``   | Show the current queue                         | ``bjobs``                          |
+--------------+------------------------------------------------+------------------------------------+
| ``sbatch``   | Submit a batch script                          | ``bsub``                           |
+--------------+------------------------------------------------+------------------------------------+
| ``salloc``   | Submit an interactive job                      | ``bsub -Is $SHELL``                |
+--------------+------------------------------------------------+------------------------------------+
| ``srun``     | Launch a parallel job                          | ``jsrun``                          |
+--------------+------------------------------------------------+------------------------------------+
| ``sinfo``    | Show node/partition info                       | ``bqueues`` or ``bhosts``          |
+--------------+------------------------------------------------+------------------------------------+
| ``sacct``    | View accounting information for jobs/job steps | ``bacct``                          |
+--------------+------------------------------------------------+------------------------------------+
| ``scancel``  | Cancel a job or job step                       | ``bkill``                          |
+--------------+------------------------------------------------+------------------------------------+
| ``scontrol`` | View or modify job configuration.              | ``bstop``, ``bresume``, ``bmod``   |
+--------------+------------------------------------------------+------------------------------------+


Batch Scripts
-------------

The most common way to interact with the batch system is via batch scripts. A batch script is simply a shell script with added directives to request various resoruces from or provide certain information to the scheduling system.  Aside from these directives, the batch script is simply the series of commands needed to set up and run your job.

To submit a batch script, use the command ``sbatch myjob.sl``

Consider the following batch script:

.. code-block:: bash
   :linenos:

    #!/bin/bash
    #SBATCH -A ABC123
    #SBATCH -J RunSim123
    #SBATCH -o %x-%j.out
    #SBATCH -t 1:00:00
    #SBATCH -p batch
    #SBATCH -N 1024

    cd $MEMBERWORK/abc123/Run.456
    cp $PROJWORK/abc123/RunData/Input.456 ./Input.456
    srun ...
    cp my_output_file $PROJWORK/abc123/RunData/Output.456

In the script, Slurm directives are preceded by ``#SBATCH``, making them appear as somments to the shell. Slurm looks for these directives through the first non-comment, non-whitespace line. Options after that will be ignored by Slurm (and the shell).

+------+-------------------------------------------------------------------------------------------------+
| Line | Description                                                                                     |
+======+=================================================================================================+
|    1 | Shell interpreter line                                                                          |
+------+-------------------------------------------------------------------------------------------------+
|    2 | OLCF project to charge                                                                          |
+------+-------------------------------------------------------------------------------------------------+
|    3 | Job name                                                                                        |
+------+-------------------------------------------------------------------------------------------------+
|    4 | Job standard output file (``%x`` will be replaced with the job name and ``%j`` with the Job ID) |
+------+-------------------------------------------------------------------------------------------------+
|    5 | Walltime requested (in ``HH:MM:SS`` format). See the table below for other formats.             |
+------+-------------------------------------------------------------------------------------------------+
|    6 | Partition (queue) to use                                                                        |
+------+-------------------------------------------------------------------------------------------------+
|    7 | Number of compute nodes requested                                                               |
+------+-------------------------------------------------------------------------------------------------+
|    8 | Blank line                                                                                      |
+------+-------------------------------------------------------------------------------------------------+
|    9 | Change into the run directory                                                                   |
+------+-------------------------------------------------------------------------------------------------+
|   10 | Copy the input file into place                                                                  |
+------+-------------------------------------------------------------------------------------------------+
|   11 | Run the job ( add layout details )                                                              |
+------+-------------------------------------------------------------------------------------------------+
|   12 | Copy the output file to an appropriate location.                                                |
+------+-------------------------------------------------------------------------------------------------+


Interactive Jobs
----------------

Most users will find batch jobs an easy way to use the system, as they allow you to "hand off" a job to the scheduler, allowing them to focus on other tasks while their job waits in the queue and eventually runs. Occasionally, it is necessary to run interactively, especially when developing, testing, modifying or debugging a code.

Since all compute resources are managed and scheduled by Slurm, it is not possible to simply log into the system and immediately begin running parallel codes interactively. Rather, you must request the appropriate resources from Slurm and, if necessary, wait for them to become available. This is done through an "interactive batch" job. Interactive batch jobs are submitted with the ``salloc`` command. Resources are requested via the same options that are passed via ``#SBATCH`` in a regular batch script (but without the ``#SBATCH`` prefix). For example, to request an interactive batch job with the same resources that the batch script above requests, you would use ``salloc -A ABC123 -J RunSim123 -t 1:00:00 -p batch -N 1024``. Note there is no option for an output file...you are running interactively, so standard output and standard error will be displayed to the terminal.


Common Slurm Options
--------------------

The table below summarizes options for submitted jobs. Unless otherwise noted, they can be used for either batch scripts or interactive batch jobs. For scripts, they can be added on the ``sbatch`` command line or as a ``#BSUB`` directive in the batch script. (If they're specified in both places, the command line takes precedence.) This is only a subset of all available options. Check the `Slurm Man Pages <https://slurm.schedmd.com/man_index.html>`_ for a more complete list.

+------------------------+--------------------------------------------+--------------------------------------------------------------------------------------+
| Option                 | Example Usage                              | Description                                                                          |
+========================+============================================+======================================================================================+
| ``-A``                 | ``#SBATCH -A ABC123``                      | Specifies the project to which the job should be charged                             |
+------------------------+--------------------------------------------+--------------------------------------------------------------------------------------+
| ``-N``                 | ``#SBATCH -N 1024``                        | Request 1024 nodes for the job                                                       |
+------------------------+--------------------------------------------+--------------------------------------------------------------------------------------+
| ``-t``                 | ``#SBATCH -t 4:00:00``                     | Request a walltime of 4 hours.                                                       |
|                        |                                            | Walltime requests can be specified as minutes, hours:minutes, hours:minuts:seconds   |
|                        |                                            | days-hours, days-hours:minutes, or days-hours:minutes:seconds                        |
+------------------------+--------------------------------------------+--------------------------------------------------------------------------------------+
| ``--threads-per-core`` | ``#SBATCH --threads-per-core=2``           | Number of active hardware threads per core. Can be 1 or 2 (1 is default)             |
+------------------------+--------------------------------------------+--------------------------------------------------------------------------------------+
| ``-d``                 | ``#SBATCH -d afterok:12345``               | Specify job dependency (in this example, this job cannot start until job 12345 exits |
|                        |                                            | with an exit code of 0. See the Job Dependency section for more information          |
+------------------------+--------------------------------------------+--------------------------------------------------------------------------------------+
| ``-C``                 | ``#SBATCH -C nvme``                        | Request the burst buffer/NVMe on each node be made available for your job. See       |
|                        |                                            | the Burst Buffers section for more information on using them.                        |
+------------------------+--------------------------------------------+--------------------------------------------------------------------------------------+
| ``-J``                 | ``#SBATCH -J MyJob123``                    | Specify the job name (this will show up in queue listings)                           |
+------------------------+--------------------------------------------+--------------------------------------------------------------------------------------+
| ``-o``                 | ``#SBATCH -o jobout.%j``                   | File where job STDOUT will be directed (%j will be replaced with the job ID).        |
|                        |                                            | If no `-e` option is specified, job STDERR will be placed in this file, too.         |
+------------------------+--------------------------------------------+--------------------------------------------------------------------------------------+
| ``-e``                 | ``#SBATCH -e joberr.%j``                   | File where job STDERR will be directed (%j will be replaced with the job ID).        |
|                        |                                            | If no `-o` option is specified, job STDOUT will be placed in this file, too.         |
+------------------------+--------------------------------------------+--------------------------------------------------------------------------------------+
| ``--mail-type``        | ``#SBATCH --mail-type=END``                | Send email for certain job actions. Can be a comma-separated list. Actions include   |
|                        |                                            | BEGIN, END, FAIL, REQUEUE, INVALID_DEPEND, STAGE_OUT, ALL, and more.                 |
+------------------------+--------------------------------------------+--------------------------------------------------------------------------------------+
| ``--mail-user``        | ``#SBATCH --mail-user=user@somewhere.com`` | Email address to be used for notifications.                                          |
+------------------------+--------------------------------------------+--------------------------------------------------------------------------------------+


Slurm Environment Variables
---------------------------

Slurm reads a number of environment variables, many of which can provide the same information as the job options noted above. We recommend using the job options rather than environment variables to specify job options, as it allows you to have everything self-contained within the job submission script (rather than having to remember what options you set for a given job).

Slurm also provides a number of environment variables within your running job. The following table summarizes those that may be particularly useful within your job (e.g. for naming output log files):

+--------------------------+-----------------------------------------------------------------------------------------+
| Variable                 | Description                                                                             |
+==========================+=========================================================================================+
| ``$SLURM_SUBMIT_DIR``    | The directory from which the batch job was submitted. By default, a new job starts      |
|                          | in your home directory. You can get back to the directory of job submission with        |
|                          | ``cd $SLURM_SUBMIT_DIR``. Note that this is not necessarily the same directory in which |
|                          | the batch script resides.                                                               |
+--------------------------+-----------------------------------------------------------------------------------------+
| ``$SLURM_JOBID``         | The job’s full identifier. A common use for ``$SLURM_JOBID`` is to append the job’s ID  |
|                          | to the standard output and error files.                                                 |
+--------------------------+-----------------------------------------------------------------------------------------+
| ``$SLURM_JOB_NUM_NODES`` | The number of nodes requested.                                                          |
+--------------------------+-----------------------------------------------------------------------------------------+
| ``$SLURM_JOB_NAME``      | The job name supplied by the user.                                                      |
+--------------------------+-----------------------------------------------------------------------------------------+
| ``$SLURM_NODELIST``      | The list of nodes assigned to the job.                                                  |
+--------------------------+-----------------------------------------------------------------------------------------+


Job States
----------

A job will transition through several states during its lifetime. Common ones include:

+-------+------------+-------------------------------------------------------------------------------+
| State | State      | Description                                                                   |
| Code  |            |                                                                               | 
+=======+============+===============================================================================+
| CA    | Canceled   | The job was canceled (could've been by the user or an administrator)          |
+-------+------------+-------------------------------------------------------------------------------+
| CD    | Completed  | The job completed successfully (exit code 0)                                  |
+-------+------------+-------------------------------------------------------------------------------+
| CG    | Completing | The job is in the process of completing (some processes may still be running) |
+-------+------------+-------------------------------------------------------------------------------+
| PD    | Pending    | The job is waiting for resources to be allocated                              |
+-------+------------+-------------------------------------------------------------------------------+
| R     | Running    | The job is currently running                                                  |
+-------+------------+-------------------------------------------------------------------------------+


Job Reason Codes
----------------

In addition to state codes, jobs that are pending will have a "reason code" to explain why the job is pending. Completed jobs will have a reason describing how the job ended. Some codes you might see include:

+-------------------+---------------------------------------------------------------------------------------------------------------+
| Reason            | Meaning                                                                                                       |
+===================+===============================================================================================================+
| Dependency        | Job has dependencies that have not been met                                                                   |
+-------------------+---------------------------------------------------------------------------------------------------------------+
| JobHeldUser       | Job is held at user's request                                                                                 |
+-------------------+---------------------------------------------------------------------------------------------------------------+
| JobHeldAdmin      | Job is held at system administrator's request                                                                 |
+-------------------+---------------------------------------------------------------------------------------------------------------+
| Priority          | Other jobs with higher priority exist for the partition/reservation                                           |
+-------------------+---------------------------------------------------------------------------------------------------------------+
| Reservation       | The job is waiting for its reservation to become available                                                    |
+-------------------+---------------------------------------------------------------------------------------------------------------+
| AssocMaxJobsLimit | The job is being held because the user/project has hit the limit on running jobs                              |
+-------------------+---------------------------------------------------------------------------------------------------------------+
| ReqNodeNotAvail   | The requested a particular node, but it's currently unavailable (it's in use, reserved, down, draining, etc.) |
+-------------------+---------------------------------------------------------------------------------------------------------------+
| JobLaunchFailure  | Job failed to launch (could due to system problems, invalid program name, etc.)                               |
+-------------------+---------------------------------------------------------------------------------------------------------------+
| NonZeroExitCode   | The job exited with some code other than 0                                                                    |
+-------------------+---------------------------------------------------------------------------------------------------------------+

Many other states and job reason codes exist. For a more complete description, see the ``squeue`` man page (either on the system or online).


Scheduling Policy
-----------------

In a simple batch queue system, jobs run in a first-in, first-out (FIFO) order. This can lead to inefficient use of the system. If a large job is the next to run, a strict FIFO queue can cause nodes to sit idle while waiting for the large job to start. *Backfilling* would allow smaller, shorter jobs to use those resources that would otherwise remain idle until the large job starts. With the proper algorithm, they would do so without impacting the start time of the large job. While this does make more efficient use of the system, it encourages the submission of smaller jobs.

The DOE Leadership-Class Job Mandate
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As a DOE Leadership Computing Facility, OLCF has a mandate that a large portion of Frontier's usage come from large, *leadership-class* (a.k.a. *capability*) jobs. To ensure that OLCF complies with this directive, we strongly encourage users to run jobs on Frontier that are as large as their code will allow. To that end, OLCF implements queue policies that enable large jobs to run in a timely fashion.

.. note::
  The OLCF implements queue policies that encourage the submission and timely execution of large, leadership-class jobs on Frontier.

The basic priority mechanism for jobs waiting in the queue is the time the job has been waiting in the queue. If your jobs require resources outside these policies such as higher priorit or longer walltimes, please contact help@olcf.ornl.gov

Jobs by Node Count
^^^^^^^^^^^^^^^^^^

+-----+-----------+-----------+----------------------+--------------------+
| Bin | Min Nodes | Max Nodes | Max Walltime (Hours) | Aging Boost (Days) |
+=====+===========+===========+======================+====================+
|     |           |           |                      |                    |
+-----+-----------+-----------+----------------------+--------------------+


Allocation Overuse Policy
^^^^^^^^^^^^^^^^^^^^^^^^^

Projects that overrun their allocation are still allowed to run on OLCF systems, although at a reduced priority. Like the adjustment for the number of processors requested above, this is an adjustment to the apparent submit time of the job. However, this adjustment has the effect of making jobs appear much younger than jobs submitted under projects that have not exceeded their allocation. In addition to the priority change, these jobs are also limited in the amount of wall time that can be used. For example, consider that `job1` is submitted at the same time as `job2`. The project associated with `job1` is over its allocation, while the project for `job2` is not. The batch system will consider `job2` to have been waiting for a longer time than `job1`. Additionally, projects that are at 125% of their allocated time will be limited to only 3 running jobs at a time. The adjustment to the apparent submit time depends upon the percentage that the project is over its allocation, as shown in the table below:

+----------------------+-----------+
| % of Allocation Used | Priority  |
|                      | Reduction |
+======================+===========+
| < 100%               | none      |
+----------------------+-----------+
| >=100% but <=125%    | 30 days   |
+----------------------+-----------+
| > 125%               | 365 days  |
+----------------------+-----------+


System Reservation Policy
^^^^^^^^^^^^^^^^^^^^^^^^^

Projects may request to reserve a set of nodes for a period of time by contacting help@olcf.ornl.gov. If the reservation is granted, the reserved nodes will be blocked from general use for a given period of time. Only users that have been authorized to use the reservation can utilize those resources. ince no other users can access the reserved resources, it is crucial that groups given reservations take care to ensure the utilization on those resources remains high. To prevent reserved resources from remaining idle for an extended period of time, reservations are monitored for inactivity. If activity falls below 50% of the reserved resources for more than (30) minutes, the reservation will be canceled and the system will be returned to normal scheduling. A new reservation must be requested if this occurs.

The requesting project’s allocation is charged according to the time window granted, regardless of actual utilization. For example, an 8-hour, 2,000 node reservation on Frontier would be equivalent to using 16,000 Frontier node-hours of a project’s allocation.

.. note::
  Reservations should not be confused with priority requests. If quick turnaround is needed for a few jobs or for a period of time, a priority boost should be requested. A reservation should only be requested if users need to guarantee availability of a set of nodes at a given time, such as for a live demonstration at a conference.


Job Dependencies
----------------

Oftentimes, a job will need data from some other job in the queue, but it's nonetheless convenient to submit the second job before the first finishes. Slurm allows you to submit a job with constraints that will keep it from running until these dependencies are met. These are specified with the ``-d`` option to Slurm. Common dependency flags are summarized below. In each of these examples, only a single jobid is shown but you can specify multiple job IDs as a colon-delimited list (i.e. ``#SBATCH -d afterok:12345:12346:12346``). For the ``after`` dependency, you can optionally specify a ``+time`` value for each jobid.

+-----------------------------------+---------------------------------------------------------------------------------------------------+
| Flag                              | Meaning (for the dependent job)                                                                   |
+===================================+===================================================================================================+
| ``#SBATCH -d after:jobid[+time]`` | The job can start after the specified jobs start or are canceled. The optional ``+time`` argument |
|                                   | is a number of minutes. If specified, the job cannot start until that many minutes have passed    |
|                                   | since the listed jobs start/are canceled. If not specified, there is no delay.                    |
+-----------------------------------+---------------------------------------------------------------------------------------------------+
| ``#SBATCH -d afterany:jobid``     | The job can start after the specified jobs have ended (regardless of exit state)                  |
+-----------------------------------+---------------------------------------------------------------------------------------------------+
| ``#SBATCH -d afternotok:jobid``   | The job can start after the specified jobs terminate in a failed (non-zero) state                 |
+-----------------------------------+---------------------------------------------------------------------------------------------------+
| ``#SBATCH -d afterok:jobid``      | The job can start after the specified jobs complete successfully (i.e. zero exit code)            |
+-----------------------------------+---------------------------------------------------------------------------------------------------+
| ``#SBATCH -d singleton``          | Job can begin after any previously-launched job with the same name and from the same user         |
|                                   | have completed. In other words, serialize the running jobs based on username+jobname pairs.       |
+-----------------------------------+---------------------------------------------------------------------------------------------------+


Monitoring and Modifying Batch Jobs
-----------------------------------

``scontrol hold`` and ``scontrol release``: Holding and Releasing Jobs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes you may need to place a hold on a job to keep it from starting. For example, you may have submitted it assuming some needed data was in place but later realized that data is not yet available. This can be done with the ``scontrol hold`` command. Later, when the data is ready, you can release the job (i.e. tell the system that it's now OK to run the job) with the ``scontrol release`` command. For example:

+----------------------------+------------------------------------------------------------+
| ``scontrol hold 12345``    | Place job 12345 on hold                                    | 
+----------------------------+------------------------------------------------------------+
| ``scontrol release 12345`` | Release job 12345 (i.e. tell the system it's OK to run it) |
+----------------------------+------------------------------------------------------------+


``scontrol update``: Changing Job Parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There may also be occasions where you want to modify a job that's waiting in the queue. For example, perhaps you requested 2,000 nodes but later realized this is a different data set and only needs 1,000 nodes. You can use the ``scontrol update`` command for this. For example:

+---------------------------------------------------+-----------------------------------------------+
| ``scontrol update NumNodes=1000 JobID=12345``     | Change job 12345's node request to 1000 nodes |
+---------------------------------------------------+-----------------------------------------------+
| ``scontrol update TimeLimit=4:00:00 JobID=12345`` | Change job 12345's max walltime to 4 hours    |
+---------------------------------------------------+-----------------------------------------------+


``scancel``: Cancel a Job
^^^^^^^^^^^^^^^^^^^^^^^^^

If you need to remove a job from the queue, use the ``scancel`` command. For example, ``scancel 12345``


``squeue``: View the Queue
^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``squeue`` command is used to show the batch queue. You can filter the level of detail through several command-line options. For example:

+------------------------+------------------------------------------------+
| ``squeue -l``          | Show all jobs currently in the queue           |
+------------------------+------------------------------------------------+
| ``squeue -l -u $USER`` | Show all of *your* jobs currently in the queue |
+------------------------+------------------------------------------------+


``sacct``: Get Job Accounting Information
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``sacct`` command gives detailed information about jobs currently in the queue and recently-completed jobs. You can also use it to see the various steps within a batch jobs. 

+-----------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| ``sacct -a -X``                                                                   | Show all jobs (``-a``) in the queue, but summarize the whole allocation instead of showing individual steps (``-X``) |
+-----------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| ``sacct -u $USER``                                                                | Show all of your jobs, and show the individual steps (since there was no ``-X`` option)                              |
+-----------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| ``sacct -j 12345``                                                                | Show all job steps that are part of job 12345                                                                        |
+-----------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| ``sacct -u $USER -S 2022-07-01T13:00:00 -o "jobid%5,jobname%25,nodelist%20" -X``  | Show all of your jobs since 1 PM on July 1, 2022 using a particular output format                                    |
+-----------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------+

``scontrol show job``: Get Detailed Job Information
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In addition to holding, releasing, and updating the job, the ``scontrol`` command can show detailed job information via the ``show job`` subcommand. For example, ``scontrol show job 12345``.



Srun
----------------------

The ``srun`` command is used to execute an MPI binary on one or more compute nodes in parallel.
``srun`` accepts the following common options:

+--------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+
| ``-N``                                                 | Number of nodes                                                                                                |
+--------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+
| ``-n``                                                 | Total number of MPI tasks                                                                                      |
+--------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+
| ``-c, --cpus-per-task=<ncpus>``                        | Logical cores per MPI task (default is 1)                                                                      |
+--------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+
| ``--cpu-bind=threads``                                 | | Bind tasks to CPUs.                                                                                          |
|                                                        | | ``threads`` - (default, recommended) Automatically generate masks binding tasks to threads.                  |
|                                                        | | ``no`` - Allow code to control thread affinity                                                               |
+--------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+
| ``--threads-per-core=<threads>``                       | | In task layout, use the specified maximum number of hardware threads per core                                |
|                                                        | | (default is 1; there are 2 hardware threads per physical CPU core).                                          |
|                                                        | | Must also be set in ``salloc`` or ``sbatch`` if using ``--threads-per-core=2`` in your ``srun`` command.     |
+--------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+
| ``-m, --distribution=<value>:<value>:<value>``         | | Specifies the distribution of MPI ranks across compute nodes, sockets (L3 regions), and cores, respectively. |
|                                                        | | The default values are ``block:cyclic:cyclic``                                                               |
|                                                        | | Currently, the distribution setting for cores (the third "<value>" entry) has no effect on Frontier          |
+--------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+
|  ``--ntasks-per-node=<ntasks>``                        | | If used without ``-n``: requests that a specific number of tasks be invoked on each node.                    |
|                                                        | | If used with ``-n``: treated as a *maximum* count of tasks per node.                                         |
+--------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+

.. note::
    If you do not specify the number of MPI tasks to ``srun``
    via ``-n``, the system will default to using only one task per node.


Below is a comparison table between srun and jsrun.

+--------------------------------------------+---------------------------+-------------------------+
| Option                                     | jsrun (Summit)            | srun  (Frontier)        |
+============================================+===========================+=========================+
| Number of nodes                            | ``-nnodes``               | ``-N, --nnodes``        |
+--------------------------------------------+---------------------------+-------------------------+
| Number of tasks                            | defined with resource set | ``-n, --ntasks``        |
+--------------------------------------------+---------------------------+-------------------------+
| Number of tasks per node                   | defined with resource set | ``--ntasks-per-node``   |
+--------------------------------------------+---------------------------+-------------------------+
| Number of CPUs per task                    | defined with resource set | ``-c, --cpus-per-task`` |
+--------------------------------------------+---------------------------+-------------------------+
| Number of resource sets                    | ``-n, --nrs``             | N/A                     |
+--------------------------------------------+---------------------------+-------------------------+
| Number of resource sets per host           | ``-r, --rs_per_host``     | N/A                     |
+--------------------------------------------+---------------------------+-------------------------+
| Number of tasks per resource set           | ``-a, --tasks_per_rs``    | N/A                     |
+--------------------------------------------+---------------------------+-------------------------+
| Number of CPUs per resource set            | ``-c, --cpus_per_rs``     | N/A                     |
+--------------------------------------------+---------------------------+-------------------------+
| Number of GPUs per resource set            | ``-g, --gpus_per_rs``     | N/A                     |
+--------------------------------------------+---------------------------+-------------------------+
| Bind tasks to allocated CPUs               | ``-b, --bind``            | ``--cpu-bind``          |
+--------------------------------------------+---------------------------+-------------------------+
| Do not run more than one task on resources | ``--tasks_per_rs 1``      | ``--exclusive``         |
+--------------------------------------------+---------------------------+-------------------------+


Scheduling Policy
-----------------
Job Priority by Processor Count
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Jobs are *aged* according to the job's requested processor count (older
age equals higher queue priority). Each job's requested processor count
places it into a specific *bin*. Each bin has a different aging
parameter, which all jobs in the bin receive.

+-------+-------------+-------------+------------------------+----------------------+
| Bin   | Min Nodes   | Max Nodes   | Max Walltime (Hours)   | Aging Boost (Days)   |
+=======+=============+=============+========================+======================+
| 1     | 5,645       | 9,408       | 24.0                   | 15                   |
+-------+-------------+-------------+------------------------+----------------------+
| 2     | 1,882       | 5,644       | 24.0                   | 10                   |
+-------+-------------+-------------+------------------------+----------------------+
| 3     | 184         | 1,881       | 12.0                   | 0                    |
+-------+-------------+-------------+------------------------+----------------------+
| 4     | 92          | 183         | 6.0                    | 0                    |
+-------+-------------+-------------+------------------------+----------------------+
| 5     | 1           | 91          | 2.0                    | 0                    |
+-------+-------------+-------------+------------------------+----------------------+



Simplified Node Layout
----------------------

To easily visualize ``srun`` examples, the node diagram shown in section
REFERENCE has been simplified to the picture shown below. 

.. image:: /images/Frontier_Node_Diagram_Simple.png
   :align: center
   :width: 100%
   :alt: Simplified Frontier node architecture diagram

In the diagram, each **physical** core on Frontier is composed of two
**logical** cores that are represented by a pair of blue and grey boxes. For a
given physical core, the blue box represents the logical core of the first
hardware thread, where the grey box represents the logical core of the second
hardware thread.

Process and Thread Mapping
--------------------------

This section describes how to map processes (e.g., MPI ranks) and process
threads (e.g., OpenMP threads) to the CPUs and GPUs on Frontier.

.. note:: 

   Users are highly encouraged to use the CPU- and GPU-mapping programs
   used in the following sections to check their understanding of the job steps
   (i.e., srun commands) the intend to use in their actual jobs. They can be
   found HERELINK to jobstep and hello_mpi


CPU Mapping
^^^^^^^^^^^

This sub-section covers how to map tasks to the CPU without the presence of
additional threads (i.e., solely MPI tasks -- no additional OpenMP threads).

For the following examples, Slurm’s Interactive Jobs method was used to request
an allocation of 1 compute node: ``salloc -A <project_id> -t 30 -p <parition>
-N 1``. The intent with both of the following examples is to launch 8 MPI ranks
across the node where each rank is assigned its own logical core.  Using the
``-m`` distribution flag, we will cover two common approaches to assign the MPI
ranks -- in a "round-robin" (``cyclic``) configuration and in a "packed"
(``block``) configuration.

8 MPI Ranks (round-robin)
"""""""""""""""""""""""""

Assigning MPI ranks in a "round-robin" (``cyclic``) manner across L3 cache
regions (sockets) is the default behavior on Frontier. This mode will assign
consecutive MPI tasks to different sockets before it tries to "fill up" a
socket.

Recall that the ``-m`` flag behaves like: ``-m <node distribution>:<socket
distribution>``.  Hence, the key setting to achieving the round-robin nature is
the ``-m block:cyclic`` flag, specifically the ``cyclic`` setting provided for
the "socket distribution". This ensures that the MPI tasks will be distributed
across L3 cache regions (sockets) in a cyclic (round-robin) manner.

The below ``srun`` command will achieve the intended 8 MPI "round-robin" layout:

.. code-block:: bash

    $ export OMP_NUM_THREADS=1
    $ srun -N1 -n8 -c1 --cpu-bind=threads --threads-per-core=1 -m block:cyclic ./hello_mpi_omp | sort

    MPI 000 - OMP 000 - HWT 000 - Node crusher144
    MPI 001 - OMP 000 - HWT 008 - Node crusher144
    MPI 002 - OMP 000 - HWT 016 - Node crusher144
    MPI 003 - OMP 000 - HWT 024 - Node crusher144
    MPI 004 - OMP 000 - HWT 032 - Node crusher144
    MPI 005 - OMP 000 - HWT 040 - Node crusher144
    MPI 006 - OMP 000 - HWT 048 - Node crusher144
    MPI 007 - OMP 000 - HWT 056 - Node crusher144

.. note::

   Although the above command used the default settings ``-c1``,
   ``--cpu-bind=threads``, ``--threads-per-core=1`` and ``-m block:cyclic``, it is
   always better to be explicit with your ``srun`` command to have more control
   over your node layout. The above command is equivalent to ``srun -N1 -n8``.

See the node diagram below for a visual representation of the round-robin distribution:

.. image:: /images/Frontier_Node_Diagram_Simple_mpiRR.png
   :align: center
   :width: 100%

8 MPI Ranks (packed)
"""""""""""""""""""""""""

The below image is packed across threads (``block``)

.. image:: /images/Frontier_Node_Diagram_Simple_mpiPacked.png
   :align: center
   :width: 100%

More text

Multithreading
^^^^^^^^^^^^^^

Introducing Multithreading

GPU Mapping
^^^^^^^^^^^

Mapping to GPUs (both noOpenMP / with OpenMP)
