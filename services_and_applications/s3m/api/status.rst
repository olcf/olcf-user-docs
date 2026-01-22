.. _s3m_status_api:

******
Status
******

The Status API provides unauthenticated endpoints to retrieve resource status and scheduled downtimes. Only resource-specific information related to the Facility API in the related security enclave is monitored.

**Required Permission:** None—all status endpoints are open.

.. note::

   The Python and Go examples on this page use gRPC client packages that are not yet publicly available.
   ORNL-internal users may request access on a case-by-case basis by contacting the S3M team: `olcf-s3m@email.ornl.gov <mailto:olcf-s3m@email.ornl.gov>`__.
   The REST API (curl examples) is available to all users.

List All Resources
------------------

Obtain a list of all monitored resources, their status, and any upcoming downtimes.

``GET /olcf/v1alpha/status``

.. tab-set::

   .. tab-item:: curl
      :sync: curl

      .. code-block:: shell

         curl https://s3m.olcf.ornl.gov/olcf/v1alpha/status

   .. tab-item:: Python
      :sync: python

      .. code-block:: python

         from betterproto.lib.std.google.protobuf import Empty

         client = factory.create_client(StatusStub)
         resources = await client.list_resources(Empty())

   .. tab-item:: Go
      :sync: go

      .. code-block:: go

         import (
             "context"
             "google.golang.org/protobuf/types/known/emptypb"
             statuspb "s3m.olcf.ornl.gov/apis/status/v1alpha"
         )

         client := statuspb.NewStatusClient(conn)
         resources, err := client.ListResources(context.Background(), &emptypb.Empty{})

**Response:**

.. code-block:: json

   {
       "resources": [
           {
               "name": "defiant",
               "description": "Defiant",
               "systemType": "resource",
               "securityEnclave": "open",
               "organization": "olcf",
               "status": "OPERATIONAL",
               "downtimeScheduleAvailable": true,
               "upcomingDowntimes": [
                   {
                       "resourceName": "defiant",
                       "status": "UNAVAILABLE",
                       "start": "2024-04-20T11:40:00Z",
                       "end": "2024-04-21T11:40:00Z",
                       "description": "Compute system hardware maintenance"
                   }
               ],
               "retrievedAt": "2024-04-19T13:45:01Z"
           }
       ]
   }

The ``downtimeScheduleAvailable`` field indicates if the resource has planned downtime scheduling. Testbed resources (e.g., Defiant) may not plan downtimes in advance, so ``upcomingDowntimes`` may be absent.

.. list-table::
   :header-rows: 1

   * - Cache
     - Rate Limit
   * - 15 minutes
     - None

Get Specific Resource
---------------------

Obtain status for a single resource by name.

``GET /olcf/v1alpha/status/{resourceName}``

.. tab-set::

   .. tab-item:: curl
      :sync: curl

      .. code-block:: shell

         curl https://s3m.olcf.ornl.gov/olcf/v1alpha/status/defiant

   .. tab-item:: Python
      :sync: python

      .. code-block:: python

         from s3m_apis_betterproto.status.v1alpha import GetResourceRequest

         client = factory.create_client(StatusStub)
         resource = await client.get_resource(GetResourceRequest(resource_name="defiant"))

   .. tab-item:: Go
      :sync: go

      .. code-block:: go

         import (
             "context"
             statuspb "s3m.olcf.ornl.gov/apis/status/v1alpha"
         )

         client := statuspb.NewStatusClient(conn)
         resource, err := client.GetResource(context.Background(), &statuspb.GetResourceRequest{ResourceName: "defiant"})

**Response:**

.. code-block:: json

   {
       "name": "defiant",
       "description": "Defiant",
       "systemType": "resource",
       "securityEnclave": "open",
       "organization": "olcf",
       "status": "OPERATIONAL",
       "downtimeScheduleAvailable": true,
       "upcomingDowntimes": [
           {
               "resourceName": "defiant",
               "status": "UNAVAILABLE",
               "start": "2024-04-20T11:40:00Z",
               "end": "2024-04-21T11:40:00Z",
               "description": "Compute system hardware maintenance"
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

List Current Downtimes
----------------------

Retrieve all downtimes currently in effect.

``GET /olcf/v1alpha/status/downtimes``

.. tab-set::

   .. tab-item:: curl
      :sync: curl

      .. code-block:: shell

         curl https://s3m.olcf.ornl.gov/olcf/v1alpha/status/downtimes

   .. tab-item:: Python
      :sync: python

      .. code-block:: python

         from betterproto.lib.std.google.protobuf import Empty

         client = factory.create_client(StatusStub)
         downtimes = await client.list_downtimes_current(Empty())

   .. tab-item:: Go
      :sync: go

      .. code-block:: go

         import (
             "context"
             "google.golang.org/protobuf/types/known/emptypb"
             statuspb "s3m.olcf.ornl.gov/apis/status/v1alpha"
         )

         client := statuspb.NewStatusClient(conn)
         downtimes, err := client.ListDowntimesCurrent(context.Background(), &emptypb.Empty{})

**Response:**

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

List Upcoming Downtimes
-----------------------

Retrieve all scheduled downtimes within the next 10 days.

``GET /olcf/v1alpha/status/downtimes/upcoming``

.. tab-set::

   .. tab-item:: curl
      :sync: curl

      .. code-block:: shell

         curl https://s3m.olcf.ornl.gov/olcf/v1alpha/status/downtimes/upcoming

   .. tab-item:: Python
      :sync: python

      .. code-block:: python

         from betterproto.lib.std.google.protobuf import Empty

         client = factory.create_client(StatusStub)
         downtimes = await client.list_downtimes_upcoming(Empty())

   .. tab-item:: Go
      :sync: go

      .. code-block:: go

         import (
             "context"
             "google.golang.org/protobuf/types/known/emptypb"
             statuspb "s3m.olcf.ornl.gov/apis/status/v1alpha"
         )

         client := statuspb.NewStatusClient(conn)
         downtimes, err := client.ListDowntimesUpcoming(context.Background(), &emptypb.Empty{})

**Response:**

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
