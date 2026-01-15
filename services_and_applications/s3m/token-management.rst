.. _s3m_token_management:

****************
Token Management
****************

Taking the time to properly manage tokens once they have been created is
crucial to ensuring the security of your project's data and continued access
to OLCF API resources. Here are a number of recommendations to assist you.


Immediately Revoke Tokens if Exposed!
-------------------------------------

If for any reason your token has been exposed externally or you suspect it
has been stolen by malicious actors, revoke access to that token right away.
This can be accomplished in either of the following ways:

1. Using the `myOLCF <https://s3m-myolcf.apps.olivine.ccs.ornl.gov/>`_ *Manage Tokens* interface:

   .. image:: ../uploads/myolcf/revoke_token.png
      :alt: myOLCF revoke token

2. Using the token itself to request revocation:

   .. code-block:: shell

      $ curl -i -X DELETE -H "Authorization: $TOKEN" \
          https://s3m.olcf.ornl.gov/olcf/v1/token/ctls/revoke
      HTTP/1.1 200 OK

If you suspect the token has been misused, please contact us
right away for further assistance.

Never Save Token Directly in Code
---------------------------------

Even when simply experimenting with S3M functionality, it is highly
recommended that you never save tokens directly in scripts or code that could
be committed to a repository or saved to a shared system. Instead,
always read tokens from environment variables when possible:

.. code-block:: python

   import requests
   import os

   headers = {
       "Authorization": os.getenv('S3M_TOKEN')
   }

   response = requests.get(
       "https://s3m.olcf.ornl.gov/slurm/v0.0.42/defiant/ping",
       headers=headers)

Avoid Command-Line Arguments
---------------------------

Depending on your system's configuration, providing secrets to an application via command-line arguments can expose them to other users or processes. For example, the full command a user has run can be easily observed by examining the processes found in ``/proc``:

.. code-block:: shell

   $ ./example --token abc123

   $ ps aux | grep token
   user      123 pts/0    Sl+  11:32   0:00 ./example --token abc123

Instead, loading secrets from environment variables or files is a safer
option. For example, you can force `curl <https://www.man7.org/linux/man-pages/man1/curl.1.html>`_
to read header files via *stdin* using the ``@`` symbol:

.. code-block:: shell

   $ cat header-file
   AUTHORIZATION: eyJhbGc...

   $ curl -H @header-file https://s3m.olcf.ornl.gov/slurm/v0.0.42/defiant/ping
   {"meta":{"plugin":{"type":"openapi/slurmctld", "name":"Slurm OpenAPI slurmctld"...

There are exceptions to these risks; however, it is always better to be safe
when writing your production workflows or scripts.

Verify Secret Files are Ignored
-------------------------------

When setting up your project repository, ensure that files or directories that can
contain secrets are properly ignored. Some common files include:

* `.gitignore <https://git-scm.com/docs/gitignore>`_
* `.dockerignore <https://docs.docker.com/reference/dockerfile/#dockerignore-file>`_
* `.helmignore <https://helm.sh/docs/chart_template_guide/helm_ignore_file/>`_

There are other ways you can accidentally expose secrets, so take

the time to examine your specific project's circumstances. Give extra care to
any elements of the project that you are packaging for release.


Principle of Least Privilege
---------------------------

When generating tokens, always request the minimum permissions necessary for
your workflow. Avoid using overly broad scopes or permissions. This reduces
the potential impact if a token is ever compromised and helps enforce
good security practices.

Secure Storage of Tokens
-----------------------

Tokens should be stored securely and never in plaintext files or shared
locations. Consider using secure storage solutions such as password managers,
operating system keyrings, or dedicated secrets management tools. Avoid storing
tokens in version control or in locations accessible to other users.

Example: Using Environment Variables Securely
---------------------------------------------

When using tokens in your workflow, export them as environment variables only
for the duration of your session, and unset them when finished. For example:

.. code-block:: shell

   # Export the token for use in your session
   export S3M_TOKEN="your_token_here"

   # Run your application or script
   python your_script.py

   # Unset the token when done
   unset S3M_TOKEN

This approach helps prevent accidental exposure of tokens and limits
their availability to only the processes that need them.
