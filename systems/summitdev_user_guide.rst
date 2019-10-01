.. _summitdev-user-guide:

********************
SummitDev User Guide
********************

.. _summitdev-system-overview:

System Overview
===============

The SummitDev system was an early access machine available for select teams and
staff ahead of deploying Summit, the OLCF's current flagship supercomputer. The
system is now available for Director's Discretion projects that might be new to
either the Power architecture or utilizing multiple GPUs. It is a stepping
stone for migrating codes to run on Summit. 

.. _summitdev-hardware:

Hardware
========

The system contains three racks, totaling 54 IBM POWER8 S822LC compute nodes.
Each node has 2 IBM POWER8 CPUs and 4 NVIDIA Tesla P100 GPUs. The POWER8 CPUs
have an attached 256GB of DDR4 memory. The POWER8 CPU has 10 cores, each with 8
hardware threads. The GPUs are connected by NVLink 1.0 at 80GB/s, and each GPU
has 16GB HBM2 memory. A node-local NVMe device provides 800GB of high-speed
scratch storage. Nodes are connected in a full fat-tree by EDR InfiniBand.
Summitdev has access to Alpine, the same GPFS filesystem mounted on Summit.

.. _summitdev-access:

Access
======

Access to SummitDev may be granted to Director's Discretion projects with the
intention of moving to Summit.

Connecting
==========

To connect to SummitDev, ssh to ``summitdev.ccs.ornl.gov``. For example:

::

    ssh username@summitdev.ccs.ornl.gov

For more information on connecting to OLCF resources, see :ref:`connecting-to-olcf`.

General Use
===========

While the architecture and design of SummitDev is notably different from
Summit, much of the system software is similar. See the
:doc:`./summit_user_guide` for additional information on:

- :ref:`data-storage-and-transfers`
- :ref:`burst-buffer` (NVMe)
- :ref:`shell-programming-environments`
- :ref:`compiling`
- :ref:`running-jobs`

.. _summitdev-smt:

Simultaneous Multi-Threading (SMT)
==================================

SummitDev supports SMT up to 8 hardware threads per core. The SMT mode for a
particular job can be set using a job feature. For example, to set the SMT mode
to 4 hardware threads per core in a single node (total of 80 hardware threads
per node):

.. code::

    summitdev-login1$ bsub -alloc_flags smt8 -W 30 -nnodes 1 -P proj123 -Is $SHELL
    <<Waiting for dispatch ...>>
    <<Starting on summitdev-login1>>
    summitdev-login1$ jsrun -n1 /usr/sbin/ppc64_cpu --smt
    SMT=8

.. _summitdev-batch-queue:

Batch Queue Limits
==================

+-------+--------------+
| Nodes | Max Walltime |
+=======+==============+
| <= 4  | 4 Hours      |
+-------+--------------+
| > 4   | 1 Hour       |
+-------+--------------+

