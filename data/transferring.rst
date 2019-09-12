===========================================================
Transferring Data
===========================================================

Data Transfer 
===============

Many users would like to transfer their data from or to Summit through Globus, but their institute does not provide a globus infrastructure. In the following instructions, you can learn how to create your own Globus endpoint. We don't know if or when globus will not support this approach anymore. 

How to use Globus from my laptop
--------------------------------

``scp`` and ``rsync`` are available on Summit for small remote
transfers. For larger remote transfers with Alpine, we recommend using Globus to do the remote transfer.

  Follow the steps:

-  Visit https://www.globus.org/globus-connect-personal and Install Globus Connect Personal, it is available foe Windows, Mac, and Linux

- Selecting the appropriate link there are detailed instructions about the installation, for example, for Mac: https://docs.globus.org/how-to/globus-connect-personal-mac/
- Remember the name of the endpoint that you declared, in this example, the endpoint is *laptop_gmarkom*

- When the installation has finished, click on the globus icon and select *Web: Transfer Files* as below 

.. image:: /images/globus_personal1.png
   :align: center
   :width: 200

- Globus will ask you to login, choose the *Sign in with Google*

.. image:: /images/globus_google.png
   :align: center
   :width: 600

- Now you are in the main globus web page, we select two panels (up right), we declare left the endpoint of the laptop and on the right the *OLCF DTN* (the order does not matter) and 

.. image:: /images/globus_laptop_summit.png
   :align: center

- Then navigate to the appropriate paths to select the files you want to tranfer
 
.. image:: /images/globus_laptop_transfer.png
   :align: center

- Then an activity report will appear and you can click on it to see
   the status. When the transfer is finished or failed, you will receive
   an email

.. image:: /images/globus_laptop_activity.png
   :align: center


-  You can see the status when you click to the activity report

.. image:: /images/globus_laptop_activity_done.png
   :align: center
