.. _slate_pods:

####
Pods
####

A `pod <http://kubernetes.io/docs/user-guide/pods/>`_ is the smallest unit in Kubernetes, it is a grouping of containers that will be scheduled
together onto a node in the cluster. usually it will just be one container but it could be a group
of processes that make up an application.

Pods have a lifecycle: they are defined, scheduled onto a node, and then they run until their
containers exit or the pod is removed from the node for some reason. Pods are immutable and changes
to a pod are not persisted between restarts.

A pod does **not**

* have state (store state in persistent volumes)
* move nodes once scheduled onto a node
* reschedule itself (we will use higher level controllers to manage pods)

Running a Container in a Pod with the CLI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Lets get started:

.. code-block:: text

   oc run --restart=Never hello-world-pod --image openshift/hello-openshift:latest

Under the hood, the ``oc run`` command is taking options and creating a specification
that it is then passing to Kubernetes to run. To see the spec it is creating append
``-o yaml`` to the ``oc run`` command and you will get an output of what it is sending
to Kubernetes.

The ``--restart=Never`` tells ``oc run`` to generate only a Pod spec. By default it would
generate something more advanced we will talk about later.

The ``openshift/hello-openshift`` is just a simple
`Docker image <https://hub.docker.com/r/openshift/hello-openshift/>`_

List current running pods:

.. code-block:: text

   oc get pods

Get more information on our pod:

.. code-block:: text

   oc describe pod hello-world-pod

Once we see ``Status: Running`` (near the top of the output, not the bottom) we can interact with the container:

.. code-block:: text

   oc port-forward hello-world-pod 8080:8080

And in another terminal run ``curl http://localhost:8080``

The initial port in the port pair references a non-allocated port on our local system similar to how SSH
port forwarding works.

Pods also have logs.
And we can see the logs for the pod: (whatever was printed to stdout from within the container, not kubernetes).

.. code-block:: text

   oc logs hello-world-pod

Now lets delete our pod:

.. code-block:: text

   oc delete pod hello-world-pod

Deleting the pod will remove our ability to inspect the log output from ``oc logs`` so if you are debugging an issue
you will want to keep the pod until the issue is resolved.

Running a Container in a Pod with the Web Console
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To create a single pod using the web console we will create from YAML

First go to Add to Project -> Import YAML / JSON


.. image:: /images/slate/add-to-project.png
   :target: /images/slate/add-to-project.png
   :alt: Add to Project


Then paste this YAML into the box and click Create

.. code-block:: yaml

   apiVersion: v1
   kind: Pod
   metadata:
     creationTimestamp: null
     labels:
       run: hello-world-pod
     name: hello-world-pod
   spec:
     containers:
     - image: openshift/hello-openshift:latest
       imagePullPolicy: IfNotPresent
       name: hello-world-pod
       resources: {}
     dnsPolicy: ClusterFirst
     restartPolicy: Never
   status: {}


.. image:: /images/slate/beginnersguide-import-yaml.png
   :target: /images/slate/beginnersguide-import-yaml.png
   :alt: Import YAML


On the Overview page there should be Other Resources and it should list our ``hello-world-pod`` pod.


.. image:: /images/slate/overview-other-resources.png
   :target: /images/slate/overview-other-resources.png
   :alt: Other Resources


Clicking the title will give us more information about the pod such as it's current status, the node it is
running on, and the container information like resource utilization as well as options to view the log and get
a terminal in the container.


.. image:: /images/slate/beginnersguide-hello-world-pod-describe.png
   :target: /images/slate/beginnersguide-hello-world-pod-describe.png
   :alt: Hello World Pod


Finally we can delete the pod by clicking Actions -> Delete


.. image:: /images/slate/actions-delete-pod.png
   :target: /images/slate/actions-delete-pod.png
   :alt: Pod Actions


More Information
^^^^^^^^^^^^^^^^


* `Kubernetes Pod Overview <https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/>`_
* `OpenShift Pod Overview <https://docs.openshift.org/latest/architecture/core_concepts/pods_and_services.html>`_
