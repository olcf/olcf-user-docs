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

.. note::

   The KubeConfig credentials expires every 24 hours and ``kubectl`` commands will start to error
   out. You will need to do the above steps again
   after a 24 hour period. 



Create a new namespace
----------------------

OLCF User Assistance will help you create a namespace for your project.
Please contact User Assistance at help@olcf.ornl.gov

It is helpful to also CC the your project's PI, who will need to provide permission for creation of an automation user and the namespace.

.. todo: we should probably do this by default with a Lux Kube allocation


Some Kubernetes Basics
----------------------

Kubernetes is an open-source workload manager primarily used for automating deployment, scaling, and management of containerized applications.
It provides a rich API and workload primitives that allows users to manage the application deployments of long running services such as web servers and databases.

This documentation will focus on using the ``kubectl`` command line tool for creating and
manipulating resources on Kubernetes. The Rancher dashboard can also be used to do the same things,
but here we will use it mainly for viewing the status of resources and some limited interactions.

Workloads are defined as YAML file(s)
The most basic form of workload is a ``pod``.

Setting the default namespace
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can set the default namespace for the operations you want to run with ``kubectl``
with 

.. code-block:: bash

   kubectl config set-context --current --namespace=<your namespace>

Without this, you will need to pass a ``--namespace <your namespace>`` flag to any commands you run.

.. note::

   You may need to do the above every time you set up new KubeConfig credentials in ``~/.kube/config``

.. _lux-pods:

Pods
^^^^

A pod is the most basic and fundamental workload in Kubernetes, and consists of one or more containers.
See an example below:

.. code-block:: yaml

    apiVersion: v1
    kind: Pod
    metadata:
    metadata:
      name: hello-pod
      labels:
        app: hello-pod
    spec:
      containers:
      - image: rancher/hello-world
        name: hello-pod
        ports:
        - containerPort: 80
      restartPolicy: Never


Save the above in a file named ``pod.yaml``. Create this pod with ``kubectl apply -f pod.yaml``. You
can view the status of the pod by running ``kubectl get pods``.

You can open a shell into the container in the running pod with  (TODO: verify)

.. code-block:: 

   kubectl exec -it hello-pod -- /bin/sh

Deployment
^^^^^^^^^^

A deployment is a simple and common representation of managing multiple replicated :ref:`lux-pods`.
Deployments facilitate easy scaling of pods to adjust to load.

See an example below:

.. code-block:: yaml

    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: recreate-example
    spec:
      replicas: 2
      selector:
        matchLabels:
          deployment: recreate-example
      strategy:
        # We set the type of strategy to Recreate, which means that it will be scaled down prior to being scaled up
        type: Recreate
      template:
        metadata:
          labels:
            deployment: recreate-example
        spec:
          containers:
          - image: rancher/hello-world
            name: deployment-example

An explanation:

* ``replicas`` - the number of replicas Pods
* ``selector`` - the selector to determine which Pods are managed by the Deployment and underlying `ReplicaSet <https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/>`__.
* ``template`` - the Pod specification/definition. This must include the label specified by the ``selector`` under ``metadata.labels``.

Services
^^^^^^^^

Services allow your :ref:`lux-pods` to communicate with one-another.

The below example will create a Service listening on port 9376 pointing to our Pod above:

.. code-block:: yaml

    apiVersion: v1
    kind: Service
    metadata:
      name: hello-service
    spec:
      selector:
        app: hello-pod
      ports:
        - protocol: TCP
          port: 8080
          targetPort: 80

You can then connect to the Pod from another pod by using 

.. code-block:: bash

    curl hello-service:8080

You can also create a service that refers to a Deployment

.. code-block:: yaml

    apiVersion: v1
    kind: Service
    metadata:
      name: hello-service
    spec:
      selector:
        deployment: recreate-example
      ports:
        - protocol: TCP
          port: 8080
          targetPort: 80



Port Forwarding (To View Your Application's Output)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you wish to view the output of your application you deployed on your browser, you can do so by
port forwarding to the port set up by the Service with the ``kubectl port-forward`` command.

.. code-block:: sh

   # Format: kubectl port-forward <object type>/<object name> <local port>:<remote port>
   kubectl port-forward service/hello-service 8080:8080 

   # you can also port forward directly to the pod or deployment. The remote port will be 80 since that is 
   # where the web app is being served for rancher/hello-world
   kubectl port-forward pod/hello-pod 8080:80


You can now open your browser and navigate to ``localhost:8080`` to see the webpage being served by
Pod behind the Service.

Example Application
^^^^^^^^^^^^^^^^^^^

The ``lux/guestbook`` example in the `olcf_kubernetes_examples repository <https://github.com/olcf/olcf_kubernetes_examples/>`_ 
demonstrates the above concepts together in a simple web application with a frontend and Redis.

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


Storage
-------

Using PersistentVolumeClaims
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

TBD

Accessing the Orion Filesystem
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

TBD


