.. _s3m_getting_started:

***************
Getting Started
***************

Access to the resources in the OLCF Facility API are restricted to your
project via an access token. This means that when you generate a token
using myOLCF it is always scoped to the project itself, not your user
account. For example, if using the compute resource to submit a job via Slurm
it will run under your project ``_auser`` account.

Steps to Generate a Token
-------------------------

1. Navigate to: `https://my.olcf.ornl.gov <https://my.olcf.ornl.gov>`_
2. Login using your ``UCAMS/XCAMS (Open) Log In``

   .. image:: ../uploads/myolcf/login.png
      :alt: myOLCF Login Page

3. Select your appropriate Project under which the token will be associated.

   - If your required project does not have the ability to create tokens please contact us for assistance.

   .. image:: ../uploads/myolcf/not_allowed.png
      :alt: Project Not Allowed

4. Navigate to the ``API Access -> New Tokens`` page and generate a token with the desired permissions and expirations.

   - During initial testing we are still establishing what acceptable token expirations can be offered. Feedback is always welcome but please be patient as initial values will be changed.

   .. image:: ../uploads/myolcf/new_token.png
      :alt: New Token

5. Finally copy the token and store it someplace safe. Once the screen is closed your token will no longer be accessible.

   .. image:: ../uploads/myolcf/copy_token.png
      :alt: Copy Token

Once a token has been generated you can view existing tokens, their
permissions, current expiration, and even revoke them via the GUI
found in the ``Manage Tokens`` page.

.. image:: ../uploads/myolcf/manage_tokens.png
   :alt: Manage Tokens

Token Structure
---------------

The OLCF Project Access Token is a simple JWT that will only be observed
within the S3M API. The payload of the tokens itself only conveys a small
piece of the overall token's capabilities:

.. code-block:: json

   {
     "description": "docs-example-01",
     "type": "opat",
     "aud": [
       "api.olcf.ornl.gov"
     ],
     "nbf": 1730990738,
     "iat": 1730990738,
     "jti": "9aaa44e6-f370-42f9-aafa-895994d44411"
   }

However, so long if the token is valid, you can utilize the introspection API
to gather real time data on the token and its associated permissions. This is
helpful as the expiration of your token can change based upon options such as
the delayed start and future extension feature:

.. code-block:: shell

   $ curl -s -H "Authorization: $TOKEN" \
       https://s3m.olcf.ornl.gov/olcf/v1/token/ctls/introspect | jq
   {
     "token": {
       "username": "stf040-api_auser",
       "project": "STF040-api",
       "scopes": [
         "compute-ace",
         "data-streaming"
       ],
       "plannedExpiration": "2024-11-08T14:45:38.756330Z",
       "securityEnclave": "open",
       "description": "docs-example-01",
       "oneTimeToken": false,
       "delayedStart": false,
       "delayDuration": ""
     }
   }
