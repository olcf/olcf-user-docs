.. _s3m_tokens_api:

******
Tokens
******

The Tokens API provides endpoints to introspect and revoke your OLCF Project Access Tokens.

**Required Permission:** Any valid token can perform these actions on itself.

.. note::

   The Python and Go examples on this page use gRPC client packages that are not yet publicly available.
   ORNL-internal users may request access on a case-by-case basis by contacting the S3M team: `olcf-s3m@email.ornl.gov <mailto:olcf-s3m@email.ornl.gov>`__.
   The REST API (via curl or otherwise) is available to all users.

.. _s3m_token_revocation:

Revoke a Token
--------------

**If your token has been exposed, revoke it immediately.**

Revoking a token invalidates it permanently. This is an irreversible action.

``DELETE /olcf/v1/token/ctls/revoke``

.. tab-set::

   .. tab-item:: curl
      :sync: curl

      .. code-block:: shell

         curl -X DELETE -H @.env \
             https://s3m.olcf.ornl.gov/olcf/v1/token/ctls/revoke

   .. tab-item:: Python
      :sync: python

      .. code-block:: python

         from s3m_apis_betterproto.tms.v1 import RevokeAuthTokenRequest

         client = factory.create_client(TokenControlStub)
         await client.revoke_auth_token(RevokeAuthTokenRequest())

   .. tab-item:: Go
      :sync: go

      .. code-block:: go

         import (
             "context"
             tmspb "s3m.olcf.ornl.gov/apis/tms/v1"
         )

         client := tmspb.NewTokenControlClient(conn)
         _, err := client.RevokeAuthToken(context.Background(), &tmspb.RevokeAuthTokenRequest{})

**Response:** HTTP 200 with empty body ``{}``

You can also revoke tokens via the `myOLCF Manage Tokens <https://my.olcf.ornl.gov>`_ interface.

Introspect a Token
------------------

Retrieve details about the current token including its permissions, expiration, and associated project.

``GET /olcf/v1/token/ctls/introspect``

.. tab-set::

   .. tab-item:: curl
      :sync: curl

      .. code-block:: shell

         curl -H @.env \
             https://s3m.olcf.ornl.gov/olcf/v1/token/ctls/introspect

   .. tab-item:: Python
      :sync: python

      .. code-block:: python

         from s3m_apis_betterproto.tms.v1 import IntrospectAuthTokenRequest

         client = factory.create_client(TokenControlStub)
         info = await client.introspect_auth_token(IntrospectAuthTokenRequest())

   .. tab-item:: Go
      :sync: go

      .. code-block:: go

         import (
             "context"
             tmspb "s3m.olcf.ornl.gov/apis/tms/v1"
         )

         client := tmspb.NewTokenControlClient(conn)
         info, err := client.IntrospectAuthToken(context.Background(), &tmspb.IntrospectAuthTokenRequest{})

**Response:**

.. code-block:: json

   {
     "token": {
       "username": "stf040_auser",
       "project": "STF040",
       "plannedExpiration": "2024-11-08T14:45:38.756330Z",
       "securityEnclave": "open",
       "description": "docs-example-01",
       "oneTimeToken": false,
       "delayedStart": false,
       "delayDuration": ""
     }
   }

Token Structure
---------------

OLCF Project Access Tokens are JWTs. The payload conveys basic metadata, but the full capabilities are only available via the introspection API above.

**JWT Payload Fields:**

.. code-block:: json

   {
     "description": "docs-example-01",
     "type": "opat",
     "aud": ["api.olcf.ornl.gov"],
     "nbf": 1730990738,
     "iat": 1730990738,
     "jti": "9aaa44e6-f370-42f9-aafa-895994d44411"
   }

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Field
     - Description
   * - ``description``
     - User-provided description when token was created
   * - ``type``
     - Token type (``opat`` = OLCF Project Access Token)
   * - ``aud``
     - Intended audience for the token
   * - ``nbf``
     - Not valid before (Unix timestamp)
   * - ``iat``
     - Issued at (Unix timestamp)
   * - ``jti``
     - Unique token identifier (UUID)

**Introspection Response Fields:**

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Field
     - Description
   * - ``username``
     - The project user account (``{project}_auser``)
   * - ``project``
     - Associated OLCF project
   * - ``plannedExpiration``
     - When the token will expire (ISO 8601)
   * - ``securityEnclave``
     - Security classification (e.g., ``open``)
   * - ``oneTimeToken``
     - If true, token can only be used once
   * - ``delayedStart``
     - If true, token activation was delayed
   * - ``delayDuration``
     - How long the activation was delayed
