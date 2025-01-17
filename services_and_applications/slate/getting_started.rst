.. _slate_getting_started:

***************
Getting Started
***************

This section will describe the project allocation process for Slate. This is
applicable to both the Onyx and Marble OLCF OpenShift clusters.

In addition, we will go over the process to log into Onyx and Marble, and how
namespaces work within the OpenShift context.

Requesting A Slate Project Allocation
-------------------------------------

Please fill out the `Slate Request Form
<https://www.olcf.ornl.gov/for-users/documents-forms/slate-request/>`_ in order
to use Slate resources. This must be done in order to proceed.

If you have any question please contact `User Assistance
<https://www.olcf.ornl.gov/for-users/>`_, via a **Help Ticket Submission** or
by emailing **help@olcf.ornl.gov**.

| **Required information:**
| - Existing OLCF Project ID
| - Project PI
| - Enclave (i.e. Open or Moderate Enclave - Onyx or Marble respectively)
|   **NOTE:** Frontier is in Moderate
| - Description (i.e., How you will use Slate)
| - Resource Request (i.e., CPU/Memory/Storage requirements - Default is
|   8CPU/16GB/50GB respectively)

Logging in
----------

The web UI for OpenShift is available from all of ORNL (you should be
able to reach it from your laptop on ORNL WiFi as well as the VPN).

+-----------------------------------------------------------------------------+-------------------------------------------------------------------------------------+
| Cluster                                                                     | URL                                                                                 |
+=============================================================================+=====================================================================================+
|  Marble (Moderate Production cluster with access to Frontier/Orion)         | `Marble Web Console - https://marble.ccs.ornl.gov <https://marble.ccs.ornl.gov/>`_  |
+-----------------------------------------------------------------------------+-------------------------------------------------------------------------------------+
|  Onyx   (Open Production Cluster with access to Wolf)                       | `Onyx Web Console - https://onyx.ccs.ornl.gov <https://onyx.ccs.ornl.gov/>`_        |
+-----------------------------------------------------------------------------+-------------------------------------------------------------------------------------+

Slate Namespaces
----------------

Slate Namespaces map directly to OLCF Project ID's. 

Once your Slate Project Allocation Request is approved,
you can create your own namespaces and move your allocation
around those namespaces via the quota dashboard located at `<https://quota.marble.ccs.ornl.gov>`_
and `<https://quota.onyx.ccs.ornl.gov>`_. The terms
"namespace" and "project" may get used interchangeably when referring to your
project's usable space within the requested resource boundaries
(CPU/Memory/Storage).

.. _slate_getting_started_oc:

Install the OC tool
-------------------

The ``oc`` tool provides CLI access to the OpenShift cluster. It needs to be
installed on your machine.

It is a single binary that can be downloaded from a number of places (the
choice is yours):

* Direct from the cluster (preferred):

  * `Marble Command Line Tools <https://console-openshift-console.apps.marble.ccs.ornl.gov/command-line-tools>`_

  * `Onyx Command Line Tools <https://console-openshift-console.apps.onyx.ccs.ornl.gov/command-line-tools>`_

- `Homebrew <https://brew.sh/>`_ on MacOS (need Homebrew setup first): 

 .. note::

     The Homebrew package is not always kept up to date with the latest version
     of OpenShift so some client features may not be available

 .. code-block:: bash

     $ brew install openshift-cli 

- RHEL/CentOS (requires openshift-origin repo):

 .. code-block:: bash

     $ yum install origin-clients

- From Source

`<https://github.com/openshift/oc>`_


Test login with OC Tool
-----------------------

+-----------------------------------------------------------------------------+--------------------------------------+
| Cluster                                                                     | URL                                  |
+=============================================================================+======================================+
|  Marble (Moderate Production cluster with access to Frontier/Orion)         | `<https://api.marble.ccs.ornl.gov>`_ |
+-----------------------------------------------------------------------------+--------------------------------------+
|  Onyx   (Open Production Cluster with access to Wolf)                       | `<https://api.onyx.ccs.ornl.gov>`_   |
+-----------------------------------------------------------------------------+--------------------------------------+

 Replace ``<URL>`` with the appropriate cluster link above (Onyx or Marble).

.. code-block:: bash

   $ oc login <URL> --username=loginName

where the "loginName" is your username for the cluster. After entering the login command above, ``oc`` will ask you to obtain an API token and will provide a URL like the following: ``https://oauth-openshift.apps.<CLUSTER>.ccs.ornl.gov/oauth/token/request``.

You will need to go to the given URL in your browser, log in with NCCS, click the ``Display Token`` link, copy the command under ``Log in with this token`` and enter it into your terminal.

(**NOTE**: Marble authentication uses NCCS Usernames and RSA passcodes. Onyx
uses XCAMS usernames and passwords).

Once you login, the output will tell you what projects/namespaces you have
access to. 

You can view/select/switch between projects/namespaces with the ``oc`` tool:

 .. code-block:: bash
    
    #List all projects/namespaces available to you
    $ oc get projects

    #Use or work within specific project/namespace
    $ oc project <project-name>
