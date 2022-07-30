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

NVMe
----

Each compute node on Frontier has [2x] 1.92TB \ **N**\ on-\ **V**\ olatile **Me**\mory (NVMe) storage devices (SSDs), colloquially known as a "Burst Buffer" with a peak sequential performance of 5500 MB/s (read) and 2000 MB/s (write). The NVMes could be used to reduce the time that applications wait for I/O. More information can be found later in the `Burst Buffer`_ section.


AMD GPUs
========


Each Frontier node contains 4x AMD Instinct MI250X accelerators. Each MI250X has 2
Graphical Compute Dies (GCD) for a total of 8 GCDs per node. Each GCD can be treated as
its own independent GPU.

.. note::

    **TERMINOLOGY:**

    The 8 GCDs contained in the 4 MI250X will show as 8 separate GPUs according to Slurm,
    ``ROCR_VISIBLE_DEVICES``, and the ROCr runtime, so from this point forward in the
    Frontier guide, we will simply refer to the GCDs as GPUs.

Each GPU has a peak performance of 26.5 TFLOPS (double-precision), 110 compute units, and
64 GB of high-bandwidth memory (HBM2) which can be accessed at a peak of 1.6 TB/s. The 2
GPUs on an MI250X are connected with [4x] GPU-to-GPU Infinity Fabric links for a total
bandwidth of 200+200 GB/s . Consult the diagram in the (TODO) section for
information on how the accelerators connect to each other, to the CPU, and to the network.

.. note::

   The X+X GB/s refers to bidirectional bandwidth, so X GB/s in both directions. 

Each GCD is composed of a command processor, 8 shader engines, and 110 compute units (CUs;
the hardware components that actually perform the mathematical operations), where the CUs
are distributed among the shader engines. The command processor takes the kernel from the
command queue and creates workgroups ("blocks" in CUDA terminology) which are distributed
to the shader engines. The shader engines have an Asynchronous Compute Engine (ACE;
sometimes also called a workload manager) that takes the compute tasks and workgroups it
gets from the command processor, creates wavefronts ("warps" in CUDA terminology) from the
workgroups, and distributes them to the CUs. All wavefronts from a single workgroup are
assigned to the same CU.

.. image:: /images/amd_commandqueue.png
   :align: center
   :alt: Block diagram of command processor and shader engines

..
  TODO: unified memory? If mi250x has it, what is it and how does it work
  TODO: link to HIP from scratch tutorial
  TODO: here are some references https://www.amd.com/system/files/documents/amd-cdna2-white-paper.pdf and https://www.amd.com/system/files/documents/amd-instinct-mi200-datasheet.pdf


.. _amd-nvidia-terminology:

AMD vs NVIDIA Terminology
-------------------------

+-------------------------+--------------+
| AMD                     | NVIDIA       |
+=========================+==============+
| Work-items or Threads   | Threads      |
+-------------------------+--------------+
| Workgroup               | Block        |
+-------------------------+--------------+
| Wavefront               | Warp         |
+-------------------------+--------------+
| Grid                    | Grid         |
+-------------------------+--------------+

  
Blocks (workgroups), Threads (work items), Grids, Wavefronts
------------------------------------------------------------

..
  TODO: make a decision of if we should commit to using AMD terminology or NVIDIA terminology in our documentation and training
  

When kernels are launched on a GPU, a "grid" of thread blocks are created, where the
number of thread blocks in the grid and the number of threads within each block are
defined by the programmer. The number of blocks in the grid (grid size) and the number of
threads within each block (block size) can be specified in one, two, or three dimensions
during the kernel launch. Each thread can be identified with a unique id within the
kernel, indexed along the X, Y, and Z dimensions.

- Number of blocks that can be specified along each dimension in a grid: (2147483647, 2147483647, 2147483647)
- Max number of threads that can be specified along each dimension in a block: (1024, 1024, 1024)

  - However, the total of number of threads in a block has an upper limit of 1024
    [i.e. (size of x dimension * size of y dimension * size of z dimension) cannot exceed
    1024].

Each block (or workgroup) of threads is assigned to a single Compute Unit i.e. a single
block won’t be split across multiple CUs. The threads in a block are scheduled in units of
64 threads called wavefronts (warps in CUDA terminology). When launching a kernel, up to
64KB of block level shared memory called the Local Data Store (LDS) can be statically or
dynamically allocated. This shared memory between the threads in a block allows the
threads to access block local data with much lower latency compared to using the HBM since
the data is in the compute unit itself.



The Compute Unit
----------------

.. image:: /images/amd_computeunit.png
   :align: center
   :alt: Block diagram of the AMD Instinct CDNA2 Compute Unit


Each CU has 4 Matrix Core Units (the equivalent of NVIDIA's Tensor core units) and 4
16-wide SIMD units. For a vector instruction that uses the SIMD units, each wavefront
(which has 64 threads) is assigned to a single 16-wide SIMD unit such that the wavefront
as a whole executes the instruction over 4 cycles, 16 threads per cycle. Since other
wavefronts occupy the other three SIMD units at the same time, the total throughput still
remains 1 instruction per cycle. Each CU maintains an instructions buffer for 10
wavefronts and also maintains 256 registers where each register is 64 4-byte wide
entries. 


..
  Infinty Fabric
  --------------
  
  Infinity Fabric is AMD interconnect technology for connecting various AMD components
    within the node. The two GCDs in the
  accelerator as well as connecting out to the AMD EPYC CPUs.


HIP
---

The Heterogeneous Interface for Portability (HIP) is AMD’s dedicated GPU programming
environment for designing high performance kernels on GPU hardware. HIP is a C++ runtime
API and programming language that allows developers to create portable applications on
different platforms. This means that developers can write their GPU applications and with
very minimal changes be able to run their code in any environment.  The API is very similar
to CUDA, so if you're already familiar with CUDA there is almost no additional work to
learn HIP.

If you wish to learn HIP, there is a recorded training (Github repo for video tutorial
(TODO)). If you have CUDA code on Summit and want to learn how to convert that to HIP and
test it, Summit provides the ``hip-cuda`` module with the ``hipify-perl`` tool to convert
CUDA API calls to HIP and run them on Summit. There is a recorded tutorial for that here
(TODO) (Github repo for the tutorial (TODO)).


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

Most OLCF resources like Frontier use the Slurm batch scheduler. Summit and other IBM hardware use the LSF scheduler.
Below is a comparison table of useful commands among the two schedulers.

+--------------------------------------------+-----------------------+-------------------+
| Task                                       | LSF (Summit)          | Slurm (Frontier)  |
+============================================+=======================+===================+
| View batch queue                           | ``jobstat``           | ``squeue``        |
+--------------------------------------------+-----------------------+-------------------+
| Submit batch script                        | ``bsub``              | ``sbatch``        |
+--------------------------------------------+-----------------------+-------------------+
| Submit interactive batch job               | ``bsub -Is $SHELL``   | ``salloc``        |
+--------------------------------------------+-----------------------+-------------------+
| Run parallel code within batch job         | ``jsrun``             | ``srun``          |
+--------------------------------------------+-----------------------+-------------------+


Srun
----------------------

The ``srun`` command is used to execute an MPI binary on one or more compute nodes in parallel.
``srun`` accepts the following common options:

+----------------------+---------------------------------------+
| ``-N``               | Number of nodes                       |
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
| Bind tasks to allocated CPUs               | ``-b, --bind``            | ``--cpu_bind``          |
+--------------------------------------------+---------------------------+-------------------------+
| Do not run more than one task on resources | ``--exclusive``           | ``--tasks_per_rs 1``    |
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

Thread mapping blurb goes here

CPU Mapping
^^^^^^^^^^^

Mapping to CPUs (limited to no OpenMP or OpenMP=1)

Multithreading
^^^^^^^^^^^^^^

Introducing Multithreading

GPU Mapping
^^^^^^^^^^^

Mapping to GPUs (both noOpenMP / with OpenMP)
