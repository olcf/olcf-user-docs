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

Each compute node on Frontier has [2x] 1.92TB \ **N**\ on-\ **V**\ olatile **Me**\mory (NVMe) storage devices (SSDs), colloquially known as a "Burst Buffer" with a peak sequential performance of 5500 MB/s (read) and 2000 MB/s (write). The purpose of the Burst Buffer system is to bring improved I/O performance to appropriate workloads. Users are not required to use the NVMes. Data can also be written directly to the parallel filesystem.

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


.. _frontier-running:

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


Simplified Node Layout
----------------------

To easily visualize job examples (see :ref:`frontier-mapping` further below), the
compute node diagram has been simplified to the picture shown below.

.. image:: /images/Frontier_Node_Diagram_Simple.png
   :align: center
   :width: 100%
   :alt: Simplified Frontier node architecture diagram

In the diagram, each **physical** core on a Frontier compute node is composed
of two **logical** cores that are represented by a pair of blue and grey boxes.
For a given physical core, the blue box represents the logical core of the
first hardware thread, where the grey box represents the logical core of the
second hardware thread.


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

.. _frontier-interactive:

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
| ``--threads-per-core`` | ``#SBATCH --threads-per-core=2``           | | Number of active hardware threads per core. Can be 1 or 2 (1 is default)           |
|                        |                                            | | **Must** be used if using ``--threads-per-core=2`` in your ``srun`` command.       |
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

Job Priority by Node Count
^^^^^^^^^^^^^^^^^^^^^^^^^^

Jobs are *aged* according to the job's requested node count (older
age equals higher queue priority). Each job's requested node count
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

The default job launcher for Frontier is `srun <https://slurm.schedmd.com/srun.html>`_ . The ``srun`` command is used to execute an MPI binary on one or more compute nodes in parallel.

Srun Format
^^^^^^^^^^^

::

      srun  [OPTIONS... [executable [args...]]] 

Single Command (non-interactive)

.. code-block:: bash

   $ srun -A <project_id> -t 00:05:00 -p <partition> -N 2 -n 4 --ntasks-per-node=2 ./a.out
   <output printed to terminal>

The job name and output options have been removed since stdout/stderr are typically desired in the terminal window in this usage mode.


``srun`` accepts the following common options:

+--------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+
| ``-N``                                                 | Number of nodes                                                                                                |
+--------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+
| ``-n``                                                 | Total number of MPI tasks (default is 1)                                                                       |
+--------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+
| ``-c, --cpus-per-task=<ncpus>``                        | | Logical cores per MPI task (default is 1)                                                                    |
|                                                        | | When used with ``--threads-per-core=1``: ``-c`` is equivalent to *physical* cores per task                   |
+--------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+
| ``--cpu-bind=threads``                                 | | Bind tasks to CPUs.                                                                                          |
|                                                        | | ``threads`` - (default, recommended) Automatically generate masks binding tasks to threads.                  |
+--------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+
| ``--threads-per-core=<threads>``                       | | In task layout, use the specified maximum number of hardware threads per core                                |
|                                                        | | (default is 1; there are 2 hardware threads per physical CPU core).                                          |
|                                                        | | Must also be set in ``salloc`` or ``sbatch`` if using ``--threads-per-core=2`` in your ``srun`` command.     |
+--------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+
| ``-m, --distribution=<value>:<value>:<value>``         | | Specifies the distribution of MPI ranks across compute nodes, sockets (L3 regions), and cores, respectively. |
|                                                        | | The default values are ``block:cyclic:cyclic``, see ``man srun`` for more information.                       |
|                                                        | | Currently, the distribution setting for cores (the third "<value>" entry) has no effect on Frontier          |
+--------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+
|  ``--ntasks-per-node=<ntasks>``                        | | If used without ``-n``: requests that a specific number of tasks be invoked on each node.                    |
|                                                        | | If used with ``-n``: treated as a *maximum* count of tasks per node.                                         |
+--------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+
| ``--gpus``                                             | Specify the number of GPUs required for the job (total GPUs across all nodes).                                 |
+--------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+
| ``--gpus-per-node``                                    | Specify the number of GPUs per node required for the job.                                                      |
+--------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+
| ``--gpu-bind=closest``                                 | Binds each task to the GPU which is on the same NUMA domain as the CPU core the MPI rank is running on.        |
+--------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+
| ``--gpu-bind=map_gpu:<list>``                          | Bind tasks to specific GPUs by setting GPU masks on tasks (or ranks) as specified where                        |
|                                                        | ``<list>`` is ``<gpu_id_for_task_0>,<gpu_id_for_task_1>,...``. If the number of tasks (or                      |
|                                                        | ranks) exceeds the number of elements in this list, elements in the list will be reused as                     |
|                                                        | needed starting from the beginning of the list. To simplify support for large task                             |
|                                                        | counts, the lists may follow a map with an asterisk and repetition count. (For example                         |
|                                                        | ``map_gpu:0*4,1*4``)                                                                                           |
+--------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+
| ``--ntasks-per-gpu=<ntasks>``                          | Request that there are ntasks tasks invoked for every GPU.                                                     |
+--------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+


Below is a comparison table between srun and jsrun.

+----------------------------------------------+---------------------------+-------------------------+
| Option                                       | jsrun (Summit)            | srun  (Frontier)        |
+==============================================+===========================+=========================+
| Number of nodes                              | ``-nnodes``               | ``-N, --nnodes``        |
+----------------------------------------------+---------------------------+-------------------------+
| Number of tasks                              | defined with resource set | ``-n, --ntasks``        |
+----------------------------------------------+---------------------------+-------------------------+
| Number of tasks per node                     | defined with resource set | ``--ntasks-per-node``   |
+----------------------------------------------+---------------------------+-------------------------+
| Number of CPUs per task                      | defined with resource set | ``-c, --cpus-per-task`` |
+----------------------------------------------+---------------------------+-------------------------+
| Number of resource sets                      | ``-n, --nrs``             | N/A                     |
+----------------------------------------------+---------------------------+-------------------------+
| Number of resource sets per host             | ``-r, --rs_per_host``     | N/A                     |
+----------------------------------------------+---------------------------+-------------------------+
| Number of tasks per resource set             | ``-a, --tasks_per_rs``    | N/A                     |
+----------------------------------------------+---------------------------+-------------------------+
| Number of CPUs per resource set              | ``-c, --cpus_per_rs``     | N/A                     |
+----------------------------------------------+---------------------------+-------------------------+
| Number of GPUs per resource set              | ``-g, --gpus_per_rs``     | N/A                     |
+----------------------------------------------+---------------------------+-------------------------+
| Bind tasks to allocated CPUs                 | ``-b, --bind``            | ``--cpu-bind``          |
+----------------------------------------------+---------------------------+-------------------------+
| Do not run more than one task on resources   | ``--tasks_per_rs 1``      | ``--exclusive``         |
+----------------------------------------------+---------------------------+-------------------------+
| Performance binding preference               | ``-l,--latency_priority`` | ``--hint``              |
+----------------------------------------------+---------------------------+-------------------------+
| Specify the task to resource mapping pattern | ``--launch_distribution`` | ``-m, --distribution``  |
+----------------------------------------------+---------------------------+-------------------------+


.. _frontier-mapping:


Process and Thread Mapping Examples
-----------------------------------

This section describes how to map processes (e.g., MPI ranks) and process
threads (e.g., OpenMP threads) to the CPUs and GPUs on Frontier.

Users are highly encouraged to use the CPU- and GPU-mapping programs used in
the following sections to check their understanding of the job steps (i.e.,
srun commands) they intend to use in their actual jobs.

* For the :ref:`frontier-cpu-map` and :ref:`frontier-multi-map` sections:

  A simple MPI+OpenMP "Hello, World" program (`hello_mpi_omp
  <https://code.ornl.gov/olcf/hello_mpi_omp>`__) will be used to clarify the
  mappings.

* For the :ref:`frontier-gpu-map` section:

  An MPI+OpenMP+HIP "Hello, World" program (`hello_jobstep
  <https://code.ornl.gov/olcf/hello_jobstep>`__) will be used to clarify the GPU
  mappings.


.. _frontier-cpu-map:

CPU Mapping
^^^^^^^^^^^

This subsection covers how to map tasks to the CPU without the presence of
additional threads (i.e., solely MPI tasks -- no additional OpenMP threads).

The intent with both of the following examples is to launch 8 MPI ranks across
the node where each rank is assigned its own logical (and, in this case,
physical) core.  Using the ``-m`` distribution flag, we will cover two common
approaches to assign the MPI ranks -- in a "round-robin" (``cyclic``)
configuration and in a "packed" (``block``) configuration. Slurm's
:ref:`frontier-interactive` method was used to request an allocation of 1
compute node for these examples: ``salloc -A <project_id> -t 30 -p <parition>
-N 1``

.. note::

   There are many different ways users might choose to perform these mappings,
   so users are encouraged to clone the ``hello_mpi_omp`` program and test whether
   or not processes and threads are running where intended.

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
across sockets in a cyclic (round-robin) manner.

The below ``srun`` command will achieve the intended 8 MPI "round-robin" layout:

.. code-block:: bash

    $ export OMP_NUM_THREADS=1
    $ srun -N1 -n8 -c1 --cpu-bind=threads --threads-per-core=1 -m block:cyclic ./hello_mpi_omp | sort

    MPI 000 - OMP 000 - HWT 000 - Node frontier144
    MPI 001 - OMP 000 - HWT 008 - Node frontier144
    MPI 002 - OMP 000 - HWT 016 - Node frontier144
    MPI 003 - OMP 000 - HWT 024 - Node frontier144
    MPI 004 - OMP 000 - HWT 032 - Node frontier144
    MPI 005 - OMP 000 - HWT 040 - Node frontier144
    MPI 006 - OMP 000 - HWT 048 - Node frontier144
    MPI 007 - OMP 000 - HWT 056 - Node frontier144

.. image:: /images/Frontier_Node_Diagram_Simple_mpiRR.png
   :align: center
   :width: 100%

Breaking down the ``srun`` command, we have:

* ``-N1``: indicates we are using 1 node
* ``-n8``: indicates we are launching 8 MPI tasks
* ``-c1``: indicates we are assigning 1 logical core per MPI task.
  In this case, because of ``--threads-per-core=1``, this also means 1 **physical** core per MPI task.
* ``--cpu-bind=threads``: binds tasks to threads
* ``--threads-per-core=1``: use a maximum of 1 hardware thread per physical core (i.e., only use 1 logical core per physical core)
* ``-m block:cyclic``: distribute the tasks in a block layout across nodes (default), and in a **cyclic** (round-robin) layout across L3 sockets
* ``./hello_mpi_omp``: launches the "hello_mpi_omp" executable
* ``| sort``: sorts the output

.. note::

   Although the above command used the default settings ``-c1``,
   ``--cpu-bind=threads``, ``--threads-per-core=1`` and ``-m block:cyclic``, it is
   always better to be explicit with your ``srun`` command to have more control
   over your node layout. The above command is equivalent to ``srun -N1 -n8``.

As you can see in the node diagram above, this results in the 8 MPI tasks
(outlined in different colors) being distributed "vertically" across L3
sockets.

8 MPI Ranks (packed)
""""""""""""""""""""

Instead, you can assign MPI ranks so that the L3 regions are filled in a
"packed" (``block``) manner.  This mode will assign consecutive MPI tasks to
the same L3 region (socket) until it is "filled up" or "packed" before
assigning a task to a different socket.

Recall that the ``-m`` flag behaves like: ``-m <node distribution>:<socket
distribution>``.  Hence, the key setting to achieving the round-robin nature is
the ``-m block:block`` flag, specifically the ``block`` setting provided for
the "socket distribution". This ensures that the MPI tasks will be distributed
in a packed manner.

The below ``srun`` command will achieve the intended 8 MPI "packed" layout:

.. code-block:: bash

    $ export OMP_NUM_THREADS=1
    $ srun -N1 -n8 -c1 --cpu-bind=threads --threads-per-core=1 -m block:block ./hello_mpi_omp | sort

    MPI 000 - OMP 000 - HWT 000 - Node frontier144
    MPI 001 - OMP 000 - HWT 001 - Node frontier144
    MPI 002 - OMP 000 - HWT 002 - Node frontier144
    MPI 003 - OMP 000 - HWT 003 - Node frontier144
    MPI 004 - OMP 000 - HWT 004 - Node frontier144
    MPI 005 - OMP 000 - HWT 005 - Node frontier144
    MPI 006 - OMP 000 - HWT 006 - Node frontier144
    MPI 007 - OMP 000 - HWT 007 - Node frontier144

.. image:: /images/Frontier_Node_Diagram_Simple_mpiPacked.png
   :align: center
   :width: 100%

Breaking down the ``srun`` command, the only difference than the previous example is:

* ``-m block:block``: distribute the tasks in a block layout across nodes (default), and in a **block** (packed) socket layout

As you can see in the node diagram above, this results in the 8 MPI tasks
(outlined in different colors) being distributed "horizontally" *within* a
socket, rather than being spread across different L3 sockets like with the
previous example.

.. _frontier-multi-map:

Multithreading
^^^^^^^^^^^^^^

Because a Frontier compute node has two hardware threads available (2 logical
cores per physical core), this enables the possibility of multithreading your
application (e.g., with OpenMP threads). Although the additional hardware
threads can be assigned to additional MPI tasks, this is not recommended. It is
highly recommended to only use 1 MPI task per physical core and to use OpenMP
threads instead on any additional logical cores gained when using both hardware
threads.

The following examples cover multithreading with hybrid MPI+OpenMP
applications.  In these examples, Slurm's :ref:`frontier-interactive` method
was used to request an allocation of 1 compute node:
``salloc -A <project_id> -t 30 -p <parition> -N 1``

.. note::

   There are many different ways users might choose to perform these mappings,
   so users are encouraged to clone the ``hello_mpi_omp`` program and test whether
   or not processes and threads are running where intended.

2 MPI ranks - each with 2 OpenMP threads
""""""""""""""""""""""""""""""""""""""""

In this example, the intent is to launch 2 MPI ranks, each of which spawn 2
OpenMP threads, and have all of the 4 OpenMP threads run on different physical
CPU cores.

**First (INCORRECT) attempt**

To set the number of OpenMP threads spawned per MPI rank, the
``OMP_NUM_THREADS`` environment variable can be used. To set the number of MPI
ranks launched, the ``srun`` flag ``-n`` can be used.

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

    MPI 000 - OMP 000 - HWT 000 - Node frontier001
    MPI 000 - OMP 001 - HWT 000 - Node frontier001
    MPI 001 - OMP 000 - HWT 008 - Node frontier001
    MPI 001 - OMP 001 - HWT 008 - Node frontier001

The first thing to notice here is the ``WARNING`` about oversubscribing the
available CPU cores. Also, the output shows each MPI rank did spawn 2 OpenMP
threads, but both OpenMP threads ran on the same logical core (for a given
MPI rank). This was not the intended behavior; each OpenMP thread was meant to
run on its own physical CPU core.

The problem here arises from two default settings; 1) each MPI rank is only
allocated 1 logical core (``-c 1``) and, 2) only 1 hardware thread per physical
CPU core is enabled (``--threads-per-core=1``).  When using
``--threads-per-core=1`` and ``--cpu-bind=threads`` (the default setting), 1
logical core in ``-c`` is equivalent to 1 physical core.  So in this case, each
MPI rank only has 1 physical core (with 1 hardware thread) to run on -
including any threads the process spawns - hence the WARNING and undesired
behavior.

**Second (CORRECT) attempt**

Recall that in this scenario, because of the ``--threads-per-core=1`` setting,
1 logical core is equivalent to 1 physical core when using ``-c``.  Therefore,
in order for each OpenMP thread to run on its own physical CPU core, each MPI
rank should be given 2 physical CPU cores (``-c 2``).  Now the OpenMP threads
will be mapped to unique hardware threads on separate physical CPU cores.

.. code-block:: bash

    $ export OMP_NUM_THREADS=2
    $ srun -N1 -n2 -c2 ./hello_mpi_omp | sort

    MPI 000 - OMP 000 - HWT 000 - Node frontier001
    MPI 000 - OMP 001 - HWT 001 - Node frontier001
    MPI 001 - OMP 000 - HWT 008 - Node frontier001
    MPI 001 - OMP 001 - HWT 009 - Node frontier001

Now the output shows that each OpenMP thread ran on its own physical CPU core.
More specifically (see the Frontier Compute Node diagram), OpenMP thread 000 of
MPI rank 000 ran on logical core 000 (i.e., physical CPU core 00), OpenMP
thread 001 of MPI rank 000 ran on logical core 001 (i.e., physical CPU core
01), OpenMP thread 000 of MPI rank 001 ran on logical core 008 (i.e., physical
CPU core 08), and OpenMP thread 001 of MPI rank 001 ran on logical core 009
(i.e., physical CPU core 09) - as intended.

**Third attempt - Using multiple threads per core**

To use both available hardware threads per core, the *job* must be allocated
with ``--threads-per-core=2`` (as opposed to only the job step - i.e., ``srun``
command). That value will then be inherited by ``srun`` unless explcitly
overridden with ``--threads-per-core=1``. Because we are using
``--threads-per-core=2``, the usage of ``-c`` goes back to purely meaning the
amount of **logical** cores (i.e., it is no longer equivalent to 1 physical core).

.. code-block:: bash

    $ salloc -N1 -A <project_id> -t <time> -p <partition> --threads-per-core=2

    $ export OMP_NUM_THREADS=2
    $ srun -N1 -n2 -c2 ./hello_mpi_omp | sort

    MPI 000 - OMP 000 - HWT 000 - Node frontier001
    MPI 000 - OMP 001 - HWT 064 - Node frontier001
    MPI 001 - OMP 000 - HWT 008 - Node frontier001
    MPI 001 - OMP 001 - HWT 072 - Node frontier001

Comparing this output to the Frontier Compute Node diagram, we see that each
pair of OpenMP threads is contained within a single physical core. MPI rank 000
ran on logical cores 000 and 064 (i.e. physical CPU core 00) and MPI rank
001 ran on logical cores 008 and 072 (i.e. physical CPU core 08).

.. _frontier-gpu-map:

GPU Mapping
^^^^^^^^^^^

In this sub-section, an MPI+OpenMP+HIP "Hello, World" program (`hello_jobstep
<https://code.ornl.gov/olcf/hello_jobstep>`__) will be used to clarify the GPU
mappings. Again, Slurm's :ref:`frontier-interactive` method was used to request an
allocation of 2 compute nodes for these examples: ``salloc -A <project_id> -t
30 -p <parition> -N 2``. The CPU mapping part of this example is very similar
to the example used above in the Multithreading sub-section, so the focus here
will be on the GPU mapping part.

In general, GPU mapping can be accomplished in different ways. For example, an
application might map MPI ranks to GPUs programmatically within the code using,
say, ``hipSetDevice``. In this case, since all GPUs on a node are available to
all MPI ranks on that node by default, there might not be a need to map to GPUs
using Slurm (just do it in the code). However, in another application, there
might be a reason to make only a subset of GPUs available to the MPI ranks on a
node. It is this latter case that the following examples refer to.

.. note::

   There are many different ways users might choose to perform these mappings,
   so users are encouraged to clone the ``hello_jobstep`` program and test whether
   or not processes and threads are running where intended.

.. warning::

   Due to the unique architecture of Frontier compute nodes and the way that
   Slurm currently allocates GPUs and CPU cores to job steps, it is suggested that
   all 8 GPUs on a node are allocated to the job step to ensure that optimal
   bindings are possible.

Mapping 1 task per GPU
""""""""""""""""""""""

In the following examples, each MPI rank (and its OpenMP threads) will be
mapped to a single GPU.

**Example 0: 1 MPI rank with 1 OpenMP thread and 1 GPU (single-node)**

Somewhat counterintuitively, this common test case is currently among the most
difficult. Slurm ignores GPU bindings for nodes with only a single task, so we
do not use ``--gpu-bind`` here. We must allocate only a single GPU to ensure
that only one GPU is available to the task, and since we get the first GPU
available we should bind the task to the CPU closest to the allocated GPU. 

.. code-block:: bash

    $ export OMP_NUM_THREADS=1
    $ srun -N1 -n1 -c1 --cpu-bind=map_cpu:48 --gpus=1 ./hello_jobstep

    MPI 000 - OMP 000 - HWT 048 - Node frontier001 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1

**Example 1: 8 MPI ranks - each with 2 OpenMP threads and 1 GPU (single-node)**

This example launches 8 MPI ranks (``-n8``), each with 2 physical CPU cores
(``-c2``) to launch 2 OpenMP threads (``OMP_NUM_THREADS=2``) on. In addition,
each MPI rank (and its 2 OpenMP threads) should have access to only 1 GPU. To
accomplish the GPU mapping, two new ``srun`` options will be used:

* ``--gpus-per-node`` specifies the number of GPUs required for the job
* ``--gpu-bind=closest`` binds each task to the GPU which is closest.

.. note::
    Without these additional flags, all MPI ranks would have access to all GPUs (which is the default behavior).

.. code-block:: bash

    $ export OMP_NUM_THREADS=2
    $ srun -N1 -n8 -c2 --gpus-per-node=8 --gpu-bind=closest ./hello_jobstep | sort

    MPI 000 - OMP 000 - HWT 000 - Node frontier001 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 000 - OMP 001 - HWT 001 - Node frontier001 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 001 - OMP 000 - HWT 008 - Node frontier001 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 001 - OMP 001 - HWT 009 - Node frontier001 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 002 - OMP 000 - HWT 016 - Node frontier001 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 002 - OMP 001 - HWT 017 - Node frontier001 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 003 - OMP 000 - HWT 024 - Node frontier001 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 003 - OMP 001 - HWT 025 - Node frontier001 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 004 - OMP 000 - HWT 032 - Node frontier001 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 004 - OMP 001 - HWT 033 - Node frontier001 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 005 - OMP 000 - HWT 040 - Node frontier001 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 005 - OMP 001 - HWT 041 - Node frontier001 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 006 - OMP 000 - HWT 048 - Node frontier001 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 006 - OMP 001 - HWT 049 - Node frontier001 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 007 - OMP 000 - HWT 056 - Node frontier001 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6
    MPI 007 - OMP 001 - HWT 057 - Node frontier001 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6

The output from the program contains a lot of information, so let's unpack it.
First, there are different IDs associated with the GPUs so it is important to
describe them before moving on. ``GPU_ID`` is the node-level (or global) GPU
ID, which is labeled as one might expect from looking at the Frontier Node
Diagram: 0, 1, 2, 3, 4, 5, 6, 7. ``RT_GPU_ID`` is the HIP runtime GPU ID, which
can be though of as each MPI rank's local GPU ID number (with zero-based
indexing). So in the output above, each MPI rank has access to only 1 unique
GPU - where MPI 000 has access to "global" GPU 4, MPI 001 has access to
"global" GPU 5, etc., but all MPI ranks show a HIP runtime GPU ID of 0. The
reason is that each MPI rank only "sees" one GPU and so the HIP runtime labels
it as "0", even though it might be global GPU ID 0, 1, 2, 3, 4, 5, 6, or 7. The
GPU's bus ID is included to definitively show that different GPUs are being
used.

Here is a summary of the different GPU IDs reported by the example program:

* ``GPU_ID`` is the node-level (or global) GPU ID read from
  ``ROCR_VISIBLE_DEVICES``. If this environment variable is not set (either by
  the user or by Slurm), the value of ``GPU_ID`` will be set to ``N/A`` by this
  program.

* ``RT_GPU_ID`` is the HIP runtime GPU ID (as reported from, say ``hipGetDevice``).

* ``Bus_ID`` is the physical bus ID associated with the GPUs. Comparing the bus
  IDs is meant to definitively show that different GPUs are being used.

So the job step (i.e., ``srun`` command) used above gave the desired output.
Each MPI rank spawned 2 OpenMP threads and had access to a unique GPU. The
``--gpus-per-node=8`` allocated 8 GPUs for node and the ``--gpu-bind=closest``
ensured that the closest GPU to each rank was the one used.

.. note::

   This example shows an important peculiarity of the Frontier nodes; the
   "closest" GPUs to each MPI rank are not in sequential order. For example, MPI
   rank 000 and its two OpenMP threads ran on hardware threads 000 and 001. As can
   be seen in the Frontier node diagram, these two hardware threads reside in the
   same L3 cache region, and that L3 region is connected via Infinity Fabric (blue
   line in the diagram) to GPU 4. This is an important distinction that can affect
   performance if not considered carefully. 

**Example 2: 16 MPI ranks - each with 2 OpenMP threads and 1 GPU (multi-node)**

This example will extend Example 1 to run on 2 nodes. As the output shows, it
is a very straightforward exercise of changing the number of nodes to 2
(``-N2``) and the number of MPI ranks to 16 (``-n16``).

.. code-block:: bash

    $ export OMP_NUM_THREADS=2
    $ srun -N2 -n16 -c2 --gpus-per-node=8 --gpu-bind=closest ./hello_jobstep | sort

    MPI 000 - OMP 000 - HWT 000 - Node frontier001 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 000 - OMP 001 - HWT 001 - Node frontier001 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 001 - OMP 000 - HWT 008 - Node frontier001 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 001 - OMP 001 - HWT 009 - Node frontier001 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 002 - OMP 000 - HWT 016 - Node frontier001 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 002 - OMP 001 - HWT 017 - Node frontier001 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 003 - OMP 000 - HWT 024 - Node frontier001 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 003 - OMP 001 - HWT 025 - Node frontier001 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 004 - OMP 000 - HWT 032 - Node frontier001 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 004 - OMP 001 - HWT 033 - Node frontier001 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 005 - OMP 000 - HWT 040 - Node frontier001 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 005 - OMP 001 - HWT 041 - Node frontier001 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 006 - OMP 000 - HWT 048 - Node frontier001 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 006 - OMP 001 - HWT 049 - Node frontier001 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 007 - OMP 000 - HWT 056 - Node frontier001 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6
    MPI 007 - OMP 001 - HWT 057 - Node frontier001 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6
    MPI 008 - OMP 000 - HWT 000 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 008 - OMP 001 - HWT 001 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 009 - OMP 000 - HWT 008 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 009 - OMP 001 - HWT 009 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 010 - OMP 000 - HWT 016 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 010 - OMP 001 - HWT 017 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 011 - OMP 000 - HWT 024 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 011 - OMP 001 - HWT 025 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 012 - OMP 000 - HWT 032 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 012 - OMP 001 - HWT 033 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 013 - OMP 000 - HWT 040 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 013 - OMP 001 - HWT 041 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 014 - OMP 000 - HWT 048 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 014 - OMP 001 - HWT 049 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 015 - OMP 000 - HWT 056 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6
    MPI 015 - OMP 001 - HWT 057 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6

**Example 3: 8 MPI ranks - each with 2 OpenMP threads and 1 *specific* GPU (single-node)**

This example will be very similar to Example 1, but instead of using
``--gpu-bind=closest`` to map each MPI rank to the closest GPU,
``--gpu-bind=map_gpu`` will be used to map each MPI rank to a *specific* GPU.
The ``map_gpu`` option takes a comma-separated list of GPU IDs to specify how
the MPI ranks are mapped to GPUs, where the form of the comma-separated list is
``<gpu_id_for_task_0>, <gpu_id_for_task_1>,...``.

.. code:: bash

    $ export OMP_NUM_THREADS=2
    $ srun -N1 -n8 -c2 --gpus-per-node=8 --gpu-bind=map_gpu:4,5,2,3,6,7,0,1 ./hello_jobstep | sort

    MPI 000 - OMP 000 - HWT 000 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 000 - OMP 001 - HWT 001 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 001 - OMP 000 - HWT 008 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 001 - OMP 001 - HWT 009 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 002 - OMP 000 - HWT 016 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 002 - OMP 001 - HWT 017 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 003 - OMP 000 - HWT 024 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 003 - OMP 001 - HWT 025 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 004 - OMP 000 - HWT 032 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 004 - OMP 001 - HWT 033 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 005 - OMP 000 - HWT 040 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 005 - OMP 001 - HWT 041 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 006 - OMP 000 - HWT 048 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 006 - OMP 001 - HWT 049 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 007 - OMP 000 - HWT 056 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6
    MPI 007 - OMP 001 - HWT 057 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6

Here, the output is the same as the results from Example 1. This is because the
8 GPU IDs in the comma-separated list happen to specify the GPUs within the
same L3 cache region that the MPI ranks are in. So MPI 000 is mapped to GPU 4,
MPI 001 is mapped to GPU 5, etc.

While this level of control over mapping MPI ranks to GPUs might be useful for
some applications, it is always important to consider the implication of the
mapping. For example, if the order of the GPU IDs in the ``map_gpu`` option is
reversed, the MPI ranks and the GPUs they are mapped to would be in different
L3 cache regions, which could potentially lead to poorer performance.

**Example 4: 16 MPI ranks - each with 2 OpenMP threads and 1 *specific* GPU (multi-node)**

Extending Examples 2 and 3 to run on 2 nodes is also a straightforward exercise
by changing the number of nodes to 2 (``-N2``) and the number of MPI ranks to
16 (``-n16``).

.. code:: bash

    $ export OMP_NUM_THREADS=2
    $ srun -N2 -n16 -c2 --gpus-per-node=8 --gpu-bind=map_gpu:4,5,2,3,6,7,0,1 ./hello_jobstep | sort
    
    MPI 000 - OMP 000 - HWT 000 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 000 - OMP 001 - HWT 001 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 001 - OMP 000 - HWT 008 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 001 - OMP 001 - HWT 009 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 002 - OMP 000 - HWT 016 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 002 - OMP 001 - HWT 017 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 003 - OMP 000 - HWT 024 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 003 - OMP 001 - HWT 025 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 004 - OMP 000 - HWT 032 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 004 - OMP 001 - HWT 033 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 005 - OMP 000 - HWT 040 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 005 - OMP 001 - HWT 041 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 006 - OMP 000 - HWT 048 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 006 - OMP 001 - HWT 049 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 007 - OMP 000 - HWT 056 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6
    MPI 007 - OMP 001 - HWT 057 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6
    MPI 008 - OMP 000 - HWT 000 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 008 - OMP 001 - HWT 001 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 009 - OMP 000 - HWT 008 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 009 - OMP 001 - HWT 009 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 010 - OMP 000 - HWT 016 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 010 - OMP 001 - HWT 017 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 011 - OMP 000 - HWT 024 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 011 - OMP 001 - HWT 025 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 012 - OMP 000 - HWT 032 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 012 - OMP 001 - HWT 033 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 013 - OMP 000 - HWT 040 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 013 - OMP 001 - HWT 041 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 014 - OMP 000 - HWT 048 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 014 - OMP 001 - HWT 049 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 015 - OMP 000 - HWT 056 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6
    MPI 015 - OMP 001 - HWT 057 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6

Mapping multiple MPI ranks to a single GPU
""""""""""""""""""""""""""""""""""""""""""

In the following examples, 2 MPI ranks will be mapped to 1 GPU. For the sake of
brevity, ``OMP_NUM_THREADS`` will be set to ``1``, so ``-c1`` will be used
unless otherwise specified.

.. note::

   On AMD's MI250X, multi-process service (MPS) is not needed since multiple
   MPI ranks per GPU is supported natively.

**Example 5: 16 MPI ranks - where 2 ranks share a GPU (round-robin, single-node)**

This example launches 16 MPI ranks (``-n16``), each with 1 physical CPU core
(``-c1``) to launch 1 OpenMP thread (``OMP_NUM_THREADS=1``) on. The MPI ranks
will be assigned to GPUs in a round-robin fashion so that each of the 8 GPUs on
the node are shared by 2 MPI ranks. To accomplish this GPU mapping, a new
``srun`` options will be used:

* ``--ntasks-per-gpu`` specifies the number of MPI ranks that will share access to a GPU.

.. code:: bash

    $ export OMP_NUM_THREADS=1
    $ srun -N1 -n16 -c1 --ntasks-per-gpu=2 --gpu-bind=closest ./hello_jobstep | sort

    MPI 000 - OMP 000 - HWT 000 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 001 - OMP 000 - HWT 008 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 002 - OMP 000 - HWT 016 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 003 - OMP 000 - HWT 024 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 004 - OMP 000 - HWT 032 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 005 - OMP 000 - HWT 040 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 006 - OMP 000 - HWT 048 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 007 - OMP 000 - HWT 056 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6
    MPI 008 - OMP 000 - HWT 001 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 009 - OMP 000 - HWT 009 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 010 - OMP 000 - HWT 017 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 011 - OMP 000 - HWT 025 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 012 - OMP 000 - HWT 033 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 013 - OMP 000 - HWT 041 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 014 - OMP 000 - HWT 049 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 015 - OMP 000 - HWT 057 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6


The output shows the round-robin (``cyclic``) distribution of MPI ranks to
GPUs. In fact, it is a round-robin distribution of MPI ranks *to L3 cache
regions* (the default distribution). The GPU mapping is a consequence of where
the MPI ranks are distributed; ``--gpu-bind=closest`` simply maps the GPU in an
L3 cache region to the MPI ranks in the same L3 region.

**Example 6: 32 MPI ranks - where 2 ranks share a GPU (round-robin, multi-node)**

This example is an extension of Example 5 to run on 2 nodes.

.. code:: bash

    $ export OMP_NUM_THREADS=1
    $ srun -N2 -n32 -c1 --ntasks-per-gpu=2 --gpu-bind=closest ./hello_jobstep | sort

    MPI 000 - OMP 000 - HWT 000 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 001 - OMP 000 - HWT 008 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 002 - OMP 000 - HWT 016 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 003 - OMP 000 - HWT 024 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 004 - OMP 000 - HWT 032 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 005 - OMP 000 - HWT 040 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 006 - OMP 000 - HWT 048 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 007 - OMP 000 - HWT 056 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6
    MPI 008 - OMP 000 - HWT 004 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 009 - OMP 000 - HWT 012 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 010 - OMP 000 - HWT 020 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 011 - OMP 000 - HWT 028 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 012 - OMP 000 - HWT 036 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 013 - OMP 000 - HWT 044 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 014 - OMP 000 - HWT 052 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 015 - OMP 000 - HWT 060 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6
    MPI 016 - OMP 000 - HWT 000 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 017 - OMP 000 - HWT 008 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 018 - OMP 000 - HWT 016 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 019 - OMP 000 - HWT 024 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 020 - OMP 000 - HWT 034 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 021 - OMP 000 - HWT 041 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 022 - OMP 000 - HWT 048 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 023 - OMP 000 - HWT 056 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6
    MPI 024 - OMP 000 - HWT 006 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 025 - OMP 000 - HWT 012 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 026 - OMP 000 - HWT 021 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 027 - OMP 000 - HWT 028 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 028 - OMP 000 - HWT 036 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 029 - OMP 000 - HWT 044 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 030 - OMP 000 - HWT 052 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 031 - OMP 000 - HWT 060 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6


**Example 7: 16 MPI ranks - where 2 ranks share a GPU (packed, single-node)**

This example launches 16 MPI ranks (``-n16``), each with 4 physical CPU cores
(``-c4``) to launch 1 OpenMP thread (``OMP_NUM_THREADS=1``) on. The MPI ranks
will be assigned to GPUs in a packed fashion so that each of the 8 GPUs on the
node are shared by 2 MPI ranks. Similar to Example 5, ``-ntasks-per-gpu=2``
will be used, but a new ``srun`` flag will be used to change the default
round-robin (``cyclic``) distribution of MPI ranks across NUMA domains:

* ``--distribution=<value>[:<value>][:<value>]`` specifies the distribution of
  MPI ranks across compute nodes, sockets (L3 cache regions on Frontier), and
  cores, respectively. The default values are ``block:cyclic:cyclic``, which is
  where the ``cyclic`` assignment comes from in the previous examples.

.. note::

   In the job step for this example, ``--distribution=*:block`` is used, where
   ``*`` represents the default value of ``block`` for the distribution of MPI
   ranks across compute nodes and the distribution of MPI ranks across L3 cache
   regions has been changed to ``block`` from its default value of ``cyclic``.

.. note::

   Because the distribution across L3 cache regions has been changed to a
   "packed" (``block``) configuration, caution must be taken to ensure MPI ranks
   end up in the L3 cache regions where the GPUs they intend to be mapped to are
   located. To accomplish this, the number of physical CPU cores assigned to an
   MPI rank was increased - in this case to 4. Doing so ensures that only 2 MPI
   ranks can fit into a single L3 cache region. If the value of ``-c`` was left at
   ``1``, all 8 MPI ranks would be "packed" into the first L3 region, where the
   "closest" GPU would be GPU 4 - the only GPU in that L3 region.

   Notice that this is not a workaround like in Example 6, but a requirement
   due to the ``block`` distribution of MPI ranks across NUMA domains.

.. code:: bash

    $ export OMP_NUM_THREADS=1
    $ srun -N1 -n16 -c4 --ntasks-per-gpu=2 --gpu-bind=closest --distribution=*:block ./hello_jobstep | sort
    
    MPI 000 - OMP 000 - HWT 000 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 001 - OMP 000 - HWT 004 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 002 - OMP 000 - HWT 008 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 003 - OMP 000 - HWT 012 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 004 - OMP 000 - HWT 016 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 005 - OMP 000 - HWT 020 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 006 - OMP 000 - HWT 024 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 007 - OMP 000 - HWT 028 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 008 - OMP 000 - HWT 032 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 009 - OMP 000 - HWT 036 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 010 - OMP 000 - HWT 040 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 011 - OMP 000 - HWT 044 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 012 - OMP 000 - HWT 048 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 013 - OMP 000 - HWT 052 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 014 - OMP 000 - HWT 056 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6
    MPI 015 - OMP 000 - HWT 060 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6

The overall effect of using ``--distribution=*:block`` and increasing the
number of physical CPU cores available to each MPI rank is to place the first
two MPI ranks in the first L3 cache region with GPU 4, the next two MPI ranks
in the second L3 cache region with GPU 5, and so on.

**Example 8: 32 MPI ranks - where 2 ranks share a GPU (packed, multi-node)**

This example is an extension of Example 7 to use 2 compute nodes. With the
appropriate changes put in place in Example 7, it is a straightforward exercise
to change to using 2 nodes (``-N2``) and 32 MPI ranks (``-n32``).

.. code:: bash

    $ export OMP_NUM_THREADS=1
    $ srun -N2 -n32 -c4 --ntasks-per-gpu=2 --gpu-bind=closest --distribution=*:block ./hello_jobstep | sort
    
    MPI 000 - OMP 000 - HWT 000 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 001 - OMP 000 - HWT 004 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 002 - OMP 000 - HWT 010 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 003 - OMP 000 - HWT 012 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 004 - OMP 000 - HWT 016 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 005 - OMP 000 - HWT 021 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 006 - OMP 000 - HWT 024 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 007 - OMP 000 - HWT 028 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 008 - OMP 000 - HWT 032 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 009 - OMP 000 - HWT 037 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 010 - OMP 000 - HWT 041 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 011 - OMP 000 - HWT 044 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 012 - OMP 000 - HWT 049 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 013 - OMP 000 - HWT 052 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 014 - OMP 000 - HWT 056 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6
    MPI 015 - OMP 000 - HWT 060 - Node frontier002 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6
    MPI 016 - OMP 000 - HWT 000 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 017 - OMP 000 - HWT 004 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 4 - Bus_ID d1
    MPI 018 - OMP 000 - HWT 008 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 019 - OMP 000 - HWT 013 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 5 - Bus_ID d6
    MPI 020 - OMP 000 - HWT 016 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 021 - OMP 000 - HWT 020 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID c9
    MPI 022 - OMP 000 - HWT 024 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 023 - OMP 000 - HWT 028 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID ce
    MPI 024 - OMP 000 - HWT 034 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 025 - OMP 000 - HWT 036 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 6 - Bus_ID d9
    MPI 026 - OMP 000 - HWT 040 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 027 - OMP 000 - HWT 044 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 7 - Bus_ID de
    MPI 028 - OMP 000 - HWT 048 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 029 - OMP 000 - HWT 052 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c1
    MPI 030 - OMP 000 - HWT 056 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6
    MPI 031 - OMP 000 - HWT 060 - Node frontier004 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID c6


**Example 9: 4 independent and simultaneous job steps in a single allocation**

This example shows how to run multiple job steps simultaneously in a single
allocation. The example below demonstrates running 4 independent, single rank
MPI executions on a single node, however the example could be extrapolated to
more complex invocations using the above examples.

Submission script:

.. code:: bash

    #!/bin/bash
    #SBATCH -A <projid>
    #SBATCH -N 1
    #SBATCH -t 10

    srun -N1 -c1 --gpus-per-task=1 --exact ./hello_jobstep &
    srun -N1 -c1 --gpus-per-task=1 --exact ./hello_jobstep &
    srun -N1 -c1 --gpus-per-task=1 --exact ./hello_jobstep &
    srun -N1 -c1 --gpus-per-task=1 --exact ./hello_jobstep &
    wait


Output:

.. code:: bash

   MPI 000 - OMP 000 - HWT 003 - Node frontier25 - RT_GPU_ID 0 - GPU_ID 3 - Bus_ID 09
   MPI 000 - OMP 000 - HWT 001 - Node frontier25 - RT_GPU_ID 0 - GPU_ID 1 - Bus_ID 87
   MPI 000 - OMP 000 - HWT 002 - Node frontier25 - RT_GPU_ID 0 - GPU_ID 2 - Bus_ID 48
   MPI 000 - OMP 000 - HWT 000 - Node frontier25 - RT_GPU_ID 0 - GPU_ID 0 - Bus_ID c9

.. note::

   The ``--exact`` parameter is important to avoid the error message ``srun:
   Job <job id> step creation temporarily disabled, retrying (Requested nodes are
   busy)``. The ``wait`` command is also critical, or your job script and
   allocation will immediately end after launching your jobs in the background.

.. note::

   This may result in a sub-optimal alignment of CPU and GPU on the node, as
   shown in the example output. Unfortunately, at the moment there is not a
   workaround for this, however improvements are possible in future SLURM updates.



Multiple GPUs per MPI rank
""""""""""""""""""""""""""

As mentioned previously, all GPUs are accessible by all MPI ranks by default,
so it is possible to *programatically* map any combination of GPUs to MPI
ranks. It should be noted however that Cray MPICH does not support GPU-aware
MPI for multiple GPUs per rank, so this binding is not suggested.


Software
============

Visualization and analysis tasks should be done on the Andes cluster. There are a few tools provided for various visualization tasks, as described in the :ref:`visualization-tools` section of the :ref:`andes-user-guide`.

For a full list of software available at the OLCF, please see the Software section (coming soon).

Debugging
============

Debugging text goes here

Optimization and Profiling
==========================

Getting started
---------------

``rocprof`` gathers metrics on kernels run on AMD GPU architectures. The profiler works for HIP kernels, as well as offloaded kernels from OpenMP target offloading, OpenCL, and abstraction layers such as Kokkos.
For a simple view of kernels being run, ``rocprof --stats --timestamp on`` is a great place to start.
With the ``--stats`` option enabled, ``rocprof`` will generate a file that is named ``results.stats.csv`` by default, but named ``<output>.stats.csv`` if the ``-o`` flag is supplied.
This file will list all kernels being run, the number of times they are run, the total duration and the average duration (in nanoseconds) of the kernel, and the GPU usage percentage.
More detailed infromation on ``rocprof`` profiling modes can be found at `ROCm Profiler <https://rocmdocs.amd.com/en/latest/ROCm_Tools/ROCm-Tools.html>`__ documentation.


Roofline profiling
------------------
The `Roofline <https://docs.nersc.gov/tools/performance/roofline/>`__ performance model is an increasingly popular way to demonstrate and understand application performance.
This section documents how to construct a simple roofline model for a single kernel using ``rocprof``.
This roofline model is designed to be comparable to rooflines constructed by NVIDIA's `NSight Compute <https://developer.nvidia.com/blog/accelerating-hpc-applications-with-nsight-compute-roofline-analysis/>`__.
A roofline model plots the achieved performance (in floating-point operations per second, FLOPS/s) as a function of operational (or arithmetic) intensity (in FLOPS per Byte).
The model detailed here calculates the bytes moved as they move to and from the GPU's HBM.

.. note::

    Integer instructions, cache levels, and matrix-FMA operations are currently not considered.

To get started, you will need to make an input file for ``rocprof``, to be passed in through ``rocprof -i <input_file> --timestamp on -o my_output.csv <my_exe>``.
Below is an example, and contains the information needed:

.. code:: bash

    pmc : SQ_INSTS_VALU_ADD_F16 SQ_INSTS_VALU_MUL_F16 SQ_INSTS_VALU_FMA_F16 SQ_INSTS_VALU_TRANS_F16
    pmc : SQ_INSTS_VALU_ADD_F32 SQ_INSTS_VALU_MUL_F32 SQ_INSTS_VALU_FMA_F32 SQ_INSTS_VALU_TRANS_F32
    pmc : SQ_INSTS_VALU_ADD_F64 SQ_INSTS_VALU_MUL_F64 SQ_INSTS_VALU_FMA_F64 SQ_INSTS_VALU_TRANS_F64
    pmc : SQ_INSTS_VALU_MFMA_MOPS_F16 SQ_INSTS_VALU_MFMA_MOPS_BF16 SQ_INSTS_VALU_MFMA_MOPS_F32 SQ_INSTS_VALU_MFMA_MOPS_F64
    pmc : TCC_EA_RDREQ_32B_sum TCC_EA_RDREQ_sum TCC_EA_WRREQ_sum TCC_EA_WRREQ_64B_sum
    gpu: 0


.. note::

    In an application with more than one kernel, you should strongly consider filtering by kernel name by adding a line like: ``kernel: <kernel_name>`` to the ``rocprof`` input file.

This provides the minimum set of metrics used to construct a roofline model.

Theoretical Roofline
^^^^^^^^^^^^^^^^^^^^

The theoretical (attainable) roofline constructs a theoretical maximum performance for each operational intensity.
The theoretical roofline can be constructed as:

.. math::

    FLOPS_{peak} = minimum(OpIntensity * BW_{HBM}, theoretical\_flops)


Achieved FLOPS/s
^^^^^^^^^^^^^^^^

We calculate the achieved performance at the desired level (here, double-precision floating point, FP64), by summing each metric count and weighting the FMA metric by 2, since a fused multiply-add is considered 2 floating point operations.
Also note that these ``SQ_INSTS_VALU_*`` metrics are reported as per-simd, so we mutliply by the wavefront size as well.
We use this equation to calculate the number of double-precision FLOPS:

.. math::

    FP64\_FLOPS = 64 * (SQ\_INSTS\_VALU\_ADD\_F64 + SQ\_INSTS\_VALU\_MUL\_F64 + 2 * SQ\_INSTS\_VALU\_FMA\_F64)

Then, we divide the number of FLOPS by the elapsed time of the kernel.
This is found from subtracting the ``rocprof`` metrics ``EndNs`` by ``BeginNs``, provided by ``--timestamp on``, then converting from nanoseconds to seconds by dividing by 1,000,000,000 (power(10,9)).

Operational Intensity
^^^^^^^^^^^^^^^^^^^^^

Operational intensity calculates the ratio of FLOPS to bytes moved between HBM and L2 cache.
We calculated FLOPS above (FP64_FLOPS).
We can calculate the number of bytes moved using the ``rocprof`` metrics ``TCC_EA_WRREQ_64B``, ``TCC_EA_WRREQ_sum``, ``TCC_EA_RDREQ_32B``, and ``TCC_EA_RDREQ_sum``.
``TCC`` refers to the L2 cache, and ``EA`` is the interface between L2 and HBM.
``WRREQ`` and ``RDREQ`` are write-requests and read-requests, respectively.
Each of these requests is either 32 bytes or 64 bytes.
So we calculate the number of bytes traveling over the EA interface as:

.. math::

    BytesMoved = BytesWritten + BytesRead

where

.. math::

    BytesWritten = 64 * TCC\_EA\_WRREQ\_64B + 32 * (TCC\_EA\_WRREQ\_sum - TCC\_EA\_WRREQ\_64B)

.. math::

    BytesRead = 32 * TCC\_EA\_RDREQ\_32B + 64 * (TCC\_EA\_RDREQ\_sum - TCC\_EA\_RDREQ\_32B)


CrayPat (From Titan Guide, needs updating)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

CrayPat is a performance analysis tool for evaluating program execution on Cray systems. CrayPat consists of three main components:

pat_build - used to instrument the program for analysis
pat_report - a text report generator that can be used to explore data gathered by instrumented program execution
Apprentice2 - a graphical analysis tool that can be used in addition to pat_report to explore and visualize the data gathered by instrumented program execution

.. note::
    Details of these components can be found in the pat_build, pat_report, and app2 man pages made available by loading the perftools-base module.

The standard workflow for program profiling with CrayPat is as follows:

Load the perftools-base and perftools modules
Build your application as normal
Instrument the application with pat_build
Execute the instrumented application
View the performance data generated in Step 4 with pat_report and Apprentice2
The following steps will guide you through performing a basic analysis with CrayPat and Apprentice2.

Begin with a fully debugged and executable program. Since CrayPat is a performance analysis tool, not a debugger, the targeted program must be capable of running to completion, or intentional termination.





