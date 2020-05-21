******
Andes
******

System Overview
===============

Andes is a replacement for the Rhea system. Andes has 8 login nodes, 704
compute nodes and 9 GPU nodes. The primary purpose of Andes is to provide a
conduit for large-scale scientific discovery via pre/post processing and
analysis of simulation data generated on Summit.  Users with accounts on Summit
will automatically be given access to Andes.

.. _andes-compute-nodes:

Compute nodes
-------------

Andes contains 704 compute nodes and 9 GPU nodes. Andes has two partitions:

+-------------+-------------+---------+-------------------+------------------------------------+
| Partition   | Node Count  | Memory  | GPU               | CPU                                |
+=============+=============+=========+===================+====================================+
| andes       | 704         | 256 GB  | N/A               | [2x] AMD EPYC 7302 16Core Processor|
| (default)   |             |         |                   | 3.0 GHz                            |   
|             |             |         |                   | (total 32 cores *per node*)        |
+-------------+-------------+---------+-------------------+------------------------------------+
| gpu         | 9           | 1 TB    | [2x]              | [2x] Intel\ |R| Xeon\ |R| E5-2695  |
|             |             |         | NVIDIA\ |R|       | @2.3 GHz - 14 cores, 28 HT         |
|             |             |         | K80               | (total 28 cores, 56 HT *per node*) |
+-------------+-------------+---------+-------------------+-----------------------------------+

**Andes Partition**

The first 704 nodes make up the *andes* partition, where each node contains two
16-core 3.0 GHz AMD EPYC 7302 processors and 256GB of main memory.  Each CPU in
this partition features 16 physical cores, for a total of 32 physical cores per
node.

**GPU Partition**

Andes also has 9 large memory/GPU nodes, which make up the *gpu* partition.
These nodes each have 1TB of main memory and two NVIDIA K80 GPUs in addition to
two 14-core 2.30 GHz Intel Xeon processors with HT Technology. Each CPU in this
partition features 14 physical cores, for a total of 28 physical cores per
node.  With Hyper-Threading enabled, these nodes have 56 logical cores that can
execute 56 hardware threads for increased parallelism.

.. note::
    To access the gpu partition, batch job submissions should request ``-p gpu``.

Both compute partitions are accessible through the same batch queue from Andes' login nodes.


.. _andes-login-nodes:

Login nodes
-----------

Andes features 8 login nodes which are identical to the *andes* partition
compute nodes.  The login nodes provide an environment for editing, compiling,
and launching codes onto the compute nodes. All Andes users will access the
system through these same login nodes, and as such, any CPU- or
memory-intensive tasks on these nodes could interrupt service to other users.
As a courtesy, we ask that you refrain from doing any analysis or visualization
tasks on the login nodes.

For more information on connecting to OLCF resources, see :ref:`connecting-to-olcf`.
