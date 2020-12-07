***************************
User-Centric Data Storage
***************************


The following table summarizes user-centric storage areas available on OLCF
resources and lists relevant polices.


**User-Centric Storage Areas**

+---------------------+---------------------------------------------+----------------+-------------+--------+---------+---------+------------+------------------+
| Area                | Path                                        | Type           | Permissions |  Quota | Backups | Purged  | Retention  | On Compute Nodes |
+=====================+=============================================+================+=============+========+=========+=========+============+==================+
| User Home           | ``/ccs/home/[userid]``                      | NFS            | User set    |  50 GB | Yes     | No      | 90 days    | Read-only        |
+---------------------+---------------------------------------------+----------------+-------------+--------+---------+---------+------------+------------------+
| User Archive [#f1]_ | ``/home/[userid]``                          | HPSS           | User set    |  2TB   | No      | No      | 90 days    | No               |   
+---------------------+---------------------------------------------+----------------+-------------+--------+---------+---------+------------+------------------+
| User Archive [#f2]_ | ``/home/[userid]``                          | HPSS           | 700         |  N/A   | N/A     | N/A     | N/A        | No               |   
+---------------------+---------------------------------------------+----------------+-------------+--------+---------+---------+------------+------------------+

.. rubric:: footnotes


.. [#f1] This entry is for legacy User Archive directories which contained user data on January 14, 2020. There is also a quota/limit of 2,000 files on this directory.

.. [#f2] User Archive directories that were created (or had no user data) after January 14, 2020. Settings other than permissions are not applicable because directories are root-owned and contain no user files.


.. _user-home-directories-nfs:

User Home Directories (NFS)
============================

The environment variable ``$HOME`` will always point to your current home
directory. It is recommended, where possible, that you use this variable to
reference your home directory. In cases in which using ``$HOME`` is not
feasible, it is recommended that you use ``/ccs/home/$USER``.

Users should note that since this is an NFS-mounted filesystem, its performance
will not be as high as other filesystems.

User Home Quotas
-----------------

Quotas are enforced on user home directories. To request an increased quota,
contact the OLCF User Assistance Center. To view your current quota and usage,
use the ``quota`` command:


.. code::

    $ quota -Qs
    Disk quotas for user usrid (uid 12345):
         Filesystem  blocks   quota   limit   grace   files   quota   limit   grace
    nccsfiler1a.ccs.ornl.gov:/vol/home
                      4858M   5000M   5000M           29379   4295m   4295m


User Home Permissions
----------------------

The default permissions for user home directories are ``0750`` (full access to
the user, read and execute for the group). Users have the ability to change
permissions on their home directories, although it is recommended that
permissions be set to as restrictive as possible (without interfering with your
work).

User Home Backups
-----------------

If you accidentally delete files from your home directory
(``/ccs/home/$USER``), you may be able to retrieve them. Online backups are
performed at regular intervals. Hourly backups for the past 24 hours, daily
backups for the last 7 days, and once-weekly backups are available. It is
possible that the deleted files are available in one of those backups. The
backup directories are named ``hourly.*``, ``daily.*``, and ``weekly.*`` where
``*`` is the date/time stamp of backup creation. For example,
``hourly.2020-01-01-0905`` is an hourly backup made on January 1st, 2020 at
9:05 AM.

The backups are accessed via the ``.snapshot`` subdirectory. Note that ``ls``
alone (or even ``ls -a``) will not show the ``.snapshot`` subdirectory exists,
though ``ls .snapshot`` will show its contents. The ``.snapshot`` feature is
available in any subdirectory of your home directory and will show the online
backups available for that subdirectory. 

To retrieve a backup, simply copy it into your desired destination with the
``cp`` command.

User Website Directory
----------------------

Users interested in sharing files publicly via the World Wide Web can request a
user website directory be created for their account. User website directories
(``~/www``) have a 5GB storage quota and allow access to files at
``http://users.nccs.gov/~user`` (where ``user`` is your userid). If you are
interested in having a user website directory created, please contact the User
Assistance Center at help@olcf.ornl.gov.

User Archive Directories (HPSS)
================================

.. note::
    Use of User Archive areas for data storage is deprecated as of January 14, 2020.
    The user archive area for any user account created after that date (or for any
    user archive directory that is empty of user files after that date) will contain
    only symlinks to the top-level directories for each of the user's projects on
    HPSS. Users with existing data in a User Archive directory are encouraged to
    move that data to an appropriate project-based directory as soon as possible.
    
    The information below is simply for reference for those users with existing 
    data in User Archive directories.

The High Performance Storage System (HPSS) at the OLCF provides longer-term
storage for the large amounts of data created on the OLCF compute systems. The
mass storage facility consists of tape and disk storage components, servers, and
the HPSS software. After data is uploaded, it persists on disk for some period
of time. The length of its life on disk is determined by how full the disk
caches become. When data is migrated to tape, it is done so in a first-in,
first-out fashion.

User archive areas on HPSS are intended for storage of data not immediately
needed in either User Home directories (NFS) or User Work directories (GPFS).
User Archive directories should not be used to store project-related data.
Rather, Project Archive directories should be used for project data.

User archive directories are located at ``/home/$USER``.

User Archive Access
--------------------

Each OLCF user receives an HPSS account automatically. Users can transfer data
to HPSS from any OLCF system using the HSI or HTAR utilities. For more
information on using HSI or HTAR, see the :ref:`hpss` .

User Archive Accounting
------------------------

Each file and directory on HPSS is associated with an HPSS storage allocation.
For information on HPSS storage allocations, please visit the :ref:`policy`
section.

For information on usage and best practices for HPSS, please see the :ref:`hpss`
documentation.
