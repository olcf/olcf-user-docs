.. _slate_guided_tutorial_cli:

********************
Guided Tutorial: CLI
********************

This tutorial is a continuation of the :ref:`slate_guided_tutorial` and you should start there.

.. caution::

   You will be creating a single Pod in this tutorial which is not sufficient for a production service


Adding a Pod to your Project
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Before using the CLI it would be wise to read our :ref:`Getting Started on the CLI<slate_getting_started_oc>` doc.

Once the ``oc`` client has been installed and is logged into the cluster you need to switch to your :term:`Project`. Switching to a :term:`Project` allows the ``oc`` client to assume that the commands it is running should be executed inside of the  :term:`Project` that you switch to. You could alternatively not switch to a project and append the ``-n`` flag to each command you run followed by the name of the project you wish to run your command in. That being said, switch to your project:

.. code-block:: bash

   oc project <PROJECT_NAME>

Where `<PROJECT_NAME>` above is the name of your :term:`Project` which will be the name of your RATS allocation. If you need to double check your :term:`Project` name you can run:

.. code-block:: bash

   oc get projects

to get a list of projects that you have access to.

Now, to get a list of pods that exist in the project run:

.. code-block:: bash

   oc get pods

This should not return any :term:`Pods` because there will not be any pods in the project yet.

To remedy this problem we will create a pod. Below is a basic definition of a pod in YAML. Copy this and save it to a file named "pod.yaml".

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

With the above YAML saved in a "pod.yaml" file we can now create the pod with the following command:

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

.. note::
   The ``-f`` flag will follow the logs. You can run the logs command without the ``-f`` flag to get a snapshot of the logs. 

.. code-block:: bash

   oc get pod <POD_NAME> -o yaml

Will allow you to view the YAML representation that exists in Openshift that defines your pod. You may notice that the YAML contains many more key/value pairs than the YAML that we have in our "pod.yaml" file. This is correct and is because extra YAML is added during the pod creation process.

Finally, to get a remote shell in the pod we run the ``oc rsh <POD_NAME>`` command. This will default to using ``/bin/sh`` in the pod. If a different shell is required, we can provide the optional ``--shell=/path/to/shell`` flag. For example, if we wanted to open a bash shell in the pod we would run the following command:

.. code-block:: bash

   oc rsh --shell='/bin/bash' <POD_NAME>
   
If you have multiple containers in your pod, the ``oc rsh <POD_NAME>`` command will default to the first container. If you would like to start a remote shell in one of the other containers, you can use the optional ``-c <CONTAINER_NAME>`` flag.