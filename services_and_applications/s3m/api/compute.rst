.. _s3m_compute_api:

*******
Compute
*******

The Compute API provides access to SLURM job scheduling on select OLCF resources. The implementation is
"SLURM Indirect"—it mirrors the `official SLURM REST API <https://slurm.schedmd.com/rest_api.html>`_ structure.

**Required Permission:** ``compute-ace`` or ``compute-ace-readonly``

.. note::

   The Python and Go examples on this page use gRPC client packages that are not yet publicly available.
   ORNL-internal users may request access by contacting the S3M team: `olcf-s3m@email.ornl.gov <mailto:olcf-s3m@email.ornl.gov>`__.
   The REST API (via curl or otherwise) is available to all users.

Available Resources
-------------------

* Defiant II (``defiant``)
* Wombat (``wombat``)
* Quokka (``quokka``)

.. note::

   API version v0.0.42 endpoints remain available but are deprecated. Migrate to v0.0.43 for full compatibility with
   SLURM 25.05.

Ping Resource
-------------

Check the health status of a compute resource.

``GET /slurm/v0.0.43/{resource}/ping``

.. tab-set::

   .. tab-item:: curl
      :sync: curl

      .. code-block:: shell

         curl -H @.env \
             https://s3m.olcf.ornl.gov/slurm/v0.0.43/defiant/ping

   .. tab-item:: Python
      :sync: python

      .. code-block:: python

         from betterproto.lib.std.google.protobuf import Empty

         client = factory.create_client(SlurmIndirectStub)
         pong = await client.ping(Empty())

   .. tab-item:: Go
      :sync: go

      .. code-block:: go

         import (
             "context"
             "google.golang.org/protobuf/types/known/emptypb"
             slurmv0043pb "s3m.olcf.ornl.gov/apis/slurm/v0043"
         )

         client := slurmv0043pb.NewSlurmIndirectClient(conn)
         pong, err := client.Ping(context.Background(), &emptypb.Empty{})

   .. tab-item:: Python (``requests``)
    :sync: python-requests

        .. code-block:: python

                import os
                import requests

                S3M_BASE_PATH = "https://s3m.olcf.ornl.gov/slurm/v0.0.43"
                S3M_TOKEN = os.getenv("S3M_TOKEN")
                resource = "defiant"

                # This sets the Authorization header like the curl example
                headers = {
                    "Authorization": S3M_TOKEN,
                }

                response = requests.get(
                    f"{S3M_BASE_PATH}/{resource}/ping",
                    headers=headers,
                )

                if response.ok:
                    compute_response = response.json()
                    print(compute_response)

                else:
                    raise ValueError("Request to S3M failed")


List Partitions
---------------

Get available partitions (queues) on a resource.

``GET /slurm/v0.0.43/{resource}/partitions``

.. tab-set::

   .. tab-item:: curl
      :sync: curl

      .. code-block:: shell

         curl -H @.env \
             https://s3m.olcf.ornl.gov/slurm/v0.0.43/defiant/partitions

   .. tab-item:: Python
      :sync: python

      .. code-block:: python

         from betterproto.lib.std.google.protobuf import Empty

         client = factory.create_client(SlurmIndirectStub)
         partitions = await client.get_partitions(Empty())

   .. tab-item:: Go
      :sync: go

      .. code-block:: go

         import (
             "context"
             "google.golang.org/protobuf/types/known/emptypb"
             slurmv0043pb "s3m.olcf.ornl.gov/apis/slurm/v0043"
         )

         client := slurmv0043pb.NewSlurmIndirectClient(conn)
         partitions, err := client.GetPartitions(context.Background(), &emptypb.Empty{})

   .. tab-item:: Python (``requests``)
    :sync: python-requests

        .. code-block:: python

                import os
                import requests

                S3M_BASE_PATH = "https://s3m.olcf.ornl.gov/slurm/v0.0.43"
                S3M_TOKEN = os.getenv("S3M_TOKEN")
                resource = "defiant"

                # This sets the Authorization header like the curl example
                headers = {
                    "Authorization": S3M_TOKEN,
                }

                response = requests.get(
                    f"{S3M_BASE_PATH}/{resource}/partitions",
                    headers=headers,
                )

                if response.ok:
                    compute_response = response.json()
                    print(compute_response)

                else:
                    raise ValueError("Request to S3M failed")


Submit a Job
------------

Submit a new batch job to the scheduler.

``POST /slurm/v0.0.43/{resource}/job/submit``

.. tab-set::

   .. tab-item:: curl
      :sync: curl

      .. code-block:: shell

         curl -X POST -H @.env \
             -H "Content-Type: application/json" \
             https://s3m.olcf.ornl.gov/slurm/v0.0.43/defiant/job/submit \
             -d '{
               "job": {
                 "name": "my-job",
                 "account": "STF040",
                 "partition": "batch-cpu",
                 "minimum_nodes": 1,
                 "tasks": 1,
                 "time_limit": {"number": 60, "set": true},
                 "current_working_directory": "/lustre/polis/stf040/scratch/user",
                 "environment": ["PATH=/usr/bin"],
                 "script": "#!/bin/bash\necho Hello World"
               }
             }'

   .. tab-item:: Python
      :sync: python

      .. code-block:: python

         from s3m_apis_betterproto.slurm.v0043 import JobSubmitReq, JobSubmitReqJobDescription, Uint32NoVal

         client = factory.create_client(SlurmIndirectStub)
         result = await client.post_job_submit(JobSubmitReq(
             job=JobSubmitReqJobDescription(
                 name="my-job",
                 account="STF040",
                 partition="batch-cpu",
                 minimum_nodes=1,
                 tasks=1,
                 time_limit=Uint32NoVal(number=60, set=True),
                 current_working_directory="/lustre/polis/stf040/scratch/user",
                 environment=["PATH=/usr/bin"],
                 script="#!/bin/bash\necho Hello World"
             )
         ))

   .. tab-item:: Go
      :sync: go

      .. code-block:: go

         import (
             "context"
             "google.golang.org/protobuf/proto"
             slurmv0043pb "s3m.olcf.ornl.gov/apis/slurm/v0043"
         )

         client := slurmv0043pb.NewSlurmIndirectClient(conn)
         result, err := client.PostJobSubmit(context.Background(), &slurmv0043pb.JobSubmitReq{
             Job: &slurmv0043pb.JobSubmitReq_JobDescription{
                 Name:                    "my-job",
                 Account:                 "STF040",
                 Partition:               "batch-cpu",
                 MinimumNodes:            proto.Int32(1),
                 Tasks:                   proto.Int32(1),
                 TimeLimit:               &slurmv0043pb.Uint32NoVal{Number: 60, Set: true},
                 CurrentWorkingDirectory: "/lustre/polis/stf040/scratch/user",
                 Environment:             []string{"PATH=/usr/bin"},
                 Script:                  "#!/bin/bash\necho Hello World",
             },
         })

   .. tab-item:: Python (``requests``)
    :sync: python-requests

        .. code-block:: python

                import os
                import requests

                S3M_BASE_PATH = "https://s3m.olcf.ornl.gov/slurm/v0.0.43"
                S3M_TOKEN = os.getenv("S3M_TOKEN")
                resource = "defiant"

                headers = {
                    "Authorization": S3M_TOKEN,
                    "Content-Type: application/json"
                }

                # This section defines the job to submit
                payload = {
                    "job": {
                        "name": "my-job",
                        "account": "STF040",
                        "partition": "batch-cpu",
                        "minimum_nodes": 1,
                        "tasks": 1,
                        "time_limit": {"number": 60, "set": true},
                        "current_working_directory": "/lustre/polis/stf040/scratch/user",
                        "environment": ["PATH=/usr/bin"],
                        "script": "#!/bin/bash\necho Hello World"
                    }
                }

                response = requests.post(
                    f"{S3M_BASE_PATH}/{resource}/job/submit",
                    headers=headers,
                    data=payload,
                )

                if response.ok:
                    compute_response = response.json()
                    print(compute_response)

                else:
                    raise ValueError("Request to S3M failed")


**Response:**

.. code-block:: json

   {
     "job_id": 12345,
     "step_id": "batch"
   }

Get Job Status
--------------

Retrieve details about a specific job.

``GET /slurm/v0.0.43/{resource}/job/{job_id}``

.. tab-set::

   .. tab-item:: curl
      :sync: curl

      .. code-block:: shell

         curl -H @.env \
             https://s3m.olcf.ornl.gov/slurm/v0.0.43/defiant/job/12345

   .. tab-item:: Python
      :sync: python

      .. code-block:: python

         from s3m_apis_betterproto.slurm.v0043 import JobIdReq

         client = factory.create_client(SlurmIndirectStub)
         job = await client.get_job(JobIdReq(job_id="12345"))

   .. tab-item:: Go
      :sync: go

      .. code-block:: go

         import (
             "context"
             slurmv0043pb "s3m.olcf.ornl.gov/apis/slurm/v0043"
         )

         client := slurmv0043pb.NewSlurmIndirectClient(conn)
         job, err := client.GetJob(context.Background(), &slurmv0043pb.JobIdReq{JobId: "12345"})

   .. tab-item:: Python (``requests``)
    :sync: python-requests

        .. code-block:: python

                import os
                import requests

                S3M_BASE_PATH = "https://s3m.olcf.ornl.gov/slurm/v0.0.43"
                S3M_TOKEN = os.getenv("S3M_TOKEN")
                resource = "defiant"
                job_id="12345"

                # This sets the Authorization header like the curl example
                headers = {
                    "Authorization": S3M_TOKEN,
                }

                response = requests.get(
                    f"{S3M_BASE_PATH}/{resource}/job/{job_id}",
                    headers=headers,
                )

                if response.ok:
                    compute_response = response.json()
                    print(compute_response)

                else:
                    raise ValueError("Request to S3M failed")


List All Jobs
-------------

Retrieve all jobs visible to your project.

``GET /slurm/v0.0.43/{resource}/jobs``

.. tab-set::

   .. tab-item:: curl
      :sync: curl

      .. code-block:: shell

         curl -H @.env \
             https://s3m.olcf.ornl.gov/slurm/v0.0.43/defiant/jobs

   .. tab-item:: Python
      :sync: python

      .. code-block:: python

         from betterproto.lib.std.google.protobuf import Empty

         client = factory.create_client(SlurmIndirectStub)
         jobs = await client.get_jobs(Empty())

   .. tab-item:: Go
      :sync: go

      .. code-block:: go

         import (
             "context"
             "google.golang.org/protobuf/types/known/emptypb"
             slurmv0043pb "s3m.olcf.ornl.gov/apis/slurm/v0043"
         )

         client := slurmv0043pb.NewSlurmIndirectClient(conn)
         jobs, err := client.GetJobs(context.Background(), &emptypb.Empty{})

   .. tab-item:: Python (``requests``)
    :sync: python-requests

        .. code-block:: python

                import os
                import requests

                S3M_BASE_PATH = "https://s3m.olcf.ornl.gov/slurm/v0.0.43"
                S3M_TOKEN = os.getenv("S3M_TOKEN")
                resource = "defiant"

                # This sets the Authorization header like the curl example
                headers = {
                    "Authorization": S3M_TOKEN,
                }

                response = requests.get(
                    f"{S3M_BASE_PATH}/{resource}/jobs",
                    headers=headers,
                )

                if response.ok:
                    compute_response = response.json()
                    print(compute_response)

                else:
                    raise ValueError("Request to S3M failed")


Cancel a Job
------------

Cancel a running or pending job.

``DELETE /slurm/v0.0.43/{resource}/job/{job_id}``

.. tab-set::

   .. tab-item:: curl
      :sync: curl

      .. code-block:: shell

         curl -X DELETE -H @.env \
             https://s3m.olcf.ornl.gov/slurm/v0.0.43/defiant/job/12345

   .. tab-item:: Python
      :sync: python

      .. code-block:: python

         from s3m_apis_betterproto.slurm.v0043 import DeleteJobReq

         client = factory.create_client(SlurmIndirectStub)
         await client.delete_job(DeleteJobReq(job_id="12345"))

   .. tab-item:: Go
      :sync: go

      .. code-block:: go

         import (
             "context"
             slurmv0043pb "s3m.olcf.ornl.gov/apis/slurm/v0043"
         )

         client := slurmv0043pb.NewSlurmIndirectClient(conn)
         _, err := client.DeleteJob(context.Background(), &slurmv0043pb.DeleteJobReq{JobId: "12345"})

   .. tab-item:: Python (``requests``)
    :sync: python-requests

        .. code-block:: python

                import os
                import requests

                S3M_BASE_PATH = "https://s3m.olcf.ornl.gov/slurm/v0.0.43"
                S3M_TOKEN = os.getenv("S3M_TOKEN")
                resource = "defiant"
                job_id="12345"

                # This sets the Authorization header like the curl example
                headers = {
                    "Authorization": S3M_TOKEN,
                }

                response = requests.delete(
                    f"{S3M_BASE_PATH}/{resource}/job/{job_id}",
                    headers=headers,
                )

                if response.ok:
                    compute_response = response.json()
                    print(compute_response)

                else:
                    raise ValueError("Request to S3M failed")


**Optional Parameters:**

* ``signal`` — Signal to send (e.g., ``SIGTERM``, ``SIGKILL``). Default is ``SIGTERM``.
* ``flags`` — Additional flags for job cancellation.

List Nodes
----------

Get information about compute nodes on a resource.

``GET /slurm/v0.0.43/{resource}/nodes``

.. tab-set::

   .. tab-item:: curl
      :sync: curl

      .. code-block:: shell

         curl -H @.env \
             https://s3m.olcf.ornl.gov/slurm/v0.0.43/defiant/nodes

   .. tab-item:: Python
      :sync: python

      .. code-block:: python

         from betterproto.lib.std.google.protobuf import Empty

         client = factory.create_client(SlurmIndirectStub)
         nodes = await client.get_nodes(Empty())

   .. tab-item:: Go
      :sync: go

      .. code-block:: go

         import (
             "context"
             "google.golang.org/protobuf/types/known/emptypb"
             slurmv0043pb "s3m.olcf.ornl.gov/apis/slurm/v0043"
         )

         client := slurmv0043pb.NewSlurmIndirectClient(conn)
         nodes, err := client.GetNodes(context.Background(), &emptypb.Empty{})

   .. tab-item:: Python (``requests``)
    :sync: python-requests

        .. code-block:: python

                import os
                import requests

                S3M_BASE_PATH = "https://s3m.olcf.ornl.gov/slurm/v0.0.43"
                S3M_TOKEN = os.getenv("S3M_TOKEN")
                resource = "defiant"

                # This sets the Authorization header like the curl example
                headers = {
                    "Authorization": S3M_TOKEN,
                }

                response = requests.get(
                    f"{S3M_BASE_PATH}/{resource}/nodes",
                    headers=headers,
                )

                if response.ok:
                    compute_response = response.json()
                    print(compute_response)

                else:
                    raise ValueError("Request to S3M failed")


List Reservations
-----------------

Get reservations on a resource.

``GET /slurm/v0.0.43/{resource}/reservations``

.. tab-set::

   .. tab-item:: curl
      :sync: curl

      .. code-block:: shell

         curl -H @.env \
             https://s3m.olcf.ornl.gov/slurm/v0.0.43/defiant/reservations

   .. tab-item:: Python
      :sync: python

      .. code-block:: python

         from betterproto.lib.std.google.protobuf import Empty

         client = factory.create_client(SlurmIndirectStub)
         reservations = await client.get_reservations(Empty())

   .. tab-item:: Go
      :sync: go

      .. code-block:: go

         import (
             "context"
             "google.golang.org/protobuf/types/known/emptypb"
             slurmv0043pb "s3m.olcf.ornl.gov/apis/slurm/v0043"
         )

         client := slurmv0043pb.NewSlurmIndirectClient(conn)
         reservations, err := client.GetReservations(context.Background(), &emptypb.Empty{})

   .. tab-item:: Python (``requests``)
    :sync: python-requests

        .. code-block:: python

                import os
                import requests

                S3M_BASE_PATH = "https://s3m.olcf.ornl.gov/slurm/v0.0.43"
                S3M_TOKEN = os.getenv("S3M_TOKEN")
                resource = "defiant"

                # This sets the Authorization header like the curl example
                headers = {
                    "Authorization": S3M_TOKEN,
                }

                response = requests.get(
                    f"{S3M_BASE_PATH}/{resource}/reservations",
                    headers=headers,
                )

                if response.ok:
                    compute_response = response.json()
                    print(compute_response)

                else:
                    raise ValueError("Request to S3M failed")


Scheduler Diagnostics
---------------------

Get diagnostic information about the SLURM scheduler.

``GET /slurm/v0.0.43/{resource}/diag``

.. tab-set::

   .. tab-item:: curl
      :sync: curl

      .. code-block:: shell

         curl -H @.env \
             https://s3m.olcf.ornl.gov/slurm/v0.0.43/defiant/diag

   .. tab-item:: Python
      :sync: python

      .. code-block:: python

         from betterproto.lib.std.google.protobuf import Empty

         client = factory.create_client(SlurmIndirectStub)
         diag = await client.get_diag(Empty())

   .. tab-item:: Go
      :sync: go

      .. code-block:: go

         import (
             "context"
             "google.golang.org/protobuf/types/known/emptypb"
             slurmv0043pb "s3m.olcf.ornl.gov/apis/slurm/v0043"
         )

         client := slurmv0043pb.NewSlurmIndirectClient(conn)
         diag, err := client.GetDiag(context.Background(), &emptypb.Empty{})

   .. tab-item:: Python (``requests``)
    :sync: python-requests

        .. code-block:: python

                import os
                import requests

                S3M_BASE_PATH = "https://s3m.olcf.ornl.gov/slurm/v0.0.43"
                S3M_TOKEN = os.getenv("S3M_TOKEN")
                resource = "defiant"

                # This sets the Authorization header like the curl example
                headers = {
                    "Authorization": S3M_TOKEN,
                }

                response = requests.get(
                    f"{S3M_BASE_PATH}/{resource}/diag",
                    headers=headers,
                )

                if response.ok:
                    compute_response = response.json()
                    print(compute_response)

                else:
                    raise ValueError("Request to S3M failed")

For full request/response details, see the `SLURM REST API documentation <https://slurm.schedmd.com/rest_api.html>`_.
