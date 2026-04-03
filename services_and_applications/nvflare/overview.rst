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