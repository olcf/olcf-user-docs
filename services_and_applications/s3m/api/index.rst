.. _s3m_api_reference:

*************
API Reference
*************

All S3M APIs are accessible via REST. Use ``curl`` or any HTTP client to interact with them directly. Python and Go
client libraries are also available for more complex integrations.

Most endpoints require authentication via the ``Authorization`` header with your S3M token. See :doc:`../get-a-token`
to obtain one.

.. toctree::
   :maxdepth: 2

   status
   tokens
   compute
   streaming

.. list-table::
   :header-rows: 1
   :widths: 20 50 30

   * - API
     - Description
     - Authentication
   * - :doc:`status`
     - Resource status and scheduled downtimes
     - None required
   * - :doc:`tokens`
     - Token introspection and revocation
     - Required
   * - :doc:`compute`
     - SLURM job submission and management
     - Required (``compute-ace`` scope)
   * - :doc:`streaming`
     - RabbitMQ and Redis cluster provisioning
     - Required (``data-streaming`` scope)
