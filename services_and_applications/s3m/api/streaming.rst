.. _s3m_streaming_api:

*********
Streaming
*********

The Streaming API enables on-demand provisioning of message queue clusters for high-throughput data streaming to OLCF
compute resources.

**Required Permission:** ``data-streaming``

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

.. toctree::
   :hidden:

   streaming-rabbitmq
   streaming-redis
