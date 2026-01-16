.. _s3m_project_setup:

********************
Set Up Your Project
********************

All S3M services are accessible via RESTful JSON APIs, so they're fully usable via ``curl`` or HTTP requests in your
language. For more complex integrations, auto-generated Python and Go client libraries are available; these may help
you catch issues with your requests, and make it easier to develop against S3M using an IDE with code assistance.

.. tab-set::

   .. tab-item:: curl
      :sync: curl

      **No Setup Required**

      Use ``curl`` or any HTTP client to call the REST API directly.

      **Authentication**

      Most S3M endpoints require your token in the ``Authorization`` header:

      .. code-block:: shell

         export S3M_TOKEN="your-token-here"

         curl -H "Authorization: $S3M_TOKEN" \
             https://s3m.olcf.ornl.gov/olcf/v1alpha/status

      **Secure Token Handling**

      Avoid passing tokens directly on the command line, where they may appear in shell history or process listings.
      Consider storing them in env files instead:

      .. code-block:: shell

         # Create an env file (add to .gitignore!)
         echo 'export S3M_TOKEN="your-token-here"' > .env

         # Source the file and use the variable
         source .env && curl -H "Authorization: $S3M_TOKEN" \
             https://s3m.olcf.ornl.gov/olcf/v1alpha/status

      Please add such files to your ``.gitignore``! See :doc:`token-management` for more security best practices.

   .. tab-item:: Python
      :sync: python

      **Prerequisites**

      * Python 3.9+

      **Installation**

      Install the ``s3m-apis-betterproto`` library directly from our internal GitLab repository.

      .. code-block:: shell

         pip install git+https://code.ornl.gov/s3m/s3m-apis.pyb.git

      **Project Template**

      The library provides a ``S3MClientFactory`` helper class to initiate S3M connections. Use it as an asynchronous
      context manager to ensure connections are closed properly.

      .. code-block:: python

         import asyncio
         import os
         from s3m_apis_betterproto.clientfactory import S3MClientFactory

         SERVICE_URL = "s3m.olcf.ornl.gov"

         async def main():
             # Status doesn't require a token, so you can leave the second arg blank
             token = os.environ.get('S3M_TOKEN', '')

             async with S3MClientFactory(SERVICE_URL, token) as factory:
                 # Create client stubs and make API calls here
                 # Example: client = factory.create_client(StatusStub)
                 pass

         if __name__ == "__main__":
             asyncio.run(main())

      **Available Client Stubs**

      Import the stub for the API you need:

      .. code-block:: python

         from s3m_apis_betterproto.status.v1alpha import StatusStub
         from s3m_apis_betterproto.slurm.v0043 import SlurmIndirectStub
         from s3m_apis_betterproto.streaming.v1alpha import StreamingStub
         from s3m_apis_betterproto.tms.v1 import TokenControlStub

   .. tab-item:: Go
      :sync: go

      **Prerequisites**

      * Go 1.24+
      * **SSH Key Setup**: The Go module is hosted on a private ORNL GitLab instance (``code.ornl.gov``). You must have
      an SSH key pair configured on your machine and the public key registered in your
      `code.ornl.gov profile <https://code.ornl.gov/-/user_settings/ssh_keys>`_.

      **Project Initialization**

      Create a new directory for your project and initialize the Go module:

      .. code-block:: shell

         mkdir my-s3m-project
         cd my-s3m-project
         go mod init my-s3m-project

      **Installation**

      Because ``s3m.olcf.ornl.gov/apis`` is a private Go module stored on an ORNL GitLab instance at ``code.ornl.gov``,
      Go cannot discover it automatically via the public proxy. You must use a ``replace`` directive to tell Go
      specifically where to find the source code.

      .. code-block:: shell

         # Point the module path to the private git repository
         go mod edit -replace s3m.olcf.ornl.gov/apis=code.ornl.gov/s3m/s3m-apis.go.git@latest

         # Download the module (GOPRIVATE makes Go use your SSH key for authentication)
         GOPRIVATE=code.ornl.gov go get s3m.olcf.ornl.gov/apis
         GOPRIVATE=code.ornl.gov go mod tidy

      **An example main.go file**

      Use ``s3mutil.NewS3MConn`` to establish a secure gRPC connection.

      .. code-block:: go

         package main

         import (
             "context"
             "os"

             "s3m.olcf.ornl.gov/apis/pkg/s3mutil"
         )

         const ServiceURL = "s3m.olcf.ornl.gov"

         func main() {
             token := os.Getenv("S3M_TOKEN")

             conn, err := s3mutil.NewS3MConn(ServiceURL, token)
             if err != nil {
                 panic(err)
             }
             defer conn.Close()

             // Create clients and make API calls here
             // Example: client := statuspb.NewStatusClient(conn)
         }

      **Available Client Packages**

      Import the package for the API you need:

      .. code-block:: go

         import (
             statuspb "s3m.olcf.ornl.gov/apis/status/v1alpha"
             slurmpb "s3m.olcf.ornl.gov/apis/slurm/v0043"
             streamingpb "s3m.olcf.ornl.gov/apis/streaming/v1alpha"
             tmspb "s3m.olcf.ornl.gov/apis/tms/v1"
         )
