.. _nvflare_overview:

********
Overview
********

`NVFlare <https://nvflare.readthedocs.io/en/main/>`_ is an open-source SDK that enables researchers to transition existing machine learning workflows 
into a secure, federated environment with minimal code modifications. It is specifically designed for data scientists who need to train robust AI 
models on sensitive datasets that are siloed by privacy regulations, intellectual property protections, or strict compliance requirements.

How NVFlare Works
-----------------

NVFlare overcomes the limitations of traditional centralized training by bringing the model to the data, rather than the data to the model:

* **Localized Training**: Raw data remains strictly local and private to each participant (client). The central server sends the model architecture to these clients, where training occurs on-site.

* **Secure Aggregation**: Instead of sharing data, clients send only their model weight updates back to the server.

* **Global Intelligence**: The server securely aggregates these local updates into a "global model". This allows the final model to learn from a diverse, multi-institutional dataset without the sensitive information ever leaving its original source.

Getting Started
---------------

The OLCF offers users a simple means of deploying and managing NVFlare campaigns via `myOLCF <https://my.olcf.ornl.gov/>`_.
Firstly, you will need to opt into the service by navigating to the `Federated Learning >> Opt In/Out` tab and change your status to "Yes".

.. image:: /images/nvflare/opt_in.heic

Once opted-in you will see 3 additional subtabs:

* :ref:`campaigns` - landing page that shows the current FL campaigns you have created and are managing, and the campaigns in which you have joined as a member.
* :ref:`campaign_create` - page that allows you to create new campaigns.
* :ref:`campaign_market` - page that displays other campaigns that are currently being advertised.

.. _campaigns:

Project Campaigns
-----------------

The `Project Campaign(s)` page is the dedicated portal for managing the campaigns you own or have joined.
If you have created a campaign, you may view and edit the details, approve or decline join requests, and deploy or
conclude your campaign from this page. If a reservation on Frontier is required for coordinated deployment and training of your
model, you may make a reservation request using the `Request Reservation` button. The `Request Reservation` will
submit a templated ticket to the OLCF help desk on your behalf and will initiate the approval process from the OLCF 
Resource Utilization Council (RUC). After the RUC approves of the reservation, the reservation details including the 
reservation name, time and resource allotment will be displayed in the `Frontier Reservations` subsection. Once a campaign
has been deployed, all participating projects - including campaign managers - can download the necessary startup files and
scripts from the `Projects Participating` subsection. For more details on getting started after campaign deployment, please
see :ref:`nvflare_connect`.

.. image:: /images/nvflare/campaign_details.heic

.. _campaign_create:

FL Campaign Create
------------------

The `FL Campaign Create` page is where you provide the details and Python package requirements of your campaign.
Your campaign description should be informative and specific, so that others may discover your campaign on the
:ref:`campaign_market` and contribute to your campaign goals. The `Campaign Python Packages` will be utilized during the
deployment build process to create your campaign environment. Here you may optionally choose to advertise your campaign
on the :ref:`campaign_market` at creation time. After creation, campaign managers can change whether or not their campaign is adverstised
any time on the :ref:`campaigns` page.

.. warning::
    If any listed Python package in `Campaign Python Packages` are known to have high or critical vulnerabilites, the campaign will be prohibited 
    from deploying and a banner will display warning you of the insecure packages.

.. image:: /images/nvflare/campaign_create.heic

.. _campaign_market:

FL Campaign Market
------------------

The `FL Campaign Market` is where you can find campaigns advertised by other projects. The `Request to Join` button will send
an approval request to the manager of the campaign. A greyed out `Already Sent Request` button will appear for campaigns you
own, have already joined, or have a pending request.

.. image:: /images/nvflare/campaign_market.heic


