******************
Storage Overview
******************


OLCF users have many options for data storage. Each user has multiple
user-affiliated storage spaces, and each project has multiple project-affiliated
storage spaces where data can be shared for collaboration.  Below we give an
overview and explain where each storage area is mounted.


Storage Areas
=============

The storage area to use in any given situation depends upon the activity you
wish to carry out. Each user has a User Home area on a Network File System (NFS)
and a User Archive area on the archival High Performance Storage System (HPSS).
These user storage areas are intended to house user-specific files. Each project
has a Project Home area on NFS, multiple Project Work areas on Spectrum Scale,
and a Project Archive area on HPSS. These project storage areas are intended to
house project-centric files. We have defined several areas as listed below by
function:

- **User Home:** Long-term data for routine access that is unrelated to a
  project. It is mounted on compute nodes of Summit as read only

- **User Archive:** Long-term data for archival access that is unrelated to a
  project.

- **Project Home:** Long-term project data for routine access that's shared
  with other project members. It is mounted on compute nodes of Summit as read
  only

- **Member Work:** Short-term user data for fast, batch-job access that is not
  shared with other project members.

- **Project Work:** Short-term project data for fast, batch-job access that's
  shared with other project members.

- **World Work:** Short-term project data for fast, batch-job access that's
  shared with OLCF users outside your project.

- **Project Archive:** Long-term project data for archival access that's shared
  with other project members.


.. _alpine-ibm-spectrum-scale-filesystem:

Alpine IBM Spectrum Scale Filesystem
=====================================

Summit mounts a POSIX-based IBM Spectrum Scale parallel filesystem called
Alpine. Alpine's maximum capacity is 250 PB. It is consisted of 77 IBM Elastic
Storage Server (ESS) GL4 nodes running IBM Spectrum Scale 5.x which are called
Network Shared Disk (NSD) servers. Each IBM ESS GL4 node, is a scalable storage
unit (SSU), constituted by two dual-socket IBM POWER9 storage servers, and a 4X
EDR InfiniBand network for up to 100Gbit/sec of networking bandwidth.  The
maximum performance of the final production system will be about 2.5 TB/s for
sequential I/O and 2.2 TB/s for random I/O under FPP mode, which means each
process, writes its own file. Metada operations are improved with around to
minimum 50,000 file access per sec and aggregated up to 2.6 million accesses of
32KB small files.  


.. figure:: /images/summit_nds_final.png
   :align: center

   Figure 1. An example of the NDS servers on Summit

Performance under not ideal workload
------------------------------------

The I/O performance can be lower than the optimal one when you save one single
shared file with non-optimal I/O pattern. Moreover, the previous performance
results are achieved under an ideal system, the system is dedicated, and a
specific number of compute nodes are used. The file system is shared across many
users; the I/O performance can vary because other users that perform heavy I/O
as also executing large scale jobs and stress the interconnection network.
Finally, if the I/O pattern is not aligned, then the I/O performance can be
significantly lower than the ideal one.  Similar, related to the number of the
concurrent users, is applied for the metadata operations, they can be lower than
the expected performance.

Tips
-----

- For best performance on the IBM Spectrum Scale filesystem, use large page
  aligned I/O and asynchronous reads and writes. The filesystem blocksize is
  16MB, the minimum fragment size is 16K so when a file under 16K is stored, it
  will still use 16K of the disk. Writing files of 16 MB or larger, will achieve
  better performance. All files are striped across LUNs which are distributed
  across all IO servers.

- If your application occupies up to two compute nodes and it requires a
  significant number of I/O operations, you could try to add the following flag
  in your job script  file and investigate if the total execution time is
  decreased. This flag could cause worse results, it depends on the application.

                   ``#BSUB -alloc_flags maximizegpfs``

Major difference between Lustre and IBM Spectrum Scale
-------------------------------------------------------

The file systems have many technical differences, but we will mention only what
a user needs to be familiar with:

- On Summit, there is no concept of striping from the user point of view, the
  user uses the Alpine storage without the need to declare the striping for
  files/directories. The GPFS will handle the workload, the file system was
  tuned during the installation.


