.. _policy:

*******
Policy
*******



A brief description of each area and basic guidelines to follow are provided in
the table below:

{{ mk_tbl(Filesystems, "area", "path", "type", "permissions", "backups", "purged", "quota", "compute node access") }}


On Summit paths to the various project-centric work storage areas are simplified
by the use of environment variables that point to the proper directory on a
per-user basis:

- Member Work Directory:  ``$MEMBERWORK = /gpfs/alpine/scratch/[userid]``
- Project Work Directory: ``$PROJWORK = /gpfs/alpine/proj-shared``
- World Work Directory: ``$WORLDWORK = /gpfs/alpine/world-shared``

Information
============

- Although there are no hard quota limits for the project storage, an upper
  storage limit should be reported in the project request. The available space
  of a project can be modified upon request.

Purge
======

To keep the Spectrum Scale file system exceptionally performant, files that have
not been accessed in the project and user areas are purged at the intervals
shown in the table above. Please make sure that valuable data is moved off of
these systems regularly. See :ref:`hpss`. for information about using the HSI
and HTAR utilities to archive data on HPSS. Just to note that when you read a
file, then the 90 days counter restarts.

Data Retention
==============

By default, the OLCF does not guarantee lifetime data retention on any OLCF
resources. Following a user account deactivation or project end, user and
project data in non-purged areas will be retained for 90 days. After this
timeframe, the OLCF retains the right to delete data. Data in purged areas
remains subject to normal purge policies.
