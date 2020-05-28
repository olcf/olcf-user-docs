***********************************
Getting Started with ECP CI at OLCF
***********************************

It is important to note that ECP CI capabilities are currently limited to the :ref:`ascent-user-guide` system. The ability to enable this on Summit is a work in progress.

Getting Your Project Setup for ECP CI at OLCF
---------------------------------------------

An important realization is that NCCS has two separate enclaves, Open and Moderate, with different resources. The ECP CI capability is only enabled in the Open enclave at this time, running on the :ref:`ascent-user-guide` system, not the Moderate enclave (Summit).

This is important because you may already have a project setup within NCCS, for accessing Summit. If so, this project needs to be mirrored to the Open enclave for working with ECP CI on Ascent (assuming that is the project code you want to setup to use the ECP CI framework).

So, the first thing is to establish a project in the NCCS Open Enclave. There are two options for this:

	- Mirror an existing project from Moderate to Open for ECP CI
	- Request a new project to be created in the Open enclave for ECP CI

For both of these options please email `accounts@ccs.ornl.gov <accounts@ccs.ornl.gov>`_ to initate the request.

**What to include in the request(s):**

	For mirroring:

		- The project PI (they need to approave the mirror request)
		- The Project ID
		- Statement that this is for ECP CI

	For new project request:

		- Name of the project
		- Project PI
		- Initial users


What Accounds Do I Need?
------------------------

Accessing Ascent and working in the NCC Open enclave requires an ORNL Resource Account. Users can register for an account at this `User Portal <https://user.ornl.gov/>`_. 

This is different from your NCCS Account/User ID.

**NOTE:** ORNL Staff do not need to create an account and can use their standard ORNL User ID.

Applying For Project Access
---------------------------

To gain access to a project, fill out the `Account Request Form <https://www.olcf.ornl.gov/support/getting-started/olcf-account-application>`_.

**Please be sure to have this necessary information:**

	- Your ORNL Resource Account User ID
	- The Project ID
	- The Project PI

Accessing the CI Infrastructure
-------------------------------

Currently, ECP CI at OLCF is limited to the `code.ornl.gov <https://code.ornl.gov/>`_ Gitlab Server. It is specifically limited to the "ecpcitest" `group <https://code.ornl.gov/ecpcitest>`_, within that Gitlab Server.

Your NCCS Open project needs to have a Gitlab project setup, within the "ecpcitest" group, on `code.ornl.gov <https://code.ornl.gov/>`_.

Once you have your NCCS Open Project setup, please submit a ticket to `help@olcf.ornl.gov <help@olcf.ornl.gov>`_ requesting the Gitlab project be setup.

In the end, you should be able to log into these systems:

	- `code.ornl.gov <https://code.ornl.gov/>`_
	-  ssh <Your_UID>@login1.ascent.olcf.ornl.gov 

**NOTE:** Both of these systems require you to use your ORNL Resource Account User ID. This is different than your NCCS User ID.
