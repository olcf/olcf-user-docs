.. _s3m_api_reference:

*************
API Reference
*************

All S3M services are accessible as RESTful APIs, via ``curl`` or any HTTP client. Python and Go client libraries are
also available for more complex integrations.

Most endpoints require authentication via the ``Authorization`` header with your S3M token. See :ref:`s3m_get_a_token`
to obtain one.

.. toctree::
   :maxdepth: 2

   status
   tokens
   compute
   streaming

.. list-table::
   :header-rows: 1
   :widths: 20 25 25 30

   * - API
     - Description
     - Authentication
     - Example
   * - :doc:`status`
     - Resource status and scheduled downtimes
     - None required
     - ``GET https://s3m.olcf.ornl.gov/olcf/v1alpha/status``

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

   * - :doc:`tokens`
     - Token introspection and revocation
     - Required
     - ``DELETE https://s3m.olcf.ornl.gov/olcf/v1/token/ctls/revoke``

       **Response:** ``{}``

   * - :doc:`compute`
     - SLURM job submission and management
     - Required (``compute-ace`` scope)
     - ``GET https://s3m.olcf.ornl.gov/olcf/v1/slurm/open/v0.0.43/defiant/ping``

       **Response:** See `SLURM REST API <https://slurm.schedmd.com/rest_api.html>`_

   * - :doc:`streaming`
     - RabbitMQ and Redis cluster provisioning
     - Required (``data-streaming`` scope)
     - ``GET https://s3m.olcf.ornl.gov/olcf/open/v1alpha/streaming/list_backends``

       **Response:**

       .. code-block:: json

        {
          "backends": [
            {
              "engine": "redis",
              "kind": "valkey-general",
              "description": "Valkey cluster (Redis-compatible)",
              "resourceOptions": [
                {
                  "key": "cpus",
                  "description": "CPUs per node/replica",
                  "min": 1,
                  "max": 4,
                  "default": 2
                },
                {
                  "key": "ram-gbs",
                  "description": "RAM per node/replica in GBs",
                  "min": 1,
                  "max": 4,
                  "default": 2
                }
              ],
              "featureFlags": []
            }
          ]
        }

