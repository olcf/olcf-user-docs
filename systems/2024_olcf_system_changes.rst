.. _2024-olcf-system-changes:

**************************************
2024 Notable System Changes
**************************************

.. _system_change_overview:

This page lists multiple notable changes to OLCF resources.


1. **HPSS Decommission and Kronos Availability**

After decades in service and having served hundreds of users that have archived over 160 petabytes, HPSS is reaching end of its life and will be decommissioned early in 2025.  Please pay attention to the following key dates as you migrate workloads from the center's HPSS resource to the new nearline resource, Kronos.

.. list-table:: 
   :widths: 20 150
   :header-rows: 1

   * - Date
     - HPSS Decommission and Kronos Availability Timeline
   * - :ref:`Late July<kronos_overview>`
     - Kronos available.
   * - :ref:`August 30<hpss_read_only>`
     - HPSS becomes read-only. **To help spread the HPSS migration load, please reach out to help@olcf.ornl.gov to help coordinate your large HPSS data migrations.**
   * - :ref:`January 31, 2025<hpss_decom>`
     - HPSS decommissioned.  **ALL REMAINING DATA WILL BE PERMANENTLY DELETED**


2. **Summit and Alpine2 Decommissions**

After almost 6 years of production service providing over 200 million node hours to researchers around the world, Summit will be decommissioned on November 15, 2024.  Please pay close attention to the Summit and Alpine2 decommission dates below and plan your research and data migration accordingly.

.. list-table:: 
   :widths: 20 150
   :header-rows: 1

   * - Date
     - Summit and Alpine2 Decommission Timeline
   * - :ref:`November 15<summit_decom>`
     - Summit decommissioned; last day to run batch jobs.
   * - :ref:`November 19<alpine2_read_only>`
     - Alpine2 unmounted from Andes and becomes read-only on DTNs. 
   * - :ref:`January 31, 2025<alpine2_decom>`
     - Alpine2 decommissioned.  **ALL REMAINING DATA WILL BE PERMANENTLY DELETED**

===========================================
HPSS Decommission and Kronos Availability 
===========================================

.. _kronos_overview:

Late July 2024 - Kronos available
----------------------------------------------------

On July 31, Kronos was made available to early users.  Following a period of testing, the resource will be available to all HPSS users.   If you would like to participate in Kronos early testing, please reach out to help@olcf.ornl.gov. 

Kronos Overview
^^^^^^^^^^^^^^^^

Overview
  Kronos is the center's new nearline storage resource.  Kronos is multi-tiered containing both disk and tape.  Users will interact with the system's disk sub-system which leverages IBM Storage Scale (GPFS).  Data stored on the disk sub-system will automatically be stored on they system's tape sub-system.  The disk sub-system will provide an initial capacity of 134 PB with the ability to expand as need increases.  Kronos is capable of bandwidth of up-to 200 GB/s from the center's Data Transfer Nodes (DTNs).

Availability Timeline
  Kronos is expected to be available late July 2024.

Access / Data Transfer
  Kronos will be mounted on the moderate Data Transfer Nodes.  Because the system will be mounted as a filesystem, standard UNIX command and tools can be used to interact with Kronos.  The resource will also be accessible through the OLCF Kronos collection in Globus.

  Please note that Kronos will not be mounted on the compute nodes of Frontier or Andes.

  Because Kronos is in the moderate security enclave, all projects with allocations to Summit, Frontier, or Andes will receive an allocation on Kronos.

Project Quotas
  To help ensure available space for all Kronos projects, each project has a 200TB quota.  All data stored in /nl/kronos/olcf/<projectID> will count toward the project's quota.  Please reach out to help@olcf.ornl.gov to request exemptions to the default quota.

.. note::
  To help ensure available space for all Kronos projects, each project has a default 200TB quota.  Please contact help@olcf.ornl.gov for quota increase requests.


Directory Structure
  Kronos will use a directory structure similar to other center-wide storage resources:

  .. list-table::
   :widths: 20 12 12 12 80
   :header-rows: 1

   * - Path
     - Permissions
     - Owner
     - Group
     - Description
   * - /nl/kronos/olcf/<projectID>/proj-shared
     - 755
     - root
     - <projectID> UNIX group
     - Data shared between project members.
   * - /nl/kronos/olcf/<projectID>/users/<userID>
     - 700
     - <userID>
     - <projectID> UNIX group
     - User data, access is limited to user by default, but each user can modify their directory permissions to share with other project members.
   * - /nl/kronos/olcf/<projectID>/world-shared
     - 2775
     - root
     - <projectID> UNIX group
     - Data accessible to others in the OLCF user community



HPSS and Kronos Comparison
^^^^^^^^^^^^^^^^^^^^^^^^^^^



  .. list-table:: Notable comparisons between Kronos and HPSS
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


.. _hpss_read_only:

August 30, 2024 - HPSS becomes read-only
----------------------------------------

In preparation for HPSS's decommission in January 2025, the HPSS will become read-only from all OLCF resources on August 30, 2024.

We highly encourage all teams to start migrating needed data from the HPSS now.  If you wait too late in the year to begin the transition, you will run the risk of running out of time to move your data before the system is decommissioned.  It is important to note that any data remaining on the HPSS after January 31, 2025, will be unavailable. We expect HPSS periods of access impacts due to the expected volumes of data migrating off of the HPSS. To help spread the HPSS migration load, please reach out to help@olcf.ornl.gov to help coordinate your larger HPSS data migrations.

.. _hpss-migration:

Data migration
^^^^^^^^^^^^^^^

.. note::
  We expect HPSS periods of access impacts due to the expected volumes of data migrating off of the HPSS. To help spread the HPSS migration load, please reach out to help@olcf.ornl.gov to help coordinate your large HPSS data migrations.  

Copying data directly from HPSS to Kronos
  The hsi utility will provide the best performance and HPSS tape organization.  To transfer data from the HPSS to Kronos, the preferred method is to utilize the hsi utility from the DTN.  Since the DTN will mount Kronos, hsi transfers can be performed from within a Kronos directory on the DTNs.

.. note::
  You may see longer retrieval times for data stored only on tape than data stored on disk.  Please consider physical tape access overhead when planning your data migration.  Please reach out to help@olcf.ornl.gov with extended retrieval delay concerns.

Data Deletion
  Due to the added overhead of data deletion, we ask that users not delete data from the HPSS.

Globus
  The Globus utility is not aware of the underlying HPSS tape storage structure.  To help spread the load over the resource's tape retrieval system, we ask that Globus not be used to migrate data off of the HPSS.  Instead, please use the HPSS ``hsi`` utility.  The HPSS Globus collection will be disabled on August 30, 2024 to help ensure efficient migration from HPSS tape.

.. warning::
  The Globus utility is not aware of the underlying HPSS tape storage structure.  To help ensure safe and efficient migration of data from tape, the HPSS Globus collection will be disabled on August 30, 2024.  Instead of Globus, please use the HPSS ``hsi`` utility.  

HSI Data Lists
  The HPSS ``hsi`` utility is the preferred tool for HPSS data migration because it is aware of the HPSS tape storage structure.  To ensure the most efficient retrieval of data stored on tape, we recommend passing list files to ``hsi``.  Please also see the ``hsi_xfer`` utility below for an easy way to utilize the hsi data list feature.

  * **Bad practice** Successive ``hsi get`` calls

    .. code:: bash

      $ hsi get /hpss/prod/abc123/users/userA/file1
      $ hsi get /hpss/prod/abc123/users/userA/file2
      $ hsi get /hpss/prod/abc123/users/userA/file3



  * **Good practice** create a list file & call ``hsi`` once

    .. code-block:: bash

      $ cat getfiles.lst
      get <<EOF
      /hpss/prod/abc123/users/userA/file1
      /hpss/prod/abc123/users/userA/file2
      /hpss/prod/abc123/users/userA/file3
      EOF

      $ hsi "in getfiles.lst"


hsi_xfer Utility
  The ``hsi_xfer`` utility provides an easy way to utilize the hsi data list feature.  The utility will recursively copy a directory on the HPSS to a directory on Kronos.  The utility will create the needed data lists and call hsi behind the scenes.  Please note that you must specify full paths for both the source and destination diretories.  The utility can be executed on the DTN after loading the ``hsi_xfer`` module. Additional documentation on the ``hsi_xfer`` utility (common flags, common problems, etc.) can be found `here <https://www.olcf.ornl.gov/wp-content/uploads/hsi_xfer_notes.pdf>`__ .

  * **Syntax** ``hsi_xfer hpss_source_dir kronos_destination_dir`` 

  * **Example** The following will recursively copy data from hpss_dir to kronos_dir

    .. code-block:: bash

      dtn101 413> module load hsi_xfer
      dtn101 414> hsi_xfer /home/<userID>/hpss_dir /nl/kronos/olcf/<projID>/<userID>/kronos_dir


.. note::
  The ``hsi_xfer`` utility is available on the DTN.

.. warning::
  The ``hsi_xfer`` utility requires full paths.  Please specify the full path to the source and destination directories.

.. note::
  To maximize availability of transfer resources for all users, there is a limit of one active ``hsi_xfer`` operation per user



.. _hpss_decom:

January 31, 2025 - HPSS decommissioned
--------------------------------------

On January 31, 2025, data remaining on the HPSS will no longer be accessible and will be permanently deleted. Following this date, the OLCF will no longer be able to retrieve data remaining on HPSS.

.. warning::
  January 31, 2025, all remaining HPSS data will be **PERMANENTLY DELETED**.  Do not wait to move needed data.

=================================
Summit and Alpine2 Decommissions
=================================

.. _summit_decom:

November 15, 2024 - Summit decommissioned
-----------------------------------------

**On November 15, 2024, Summit will be decommissioned.** Batch jobs will be allowed to execute until 08:00 AM (EST) November 15.  Jobs remaining in the queue after this time will be deleted.  

Please pay close attention to the Summit and Alpine2 decommission dates and plan your research and data migration accordingly.  Please also note that the Summit decommission date is firm: The machine will very quickly be physically disassembled starting November 15.

.. note::
  Summit decommission date is firm: The machine will very quickly be physically disassembled starting November 15.  **It will not be physically possible to run batch jobs after November 15.**


.. _alpine2_read_only:

November 19, 2024 - Alpine2 read-only
--------------------------------------

On November 19, 2024, Alpine2 will be unmounted from Andes and will be mounted read-only from the DTNs.

* **Alpine2 unmounted from Andes**

  * On November 19, Alpine2 will be unmounted from Andes
  * Please manage your workflows such that Andes batch jobs requiring Alpine2 will complete prior to November 19.
  * Andes batch jobs requiring Alpine2 after this date will fail

* **Alpine2 mounted read-only on DTNs**

  * To allow time to migrate needed data off of Alpine2, the OLCF DTN resources will mount Alpine2 as read-only on November 19
  * Alpine2 will remain available read-only on the DTNs through Alpine2's decommission date.


.. _alpine2_decom:

January 31, 2025 - Alpine2 decommissioned
-----------------------------------------

On January 31, 2025, data remaining on Alpine2 will no longer be accessible and will be permanently deleted. Following this date, the OLCF will no longer be able to retrieve data remaining on Alpine2.

.. warning::
  January 31, 2025, all remaining Alpine2 data will be **PERMANENTLY DELETED**.  Do not wait to move needed data.




