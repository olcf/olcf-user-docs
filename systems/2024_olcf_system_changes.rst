.. _2024-olcf-system-changes:

**************************************
2024 Notable System Changes
**************************************

.. _system_change_overview:


After decades in service and having served hundreds of users that have archived over 160 petabytes, HPSS is reaching end of its life and will be decommissioned early in 2025.

Please pay attention to the following key dates as you migrate workloads from the center's HPSS resource to the new nearline resource, Kronos.


.. list-table:: 2024 OLCF System Decommissions and Notable Changes
   :widths: 20 150
   :header-rows: 1

   * - Date
     - Event
   * - :ref:`May 2024<kronos_overview>`
     - Kronos available for production use.
   * - :ref:`June 2024<hpss_read_only>`
     - HPSS becomes read-only. 
   * - :ref:`January 2025<hpss_decom>`
     - HPSS decommissioned.  **ALL REMAINING DATA WILL BE PERMANENTLY DELETED**



.. _kronos_overview:

May 2024 - Kronos available for production use
-----------------------------------------------

Kronos is expected to be available May 2024.  Updates to the availability schedule will be posted to this site and through the OLCF weekly email.

Kronos Overview
^^^^^^^^^^^^^^^^

Overview
  Kronos is the center's new nearline storage resource.  Kronos is multi-tiered containing both disk and tape.  Users will interact with the system's disk sub-system which leverages IBM Storage Scale (GPFS).  Data stored on the disk sub-system will automatically be stored on they system's tape sub-system.  The disk sub-system will provide an initial capacity of 134 PB with the ability to expand as need increases.  Kronos is capable of bandwidth of up-to 200 GB/s from the center's Data Transfer Nodes.

Availability Timeline
  Kronos is expected to be available May 2024.

Access / Data Transfer
  Kronos will be mounted on the moderate Data Transfer Nodes, Frontier login nodes, and Andes login nodes.  Because the system will be mounted as a filesystem, standard UNIX command and tools can be used to interact with Kronos.  The resource will also be accessible through the OLCF DTN endpoint in Globus.

  Please note that Kronos will not be mounted on the compute nodes of Frontier or Andes.

  Because Kronos is in the moderate security enclave, all projects with allocations to Summit, Frontier, or Andes will receive an allocation on Kronos.

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
     - DTNs and login nodes
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

June 2024 - HPSS becomes read-only
-----------------------------------

In preparation for HPSS's decommission in January 2025, the HPSS will become read-only from all OLCF resources in June 2024.

We highly encourage all teams to start migrating needed data from the HPSS now.  If you wait too late in the year to begin the transition, you will run the risk of running out of time to move your data before the system is decommissioned.  It is important to note that any data remaining on the HPSS after December 31, 2024, will be unavailable. We expect HPSS periods of access impacts due to the expected volumes of data migrating off of the HPSS. To help spread the HPSS migration load, please reach out to help@olcf.ornl.gov to help coordinate your larger HPSS data migration.

Data migration
^^^^^^^^^^^^^^^

Copying data directly from HPSS to Kronos
  The hsi utility will provide the best performance and HPSS tape organization.  To transfer data from the HPSS to Kronos, the preferred method is to utilize the hsi utility from the DTN.  Since the DTN will mount Kronos, hsi transfers can be performed from within a Kronos directory on the DTNs.

.. note::
  You may see longer retrieval times for data stored only on tape than data stored on disk.  Please consider physical tape access overhead when planning your data migration.  Please reach out to help@olcf.ornl.gov with extended retrieval delay concerns.

Data Deletion
  Due to the added overhead of data deletion, we ask that users not delete data from the HPSS.




.. _hpss_decom:

January 2025 - HPSS decommissioned
-----------------------------------

On January 01, data remaining on the HPSS will no longer be accessible and will be permanently deleted. Following this date, the OLCF will no longer be able to retrieve data remaining on HPSS.

.. warning::
  Jan 2025, all remaining HPSS data will be **PERMANENTLY DELETED**.  Do not wait to move needed data.
