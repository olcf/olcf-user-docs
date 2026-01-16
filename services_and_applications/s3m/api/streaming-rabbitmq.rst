.. _s3m_streaming_rabbitmq:

**************************
S3M - Streaming: RabbitMQ
**************************

RabbitMQ is a full-featured message broker with queues and bindings.

**Required Permission:** ``data-streaming``

Cluster Lifecycle
-----------------

* **Lifetime:** 7 day countdown from time of creation
* **Extension:** Countdown can be reset as many times as needed using the extension endpoint
* **Expiration:** Clusters are automatically deleted when they expire, and cannot be restored

Provision Cluster
-----------------

Create a new RabbitMQ cluster. The cluster will not be immediately accessible—monitor status with list or get endpoints.

``POST /olcf/v1alpha/streaming/rabbitmq/provision_cluster``

.. tab-set::

   .. tab-item:: curl
      :sync: curl

      .. code-block:: shell

         curl -X POST -H @.env \
             -H "Content-Type: application/json" \
             https://s3m.olcf.ornl.gov/olcf/v1alpha/streaming/rabbitmq/provision_cluster \
             -d '{
               "kind": "general",
               "name": "mycluster",
               "resourceSettings": {
                 "cpus": 2,
                 "ram-gbs": 4,
                 "nodes": 2
               }
             }'

   .. tab-item:: Python
      :sync: python

      .. code-block:: python

         from s3m_apis_betterproto.streaming.v1alpha import ProvisionRabbitMqClusterRequest

         client = factory.create_client(RabbitMqStreamingStub)
         result = await client.provision_rabbit_mq_cluster(ProvisionRabbitMqClusterRequest(
             kind="general",
             name="mycluster",
             resource_settings={"cpus": 2, "ram-gbs": 4, "nodes": 2}
         ))

   .. tab-item:: Go
      :sync: go

      .. code-block:: go

         import (
             "context"
             streamingpb "s3m.olcf.ornl.gov/apis/streaming/v1alpha"
         )

         client := streamingpb.NewRabbitMQStreamingClient(conn)
         result, err := client.ProvisionRabbitMQCluster(context.Background(), &streamingpb.ProvisionRabbitMQClusterRequest{
             Kind: "general",
             Name: "mycluster",
             ResourceSettings: map[string]int32{"cpus": 2, "ram-gbs": 4, "nodes": 2},
         })

**Response:**

.. code-block:: json

   {
     "username": "stf040-api",
     "password": "bMjHlJKjHQGbWrnO",
     "amqpsUrl": "amqps://stf040-api:bMjHlJKjHQGbWrnO@rmq-stf040-api-mycluster.io.s3m-streams.apps.olivine.ccs.ornl.gov:443",
     "mgmtUrl": "https://rmq-stf040-api-mycluster.mgmt.s3m-streams.apps.olivine.ccs.ornl.gov"
   }

List Clusters
-------------

``GET /olcf/v1alpha/streaming/rabbitmq/list_clusters``

.. tab-set::

   .. tab-item:: curl
      :sync: curl

      .. code-block:: shell

         curl -H @.env \
             https://s3m.olcf.ornl.gov/olcf/v1alpha/streaming/rabbitmq/list_clusters

   .. tab-item:: Python
      :sync: python

      .. code-block:: python

         from s3m_apis_betterproto.streaming.v1alpha import ListRabbitMqClustersRequest

         client = factory.create_client(RabbitMqStreamingStub)
         clusters = await client.list_rabbit_mq_clusters(ListRabbitMqClustersRequest())

   .. tab-item:: Go
      :sync: go

      .. code-block:: go

         import (
             "context"
             streamingpb "s3m.olcf.ornl.gov/apis/streaming/v1alpha"
         )

         client := streamingpb.NewRabbitMQStreamingClient(conn)
         clusters, err := client.ListRabbitMQClusters(context.Background(), &streamingpb.ListRabbitMQClustersRequest{})

Get Cluster
-----------

``GET /olcf/v1alpha/streaming/rabbitmq/cluster/{name}``

.. tab-set::

   .. tab-item:: curl
      :sync: curl

      .. code-block:: shell

         curl -H @.env \
             https://s3m.olcf.ornl.gov/olcf/v1alpha/streaming/rabbitmq/cluster/mycluster

   .. tab-item:: Python
      :sync: python

      .. code-block:: python

         from s3m_apis_betterproto.streaming.v1alpha import GetRabbitMqClusterRequest

         client = factory.create_client(RabbitMqStreamingStub)
         cluster = await client.get_rabbit_mq_cluster(GetRabbitMqClusterRequest(name="mycluster"))

   .. tab-item:: Go
      :sync: go

      .. code-block:: go

         import (
             "context"
             streamingpb "s3m.olcf.ornl.gov/apis/streaming/v1alpha"
         )

         client := streamingpb.NewRabbitMQStreamingClient(conn)
         cluster, err := client.GetRabbitMQCluster(context.Background(), &streamingpb.GetRabbitMQClusterRequest{Name: "mycluster"})

Extend Cluster
--------------

Reset the cluster's lifetime to 7 days from now.

``POST /olcf/v1alpha/streaming/rabbitmq/extend/{name}``

.. tab-set::

   .. tab-item:: curl
      :sync: curl

      .. code-block:: shell

         curl -X POST -H @.env \
             https://s3m.olcf.ornl.gov/olcf/v1alpha/streaming/rabbitmq/extend/mycluster

   .. tab-item:: Python
      :sync: python

      .. code-block:: python

         from s3m_apis_betterproto.streaming.v1alpha import ExtendRabbitMqClusterLifeRequest

         client = factory.create_client(RabbitMqStreamingStub)
         result = await client.extend_rabbit_mq_cluster_life(ExtendRabbitMqClusterLifeRequest(name="mycluster"))

   .. tab-item:: Go
      :sync: go

      .. code-block:: go

         import (
             "context"
             streamingpb "s3m.olcf.ornl.gov/apis/streaming/v1alpha"
         )

         client := streamingpb.NewRabbitMQStreamingClient(conn)
         result, err := client.ExtendRabbitMQClusterLife(context.Background(), &streamingpb.ExtendRabbitMQClusterLifeRequest{Name: "mycluster"})

Delete Cluster
--------------

``DELETE /olcf/v1alpha/streaming/rabbitmq/cluster/{name}``

.. tab-set::

   .. tab-item:: curl
      :sync: curl

      .. code-block:: shell

         curl -X DELETE -H @.env \
             https://s3m.olcf.ornl.gov/olcf/v1alpha/streaming/rabbitmq/cluster/mycluster

   .. tab-item:: Python
      :sync: python

      .. code-block:: python

         from s3m_apis_betterproto.streaming.v1alpha import DeleteRabbitMqClusterRequest

         client = factory.create_client(RabbitMqStreamingStub)
         await client.delete_rabbit_mq_cluster(DeleteRabbitMqClusterRequest(name="mycluster"))

   .. tab-item:: Go
      :sync: go

      .. code-block:: go

         import (
             "context"
             streamingpb "s3m.olcf.ornl.gov/apis/streaming/v1alpha"
         )

         client := streamingpb.NewRabbitMQStreamingClient(conn)
         _, err := client.DeleteRabbitMQCluster(context.Background(), &streamingpb.DeleteRabbitMQClusterRequest{Name: "mycluster"})
