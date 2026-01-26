.. _s3m_project_setup:

********************
Set Up Your Project
********************

All S3M services are accessible via RESTful JSON APIs, so you can use ``curl`` or HTTP requests in your language of
choice. For more complex integrations, auto-generated Python and Go client libraries are available; these may help you
catch issues with your requests and make it easier to develop against S3M using an IDE with code assistance.

.. note::

   The following OpenAPI v3 spec is not publicly available.
   ORNL-internal users may request access by contacting the S3M team: `olcf-s3m@email.ornl.gov <mailto:olcf-s3m@email.ornl.gov>`__.

You can obtain the S3M API's OpenAPI v3 spec `here <https://code.ornl.gov/s3m/s3m-apis.specs/-/blob/main/openapi3/openapi.yaml?ref_type=heads>`__.

.. tab-set::

   .. tab-item:: curl (REST)
      :sync: curl

      **No Setup Required**

      Use ``curl`` or any HTTP client to call the REST API directly.

      **Authentication**

      Most S3M endpoints require your token in the ``Authorization`` header. Store your token in a header file for
      secure, repeatable use:

      .. code-block:: shell

         # Create a header file with your token (replace with your actual token)
         echo "Authorization: your-token-here" > .env

         # Add to .gitignore to prevent accidental commits
         echo ".env" >> .gitignore

         # Use curl's @ syntax to read the header from the file
         curl -H @.env https://s3m.olcf.ornl.gov/olcf/v1alpha/status

      This approach keeps tokens out of your shell history and environment variables.
      See :doc:`token-management` for more security best practices.

   .. tab-item:: Python
      :sync: python

      .. note::

         The gRPC API specs, Python client package, and Go client package are not yet publicly available. ORNL-internal users may request access by contacting the S3M team: `olcf-s3m@email.ornl.gov <mailto:olcf-s3m@email.ornl.gov>`__.

      **Prerequisites**

      * Python 3.9+
      * **SSH Key Setup**: The Python module is hosted on a private ORNL GitLab instance (``code.ornl.gov``). You must have an SSH key pair configured on your machine and the public key registered in your `code.ornl.gov profile <https://code.ornl.gov/-/user_settings/ssh_keys>`_.

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
         from s3m_apis_betterproto.streaming.v1alpha import StreamingStub, RabbitMqStreamingStub, RedisStreamingStub
         from s3m_apis_betterproto.tms.v1 import TokenControlStub

   .. tab-item:: Go
      :sync: go

      .. note::

         The gRPC API specs, Python client package, and Go client package are not yet publicly available. ORNL-internal users may request access by contacting the S3M team: `olcf-s3m@email.ornl.gov <mailto:olcf-s3m@email.ornl.gov>`__

      **Prerequisites**

      * Go 1.24+
      * **SSH Key Setup**: The Go module is hosted on a private ORNL GitLab instance (``code.ornl.gov``). You must have an SSH key pair configured on your machine and the public key registered in your `code.ornl.gov profile <https://code.ornl.gov/-/user_settings/ssh_keys>`_.

      **Project Initialization**

      Because ``s3m.olcf.ornl.gov/apis`` is a private Go module stored on an ORNL GitLab instance at ``code.ornl.gov``,
      Go cannot discover it automatically via the public proxy. You must use a ``replace`` directive to tell Go
      specifically where to find the source code.

      .. code-block:: shell

         # Make a project folder
         mkdir my-s3m-project
         cd    my-s3m-project

         # Define your project and point it to the ORNL-internal Go S3M module
         go mod init my-s3m-project
         go mod edit -replace s3m.olcf.ornl.gov/apis=code.ornl.gov/s3m/s3m-apis.go.git@latest

         # Go should now download the module and save it in your repo. GOPRIVATE makes Go use your SSH key for authentication
         export GOPRIVATE=code.ornl.gov
         go mod tidy
         go mod vendor

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

   .. tab-item:: Python (``requests``)
        :sync: python-requests

        **Prerequisites**

        * Python 3.9+
        * ``requests`` Python library
        * a ``.env`` file with ``S3M_TOKEN=<your token>``

        **Setup**

        .. code-block:: bash

            source .env
            pip install requests

        **Authentication and Usage**

        .. code-block:: python

            import os
            import requests

            S3M_BASE_PATH = "https://s3m.olcf.ornl.gov/olcf/v1alpha"
            S3M_TOKEN = os.getenv("S3M_TOKEN")

            # This sets the Authorization header like the curl example
            headers = {
                "Authorization": S3M_TOKEN,
            }

            response = requests.get(
                S3M_BASE_PATH + "/status", # to target the "status" service
                headers=headers,
            )

            if response.ok:
                status_response = response.json()
                print(status_response)

            else:
                raise ValueError("Request to S3M failed")