===========================================================
Transferring Data
===========================================================

Data Transfer 
===============

Many users will need to move or copy their data from Titan (Atlas) to
Summit (Alpine). The Alpine file system is mounted on OLCF's data
transfer nodes and is feasible to transfer data with tools such as
globus. The following sections will outline the current options for
transferring data to and from Alpine.


Below is a screencast showing the process of transferring data from
Atlas to Alpine.

Remote Transfers with Alpine
----------------------------

``scp`` and ``rsync`` are available on Summit for small remote
transfers. For larger remote transfers with Alpine, we recommend staging
the data through Alpine and using Globus to do the remote transfer.

  Follow the steps:

-  Visit www.globus.org and login

.. image:: /images/globus_first_page.png
   :align: center

-  Then select the organization that you belong, if you don't work for
   ORNL, do not select ORNL. If your organization is not in the list,
   create a Globus account

.. image:: /images/globus_organization.png
   :align: center

-  Search for the endpoint **OLCF DTN**

.. image:: /images/search_endpoint1.png
   :align: center

.. image:: /images/search_endpoint2.png
   :align: center


-  Declare path

.. image:: /images/declare_path.png
   :align: center

add image
add image

-  Open a second panel to declare where your files would like to be
   transferred, select if you want an encrypt transfer, select your
   file/folder and click start

add image
add image
add image


-  Then an activity report will appear and you can click on it to see
   the status. When the transfer is finished or failed, you will receive
   an email

add image
add image

