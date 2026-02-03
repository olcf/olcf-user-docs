.. _s3m_get_a_token:

***********
Get a Token
***********

.. warning::

   **Before generating a token, understand these security essentials:**

   - Tokens are tied to you and are **your** responsibility, not just the project's
   - **Never** commit tokens to git or share them publicly
   - **Immediately revoke** exposed tokens (see :ref:`s3m_token_revocation`)
   - Use **minimum necessary permissions** for your workflow

   For more on token security, see :doc:`token-management`.

Access to the resources in the OLCF Facility API is restricted to your project via an access token. This means that
when you generate a token using myOLCF it is always scoped to the project itself, not your user account. For example,
if using the compute resource to submit a job via Slurm it will run under your project ``_auser`` account.

Generate a Token
----------------

**1. Navigate to:** `https://my.olcf.ornl.gov <https://my.olcf.ornl.gov>`_

**2. Log in using an Open account.**

   .. image:: ../uploads/myolcf/myOLCF_Login.png
      :alt: myOLCF Login Page

**3. Select the Project you want an S3M token for.**

   .. note::
       If your required project doesn't have an "S3M Access" option in the sidebar, S3M likely isn't enabled for it yet;
       please contact S3M support at <olcf-s3m@email.ornl.gov> for help.

   .. image:: ../uploads/myolcf/Select_Project.png
      :alt: Select Project

**4. Navigate to the** ``S3M Access -> New Token`` **page.** Here you can generate a token with the desired permissions
and expiration controls.

   .. image:: ../uploads/myolcf/Create_Token.png
      :alt: Create Token

5. **Finally, copy the token and store it someplace safe (please, NOT in source code).** Once you leave this page, you
   can't retrieve your token again.

Manage Existing Tokens
----------------------

You can view existing tokens, their permissions, current expiration, and revoke them via the ``Manage Tokens`` page.
