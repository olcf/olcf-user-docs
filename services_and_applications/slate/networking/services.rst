.. _slate_services:

********
Services
********

In Kubernetes, a :term:`Service` is an internal load balancer which identifies a set of pods and can proxy traffic to them.
This set of pods is determined by a label selector.

A service is a **stable** way of accessing a set of pods, which are ephemeral. 

When a service is created, it is granted a ``ClusterIP``\ , which is an IP address internal to the
Kubernetes cluster. Other pods can use this ClusterIP to access the service.

Here is an example service definition:

.. code-block:: yaml

   apiVersion: v1
   kind: Service
   metadata:
     name: my-service
   spec:
     selector:
       name: my-app
     ports:
     - port: 8080
       protocol: TCP
       targetPort: 8080

This definition tells Kubernetes that all pods with the label "my-app" are associated with this service. Any traffic to the service should be distributed
among these pods. 

The *port* parameter contains what port the service listens on, and the *targetPort* parameter contains the port to which the service forwards connections.

Creating Services
-----------------

CLI
^^^

On the command line, services can be created with the command ``oc create``. Assuming our YAML file from above is in the file ``my-service.yaml``\ , you can
create the service with

.. code-block:: text

   $ oc create -f my-service.yaml

Then, you can run ``oc describe service my-service`` to see some information about it.

.. code-block:: text

   $ oc describe service my-service
   Name:                   my-service
   Labels:                 <none>
   Selector:               name=my-app
   Type:                   ClusterIP
   IP:                     172.31.34.153
   Port:                   <unnamed>       8080/TCP
   Endpoints:              10.132.7.126:8080,10.132.7.127:8080,10.132.7.123:8080
   Session Affinity:       None
   No events.

In this example, looking at *Endpoints*\ , we have 3 pods running with the ``my-app`` selector. This means that from inside the cluster
if an application accesses the ClusterIP on port 8080 the traffic will be directed to one of the three pods.

Accessing Services from Outside the Cluster
-------------------------------------------

A service of type ClusterIP will only ever be accessible from inside the cluster. If you need access to your service from outside
of the cluster there are a few different options.

Route
^^^^^

In general, using FQDNs to access a service is more convenient. If your service communicates over HTTP or HTTPS, you can set up a 
:ref:`slate_routes` to achieve this. If your service uses another protocol, you can use :ref:`slate_nodeports`.

NodePort
^^^^^^^^

NodePort is a type of Service that reserves a port across the cluster that can route traffic to your pods. This is more flexible
than a Route and can handle any TCP or UDP traffic.
