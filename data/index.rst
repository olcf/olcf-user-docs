.. _data-storage-and-transfers:

############################
Data Storage and Transfers
############################

OLCF users have many options for data storage. Each user has multiple user-affiliated storage spaces, and each project has multiple project-affiliated storage spaces where data can be shared for collaboration.  Below we give an overview and explain where each storage area is mounted.

************************
Summary of Storage Areas
************************

The storage area to use in any given situation depends upon the activity you wish to carry out. Storage areas are either user-centric or project-centric, and are further divided by the underlying storage type (e.g., Network File System (NFS), IBM Spectrum Scale, Nearline). Each storage type has a different intended use as described below.

Each user has a User Home area on NFS. Each project has a Project Home area on NFS, and multiple Work areas on Spectrum Scale/Lustre. Moderate projects each have an archival storage area on Kronos with project-shared, world-shared, and users directories (each of these 3 areas share a 200TB total Archival quota). The different storage areas are summarized in the list and table below.

- **User Home:** Long-term data for routine access that is unrelated to a project. It is mounted as read/write on the Frontier compute nodes, but we strongly recommend that users launch and run jobs from the Orion parallel filesystem due to its larger storage capacity and superior performance.
- **Project Home:** Long-term project data for routine access that's shared with other project members. It is mounted as read/write on the Frontier compute nodes, but we strongly recommend that users launch and run jobs from the Orion parallel filesystem due to its larger storage capacity and superior performance.
- **Member Work:** Short-term user data for fast, batch-job access that is not shared with other project members.
- **Project Work:** Short-term project data for fast, batch-job access that's shared with other project members.
- **World Work:** Short-term project data for fast, batch-job access that's shared with users outside your project.
- **Member Archive:** Long-term project data for archival access that is not shared with other project members.
- **Project Archive:** Long-term project data for archival access that's shared with other project members.
- **World Archive:** Long-term project data for archival access that's shared with users outside your project.

.. _data-filesystem-summary:

+--------------------------------+---------------------------------------------+---------+------------------------+-------------+-----------+---------+---------+------------+-----------------------------------------+
| Area                           | Path                                        | Enclave | Type                   | Permissions |   Quota   | Backups | Purged  | Retention  | On Compute Nodes                        |
+================================+=============================================+=========+========================+=============+===========+=========+=========+============+=========================================+
| User Home                      | ``/ccs/home/[userid]``                      | M1, M2  | NFS                    | User set    |   50 GB   | Yes     | No      | 90 days    | Frontier: Read/Write                    |
+--------------------------------+---------------------------------------------+---------+------------------------+-------------+-----------+---------+---------+------------+-----------------------------------------+
| User Archive                   | ``/nl/kronos/olcf/[projid]/users/[userid]`` | M1      | Nearline               | User set    |  200 TB*  | Yes     | No      | 90 days    | No                                      |
+--------------------------------+---------------------------------------------+---------+------------------------+-------------+-----------+---------+---------+------------+-----------------------------------------+
| Project Home                   | ``/ccs/proj/[projid]``                      | M1, M2  | NFS                    | 770         |   50 GB   | Yes     | No      | 90 days    | Frontier: Read/Write                    |
+--------------------------------+---------------------------------------------+---------+------------------------+-------------+-----------+---------+---------+------------+-----------------------------------------+
| Orion Member Work              | ``/lustre/orion/[projid]/scratch/[userid]`` | M1, M2  | Lustre HPE ClusterStor | 700         |   50 TB   | No      | 90 days | N/A [#f4]_ | Read/Write                              |
+--------------------------------+---------------------------------------------+---------+------------------------+-------------+-----------+---------+---------+------------+-----------------------------------------+
| Orion Project Work             | ``/lustre/orion/[projid]/proj-shared``      | M1, M2  | Lustre HPE ClusterStor | 770         |   50 TB   | No      | 90 days | N/A [#f4]_ | Read/Write                              |
+--------------------------------+---------------------------------------------+---------+------------------------+-------------+-----------+---------+---------+------------+-----------------------------------------+
| Orion World Work               | ``/lustre/orion/[projid]/world-shared``     | M1      | Lustre HPE ClusterStor | 775         |   50 TB   | No      | 90 days | N/A [#f4]_ | Read/Write                              |
+--------------------------------+---------------------------------------------+---------+------------------------+-------------+-----------+---------+---------+------------+-----------------------------------------+
| Alpine2 Member Work            | ``/gpfs/alpine2/[projid]/scratch/[userid]`` | M1, M2  | Spectrum Scale         | 700 [#f3]_  |   50 TB   | No      | 90 days | N/A [#f4]_ | Read/Write                              |
+--------------------------------+---------------------------------------------+---------+------------------------+-------------+-----------+---------+---------+------------+-----------------------------------------+
| Alpine2 Project Work           | ``/gpfs/alpine2/[projid]/proj-shared``      | M1, M2  | Spectrum Scale         | 770         |   50 TB   | No      | 90 days | N/A [#f4]_ | Read/Write                              |
+--------------------------------+---------------------------------------------+---------+------------------------+-------------+-----------+---------+---------+------------+-----------------------------------------+
| Alpine2 World Work             | ``/gpfs/alpine2/[projid]/world-shared``     | M1      | Spectrum Scale         | 775         |   50 TB   | No      | 90 days | N/A [#f4]_ | Read/Write                              |
+--------------------------------+---------------------------------------------+---------+------------------------+-------------+-----------+---------+---------+------------+-----------------------------------------+
| Project Archive                | ``/nl/kronos/olcf/[projid]/proj-shared``    | M1      | Nearline               | 770         |  200 TB*  | No      | No      | 90 days    | No                                      |
+--------------------------------+---------------------------------------------+---------+------------------------+-------------+-----------+---------+---------+------------+-----------------------------------------+
| World Archive                  | ``/nl/kronos/olcf/[projid]/world-shared``   | M1      | Nearline               | 775         |  200 TB*  | No      | No      | 90 days    | No                                      |
+--------------------------------+---------------------------------------------+---------+------------------------+-------------+-----------+---------+---------+------------+-----------------------------------------+
| Moderate Enhanced User Home    | ``/gpfs/arx/[projid]/home/[userid]``        | ME      | Spectrum Scale         | 700         |   50 TB   | No      | 90 days | N/A [#f4]_ | Read/Write                              |
+--------------------------------+---------------------------------------------+---------+------------------------+-------------+-----------+---------+---------+------------+-----------------------------------------+
| Moderate Enhanced Member Work  | ``/gpfs/arx/[projid]/scratch/[userid]``     | ME      | Spectrum Scale         | 700         |   50 TB   | No      | 90 days | N/A [#f4]_ | Read/Write                              |
+--------------------------------+---------------------------------------------+---------+------------------------+-------------+-----------+---------+---------+------------+-----------------------------------------+
| Moderate Enhanced Project Work | ``/gpfs/arx/[projid]/proj-shared/[userid]`` | ME      | Spectrum Scale.        | 770         |   50 TB   | No      | 90 days | N/A [#f4]_ | Read/Write                              |
+--------------------------------+---------------------------------------------+---------+------------------------+-------------+-----------+---------+---------+------------+-----------------------------------------+
| Open User Home                 | ``/ccsopen/home/[userid]``                  | O       | NFS                    | User set    |   50 GB   | Yes     | No      | 90 days    | Read-only                               |
+--------------------------------+---------------------------------------------+---------+------------------------+-------------+-----------+---------+---------+------------+-----------------------------------------+
| Open Project Home              | ``/ccsopen/proj/[projid]``                  | O       | NFS                    | 770         |   50 GB   | Yes     | No      | 90 days    | Read-only                               |
+--------------------------------+---------------------------------------------+---------+------------------------+-------------+-----------+---------+---------+------------+-----------------------------------------+
| Open Member Work               | ``/gpfs/wolf/[projid]/scratch/[userid]``    | O       | Spectrum Scale         | 700 [#f3]_  |   50 TB   | No      | 90 days | N/A [#f4]_ | Read/Write                              |
+--------------------------------+---------------------------------------------+---------+------------------------+-------------+-----------+---------+---------+------------+-----------------------------------------+
| Open Project Work              | ``/gpfs/wolf/[projid]/proj-shared``         | O       | Spectrum Scale         | 770         |   50 TB   | No      | 90 days | N/A [#f4]_ | Read/Write                              |
+--------------------------------+---------------------------------------------+---------+------------------------+-------------+-----------+---------+---------+------------+-----------------------------------------+
| Open World Work                | ``/gpfs/wolf/[projid]/world-shared``        | O       | Spectrum Scale         | 775         |   50 TB   | No      | 90 days | N/A [#f4]_ | Read/Write                              |
+--------------------------------+---------------------------------------------+---------+------------------------+-------------+-----------+---------+---------+------------+-----------------------------------------+

.. note::
   The three archival storage areas share a single project-centric 200TB quota.

| **Area -** The general name of the storage area.
| **Path -** The path (symlink) to the storage area's directory.
| **Enclave -** The security enclave where the path is available. There are several security enclaves:
|      - *Open (O) -* Ascent and other OLCF machines accessible with a username/password
|      - *Moderate Projects not subject to export control (M1)* - These are projects on machines such as Frontier or Andes that require 2-factor authentication but are not subject to export control restrictions.
|      - *Moderate Projects subject to export control (M2) -* Same as M1, but projects that are subject to export control restrictions.
|      - *Moderated Enhanced (ME) -* These are projects that might involve HIPAA or ITAR regulations. These projects utilize Frontier compute resources but have extra security precautions and separate file systems.
| **Type -** The underlying software technology supporting the storage area.
| **Permissions -** UNIX Permissions enforced on the storage area's top-level directory.
| **Quota -** The limits placed on total number of bytes and/or files in the storage area.
| **Backups -** States if the data is automatically duplicated for disaster recovery purposes.
| **Purged -** Period of time, post-file-access, after which a file will be marked as eligible for permanent deletion.
| **Retention -** Period of time, post-account-deactivation or post-project-end, after which data will be marked as eligible for permanent deletion.
| **On Compute Nodes -** Is this filesystem available on compute nodes (no, available but read-only, and available read/write)

.. important::
    Files within "Work" directories (i.e., Member Work, Project Work, World Work) are *not* backed up and are *purged* on a regular basis according to the timeframes listed above.

.. tip::
    If your home directory reaches its quota, your batch jobs might fail with the error ``cat: write error: Disk quota exceeded``. This error may not be intuitive, especially if your job exclusively uses work areas that are well under quota. The error is actually related to your home directory quota. Sometimes, batch systems write temporary files to the home directory, so if the home directory is over quota and that file creation fails, the job will fail with the quota error.

    You can check your home directory quota with the ``quota`` command. If it is over quota, you need to bring usage under the quota and then your jobs should run without encountering the ``Disk quota exceeded`` error.

.. rubric:: Footnotes

.. [#f3] Permissions on Member Work directories can be controlled to an extent by project members. By default, only the project member has any accesses, but accesses can be granted to other project members by setting group permissions accordingly on the Member Work directory. The parent directory of the Member Work directory prevents accesses by "UNIX-others" and cannot be changed.

.. [#f4] Retention is not applicable as files will follow purge cycle.


.. On Frontier, Andes, and the DTNs, additional paths to the various project-centric work areas are available via the following symbolic links and/or environment variables:

.. - Member Work Directory:  ``/gpfs/alpine/scratch/[userid]/[projid]`` or ``$MEMBERWORK/[projid]``
.. - Project Work Directory: ``/gpfs/alpine/proj-shared/[projid]`` or ``$PROJWORK/[projid]``
.. - World Work Directory: ``/gpfs/alpine/world-shared/[projid]`` or ``$WORLDWORK/[projid]``

On Frontier additional paths to the various project-centric work areas are available via the following symbolic links and/or environment variables:

- Member Work Orion Directory:  ``/lustre/orion/scratch/[userid]/[projid]`` or ``$MEMBERWORK/[projid]``
- Project Work Orion  Directory: ``/lustre/orion/proj-shared/[projid]`` or ``$PROJWORK/[projid]``
- World Work Orion Directory: ``/lustre/orion/world-shared/[projid]`` or ``$WORLDWORK/[projid]``



.. _data-user-centric-areas:

==================================
Notes on User-Centric Data Storage
==================================

.. _data-user-home-directories-nfs:

User Home Directories (NFS)
===========================

The environment variable ``$HOME`` will always point to your current home directory. It is recommended, where possible, that you use this variable to reference your home directory. In cases in which using ``$HOME`` is not feasible, it is recommended that you use ``/ccs/home/$USER`` (or ``/ccsopen/home/$USER`` for home directories in the open enclave).

Users should note that since this is an NFS-mounted filesystem, its performance will not be as high as other filesystems.

User Home Quotas
----------------

Quotas are enforced on user home directories. To request an increased quota, contact the OLCF User Assistance Center. To view your current quota and usage, use the ``quota`` command:


.. code::

    $ quota -Qs
    Disk quotas for user usrid (uid 12345):
         Filesystem  blocks   quota   limit   grace   files   quota   limit   grace
    nccsfiler1a.ccs.ornl.gov:/vol/home
                      4858M   5000M   5000M           29379   4295m   4295m

.. note::
   Moderate enhanced projects home directores are located in GPFS. There is no enforced quota, but it is recommended that users not exceed 50 TB. These directories are subject to the 90 day purge.


.. tip::
   To find your project quota, you use the ``df`` command as described in :ref:`project-quota`, instead of the ``quota`` command.

User Home Permissions
---------------------

The default permissions for user home directories is shown in the :ref:`Filesystem Summary Table <data-filesystem-summary>`. Users have the ability to change permissions on their home directories, although it is recommended that permissions be set to as restrictive as possible (without interfering with your work).

.. note::
   Moderate enhanced projects have home directory permissions set to ``0700`` and are automatically reset to that if changed by the user.

User Home Backups
-----------------

If you accidentally delete files from your home directory, you may be able to retrieve them. Online backups are performed at regular intervals. Hourly backups for the past 24 hours, daily backups for the last 7 days, and once-weekly backups are available. It is possible that the deleted files are available in one of those backups. The backup directories are named ``hourly.*``, ``daily.*``, and ``weekly.*`` where ``*`` is the date/time stamp of backup creation. For example, ``hourly.2020-01-01-0905`` is an hourly backup made on January 1st, 2020 at 9:05 AM.

The backups are accessed via the ``.snapshot`` subdirectory. Note that ``ls`` alone (or even ``ls -a``) will not show the ``.snapshot`` subdirectory exists, though ``ls .snapshot`` will show its contents. The ``.snapshot`` feature is available in any subdirectory of your home directory and will show the online backups available for that subdirectory. 

To retrieve a backup, simply copy it into your desired destination with the ``cp`` command.

.. note::
   There are no backups for moderate enhanced project home directories.

User Website Directory
----------------------

Users interested in sharing files publicly via the World Wide Web can request a user website directory be created for their account. User website directories (``~/www``) have a 5GB storage quota and allow access to files at ``http://users.nccs.gov/~user`` (where ``user`` is your userid). If you are interested in having a user website directory created, please contact the User Assistance Center at help@olcf.ornl.gov.

.. _data-project-centric-areas:

=====================================
Notes on Project-Centric Data Storage
=====================================


Project directories provide members of a project with a common place to store code, data, and other files related to their project.

.. _data-project-home-directories-nfs:

Project Home Directories (NFS)
==============================

Open and Moderate Projects are provided with a Project Home storage area in the NFS-mounted filesystem. This area is intended for storage of data, code, and other files that are of interest to all members of a project. Since Project Home is an NFS-mounted filesystem, its performance will not be as high as other filesystems. 

.. note::
   Moderate Enhanced projects are not provided with Project Home spaces, just Project Work spaces.


.. _project-quota:

Project Home Path, Quota, and Permissions
-----------------------------------------

The path, quota, and permissions for Project Home directories are summarized in the :ref:`Filesystem Summary Table <data-filesystem-summary>`.

Quotas are enforced on Project Home directories. To check a Project Home directory’s usage, run ``df -h /ccs/proj/[projid]`` (where ``[projid]`` is the project ID). Note, however, that permission settings on some subdirectories may prevent you from accessing them, and in that case you will not be able to obtain the correct usage. If this is the case, contact help@olcf.ornl.gov for the usage information.

Project Home directories are root-owned and are associated with the project's Unix group. Default permissions are set such that only members of the project can access the directory, and project members are not able to change permissions of the top-level directory.

Project Home Backups
--------------------

If you accidentally delete files from your project home directory, you may be able to retrieve them. Online backups are performed at regular intervals.  Hourly backups for the past 24 hours, daily backups for the last 7 days, and once-weekly backups are available. It is possible that the deleted files are available in one of those backups. The backup directories are named ``hourly.*``, ``daily.*``, and ``weekly.*`` where ``*`` is the date/time stamp of backup creation. For example, ``hourly.2020-01-01-0905`` is an hourly backup made on January 1st, 2020 at
9:05 AM.

The backups are accessed via the ``.snapshot`` subdirectory. Note that ``ls`` alone (or even ``ls -a``) will not show the ``.snapshot`` subdirectory exists, though ``ls .snapshot`` will show its contents. The ``.snapshot`` feature is available in any subdirectory of your project home directory and will show the online backups available for that subdirectory.

To retrieve a backup, simply copy it into your desired destination with the ``cp`` command.

Project Work Areas
==================

Three Project Work Areas to Facilitate Collaboration
----------------------------------------------------

To facilitate collaboration among researchers, the OLCF provides (3) distinct types of project-centric work storage areas: *Member Work* directories, *Project Work* directories, and *World Work* directories.  Each directory should be used for storing files generated by computationally-intensive HPC jobs related to a project. 

.. note::
   - Moderate enhanced projects do not have World Work directories and the filesystem is called "arx" rather than "alpine"
   - Moderate projects subject to export control do not have World Work directories
   - Open projects' work areas are in the "wolf" filesystem rather than "alpine"

The difference between the three storage areas lies in the accessibility of the data to project members and to researchers outside of the project. Member Work directories are accessible only by an individual project member by default. Project Work directories are accessible by all project members.  World Work directories are potentially readable by any user on the system.

Permissions
-----------

UNIX Permissions on each project-centric work storage area differ according to the area’s intended collaborative use. Under this setup, the process of sharing data with other researchers amounts to simply ensuring that the data resides in the proper work directory.

-  Member Work Directory: ``700``
-  Project Work Directory: ``770``
-  World Work Directory: ``775``

For example, if you have data that must be restricted only to yourself, keep them in your Member Work directory for that project (and leave the default permissions unchanged). If you have data that you intend to share with researchers within your project, keep them in the project’s Project Work directory. If you have data that you intend to share with researchers outside of a project, keep them in the project’s World Work directory.

Backups
-------

Member Work, Project Work, and World Work directories **are not backed up**. Project members are responsible for backing up these files, either to Project Archive areas (:ref:`kronos`) or to an off-site location.

Project Archive Directories
===========================

Moderate projects without export control restrictions are also allocated project-specific archival space on :ref:`kronos`. The default quota is shown on the table at the top of this page (200TB). If a higher quota is needed, contact the User Assistance Center.

.. note::
    There is no archival storage for Moderate Enhanced Projects, Moderate Projects subject to export control, or Open projects.

Three Project Archive Areas Facilitate Collaboration on Archival Data
---------------------------------------------------------------------

To facilitate collaboration among researchers, the OLCF provides (3) distinct types of project-centric archival storage areas: *Member Archive* directories, *Project Archive* directories, and *World Archive* directories.  These directories should be used for storage of data not immediately needed in either the Project Home (NFS) areas or Project Work (Orion/Alpine2) areas and to serve as a location to store backup copies of project-related files.

As with the three project work areas, the difference between these three areas lies in the accessibility of data to project members and to researchers outside of the project. Member Archive directories are accessible only by an individual project member by default, Project Archive directories are accessible by all project members, and World Archive directories are readable by any user on the system.

All three  archival storage areas above share a single 200TB project-centric quota on Kronos.

Permissions
-----------

UNIX Permissions on each project-centric archive storage area differ according to the area’s intended collaborative use. Under this setup, the process of sharing data with other researchers amounts to simply ensuring that the data resides in the proper archive directory.

-  Member Archive Directory: ``700``
-  Project Archive Directory: ``770``
-  World Archive Directory: ``775``

For example, if you have data that must be restricted only to yourself, keep them in your Member Archive directory for that project (and leave the default permissions unchanged). If you have data that you intend to share with researchers within your project, keep them in the project’s Project Archive directory. If you have data that you intend to share with researchers outside of a project, keep them in the project’s World Archive directory.

HPSS Project Archive Access
---------------------------

.. warning::
   On January 31, 2025, data remaining on the HPSS will no longer be accessible and will be **PERMANENTLY DELETED**. Following this date, the OLCF will no longer be able to retrieve data remaining on HPSS. Please do not wait to move needed data. For more information on migrating data from HPSS to Kronos (the center's new archival storage system) see the :ref:`hpss-migration` section.

Project Archive directories may only be accessed via utilities called HSI and HTAR. For more information on using HSI or HTAR, see the :ref:`data-hpss` section.

.. note::
   HPSS is now read-only. Users cannot transfer data into HPSS and should instead use :ref:`kronos`. For more information on migrating your files from HPSS to Kronos or another storage location, see the :ref:`hpss-migration` section.

Kronos Project Archive Access
-----------------------------

For information on accessing archival storage areas on Kronos, see the :ref:`kronos` section.

.. _data-policy:

*************
Data Policies
*************

===========
Information
===========

Although there are no hard quota limits for project storage, an upper storage limit should be reported in the project request. The available space of a project can be modified upon request.

================
Special Requests
================

If you need an exception to the limits listed in the table above, such as a higher quota in your User/Project Home or a purge exemption in a Member/Project/World Work area, contact help@olcf.ornl.gov with a summary of the exception that you need.

==============
Data Retention
==============

By default, the OLCF does not guarantee lifetime data retention on any OLCF resources. Following a user account deactivation or project end, user and project data in non-purged areas will be retained for 90 days. After this timeframe, the OLCF retains the right to delete data. Data in purged areas remains subject to normal purge policies.


.. _data-orion-lustre-hpe-clusterstor-filesystem:

***************************************
Orion Lustre HPE ClusterStor Filesystem 
***************************************

Frontier mounts Orion, a parallel filesystem based on Lustre and HPE ClusterStor, with a 679 PB usable namespace (/lustre/orion/). In addition to Frontier, Orion is available on the OLCF's data transfer nodes. Files older than 90 days are purged from Orion.

Orion is a cluster of servers with approximately 500 nodes. Each node plays a role in providing a POSIX namespace for users (/lustre/orion/). A file on Lustre consists of one or more components that may hit one or more servers. Lustre has a distributed lock management process for concurrent access to files or regions within files. 

Orion has three performance tiers:

* A flash-based performance tier of 5,400 nonvolatile memory express (NVMe) devices that provides 11.5 petabytes (PB) of capacity at peak read-write speeds of 10 TB/s.
* A hard-disk-based capacity tier that provides 679 PB at peak read speeds of 5.5 TB/s and peak write speeds of 4.6 TB/s.
* A flash-based metadata tier of 480 NVMe devices provides an additional capacity of 10 PB.

================================================
Orion Performance Tiers and File Striping Policy
================================================

Lustre, in addition to other servers and components, is composed of Objects Storage Targets (OSTs) on which the data for files is stored. A file may be "striped" or divided over multiple OSTs. Striping provides the ability to store files that are larger than the space available on any single OST and allows a larger I/O bandwidth than could be managed by a single OST. Striping is one of the main differences between Frontier's Orion Lustre and Summit's Alpine GPFS filesystems because GPFS has no concept of striping exposed to the user. For Orion, files are striped between object storage targets (OST) in the three capacity tiers to achieve the best performance. Below, we describe this automatic file striping policy and its motivations.

Orion uses a feature called Data-on-Metadata-Target (DoM), where a portion of the file is stored along with the file’s metadata. Currently, directories are configured to store up to the first 256 KB of a file on the metadata tier using DoM. This reduces contention and provides better performance for small file I/O. Orion uses a feature called Progressive File Layout (PFL) to change the striping of a file as it grows. For example, a file smaller than 8 MB will be striped to a single OST, and larger files will be striped across multiple OSTs, taking advantage of more hardware resources. As files grow larger, they are automatically striped between the storage tiers.
OLCF is refining the automatic file striping policy to optimize I/O performance for users.

.. note::
   Because of the complexity of file striping between Orion's performance tiers, users should refrain from attempting to manually control file striping, unless they are writing single files in excess of 512 GB in size. 

Some sufficiently large (>512 GB per file) single-shared-file workloads may benefit from explicit striping. Below are some reccomendations: 


+---------+--------------------------------------------+
| Size    | Stripe Command                             |
+=========+============================================+
| 512 GB+ | lfs setstripe -c 8 -p capacity -S 16M      |
+---------+--------------------------------------------+
| 1 TB+   | lfs setstripe -c 16 -p capacity -S 16M     |
+---------+--------------------------------------------+
| 8 TB+   | lfs setstripe -c 64 -p capacity -S 16M     |
+---------+--------------------------------------------+
| 16 TB+  | lfs setstripe -c 128 -p capacity -S 16M    |
+---------+--------------------------------------------+


.. note::
   When manually setting striping you must specify ``-p capacity`` with the stripe command. Otherwise, Orion defaults to using the performance tier, which isn't optimized for handling larger single files. 


If you feel that the default file striping on Orion or the recommended striping for large single-shared-file workloads is not meeting your needs, please contact OLCF-help so that we can work with you to understand your application's I/O performance.


============================================   
I/O Patterns that Benefit from File Striping
============================================

Lustre's file striping will most likely improve performance for applications that read or write to a single (or multiple) large shared files.

Striping will likely have little or no performance benefit for:

* Serial I/O, where a single processor performs all the I/O
* Multiple nodes perform I/O but access files at different times.
* Multiple nodes perform I/O simultaneously to different files that are small (each < 100 MB)
* I/O that uses one file per process

=====================
LFS setstripe wrapper
=====================

The OLCF provides a wrapper for the ``lfs setstripe`` command that simplifies the process of striping files. The wrapper will enforce that certain settings are used to ensure that striping is done correctly. This will help to ensure good performance for users as well as prevent filesystem issues that could arise from incorrect striping practices. The wrapper is accessible via the ``lfs-wrapper`` module and will soon be added to the default environment on Frontier. 

Orion is different than other Lustre filesystems that you may have used previously. To make effective use of Orion and to help ensure that the filesystem performs well for all users, it is important that you do the following:

* Use the `capacity` OST pool tier (e.g., ``lfs setstripe -p capacity``)
* Stripe across no more than 450 OSTs (e.g., ``lfs setstripe -c`` <= 450)

When the module is active in your environment, the wrapper will enforce the above settings. The wrapper will also do the following:

* If a user provides a stripe count of -1 (e.g., ``lfs setstripe -c -1``) the wrapper will set the stripe count to the maximum allowed by the filesystem (currently 450)
* If a user provides a stripe count of 0 (e.g., ``lfs setstripe -c 0``) the wrapper will use the OLCF default striping command which has been optimized by the OLCF filesystem managers: ``lfs setstripe -E 256K -L mdt -E 8M -c 1 -S 1M -p performance -z 64M -E 128G -c 1 -S 1M -z 16G -p capacity -E -1 -z 256G -c 8 -S 1M -p capacity``

Please contact the OLCF User Assistance Center if you have any questions about using the wrapper or if you encounter any issues.

========================
Lustre File Locking Tips
========================

File locking is the process of restricting only one process or user to access a file or region of a file. It prevents race conditions when writing data from multiple processes. Lustre uses a distributed lock management (LDLM) system for consistency and access. Concurrent operations on files/directories flow through this LDLM system.  Locks are generally managed on a per-client level and there are limits to the number of concurrent locks each client can have on each storage target (MDT/OST). While locking is good and necessary, certain I/O patterns can become very slow if they generate a large amount of lock contention. 

Here are some things to avoid to minimizing lock impact: 

* Multiple clients opening the same byte range of a file for writing 
* Multiple clients appending to the same file (subset of previous) 
* Multiple clients concurrently creating numerous files or directories in the same directory

If your code does any of these, you may want to adjust it to avoid or limit them and then test to see if that improves your write performance. 

=================================
Darshan-runtime and I/O Profiling
=================================

The darshan-runtime modulefile is part of DefApps and is loaded by default on Frontier. This module allows users to profile the I/O of their applications with minimal impact. The logs are available to users on the Orion file system in /lustre/orion/darshan/<system>/<yyyy>/<mm>/<dd>. 

Unloading darshan-runtime is recommended for users profiling their applications with other profilers to prevent conflicts.

=====
Purge
=====

To help ensure performance and availability for all projects, Orion is regularly purged. Files that have not been accessed (e.g., read) or modified within 90-days are eligible to be purged. **The purge runs continuously** as a rolling window, deleting data as it finds eligible files.

For example, let's say you have these files on Orion as of ``01/01/2025``:

.. code-block:: bash

    $ ls -l
    -rw-r--r--  1 ...  ...  ... Oct 2 2024 file1.txt (eligible to be purged on 1/1/25) (currently 91 days old)
    -rw-r--r--  1 ...  ...  ... Oct 3 2024 file2.txt (eligible to be purged on 1/2/25) (currently 90 days old)
    -rw-r--r--  1 ...  ...  ... Dec 1 2024 file3.txt (eligible to be purged on 3/2/25) (currently 31 days old)

Because ``file1.txt`` is over 90 days old, ``file1.txt`` will be purged "today".
Although ``file2.txt`` is safe "today", on January 2nd ("tomorrow"), ``file2.txt`` will be purged.
The purge will continuously run and it won't be until March 2nd that ``file3.txt`` will be purged (unless accessed or modified by that time).

Because Orion is considered scratch and not backed-up by the center, data owners should ensure needed data is regularly backed-up. See :ref:`kronos` for information about using the center's archival storage resource.

Temporary purge exmptions can be requested by contacting help@olcf.ornl.gov .

.. warning::
   Orion is a scratch filesystem.  Data that has not been accessed in 90-days are eligible for purge.  Data owners are responsible for backing up needed data.




.. _data-hpss:

**************************
HPSS Data Archival System
**************************

.. warning::
   On January 31, 2025, HPSS was decommissioned. The OLCF is no longer be able to retrieve data remaining on HPSS. 


.. _kronos:

***************************************
Kronos Nearline Archival Storage System
***************************************

Kronos is the center’s new nearline storage resource. Kronos is multi-tiered containing both disk and tape. Users will interact with the system’s disk sub-system which leverages IBM Storage Scale (GPFS). Data stored on the disk sub-system will automatically be stored on they system’s tape sub-system. The disk sub-system will provide an initial capacity of 134 PB with the ability to expand as need increases. Kronos is capable of bandwidth of up-to 200 GB/s from the center’s Data Transfer Nodes.

======================
Access / Data Transfer
======================

Kronos is mounted on the moderate security enclave Data Transfer Nodes (``dtn.ccs.ornl.gov``) and is accessible via `Globus <https://www.globus.org>`_ at the "**OLCF Kronos**" collection. Standard UNIX commands and tools can also be used to interact with Kronos (scp, rsync, etc.).

For more information on using `scp` and `rsync` to transfer data to and from OLCF resources, see the :ref:`clitools` section.

For more information on using Globus to transfer data to and from OLCF resources, see the :ref:`data-transferring-data-globus` section.

.. note::
   Kronos is only available through the "**OLCF Kronos**" Globus collection and is *NOT* accessible from the "OLCF DTN (Globus 5)" collection.

===================
Directory Structure
===================
Kronos uses a directory structure similar to other center-wide storage resources:

.. list-table::
   :widths: 20 12 12 12 80
   :header-rows: 1

   * - Path
     - Permissions
     - Owner
     - Group
     - Description
   * - ``/nl/kronos/olcf/<projectID>/proj-shared``
     - 755
     - root
     - <projectID> UNIX group
     - Data shared between project members.
   * - ``/nl/kronos/olcf/<projectID>/users/<userID>``
     - 700
     - <userID>
     - <projectID> UNIX group
     - User data, access is limited to user by default, but each user can modify their directory permissions to share with other project members.
   * - ``/nl/kronos/olcf/<projectID>/world-shared``
     - 2775
     - root
     - <projectID> UNIX group
     - Data accessible to others in the OLCF user community

==============
Project Quotas
==============

To help ensure available space for all Kronos projects, each project has a 200TB quota. All data stored in ``/nl/kronos/olcf/<projectID>`` will count toward the project’s quota. Please reach out to help@olcf.ornl.gov to request exemptions to the default quota.


==========================
Kronos and HPSS Comparison
==========================

.. list-table::
   :widths: 30 30 30
   :header-rows: 1

   * - Process
     - HPSS
     - Kronos
   * - Accessibility
     - DTNs and login nodes
     - DTNs
   * - Transfer tools
     - hsi, htar, globus
     - globus and standard UNIX transfer utilities
   * - File and directory management
     - hsi
     - standard UNIX utilities
   * - Data retrieval speeds
     - Fluctuates based on data location, can see delay if only stored on tape
     - All data stored on disk providing consistent access experience

.. _data-transferring-data:

******************
Transferring Data
******************

.. _data-transferring-data-globus:

============
Globus
============

Three Globus Collections have been established for OLCF resources. 

.. list-table::
   :header-rows: 1

   * - Globus Collection
     - Storage Areas

   * - OLCF DTN (Globus 5)
     - Moderate User/Project Home (NFS), Orion (Lustre), and Alpine2 (GPFS) filesystems

   * - OLCF Kronos
     - Kronos (Archival)

   * - NCCS Open DTN (Globus 5)
     - Open User/Project Home (NFS), Wolf2 (GPFS) filesystem

By selecting one of these collections and some offsite collection, you can use Globus to transfer data to/from that storage area at OLCF. By selecting the "OLCF DTN (Globus 5)" and "OLCF Kronos" collections, you can transfer data between Kronos and one of our other filesystems mounted on the DTNs. 

.. note::
   Globus v4 collections are no longer be supported. Please use the "OLCF DTN (Globus 5)", "OLCF Open DTN (Globus 5), and "OLCF Kronos" collections.

**Globus Warnings:** 

* Globus transfers do not preserve file permissions. Arriving files will have (rw-r--r--) permissions, meaning arriving files will have *user* read and write permissions and *group* and *world* read permissions. Note that the arriving files will not have any execute permissions, so you will need to use chmod to reset execute permissions before running a Globus-transferred executable.


* Globus will overwrite files at the destination with identically named source files. This is done without warning.

* Globus has restriction of 8 active transfers across all the users. Each user has a limit of 3 active transfers, so it is required to transfer a lot of data on each transfer than less data across many transfers. 

* If a folder is constituted with mixed files including thousands of small files (less than 1MB each one), it would be better to tar the small files.  Otherwise, if the files are larger, Globus will handle them. 


Using Globus to Move Data Between Collections 
=============================================

The following example is intended to help users move data to and from the Orion filesystem.
 
.. note::
  
 Globus does not preserve file permissions and will overwrite destination files with identically named source files without warning.
 

Below is a summary of the steps for data transfer using Globus:

1.	Login to `globus.org <https://www.globus.org>`_ using your globus ID and password. If you do not have a globusID, set one up here: 
`Generate a globusID <https://www.globusid.org/create?viewlocale=en_US>`_. 

2.	Once you are logged in, Globus will open the “File Manager” page. Click the left side “Collection” text field in the File Manager and type “OLCF DTN (Globus 5)”.

3.	When prompted, authenticate into the OLCF DTN (Globus 5) collection using your OLCF username and PIN followed by your RSA passcode.

4.	Click in the left side “Path” box in the File Manager and enter the path to your data on Orion. For example, `/lustre/orion/stf007/proj-shared/my_orion_data`. You should see a list of your files and folders under the left “Path” Box.

5.	Click on all files or folders that you want to transfer in the list. This will highlight them.

6.	Click on the right side “Collection” box in the File Manager and type the name of a second collection at OLCF or at another institution. You can transfer data between different paths on the Orion filesystem with this method too; Just use the OLCF DTN (Globus 5) collection again in the right side “Collection” box. 

7.	Click in the right side “Path” box and enter the path where you want to put your data on the second collection's filesystem. 

8.	Click the left "Start" button.

9.	Click on “Activity“ in the left blue menu bar to monitor your transfer. Globus will send you an email when the transfer is complete.


Using Globus From Your Local Workstation
========================================

Globus is most frequently used to facilitate data transfer between two institutional filesystems. However, it can also be used to facilitate data transfer involving an individual workstation or laptop. The following instructions demonstrate creating a local Globus collection on your computer. 

- Visit https://app.globus.org/collections/gcp, login into globus, and Install Globus Connect Personal, it is available for Windows, Mac, and Linux.

- Follow the given instructions for setting up an collection on your computer, noting the name of the collection that you setup. 

- Once the collection is setup and globus is installed on your computer, you can search for and access the collection from the globus web interface just like any other collection, however your computer must be connected to the internet and globus must be actively running on it for the transfer to happen.


==========
HSI
==========

.. note::
   HPSS is now read-only. Users cannot transfer data into HPSS and should instead use :ref:`kronos`. For more information on migrating your files from HPSS to Kronos or another storage location, see the :ref:`hpss-migration` section.

HSI (Hierarchial Storage Interface) is used to transfer data to/from OLCF systems and HPSS. When retrieving data from a tar archive larger than 1 TB, we recommend that you pull only the files that you need rather than the full archive.  Examples of this will be given in the :ref:`htar` section below. Issuing the command ``hsi`` will start HSI in interactive mode. Alternatively, you can use:

     ``hsi [options] command(s)``

...to execute a set of HSI commands and then return. To list you files on the HPSS, you might use:

     ``hsi ls``

``hsi`` commands are similar to ``ftp`` commands. For example, ``hsi get`` and ``hsi put`` are used to retrieve and store individual files, and ``hsi mget`` and ``hsi mput`` can be used to retrieve multiple files. To send a file to HPSS, you might use:

     ``hsi put a.out : /hpss/prod/[projid]/users/[userid]/a.out``

To retrieve one, you might use:

     ``hsi get /hpss/prod/[projid]/proj-shared/a.out``

Here is a list of commonly used hsi commands.

========== ====================================================================
Command    Function
========== ====================================================================
cd         Change current directory
get, mget  Copy one or more HPSS-resident files to local files
cget       Conditional get - get the file only if it doesn't already exist
cp         Copy a file within HPSS
rm mdelete Remove one or more files from HPSS
ls         List a directory
put, mput  Copy one or more local files to HPSS
cput       Conditional put - copy the file into HPSS unless it is already there
pwd        Print current directory
mv         Rename an HPSS file
mkdir      Create an HPSS directory
rmdir      Delete an HPSS directory
========== ====================================================================

 
Additional HSI Documentation
============================

There is interactive documentation on the ``hsi`` command available by running:

     ``hsi help``

Additional documentation can be found on the `HPSS Collaboration website <http://www.hpss-collaboration.org/user_doc.shtml>`__.

.. _htar:

===========
HTAR
===========

.. note::
   HPSS is now read-only. Users cannot transfer data into HPSS and should instead use :ref:`kronos`. For more information on migrating your files from HPSS to Kronos or another storage location, see the :ref:`hpss-migration` section.

HTAR is another utility to transfer data between OLCF systems and HPSS.  The ``htar`` command provides an interface very similar to the traditional ``tar`` command found on UNIX systems. The primary difference is instead of creating a .tar file on the local filesystem, it creates that file directly on HPSS. It is used as a command-line interface.  The basic syntax of ``htar`` is:

   ``htar -{c|K|t|x|X} -f tarfile [directories] [files]``

As with the standard Unix ``tar`` utility the ``-c``, ``-x``, and ``-t`` options, respectively, function to create, extract, and list tar archive files.  The ``-K`` option verifies an existing tarfile in HPSS and the ``-X`` option can be used to re-create the index file for an existing archive. For example, to store all files in the directory ``dir1`` to a file named ``/hpss/prod/[projid]/users/[userid]/allfiles.tar`` on HPSS, use the command:

     ``htar -cvf /hpss/prod/[projid]/users/[userid]/allfiles.tar dir1/*``

To retrieve these files:

     ``htar -xvf  /hpss/prod/[projid]/users/[userid]/allfiles.tar``

``htar`` will overwrite files of the same name in the target directory.  **When possible, extract only the files you need from large archives.** To display the names of the files in the ``project1.tar`` archive file within the HPSS home directory:

     ``htar -vtf  /hpss/prod/[projid]/users/[userid]/project1.tar``

To extract only one file, ``executable.out``, from the ``project1`` directory in the Archive file called `` /hpss/prod/[projid]/users/[userid]/project1.tar``:

     ``htar -xm -f project1.tar project1/ executable.out``

To extract all files from the ``project1/src`` directory in the archive file called ``project1.tar``, and use the time of extraction as the modification time, use the following command:

     ``htar -xm -f  /hpss/prod/[projid]/users/[userid]/project1.tar project1/src``

HTAR Limitations
================

The ``htar`` utility has several limitations:

1. Appending data
-----------------
You cannot add or append files to an existing archive.

2. File Path Length
-------------------

File path names within an ``htar`` archive of the form prefix/name are limited to 154 characters for the prefix and 99 characters for the file name. Link names cannot exceed 99 characters.

3. Size
-------

There are limits to the size and number of files that can be placed in an HTAR archive:

=================================== ========================
Individual File Size Maximum        68GB, due to POSIX limit
Maximum Number of Files per Archive 1 million
=================================== ========================

For example, when attempting to HTAR a directory with one member file larger that 64GB, the following error message will appear:

.. code::

   $ htar -cvf  /hpss/prod/[projid]/users/[userid]/hpss_test.tar hpss_test/

   INFO: File too large for htar to handle: hpss_test/75GB.dat (75161927680 bytes)
   ERROR: 1 oversize member files found - please correct and retry
   ERROR: [FATAL] error(s) generating filename list
   HTAR: HTAR FAILED

Additional HTAR Documentation
=============================

For more information about ``htar``, execute ``man htar``. 


.. _clitools:

========================================
Command-Line/Terminal Tools
========================================

Command-line tools such as ``scp`` and ``rsync`` can be used to transfer data from outside OLCF.  In general, when transferring data into or out of OLCF from the command line, it's best to initiate the transfer from outside OLCF. If moving many small files, it can be beneficial to compress them into a single archive file, then transfer just the one archive file. When using command-line tools, you should use the :ref:`Data Transfer Nodes <dtn-user-guide>` rather than systems like Frontier or Andes.

* ``scp`` - secure copy (remote file copy program)

	* Sending a file to OLCF

	.. code::

   	   scp yourfile $USER@dtn.ccs.ornl.gov:/path/


	* Retrieving a file from OLCF

	.. code::

   	   scp $USER@dtn.ccs.ornl.gov:/path/yourfile .


	* Sending a directory to OLCF

	.. code::

   	   scp -r yourdirectory $USER@dtn.ccs.ornl.gov:/path/


* ``rsync`` - a fast, versatile, remote (and local) file-copying tool


	* Sync a directory named ``mydir`` from your local system to the OLCF

	.. code::

   	   rsync -avz mydir/ $USER@dtn.ccs.ornl.gov:/path/


	where:
  		* ``a`` is for archive mode\
  		* ``v`` is for verbose mode\
  		* ``z`` is for compressed mode\


	* Sync a directory from the OLCF to a local directory

	.. code::

   	   rsync -avz  $USER@dtn.ccs.ornl.gov:/path/dir/ mydir/

        * Transfer data and show progress while transferring

        .. code::

           rsync -avz --progress mydir/ $USER@dtn.ccs.ornl.gov:/path/

	* Include files or directories starting with T and exclude all others

        .. code::

           rsync -avz --progress --include 'T*' --exclude '*' mydir/ $USER@dtn.ccs.ornl.gov:/path/

	* If the file or directory exists at the target but not on the source, then delete it

        .. code::

           rsync -avz --delete $USER@dtn.ccs.ornl.gov:/path/ .

	* Transfer only the files that are smaller than 1MB

        .. code::

           rsync -avz --max-size='1m' mydir/ $USER@dtn.ccs.ornl.gov:/path/

	* If you want to verify the behavior is as intended, execute a dry-run

        .. code::

           rsync -avz --dry-run mydir/ $USER@dtn.ccs.ornl.gov:/path/

See the manual pages for more information:

.. code::

    $ man scp
    $ man rsync


* Differences:
	* ``scp`` cannot continue if it is interrupted. ``rsync`` can.
	* ``rsync`` is optimized for performance.
	* By default, ``rsync`` checks if the transfer of the data was successful.


.. note::
    Standard file transfer protocol (FTP) and remote copy (RCP) should not be used to transfer files to the NCCS high-performance computing (HPC) systems due to security concerns.


