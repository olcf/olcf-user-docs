***************************
User-Centric Data Storage
***************************


The following table summarizes user-centric storage areas available on OLCF
resources and lists relevant polices.


**User-Centric Storage Areas**

+--------------+-----------------+------+-----------------+-------------+---------+--------+-----------+
| Area         | Path            | Type | Permissions     | Quota       | Backups | Purged | Retention |
+==============+=================+======+=================+=============+=========+========+===========+
| User Home    | ``$HOME``       | NFS  | User-controlled | 50 GB       | Yes     | No     | 90 days   |
+--------------+-----------------+------+-----------------+-------------+---------+--------+-----------+
| User Archive | ``/home/$USER`` | HPSS | User-controlled | 2 TB [#f1]_ | **No**  | No     | 90 days   |
+--------------+-----------------+------+-----------------+-------------+---------+--------+-----------+

.. rubric:: footnotes

.. [#f1] In addition, there is a quota/limit of 2,000 files on this directory.


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
