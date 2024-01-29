
**************
Deploy MongoDB
**************

MongoDB is a common "NoSQL" database. We will be creating a Deployment to run the MongoDB service
and expose it external to the cluster after setting up authentication. We will also be deploying a
management Web UI for viewing queries.

Prerequisites
^^^^^^^^^^^^^

* Access to an allocation in Slate, the NCCS Kubernetes service
* ``oc`` client installed
* CLI client is logged into the cluster (\ ``oc login https://api.<cluster>.ccs.ornl.gov --username=loginName``\ )

Deploy MongoDB
^^^^^^^^^^^^^^

We will be deploying MongoDB with a
`StatefulSet <https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/>`_. This is a
special kind of deployment controller that is different from a normal Deployment in a few distinct
ways and is primarily meant for for applications that rely on well known names for each pod.

We will create a Service with the StatefulSet because the StatefulSet controller requires a headless
service in order to provide well-known DNS identifiers.

.. code-block:: yaml

   apiVersion: v1
   kind: Service
   metadata:
     name: mongo
     labels:
       app: mongo
   spec:
     ports:
     - port: 27017
       name: mongo
     selector:
       app: mongo
   ---
   apiVersion: apps/v1
   kind: StatefulSet
   metadata:
     name: mongo
   spec:
     serviceName: "mongo"
     replicas: 1
     selector:
       matchLabels:
         app: mongo # has to match .spec.template.metadata.labels
     template:
       metadata:
         labels:
           app: mongo # has to match .spec.selector.matchLabels
       spec:
         terminationGracePeriodSeconds: 10
         containers:
         - name: mongo
           image: mongo
           env:
           - name: MONGO_INITDB_ROOT_USERNAME
             value: admin
           - name: MONGO_INITDB_ROOT_PASSWORD
             value: password
           ports:
           - containerPort: 27017
             name: mongo
           volumeMounts:
           - name: mongo-store
             mountPath: /data/db
     volumeClaimTemplates:
     - metadata:
         name: mongo-store
       spec:
         accessModes: ["ReadWriteOnce"]
         resources:
           requests:
             storage: 1Gi

.. note::
   You should replace the value under ``MONGO_INITDB_ROOT_PASSWORD`` with something other than ``password``, such as with a randomly generated password for this purpose (just be sure to save this file and the password). While the service will not be accessible outside NCCS, it is good practice to secure your data with a secure password.

Create a file with the above contents and instantiate the objects in Kubernetes

.. code-block:: text

   oc apply -f statefulset.yaml

Run some commands to check on the StatefulSet


* ``oc describe statefulset mongo``
* ``oc logs statefulset/mongo``
* ``oc describe service mongo``
* ``oc get pods -l app=mongo -o wide``
* ``oc exec -it mongo-0 /bin/bash``

Deploy Mongoku (Management UI)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml

   apiVersion: apps/v1
   kind: Deployment
   metadata:
     labels:
       app: mongoku
     name: mongoku
   spec:
     replicas: 1
     selector:
       matchLabels:
         app: mongoku
     template:
       metadata:
         labels:
           app: mongoku
       spec:
         containers:
         - image: huggingface/mongoku
           name: mongoku

Create a file with the above contents and instantiate the objects in Kubernetes

.. code-block:: text

   oc apply -f deployment.yaml

.. note::
  Snippet created with ``oc create deployment mongoku --image huggingface/mongoku --dry-run -o yaml``

Run some commands to check on the Deployment


* ``oc describe deployment mongoku``
* ``oc logs deployment/mongoku``
* ``oc port-forward deployment/mongoku 3100:3100``

.. note::
   The ``oc port-forward`` command runs in the foreground. To test connectivity, one would need to
   use the MongoDB CLI from a second terminal.

Since we created the ``mongo`` service with the StatefulSet, all pods in our namespace will be able
to resolve that ClusterIP so we can add a server to mongoku with just the service name.

Steps to configure mongoku


* Navigate to http://localhost:3100
* Add Server -> "admin:password@mongo:27017"
* Click "mongo"

Expose MongoDB outside of the cluster
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We could use the port forwarding technique but that uses a connection that goes through the API
server for the cluster which is not very performant. We will change the Service/mongo object so
that it creates a NodePort that we can access from outside of the cluster.

.. code-block:: text

   $ oc patch service mongo -p '{"spec":{"type":"NodePort"}}'
   $ oc get service mongo
   NAME    TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)           AGE
   mongo   NodePort   172.25.233.185   <none>        27017:32093/TCP   13s

In this example, the NodePort that was automatically assigned was 32093 which is routing traffic to 27017 on the Service.

We will also need to add a network rule to allow ingress traffic.

.. code-block:: yaml

   kind: NetworkPolicy
   apiVersion: networking.k8s.io/v1
   metadata:
     name: mongo-allow-external
   spec:
     podSelector:
       matchLabels:
         app: mongo
     ingress:
       - {}
     policyTypes:
       - Ingress

Create a file with the above contents and apply the network policy:

.. code-block:: text

   oc apply -f networkpolicy.yaml

We can now connect to the db from another host inside of NCCS:

.. code-block:: text

   mongo -u admin -p password apps.<cluster>.ccs.ornl.gov:32093

* **cluster** is the Slate cluster (marble, onyx)
* The port number should be the one listed from the ``service`` command listed above. It may differ from the example, so be sure to update accordingly.
* Change the password to the randomly generated one you created during set up.

Teardown
^^^^^^^^

Once we have finished, we should remove the resources we created.

.. note::
  We have to remove the PVC that was created by the StatefulSet

.. code-block:: text

   oc delete service mongo
   oc delete statefulset mongo
   oc delete persistentvolumeclaim mongo-store-mongo-0
   oc delete deployment mongoku
