.. _frontier-user-guide:

*******************
Frontier User Guide
*******************

.. _system_overview:

System Overview
===============

Frontier is a HPE Cray EX supercomputer located at the Oak Ridge Leadership Computing Facility. With a theoretical peak double-precision performance of approximately 2 exaflops (2 quintillion calculations per second), it is the fastest system in the world for a wide range of traditional computational science applications. The system has 74 Olympus rack HPE cabinets, each with 128 AMD compute nodes, and a total of 9,408 AMD compute nodes.


.. _frontier-nodes:

Frontier Compute Nodes
----------------------

Each Frontier compute node consists of [1x] 64-core AMD EPYC 7A53 "Optimized 3rd Gen EPYC" CPU (with 2 hardware threads per physical core) with access to 512 GB of DDR4 memory. Each node also contains [4x] AMD MI250X, each with 2 Graphics Compute Dies (GCDs) for a total of 8 GCDs per node. The programmer can think of the 8 GCDs as 8 separate GPUs, each having 64 GB of high-bandwidth memory (HBM2E). The CPU is connected to each GCD via Infinity Fabric CPU-GPU, allowing a peak host-to-device (H2D) and device-to-host (D2H) bandwidth of 36+36 GB/s. The 2 GCDs on the same MI250X are connected with Infinity Fabric GPU-GPU with a peak bandwidth of 200 GB/s. The GCDs on different MI250X are connected with Infinity Fabric GPU-GPU in the arrangement shown in the Frontier Node Diagram below, where the peak bandwidth ranges from 50-100 GB/s based on the number of Infinity Fabric connections between individual GCDs.

.. note::

    **TERMINOLOGY:**

    The 8 GCDs contained in the 4 MI250X will show as 8 separate GPUs according to Slurm, ``ROCR_VISIBLE_DEVICES``, and the ROCr runtime, so from this point forward in the quick-start guide, we will simply refer to the GCDs as GPUs.

.. image:: /images/Frontier_Node_Diagram.jpg
   :align: center
   :width: 100%
   :alt: Frontier node architecture diagram

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


Node Types
----------

On Frontier, there are three major types of nodes you will encounter:
Login, Launch, and Compute. While all of these are similar in terms of
hardware (see: :ref:`frontier-nodes`), they differ considerably in their intended
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
|             | running, it will execute on a Launch Node. (If you were a user of Titan,         |
|             | these are similar in function to service nodes on that system). All commands     |
|             | within your job script (or the commands you run in an interactive job) will run  |
|             | on a launch node. Like login nodes, these are shared resources so you should not |
|             | run multiprocessor/threaded programs on Launch nodes. It is appropriate to       |
|             | launch the jsrun command from launch nodes.                                      |
+-------------+----------------------------------------------------------------------------------+
| Compute     | Most of the nodes on Summit are compute nodes. These are where                   |
|             | your parallel job executes. They're accessed via the jsrun command.              |
+-------------+----------------------------------------------------------------------------------+


System Interconnect
-------------------

The Frontier nodes are connected with [4x] HPE Slingshot 200 Gbps (25 GB/s) NICs providing a node-injection bandwidth of 800 Gbps (100 GB/s).

File Systems
------------

Frontier is connected to the center-wide(?) Orion Lustre filesystem providing 695(? - is that center wide?) PB of storage capacity with a peak write speed of 4.4 TB/s (unclear - got this values from Bronsons user call). Frontier also has access to the center-wide NFS-based filesystem (which provides user and project home areas). 

I cannot find information about the future of HPSS access on Frontier. I know that Crusher currently does not have access, per the crusher doc. I assume it will, and would look like this:
Frontier will also access to the center’s High Performance Storage System (HPSS) - for user and project archival storage - users can log in to the :ref:`dtn-user-guide` to move data to/from HPSS.

Operating System
----------------

State the operating system and current version.


GPUs
----

Each Frontier compute node contains 4 AMD MI250X. The AMD MI250X has a peak performance of 53 TFLOPS in double-precision for modeling and simulation. Each MI250X contains 2 GPUs, where each GPU has a peak performance of 26.5 TFLOPS (double-precision), 110 compute units, and 64 GB of high-bandwidth memory (HBM2) which can be accessed at a peak of 1.6 TB/s. The 2 GPUs on an MI250X are connected with Infinity Fabric with a bandwidth of 200 GB/s (in both directions simultaneously).


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

----

Programming Environment
=======================

[NOTE - I am assuming that nothing will be changing as far as the use of Lmod in managing packages]

Frontier users are provided with many pre-installed software packages and scientific libraries. To facilitate this, environment management tools are used to handle necessary changes to the shell.

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

----

AMD GPUs
========

Each Frontier node uses 4 AMD MI200 GPUs.

Running Jobs
============

Initial placeholder for running jobs section.
Running jobs on Frontier is fun!
