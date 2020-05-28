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


What Accounds Do I Need
-----------------------
