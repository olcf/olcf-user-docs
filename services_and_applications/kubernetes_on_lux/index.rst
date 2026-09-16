=================
Kubernetes On Lux
=================

Kubernetes on Lux is administered through Rancher. You can access the `dashboard here <https://console.apps.slate-mod.ccs.ornl.gov/dashboard/home>`__ .

Setting up the kubectl commandline tool
---------------------------------------

* Follow the steps from `kubectl docs <>`__ that is most appropriate to install kubectl on your laptop or workstation. 
* Then navigate to the Lux Rancher dashboard.
* Click on the button in the top navbar that says 'Copy KubeConfig to Clipboard'. This copies the
  configuration into your clipboard.
* On your laptop or workstation, create a file named `~/.kube/config` and paste the contents into
  the file.

You should now be able to use ``kubectl`` to perform operations on Kubernetes on Lux. 

Create a new namespace
----------------------

Some Kubernetes Basics
----------------------


GPU Usage on Kubernetes
-----------------------

Accessing the Orion Filesystem
------------------------------


