.. _2023-olcf-system-changes:

**************************************
2023 Notable System Changes
**************************************

.. _system_change_overview:


As the OLCF brings Frontier into full production and begins preparations for future resources, you should be aware of plans that will impact Summit, Andes, and the Alpine filesystem in 2023.

Please pay attention to the following key dates as you plan your science campaigns and data migration for the remainder of the year:

.. list-table:: 2023 OLCF System Decommissions and Notable Changes
   :widths: 20 150
   :header-rows: 1

   * - Date
     - Event
   * - :ref:`Sep 19<summit_proposals_open>` 
     - Submission system opens for 2024 Summit proposals.
   * - :ref:`Dec 18<summit_last_day_batch>` 
     - Last day to execute batch jobs on Summit.
   * - :ref:`Dec 18<andes_last_day_batch>` 
     - Last day to use Alpine from Andes.
   * - :ref:`Dec 19<alpine_readonly>` 
     - Alpine becomes read-only and available only from DTNs. **Please do not wait, begin transferring your Lustre data now.** 
   * - :ref:`Jan 01<alpine_decom>`
     - Alpine decommissioned.  **ALL REMAINING DATA WILL BE PERMANENTLY DELETED** 
   * - :ref:`Early 2024<summit_return_to_service>`
     - Summit available for projects with 2024 allocation. 
   * - :ref:`Early 2024<alpine_ii_available>`
     - Alpine II filesystem available. 





.. _summit_proposals_open:

Sep 19, 2023 - Submission system opens for 2024 Summit proposals  
----------------------------------------------------------------

The Department of Energy is extending Summit operations through October 2024, enabling researchers to pursue projects on one of the world’s leading AI-enabled open science supercomputing platforms.  OLCF will allocate Summit through new programs for calendar year 2024.

SummitPLUS is one of the new allocation programs that will be used to allocate a significant portion of the system for 2024. The program is open to researchers from academia, government laboratories, federal agencies, and industry. We welcome proposals for computationally ready projects from investigators who are new to Summit, as well as from previous INCITE, ALCC, DD, ECP awardees and projects. We encourage proposals on emerging paradigms for computational campaigns including data-intensive science and AI/ML.

Individuals or teams interested in SummitPLUS must submit a proposal through the https://my.olcf.ornl.gov/ portal from September 19 to October 30.  Once on the portal, go to “New Accounts” across the top and then “Project Application”. Choose the SummitPLUS form from the dropdown list.

Summit will continue to be allocated in node hours, and a typical SummitPLUS award will be between 100,000 – 250,000 node hours. The proposals will undergo review and the OLCF will notify awardees in mid-to-late November. Projects are anticipated to start in mid-to-late January 2024.

Timeline
    * Proposals accepted beginning September 19
    * Proposals will undergo review and the OLCF will notify awardees in mid-to-late November.
    * Projects are anticipated to start in mid-to-late January 2024.


.. _summit_last_day_batch:

Dec 18, 2023 - Last day to execute batch jobs on Summit 
--------------------------------------------------------

Your project may continue to submit jobs on Summit through your current project's end date (which varies by allocation program) or December 18th (whichever comes first).  The last day batch jobs from current projects will run on Summit is December 18, 2023. 

Summit will accept batch jobs prior to 08:00 on December 18, but only batch jobs that will complete prior to 08:00 Dec 18 will run.  All batch jobs remaining in the queue at 08:00, Dec 18 will be deleted.


.. _andes_last_day_batch:

Dec 18, 2023 - Last day to use Alpine on Andes
--------------------------------------------------------

Alpine will be unmounted from Andes on December 19.  Jobs must be modified to use Orion as their scratch filesystem prior to this day.


.. _alpine_readonly:

Dec 19, 2023 - Alpine becomes read-only 
-----------------------------------------

In preparation for Alpine's decommission on January 01, Alpine will become read-only from all OLCF systems on December 19.

To assist you with moving your data off of Alpine, the DTN's mount the new Orion filesystem and all projects with access to Alpine have now been granted access to the Orion filesystem.

.. warning::
  Please do not wait to migrate needed data, begin migrating all needed data now.

We highly encourage all teams to start migrating and/or deleting data from the Alpine filesystem now.  If you wait too late in the year to begin the transition, you will run the risk of running out of time to move your data before the system is decommissioned.  It is important to note that any data remaining on the Alpine filesystem after December 31, 2023, will truly be unavailable and not recoverable in any way as the system will be dismantled and the drives will be shredded.  

Data migration
^^^^^^^^^^^^^^^

Moving data off-site
  Globus is the suggested tool to move data off-site
  
  Standard tools such as rsync and scp can also be used through the DTN, but may be slower and require more manual intervention than Globus

Copying data directly from Alpine (GPFS) to Orion (Lustre)
  Globus is the suggested tool to transfer needed data from Alpine to Orion.
  
  Globus should be used when transfer large amounts of data.
  
  Standard tools such as rsync and cp can also be used. The DTN mounts both filesystems and should be used when transferring with rsync and cp tools. These methods should not be used to transfer large amounts of data.

Copying data to the HPSS archive system
  The hsi and htar utilities can be used to to transfer data from the Orion filesystem to the HPSS. The tools can also be used to transfer data from the HPSS to the Orion filesystem.
  
  Globus is also available to transfer data directly to the HPSS
  
  Please do not use the HPSS as a method to migrate data
    * Due to the large amounts of data on the Alpine scratch filesystem and the limited available space on the HPSS archive system, we strongly recommend not using the HPSS to transfer data between Alpine and Orion.
    * Due to available bandwidth, transferring data through the HPSS will be a slower route than using Globus to transfer directly between Alpine and Orion.
    * Transferring data through the HPSS is a multi-step process and will be slower than direct transfers using Globus.

.. note::
  Globus is the suggested tool to migrate data off of Alpine.  Please do not use HPSS as a data migration method. 



.. _alpine_decom:

Jan 01, 2024 - Alpine decommissioned 
-------------------------------------

On January 01, data remaining on the GPFS filesystem, Alpine, will no longer be accessible and will be permanently deleted . Following this date, the OLCF will no longer be able to retrieve data remaining on Alpine.

Due to the large amount of data on the filesystems, we strongly urge you to start transferring your data now, and do not wait until later in the year.

.. warning::
  Jan 01, all remaining Alpine data will be **PERMANENTLY DELETED**.  Do not wait to move needed data.



.. _summit_return_to_service:

Early 2024 - Summit available for projects with 2024 allocation. 
-----------------------------------------------------------------

Summit will be returned to service early 2024.

Projects awarded a 2024 Summit allocation will be able to log into Summit and submit batch jobs once the system has been made available.


.. note::
  Please note, Summit will mount a new filesystem once returned to service.
    * Data stored on Alpine at the time of its decommission on January 01 will not be available.
    * Users will be responsible for transferring data onto Summit's new filesystem



.. _alpine_ii_available:

Early 2024 - Alpine II filesystem available
-----------------------------------------------------------------
 
Alpine II will be available early 2024.

The previous center-wide GPFS scratch filesystem, Alpine, will be decommissioned in January 2024. A new scratch filesystem will be made available for projects with 2024 Summit allocations in early 2024. Users will be responsible for transferring any needed data onto the new scratch filesystem once available.  



