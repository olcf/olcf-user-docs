******************
Summit User Guide
******************

Summit Documentation Resources
==============================

In addition to this Summit User Guide, there are other sources of
documentation, instruction, and tutorials that could be useful for
Summit users. The `OLCF Training
Archive <https://www.olcf.ornl.gov/for-users/training/training-archive/>`__
provides a list of previous training events, including multi-day Summit
Workshops. Some examples of topics addressed during these workshops
include using Summit's NVME burst buffers, CUDA-aware MPI, advanced
networking and MPI, and multiple ways of programming multiple GPUs per
node.

System Overview
===============

Summit is an IBM system located at the Oak Ridge Leadership Computing
Facility. With a theoretical peak double-precision performance of
approximately 200 PF, it is one of the most capable systems in the world
for a wide range of traditional computational science applications. It
is also one of the "smartest" computers in the world for deep learning
applications with a mixed-precision capability in excess of 3 EF.

Summit Nodes
------------

The basic building block of Summit is the IBM Power System AC922 node.
Each of the approximately 4,600 compute nodes on Summit contains two IBM
POWER9 processors and six `NVIDIA Volta
V100 </for-users/system-user-guides/summit/nvidia-v100-gpus/>`__
accelerators and provides a theoretical double-precision capability of
approximately 40 TF. Each POWER9 processor is connected via dual NVLINK
bricks, each capable of a 25GB/s transfer rate in each direction. Nodes
contain 512 GB of DDR4 memory for use by the POWER9 processors and 96 GB
of High Bandwidth Memory (HBM2) for use by the accelerators.
Additionally, each node has 1.6TB of non-volatile memory that can be
used as a burst buffer. The POWER9 processor is built around IBM’s SIMD
Multi-Core (SMC). The processor provides 22 SMCs with separate 32kB L1
data and instruction caches. Pairs of SMCs share a 512kB L2 cache and a
10MB L3 cache. SMCs support Simultaneous Multi-Threading (SMT) up to a
level of 4, meaning each physical core supports up to 4 `hardware
threads <#hardware-threads>`__. The POWER9 processors and V100
accelerators are cooled with cold plate technology. The remaining
components are cooled through more traditional methods, although exhaust
is passed through a back-of-cabinet heat exchanger prior to being
released back into the room. Both the cold plate and heat exchanger
operate using medium temperature water which is more cost-effective for
the center to maintain than chilled water used by older systems.

Node Types
----------

On Summit, there are three major types of nodes you will encounter:
Login, Launch, and Compute. While all of these are similar in terms of
`hardware <#summit-nodes>`__, they differ considerably in their intended
use.

+-------------+----------------------------------------------------------------------------------+
| Node Type   | Description                                                                      |
+=============+==================================================================================+
| Login       | When you connect to Summit, you're placed on a login node. This                  |
|             | is the place to write/edit/compile your code, manage data, submit jobs, etc. You |
|             | should never launch parallel jobs from a login node nor should you run threaded  |
|             | jobs on a login node. Login nodes are shared resources that are in use by many   |
|             | users simultaneously.                                                            |
+-------------+----------------------------------------------------------------------------------+
| Launch      | When your batch script (or interactive batch job) starts                         |
|             | running, it will execute on a Launch Node. (If you are/were a user of Titan,     |
|             | these are similar in function to service nodes on that system). All commands     |
|             | within your job script (or the commands you run in an interactive job) will run  |
|             | on a launch node. Like login nodes, these are shared resources so you should not |
|             | run multiprocessor/threaded programs on Launch nodes. It is appropriate to       |
|             | launch the jsrun command from launch nodes.                                      |
+-------------+----------------------------------------------------------------------------------+
| Compute     | Most of the nodes on Summit are compute nodes. These are where                   |
|             | your parallel job executes. They're accessed via the jsrun command.              |
+-------------+----------------------------------------------------------------------------------+

Although the nodes are logically organized into different types, they
all contain similar hardware. As a result of this homogeneous
architecture there is not a need to cross-compile when building on a
login node. Since login nodes have similar hardware resources as compute
nodes, any tests that are run by your build process (especially by
utilities such as ``autoconf`` and ``cmake``) will have access to the
same type of hardware that is on compute nodes and should not require
intervention that might be required on non-homogeneous systems.

    **NOTE:** Login nodes have (2) 16-core Power9 CPUs and (4) V100 GPUs.
    Compute nodes have (2) 22-core Power9 CPUs and (6) V100 GPUs.

System Interconnect
-------------------

Summit nodes are connected to a dual-rail EDR InfiniBand network
providing a node injection bandwidth of 23 GB/s. Nodes are
interconnected in a Non-blocking Fat Tree topology. This interconnect is
a three-level tree implemented by a switch to connect nodes within each
cabinet (first level) along with Director switches (second and third
level) that connect cabinets together.

File Systems
------------

Summit is connected to an IBM Spectrum Scale™ filesystem providing 250PB
of storage capacity with a peak write speed of 2.5 TB/s. Summit also has
access to the center-wide NFS-based filesystem (which provides user and
project home areas) and has access to the center’s High Performance
Storage System (HPSS) for user and project archival storage.

Operating System
----------------

Summit is running Red Hat Enterprise Linux (RHEL) version 7.5.

Hardware Threads
----------------

The IBM POWER9 processor supports Hardware Threads. Each of the POWER9’s
physical cores has 4 “slices”. These slices provide Simultaneous Multi
Threading (SMT) support within the core. Three SMT modes are supported:
SMT4, SMT2, and SMT1. In SMT4 mode, each of the slices operates
independently of the other three. This would permit four separate
streams of execution (i.e. OpenMP threads or MPI tasks) on each physical
core. In SMT2 mode, pairs of slices work together to run tasks. Finally,
in SMT1 mode the four slices work together to execute the task/thread
assigned to the physical core. Regardless of the SMT mode used, the four
slices share the physical core’s L1 instruction & data caches.
https://vimeo.com/283756938

NVIDIA V100 GPUs
================

The NVIDIA Tesla V100 accelerator has a peak performance of 7.8 TFLOP/s
(double-precision) and contributes to a majority of the computational
work performed on Summit. Each V100 contains 80 streaming
multiprocessors (SMs), 16 GB of high-bandwidth memory (HBM2), and a 6 MB
L2 cache that is available to the SMs. The GigaThread Engine is
responsible for distributing work among the SMs and (8) 512-bit memory
controllers control access to the 16 GB of HBM2 memory. The V100 uses
NVIDIA's NVLink interconnect to pass data between GPUs as well as from
CPU-to-GPU.

.. image:: /images/GV100_FullChip_Diagram_FINAL2_a.png
   :align: center

NVIDIA V100 SM
--------------

Each SM on the V100 contains 32 FP64 (double-precision) cores, 64 FP32
(single-precision) cores, 64 INT32 cores, and 8 tensor cores. A 128-KB
combined memory block for shared memory and L1 cache can be configured
to allow up to 96 KB of shared memory. In addition, each SM has 4
texture units which use the (configured size of the) L1 cache.

.. image:: /images/GV100_SM_Diagram-FINAL2.png
   :align: center

HBM2
----

Each V100 has access to 16 GB of high-bandwidth memory (HBM2), which can
be accessed at speeds of up to 900 GB/s. Access to this memory is
controlled by (8) 512-bit memory controllers, and all accesses to the
high-bandwidth memory go through the 6 MB L2 cache.

NVIDIA NVLink
-------------

The processors within a node are connected by NVIDIA's NVLink
interconnect. Each link has a peak bandwidth of 25 GB/s (in each
direction), and since there are 2 links between processors, data can be
transferred from GPU-to-GPU and CPU-to-GPU at a peak rate of 50 GB/s.

    **NOTE:** The 50-GB/s peak bandwidth stated above is for data transfers
    in a single direction. However, this bandwidth can be achieved in both
    directions simultaneously, giving a peak "bi-directional" bandwidth of
    100 GB/s between processors.

The figure below shows a schematic of the NVLink connections between the
CPU and GPUs on a single socket of a Summit node.

.. image:: /images/NVLink2.png
   :align: center

Tensor Cores
------------

The Tesla V100 contains 640 tensor cores (8 per SM) intended to enable
faster training of large neural networks. Each tensor core performs a
``D = AB + C`` operation on 4x4 matrices. A and B are FP16 matrices,
while C and D can be either FP16 or FP32:

.. image:: /images/nv_tensor_core_1.png
   :width: 85.0%
   :align: center

Each of the 16 elements that result from the AB matrix multiplication
come from 4 floating-point fused-multiply-add (FMA) operations
(basically a dot product between a row of A and a column of B). Each
FP16 multiply yields a full-precision product which is accumulated in a
FP32 result:

.. image:: /images/nv_tensor_core_2.png
   :width: 85.0%
   :align: center

Each tensor core performs 64 of these FMA operations per clock. The 4x4
matrix operations outlined here can be combined to perform matrix
operations on larger (and higher dimensional) matrices.

Volta Multi-Process Service
---------------------------

When a CUDA program begins, each MPI rank creates a separate CUDA
context on the GPU, but the scheduler on the GPU only allows one CUDA
context (and so one MPI rank) at a time to launch on the GPU. This means
that multiple MPI ranks can share access to the same GPU, but each rank
gets exclusive access while the other ranks wait (time-slicing). This
can cause the GPU to become underutilized if a rank (that has exclusive
access) does not perform enough work to saturate the resources of the
GPU. The following figure depicts such time-sliced access to a pre-Volta
GPU.

.. image:: /images/nv_mps_1.png
   :align: center

The Multi-Process Service (MPS) enables multiple processes (e.g. MPI ranks) to
*concurrently* share the resources on a single GPU. This is accomplished by
starting an MPS server process, which funnels the work from multiple CUDA
contexts (e.g. from multiple MPI ranks) into a single CUDA context. In some
cases, this can increase performance due to better utilization of the resources.
The figure below illustrates MPS on a pre-Volta GPU.

.. image:: /images/nv_mps_2.png
   :width: 65.0%
   :align: center

Volta GPUs improve MPS with new capabilities. For instance, each Volta
MPS client (MPI rank) is assigned a "subcontext" that has its own GPU
address space, instead of sharing the address space with other clients.
This isolation helps protect MPI ranks from out-of-range reads/writes
performed by other ranks within CUDA kernels. Because each subcontext
manages its own GPU resources, it can submit work directly to the GPU
without the need to first pass through the MPS server. In addition,
Volta GPUs support up to 48 MPS clients (up from 16 MPS clients on
Pascal).

.. image:: /images/nv_mps_3.png
   :width: 65.0%
   :align: center

  For more information, please see the following document from NVIDIA:
https://docs.nvidia.com/deploy/pdf/CUDA_Multi_Process_Service_Overview.pdf

Unified Memory
--------------

Unified memory is a single virtual address space that is accessible to
any processor in a system (within a node). This means that programmers
only need to allocate a single unified-memory pointer (e.g. using
cudaMallocManaged) that can be accessed by both the CPU and GPU, instead
of requiring separate allocations for each processor. This "managed
memory" is automatically migrated to the accessing processor, which
eliminates the need for explicit data transfers.

.. image:: /images/nv_um_1.png
   :width: 60.0%
   :align: center

  On Pascal-generation GPUs and later, this automatic migration is
enhanced with hardware support. A page migration engine enables GPU page
faulting, which allows the desired pages to be migrated to the GPU "on
demand" instead of the entire "managed" allocation. In addition, 49-bit
virtual addressing allows programs using unified memory to access the
full system memory size. The combination of GPU page faulting and larger
virtual addressing allows programs to oversubscribe the system memory,
so very large data sets can be processed. In addition, new CUDA API
functions introduced in CUDA8 allow users to fine tune the use of
unified memory. Unified memory is further improved on Volta GPUs through
the use of access counters that can be used to automatically tune
unified memory by determining where a page is most often accessed. For
more information, please see the following section of NVIDIA's CUDA
Programming Guide:
http://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#um-unified-memory-programming-hd

Independent Thread Scheduling
-----------------------------

The V100 supports independent thread scheduling, which allows threads to
synchronize and cooperate at sub-warp scales. Pre-Volta GPUs implemented
warps (groups of 32 threads which execute instructions in
single-instruction, multiple thread - SIMT - mode) with a single call
stack and program counter for a warp as a whole.

.. image:: /images/nv_ind_threads_1.png
   :align: center

Within a warp, a mask is used to specify which threads are currently
active when divergent branches of code are encountered. The (active)
threads within each branch execute their statements serially before
threads in the next branch execute theirs. This means that programs on
pre-Volta GPUs should avoid sub-warp synchronization; a sync point in
the branches could cause a deadlock if all threads in a warp do not
reach the synchronization point.

.. image:: /images/nv_ind_threads_2.png
   :align: center

The Volta V100 introduces warp-level synchronization by implementing warps with
a program counter and call stack for each individual thread (i.e.  independent
thread scheduling).

.. image:: /images/nv_ind_threads_3.png
   :align: center

This implementation allows threads to diverge and synchronize at the sub-warp
level using the \_\_syncwarp() function. The independent thread scheduling
enables the thread scheduler to stall execution of any thread, allowing other
threads in the warp to execute different statements. This means that threads in
one branch can stall at a sync point and wait for the threads in the other
branch to reach their sync point.

.. image:: /images/nv_ind_threads_4.png
   :align: center

For more information, please see the following section of NVIDIA's CUDA
Programming Guide:
http://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#independent-thread-scheduling-7-x

Tesla V100 Specifications
-------------------------

+----------------------------------------------------+----------------------------+
| Compute Capability                                 | 7.0                        |
+----------------------------------------------------+----------------------------+
| Peak double precision floating point performance   | 7.8 TFLOP/s                |
+----------------------------------------------------+----------------------------+
| Peak single precision floating point performance   | 15.7 TFLOP/s               |
+----------------------------------------------------+----------------------------+
| Single precision CUDA cores                        | 5120                       |
+----------------------------------------------------+----------------------------+
| Double precision CUDA cores                        | 2560                       |
+----------------------------------------------------+----------------------------+
| Tensor cores                                       | 640                        |
+----------------------------------------------------+----------------------------+
| Clock frequency                                    | 1530 MHz                   |
+----------------------------------------------------+----------------------------+
| Memory Bandwidth                                   | 900 GB/s                   |
+----------------------------------------------------+----------------------------+
| Memory size (HBM2)                                 | 16 GB                      |
+----------------------------------------------------+----------------------------+
| L2 cache                                           | 6 MB                       |
+----------------------------------------------------+----------------------------+
| Shared memory size / SM                            | Configurable up to 96 KB   |
+----------------------------------------------------+----------------------------+
| Constant memory                                    | 64 KB                      |
+----------------------------------------------------+----------------------------+
| Register File Size                                 | 256 KB (per SM)            |
+----------------------------------------------------+----------------------------+
| 32-bit Registers                                   | 65536 (per SM)             |
+----------------------------------------------------+----------------------------+
| Max registers per thread                           | 255                        |
+----------------------------------------------------+----------------------------+
| Number of multiprocessors (SMs)                    | 80                         |
+----------------------------------------------------+----------------------------+
| Warp size                                          | 32 threads                 |
+----------------------------------------------------+----------------------------+
| Maximum resident warps per SM                      | 64                         |
+----------------------------------------------------+----------------------------+
| Maximum resident blocks per SM                     | 32                         |
+----------------------------------------------------+----------------------------+
| Maximum resident threads per SM                    | 2048                       |
+----------------------------------------------------+----------------------------+
| Maximum threads per block                          | 1024                       |
+----------------------------------------------------+----------------------------+
| Maximum block dimensions                           | 1024, 1024, 64             |
+----------------------------------------------------+----------------------------+
| Maximum grid dimensions                            | 2147483647, 65535, 65535   |
+----------------------------------------------------+----------------------------+
| Maximum number of MPS clients                      | 48                         |
+----------------------------------------------------+----------------------------+

 

Further Reading
---------------

For more information on the NVIDIA Volta architecture, please visit the
following (outside) links.

* `NVIDIA Volta Architecture White Paper <http://images.nvidia.com/content/volta-architecture/pdf/volta-architecture-whitepaper.pdf>`_
* `NVIDIA PARALLEL FORALL blog article <https://devblogs.nvidia.com/parallelforall/inside-volta/>`_

Connecting
==========

FIXME

Data Storage & Transfers
========================

Storage Overview
----------------

OLCF users have many options for data storage. Each user has multiple
user-affiliated storage spaces, and each project has multiple
project-affiliated storage spaces where data can be shared for
collaboration. Below we give an overview and explain where each storage
area is mounted.

Alpine IBM Spectrum Scale Filesystem
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Summit mounts a POSIX-based IBM Spectrum Scale parallel filesystem
called Alpine. Alpine's maximum capacity is 250 PB. It is consisted of
77 IBM Elastic Storage Server (ESS) GL4 nodes running IBM Spectrum Scale
5.x which are called Network Shared Disk (NSD) servers. Each IBM ESS GL4
node, is a scalable storage unit (SSU), constituted by two dual-socket
IBM POWER9 storage servers, and a 4X EDR InfiniBand network for up to
100Gbit/sec of networking bandwidth. The maximum performance of the
final production system will be about 2.5 TB/s for sequential I/O and
2.2 TB/s for random I/O under FPP mode, which means each process, writes
its own file. Metada operations are improved with around to minimum
50,000 file access per sec and aggregated up to 2.6 million accesses of
32KB small files.

.. figure:: /images/summit_nds_final.png
   :class: normal aligncenter wp-image-5726545 size-full
   :width: 779px
   :height: 462px
   :align: center

   Figure 1. An example of the NDS servers on Summit

Performance under not ideal workload
""""""""""""""""""""""""""""""""""""

The I/O performance can be lower than the optimal one when you save one
single shared file with non-optimal I/O pattern. Moreover, the previous
performance results are achieved under an ideal system, the system is
dedicated, and a specific number of compute nodes are used. The file
system is shared across many users; the I/O performance can vary because
other users that perform heavy I/O as also executing large scale jobs
and stress the interconnection network. Finally, if the I/O pattern is
not aligned, then the I/O performance can be significantly lower than
the ideal one. Similar, related to the number of the concurrent users,
is applied for the metadata operations, they can be lower than the
expected performance.

Tips
""""

-  For best performance on the IBM Spectrum Scale filesystem, use large
   page aligned I/O and asynchronous reads and writes. The filesystem
   blocksize is 16MB, the minimum fragment size is 16K so when a file
   under 16K is stored, it will still use 16K of the disk. Writing files
   of 16 MB or larger, will achieve better performance. All files are
   striped across LUNs which are distributed across all IO servers.
-  If your application occupies up to two compute nodes and it requires
   a significant number of I/O operations, you could try to add the
   following flag in your job script file and investigate if the total
   execution time is decreased. This flag could cause worse results, it
   depends on the application.

``#BSUB -alloc_flags maximizegpfs``

Major difference between Titan (Lustre) and Summit (IBM Spectrum Scale)
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

The file systems have many technical differences, but we will mention
only what a user needs to be familiar with:

-  On Summit, there is no concept of striping from the user point of
   view, the user uses the Alpine storage without the need to declare
   the striping for files/directories. The GPFS will handle the
   workload, the file system was tuned during the installation.

Storage Areas
---------------

The storage area to use in any given situation depends upon the activity
you wish to carry out. Each user has a User Home area on a Network File
System (NFS) and a User Archive area on the archival High Performance
Storage System (HPSS). These user storage areas are intended to house
user-specific files. Each project has a Project Home area on NFS,
multiple Project Work areas on Lustre and Spectrum Scale, and a Project
Archive area on HPSS. These project storage areas are intended to house
project-centric files. We have defined several areas as listed below by
function:

*  **User Home:** Long-term data for routine access that is unrelated to
   a project. It is mounted on compute nodes of Summit as read only
*  **User Archive:** Long-term data for archival access that is
   unrelated to a project.
*  **Project Home:** Long-term project data for routine access that's
   shared with other project members. It is mounted on compute nodes of
   Summit as read only
*  **Member Work:** Short-term user data for fast, batch-job access that
   is not shared with other project members. There are versions of this
   on both the Atlas Lustre filesystem and the Alpine Spectrum Scale
   filesystem.
*  **Project Work:** Short-term project data for fast, batch-job access
   that's shared with other project members. There are versions of this
   on both the Atlas Lustre filesystem and the Alpine Spectrum Scale
   filesystem.
*  **World Work:** Short-term project data for fast, batch-job access
   that's shared with OLCF users outside your project. There are
   versions of this on both the Atlas Lustre filesystem and the Alpine
   Spectrum Scale filesystem.
*  **Project Archive:** Long-term project data for archival access
   that's shared with other project members.

Storage policy
-----------------

A brief description of each area and basic guidelines to follow are
provided in the table below:

+---------------------+-----------------------------------------------+------------------+---------------+-----------+-----------+---------+----------------------------+
| *Name*              | Path                                          | Type             | Permissions   | Backups   | Purged    | Quota   | Mounted on Compute nodes   |
+=====================+===============================================+==================+===============+===========+===========+=========+============================+
| *User Home*         | ``$HOME``                                     | NFS              | User Set      | yes       | no        | 50GB    | Read-only                  |
+---------------------+-----------------------------------------------+------------------+---------------+-----------+-----------+---------+----------------------------+
| *User Archive*      | ``/home/$USER``                               | HPSS             | User Set      | no        | no        | 2TB     | No                         |
+---------------------+-----------------------------------------------+------------------+---------------+-----------+-----------+---------+----------------------------+
| *Project Home*      | ``/ccs/proj/[projid]``                        | NFS              | 770           | yes       | no        | 50GB    | Read-only                  |
+---------------------+-----------------------------------------------+------------------+---------------+-----------+-----------+---------+----------------------------+
| *Member Work*       | ``/gpfs/alpine/scratch/[userid]/[projid]/``   | Spectrum Scale   | 700           | no        | 90 days   | 50TB    | Yes                        |
+---------------------+-----------------------------------------------+------------------+---------------+-----------+-----------+---------+----------------------------+
| *Project Work*      | ``/gpfs/alpine/proj-shared/[projid]``         | Spectrum Scale   | 770           | no        | 90 days   | 50TB    | Yes                        |
+---------------------+-----------------------------------------------+------------------+---------------+-----------+-----------+---------+----------------------------+
| *World Work*        | ``/gpfs/alpine/world-shared/[projid]``        | Spectrum Scale   | 775           | no        | 90 days   | 50TB    | Yes                        |
+---------------------+-----------------------------------------------+------------------+---------------+-----------+-----------+---------+----------------------------+
| *Project Archive*   | ``/proj/[projid]``                            | HPSS             | 770           | no        | no        | 100TB   | No                         |
+---------------------+-----------------------------------------------+------------------+---------------+-----------+-----------+---------+----------------------------+

For storage policy on TITAN, click here

On Summit paths to the various project-centric work storage areas are
simplified by the use of environment variables that point to the proper
directory on a per-user basis:

-  Member Work Directory: ``$MEMBERWORK/[projid]``
-  Project Work Directory: ``$PROJWORK/[projid]``
-  World Work Directory: ``$WORLDWORK/[projid]``

These environment variables are not set on the data transfer nodes.

Information
^^^^^^^^^^^

-  Although there are no hard quota limits, an upper storage limit
   should be reported in the project request. The available space of a
   project can be modified upon request.
-  The user will be informed when the project reaches 90% of the
   requested storage utilization.

Purge
^^^^^

To keep the Lustre and Spectrum Scale file systems exceptionally
performant, untouched files in the project and user areas are purged at
the intervals shown in the table above. Please make sure that valuable
data is moved off of these systems regularly. See `HPSS Best
Practices <./#hpss-best-practices>`__ for information about using the
HSI and HTAR utilities to archive data on HPSS.

Retention
^^^^^^^^^

At the completion of a project or at the end of a member's association
with the project, data will be available for 90 days, except in areas
that are purged, in that case, the data will be retained according to
the purge policy. After 90 days, the data will not be available but not
purged for another 60 days, where the data will be removed if it not
requested otherwise.

Other OLCF Storage Systems
----------------------------

The High Performance Storage System (HPSS) at the OLCF provides
longer-term storage for the large amounts of data created on the OLCF
compute systems. The HPSS is accessible from all OLCF Filesystems
through utilities called HSI and HTAR. For more information on using HSI
or HTAR, see the `HPSS Best Practices <./#hpss-best-practices>`__
documentation. OLCF also has a Network File System, referred to as NFS,
and Lustre filesystems called Atlas. Summit does not mount Lustre.
However, during the early use of Summit, users may need to use Lustre in
a multi-stage process with HPSS for larger data transfer with Alpine. To
learn more about this please see `Data Transfer and
Summit <./#data-transfer-and-summit>`__ section below. The following
shows the availability of each of the filesystems on primary OLCF
clusters and supercomputers.

+------------------------------------+------------+-------------+------------+-----------------------+------------+------------+
| Area                               | Summit     | Summitdev   | Titan      | Data Transfer Nodes   | Rhea       | Eos        |
+====================================+============+=============+============+=======================+============+============+
| Atlas Lustre Filesystem            | no         | no          | yes        | yes                   | yes        | yes        |
+------------------------------------+------------+-------------+------------+-----------------------+------------+------------+
| Alpine Spectrum Scale Filesystem   | yes        | yes         | no         | yes                   | no         | no         |
+------------------------------------+------------+-------------+------------+-----------------------+------------+------------+
| NFS Network Filesystem             | yes        | yes         | yes        | yes                   | yes        | yes        |
+------------------------------------+------------+-------------+------------+-----------------------+------------+------------+
| HPSS                               | HSI/Htar   | HSI/Htar    | HSI/Htar   | HSI/Htar              | HSI/Htar   | HSI/Htar   |
+------------------------------------+------------+-------------+------------+-----------------------+------------+------------+

Guidelines
-----------

A brief description of each area and basic guidelines to follow are
provided in the table below:

+-------------------+-------------------+---------------------------------------------+----------------+-------------+---------+------------+-------+
| *System*          | *Name*            | Path                                        | Type           | Permissions | Backups | Purged     | Quota |
+===================+===================+=============================================+================+=============+=========+============+=======+
| *User Home*       | *User Home*       | ``$HOME``                                   | NFS            | User Set    | yes     | no         | 50GB  |
+-------------------+-------------------+---------------------------------------------+----------------+-------------+---------+------------+-------+
| *User Archive*    | *User Archive*    | ``/home/$USER``                             | HPSS           | User Set    | no      | no         | 2TB   |
+-------------------+-------------------+---------------------------------------------+----------------+-------------+---------+------------+-------+
| *Project Home*    | *Project Home*    | ``/ccs/proj/[projid]``                      | NFS            | 770         | yes     | no         | 50GB  |
+-------------------+-------------------+---------------------------------------------+----------------+-------------+---------+------------+-------+
| **Alpine**        | *Member Work*     | ``/gpfs/alpine/scratch/[userid]/[projid]/`` | Spectrum Scale | 700         | no      | 90 days    | 50TB  |
+                   +-------------------+---------------------------------------------+----------------+-------------+---------+------------+-------+
|                   | *Project Work*    | ``/gpfs/alpine/proj-shared/[projid]/``      | Spectrum Scale | 770         | no      | 90 days    | 50TB  |
+                   +-------------------+---------------------------------------------+----------------+-------------+---------+------------+-------+
|                   | *World Work*      | ``/gpfs/alpine/world-shared/[projid]/``     | Spectrum Scale | 775         | no      | 90 days    | 50TB  |
+-------------------+-------------------+---------------------------------------------+----------------+-------------+---------+------------+-------+
| **Atlas**         | *Member Work*     | ``/lustre/atlas/scratch/[userid]/[projid]`` | Lustre         | 700         | no      | 14 days    | 10TB  |
+                   +-------------------+---------------------------------------------+----------------+-------------+---------+------------+-------+
|                   | *Project Work*    | ``/lustre/atlas/proj-shared/[projid]``      | Lustre         | 770         | no      | 90 days    | 100TB |
+                   +-------------------+---------------------------------------------+----------------+-------------+---------+------------+-------+
|                   | *World Work*      | ``/lustre/atlas/world-shared/[projid]``     | Lustre         | 775         | no      | 90 days    | 10TB  |
+-------------------+-------------------+---------------------------------------------+----------------+-------------+---------+------------+-------+
| *Project Archive* | *Project Archive* | ``/proj/[projid]``                          | HPSS           | 770         | no      | no         | 100TB |
+-------------------+-------------------+---------------------------------------------+----------------+-------------+---------+------------+-------+


Backups for Files on NFS
^^^^^^^^^^^^^^^^^^^^^^^^

Online backups are performed at regular intervals for your files in
project home and user home. Hourly backups for the past 24 hours, daily
backups for the last 7 days, and 1 weekly backup are available. The
backup directories are named ``hourly.*``, ``daily.* ``, and
``weekly.* `` where ``*`` is the date/time stamp of the backup. For
example, ``hourly.2016-12-01-0905`` is an hourly backup made on December
1, 2016 at 9:05 AM. The backups are accessed via the ``.snapshot``
subdirectory. You may list your available hourly/daily/weekly backups by
doing “\ ``ls .snapshot``\ ”. The ``.snapshot`` feature is available in
any subdirectory of your home directory and will show the online backup
of that subdirectory. In other words, you don’t have to start at
``/ccs/home/$USER`` and navigate the full directory structure; if you’re
in a /ccs/home subdirectory several “levels” deep, an
“\ ``ls .snapshot``\ ” will access the available backups of that
subdirectory. To retrieve a backup, simply copy it into your desired
destination with the ``cp`` command.

Retention
^^^^^^^^^

At the completion of a project or at the end of a member's association
with the project, data will be retained for 90 days, except in areas
that are purged, in that case the data will be retained according the
purge policy. A more detailed description of each storage area is given
below. [ls\_content\_block id="26702"]

User-Centric Data Storage
-------------------------

Users are provided with several storage areas, each of which serve
different purposes. These areas are intended for storage of user data,
not for storage of project data.

The following table summarizes user-centric storage areas available on
OLCF resources and lists relevant polices.

**User-Centric Storage Areas**

+--------------+-----------------+------+-----------------+-------------+---------+--------+-----------+
| Area         | Path            | Type | Permissions     | Quota       | Backups | Purged | Retention |
+==============+=================+======+=================+=============+=========+========+===========+
| User Home    | ``$HOME``       | NFS  | User-controlled | 50 GB       | Yes     | No     | 90 days   |
+--------------+-----------------+------+-----------------+-------------+---------+--------+-----------+
| User Archive | ``/home/$USER`` | HPSS | User-controlled | 2 TB [#f1]_ | **No**  | No     | 90 days   |
+--------------+-----------------+------+-----------------+-------------+---------+--------+-----------+

.. rubric:: footnotes

.. [#f1] In addition, there is a quota/limit of 2,000 files on this directory.

User Home Directories (NFS)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Each user is provided a home directory to store frequently used items
such as source code, binaries, and scripts.

User Home Path
""""""""""""""

Home directories are located in a Network File System (NFS) that is
accessible from all OLCF resources as ``/ccs/home/$USER``.

The environment variable ``$HOME`` will always point to your current
home directory. It is recommended, where possible, that you use this
variable to reference your home directory. In cases in which using
``$HOME`` is not feasible, it is recommended that you use
``/ccs/home/$USER``.

Users should note that since this is an NFS-mounted filesystem, its
performance will not be as high as other filesystems.

User Home Quotas
""""""""""""""""

Quotas are enforced on user home directories. To request an increased
quota, contact the OLCF User Assistance Center. To view your current
quota and usage, use the ``quota`` command:

.. code::

    $ quota -Qs
    Disk quotas for user usrid (uid 12345):
         Filesystem  blocks   quota   limit   grace   files   quota   limit   grace
    nccsfiler1a.ccs.ornl.gov:/vol/home
                      4858M   5000M   5000M           29379   4295m   4295m

User Home Backups
"""""""""""""""""

If you accidentally delete files from your home directory, you may be
able to retrieve them. Online backups are performed at regular
intervals. Hourly backups for the past 24 hours, daily backups for the
last 7 days, and 1 weekly backup are available. It is possible that the
deleted files are available in one of those backups. The backup
directories are named ``hourly.*``, ``daily.* ``, and ``weekly.* ``
where ``*`` is the date/time stamp of the backup. For example,
``hourly.2016-12-01-0905`` is an hourly backup made on December 1, 2016
at 9:05 AM.

The backups are accessed via the ``.snapshot`` subdirectory. Note that
if you do an ``ls`` (even with the ``-a`` option) of any directory you
won’t see a ``.snapshot`` subdirectory, but you’ll be able to do
“\ ``ls .snapshot``\ ” nonetheless. This will show you the
hourly/daily/weekly backups available. The ``.snapshot`` feature is
available in any subdirectory of your home directory and will show the
online backup of that subdirectory. In other words, you don’t have to
start at ``/ccs/home/$USER`` and navigate the full directory structure;
if you’re in a /ccs/home subdirectory several “levels” deep, an
“\ ``ls .snapshot``\ ” will access the available backups of that
subdirectory.

To retrieve a backup, simply copy it into your desired destination with
the ``cp`` command.

User Home Permissions
"""""""""""""""""""""

The default permissions for user home directories are ``0750`` (full
access to the user, read and execute for the group). Users have the
ability to change permissions on their home directories, although it is
recommended that permissions be set to as restrictive as possible
(without interfering with your work).

User Website Directory
""""""""""""""""""""""

Users interested in sharing files publicly via the World Wide Web can
request a user website directory be created for their account. User
website directories (``~/www``) have a 5GB storage quota and allow
access to files at ``http://users.nccs.gov/~user`` (where ``user`` is
your userid). If you are interested in having a user website directory
created, please contact the User Assistance Center at
help@olcf.ornl.gov.

User Archive Directories (HPSS)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The High Performance Storage System (HPSS) at the OLCF provides
longer-term storage for the large amounts of data created on the OLCF
compute systems. The mass storage facility consists of tape and disk
storage components, servers, and the HPSS software. After data is
uploaded, it persists on disk for some period of time. The length of its
life on disk is determined by how full the disk caches become. When data
is migrated to tape, it is done so in a first-in, first-out fashion.

User archive areas on HPSS are intended for storage of data not
immediately needed in either User Home directories (NFS) or User Work
directories (Lustre®). User Archive areas also serve as a location for
users to store backup copies of user files. User Archive directories
should not be used to store project-related data. Rather, Project
Archive directories should be used for project data.

User archive directories are located at ``/home/$USER``.

User Archive Access
"""""""""""""""""""

Each OLCF user receives an HPSS account automatically. Users can
transfer data to HPSS from any OLCF system using the HSI or HTAR
utilities. For more information on using HSI or HTAR, see the `HPSS Best
Practices <./#hpss-best-practices>`__ section.

User Archive Accounting
"""""""""""""""""""""""

Each file and directory on HPSS is associated with an HPSS storage
allocation. For information on HPSS storage allocations, please visit
the `HPSS Archive Accounting <./#hpss-archive-accounting>`__ section.

For information on usage and best practices for HPSS, please see the
section `HPSS - High Performance Storage
System <./#hpss-high-performance-storage-system>`__ below.

--------------


Project-Centric Data Storage
----------------------------

Project directories provide members of a project with a common place to
store code, data, and other files related to their project.

Project Home Directories (NFS)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+------------------+--------------------------+--------+---------------+-----------+----------+---------+
| *Name*           | Path                     | Type   | Permissions   | Backups   | Purged   | Quota   |
+==================+==========================+========+===============+===========+==========+=========+
| *Project Home*   | ``/ccs/proj/[projid]``   | NFS    | 770           | yes       | no       | 50GB    |
+------------------+--------------------------+--------+---------------+-----------+----------+---------+

Projects are provided with a Project Home storage area in the
NFS-mounted filesystem. This area is intended for storage of data, code,
and other files that are of interest to all members of a project. Since
Project Home is an NFS-mounted filesystem, its performance will not be
as high as other filesystems.

Project Home Path
"""""""""""""""""

Project Home area is accessible at ``/ccs/proj/abc123`` (where
``abc123`` is your project ID).

Project Home Quotas
"""""""""""""""""""

To check your project's current usage, run ``df -h /ccs/proj/abc123``
(where ``abc123`` is your project ID). Quotas are enforced on project
home directories. The current limit is shown in the table above.

Project Home Permissions
""""""""""""""""""""""""

The default permissions for project home directories are ``0770`` (full
access to the user and group). The directory is owned by root and the
group includes the project's group members. All members of a project
should also be members of that group-specific project. For example, all
members of project "ABC123" should be members of the "abc123" UNIX
group.

Three Project Work Areas to Facilitate Collaboration
""""""""""""""""""""""""""""""""""""""""""""""""""""

To facilitate collaboration among researchers, the OLCF provides (3)
distinct types of project-centric work storage areas: *Member Work*
directories, *Project Work* directories, and *World Work* directories.
Each directory should be used for storing files generated by
computationally-intensive HPC jobs related to a project.

+----------------+--------------------------------------------+-----------------+-------------+---------+-----------+-------+
| *Name*         | Path                                       | Type            | Permissions | Backups | Purged    | Quota |
+================+============================================+=================+=============+=========+===========+=======+
| *Member Work*  | ``/lustre/atlas/scratch/[projid]``         | Lustre          | 700         | no      | 14 days   | 10TB  |
+                +--------------------------------------------+-----------------+-------------+---------+-----------+-------+
|                | ``/gpfs/alpine/scratch/[userid]/[projid]`` | Spectrum Scale  | 700         | no      | 90 days   | 50TB  |
+----------------+--------------------------------------------+-----------------+-------------+---------+-----------+-------+
| *Project Work* | ``/lustre/atlas/proj-shared/[projid]``     | Lustre          | 770         | no      | 90 days   | 100TB |
+                +--------------------------------------------+-----------------+-------------+---------+-----------+-------+
|                | ``/gpfs/alpine/proj-shared/[projid]``      | Spectrum Scale  | 770         | no      | 90 days   | 50TB  |
+----------------+--------------------------------------------+-----------------+-------------+---------+-----------+-------+
| *World Work*   | ``/lustre/atlas/world-shared/[projid]``    | Lustre          | 775         | no      | 90 days   | 10TB  |
+                +--------------------------------------------+-----------------+-------------+---------+-----------+-------+
|                | ``/gpfs/alpine/world-shared/[projid]``     | Spectrum Scale  | 775         | no      | 90 days   | 50TB  |
+----------------+--------------------------------------------+-----------------+-------------+---------+-----------+-------+

The difference between the three lies in the accessibility of the data
to project members and to researchers outside of the project. Member
Work directories are accessible only by an individual project member by
default. Project Work directories are accessible by all project members.
World Work directories are readable by any user on the system.

Permissions
___________

UNIX Permissions on each project-centric work storage area differ
according to the area's intended collaborative use. Under this setup,
the process of sharing data with other researchers amounts to simply
ensuring that the data resides in the proper work directory.

-  Member Work Directory: ``700``
-  Project Work Directory: ``770``
-  World Work Directory: ``775``

For example, if you have data that must be restricted only to yourself,
keep them in your Member Work directory for that project (and leave the
default permissions unchanged). If you have data that you intend to
share with researchers within your project, keep them in the project's
Project Work directory. If you have data that you intend to share with
researchers outside of a project, keep them in the project's World Work
directory.

Backups
"""""""

Member Work, Project Work, and World Work directories **are not backed
up**. Project members are responsible for backing up these files, either
to Project Archive areas (HPSS) or to an off-site location.

Project Archive Directories
^^^^^^^^^^^^^^^^^^^^^^^^^^^

+---------------------+----------------------+--------+---------------+-----------+----------+---------+
| *Name*              | Path                 | Type   | Permissions   | Backups   | Purged   | Quota   |
+=====================+======================+========+===============+===========+==========+=========+
| *Project Archive*   | ``/proj/[projid]``   | HPSS   | 770           | no        | no       | 100TB   |
+---------------------+----------------------+--------+---------------+-----------+----------+---------+

Projects are also allocated project-specific archival space on the High
Performance Storage System (HPSS). The default quota is shown on the
table above. If a higher quota is needed, contact the User Assistance
Center. The Project Archive space on HPSS is intended for storage of
data not immediately needed in either Project Home (NFS) areas nor
Project Work (Alpine) areas, and to serve as a location to store backup
copies of project-related files.

Project Archive Path
""""""""""""""""""""

The project archive directories are located at ``/proj/pjt000`` (where
``pjt000`` is your Project ID).

Project Archive Access
""""""""""""""""""""""

Project Archive directories may only be accessed via utilities called
HSI and HTAR. For more information on using HSI or HTAR, see the `HPSS
Best Practices <./#hpss-best-practices>`__ section. [ls\_content\_block
id="7126959"] [ls\_content\_block id="5798390"]

Software
========

For a full list of software available at the OLCF, please see the
`Software </for-users/software/>`__ section.

Shell & Programming Environments
================================

OLCF systems provide hundreds of software packages and scientific
libraries pre-installed at the system-level for users to take advantage
of. To facilitate this, environment management tools are employed to
handle necessary changes to the shell. The sections below provide
information about using these management tools on Summit.

Default Shell
-------------

A user’s default shell is selected when completing the User Account
Request form. The chosen shell is set across all OLCF resources, and is
the shell interface a user will be presented with upon login to any OLCF
system. Currently, supported shells include:

-  bash
-  tsch
-  csh
-  ksh

If you would like to have your default shell changed, please contact the
`OLCF User Assistance Center </for-users/user-assistance/>`__ at
help@nccs.gov.

Environment Management with Lmod
--------------------------------

Environment modules are provided through
`Lmod <https://lmod.readthedocs.io/en/latest/>`__, a Lua-based module
system for dynamically altering shell environments. By managing changes
to the shell’s environment variables (such as ``PATH``,
``LD_LIBRARY_PATH``, and ``PKG_CONFIG_PATH``), Lmod allows you to alter
the software available in your shell environment without the risk of
creating package and version combinations that cannot coexist in a
single environment. Lmod is a recursive environment module system,
meaning it is aware of module compatibility and actively alters the
environment to protect against conflicts. Messages to stderr are issued
upon Lmod implicitly altering the environment. Environment modules are
structured hierarchically by compiler family such that packages built
with a given compiler will only be accessible if the compiler family is
first present in the environment.

    **Note:** Lmod can interpret both Lua modulefiles and legacy Tcl
    modulefiles. However, long and logic-heavy Tcl modulefiles may require
    porting to Lua.

General Usage
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
on a per-user basis in ``$HOME/.lmod.d``. To create a collection called
"NAME" from the currently loaded modules, simply call
``module save NAME``. Omitting "NAME" will set the user’s default
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
    variable LMOD\_SYSTEM\_NAME). This ensures that only collections
    appended with the name of the current system are visible.

The following screencast shows an example of setting up user-defined
module collections on Summit. https://vimeo.com/293582400

Compiling
=========

Compilers
---------

Available Compilers
^^^^^^^^^^^^^^^^^^^

The following compilers are available on Summit: **XL:** IBM XL
Compilers *(loaded by default)* **LLVM:** LLVM compiler infrastructure
**PGI:** Portland Group compiler suite **GNU:** GNU Compiler Collection
**NVCC**: CUDA C compiler Upon login, the default versions of the XL
compiler suite and Spectrum Message Passing Interface (MPI) are added to
each user's environment through the modules system. No changes to the
environment are needed to make use of the defaults. Multiple versions of
each compiler family are provided, and can be inspected using the
modules system:

::

    summit$ module -t avail pgi
    /sw/summit/modulefiles/site/linux-rhel7-ppc64le/Core:
    pgi/17.10-patched
    pgi/18.3
    pgi/18.4
    pgi/18.5
    pgi/18.7

C compilation
^^^^^^^^^^^^^

    **Note:** type char is unsigned by default

+--------------+------------------+----------------+---------------+------------------+------------------+---------------------------+--------------------+
| **Vendor**   | **Module**       | **Compiler**   | **Version**   | **Enable C99**   | **Enable C11**   | **Default signed char**   | **Define macro**   |
+==============+==================+================+===============+==================+==================+===========================+====================+
| **IBM**      | xl               | xlc xlc\_r     | 13.1.6        | -std=gnu99       | -std=gnu11       | -qchar=signed             | -WF,-D             |
+--------------+------------------+----------------+---------------+------------------+------------------+---------------------------+--------------------+
| **GNU**      | system default   | gcc            | 4.8.5         | -std=gnu99       | -std=gnu11       | -fsigned-char             | -D                 |
+--------------+------------------+----------------+---------------+------------------+------------------+---------------------------+--------------------+
| **GNU**      | gcc              | gcc            | 6.4.0         | -std=gnu99       | -std=gnu11       | -fsigned-char             | -D                 |
+--------------+------------------+----------------+---------------+------------------+------------------+---------------------------+--------------------+
| **LLVM**     | llvm             | clang          | 3.8.0         | default          | -std=gnu11       | -fsigned-char             | -D                 |
+--------------+------------------+----------------+---------------+------------------+------------------+---------------------------+--------------------+
| **PGI**      | pgi              | pgcc           | 17.10         | -c99             | -c11             | -Mschar                   | -D                 |
+--------------+------------------+----------------+---------------+------------------+------------------+---------------------------+--------------------+

C++ compilations
^^^^^^^^^^^^^^^^

    **Note:** type char is unsigned by default

+--------------+------------------+-------------------+---------------+--------------------------------+--------------------------------+---------------------------+--------------------+
| **Vendor**   | **Module**       | **Compiler**      | **Version**   | **Enable C++11**               | **Enable C++14**               | **Default signed char**   | **Define macro**   |
+==============+==================+===================+===============+================================+================================+===========================+====================+
| **IBM**      | xl               | xlc++, xlc++\_r   | 13.1.6        | -std=gnu++11                   | -std=gnu++1y *(PARTIAL)*       | -qchar=signed             | -WF,-D             |
+--------------+------------------+-------------------+---------------+--------------------------------+--------------------------------+---------------------------+--------------------+
| **GNU**      | system default   | g++               | 4.8.5         | -std=gnu++11                   | -std=gnu++1y                   | -fsigned-char             | -D                 |
+--------------+------------------+-------------------+---------------+--------------------------------+--------------------------------+---------------------------+--------------------+
| **GNU**      | gcc              | g++               | 6.4.0         | -std=gnu++11                   | -std=gnu++1y                   | -fsigned-char             | -D                 |
+--------------+------------------+-------------------+---------------+--------------------------------+--------------------------------+---------------------------+--------------------+
| **LLVM**     | llvm             | clang++           | 3.8.0         | -std=gnu++11                   | -std=gnu++1y                   | -fsigned-char             | -D                 |
+--------------+------------------+-------------------+---------------+--------------------------------+--------------------------------+---------------------------+--------------------+
| **PGI**      | pgi              | pgc++             | 17.10         | -std=c++11 --gnu\_extensions   | -std=c++14 --gnu\_extensions   | -Mschar                   | -D                 |
+--------------+------------------+-------------------+---------------+--------------------------------+--------------------------------+---------------------------+--------------------+

Fortran compilation
^^^^^^^^^^^^^^^^^^^

+--------------+------------------+-----------------------------------+----------------+-------------------------------+-------------------------------+-------------------------------+--------------------+
| **Vendor**   | **Module**       | **Compiler**                      | **Version**    | **Enable F90**                | **Enable F2003**              | **Enable F2008**              | **Define macro**   |
+==============+==================+===================================+================+===============================+===============================+===============================+====================+
| **IBM**      | xl               | xlf xlf90 xlf95 xlf2003 xlf2008   | 15.1.6         | -qlanglvl=90std               | -qlanglvl=2003std             | -qlanglvl=2008std             | -WF,-D             |
+--------------+------------------+-----------------------------------+----------------+-------------------------------+-------------------------------+-------------------------------+--------------------+
| **GNU**      | system default   | gfortran                          | 4.8.5, 6.4.0   | -std=f90                      | -std=f2003                    | -std=f2008                    | -D                 |
+--------------+------------------+-----------------------------------+----------------+-------------------------------+-------------------------------+-------------------------------+--------------------+
| **LLVM**     | llvm             | xlflang                           | 3.8.0          | n/a                           | n/a                           | n/a                           | -D                 |
+--------------+------------------+-----------------------------------+----------------+-------------------------------+-------------------------------+-------------------------------+--------------------+
| **PGI**      | pgi              | pgfortran                         | 17.10          | use .F90 source file suffix   | use .F03 source file suffix   | use .F08 source file suffix   | -D                 |
+--------------+------------------+-----------------------------------+----------------+-------------------------------+-------------------------------+-------------------------------+--------------------+

    **Note:** \* The xlflang module currently conflicts with the clang
    module. This restriction is expected to be lifted in future releases.

MPI
^^^

MPI on Summit is provided by IBM Spectrum MPI. Spectrum MPI provides
compiler wrappers that automatically choose the proper compiler to build
your application. The following compiler wrappers are available: **C**:
``mpicc`` **C++**: ``mpic++``, ``mpiCC`` **Fortran**: ``mpifort``,
``mpif77``, ``mpif90`` While these wrappers conveniently abstract away
linking of Spectrum MPI, it's sometimes helpful to see exactly what's
happening when invoked. The ``--showme`` flag will display the full link
lines, without actually compiling:

::

    summit$ mpicc --showme
    /sw/summit/xl/16.1.1-beta6/xlC/16.1.1/bin/xlc -I/autofs/nccs-svm1_sw/summit/.swci/1-compute/opt/spack/20171006/linux-rhel7-ppc64le/xl-16.1.1-beta6/spectrum-mpi-10.2.0.7-20180830-eyo7zxm2piusmyffr3iytmgwdacl67ju/include -pthread -L/autofs/nccs-svm1_sw/summit/.swci/1-compute/opt/spack/20171006/linux-rhel7-ppc64le/xl-16.1.1-beta6/spectrum-mpi-10.2.0.7-20180830-eyo7zxm2piusmyffr3iytmgwdacl67ju/lib -lmpiprofilesupport -lmpi_ibm

OpenMP
^^^^^^

    **Note:** When using OpenMP with IBM XL compilers, the thread-safe
    compiler variant is required; These variants have the same name as the
    non-thread-safe compilers with an additional ``_r`` suffix. e.g. to
    compile OpenMPI C code one would use ``xlc_r``

    **Note:** OpenMP offloading support is still under active development.
    Performance and debugging capabilities in particular are expected to
    improve as the implementations mature.

+---------------+-------------------+---------------------+-------------------+---------------------------------------------------------------------------------+
| **Vendor**    | **3.1 Support**   | **Enable OpenMP**   | **4.x Support**   | **Enable OpenMP 4.x Offload**                                                   |
+===============+===================+=====================+===================+=================================================================================+
| **IBM**       | FULL              | -qsmp=omp           | PARTIAL           | -qsmp=omp -qoffload                                                             |
+---------------+-------------------+---------------------+-------------------+---------------------------------------------------------------------------------+
| **GNU**       | FULL              | -fopenmp            | PARTIAL           | -fopenmp                                                                        |
+---------------+-------------------+---------------------+-------------------+---------------------------------------------------------------------------------+
| **clang**     | FULL              | -fopenmp            | PARTIAL           | -fopenmp -fopenmp-targets=nvptx64-nvidia-cuda --cuda-path=${OLCF\_CUDA\_ROOT}   |
+---------------+-------------------+---------------------+-------------------+---------------------------------------------------------------------------------+
| **xlflang**   | FULL              | -fopenmp            | PARTIAL           | -fopenmp -fopenmp-targets=nvptx64-nvidia-cuda                                   |
+---------------+-------------------+---------------------+-------------------+---------------------------------------------------------------------------------+
| **PGI**       | FULL              | -mp                 | NONE              | NONE                                                                            |
+---------------+-------------------+---------------------+-------------------+---------------------------------------------------------------------------------+

OpenACC
^^^^^^^

+--------------+--------------------+-----------------------+-------------------------+
| **Vendor**   | **Module**         | **OpenACC Support**   | **Enable OpenACC**      |
+==============+====================+=======================+=========================+
| **IBM**      | xl                 | NONE                  | NONE                    |
+--------------+--------------------+-----------------------+-------------------------+
| **GNU**      | system default     | NONE                  | NONE                    |
+--------------+--------------------+-----------------------+-------------------------+
| **GNU**      | gcc                | 2.5                   | -fopenacc               |
+--------------+--------------------+-----------------------+-------------------------+
| **LLVM**     | clang or xlflang   | NONE                  | NONE                    |
+--------------+--------------------+-----------------------+-------------------------+
| **PGI**      | pgi                | 2.5                   | -acc, -ta=nvidia:cc70   |
+--------------+--------------------+-----------------------+-------------------------+

CUDA compilation
^^^^^^^^^^^^^^^^

NVIDIA
""""""

CUDA C/C++ support is provided through the ``cuda`` module. **nvcc** :
Primary CUDA C/C++ compiler

Language support


**-std=c++11** : provide C++11 support **--expt-extended-lambda** :
provide experimental host/device lambda support
**--expt-relaxed-constexpr** : provide experimental host/device
constexpr support

Compiler support


NVCC currently supports XL, GCC, and PGI C++ backends. **--ccbin** : set
to host compiler location

CUDA Fortran compilation
^^^^^^^^^^^^^^^^^^^^^^^^

IBM
"""

The IBM compiler suite is made available through the default loaded xl
module, the cuda module is also required. xlcuf : primary Cuda fortran
compiler, thread safe **Language support flags** -qlanglvl=90std :
provide Fortran90 support -qlanglvl=95std : provide Fortran95 support
-qlanglvl=2003std : provide Fortran2003 support -qlanglvl=2008std :
provide Fortran2003 support

PGI
"""

The PGI compiler suite is available through the pgi module. pgfortran :
Primary fortran compiler with CUDA Fortran support

Language support:


Files with .cuf suffix automatically compiled with cuda fortran support
Standard fortran suffixed source files determines the standard involved,
see the man page for full details -Mcuda : Enable CUDA Fortran on
provided source file

Linking in Libraries
--------------------

OLCF systems provide hundreds of software packages and scientific
libraries pre-installed at the system-level for users to take advantage
of. In order to link these libraries into an application, users must
direct the compiler to their location. The ``module show`` command can
be used to determine the location of a particular library. For example

::

    summit$ module show essl
    ------------------------------------------------------------------------------------
       /sw/summit/modulefiles/core/essl/6.1.0-1:
    ------------------------------------------------------------------------------------
    whatis("ESSL 6.1.0-1 ")
    prepend_path("LD_LIBRARY_PATH","/sw/summit/essl/6.1.0-1/essl/6.1/lib64")
    append_path("LD_LIBRARY_PATH","/sw/summit/xl/16.1.1-beta4/lib")
    prepend_path("MANPATH","/sw/summit/essl/6.1.0-1/essl/6.1/man")
    setenv("OLCF_ESSL_ROOT","/sw/summit/essl/6.1.0-1/essl/6.1")
    help([[ESSL 6.1.0-1

    ]])

When this module is loaded, the ``$OLCF_ESSL_ROOT`` environment variable
holds the path to the ESSL installation, which contains the lib64/ and
include/ directories:

::

    summit$ module load essl
    summit$ echo $OLCF_ESSL_ROOT
    /sw/summit/essl/6.1.0-1/essl/6.1
    summit$ ls $OLCF_ESSL_ROOT
    FFTW3  READMES  REDIST.txt  include  iso-swid  ivps  lap  lib64  man  msg

The following screencast shows an example of linking two libraries into
a simple program on Summit. https://vimeo.com/292015868

Running Jobs
============

As is the case on other OLCF systems, computational work on Summit is
performed within jobs. A typical job consists of several components:

-  A submission script
-  An executable
-  Input files needed by the executable
-  Output files created by the executable

In general, the process for running a job is to:

#. Prepare executables and input files
#. Write the batch script
#. Submit the batch script
#. Monitor the job's progress before and during execution

The following sections will provide more information regarding running
jobs on Summit. Summit uses IBM Spectrum Load Sharing Facility (LSF) as
the batch scheduling system.

Login, Launch, and Compute Nodes
--------------------------------

Recall from the `System
Overview </for-users/system-user-guides/summit/system-overview/>`__
section that Summit has three types of nodes: login, launch, and
compute. When you log into the system, you are placed on a login node.
When your `batch scripts <#batch-scripts>`__ or `interactive
jobs <#interactive-jobs>`__ run, the resulting shell will run on a
launch node. Compute nodes are accessed via the ``jsrun`` command. The
``jsrun`` command should only be issued from within an LSF job (either
batch or interactive) on a launch node. Othewise, you will not have any
compute nodes allocated and your parallel job will run on the login
node. If this happens, your job will interfere with (and be interfered
with by) other users' login node tasks.

Batch Scripts
-------------

The most common way to interact with the batch system is via batch jobs.
A batch job is simply a shell script with added directives to request
various resources from or provide certain information to the batch
scheduling system. Aside from the lines containing LSF options, the
batch script is simply the series commands needed to set up and run your
job. To submit a batch script, use the bsub command: ``bsub myjob.lsf``

If you’ve previously used LSF, you’re probably used to submitting a job
with input redirection (i.e. ``bsub < myjob.lsf``). This is not needed
(and will not work) on Summit.

As an example, consider the following batch script:

.. code::

    1.   #!/bin/bash
    2.  # Begin LSF Directives
    3.  #BSUB -P ABC123
    4.  #BSUB -W 3:00
    5.  #BSUB -nnodes 2048
    6.  #BSUB -alloc_flags gpumps
    7.  #BSUB -J RunSim123
    8.  #BSUB -o RunSim123.%J
    9.  #BSUB -e RunSim123.%J
    10.
    11. cd $MEMBERWORK/abc123
    12. cp $PROJWORK/abc123/RunData/Input.123 ./Input.123
    13. date
    14. jsrun -n 4092 -r 2 -a 12 -g 3 ./a.out
    15. cp my_output_file /ccs/proj/abc123/Output.123

+----------+------------+--------------------------------------------------------------------------------------------+
| Line #   | Option     | Description                                                                                |
+==========+============+============================================================================================+
| 1        |            | Shell specification. This script will run under with bash as the shell                     |
+----------+------------+--------------------------------------------------------------------------------------------+
| 2        |            | Comment line                                                                               |
+----------+------------+--------------------------------------------------------------------------------------------+
| 3        | Required   | This job will charge to the ABC123 project                                                 |
+----------+------------+--------------------------------------------------------------------------------------------+
| 4        | Required   | Maximum walltime for the job is 3 hours                                                    |
+----------+------------+--------------------------------------------------------------------------------------------+
| 5        | Required   | The job will use 2,048 nodes                                                               |
+----------+------------+--------------------------------------------------------------------------------------------+
| 6        | Optional   | Enable GPU Multi-Process Service                                                           |
+----------+------------+--------------------------------------------------------------------------------------------+
| 7        | Optional   | The name of the job is RunSim123                                                           |
+----------+------------+--------------------------------------------------------------------------------------------+
| 8        | Optional   | Write standard output to a file named RunSim123.#, where # is the job ID assigned by LSF   |
+----------+------------+--------------------------------------------------------------------------------------------+
| 9        | Optional   | Write standard error to a file named RunSim123.#, where # is the job ID assigned by LSF    |
+----------+------------+--------------------------------------------------------------------------------------------+
| 10       | -          | Blank line                                                                                 |
+----------+------------+--------------------------------------------------------------------------------------------+
| 11       | -          | Change into one of the scratch filesystems                                                 |
+----------+------------+--------------------------------------------------------------------------------------------+
| 12       | -          | Copy input files into place                                                                |
+----------+------------+--------------------------------------------------------------------------------------------+
| 13       | -          | Run the ``date`` command to write a timestamp to the standard output file                  |
+----------+------------+--------------------------------------------------------------------------------------------+
| 14       | -          | Run the executable                                                                         |
+----------+------------+--------------------------------------------------------------------------------------------+
| 15       | -          | Copy output files from the scratch area into a more permanent location                     |
+----------+------------+--------------------------------------------------------------------------------------------+

Interactive Jobs
----------------

Most users will find batch jobs to be the easiest way to interact with
the system, since they permit you to hand off a job to the scheduler and
then work on other tasks; however, it is sometimes preferable to run
interactively on the system. This is especially true when developing,
modifying, or debugging a code. Since all compute resources are
managed/scheduled by LSF, it is not possible to simply log into the
system and begin running a parallel code interactively. You must request
the appropriate resources from the system and, if necessary, wait until
they are available. This is done with an “interactive batch” job.
Interactive batch jobs are submitted via the command line, which
supports the same options that are passed via ``#BSUB`` parameters in a
batch script. The final options on the command line are what makes the
job “interactive batch”: ``-Is`` followed by a shell name. For example,
to request an interactive batch job (with bash as the shell) equivalent
to the sample batch script above, you would use the command:
``bsub -W 3:00 -nnodes 2048 -P ABC123 -Is /bin/bash``

Common bsub Options
-------------------

The table below summarizes options for submitted jobs. Unless otherwise
noted, these can be used from batch scripts or interactive jobs. For
interactive jobs, the options are simply added to the ``bsub`` command
line. For batch scripts, they can either be added on the ``bsub``
command line or they can appear as a ``#BSUB`` directive in the batch
script. If conflicting options are specified (i.e. different walltime
specified on the command line versus in the script), the option on the
command line takes precedence. Note that LSF has numerous options; only
the most common ones are described here. For more in-depth information
about other LSF options, see the
`documentation <#for-more-information>`__.

+--------------------+----------------------------------------+----------------------------------------------------------------------------------+
| Option             | Example Usage                          | Description                                                                      |
+====================+========================================+==================================================================================+
| ``-W``             | ``#BSUB -W 50``                        | Requested                                                                        |
|                    |                                        | maximum walltime. NOTE: The format is [hours:]minutes, not                       |
|                    |                                        | [[hours:]minutes:]seconds like PBS/Torque/Moab                                   |
+--------------------+----------------------------------------+----------------------------------------------------------------------------------+
| ``-nnodes``        | ``#BSUB -nnodes 1024``                 | Number of nodes                                                                  |
|                    |                                        | NOTE: There is specified with only one hyphen (i.e. -nnodes, not --nnodes)       |
+--------------------+----------------------------------------+----------------------------------------------------------------------------------+
| ``-P``             | ``#BSUB -P ABC123``                    | Specifies the                                                                    |
|                    |                                        | project to which the job should be charged                                       |
+--------------------+----------------------------------------+----------------------------------------------------------------------------------+
| ``-o``             | ``#BSUB -o jobout.%J``                 | File into which                                                                  |
|                    |                                        | job STDOUT should be directed (%J will be replaced with the job ID number) If    |
|                    |                                        | you do not also specify a STDERR file with ``-e`` or ``-eo``, STDERR will also   |
|                    |                                        | be written to this file.                                                         |
+--------------------+----------------------------------------+----------------------------------------------------------------------------------+
| ``-e``             | ``#BSUB -e jobout.%J``                 | File into which                                                                  |
|                    |                                        | job STDERR should be directed (%J will be replaced with the job ID number)       |
+--------------------+----------------------------------------+----------------------------------------------------------------------------------+
| ``-J``             | ``#BSUB -J MyRun123``                  | Specifies the                                                                    |
|                    |                                        | name of the job (if not present, LSF will use the name of the job script as the  |
|                    |                                        | job’s name)                                                                      |
+--------------------+----------------------------------------+----------------------------------------------------------------------------------+
| ``-w``             | ``#BSUB -w ended()``                   | Place a dependency on the job                                                    |
+--------------------+----------------------------------------+----------------------------------------------------------------------------------+
| ``-N``             | ``#BSUB -N``                           | Send a job report via email when the job completes                               |
+--------------------+----------------------------------------+----------------------------------------------------------------------------------+
| ``-XF``            | ``#BSUB -XF``                          | Use X11 forwarding                                                               |
+--------------------+----------------------------------------+----------------------------------------------------------------------------------+
| ``-alloc_flags``   | ``#BSUB -alloc_flags "gpumps smt1"``   | Used to request                                                                  |
|                    |                                        | GPU Multi-Process Service (MPS) and to set SMT (Simultaneous Multithreading)     |
|                    |                                        | levels. Only one "#BSUB alloc\_flags" command is recognized so multiple          |
|                    |                                        | alloc\_flags options need to be enclosed in quotes and space-separated. Setting  |
|                    |                                        | gpumps enables NVIDIA’s Multi-Process Service, which allows multiple MPI ranks   |
|                    |                                        | to simultaneously access a GPU. Setting smt\ *n* (where *n* is 1, 2, or 4) sets  |
|                    |                                        | different SMT levels. To run with 2 hardware threads per physical core, you’d    |
|                    |                                        | use smt2. The default level is smt4.                                             |
+--------------------+----------------------------------------+----------------------------------------------------------------------------------+

Batch Environment Variables
---------------------------

LSF provides a number of environment variables in your job’s shell
environment. Many job parameters are stored in environment variables and
can be queried within the batch job. Several of these variables are
summarized in the table below. This is not an all-inclusive list of
variables available to your batch job; in particular only LSF variables
are discussed, not the many “standard” environment variables that will
be available (such as ``$PATH``).

+-----------------------+------------------------------------------------------+
| Variable              | Description                                          |
+=======================+======================================================+
| ``LSB_JOBID``         | The ID assigned to the job by LSF                    |
+-----------------------+------------------------------------------------------+
| ``LS_JOBPID``         | The job’s process ID                                 |
+-----------------------+------------------------------------------------------+
| ``LSB_JOBINDEX``      | The job’s index (if it belongs to a job array)       |
+-----------------------+------------------------------------------------------+
| ``LSB_HOSTS``         | The hosts assigned to run the job                    |
+-----------------------+------------------------------------------------------+
| ``LSB_QUEUE``         | The queue from which the job was dispatched          |
+-----------------------+------------------------------------------------------+
| ``LSB_INTERACTIVE``   | Set to “Y” for an interactive job; otherwise unset   |
+-----------------------+------------------------------------------------------+
| ``LS_SUBCWD``         | The directory from which the job was submitted       |
+-----------------------+------------------------------------------------------+

Job States
----------

A job will progress through a number of states through its lifetime. The
states you’re most likely to see are:

+---------+-----------------------------------------------------------------------------+
| State   | Description                                                                 |
+=========+=============================================================================+
| PEND    | Job is pending                                                              |
+---------+-----------------------------------------------------------------------------+
| RUN     | Job is running                                                              |
+---------+-----------------------------------------------------------------------------+
| DONE    | Job completed normally (with an exit code of 0)                             |
+---------+-----------------------------------------------------------------------------+
| EXIT    | Job completed abnormally                                                    |
+---------+-----------------------------------------------------------------------------+
| PSUSP   | Job was suspended (either by the user or an administrator) while pending    |
+---------+-----------------------------------------------------------------------------+
| USUSP   | Job was suspended (either by the user or an administrator) after starting   |
+---------+-----------------------------------------------------------------------------+
| SSUSP   | Job was suspended by the system after starting                              |
+---------+-----------------------------------------------------------------------------+

Scheduling Policy
-----------------

In a simple batch queue system, jobs run in a first-in, first-out (FIFO)
order. This often does not make effective use of the system. A large job
may be next in line to run. If the system is using a strict FIFO queue,
many processors sit idle while the large job waits to run. *Backfilling*
would allow smaller, shorter jobs to use those otherwise idle resources,
and with the proper algorithm, the start time of the large job would not
be delayed. While this does make more effective use of the system, it
indirectly encourages the submission of smaller jobs.

The DOE Leadership-Class Job Mandate
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As a DOE Leadership Computing Facility, the OLCF has a mandate that a
large portion of Summit's usage come from large, *leadership-class* (aka
*capability*) jobs. To ensure the OLCF complies with DOE directives, we
strongly encourage users to run jobs on Summit that are as large as
their code will warrant. To that end, the OLCF implements queue policies
that enable large jobs to run in a timely fashion.

    **Note:** The OLCF implements queue policies that encourage the
    submission and timely execution of large, leadership-class jobs on
    Summit.

The basic priority-setting mechanism for jobs waiting in the queue is
the time a job has been waiting relative to other jobs in the queue. If
your jobs require resources outside these queue policies, please
complete the relevant request form on the `Special
Requests </for-users/getting-started/special-request-form/>`__ page. If
you have any questions or comments on the queue policies below, please
direct them to the User Assistance Center.

Job Priority by Processor Count
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Jobs are *aged* according to the job's requested processor count (older
age equals higher queue priority). Each job's requested processor count
places it into a specific *bin*. Each bin has a different aging
parameter, which all jobs in the bin receive.

+-------+-------------+-------------+------------------------+----------------------+
| Bin   | Min Nodes   | Max Nodes   | Max Walltime (Hours)   | Aging Boost (Days)   |
+=======+=============+=============+========================+======================+
| 1     | 2,765       | 4,608       | 24.0                   | 15                   |
+-------+-------------+-------------+------------------------+----------------------+
| 2     | 922         | 2,764       | 24.0                   | 10                   |
+-------+-------------+-------------+------------------------+----------------------+
| 3     | 92          | 921         | 12.0                   | 0                    |
+-------+-------------+-------------+------------------------+----------------------+
| 4     | 46          | 91          | 6.0                    | 0                    |
+-------+-------------+-------------+------------------------+----------------------+
| 5     | 1           | 45          | 2.0                    | 0                    |
+-------+-------------+-------------+------------------------+----------------------+

``batch`` Queue Policy
"""""""""""""""""""""""

The ``batch`` queue is the default queue for production work on Summit.
Most work on Summit is handled through this queue. It enforces the
following policies:

-  Limit of (4) *eligible-to-run* jobs per user.
-  Jobs in excess of the per user limit above will be placed into a
   *held* state, but will change to eligible-to-run at the appropriate
   time.
-  Users may have only (100) jobs queued at any state at any time.
   Additional jobs will be rejected at submit time.

    **Note:** The *eligible-to-run* state is not the *running* state.
    Eligible-to-run jobs have not started and are waiting for resources.
    Running jobs are actually executing.

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
Additionally, projects that are at 125% of their allocated time will be
limited to only one running job at a time. The adjustment to the
apparent submit time depends upon the percentage that the project is
over its allocation, as shown in the table below:

+------------------------+----------------------+
| % Of Allocation Used   | Priority Reduction   |
+========================+======================+
| < 100%                 | 0 days               |
+------------------------+----------------------+
| 100% to 125%           | 30 days              |
+------------------------+----------------------+
| > 125%                 | 365 days             |
+------------------------+----------------------+

System Reservation Policy
^^^^^^^^^^^^^^^^^^^^^^^^^

Projects may request to reserve a set of processors for a period of time
through the reservation request form, which can be found on the `Special
Requests <http://www.olcf.ornl.gov/support/getting-started/special-request-form/>`__
page. If the reservation is granted, the reserved processors will be
blocked from general use for a given period of time. Only users that
have been authorized to use the reservation can utilize those resources.
Since no other users can access the reserved resources, it is crucial
that groups given reservations take care to ensure the utilization on
those resources remains high. To prevent reserved resources from
remaining idle for an extended period of time, reservations are
monitored for inactivity. If activity falls below 50% of the reserved
resources for more than (30) minutes, the reservation will be canceled
and the system will be returned to normal scheduling. A new reservation
must be requested if this occurs. The requesting project's allocation is
charged according to the time window granted, regardless of actually
utilization. For example, an 8-hour, 2,000 node reservation on Summit
would be equivalent to using 16,000 Summit node-hours of a project's
allocation.

--------------

Job Dependencies
----------------

As is the case with many other queuing systems, it is possible to place
dependencies on jobs to prevent them from running until other jobs have
started/completed/etc. Several possible dependency settings are
described in the table below:

+-----------------------------------------------+---------------------------------------------------------------------------------+
| Expression                                    | Meaning                                                                         |
+===============================================+=================================================================================+
| ``#BSUB -w started(12345)``                   | The job will not start until                                                    |
|                                               | job 12345 starts. Job 12345 is considered to have started if is in any of the   |
|                                               | following states: USUSP, SSUSP, DONE, EXIT or RUN (with any pre-execution       |
|                                               | command specified by ``bsub -E`` completed)                                     |
+-----------------------------------------------+---------------------------------------------------------------------------------+
| ``#BSUB -w done(12345)`` ``#BSUB -w 12345``   | The job will not start until                                                    |
|                                               | job 12345 has a state of DONE (i.e. completed normally). If a job ID is given   |
|                                               | with no condition, ``done()`` is assumed.                                       |
+-----------------------------------------------+---------------------------------------------------------------------------------+
| ``#BSUB -w exit(12345)``                      | The job will not start until                                                    |
|                                               | job 12345 has a state of EXIT (i.e. completed abnormally)                       |
+-----------------------------------------------+---------------------------------------------------------------------------------+
| ``#BSUB -w ended(12345)``                     | The job will not start until                                                    |
|                                               | job 12345 has a state of EXIT or DONE                                           |
+-----------------------------------------------+---------------------------------------------------------------------------------+

Dependency expressions can be combined with logical operators. For
example, if you want a job held until job 12345 is DONE and job 12346
has started, you can use ``#BSUB -w "done(12345) && started(12346)"``

Monitoring Jobs
---------------

LSF provides several utilities with which you can monitor jobs. These
include monitoring the queue, getting details about a particular job,
viewing STDOUT/STDERR of running jobs, and more. The most
straightforward monitoring is with the ``bjobs`` command. This command
will show the current queue, including both pending and running jobs.
Running ``bjobs -l`` will provide much more detail about a job (or group
of jobs). For detailed output of a single job, specify the job id after
the ``-l``. For example, for detailed output of job 12345, you can run
``bjobs -l 12345`` . Other options to ``bjobs`` are shown below. In
general, if the command is specified with ``-u all`` it will show
information for all users/all jobs. Without that option, it only shows
your jobs. Note that this is not an exhaustive list. See ``man bjobs``
for more information.

+-----------------------+--------------------------------------------------------------------------------+
| Command               | Description                                                                    |
+=======================+================================================================================+
| ``bjobs``             | Show your current jobs in the queue                                            |
+-----------------------+--------------------------------------------------------------------------------+
| ``bjobs -u all``      | Show currently queued jobs for all users                                       |
+-----------------------+--------------------------------------------------------------------------------+
| ``bjobs -P ABC123``   | Shows currently-queued jobs for project ABC123                                 |
+-----------------------+--------------------------------------------------------------------------------+
| ``bjobs -UF``         | Don't format output (might be useful if you're using the output in a script)   |
+-----------------------+--------------------------------------------------------------------------------+
| ``bjobs -a``          | Show jobs in all states, including recently finished jobs                      |
+-----------------------+--------------------------------------------------------------------------------+
| ``bjobs -l``          | Show long/detailed output                                                      |
+-----------------------+--------------------------------------------------------------------------------+
| ``bjobs -l 12345``    | Show long/detailed output for jobs 12345                                       |
+-----------------------+--------------------------------------------------------------------------------+
| ``bjobs -d``          | Show details for recently completed jobs                                       |
+-----------------------+--------------------------------------------------------------------------------+
| ``bjobs -s``          | Show suspended jobs, including the reason(s) they're suspended                 |
+-----------------------+--------------------------------------------------------------------------------+
| ``bjobs -r``          | Show running jobs                                                              |
+-----------------------+--------------------------------------------------------------------------------+
| ``bjobs -p``          | Show pending jobs                                                              |
+-----------------------+--------------------------------------------------------------------------------+
| ``bjobs -w``          | Use "wide" formatting for output                                               |
+-----------------------+--------------------------------------------------------------------------------+

If you want to check the STDOUT/STDERR of a currently running job, you
can do so with the ``bpeek`` command. The command supports several
options:

+------------------------+---------------------------------------------------------------------------------------------+
| Command                | Description                                                                                 |
+========================+=============================================================================================+
| ``bpeek -J jobname``   | Show STDOUT/STDERR for the job you've most recently submitted with the name jobname         |
+------------------------+---------------------------------------------------------------------------------------------+
| ``bpeek 12345``        | Show STDOUT/STDERR for job 12345                                                            |
+------------------------+---------------------------------------------------------------------------------------------+
| ``bpeek -f ...``       | Used with other options. Makes ``bpeek`` use ``tail -f`` and exit once the job completes.   |
+------------------------+---------------------------------------------------------------------------------------------+

The OLCF also provides ``jobstat``, which adds dividers in the queue to
identify jobs as running, eligible, or blocked. Run without arguments,
``jobstat`` provides a snapshot of the entire batch queue. Additional
information, including the number of jobs in each state, total nodes
available, and relative job priority are also included.
``jobstat -u <username>`` restricts output to only the jobs of a
specific user. See the ``jobstat`` man page for a full list of
formatting arguments.

::

    $ jobstat -u <user>
    --------------------------- Running Jobs: 2 (4544 of 4604 nodes, 98.70%) ---------------------------
    JobId    Username   Project          Nodes Remain     StartTime       JobName
    331590   user     project           2     57:06      04/09 10:06:23  Not_Specified
    331707   user     project           40    39:47      04/09 11:04:04  runA
    ----------------------------------------- Eligible Jobs: 3 -----------------------------------------
    JobId    Username   Project          Nodes Walltime   QueueTime       Priority JobName
    331712   user     project           80    45:00      04/09 11:06:23  501.00   runB
    331713   user     project           90    45:00      04/09 11:07:19  501.00   runC
    331714   user     project           100   45:00      04/09 11:07:49  501.00   runD
    ----------------------------------------- Blocked Jobs: 1 ------------------------------------------
    JobId    Username   Project          Nodes Walltime   BlockReason
    331715   user        project           12    2:00:00    Job dependency condition not satisfied

Inspecting Backfill
^^^^^^^^^^^^^^^^^^^

``bjobs`` and ``jobstat`` help to identify what’s currently running and
scheduled to run, but sometimes it’s beneficial to know how much of the
system is *not* currently in use or scheduled for use. The ``bslots``
command can be used to inspect backfill windows and answer the question
“How many nodes are currently available, and for how long will they
remain available?” This can be thought of as identifying gaps in the
system’s current job schedule. By intentionally requesting resources
within the parameters of a backfill window, one can potentially shorten
their queued time and improve overall system utilization. LSF uses
“slots” to describe allocatable resources. Summit compute nodes have 1
slot per CPU core, for a total of 42 per node ([2x] Power9 CPUs, each
with 21 cores). Since Summit nodes are scheduled in whole-node
allocations, the output from ``bslots`` can be divided by 42 to see how
many nodes are currently available. By default, ``bslots`` output
includes launch node slots, which can cause unwanted and inflated
fractional node values. The output can be adjusted to reflect only
available compute node slots with the flag ``-R”select[CN]”``. For
example,

::

    $ bslots -R"select[CN]"
    SLOTS          RUNTIME
    42             25 hours 42 minutes 51 seconds
    27384          1 hours 11 minutes 50 seconds

27384 compute node slots / 42 slots per node = 652 compute nodes are
available for 1 hour, 11 minutes, 50 seconds. A more specific ``bslots``
query could check for a backfill window with space to fit a 1000 node
job for 10 minutes:

::

    $ bslots -R"select[CN]" -n $((1000*42)) -W10
    SLOTS          RUNTIME
    127764         22 minutes 55 seconds

There is no guarantee that the slots reported by ``bslots`` will still
be available at time of new job submission.

Interacting With Jobs
---------------------

Sometimes it’s necessary to interact with a batch job after it has been
submitted. LSF provides several commands for interacting with
already-submitted jobs.

Many of these commands can operate on either one job or a group of jobs.
In general, they only operate on the most recently submitted job that
matches other criteria provided unless “0” is specified as the job id.

Suspending and Resuming Jobs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

LSF supports user-level suspension and resumption of jobs. Jobs are
suspended with the ``bstop`` command and resumed with the ``bresume``
command. The simplest way to invoke these commands is to list the job id
to be suspended/resumed:

.. code::

    bstop 12345
    bresume 12345

Instead of specifying a job id, you can specify other criteria that will
allow you to suspend some/all jobs that meet other criteria such as a
job name, a queue name, etc. These are described in the manpages for
``bstop`` and ``bresume``.

Signaling Jobs
^^^^^^^^^^^^^^

You can send signals to jobs with the ``bkill`` command. While the
command name suggests its only purpose is to terminate jobs, this is not
the case. Similar to the ``kill`` command found in Unix-like operating
systems, this command can be used to send various signals (not just
``SIGTERM`` and ``SIGKILL``) to jobs. The command can accept both
numbers and names for signals. For a list of accepted signal names, run
``bkill -l``. Common ways to invoke the command include:

+---------------------------+----------------------------------------------------------------------------------+
| Command                   | Description                                                                      |
+===========================+==================================================================================+
| ``bkill 12345``           | Force a job to stop by sending ``SIGINT``,                                       |
|                           | ``SIGTERM``, and ``SIGKILL``. These signals are sent in that order, so users     |
|                           | can write applications such that they will trap ``SIGINT`` and/or ``SIGTERM``    |
|                           | and exit in a controlled manner.                                                 |
+---------------------------+----------------------------------------------------------------------------------+
| ``bkill -s USR1 12345``   | Send ``SIGUSR1`` to job 12345 NOTE: When                                         |
|                           | specifying a signal by name, omit SIG from the name. Thus, you specify ``USR1``  |
|                           | and not ``SIGUSR1`` on the ``bkill`` command line.                               |
+---------------------------+----------------------------------------------------------------------------------+
| ``bkill -s 9 12345``      | Send signal 9 to job 12345                                                       |
+---------------------------+----------------------------------------------------------------------------------+

Like ``bstop`` and ``bresume``, ``bkill`` command also supports
identifying the job(s) to be signaled by criteria other than the job id.
These include some/all jobs with a given name, in a particular queue,
etc. See ``man bkill`` for more information.

Checkpointing Jobs
^^^^^^^^^^^^^^^^^^

LSF documentation mentions the ``bchkpnt`` and ``brestart`` commands for
checkpointing and restarting jobs, as well as the ``-k`` option to
``bsub`` for configuring checkpointing. Since checkpointing is very
application specific and a wide range of applications run on OLCF
resources, this type of checkpointing is not configured on Summit. If
you wish to use checkpointing (which is highly encouraged), you’ll need
to configure it within your application. If you wish to implement some
form of on-demand checkpointing, keep in mind the ``bkill`` command is
really a signaling command and you can have your job script/application
checkpoint as a response to certain signals (such as ``SIGUSR1``).

Other LSF Commands
------------------

The table below summarizes some additional LSF commands that might be
useful.

+------------------+---------------------------------------------------------------------------+
| Command          | Description                                                               |
+==================+===========================================================================+
| ``bparams -a``   | Show current parameters for LSF The behavior/available                    |
|                  | options for some LSF commands depend on settings in various configuration |
|                  | files. This command shows those settings without having to search for the |
|                  | actual files.                                                             |
+------------------+---------------------------------------------------------------------------+
| ``bjdepinfo``    | Show job dependency information (could be useful in                       |
|                  | determining what job is keeping another job in a pending state)           |
+------------------+---------------------------------------------------------------------------+

PBS/Torque/MOAB-to-LSF Translation
----------------------------------

More details about these commands are given elsewhere in this section;
the table below is simply for your convenience in looking up various LSF
commands. Users of other OLCF resources are likely familiar with
PBS-like commands which are used by the Torque/Moab instances on other
systems. The table below summarizes the equivalent LSF command for
various PBS/Torque/Moab commands.

+--------------------------+----------------------------------+----------------------------------------------------+
| LSF Command              | PBS/Torque/Moab Command          | Description                                        |
+==========================+==================================+====================================================+
| ``bsub job.sh``          | ``qsub job.sh``                  | Submit the job script job.sh to the batch system   |
+--------------------------+----------------------------------+----------------------------------------------------+
| ``bsub -Is /bin/bash``   | ``qsub -I``                      | Submit an interactive batch job                    |
+--------------------------+----------------------------------+----------------------------------------------------+
| ``bjobs -u all``         | ``qstat showq``                  | Show jobs currently in the queue NOTE: without the |
|                          |                                  | -u all argument, bjobs will only show your jobs    |
+--------------------------+----------------------------------+----------------------------------------------------+
| ``bjobs -l``             | ``checkjob``                     | Get information about a specific job               |
+--------------------------+----------------------------------+----------------------------------------------------+
| ``bjobs -d``             | ``showq -c``                     | Get information about completed jobs               |
+--------------------------+----------------------------------+----------------------------------------------------+
| ``bjobs -p``             | ``showq -i showq -b checkjob``   | Get information about pending jobs                 |
+--------------------------+----------------------------------+----------------------------------------------------+
| ``bjobs -r``             | ``showq -r``                     | Get information about running jobs                 |
+--------------------------+----------------------------------+----------------------------------------------------+
| ``bkill``                | ``qsig``                         | Send a signal to a job                             |
+--------------------------+----------------------------------+----------------------------------------------------+
| ``bkill``                | ``qdel``                         | Terminate/Kill a job                               |
+--------------------------+----------------------------------+----------------------------------------------------+
| ``bstop``                | ``qhold``                        | Hold a job/stop a job from running                 |
+--------------------------+----------------------------------+----------------------------------------------------+
| ``bresume``              | ``qrls``                         | Release a held job                                 |
+--------------------------+----------------------------------+----------------------------------------------------+
| ``bqueues``              | ``qstat -q``                     | Get information about queues                       |
+--------------------------+----------------------------------+----------------------------------------------------+
| ``bjdepinfo``            | ``checkjob``                     | Get information about job dependencies             |
+--------------------------+----------------------------------+----------------------------------------------------+

The table below shows shows LSF (bsub) command-line/batch script options
and the PBS/Torque/Moab (qsub) options that provide similar
functionality.

+---------------------------------+------------------------------------------------+------------------------------------------------------------+
| LSF Option                      | PBS/Torque/Moab Option                         | Description                                                |
+=================================+================================================+============================================================+
| ``#BSUB -W 60``                 | ``#PBS -l walltime=1:00:00``                   | Request a walltime of 1 hour                               |
+---------------------------------+------------------------------------------------+------------------------------------------------------------+
| ``#BSUB -nnodes 1024``          | ``#PBS -l nodes=1024``                         | Request 1024 nodes                                         |
+---------------------------------+------------------------------------------------+------------------------------------------------------------+
| ``#BSUB -P ABC123``             | ``#PBS -A ABC123``                             | Charge the job to project ABC123                           |
+---------------------------------+------------------------------------------------+------------------------------------------------------------+
| ``#BSUB -alloc_flags gpumps``   | No equivalent (set via environment variable)   | Enable multiple MPI tasks to simultaneously access a GPU   |
+---------------------------------+------------------------------------------------+------------------------------------------------------------+

Easy Mode vs. Expert Mode
-------------------------

The Cluster System Management (CSM) component of the job launch
environment supports two methods of job submission, termed “easy” mode
and “expert” mode. The difference in the modes is where the
responsibility for creating the LSF resource string is placed. In easy
mode, the system software converts options such as -nnodes in a batch
script into the resource string needed by the scheduling system. In
expert mode, the user is responsible for creating this string and
options such as -nnodes cannot be used. In easy mode, you will not be
able to use ``bsub -R`` to create resource strings. The system will
automatically create the resource string based on your other ``bsub``
options. In expert mode, you will be able to use ``-R``, but you will
not be able to use the following options to ``bsub``: ``-ln_slots``,
``-ln_mem``, ``-cn_cu``, or ``-nnodes``. Most users will want to use
easy mode. However, if you need precise control over your job’s
resources, such as placement on (or avoidance of) specific nodes, you
will need to use expert mode. To use expert mode, add ``#BSUB -csm y``
to your batch script (or ``-csm y`` to your ``bsub`` command line).

Hardware Threads
----------------

Hardware threads are a feature of the POWER9 processor through which
individual physical cores can support multiple execution streams,
essentially looking like one or more virtual cores (similar to
hyperthreading on some Intel® microprocessors). This feature is often
called Simultaneous Multithreading or SMT. The POWER9 processor on
Summit supports SMT levels of 1, 2, or 4, meaning (respectively) each
physical core looks like 1, 2, or 4 virtual cores. The SMT level is
controlled by the ``-alloc_flags`` option to ``bsub``. For example, to
set the SMT level to 2, add the line ``#BSUB –alloc_flags smt2`` to your
batch script or add the option ``-alloc_flags smt2`` to you ``bsub``
command line.

The default SMT level is 4.

System Service Core Isolation
-----------------------------

One core per socket is set aside for system service tasks. The cores are
not available to jsrun. When listing available resources through jsrun,
you will not see cores with hyperthreads 84-87 and 172-175. Isolating a
socket's system services to a single core helps to reduce jitter and
improve performance of tasks performed on the socket's remaining cores.
The isolated core always operates at SMT4 regardless of the batch job's
SMT level.

GPFS System Service Isolation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, GPFS system service tasks are forced onto only the isolated
cores. This can be overridden at the batch job level using the
``maximizegpfs`` argument to LSF's ``alloc_flags``. For example:

::

     #BSUB -alloc_flags maximizegpfs

The maximizegpfs flag will allow GPFS tasks to utilize any core on the
compute node. This may be beneficial because it provides more resources
for GPFS service tasks, but it may also cause resource contention for
the jsrun compute job.

MPS
---

The Multi-Process Service (MPS) enables multiple processes (e.g. MPI
ranks) to concurrently share the resources on a single GPU. This is
accomplished by starting an MPS server process, which funnels the work
from multiple CUDA contexts (e.g. from multiple MPI ranks) into a single
CUDA context. In some cases, this can increase performance due to better
utilization of the resources. As mentioned in the `COMMON BSUB
OPTIONS <https://www.olcf.ornl.gov/for-users/system-user-guides/summit/running-jobs/#common-bsub-options>`__
section above, MPS can be enabled with the ``-alloc_flags "gpumps"``
option to bsub. The screencast below shows an example of how to start an
MPS server process for a job. https://vimeo.com/292016149

Resource Accounting
-------------------

While logged into Summit, users can show their YTD usage and allocation
by project using the ``showusage`` command. System specific details can
be obtained with the ``-s`` flag. For example,

.. code::

    $ showusage -s summit

    summit usage for the project's current allocation period:
                                      Project Totals          [USERID]
     Project      Allocation        Usage    Remaining          Usage
    __________________________|____________________________|_____________
     [PROJID1]        50000   |      15728        34272    |         65
     [PROJID2]        20000   |       1234        18766    |          0

For additional details, please see the help message printed when using
the ``-h`` flag:

.. code::

     $ showusage -h

Other Notes
-----------

Compute nodes are only allocated to one job at a time; they are not
shared. This is why users request nodes (instead of some other resource
such as cores or GPUs) in batch jobs and is why projects are charged
based on the number of nodes allocated multiplied by the amount of time
for which they were allocated. Thus, a job using only 1 core on each of
its nodes is charged the same as a job using every core and every GPU on
each of its nodes.

Job Launcher (jsrun)
--------------------

The default job launcher for Summit is ``jsrun``. jsrun was developed by
IBM for the Oak Ridge and Livermore Power systems. The tool will execute
a given program on resources allocated through the LSF batch scheduler;
similar to ``mpirun`` and ``aprun`` functionality.

Compute Node Description
^^^^^^^^^^^^^^^^^^^^^^^^

The following compute node image will be used to discuss jsrun resource
sets and layout.


.. image:: /images/summit-node-description-1.png
   :class: normal aligncenter wp-image-775250
   :width: 85%
   :align: center

-  1 node
-  2 sockets (grey)
-  42 physical cores\* (dark blue)
-  168 hardware cores (light blue)
-  6 GPUs (orange)
-  2 Memory blocks (yellow)

**\*Core Isolation:** 1 core on each socket has been set aside for
overhead and is not available for allocation through jsrun. The core has
been omitted and is not shown in the above image.

Resource Sets
^^^^^^^^^^^^^

While jsrun performs similar job launching functions as aprun and
mpirun, its syntax is very different. A large reason for syntax
differences is the introduction of the ``resource set`` concept. Through
resource sets, jsrun can control how a node appears to each job. Users
can, through jsrun command line flags, control which resources on a node
are visible to a job. Resource sets also allow the ability to run
multiple jsruns simultaneously within a node. Under the covers, a
resource set is a cgroup.

At a high level, a resource set allows users to configure what a node
look like to their job.

Jsrun will create one or more resource sets within a node. Each resource
set will contain 1 or more cores and 0 or more GPUs. A resource set can
span sockets, but it may not span a node. While a resource set can span
sockets within a node, consideration should be given to the cost of
cross-socket communication. By creating resource sets only within
sockets, costly communication between sockets can be prevented.

One or more resource sets can be created on a single node and can span
sockets. But, a resource set can not span nodes.

While a resource set can span sockets within a node, consideration
should be given to the cost of cross-socket communication. Creating
resource sets within sockets will prevent cross-socket communication.

Subdividing a Node with Resource Sets
"""""""""""""""""""""""""""""""""""""

Resource sets provides the ability to subdivide node’s resources into
smaller groups. The following examples show how a node can be subdivided
and how many resource set could fit on a node.

.. image:: /images/summit-resource-set-subdivide.png
   :class: normal aligncenter size-full wp-image-775849
   :width: 600px
   :height: 360px
   :align: center

Multiple Methods to Creating Resource Sets
""""""""""""""""""""""""""""""""""""""""""

Resource sets should be created to fit code requirements. The following
examples show multiple ways to create resource sets that allow two MPI
tasks access to a single GPU.

#. 6 resource sets per node: 1 GPU, 2 cores per (Titan)

   .. image:: https://www.olcf.ornl.gov/wp-content/uploads/2018/03/RS-summit-example-1GPU-2Cores.png
      :class: normal aligncenter size-full wp-image-775999
      :width: 500px
      :height: 300px

   In this case, CPUs can only see single assigned GPU.

#. 2 resource sets per node: 3 GPUs and 6 cores per socket

   .. image:: https://www.olcf.ornl.gov/wp-content/uploads/2018/03/RS-summit-example-3GPU-6Cores.png
      :class: normal aligncenter size-full wp-image-776000
      :width: 600px
      :height: 360px

   In this case, all 6 CPUs can see 3 GPUs. Code must manage CPU -> GPU
   communication. CPUs on socket0 can not access GPUs or Memory on socket1.

#. Single resource set per node: 6 GPUs, 12 cores

   .. image:: https://www.olcf.ornl.gov/wp-content/uploads/2018/03/RS-summit-example-6GPU-12Core.png
      :class: normal aligncenter size-full wp-image-776142
      :width: 600px
      :height: 360px

   In this case, all 12 CPUs can see all node’s 6 GPUs. Code must manage CPU to
   GPU communication. CPUs on socket0 can access GPUs and Memory on socket1.
   Code must manage cross socket communication.

Designing a Resource Set
""""""""""""""""""""""""

Resource sets allow each jsrun to control how the node appears to a
code. This method is unique to jsrun, and requires thinking of each job
launch differently than aprun or mpirun. While the method is unique, the
method is not complicated and can be reasoned in a few basic steps. The
first step to creating resource sets is understanding how a code would
like the node to appear. For example, the number of tasks/threads per
GPU. Once this is understood, the next step is to simply calculate the
number of resource sets that can fit on a node. From here, the number of
needed nodes can be calculated and passed to the batch job request. The
basic steps to creating resource sets:

1) Understand how your code expects to interact with the system.
    How many tasks/threads per GPU?
    Does each task expect to see a single GPU? Do multiple tasks expect
    to share a GPU? Is the code written to internally manage task to GPU
    workload based on the number of available cores and GPUs?
2) Create resource sets containing the needed GPU to task binding
    Based on how your code expects to interact with the system, you can
    create resource sets containing the needed GPU and core resources.
    If a code expects to utilize one GPU per task, a resource set would
    contain one core and one GPU. If a code expects to pass work to a
    single GPU from two tasks, a resource set would contain two cores
    and one GPU.
3) Decide on the number of resource sets needed
    Once you understand tasks, threads, and GPUs in a resource set, you
    simply need to decide the number of resource sets needed.

As on Titan it is useful to keep the general layout of a node in mind
when laying out resource sets.

Launching a Job with jsrun
^^^^^^^^^^^^^^^^^^^^^^^^^^

jsrun Format
""""""""""""

::

      jsrun    [ -n #resource sets ]   [tasks, threads, and GPUs within each resource set]   program [ program args ]

Common jsrun Options
""""""""""""""""""""

Below are common jsrun options. More flags and details can be found in
the jsrun man page.


+---------------------------+--------+------------------------------------------------------+------------------------------+
| Flags                              |                                                      |                              |
+---------------------------+--------+  Description                                         + Default Value                +
| Long                      | Short  |                                                      |                              |
+===========================+========+======================================================+==============================+
| ``--nrs``                 | ``-n`` | Number of resource sets                              | All available physical cores |
+---------------------------+--------+------------------------------------------------------+------------------------------+
| ``--tasks_per_rs``        | ``-a`` | Number of MPI tasks (ranks) per resource set         | Not set by default, instead  |
|                           |        |                                                      | total tasks (-p) set         |
+---------------------------+--------+------------------------------------------------------+------------------------------+
| ``--cpu_per_rs``          | ``-c`` | Number of CPUs (cores) per resource set.             | 1                            |
+---------------------------+--------+------------------------------------------------------+------------------------------+
| ``--gpu_per_rs``          | ``-g`` | Number of GPUs per resource set                      | 0                            |
+---------------------------+--------+------------------------------------------------------+------------------------------+
| ``--bind``                | ``-b`` | Binding of tasks within a resource set. Can be none, | packed:1                     |
|                           |        | rs, or packed:#                                      |                              |
+---------------------------+--------+------------------------------------------------------+------------------------------+
| ``--rs_per_host``         | ``-r`` | Number of resource sets per host                     | No default                   |
+---------------------------+--------+------------------------------------------------------+------------------------------+
| ``--latency_priority``    | ``-l`` | Latency Priority. Controls layout                    | gpu-cpu,cpu-mem,cpu-cpu      |
|                           |        | priorities. Can currently be cpu-cpu or gpu-cpu      |                              |
+---------------------------+--------+------------------------------------------------------+------------------------------+
| ``--launch_distribution`` | ``-d`` | How tasks are started on resource sets               | packed                       |
+---------------------------+--------+------------------------------------------------------+------------------------------+

It's recommended to explicitly specify ``jsrun`` options. This most
often includes ``--nrs``,\ ``--cpu_per_rs``, ``--gpu_per_rs``,
``--tasks_per_rs``, ``--bind``, and ``--launch_distribution``.

Aprun to jsrun
""""""""""""""

Mapping aprun commands used on Titan to Summit's jsrun is only possible
in simple single GPU cases. The following table shows some basic single
GPU examples that could be executed on Titan or Summit. In the single
node examples, each resource set will resemble a Titan node containing a
single GPU and one or more cores. Although not required in each case,
common jsrun flags (resource set count, GPUs per resource set, tasks per
resource set, cores per resource set, binding) are included in each
example for reference. The jsrun ``-n`` flag can be used to increase the
number of resource sets needed. Multiple resource sets can be created on
a single node. If each MPI task requires a single GPU, up to 6 resource
sets could be created on a single node.

+-------------------------+-------------+--------------------+-----------------+-------------------------------------+
| GPUs per Resource Set   | MPI Tasks   | Threads per Task   | aprun           | jsrun                               |
+=========================+=============+====================+=================+=====================================+
| 1                       | 1           | 0                  | aprun -n1       | jsrun -n1 -g1 -a1 -c1               |
+-------------------------+-------------+--------------------+-----------------+-------------------------------------+
| 1                       | 2           | 0                  | aprun -n2       | jsrun -n1 -g1 -a2 -c1               |
+-------------------------+-------------+--------------------+-----------------+-------------------------------------+
| 1                       | 1           | 4                  | aprun -n1 -d4   | jsrun -n1 -g1 -a1 -c4 -bpacked:4    |
+-------------------------+-------------+--------------------+-----------------+-------------------------------------+
| 1                       | 2           | 8                  | aprun -n2 -d8   | jsrun -n1 -g1 -a2 -c16 -bpacked:8   |
+-------------------------+-------------+--------------------+-----------------+-------------------------------------+

The jsrun ``-n`` flag can be used to increase the number of resource
sets needed. Multiple resource sets can be created on a single node. If
each MPI task requires a single GPU, up to 6 resource sets could be
created on a single node.

For cases when the number of tasks per resource set (i.e. the ``-a``
flag) is greater than one, the job must use ``-alloc_flags "gpumps"``.
This allows multiple tasks to share the same GPU.

  The following example images show how a single-gpu/single-task job
would be placed on a single Titan and Summit node. On Summit, the red
box represents a resource set created by jsrun. The resource set looks
similar to a Titan node, containing a single GPU, a single core, and
memory.

+--------------+-------------------------+
| Titan Node   | Summit Node             |
+==============+=========================+
| aprun -n1    | jsrun -n1 -g1 -a1 -c1   |
+--------------+-------------------------+
| |image18|    | |image19|               |
+--------------+-------------------------+

.. |image18| image:: /images/titan-node-1task-1gpu.png
   :class: normal aligncenter
.. |image19| image:: /images/summit-node-1rs-1task-1gpu-example.png
   :class: normal aligncenter

Because Summit's nodes are much larger than Titan's, 6 single-gpu
resource sets can be created on a single Summit node. The following
image shows how six single-gpu, single-task resource sets would be
placed on a node by default. In the example, the command
``jsrun -n6 -g1 -a1 -c1`` is used to create six single-gpu resource sets
on the node. Each resource set is indicated by differing colors. Notice,
the ``-n`` flag is all that changed between the above single resource
set example. The ``-n`` flag tells jsrun to create six resource sets.

.. figure:: https://www.olcf.ornl.gov/wp-content/uploads/2018/03/summit-2node-1taskpergpu.png
   :class: normal aligncenter size-full wp-image-776599
   :width: 1318px
   :height: 520px
 
   ``jsrun -n 6 -g 1 -a 1 -c 1`` starts 6 resource sets, each indicated by
   differing colors.  Each resource contains 1 GPU, 1 Core, and memory.  The
   red resource set contains GPU 0 and Core 0.  The purple resource set
   contains GPU 3 and Core 84.  ``-n 6`` tells jsrun how many resource sets to
   create.  In this example, each resource set is similar to a single Titan
   node.


jsrun Examples
^^^^^^^^^^^^^^

The below examples were launched in the following 2 node interactive
batch job:

::

    summit> bsub -nnodes 2 -Pprj123 -W02:00 -Is $SHELL

Single MPI Task, single GPU per RS
""""""""""""""""""""""""""""""""""

The following example will create 12 resource sets each with 1 MPI task
and 1 GPU. Each MPI task will have access to a single GPU. Rank 0 will
have access to GPU 0 on the first node ( red resource set). Rank 1 will
have access to GPU 1 on the first node ( green resource set). This
pattern will continue until 12 resources sets have been created. The
following jsrun command will request 12 resource sets (``-n12``) 6 per
node (``-r6``). Each resource set will contain 1 MPI task (``-a1``),
1 GPU (``-g1``), and 1 core (``-c1``).

.. image:: /images/summit-jsrun-example-1Core-1GPU.png
   :class: normal aligncenter size-full wp-image-776751
   :width: 600px
   :height: 300px

::

    summit> jsrun -n12 -r6 -a1 -g1 -c1 ./a.out
    Rank:    0; NumRanks: 12; RankCore:   0; Hostname: h41n04; GPU: 0
    Rank:    1; NumRanks: 12; RankCore:   4; Hostname: h41n04; GPU: 1
    Rank:    2; NumRanks: 12; RankCore:   8; Hostname: h41n04; GPU: 2
    Rank:    3; NumRanks: 12; RankCore:  84; Hostname: h41n04; GPU: 3
    Rank:    4; NumRanks: 12; RankCore:  89; Hostname: h41n04; GPU: 4
    Rank:    5; NumRanks: 12; RankCore:  92; Hostname: h41n04; GPU: 5

    Rank:    6; NumRanks: 12; RankCore:   0; Hostname: h41n03; GPU: 0
    Rank:    7; NumRanks: 12; RankCore:   4; Hostname: h41n03; GPU: 1
    Rank:    8; NumRanks: 12; RankCore:   8; Hostname: h41n03; GPU: 2
    Rank:    9; NumRanks: 12; RankCore:  84; Hostname: h41n03; GPU: 3
    Rank:   10; NumRanks: 12; RankCore:  89; Hostname: h41n03; GPU: 4
    Rank:   11; NumRanks: 12; RankCore:  92; Hostname: h41n03; GPU: 5

Multiple tasks, single GPU per RS
"""""""""""""""""""""""""""""""""

The following jsrun command will request 12 resource sets (``-n12``).
Each resource set will contain 2 MPI tasks (``-a2``), 1 GPU
(``-g1``), and 2 cores (``-c2``). 2 MPI tasks will have access to a
single GPU. Ranks 0 - 1 will have access to GPU 0 on the first node (
red resource set). Ranks 2 - 3 will have access to GPU 1 on the first
node ( green resource set). This pattern will continue until 12 resource
sets have been created.

.. image:: /images/summit-jsrun-example-2taskperGPU.png
   :class: normal aligncenter size-full wp-image-777053
   :width: 600px
   :height: 300px

**Adding cores to the RS:** The ``-c`` flag should be used to request
the needed cores for tasks and treads. The default -c core count is 1.
In the above example, if -c is not specified both tasks will run on a
single core.

::

    summit> jsrun -n12 -a2 -g1 -c2 -dpacked ./a.out | sort
    Rank:    0; NumRanks: 24; RankCore:   0; Hostname: a01n05; GPU: 0
    Rank:    1; NumRanks: 24; RankCore:   4; Hostname: a01n05; GPU: 0

    Rank:    2; NumRanks: 24; RankCore:   8; Hostname: a01n05; GPU: 1
    Rank:    3; NumRanks: 24; RankCore:  12; Hostname: a01n05; GPU: 1

    Rank:    4; NumRanks: 24; RankCore:  16; Hostname: a01n05; GPU: 2
    Rank:    5; NumRanks: 24; RankCore:  20; Hostname: a01n05; GPU: 2

    Rank:    6; NumRanks: 24; RankCore:  88; Hostname: a01n05; GPU: 3
    Rank:    7; NumRanks: 24; RankCore:  92; Hostname: a01n05; GPU: 3

    Rank:    8; NumRanks: 24; RankCore:  96; Hostname: a01n05; GPU: 4
    Rank:    9; NumRanks: 24; RankCore: 100; Hostname: a01n05; GPU: 4

    Rank:   10; NumRanks: 24; RankCore: 104; Hostname: a01n05; GPU: 5
    Rank:   11; NumRanks: 24; RankCore: 108; Hostname: a01n05; GPU: 5

    Rank:   12; NumRanks: 24; RankCore:   0; Hostname: a01n01; GPU: 0
    Rank:   13; NumRanks: 24; RankCore:   4; Hostname: a01n01; GPU: 0

    Rank:   14; NumRanks: 24; RankCore:   8; Hostname: a01n01; GPU: 1
    Rank:   15; NumRanks: 24; RankCore:  12; Hostname: a01n01; GPU: 1

    Rank:   16; NumRanks: 24; RankCore:  16; Hostname: a01n01; GPU: 2
    Rank:   17; NumRanks: 24; RankCore:  20; Hostname: a01n01; GPU: 2

    Rank:   18; NumRanks: 24; RankCore:  88; Hostname: a01n01; GPU: 3
    Rank:   19; NumRanks: 24; RankCore:  92; Hostname: a01n01; GPU: 3

    Rank:   20; NumRanks: 24; RankCore:  96; Hostname: a01n01; GPU: 4
    Rank:   21; NumRanks: 24; RankCore: 100; Hostname: a01n01; GPU: 4

    Rank:   22; NumRanks: 24; RankCore: 104; Hostname: a01n01; GPU: 5
    Rank:   23; NumRanks: 24; RankCore: 108; Hostname: a01n01; GPU: 5

    summit>

Multiple Task, Multiple GPU per RS
""""""""""""""""""""""""""""""""""

The following example will create 4 resource sets each with 6 tasks and
3 GPUs. Each set of 6 MPI tasks will have access to 3 GPUs. Ranks 0 - 5
will have access to GPUs 0 - 2 on the first socket of the first node (
red resource set). Ranks 6 - 11 will have access to GPUs 3 - 5 on the
second socket of the first node ( green resource set). This pattern will
continue until 4 resource sets have been created. The following jsrun
command will request 4 resource sets (``-n4``). Each resource set will
contain 6 MPI tasks (``-a6``), 3 GPUs (``-g3``), and 6 cores
(``-c6``).

.. image:: /images/RS-summit-example-24Tasks-3GPU-6Cores.png
   :class: normal aligncenter size-full wp-image-792423
   :width: 600px
   :height: 300px

::

    summit> jsrun -n 4 -a 6 -c 6 -g 3 -d packed -l GPU-CPU ./a.out
    Rank:    0; NumRanks: 24; RankCore:   0; Hostname: a33n06; GPU: 0, 1, 2
    Rank:    1; NumRanks: 24; RankCore:   4; Hostname: a33n06; GPU: 0, 1, 2
    Rank:    2; NumRanks: 24; RankCore:   8; Hostname: a33n06; GPU: 0, 1, 2
    Rank:    3; NumRanks: 24; RankCore:  12; Hostname: a33n06; GPU: 0, 1, 2
    Rank:    4; NumRanks: 24; RankCore:  16; Hostname: a33n06; GPU: 0, 1, 2
    Rank:    5; NumRanks: 24; RankCore:  20; Hostname: a33n06; GPU: 0, 1, 2

    Rank:    6; NumRanks: 24; RankCore:  88; Hostname: a33n06; GPU: 3, 4, 5
    Rank:    7; NumRanks: 24; RankCore:  92; Hostname: a33n06; GPU: 3, 4, 5
    Rank:    8; NumRanks: 24; RankCore:  96; Hostname: a33n06; GPU: 3, 4, 5
    Rank:    9; NumRanks: 24; RankCore: 100; Hostname: a33n06; GPU: 3, 4, 5
    Rank:   10; NumRanks: 24; RankCore: 104; Hostname: a33n06; GPU: 3, 4, 5
    Rank:   11; NumRanks: 24; RankCore: 108; Hostname: a33n06; GPU: 3, 4, 5

    Rank:   12; NumRanks: 24; RankCore:   0; Hostname: a33n05; GPU: 0, 1, 2
    Rank:   13; NumRanks: 24; RankCore:   4; Hostname: a33n05; GPU: 0, 1, 2
    Rank:   14; NumRanks: 24; RankCore:   8; Hostname: a33n05; GPU: 0, 1, 2
    Rank:   15; NumRanks: 24; RankCore:  12; Hostname: a33n05; GPU: 0, 1, 2
    Rank:   16; NumRanks: 24; RankCore:  16; Hostname: a33n05; GPU: 0, 1, 2
    Rank:   17; NumRanks: 24; RankCore:  20; Hostname: a33n05; GPU: 0, 1, 2

    Rank:   18; NumRanks: 24; RankCore:  88; Hostname: a33n05; GPU: 3, 4, 5
    Rank:   19; NumRanks: 24; RankCore:  92; Hostname: a33n05; GPU: 3, 4, 5
    Rank:   20; NumRanks: 24; RankCore:  96; Hostname: a33n05; GPU: 3, 4, 5
    Rank:   21; NumRanks: 24; RankCore: 100; Hostname: a33n05; GPU: 3, 4, 5
    Rank:   22; NumRanks: 24; RankCore: 104; Hostname: a33n05; GPU: 3, 4, 5
    Rank:   23; NumRanks: 24; RankCore: 108; Hostname: a33n05; GPU: 3, 4, 5
    summit>

Single Task, Multiple GPUs, Multiple Threads per RS
"""""""""""""""""""""""""""""""""""""""""""""""""""

The following example will create 12 resource sets each with 1 task, 4
threads, and 1 GPU. Each MPI task will start 4 threads and have access
to 1 GPU. Rank 0 will have access to GPU 0 and start 4 threads on the
first socket of the first node ( red resource set). Rank 2 will have
access to GPU 1 and start 4 threads on the second socket of the first
node ( green resource set). This pattern will continue until 12 resource
sets have been created. The following jsrun command will create 12
resource sets (``-n12``). Each resource set will contain 1 MPI task
(``-a1``), 1 GPU (``-g1``), and 4 cores (``-c4``). Notice that
more cores are requested than MPI tasks; the extra cores will be needed
to place threads. Without requesting additional cores, threads will be
placed on a single core.

.. image:: /images/RS-summit-example-4Threads-4Core-1GPU.png
   :class: normal aligncenter size-full wp-image-792873
   :width: 600px
   :height: 300px

**Requesting Cores for Threads:** The ``-c`` flag should be used to
request additional cores for thread placement. Without requesting
additional cores, threads will be placed on a single core.

**Binding Cores to Tasks:** The ``-b`` binding flag should be used to
bind cores to tasks. Without specifying binding, all threads will be
bound to the first core.

::

    summit> setenv OMP_NUM_THREADS 4
    summit> jsrun -n12 -a1 -c4 -g1 -b packed:4 -d packed ./a.out
    Rank: 0; RankCore: 0; Thread: 0; ThreadCore: 0; Hostname: a33n06; OMP_NUM_PLACES: {0},{4},{8},{12}
    Rank: 0; RankCore: 0; Thread: 1; ThreadCore: 4; Hostname: a33n06; OMP_NUM_PLACES: {0},{4},{8},{12}
    Rank: 0; RankCore: 0; Thread: 2; ThreadCore: 8; Hostname: a33n06; OMP_NUM_PLACES: {0},{4},{8},{12}
    Rank: 0; RankCore: 0; Thread: 3; ThreadCore: 12; Hostname: a33n06; OMP_NUM_PLACES: {0},{4},{8},{12}

    Rank: 1; RankCore: 16; Thread: 0; ThreadCore: 16; Hostname: a33n06; OMP_NUM_PLACES: {16},{20},{24},{28}
    Rank: 1; RankCore: 16; Thread: 1; ThreadCore: 20; Hostname: a33n06; OMP_NUM_PLACES: {16},{20},{24},{28}
    Rank: 1; RankCore: 16; Thread: 2; ThreadCore: 24; Hostname: a33n06; OMP_NUM_PLACES: {16},{20},{24},{28}
    Rank: 1; RankCore: 16; Thread: 3; ThreadCore: 28; Hostname: a33n06; OMP_NUM_PLACES: {16},{20},{24},{28}

    ...

    Rank: 10; RankCore: 104; Thread: 0; ThreadCore: 104; Hostname: a33n05; OMP_NUM_PLACES: {104},{108},{112},{116}
    Rank: 10; RankCore: 104; Thread: 1; ThreadCore: 108; Hostname: a33n05; OMP_NUM_PLACES: {104},{108},{112},{116}
    Rank: 10; RankCore: 104; Thread: 2; ThreadCore: 112; Hostname: a33n05; OMP_NUM_PLACES: {104},{108},{112},{116}
    Rank: 10; RankCore: 104; Thread: 3; ThreadCore: 116; Hostname: a33n05; OMP_NUM_PLACES: {104},{108},{112},{116}

    Rank: 11; RankCore: 120; Thread: 0; ThreadCore: 120; Hostname: a33n05; OMP_NUM_PLACES: {120},{124},{128},{132}
    Rank: 11; RankCore: 120; Thread: 1; ThreadCore: 124; Hostname: a33n05; OMP_NUM_PLACES: {120},{124},{128},{132}
    Rank: 11; RankCore: 120; Thread: 2; ThreadCore: 128; Hostname: a33n05; OMP_NUM_PLACES: {120},{124},{128},{132}
    Rank: 11; RankCore: 120; Thread: 3; ThreadCore: 132; Hostname: a33n05; OMP_NUM_PLACES: {120},{124},{128},{132}

    summit>

Hardware Threads: Multiple Threads per Core
"""""""""""""""""""""""""""""""""""""""""""

Each physical core on Summit contains 4 hardware threads. The SMT level
can be set using LSF flags:

SMT1

::

    #BSUB -alloc_flags smt1
    jsrun -n1 -c1 -a1 -bpacked:4 csh -c 'echo $OMP_PLACES’
    0

SMT2

::

    #BSUB -alloc_flags smt2
    jsrun -n1 -c1 -a1 -bpacked:4 csh -c 'echo $OMP_PLACES’
    {0:2}

SMT4

::

    #BSUB -alloc_flags smt4
    jsrun -n1 -c1 -a1 -bpacked:4 csh -c 'echo $OMP_PLACES’
    {0:4}

.. image:: /images/FS-summit-example-MultiThreadPerCore.png
   :class: normal aligncenter size-full wp-image-797960
   :width: 600px
   :height: 300px

Common Use Cases
""""""""""""""""

The following table provides a quick reference for creating resource
sets of various common use cases. The ``-n`` flag can be altered to
specify the number of resource sets needed.

+-----------------+-------------+-----------+------------------+--------+---------------------------------------+
| Resource Sets   | MPI Tasks   | Threads   | Physical Cores   | GPUs   | jsrun Command                         |
+=================+=============+===========+==================+========+=======================================+
| 1               | 42          | 0         | 42               | 0      | jsrun -n1 -a42 -c42 -g0               |
+-----------------+-------------+-----------+------------------+--------+---------------------------------------+
| 1               | 1           | 0         | 1                | 1      | jsrun -n1 -a1 -c1 -g1                 |
+-----------------+-------------+-----------+------------------+--------+---------------------------------------+
| 1               | 2           | 0         | 2                | 1      | jsrun -n1 -a2 -c2 -g1                 |
+-----------------+-------------+-----------+------------------+--------+---------------------------------------+
| 1               | 1           | 0         | 1                | 2      | jsrun -n1 -a1 -c1 -g2                 |
+-----------------+-------------+-----------+------------------+--------+---------------------------------------+
| 1               | 1           | 21        | 21               | 3      | jsrun -n1 -a1 -c21 -g3 -bpacked:21    |
+-----------------+-------------+-----------+------------------+--------+---------------------------------------+

 

jsrun Tools
^^^^^^^^^^^

This section describes tools that users might find helpful to better
understand the jsrun job launcher.

Hello\_jsrun
""""""""""""

Hello\_jsrun is a "Hello World"-type program that users can run on
Summit nodes to better understand how MPI ranks and OpenMP threads are
mapped to the hardware. https://code.ornl.gov/t4p/Hello_jsrun A
screencast showing how to use Hello\_jsrun is also available:
https://vimeo.com/261038849

jsrunVisualizer
"""""""""""""""

jsrunVisualizer is a web-application that mimics basic jsrun behavior
locally in your browser. It's an easy way to get familiar with jsrun
options for Summit, understand how multiple flags interact, and share
your layout ideas with others. Once you've crafted your per-node
resource sets, you can take the job script it generates and run the same
layout on Summit itself! https://jsrunvisualizer.olcf.ornl.gov/
https://vimeo.com/299079999

More Information
^^^^^^^^^^^^^^^^

This section provides some of the most commonly used LSF commands as
well as some of the most useful options to those commands and
information on ``jsrun``, Summit's job launch command. Many commands
have much more information than can be easily presented here. More
information about these commands is available via the online manual
(i.e. ``man jsrun``). Additional LSF information can be found on `IBM’s
website <https://www.ibm.com/developerworks/community/wikis/home?lang=en#!/wiki/New%20IBM%20Platform%20LSF%20Wiki/page/LSF%20documentation>`__,
specifically the `Running
Jobs <https://www.ibm.com/developerworks/community/wikis/form/anonymous/api/wiki/99245193-fced-40e5-90df-a0e9f50a0fb0/page/22e9aefe-a2e8-46e6-ad62-2ff5860f45aa/attachment/d6b2c089-eb88-48a6-80ce-acff94a7f02c/media/lsf_users_guide.pdf>`__
and `Command
Reference <https://www.ibm.com/developerworks/community/wikis/form/anonymous/api/wiki/99245193-fced-40e5-90df-a0e9f50a0fb0/page/22e9aefe-a2e8-46e6-ad62-2ff5860f45aa/attachment/f8aad44b-8e1c-4051-95c9-d2c80fe90cf3/media/lsf_command_ref.pdf>`__
Documents.

CUDA-Aware MPI
--------------

CUDA-Aware MPI and GPUDirect are often used interchangeably, but they
are distinct topics. CUDA-Aware MPI allows GPU buffers (e.g., GPU memory
allocated with ``cudaMalloc``) to be used directly in MPI calls rather
than requiring data to be manually transferred to/from a CPU buffer
(e.g., using ``cudaMemcpy``) before/after passing data in MPI calls. By
itself, CUDA-Aware MPI does not specify whether data is staged through
CPU memory or, for example, transferred directly between GPUs when
passing GPU buffers to MPI calls. That is where GPUDirect comes in.
GPUDirect is a technology that can be implemented on a system to enhance
CUDA-Aware MPI by allowing data transfers directly between GPUs on the
same node (peer-to-peer) and/or directly between GPUs on different nodes
(with RDMA support) without the need to stage data through CPU memory.
On Summit, both peer-to-peer and RDMA support are implemented. To enable
CUDA-Aware MPI in a job, use the following argument to ``jsrun``:

.. code::

    jsrun --smpiargs="-gpu" ...

Debugging
=========

Arm DDT
-------

Arm DDT is an advanced debugging tool used for scalar, multi-threaded,
and large-scale parallel applications. In addition to traditional
debugging features (setting breakpoints, stepping through code,
examining variables), DDT also supports attaching to already-running
processes and memory debugging. In-depth details of DDT can be found in
the `Official DDT User
Guide <https://www.allinea.com/user-guide/forge/userguide.html>`__, and
instructions for how to use it on OLCF systems can be found on the
`Forge (DDT/MAP) Software Page </software_package/forge/>`__. DDT is the
OLCF's recommended debugging software for large parallel applications.

GDB
---

`GDB <https://www.gnu.org/software/gdb/>`__, the GNU Project Debugger,
is a command-line debugger useful for traditional debugging and
investigating code crashes. GDB lets you debug programs written in Ada,
C, C++, Objective-C, Pascal (and many other languages). GDB is available
on Summit under all compiler families:

.. code::

    module load gdb

Additional information about GDB usage and OLCF-provided builds can be
found on the `GDB Software Page </software_package/gdb/>`__.

Valgrind
--------

`Valgrind <http://valgrind.org>`__ is an instrumentation framework for
building dynamic analysis tools. There are Valgrind tools that can
automatically detect many memory management and threading bugs, and
profile your programs in detail. You can also use Valgrind to build new
tools. The Valgrind distribution currently includes five
production-quality tools: a memory error detector, a thread error
detector, a cache and branch-prediction profiler, a call-graph
generating cache profiler, and a heap profiler. It also includes two
experimental tools: a data race detector, and an instant memory leak
detector. The Valgrind tool suite provides a number of debugging and
profiling tools. The most popular is Memcheck, a memory checking tool
which can detect many common memory errors such as:

- Touching memory you shouldn’t (eg. overrunning heap block boundaries,
  or reading/writing freed memory).
- Using values before they have been initialized.
- Incorrect freeing of memory, such as double-freeing heap blocks.
- Memory leaks.

Valgrind is available on Summit under all compiler families:

.. code::

    module load valgrind

Additional information about Valgrind usage and OLCF-provided builds can
be found on the `Valgrind Software
Page </software_package/valgrind/>`__.

Optimizing and Profiling
========================

Profiling CUDA Code with NVPROF
-------------------------------

NVIDIA's command-line profiler, ``nvprof``, provides profiling for CUDA
codes. No extra compiling steps are required to use ``nvprof``. The
profiler includes tracing capability as well as the ability to gather
many performance metrics, including FLOPS. The profiler data output can
be saved and imported into the NVIDIA Visual Profiler for additional
graphical analysis. To use ``nvprof``, the ``cuda`` module must be
loaded.

::

    summit> module load cuda

A simple "Hello, World!" run using ``nvprof`` can be done by adding
"nvprof" to the
`jsrun </for-users/system-user-guides/summit/running-jobs/#job-launcher>`__
line in your `batch
script </for-users/system-user-guides/summit/running-jobs/#batch-scripts>`__.

::

    ...
    jsrun -n1 -a1 -g1 nvprof ./hello_world_gpu
    ...

Although ``nvprof`` doesn't provide aggregated MPI data, the ``%h`` and
``%p`` output file modifiers can be used to create separate output files
for each host and process.

::

    ...
    jsrun -n1 -a1 -g1 nvprof -o output.%h.%p ./hello_world_gpu
    ...

There are many various metrics and events that the profiler can capture.
For example, to output the number of double-precision FLOPS, you may use
the following:

::

    ...
    jsrun -n1 -a1 -g1 nvprof --metrics flops_dp -o output.%h.%p ./hello_world_gpu
    ...

To see a list of all available metrics and events, use the following:

::

    summit> nvprof --query-metrics
    summit> nvprof --query-events

While using ``nvprof`` on the command-line is a quick way to gain
insight into your CUDA application, a full visual profile is often even
more useful. For information on how to view the output of ``nvprof`` in
the NVIDIA Visual Profiler, see the `NVIDIA
Documentation <http://docs.nvidia.com/cuda/profiler-users-guide/#nvprof-overview>`__.

Score-P
-------

[ls\_content\_block id="24659" para="full"] For detailed information
about using Score-P on Summit and the builds available, please see the
`Score-P Software Page </software_package/score-p/>`__.

Vampir
------

[ls\_content\_block id="24496" para="full"] For detailed information
about using Vampir on Summit and the builds available, please see the
`Vampir Software Page </software_package/vampir/>`__.

Known Issues
============

Open Issues
-----------

JSM Fault Tolerance causes jobs to fail to start
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Adding ``FAULT_TOLERANCE=1`` in your individual ``~/.jsm.conf`` file,
will result in LSF jobs failing to successfully start. A bug has been
filed with IBM to address this issue.

CSM-based launch is not currently supported
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Users should not use ``JSMD_LAUNCH_MODE=csm`` in their ``~/.jsm.conf``
file at this time. A bug has been filed with IBM to address this issue.

Spindle is not currently supported
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Users should not use ``USE_SPINDLE=1`` or ``LOAD_SPINDLE=1`` in their
``~/.jsm.conf`` file at this time. A bug has been filed with IBM to
address this issue.

Spectrum MPI tunings needed for maximum bandwidth
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, Spectrum MPI is configured for minimum latency. If your
application needs maximum bandwidth, the following settings are
recommended:

::

    $ export PAMI_ENABLE_STRIPING=1
    $ export PAMI_IBV_ADAPTER_AFFINITY=1
    $ export PAMI_IBV_DEVICE_NAME="mlx5_0:1,mlx5_3:1"
    $ export PAMI_IBV_DEVICE_NAME_1="mlx5_3:1,mlx5_0:1"

Debugging slow application startup or slow performance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order for debugging and profiling tools to work, you need to unload
Darshan

::

    $ module unload darshan-runtime

Spectrum MPI provides a tracing library that can be helpful to gather
more detail information about the MPI communication of your job. To
gather MPI tracing data, you can set
``export OMPI_LD_PRELOAD_POSTPEND=$OLCF_SPECTRUM_MPI_ROOT/lib/libmpitrace.so``
in your environment. This will generate profile files with timings for
the individual processes of your job. In addition, to debug slow startup
JSM provides the option to create a progress file. The file will show
information that can be helpful to pinpoint if a specific node is
hanging or slowing down the job step launch. To enable it, you can use:
``jsrun --progress ./my_progress_file_output.txt``.

-a flag ignored when using a jsrun resource set file with -U
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When using file-based specification of resource sets with ``jsrun -U``,
the ``-a`` flag (number of tasks per resource set) is ignored. This has
been reported to IBM and they are investigating. It is generally
recommended to use jsrun explicit resource files (ERF) with
``--erf_input`` and ``--erf_output`` instead of ``-U``.

-g flag causes internal compiler error with XL compiler
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some users have reported an internal compiler error when compiling their
code with XL with the \`-g\` flag. This has been reported to IBM and
they are investigating.

Jobs suspended due to retry limit / Queued job flip-flops between queued/running states
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some users have reported seeing their jobs transition from the normal
queued state, into a running state, and then back again to queued.
Sometimes this can happen multiple times. Eventually, internal limits in
the LSF scheduler will be reached, at which point the job will no longer
be eligible for running. The bhist command can be used to see if a job
is cycling between running and eligible states. The pending reason given
by bhist can also be useful to debug. This can happen due to
modifications that the user has made to their environment on the system,
incorrect ssh key setup, attempting to load unavailable/broken modules.
or system problems with individual nodes. When jobs are observed to
flip-flop between running and queued, and/or become ineligible without
explanation, then deeper investigation is required and the user should
write to help@olcf.ornl.gov.

jsrun explicit resource file (ERF) output format error
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

jsrun's option to create an explicit resource file (--erf\_output) will
incorrectly create a file with one line per rank. When reading the file
in with (--erf\_input) you will see warnings for overlapping resource
sets. This issue has been reported. The work around is to manually
update the created erf file to contain a single line per resource set
with multiple ranks per line.

jsrun explicit resource file (ERF) allocates incorrect resources
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When using an ERF that requests cores on a compute node’s second socket
(hardware threads 88-171), the set of cores allocated on the second
socket are shifted upwards by (1) physical core. For example: The
following ERF requests the first physical core on each socket:

::

    2 : {host: * ; cpu: {0-3},{88-91}}

``jsrun`` currently shifts the second socket’s allocation by (1)
physical core, allocating 92-95 instead of the specified 88-91.

::

    $ jsrun --erf_input ERF_filename js_task_info | sort

    Task 0 ( 0/2, 0/2 ) is bound to cpu[s] 0-3 on host h36n03 with OMP_NUM_THREADS=1 and with OMP_PLACES={0:4}

    Task 1 ( 1/2, 1/2 ) is bound to cpu[s] 92-95 on host h36n03 with OMP_NUM_THREADS=1 and with OMP_PLACES={92:4}

Job hangs in MPI\_Finalize
^^^^^^^^^^^^^^^^^^^^^^^^^^

There is a known issue in Spectrum MPI 10.2.0.10 provided by the
``spectrum-mpi/10.2.0.10-20181214`` modulefile that causes a hang in
``MPI_Finalize`` when ROMIO 3.2.1 is being used and the
``darshan-runtime`` modulefile is loaded. The recommended and default
Spectrum MPI version as of March 3, 2019 is Spectrum MPI 10.2.0.11
provided by the ``spectrum-mpi/10.2.0.11-20190201`` modulefile. If you
are seeing this issue, please make sure that you are using the latest
version of Spectrum MPI. If you need to use a previous version of
Spectrum MPI, your options are:

-  Unload the ``darshan-runtime`` modulefile.
-  Alternatively, set ``export OMPI_MCA_io=romio314`` in your
   environment to use the previous version of ROMIO. Please note that
   this version has known performance issues with parallel HDF5 (see
   "Slow performance using parallel HDF5" issue below).

jsrun latency priority capitalization allocates incorrect resources
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

jsrun's latency priority (\`-l\`) flag can be given lowercase values
(i.e. gpu-cpu) or capitalized values (i.e. GPU-CPU). Expected behavior:

When capitalized, jsrun should not compromise on the resource layout,
and will wait to begin the job step until the ideal resources are
available. When given a lowercase value, jsrun will not wait, but
initiate the job step with the most ideal layout as is available at the
time. This also means that when there's no resource contention, such as
running a single job step at a time, capitalization should not matter,
as they should both yield the same resources.

Actual behavior:

Capitalizing the latency priority value may allocate incorrect
resources, or even cause the job step to fail entirely.

Recommendation:

It is currently recommended to only use the lowercase values to (-l /
--latency\_priority). The system default is: gpu-cpu,cpu-mem,cpu-cpu.
Since this ordering is used implicitly when the -l flag is omitted, this
issue only impacts submissions which explicitly include a latency
priority in the jsrun command.

Error when using complex datatypes with MPI Collectives and GPUDirect
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Users have reported errors when using complex datatypes with MPI
Collectives and GPUDirect:

::

    jsrun --smpiargs="-gpu" -n 6 -a 1 -g 1   ./a.out
    [h35n05:113506] coll:ibm:allreduce: GPU awareness in PAMI requested. It is not safe to defer to another component.
    [h35n05:113506] *** An error occurred in MPI_Allreduce
    [h35n05:113506] *** reported by process [3199551009,2]
    [h35n05:113506] *** on communicator MPI_COMM_WORLD
    [h35n05:113506] *** MPI_ERR_UNSUPPORTED_OPERATION: operation not supported
    [h35n05:113506] *** MPI_ERRORS_ARE_FATAL (processes in this communicator will now abort,
    [h35n05:113506] ***    and potentially your MPI job)
    [h35n05:113509] coll:ibm:allreduce: GPU awareness in PAMI requested. It is not safe to defer to another component.

This is a known issue with libcoll and the SMPI team is working to
resolve it. In the mean time, a workaround is to treat the complex array
as a real array with double the length if the operation is not
MPI\_Prod. Note: This requires code modification. An alternative
workaround is to disable IBM optimized collectives. This will impact
performance however but requires no code changes and should be correct
for all MPI\_Allreduce operations. You can do this by adding the
following option to your jsrun command line:
``--smpiargs="-HCOLL -FCA -mca coll_hcoll_enable 1 -mca coll_hcoll_np 0 -mca coll ^basic -mca coll ^ibm -async"``

Resolved Issues
---------------

Parallel I/O crash on GPFS with latest MPI ROMIO
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In some cases with large number of MPI processes when there is not
enough memory available on the compute node, the Abstract-Device
Interface for I/O (ADIO) driver can break with this error: Out of memory
in file
../../../../../../../opensrc/ompi/ompi/mca/io/romio321/romio/adio/ad\_gpfs/ad\_gpfs\_rdcoll.c,
line 1178 The solution is to declare in your submission script:

::

    export GPFSMPIO_COMM=1

This command will use non-blocking MPI calls and not MPI\_Alltoallv for
exchange of data between the MPI I/O aggregators which requires
significant more amount of memory. The following issues were resolved
with the May 21, 2019 upgrade:

Issue with CUDA Aware MPI with >1 resource set per node (Resolved: May 21, 2019)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Attempting to run an application with CUDA aware MPI using more than one
resource set per node with produce the following error on each MPI rank:

::

    /__SMPI_build_dir__________________________________________/ibmsrc/pami/ibm-pami/buildtools/pami_build_port/../pami/components/devices/ibvdevice/CudaIPCPool.h:300:
    [0]Error opening IPC Memhandle from peer:1, invalid argument
    CUDA level IPC failure: this has been observed in environments where cgroups separate the visible GPUs between ranks. The option -x PAMI_DISABLE_IPC=1 can be used to disable CUDA level IPC.[:] *** Process received signal ***

Spectrum MPI relies on CUDA Inter-process Communication (CUDA IPC) to
provide fast on-node between GPUs. At present this capability cannot
function with more than one resource set per node.

#. Set the environment variable ``PAMI_DISABLE_IPC=1`` to force Spectrum
   MPI to not use fast GPU Peer-to-peer communication. This option will
   allow your code to run with more than one resource set per host, but
   you may see slower GPU to GPU communication.
#. Run in a single resource set per host, i.e. with
   ``jsrun --gpu_per_rs 6``

If on-node MPI communication between GPUs is critical to your
application performance, option B is recommended but you’ll need to set
the GPU affinity manually. This could be done with an API call in your
code (e.g. ``cudaSetDevice``), or by using a wrapper script.

Simultaneous backgrounded jsruns (Resolved: May 21, 2019)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We have seen occasional errors from batch jobs with multiple
simultaneous backgrounded jsrun commands. Jobs may see pmix errors
during the noted failures. <!–– Since the issue is occasional, multiple
resubmits can be a workaround at this point. -->

--------------

The following issue was resolved with the software default changes from
March 12, 2019 that set Spectrum MPI 10.2.0.11 (20190201) as default and
moved ROMIO to version 3.2.1:

Slow performance using parallel HDF5 (Resolved: March 12, 2019)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A performance issue has been identified using parallel HDF5 with the
default version of ROMIO provided in
``spectrum-mpi/10.2.0.10-20181214``. To fully take advantage of parallel
HDF5, users need to switch to the newer version of ROMIO and use ROMIO
hints. The following shows recommended variables and hints for a 2 node
job. Please note that hints must be tuned for a specific job.

::

    $ module unload darshan-runtime
    $ export OMPI_MCA_io=romio321
    $ export ROMIO_HINTS=./my_romio_hints
    $ cat $ROMIO_HINTS
    romio_cb_write enable
    romio_ds_write enable
    cb_buffer_size 16777216
    cb_nodes 2

--------------

The following issues were resolved with the February 19, 2019 upgrade:

Job step cgroups are not currently supported (Resolved: February 19, 2019)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A regression was introduced in JSM 10.02.00.10rtm2 that prevents job
step cgroups from being created as a result, JSM, is defaulting to
setting ``CUDA_VISIBLE_DEVICES`` in order to allocate GPUs to specific
resource sets. Because of this issue, even if using ``--gpu_per_rs 0``
or ``-g 0``, every resource set in the step will be able to see all 6
GPUs in a node.

JSM stdio options do not create files (Resolved: February 19, 2019)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When using ``--stdio_stdout`` or ``--stdio_stderr`` users must use
absolute paths. Using relative paths (e.g. ``./my_stdout``) will not
successfully create the file in the user's current working directory. An
bug has been filed with IBM to fix this issue and allow relative paths.

JSM crash when using different number of resource sets per host (Resolved: February 19, 2019)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In some cases users will encounter a segmentation fault when running job
steps that have uneven number of resource sets per node. For example:

::

    $ jsrun --nrs 41 -c 21 -a 1 --bind rs ./a.out
    [a03n07:74208] *** Process received signal ***
    [a03n07:74208] Signal: Segmentation fault (11)
    [a03n07:74208] Signal code: Address not mapped (1)
    [a03n07:74208] Failing at address: (nil)
    ...

As a workaround, two environment variables are set as default in the
user environment ``PAMI_PMIX_USE_OLD_MAPCACHE=1`` and
``OMPI_MCA_coll_ibm_xml_disable_cache=1``.

CUDA 10.1 Known Issues
----------------------

Default nvprof setting clobbers ``LD_PRELOAD``, interfering with SpectrumMPI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

CUDA 10 adds a new feature to profile CPU side OpenMP constructs (see
https://docs.nvidia.com/cuda/profiler-users-guide/index.html#openmp).
This feature is enabled by default and has a bug which will cause it to
overwrite the contents of ``LD_PRELOAD``. SpectrumMPI requires a library
(``libpami_cuda_hook.so``) to be preloaded in order to function. All MPI
applications on Summit will break when run in nvprof with default
settings. The workaround is to disable the new OpenMP profiling feature:

::

    $ jsrun  nvprof --openmp-profiling off

MPI annotation may cause segfaults with applications using MPI\_Init\_thread
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Users on Summit can have MPI calls automatically annotated in ``nvprof``
timelines using the ``nvprof --annotate-mpi openmpi`` option. If the
user calls ``MPI_Init_thread`` instead of ``MPI_Init``, ``nvprof`` may
segfault, as ``MPI_Init_thread`` is currently not being wrapped by
``nvprof``. The current alternative is to build and follow the
instructions from
https://github.com/NVIDIA/cuda-profiler/tree/mpi_init_thread.

cudaMemAdvise before context creation leads to a kernel panic
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There is a (very rare) driver bug involving cudaManagedMemory that can
cause a kernel panic. If you encounter this bug, please contact the
`OLCF User Support <mailto:help@olcf.ornl.gov>`__ team. The easiest
mitigation is for the user code to initialize a context on every GPU
with which it intends to interact (for example by calling
``cudaFree(0)`` while each device is active).

Some uses of Thrust complex vectors fail at compile time with warnings of identifiers being ``undefined in device code``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This issue comes from the fact that ``std::complex`` is not
``__host__``/``__device__`` annotated, so all its functions are
implicitly ``__host__``. There is a mostly simple workaround, assuming
this is compiled as C++11: in ``complex.h`` and ``complex.inl``,
annotate the functions that deal with ``std::complex`` as
``__host__ __device__`` (they are the ones that are annotated only as
``__host__`` right now), and then compile with
``--expt-relaxed-constexpr``. Users that encounter this issue, can use
the following workaround. copy the entirety of
``${OLCF_CUDA_ROOT}/include/thrust`` to a private location, make the
above edits to ``thrust/complex.h`` and
``thrust/detail/complex/complex.inl``, and then add that to your include
path:

::

    $ nvcc -ccbin=g++ --expt-relaxed-constexpr assignment.cu -I./

A permanent fix of this issue is expected in the version of Thrust
packed with CUDA 10.1 update 1

Breakpoints in CUDA kernels recommendation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``cuda-gdb`` allows for breakpoints to be set inside CUDA kernels to
inspect the program state on the GPU. This can be a valuable debugging
tool but breaking inside kernels does incur significant overhead that
should be included in your expected runtime. The time required to hit a
breakpoint inside a CUDA kernel depends on how many CUDA threads are
used to execute the kernel. It may take several seconds to stop at
kernel breakpoints for very large numbers of threads. For this reason,
it is recommended to choose breakpoints judiciously, especially when
running the debugger in "batch" or "offline" mode where this overhead
may be misperceived as the code hanging. If possible, debugging a
smaller problem size with fewer active threads can be more pleasant.

Training System (Ascent)
========================

**NOTE:** Ascent is a training system that is not intended to be used as
an OLCF user resource. Access to the system is only obtained through
OLCF training events.

Ascent is an 18-node stand-alone system with the same architecture as
Summit (see `**Summit
Nodes** <https://www.olcf.ornl.gov/for-users/system-user-guides/summit/summit-user-guide/#system-overview>`__
section above), so most of this Summit User Guide can be referenced for
Ascent as well. However, aside from the number of compute nodes, there
are other differences between the two systems. Most notably, Ascent sits
in the NCCS Open Security Enclave, which is subject to fewer
restrictions than the Moderate Security Enclave that systems such as
Summit belong to. This means that participants in OLCF training events
can go through a streamlined version of the approval process before
gaining access to the system. The remainder of this section of the user
guide describes "Ascent-specific" information intended for participants
of OLCF training events.

File Systems
------------

It is important to note that because Ascent sits in the NCCS Open
Security Enclave, it also mounts different file systems than Summit.
These file systems provide both user-affiliated and project-affiliated
storage areas for each user.

NFS Directories
^^^^^^^^^^^^^^^

Upon logging into Ascent, users will be placed in their own personal
home (NFS) directory, ``/ccsopen/home/[userid]``, which can only be
accessed by that user. Users also have access to an NFS project
directory, ``/ccsopen/proj/[projid]``, which is visible to all members
of a project. Both of these NFS directories are commonly used to store
source code and build applications.

GPFS Directories
^^^^^^^^^^^^^^^^

Users also have access to a (GPFS) parallel file system, called wolf,
which is where data should be written when running on Ascent's compute
nodes. Under ``/gpfs/wolf/[projid]``, there are 3 directories:

::

    $ ls /gpfs/wolf/[projid]
    proj-shared  scratch  world-shared

-  ``proj-shared`` can be accessed by all members of a project.
-  ``scratch`` contains directories for each user of a project and only
   that user can access their own directory.
-  ``world-shared`` can be accessed by any users on the system in any
   project.

Obtaining Access to Ascent
--------------------------

**NOTE:** Ascent is a training system that is not intended to be used as
an OLCF user resource. Access to the system is only obtained through
OLCF training events.

This sub-section describes the process of obtaining access to Ascent for
an OLCF training event. Please follow the steps below to request access.

Step 1: Fill out and submit an `**OLCF Account Application Form** <https://www.olcf.ornl.gov/for-users/documents-forms/olcf-account-application>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Enter the requested information into the form. For "Project
Information", enter the following:

.. image:: /images/Ascent_Account_Application_1.png

For "Project Information", enter the following:

.. image:: /images/Ascent_Account_Application_2.png

For "Account Information", enter the following:

.. image:: /images/Ascent_Account_Application_3.png

**NOTE:** After submitting your application, it will need to pass
through the approval process. Depending on when you submit, approval
might not occur until the next business day.

Step 2: Set Your XCAMS/UCAMS Password
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once approved, if you are a new user, your account will be created and
an email will be sent asking you to set up a password. If you already
had an XCAMS/UCAMS account, you will not be sent the email asking you to
setup a new password (simply use your existing credentials). Once
passwords are known, users can log in to Ascent using their XCAMS/UCAMS
username and password (see the next section)

Logging In to Ascent
--------------------

To log in to Ascent, please use your XCAMS/UCAMS username and password:
``$ ssh USERNAME@login1.ascent.olcf.ornl.gov``

**NOTE:** You do not need to use an RSA token to log in to Ascent.
Please use your XCAMS/UCAMS username and password (which is different
from the username and PIN + RSA token code used to log in to other OLCF
systems such as Summit).

**NOTE:** It will take ~5 minutes for your directories to be created, so
if your account was just created and you log in and you do not have a
home directory, this is likely the reason.
