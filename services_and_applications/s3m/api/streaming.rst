.. _s3m_streaming_api:

*********
Streaming
*********

The Streaming API lets you provision message queue clusters for high-throughput data streaming to OLCF compute resources.

**Required Permission:** ``data-streaming``

.. note::

   The Python and Go examples on this page use gRPC client packages that are not yet publicly available.
   ORNL-internal users may request access by contacting the S3M team: `olcf-s3m@email.ornl.gov <mailto:olcf-s3m@email.ornl.gov>`__.
   The REST API (via curl or otherwise) is available to all users.

Available Backends
------------------

.. grid:: 2
   :gutter: 3

   .. grid-item-card:: RabbitMQ →
      :link: streaming-rabbitmq
      :link-type: doc

      Full-featured message broker with queues and bindings

   .. grid-item-card:: Redis →
      :link: streaming-redis
      :link-type: doc

      High-performance Redis-compatible streams and pub/sub

Cluster Lifecycle
-----------------

All streaming clusters are created with a 7-day lifetime countdown.

Any token for a cluster's project can be used to reset the countdown at any time, using the RabbitMQ or Redis API's
extension endpoint.

When the countdown reaches 0, clusters are deleted and cannot be restored.

.. _streaming-backends:

List Available Backends
-----------------------

Discover available streaming backends and their resource options.

``GET /olcf/v1alpha/streaming/list_backends``

.. tab-set::

   .. tab-item:: curl
      :sync: curl

      .. code-block:: shell

         curl -H @.env \
             https://s3m.olcf.ornl.gov/olcf/v1alpha/streaming/list_backends

   .. tab-item:: Python
      :sync: python

      .. code-block:: python

         from s3m_apis_betterproto.streaming.v1alpha import ListBackendsRequest

         client = factory.create_client(StreamingStub)
         backends = await client.list_backends(ListBackendsRequest())

   .. tab-item:: Go
      :sync: go

      .. code-block:: go

         import (
             "context"
             streamingpb "s3m.olcf.ornl.gov/apis/streaming/v1alpha"
         )

         client := streamingpb.NewStreamingClient(conn)
         backends, err := client.ListBackends(context.Background(), &streamingpb.ListBackendsRequest{})

   .. tab-item:: Python (``requests``)
    :sync: python-requests

        .. code-block:: python

                import os
                import requests

                S3M_BASE_PATH = "https://s3m.olcf.ornl.gov/olcf/v1alpha/streaming"
                S3M_TOKEN = os.getenv("S3M_TOKEN")

                headers = {
                    "Authorization": S3M_TOKEN,
                }

                response = requests.get(
                    f"{S3M_BASE_PATH}/list_backends",
                    headers=headers,
                )

                if response.ok:
                    streaming_response = response.json()
                    print(streaming_response)

                else:
                    raise ValueError("Request to S3M failed")


.. toctree::
   :hidden:

   streaming-rabbitmq
   streaming-redis
