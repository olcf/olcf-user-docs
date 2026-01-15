.. _status_api:

******
Status
******

The Status API is a series of unauthenticated endpoints that can be used to retrieve basic details on a number of resources and their potential upcoming downtimes. Please note that only resource-specific information related to the Facility API in the related security enclave is monitored.

**Required Permission:** None, all status endpoints are open.

GET Status for All Resources
---------------------------

Obtain a list of all monitored resources, their status, and any upcoming downtimes: ``/olcf/v1alpha/status``

.. code-block:: shell

   curl https://s3m.olcf.ornl.gov/olcf/v1alpha/status

The ``downtimeScheduleAvailable`` field indicates if the associated resource has planned downtime scheduling available that will be reflected in the results. In most cases, testbed resources (e.g., Defiant) do plan for downtimes in advance due to their test-focused nature, and as such, ``upcomingDowntimes`` will likely be missing.

.. code-block:: json

   {
       "resources": [
           {
               "name": "olivine",
               "description": "OpenShift cluster for testing Themis integration",
               "systemType": "resource",
               "securityEnclave": "open",
               "organization": "olcf",
               "status": "OPERATIONAL",
               "annotations": {},
               "downtimeScheduleAvailable": false,
               "retrievedAt": "2024-04-19T13:45:01Z"
           },
           {
               "name": "defiant",
               "description": "Defiant",
               "systemType": "resource",
               "securityEnclave": "open",
               "organization": "olcf",
               "status": "OPERATIONAL",
               "annotations": {},
               "downtimeScheduleAvailable": true,
               "upcomingDowntimes": [
                   {
                       "resourceName": "defiant",
                       "status": "UNAVAILABLE",
                       "start": "2024-04-20T11:40:00Z",
                       "end": "2024-04-21T11:40:00Z",
                       "description": "Compute system hardware maintenance",
                       "attributes": {
                           "scheduled": true,
                           "reboot": true
                       },
                       "updatedAt": "2024-04-19T13:40:29Z"
                   }
               ],
               "retrievedAt": "2024-04-19T13:45:01Z"
           },
           {
               "name": "wombat",
               "description": "ARM86 Computational Resource",
               "systemType": "resource",
               "securityEnclave": "open",
               "organization": "olcf",
               "status": "UNAVAILABLE",
               "annotations": {},
               "downtimeScheduleAvailable": true,
               "retrievedAt": "2024-04-19T13:45:01Z"
           }
       ]
   }

.. list-table::
   :header-rows: 1

   * - Cache
     - Rate Limit
   * - 15 minutes
     - None

GET Status for Specific Resource
-------------------------------

Obtain a list of a target resource (limited to a monitored resource), its status, and any upcoming downtimes: ``/olcf/v1alpha/status/{resourceName}``

.. code-block:: shell

   curl https://s3m.olcf.ornl.gov/olcf/v1alpha/status/defiant

.. code-block:: json

   {
       "name": "defiant",
       "description": "Defiant",
       "systemType": "resource",
       "securityEnclave": "open",
       "organization": "olcf",
       "status": "OPERATIONAL",
       "annotations": {},
       "downtimeScheduleAvailable": true,
       "upcomingDowntimes": [
           {
               "resourceName": "defiant",
               "status": "UNAVAILABLE",
               "start": "2024-04-20T11:40:00Z",
               "end": "2024-04-21T11:40:00Z",
               "description": "Compute system hardware maintenance",
               "attributes": {
                   "scheduled": true,
                   "reboot": true
               },
               "updatedAt": "2024-04-19T13:40:29Z"
           }
       ],
       "retrievedAt": "2024-04-19T13:45:01Z"
   }

.. list-table::
   :header-rows: 1

   * - Cache
     - Rate Limit
   * - 15 minutes
     - None

GET Current Downtimes
---------------------

Retrieve a list of all current downtimes for monitored resources: ``/olcf/v1alpha/status/downtimes``

.. code-block:: shell

   curl https://s3m.olcf.ornl.gov/olcf/v1alpha/status/downtimes

.. code-block:: json

   {
       "downtimes": [
           {
               "resourceName": "defiant",
               "status": "UNAVAILABLE",
               "start": "2024-04-20T11:40:00Z",
               "end": "2024-04-21T11:40:00Z",
               "description": "Compute system hardware maintenance",
               "attributes": {
                   "scheduled": true,
                   "reboot": true
               },
               "updatedAt": "2024-04-19T13:40:29Z"
           }
       ]
   }

.. list-table::
   :header-rows: 1

   * - Cache
     - Rate Limit
   * - 15 minutes
     - None

GET Upcoming Downtimes
----------------------

Retrieve a list of all upcoming downtimes for monitored resources within the next 10 days: ``/olcf/v1alpha/status/downtimes/upcoming``

.. code-block:: shell

   curl https://s3m.olcf.ornl.gov/olcf/v1alpha/status/downtimes/upcoming

.. code-block:: json

   {
       "downtimes": [
           {
               "resourceName": "defiant",
               "status": "UNAVAILABLE",
               "start": "2024-04-20T11:40:00Z",
               "end": "2024-04-21T11:40:00Z",
               "description": "Compute system hardware maintenance",
               "attributes": {
                   "scheduled": true,
                   "reboot": true
               },
               "updatedAt": "2024-04-19T13:40:29Z"
           }
       ]
   }

.. list-table::
   :header-rows: 1

   * - Cache
     - Rate Limit
   * - 15 minutes
     - None
