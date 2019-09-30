.. _policy:

*******
Policy
*******



A brief description of each area and basic guidelines to follow are provided in
the table below:

+-------------------+---------------------------------------------+---------------------------+-------------+---------+---------+-------+--------------------------+
| *Name*            |   Path                                      |     Type                  | Permissions | Backups |  Purged | Quota | Mounted on Compute nodes |
+===================+=============================================+===========================+=============+=========+=========+=======+==========================+
| *User Home*       |   ``$HOME``                                 |     NFS                   |   User Set  |    yes  |    no   | 50GB  |   Read-only              |
+-------------------+---------------------------------------------+---------------------------+-------------+---------+---------+-------+--------------------------+
| *Project Home*    | ``/ccs/proj/[projid]``                      |     NFS                   |      770    |    yes  |    no   |  50GB |  Read-only               |
+-------------------+---------------------------------------------+---------------------------+-------------+---------+---------+-------+--------------------------+
| *User Archive*    | ``/home/$USER``                             |     HPSS                  |   User Set  |    no   |    no   |  2TB  |    No                    |
+-------------------+---------------------------------------------+---------------------------+-------------+---------+---------+-------+--------------------------+
| *Project Archive* | ``/proj/[projid]``                          |     HPSS                  |      770    |    no   |    no   | 100TB |     No                   |
+-------------------+---------------------------------------------+---------------------------+-------------+---------+---------+-------+--------------------------+
| *Member Work*     | ``/gpfs/alpine/scratch/[userid]/[projid]/`` | Spectrum Scale (ex. GPFS) |      700    |    no   | 90 days |  50TB |  Yes                     |
+-------------------+---------------------------------------------+---------------------------+-------------+---------+---------+-------+--------------------------+
| *Project Work*    | ``/gpfs/alpine/proj-shared/[projid]``       | Spectrum Scale (ex. GPFS) |      770    |    no   | 90 days |  50TB |  Yes                     |
+-------------------+---------------------------------------------+---------------------------+-------------+---------+---------+-------+--------------------------+
| *World Work*      | ``/gpfs/alpine/world-shared/[projid]``      | Spectrum Scale (ex. GPFS) |      775    |    no   | 90 days |  50TB |  Yes                     |
+-------------------+---------------------------------------------+---------------------------+-------------+---------+---------+-------+--------------------------+


On Summit paths to the various project-centric work storage areas are simplified
by the use of environment variables that point to the proper directory on a
per-user basis:

- Member Work Directory:  ``$MEMBERWORK/[projid]``
- Project Work Directory: ``$PROJWORK/[projid]``
- World Work Directory: ``$WORLDWORK/[projid]``

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
