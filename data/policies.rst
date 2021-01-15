.. _policy:

*******
Policy
*******



A brief description of each area and basic guidelines to follow are provided in
the table below:

+---------------------+---------------------------------------------+----------------+-------------+--------+---------+---------+------------+------------------+
| Area                | Path                                        | Type           | Permissions |  Quota | Backups | Purged  | Retention  | On Compute Nodes |
+=====================+=============================================+================+=============+========+=========+=========+============+==================+
| User Home           | ``/ccs/home/[userid]``                      | NFS            | User set    |  50 GB | Yes     | No      | 90 days    | Read-only        |
+---------------------+---------------------------------------------+----------------+-------------+--------+---------+---------+------------+------------------+
| User Archive [#f1]_ | ``/home/[userid]``                          | HPSS           | User set    |  2TB   | No      | No      | 90 days    | No               |
+---------------------+---------------------------------------------+----------------+-------------+--------+---------+---------+------------+------------------+
| User Archive [#f2]_ | ``/home/[userid]``                          | HPSS           | 700         |  N/A   | N/A     | N/A     | N/A        | No               |
+---------------------+---------------------------------------------+----------------+-------------+--------+---------+---------+------------+------------------+
| Project Home        | ``/ccs/proj/[projid]``                      | NFS            | 770         |  50 GB | Yes     | No      | 90 days    | Read-only        |
+---------------------+---------------------------------------------+----------------+-------------+--------+---------+---------+------------+------------------+
| Member Work         | ``/gpfs/alpine/[projid]/scratch/[userid]``  | Spectrum Scale | 700 [#f3]_  |  50 TB | No      | 90 days | N/A [#f4]_ | Yes              |
+---------------------+---------------------------------------------+----------------+-------------+--------+---------+---------+------------+------------------+
| Project Work        | ``/gpfs/alpine/[projid]/proj-shared``       | Spectrum Scale | 770         |  50 TB | No      | 90 days | N/A [#f4]_ | Yes              |
+---------------------+---------------------------------------------+----------------+-------------+--------+---------+---------+------------+------------------+
| World Work          | ``/gpfs/alpine/[projid]/world-shared``      | Spectrum Scale | 775         |  50 TB | No      | 90 days | N/A [#f4]_ | Yes              |
+---------------------+---------------------------------------------+----------------+-------------+--------+---------+---------+------------+------------------+
| Member Archive      | ``/hpss/prod/[projid]/users/$USER``         | HPSS           | 700         | 100 TB | No      | No      | 90 days    | No               |
+---------------------+---------------------------------------------+----------------+-------------+--------+---------+---------+------------+------------------+
| Project Archive     | ``/hpss/prod/[projid]/proj-shared``         | HPSS           | 770         | 100 TB | No      | No      | 90 days    | No               |
+---------------------+---------------------------------------------+----------------+-------------+--------+---------+---------+------------+------------------+
| World Archive       | ``/hpss/prod/[projid]/world-shared``        | HPSS           | 775         | 100 TB | No      | No      | 90 days    | No               |
+---------------------+---------------------------------------------+----------------+-------------+--------+---------+---------+------------+------------------+

| *Area -* The general name of storage area.
| *Path -* The path (symlink) to the storage area's directory.
| *Type -* The underlying software technology supporting the storage area.
| *Permissions -* UNIX Permissions enforced on the storage area's top-level directory.
| *Quota -* The limits placed on total number of bytes and/or files in the storage area.
| *Backups -* States if the data is automatically duplicated for disaster recovery purposes.
| *Purged -* Period of time, post-file-access, after which a file will be marked as eligible for permanent deletion.
| *Retention -* Period of time, post-account-deactivation or post-project-end, after which data will be marked as eligible for permanent deletion.
| *On Compute Nodes -* Is this filesystem available on compute nodes (yes, no, or available but read-only)

    **Important!** Files within "Work" directories (i.e., Member Work,
    Project Work, World Work) are *not* backed up and are *purged* on a
    regular basis according to the timeframes listed above.

.. rubric:: Footnotes

.. [#f1] This entry is for legacy User Archive directories which contained user data on January 14, 2020.

.. [#f2] User Archive directories that were created (or had no user data) after January 14, 2020. Settings other than permissions are not applicable because directories are root-owned and contain no user files.

.. [#f3] Permissions on Member Work directories can be controlled to an extent by project members. By default, only the project member has any accesses, but accesses can be granted to other project members by setting group permissions accordingly on the Member Work directory. The parent directory of the Member Work directory prevents accesses by "UNIX-others" and cannot be changed (security measures).

.. [#f4] Retention is not applicable as files will follow purge cycle.



On Summit, Andes, and the DTNs, additional paths to the various project-centric work areas are available
via the following symbolic links and/or environment variables:

- Member Work Directory:  ``/gpfs/alpine/scratch/[userid]/[projid]`` or ``$MEMBERWORK/[projid]``
- Project Work Directory: ``/gpfs/alpine/proj-shared/[projid]`` or ``$PROJWORK/[projid]``
- World Work Directory: ``/gpfs/alpine/world-shared/[projid]`` or ``$WORLDWORK/[projid]``

Information
============

Although there are no hard quota limits for the project storage, an upper
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

Special Requests
================

If you need an exception to the limits listed in the table above, such as a higher quota in your User/Project Home or a purge exemption in a Member/Project/World Work area, contact help@olcf.ornl.gov with a summary of the exception that you need.

Data Retention
==============

By default, the OLCF does not guarantee lifetime data retention on any OLCF
resources. Following a user account deactivation or project end, user and
project data in non-purged areas will be retained for 90 days. After this
timeframe, the OLCF retains the right to delete data. Data in purged areas
remains subject to normal purge policies.
