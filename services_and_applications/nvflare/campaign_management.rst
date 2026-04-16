.. _nvflare_management:

*******************
Campaign Management
*******************

Managing your campaign involves steps such as:
* Allowing projects onto your campaign
* Managing projects on your campaign
* Joining options for your campaign
* Adding or removing dependencies for your application
* Making group reservations for synchronous federated learning
* Deploying your campaign

In order to see your campaign details, click on "Federated Learning" -> "Project Campaign(s)", and then under "Actions"
click the "Details" button on the campaign you want to manage.

.. image:: /images/nvflare/project_campaigns.png
	:alt: An screenshot showing a populated list of project campaigns with Action buttons "Details," "Edit," and "Delete."
	:width: 50%

Managing Projects on a Campaign
===============================

Allow Projects to Join
----------------------

Projects that discovered your campaign through the marketplace will appear in the list of "Projects Requesting to Join"
You can Approve or Reject their requests in this box.

When a project is approved, members of the approved project can find your campaign in their own "Project Campaigns" list,
where files will be generated for them to run the campaign.

.. image:: /images/nvflare/project_request_join.png
	:alt: A screenshot showing a snippet of the "Projects Requesting to Join" box with active "Approve"/"Reject" buttons.
	:width: 50%

Removing Projects from Campaign
-------------------------------

Projects may need to be removed from your campaign. If that is the case, you can do so from the "Projects Participating" list.

.. image:: /images/nvflare/projects_participating.png
	:alt: A screenshot showing a snippet of the "Projects Participating" box with an active "Remove" button.
	:width: 50%

This section also gives you the ability to download your campaign's run files, and the run files of other participating
projects in your campaign.


Campaign Dependencies
=====================

Modifying Dependencies
----------------------

Environment dependencies can be modified after campaign creation discussed in :ref:`campaign_create`.

In order to modify your campaign's dependencies, click on the "Edit Campaign" button under "FL Campaign Details"
and add/update your dependencies

.. image:: /images/nvflare/campaign_details.png
	:alt: A screenshot showing a snippet of the "FL Campaign Details" box with an active "Edit Campaign" button.
	:width: 50%

You can enter your dependencies similarly to a Python "requirements.txt", with or without version specifications (``==, <=, >=``):

.. image:: /images/nvflare/requirements_spec.png
	:alt: A screenshot showing a snippet of the Campaign Edit screen, with a few Python dependencies listed.

When you are finished you can choose "Submit"

Vulnerabilities
---------------

If your campaign dependencies have a known vulnerability, there will be a list of vulnerabilities aggregated by severity
directly below your dependency list, as shown in the following image.

.. image:: /images/nvflare/vulnerability_overview.png
	:alt: A screenshot showing a snippet of the "FL Campaign Details" box with an vulnerabilities highlighted
	:width: 50%

You can view the list of discovered vulnerabilities from this screen by clicking on one of the severity labels.
E.g. ``Critical - 6`` from the screenshot above.

.. image:: /images/nvflare/vulnerability_report.png
	:alt: A screenshot showing a snippet of the "Vulnerability Details" screen with vulnerabilities displayed by severity and CVE
	:width: 50%

You can see the affected packages and their related CVE's on this page, along with potential version suggestions.


Making Reservations on OLCF Machines
====================================

myOLCF gives project PIs the ability request reservations on Frontier for synchronous federated learning to make the most
of your campaigns.

.. image:: /images/nvflare/campaign_reservation.png
	:alt: A screenshot showing a snippet of the Campaign Reservations screen with an "Add" button highlighted

A project PI can request a reservation for any number of nodes required for each participating project via the UI, and for
a specific timeslot so that the campaign can be synchronized across projects.
This request will be submitted to the OLCF Helpdesk help@olcf.ornl.gov where OLCF User Assistance will collect any necessary
additional information and communicate when a decision is made on the reservation request.
