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

This section also gives you the ability to download your campaign's run files.


Campaign Details
================

Advertising a Campaign
----------------------

A campaign can be optionally placed on the :ref:`campaign_market` for discovery, which can help recruit other projects.

In order to modify your campaign's appearance on the *Campaign Market*, click on the "Edit Campaign" button under "FL Campaign Details"
and add/update your dependencies.

.. image:: /images/nvflare/fl_campaign_details.png
	:alt: A screenshot showing a snippet of the "FL Campaign Details" box with an active "Edit Campaign" button.
	:height: 30em

At the bottom of the edit page, there is a toggle "Advertise your campaign?" which can be used to display the campaign on
the market.

Modifying Dependencies
----------------------

Environment dependencies can be modified after campaign creation discussed in :ref:`campaign_create`.

In order to modify your campaign's dependencies, click on the "Edit Campaign" button under "FL Campaign Details"
and add/update your dependencies in the "Campaign Python Packages" section.

You can enter your dependencies similarly to a Python "requirements.txt", with or without version specifications (``==, <=, >=``):

.. image:: /images/nvflare/requirements_spec.png
	:alt: A screenshot showing a snippet of the Campaign Edit screen, with a few Python dependencies listed.
	:width: 50%

When you are finished you can choose "Submit" to update your campaign requirements.

Vulnerabilities
---------------

If your campaign dependencies have a known vulnerability, there will be a list of vulnerabilities aggregated by severity
directly below your dependency list, as shown in the following image.

.. image:: /images/nvflare/vulnerability_overview.png
	:alt: A screenshot showing a snippet of the "FL Campaign Details" box with an vulnerabilities highlighted
	:height: 30em

You can view the list of discovered vulnerabilities from this screen by clicking on one of the severity labels.
E.g. ``Critical - 6`` from the screenshot above.

.. image:: /images/nvflare/vulnerability_report.png
	:alt: A screenshot showing a snippet of the "Vulnerability Details" screen with vulnerabilities displayed by severity and CVE
	:width: 50%

You can see the affected packages and their related CVE's on this page, along with potential version suggestions.


Making Reservations on OLCF Machines
====================================

myOLCF gives lead projects the ability request reservations on Frontier for synchronous federated learning to make the most
of your campaigns.

The lead project of a campaign can find the "Request Reservation" button under "FL Campaign Details"

A lead project can request a reservation for any number of nodes required for each participating project via the UI, and for
a specific timeslot so that the campaign can be synchronized across projects.
This request will be submitted to the OLCF Helpdesk help@olcf.ornl.gov where OLCF User Assistance will collect any necessary
additional information, namely PI approvals, and communicate when a decision is made on the reservation request.

.. image:: /images/nvflare/campaign_reservation.png
	:alt: A screenshot showing a snippet of the Campaign Reservations screen with populated "Start," "End,"
		"Node Count," and a "Submit" button highlighted.
	:width: 50%

After making a reservation request, you can see details around the reservation on the "Frontier Reservations" box such
as:

* Approval status
* Reservation name
* Specific start and end times
* Number of nodes requested per project

.. image:: /images/nvflare/frontier_reservations.png
	:alt: A screenshot showing a snippet of the Frontier Reservations screen with described information fields.
	:width: 50%

Deploying The Campaign
======================

Before running any campaign code, the lead project will need to deploy the management service.
This is managed in the "Campaign Deployment Status" box.
Before your campaign and its management service are deployed you will see a green "Deploy Campaign" button along with
some statistics, such as the number of current deployment statuses, number of deployments, and
cumulative duration of the deployments.

When the "Deploy Campaign" button is clicked, it will start a service on Slate for managing your campaign.
The service deployment may take a few minutes.

When the service is up and the campaign is deployed, all member projects of the campaign will have the ability to
download requisite files to connect to the management service for federated learning processes.
You can read more about running code in your campaign in the :ref:`nvflare_connect` section.

.. image:: /images/nvflare/deploy_campaign.png
	:alt: A screenshot showing a snippet of the Campaign Deployment Status screen with information on deployments, and a highlighted "Deploy Campaign" button.
	:width: 50%

When your run is finished, you can click on the "Conclude Campaign" button in the same box to stop the service.

.. warning::

	Stopping the service with the "Conclude Campaign" button will interrupt all NVFlare work in the campaign, even that
	being run on other projects.