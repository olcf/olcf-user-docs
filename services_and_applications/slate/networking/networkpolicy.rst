.. _slate_network_policies:

****************
Network Policies
****************

Network policies are specifications of how groups of pods are allowed to communicate with each other and other network endpoints. A pod is selected in a Network Policy based on a label so the Network Policy can define rules to specify traffic to that pod.

Isolation Explanation
---------------------

When you create a namespace in Slate with the Quota Dashboard some Network Policies are added to your newly created namespace. This means that pods inside your project are isolated from connections not defined in these Network Policies.

Network Policies do not conflict, they are additive. This means that if two policies match a pod the pod will be restricted to what is allowed by the union of those policies' ingress/egress rules.

Creating a Network Policy
-------------------------

In the GUI
^^^^^^^^^^

To create a Network policy using the GUI, click the **Networking** tab followed by the **Network Policy** tab:


.. image:: /images/slate/NetworkPolicy.png
   :alt: Creating Network Policies


This will place you in an editor with some boiler plate YAML. From here, you can define the network policy that you need for your namespace. Below is an example Network Policy that you would use to allow all external traffic to access a nodePort in your namespace. 

.. code-block:: yaml

   kind: NetworkPolicy
   apiVersion: networking.k8s.io/v1
   metadata:
     name: web-allow-external
   spec:
     podSelector:
       matchLabels:
         key: value
     ingress:
       - {}
     policyTypes:
       - Ingress

A blank field matches all. The above example matches on all from/port combinations. Similarly, a blank pod selector would match on all pods in the namespace. 

.. note::

  The key value pair, or label, under **spec.podSelector.matchLabels** must match exactly to the labels of the pod in your namespace that 
  the policy is intended for. For example, the above NetworkPolicy would match pods with these labels set:

  .. code-block:: yaml

    apiVersion: v1
    Kind: Pod
    metadata:
      labels:
        key: value
    ...

Using the CLI
^^^^^^^^^^^^^

To view the Network policies in your namespace you can run:

.. code-block:: bash

   oc get networkpolicy -n YOUR_NAMESPACE

To get the name of the network policy and then view object's YAML:

.. code-block:: bash

   oc get networkpolicy NETWORKPOLICY_NAME -o yaml

To create a Network Policy, define one in YAML similar to the output of the previous command and run:

.. code-block:: bash

   oc create -f FILENAME

For a more complex example of a Network Policy, please see the `Kubernetes doc. <https://kubernetes.io/docs/concepts/services-networking/network-policies/#networkpolicy-resource>`_

A full reference of Network Policies can `be found here. <https://kubernetes.io/docs/concepts/services-networking/network-policies/>`_
