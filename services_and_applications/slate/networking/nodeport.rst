.. _slate_nodeports:

*********
NodePorts
*********


A NodePort reserves a port across all nodes of the cluster. This port routes traffic
to a service, which points to the pods that match the service's label selector.

NodePorts are given in the 30000-32767 range. These are ports you can use from
outside the cluster to access resources inside of OpenShift.

For the Openshift clusters you will additionally need to `create a network policy <../networkpolicy>`_ file to allow external traffic into your namespace. 

.. image:: /images/slate/NodePort.png
   :target: /images/slate/NodePort.png
   :alt: Exposing service with NodePorts


Configuring a Service NodePort
------------------------------

CLI
^^^

For example, let's look at a mongo service (called ``mongodb``\ ) that has been created inside of the project ``my-project``.

Switch to the project with ``oc project my-project``.

If you run ``oc get services``\ , you should see your service in the list.


.. code-block:: text

   $ oc get services
   NAME                  CLUSTER-IP       EXTERNAL-IP   PORT(S)                                       AGE
   mongodb               172.31.86.69     <none>        27017/TCP                                     1d

Then, get some information about the service with ``oc describe service mongodb``.

.. code-block:: text

   $ oc describe service mongodb
   Name:                   mongodb
   Namespace:              rogersjn3-test
   Labels:                 app=mongodb-ephemeral
                           template=mongodb-ephemeral-template
   Annotations:            template.openshift.io/expose-uri=mongodb://{.spec.clusterIP}:{.spec.ports[?(.name=="mongo")].port}
   Selector:               name=mongodb
   Type:                   ClusterIP
   IP:                     172.31.86.69
   Port:                   mongo   27017/TCP
   Endpoints:              10.132.0.225:27017
   Session Affinity:       None
   Events:                 <none>

Note the ``Type`` under the service is ``ClusterIP``. This is the default value for services, but we want to expose
it with a NodePort.

In order to expose the service with a NodePort, we need to change ``spec.type`` from ``ClusterIP`` to ``NodePort``. 
This can be done with ``oc patch``.

.. code-block:: text

   oc patch service mongodb -p '{"spec": {"type": "NodePort"}}'

Then, you can run ``oc describe service mongodb`` again to see if your change has been made.

.. code-block:: text

   Name:                   mongodb
   Namespace:              rogersjn3-test
   Labels:                 app=mongodb-ephemeral
                           template=mongodb-ephemeral-template
   Annotations:            template.openshift.io/expose-uri=mongodb://{.spec.clusterIP}:{.spec.ports[?(.name=="mongo")].port}
   Selector:               name=mongodb
   Type:                   NodePort
   IP:                     172.31.86.69
   Port:                   mongo   27017/TCP
   NodePort:               mongo   32399/TCP
   Endpoints:              10.132.0.225:27017
   Session Affinity:       None
   Events:                 <none>

Note that a ``NodePort`` value will automatically be given by the service controller.

Your service can then be accessed by the scheme ``{project}.{cluster}.ccs.ornl.gov:{nodePort}``.

In this example, if the service was running on marble, I could access it with ``my-project.marble.ccs.ornl.gov:32399``
