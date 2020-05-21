.. _slate_getting_started:

*****************************
Getting Started
*****************************

This section will descsribe the project allocation process for Slate. This is applicable
to both the Onyx and Marble OLCF OpenShift clusters.

| In addtion, we will go over the process to log into Onyx and Marble and how namespaces work within the OpenShift context.

Requesting A Slate Project Allocation
-------------------------------------

Please fill out the `Slate Request Form <https://www.olcf.ornl.gov/for-users/documents-forms/slate-request/>`_ in order to use Slate resources. This must be done, in order to proceed.

If you have any question please contact `User Assitance <https://www.olcf.ornl.gov/for-users/>`_, via a **Help Ticket Submission**, by emailing **help@olcf.ornl.gov**.

| **Required information:**
| - Existing OLCF Project ID
| - Project PI
| - Enclave (i.e. Open or Moderate Enclave - Onyx or Marble respectively)
|   **NOTE:** Summit is in Moderate
| - Description (i.e. How you will use Slate)
| - Resource Request (i.e. CPU/Memory/Storage requirements - Default is 8CPU/16GB/50GB respectively)

Logging in
----------

The web UI for OpenShift should be available from all of ORNL (you should be able to reach it from your laptop on ORNL WIFI as well as the VPN).

+-----------------------------------------------------------------------------+-------------------------------------------------------------------------------------+
| Cluster                                                                     | URL                                                                                 |
+=============================================================================+=====================================================================================+
|  Marble (Moderate Production cluster with access to Summit/Alpine)          | `Marble Web Console <https://console-openshift-console.apps.marble.ccs.ornl.gov/>`_ |
+-----------------------------------------------------------------------------+-------------------------------------------------------------------------------------+
|  Onyx   (Open Production Cluster with access to Wolf)                       | `Onyx Web Console <https://onyx.ccs.ornl.gov/>`_                                    |
+-----------------------------------------------------------------------------+-------------------------------------------------------------------------------------+

Slate Namespaces
----------------

Slate Namespaces map directly to OLCF Project ID's. 

| Once your Slate Project Allocation Request is approved you will see your project's namespace, on the appropriate OpenShift Cluster, upon login.
  The terms "namespace" and "project" may get used interchangebly when referring to your project's useable space, within the requested resource boundaries (CPU/Memory/Storage), on OpenShift.