=================
Kubernetes On Lux
=================

Kubernetes on Lux is administered through Rancher. You can access the `dashboard here <https://console.apps.slate-mod.ccs.ornl.gov/dashboard/home>`__ .

.. warning::

   The Lux Kubernetes nodes don't have internet access. So either include your data as part of your
   container or set the following environment variables in your container

   .. code-block::
    
      export all_proxy=socks://proxy.ccs.ornl.gov:3128/
      export ftp_proxy=ftp://proxy.ccs.ornl.gov:3128/
      export http_proxy=http://proxy.ccs.ornl.gov:3128/
      export https_proxy=http://proxy.ccs.ornl.gov:3128/
      export no_proxy='localhost,127.0.0.0/8,*.ccs.ornl.gov'

.. note::

   We will be referencing the `olcf_kubernetes_examples repository <https://github.com/olcf/olcf_kubernetes_examples>`__ throughout this page. Make
   sure you have that repository cloned on your laptop and workstation so you can reference it.

Setting up the kubectl commandline tool
---------------------------------------

* Follow the steps from `kubectl docs <https://kubernetes.io/docs/tasks/tools/#kubectl>`__ that is most appropriate to install kubectl on your laptop or workstation. 
* Then navigate to the Lux Rancher dashboard.
* On the Rancher dashboard, click on the button in the top navbar that says 'Copy KubeConfig to Clipboard'. This copies the
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

Under ``spec.containers`` in your deployment or pod configuration, you can include the GPU resource requests
for each container request as fields under the ``.resources`` field. For example:

.. code-block::

  spec:
    containers:
    - image: "docker.io/subilabrahamornl/sampletorch:latest"
      name: gpu-pod
      command: ["python3"]
      args: ["/root/sampletorch.py"]
      resources:
        limits:
          amd.com/gpu: 1
        requests:
          amd.com/gpu: 1


See the `torch_simple example <https://github.com/olcf/olcf_kubernetes_examples/tree/main/lux/torch_simple>`__ on how to run a pod with Pytorch running an MNIST example.

Accessing the Orion Filesystem
------------------------------

TODO: TBD


