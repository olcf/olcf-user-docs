=================
Kubernetes On Lux
=================

Kubernetes on Lux is administered through Rancher. You can access the `dashboard here <https://console.apps.slate-mod.ccs.ornl.gov/dashboard/home>`__ .

.. warning::

   The Lux Kubernetes nodes don't have internet access. So either include your data as part of your
   container.

.. todo: replace or set the following environment variables in your container

.. todo:
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
      namespace: <namespace>
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
      namespace: <namespace>
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


Run ``kubectl apply -f deployment.yaml`` to create the Deployment.

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
      namespace: <namespace>
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
      namespace: <namespace>
      name: hello-service
    spec:
      selector:
        deployment: recreate-example
      ports:
        - protocol: TCP
          port: 8080
          targetPort: 80

Run ``kubectl apply -f service.yaml`` to create the service.

Jobs
^^^^

Jobs allow you to create and run a one off task or set of tasks that will run to completion and exit. if it exits It still
starts and runs a Pod underneath, with some additional facilities to control the number of
concurrent pods and number of successful completions expected. A Pod will be restarted on failure to try 
again (up to a limit you can specify). Successful completions don't count against the limit. 

As a simple example, lets create a Job that runs an `echo "hello world"` 7 times.

.. code-block:: yaml

   apiVersion: batch/v1
   kind: Job 
   metadata:
     name: hello-job
     labels:
       app: hello-job
   spec:
     completions: 7 # The job completes when it records 7 successful completions
     parallelism: 3 # this allows up to 3 pods to run in parallel at a time
     template: # this is the template for the Pod that will be run by the Job
       spec:
         containers:
           - image: rancher/hello-world
             name: hello-job
             command: ["/bin/bash"]
             args: ["-c", "echo hello world; sleep 10"]
         restartPolicy: Never


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

.. warning::

   GPUs are time limited use and cannot be used for persistent services. They can only be used in
   Jobs.

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

Requesting and Using Multiple GPUs
^^^^^^^^^^^^^^^^

TBD

Storage
-------

Pods are ephemeral and any data written within a Pod is lost when the Pod is restarted or deleted.
Kubernetes provides options for ways to store data persistently. 

Using PersistentVolumeClaims (PVCs) for Persistent Storage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A PersistentVolumeClaim (PVC) lets you request an amount of storage that you can then mount into your Pods.
The below example creates a PVC that requests 5GB of storage.

.. code-block:: yaml

   apiVersion: v1
   kind: PersistentVolumeClaim
   metadata:
     name: storage-1
   spec:
     accessModes:
       - ReadWriteOnce
     resources:
       requests:
         storage: 5Gi

Run ``kubectl apply -f pvc.yaml`` to create this PVC.

With this created, we can mount this PVC to a Pod. Below example creates a Pod with this PVC

.. code-block:: yaml

    apiVersion: v1
    kind: Pod
    metadata:
      namespace: <namespace>
      name: hello-pod
      labels:
        app: hello-pod
    spec:
      containers:
        - image: rancher/hello-world
          name: hello-pod
          ports:
            - containerPort: 80
          volumeMount:
            mountPath: /data
            name: pvol
      restartPolicy: Never
      volumes:
        name: pvol
        PersistentVolumeClaim:
          claimName: storage-1



There are two available storage classes: ``netapp-file`` and ``netapp-block`` for PVCs.
``netapp-file`` is the default and is probably what you need for most of your use cases.
``netapp-block`` is useful when you need a persistent backing store for a database. 


Temporary Storage
^^^^^^^^^^^^^^^^^

PVCs are the right option if you want to make sure your data sticks around between Pod restarts
If you would like to have some additional storage that doesn't need to be persisted between Pod
restarts (like a scratch space or a file cache), there are a couple of options.

One is ``emptyDir`` which lets you set up a cache on the node's local storage with a size limit so
you cannot write to it beyond what is allocated. For example, with our hell


.. code-block:: yaml

    apiVersion: v1
    kind: Pod
    metadata:
      namespace: <namespace>
      name: hello-pod
      labels:
        app: hello-pod
    spec:
      containers:
        - image: rancher/hello-world
          name: hello-pod
          ports:
            - containerPort: 80
          volumeMounts:
          - mountPath: /cache
            name: cache-emptydir
      restartPolicy: Never
      volumes:
      - name: cache-emptydir
        emptyDir:
          sizeLimit: 500Mi
          

Another option is ``ephemeral``, which allocates storage in the same way as PVCs and on the same hardware, and is thus
not limited by what is available on the node's local storage. Unlike PVCs, this gets deleted when
the Pod is deleted. It uses as the same parameters as PersistentVolumeClaims.

.. code-block:: yaml

    apiVersion: v1
    kind: Pod
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
          volumeMounts:
          - mountPath: /cache
            name: cache-ephemeral
      restartPolicy: Never
      volumes:
      - name: cache-ephemeral
        ephemeral:
          volumeClaimTemplate:
            metadata:
              labels:
                name: my-cache-ephemeral
            spec:
              storageClassName: netapp-file
              accessModes:
                - ReadWriteOnce
              resources:
                requests:
                  storage: 5Gi
    

You will see that this creates a pod as well as automatically create a PVC named ``<pod name>-<volume name>``. See it
with ``kubectl get pvc``.

.. note::

   Unlike PVCs, you will not specify a ``metadata.name`` in the ``volumeClaimTemplate`` for
   ephemeral storage. The name is automatically determined.

Accessing the Orion Filesystem
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

TBD


Accessing your Application
--------------------------

Gateways and HTTPRoutes for Accessing your App via the Browser
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

TBD
