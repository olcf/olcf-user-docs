.. _dtn-user-guide:

**************************
Data Transfer Nodes (DTNs)
**************************

.. _dtn-system-overview:

System Overview
===============

The Data Transfer Nodes (DTNs) are hosts specifically designed to provide optimized data transfer between OLCF systems and systems outside of the OLCF network. These nodes perform well on local-area transfers as well as the wide-area data transfers for which they are tuned. The OLCF recommends that users use these nodes to improve transfer speed and reduce load on computational systems’ login and service nodes. OLCF provides two sets of DTNs: one for systems in our moderate enclave and a second for systems in the open enclave.

.. _dtn-access-connecting:

Interactive Access
==================

DTN access is automatically granted to all enabled OLCF users. For interactive access to DTNs (``ssh``/``scp``/``sftp``), connect to ``dtn.ccs.ornl.gov`` (for the moderate enclave) or ``opendtn.ccs.ornl.gov`` (for the open enclave). For example:

::

    ssh username@dtn.ccs.ornl.gov

For more information on connecting to OLCF resources, see :ref:`connecting-to-olcf`.

Access From Globus Online
=========================

DTNs are also accessible via the "OLCF DTN" (for moderate) and "NCCS Open DTN" (for open) Globus endpoints. For more information on using Globus at OLCF see :ref:`data-transferring-data-globus`.


Batch Queue (Slurm)
===================

The moderate DTNs also support batch jobs. The system contains 8 nodes accessible through the DTN batch system.

Most OLCF resources now use the Slurm batch scheduler, including the DTNs.
Below is a table of useful commands for Slurm.

+--------------------------------------------+-------------------+
| Task                                       | Slurm             |
+============================================+===================+
| View batch queue                           | ``squeue``        |
+--------------------------------------------+-------------------+
| Submit batch script                        | ``sbatch``        |
+--------------------------------------------+-------------------+
| Submit interactive batch job               | ``salloc``        |
+--------------------------------------------+-------------------+

Queue Policy
^^^^^^^^^^^^^^^^^^^^

+------------+-------------+-------------------------------------------+
| Node Count |  Duration   |  Policy                                   |
+============+=============+===========================================+
| 1-4 Nodes  |  0 - 24 hrs |     max 1 job running **per user**        |
+------------+-------------+-------------------------------------------+

Submitting jobs to Frontier
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Submitting to the Frontier batch queue is supported from the moderate DTNs using the ``-M`` flag; however, we will need to ensure that the programming environment is not inheritied from the DTNs. The ``--export=NONE`` sbatch submission flag in combination with the ``SLURM_EXPORT_ENV`` environment variable should prevent the DTN environment from copying to the job, but does not wipe the environment on the compute nodes.  

+--------------------------------------+
| Submission Line                      |
+======================================+
| sbatch -M frontier --export=NONE ... |
+--------------------------------------+

+-----------------------------+
| Inside of the slurm script: |
+=============================+
| export SLURM_EXPORT_ENV=ALL |
+-----------------------------+

We will also need to use the SBATCH directive ``threads-per-core`` to alter the DTNs default setting to match Frontier's default setting.
::

	#SBATCH --threads-per-core=1







