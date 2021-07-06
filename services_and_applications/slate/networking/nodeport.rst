.. _slate_nodeports:

*********
NodePorts
*********


A NodePort reserves a port across all nodes of the cluster. This port routes traffic to a service, which points to the pods that match the service's label selector.

NodePorts are given in the 30000-32767 range. These are ports you can use from outside the cluster to access resources inside of OpenShift.

For the Openshift clusters you will additionally need to create a :ref:`network policy <slate_network_policies>` file to allow external traffic into your namespace. 


Configuring a Service NodePort
------------------------------

CLI
^^^

For example, let's look at service that was created in the :ref:`slate_services` document. This document assumes that it was deployed to the ``my-project`` project.


If you run ``oc get services``\ , you should see your service in the list.


.. code-block:: text
   
   $ oc get services
   NAME                  TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)     AGE
   my-service            ClusterIP   172.25.170.246   <none>        8080/TCP    8s


Then, get some information about the service with ``oc describe service my-service``.

.. code-block:: text

   $ oc describe services my-service
   Name:              my-service
   Namespace:         my-project
   Labels:            <none>
   Annotations:       <none>
   Selector:          name=my-app
   Type:              ClusterIP
   IP:                172.25.170.246
   Port:              <unset>  8080/TCP
   TargetPort:        8080/TCP
   Endpoints:         <none>
   Session Affinity:  None
   Events:            <none>

Note the ``Type`` under the service is ``ClusterIP``. This is the default value for services, but we want to expose it with a NodePort.

In order to expose the service with a NodePort, we need to change ``spec.type`` from ``ClusterIP`` to ``NodePort``. 
This can be done with ``oc patch``.

.. code-block:: text

   oc patch service my-service -p '{"spec": {"type": "NodePort"}}'

Then, you can run ``oc describe service my-service`` again to see if your change has been made.

.. code-block:: text

   $ oc describe services my-service
   Name:                     my-service
   Namespace:                my-project
   Labels:                   <none>
   Annotations:              <none>
   Selector:                 name=my-app
   Type:                     NodePort
   IP:                       172.25.170.246
   Port:                     <unset>  8080/TCP
   TargetPort:               8080/TCP
   NodePort:                 <unset>  30298/TCP
   Endpoints:                <none>
   Session Affinity:         None
   External Traffic Policy:  Cluster
   Events:                   <none>

Note that a ``NodePort`` value will automatically be given by the service controller.

Your service can then be accessed by the scheme ``apps.{cluster}.ccs.ornl.gov:{nodePort}``.

In this example, if the service was running on marble, I could access it with ``apps.marble.ccs.ornl.gov:30298``

