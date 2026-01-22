.. _s3m_streaming_redis:

***********************
S3M - Streaming: Redis
***********************

Redis backends use `Valkey <https://valkey.io>`_, an open-source Redis-compatible key-value store providing
high-performance streams and pub/sub.

**Required Permission:** ``data-streaming``

.. note::

   The Python and Go examples on this page use gRPC client packages that are not yet publicly available.
   ORNL-internal users may request access on a case-by-case basis by contacting the S3M team: `olcf-s3m@email.ornl.gov <mailto:olcf-s3m@email.ornl.gov>`__.
   The REST API (curl examples) is available to all users.

.. note::

   Multi-node Redis clusters are not currently supported.

Cluster Lifecycle
-----------------

* **Lifetime:** 7 day countdown from time of creation
* **Extension:** Countdown can be reset as many times as needed using the extension endpoint
* **Expiration:** Clusters are automatically deleted when they expire, and cannot be restored

Provision Cluster
-----------------

Create a new Redis cluster. The cluster will not be immediately accessible—monitor status with list or get endpoints.

``POST /olcf/v1alpha/streaming/redis/provision_cluster``

.. tab-set::

   .. tab-item:: curl
      :sync: curl

      .. code-block:: shell

         curl -X POST -H @.env \
             -H "Content-Type: application/json" \
             https://s3m.olcf.ornl.gov/olcf/v1alpha/streaming/redis/provision_cluster \
             -d '{
               "kind": "dragonfly-general",
               "name": "mycluster",
               "resourceSettings": {
                 "cpus": 2,
                 "ram-gbs": 4
               }
             }'

   .. tab-item:: Python
      :sync: python

      .. code-block:: python

         from s3m_apis_betterproto.streaming.v1alpha import ProvisionRedisClusterRequest

         client = factory.create_client(RedisStreamingStub)
         result = await client.provision_redis_cluster(ProvisionRedisClusterRequest(
             kind="dragonfly-general",
             name="mycluster",
             resource_settings={"cpus": 2, "ram-gbs": 4}
         ))

   .. tab-item:: Go
      :sync: go

      .. code-block:: go

         import (
             "context"
             streamingpb "s3m.olcf.ornl.gov/apis/streaming/v1alpha"
         )

         client := streamingpb.NewRedisStreamingClient(conn)
         result, err := client.ProvisionRedisCluster(context.Background(), &streamingpb.ProvisionRedisClusterRequest{
             Kind: "dragonfly-general",
             Name: "mycluster",
             ResourceSettings: map[string]int32{"cpus": 2, "ram-gbs": 4},
         })

**Response:**

.. code-block:: json

   {
     "username": "stf040-api",
     "password": "SNTaPeBOpdurUEqy",
     "url": "redis://stf040-api:SNTaPeBOpdurUEqy@redis-stf040-api-mycluster.io.s3m-streams.apps.olivine.ccs.ornl.gov:443"
   }

List Clusters
-------------

``GET /olcf/v1alpha/streaming/redis/list_clusters``

.. tab-set::

   .. tab-item:: curl
      :sync: curl

      .. code-block:: shell

         curl -H @.env \
             https://s3m.olcf.ornl.gov/olcf/v1alpha/streaming/redis/list_clusters

   .. tab-item:: Python
      :sync: python

      .. code-block:: python

         from s3m_apis_betterproto.streaming.v1alpha import ListRedisClustersRequest

         client = factory.create_client(RedisStreamingStub)
         clusters = await client.list_redis_clusters(ListRedisClustersRequest())

   .. tab-item:: Go
      :sync: go

      .. code-block:: go

         import (
             "context"
             streamingpb "s3m.olcf.ornl.gov/apis/streaming/v1alpha"
         )

         client := streamingpb.NewRedisStreamingClient(conn)
         clusters, err := client.ListRedisClusters(context.Background(), &streamingpb.ListRedisClustersRequest{})

Get Cluster
-----------

``GET /olcf/v1alpha/streaming/redis/cluster/{name}``

.. tab-set::

   .. tab-item:: curl
      :sync: curl

      .. code-block:: shell

         curl -H @.env \
             https://s3m.olcf.ornl.gov/olcf/v1alpha/streaming/redis/cluster/mycluster

   .. tab-item:: Python
      :sync: python

      .. code-block:: python

         from s3m_apis_betterproto.streaming.v1alpha import GetRedisClusterRequest

         client = factory.create_client(RedisStreamingStub)
         cluster = await client.get_redis_cluster(GetRedisClusterRequest(name="mycluster"))

   .. tab-item:: Go
      :sync: go

      .. code-block:: go

         import (
             "context"
             streamingpb "s3m.olcf.ornl.gov/apis/streaming/v1alpha"
         )

         client := streamingpb.NewRedisStreamingClient(conn)
         cluster, err := client.GetRedisCluster(context.Background(), &streamingpb.GetRedisClusterRequest{Name: "mycluster"})

Extend Cluster
--------------

Reset the cluster's lifetime to 7 days from now.

``POST /olcf/v1alpha/streaming/redis/extend/{name}``

.. tab-set::

   .. tab-item:: curl
      :sync: curl

      .. code-block:: shell

         curl -X POST -H @.env \
             https://s3m.olcf.ornl.gov/olcf/v1alpha/streaming/redis/extend/mycluster

   .. tab-item:: Python
      :sync: python

      .. code-block:: python

         from s3m_apis_betterproto.streaming.v1alpha import ExtendRedisClusterLifeRequest

         client = factory.create_client(RedisStreamingStub)
         result = await client.extend_redis_cluster_life(ExtendRedisClusterLifeRequest(name="mycluster"))

   .. tab-item:: Go
      :sync: go

      .. code-block:: go

         import (
             "context"
             streamingpb "s3m.olcf.ornl.gov/apis/streaming/v1alpha"
         )

         client := streamingpb.NewRedisStreamingClient(conn)
         result, err := client.ExtendRedisClusterLife(context.Background(), &streamingpb.ExtendRedisClusterLifeRequest{Name: "mycluster"})

Delete Cluster
--------------

``DELETE /olcf/v1alpha/streaming/redis/cluster/{name}``

.. tab-set::

   .. tab-item:: curl
      :sync: curl

      .. code-block:: shell

         curl -X DELETE -H @.env \
             https://s3m.olcf.ornl.gov/olcf/v1alpha/streaming/redis/cluster/mycluster

   .. tab-item:: Python
      :sync: python

      .. code-block:: python

         from s3m_apis_betterproto.streaming.v1alpha import DeleteRedisClusterRequest

         client = factory.create_client(RedisStreamingStub)
         await client.delete_redis_cluster(DeleteRedisClusterRequest(name="mycluster"))

   .. tab-item:: Go
      :sync: go

      .. code-block:: go

         import (
             "context"
             streamingpb "s3m.olcf.ornl.gov/apis/streaming/v1alpha"
         )

         client := streamingpb.NewRedisStreamingClient(conn)
         _, err := client.DeleteRedisCluster(context.Background(), &streamingpb.DeleteRedisClusterRequest{Name: "mycluster"})
