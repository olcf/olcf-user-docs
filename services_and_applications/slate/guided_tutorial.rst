.. _slate_guided_tutorial:

***************
Guided Tutorial
***************

This tutorial is meant to be followed step by step so you can get a basic understanding of Openshift and Openshift objects. This will only cover a very surface level knowledge of all the things you can accomplish with Openshift but will hopefully get you familiar with the foundational concepts. 

If you have not already done so, you will need to get an allocation on either our Granite or Marble cluster. To do this contact help@olcf.ornl.gov.

Before we dive in there are some terms that need to be understood. This will be a basic set of terms and a copy and paste from our :ref:`slate_glossary`, so we recommend reading that document and even keeping it handy until you are familiar with all of the definitions there. On that note, another good piece of reference documentation the :ref:`slate_examples` document. There you can find basic YAML definitions for the most common objects in Kubernetes.

Pre Openshift Tutorial Tasks
----------------------------

Terms to be familiar with for this tutorial
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Slate:** An encompassing term to describe the Openshift resources provided by the Platforms team in the HPC Data and Operations group.

**Cluster:** One of the Kubernetes cluster (Granite or Marble) that the Platform team in the HPC Data and Operations group supports. 

**Object:** Object is *something* in a Kubernetes Cluster. This something can be a Pod, Route, Deployment, Stateful Set or any one of the other things you define in YAML and create in the cluster. Objects are added to the cluster through the Kubernetes API. You will almost certainly only ever interact with the Kubernetes API through the ``oc`` client or through the web GUI at: ``https://console-openshift-console.apps.<CLUSTER_NAME>.ccs.ornl.gov``

**Host/Node:** The machine or VM that is a member of the Kubernetes cluster. A Node is where Kubernetes objects execute.

**Container:** A container is a set of linux namespaces and cgroups which isolate a running process from other containers and the rest of the OS.

**Images:** A ready to run package of software. This will contain the necessary components needed to run some specific task or application.

**Pod:** A Pod is a group of containers with shared networking and storage. These containers will be co-located and co-scheduled and run in a shared context. You can think of a Pod as a “logical host” - it contains one or more application containers which are relatively tightly coupled — in a pre-container world, being executed on the same physical or virtual machine would mean being executed on the same logical host.

**Deployment:** An object that represents multiple, identical Pods. A Deployment is an ``Owner`` of a Pod and likewise if the Deployment is deleted so too are the Pods that it owns.

**Project:** A way to divide cluster resources. Contain a subsection of authorization and policy from the cluster i.e. someone in another project cannot delete your Pods. A project gets its resource allocation from an overarching RATS project. This means that a RATS project can have a 1:1 mapping with a project or a 1:many mapping with multiple projects. All of the projects under a RATS project will take away from the quota of the overarching RATS project and all quota is managed in RATS. This is all simplified by the Quota Dashboard.

These are just the specific terms that you will need to know to make use of this tutorial. It is recommended that upon completion of this tutorial you go and familiarize yourself with the :ref:`slate_glossary` page.

Creating your project
---------------------

Before you can do anything you need a **project** to do your things in. Fortunately, when you get an allocation on one of our clusters a **project** is automatically created for you with the same name as the allocation. By using our own distinct **project** we are ensuring that we will not interfere with anyone elses work.

NOTE: Everywhere that you see `<CLUSTER_NAME>` replace that with the cluster that you will be running on (marble or onyx).

Now that you have a project you can create objects inside that project. We will be doing this with the Openshift Web GUI and the ``oc`` CLI client so you can use whichever interface you are more comfortable with in this tutorial. If you are more comfortable using the command line than you are using a GUI you can now `jump to the oc portion of this document. <#guided-oc-tutorial>`_. Otherwise, if you are more comfortable with the GUI `skip to the GUI portion of the tutorial <#guided-web-gui-tutorial>`_.

Guided Web GUI Tutorial
-----------------------

Go to ``https://console-openshift-console.apps.<CLUSTER_NAME>.ccs.ornl.gov/k8s/cluster/projects``

Adding a Pod to your Project
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once you have navigated to ``https://console-openshift-console.apps.<CLUSTER_NAME>.ccs.ornl.gov/k8s/cluster/projects`` you should see a list of **projects** or projects, that you have access to. Scroll down or use the filter box in the upper right to select your project; your project will have the same name as your allocation in RATS. Once there your screen should look similar to the picture below:


.. image:: /images/slate/project-view.png
   :target: /images/slate/project-view.png
   :alt: 


**NOTE:** The name of the pictured project is of the form ``RATS_ALLOCATION-CUSTOM_NAME``. Your project will be only ``RATS_ALLOCATION``.

From here, in the left hand hamburger menu click on the 'Workloads' tab and then the 'pods' tab:


.. image:: /images/slate/pod-view.png
   :target: /images/slate/pod-view.png
   :alt: 


Here you will be able to view all of the **pods** in your **project**. Since this is a new **project** there will be no **pods** in it. To create a **pod** click the 'Create Pod' button.

This will bring you to a screen of pre populated YAML that you can edit in the browser. This YAML is the basis of a podspec that will be sent to the API server once you click the 'Create' button in the lower left to create a **pod** in your **project**. Here we will make a few slight modifications to the podspec.

First, we will replace the ``openshift/hello-openshift`` value after the ``image`` tag with value ``image-registry.openshift-image-registry.svc:5000/openshift/ccs-rhel7-base-amd64``. This is the **image** that the **pod** will be using. We will be using the ccs-base image; a bare-bones image provided by the platforms team that is usually used as the foundation to build more complex custom images on top of.

Secondly, the **pod** needs something to do when it starts. For an nginx server this would be running nginx, for a flask app this would be running the app.py file etc. For illustrative purposes this **pod** is going to be starting a shell with the ``/bin/sh`` command, echoing a "Hello World!" prompt then running a ``cat`` command as a means to keep the pod running. Without the addition of the ``cat`` at the end the ``echo`` command would end causing the ``/bin/sh`` to end causing the **pod** to go from a status of ``Running`` to ``Completed``.  To make these changes add the following lines below the ``image`` line:

``command: ["/bin/sh","-c"]``

``args: ["echo 'Hello World!'; cat"]``

Finally, we need a tty. This will give us the ability to open a shell in our **pod** and get a better understanding of what is happing. To do this, add the following two lines under the command line that you just added:

``tty: true``

``stdin: true``

Your page should now look as follows:


.. image:: /images/slate/ccs-base-pod-yaml.png
   :target: /images/slate/ccs-base-pod-yaml.png
   :alt: 


You can now click the 'Create' button in the lower left which will take you to the screen where the **pod** is created.

You should now be on the 'Pod' screen with the 'Overview' tab selected From here you can get a quick idea of the amount of resources (memory, CPU etc) that your **pod** is using.

Click on the 'Logs' tab to get the logs from your pod. This will display "Hello World!" in our example because of our echo command. There will be a dropdown here that for our example will contain only one item named 'hello-openshift'. This is the name of the container that you are viewing the logs for inside your pod.

The 'Events' tab is for the events that took place to create your pod. This is for things that happen outside of the code that is running inside your pod such as pulling the pod image, scheduling the pod onto a node etc.

The 'Terminal' tab will give you a tty inside your pod. Here you can run most commands as you normally would on a RedHat machine.

Guided oc Tutorial
------------------

Adding a Pod to your Project
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Before using the CLI it would be wise to read our `Getting Started on the CLI <../getting_started_cli>`_ doc.

Once the **oc** client has been installed and is logged into the cluster you need to switch to your **project**. Switching to a **project** allows the **oc** client to assume that the commands it is running should be executed inside of the  **project** that you switch to. You could alternatively not switch to a project and append the ``-n`` flag to each command you run followed by the name of the project you wish to run your command in. That being said, switch to your project:

.. code-block:: bash

   oc project <PROJECT_NAME>

Where `<PROJECT_NAME>` above is the name of your **project** which will be the name of your RATS allocation. If you need to double check your **project** name you can run:

.. code-block:: bash

   oc get projects

to get a list of projects that you have access to.

Now, to get a list of pods that exist in the project run:

.. code-block:: bash

   oc get pods

This should not return any **pods** because there will not be any pods in the project yet.

To remedy this problem we will create a pod. Below is a basic definition of a pod in YAML. Copy this and save it to a file named pod.yaml.

.. code-block:: yaml

    apiVersion: v1
    kind: Pod
    metadata:
      # Pod name
      name: test-pod
    spec:
      containers:
        # Container name
        - name: test-container
          # Using the base image
          image: "image-registry.openshift-image-registry.svc:5000/openshift/ccs-rhel7-base-amd64"
          # Starting a shell
          command: ["/bin/sh","-c"]
          # Echoing a Hello World followed by an infinitely waiting cat
          args: ["echo 'Hello World!'; cat"]
          # Need a tty if we are to SSH. Need stdin for tty
          tty: true
          stdin: true

With the above YAML saved in a pod.yaml file we can now create the pod with the following command:

.. code-block:: bash

   oc create -f pod.yaml

Now if we run the command:

.. code-block:: bash

   oc get pods

We should see our pod along with some status information about the pod.

To get useful metrics about the pod we can run:

.. code-block:: bash

   oc describe pod <POD_NAME>

where `<POD_NAME>` will be the name of the pod. In our case test-pod.

To get logs from the pod we can run the command:

.. code-block:: bash

   oc logs -f <POD_NAME>

*NOTE* the ``-f`` flag will follow the logs. You can run the logs command without the ``-f`` flag to get a snapshot of the logs. Additionally, this will be empty for the pod we created above because there will be no logs from the 'cat' command.

.. code-block:: bash

   oc get <POD_NAME> -o yaml

Will allow you to view the YAML representation that exists in Openshift that defines your pod. You may notice that the YAML contains many more key/value pairs than the YAML that we have in our pod.yaml file. This is correct and is because extra YAML is added during the pod creation process.

Finally, to get a shell in the pod we run the ``oc exec`` command. What this command does is execute a command inside the pod; for us the command will be ``/bin/bash``.

.. code-block:: bash

   oc exec -it <POD_NAME> /bin/bash
