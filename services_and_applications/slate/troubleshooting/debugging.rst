---------
Debugging
---------

Debug a pod in CrashLoopBackoff
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If we have a pod that is crash looping then it is exiting too quickly to spawn a shell inside the container. We can use ``oc debug`` to start a pod with that same image but instead of the image entrypoint we use /bin/sh instead.

.. code-block:: text

   $ oc debug misbehaving-pod-1
   Defaulting container name to bad.
   Use 'oc describe pod/misbehaving-pod-1' to see all of the containers in this pod.

   Debugging with pod/misbehaving-pod-1, original command: <image entrypoint>
   Waiting for pod to start ...
   If you don't see a command prompt, try pressing enter.
   / $

Get a shell inside a pod
^^^^^^^^^^^^^^^^^^^^^^^^

What if we want to get a shell inside of the container to debug?

.. code-block:: text

   oc run centos-debug-test --restart=Never --image=centos -- /usr/bin/sleep 1d

Let's make sure it successfully gets scheduled and started, look for ``Status: Running``

.. code-block:: text

   oc describe pod centos-debug-test

Now we have a running pod, let's check it out:

.. code-block:: text

   oc exec -it centos-debug-test /bin/bash

Now let's delete the pod:

.. code-block:: text

   oc delete pod centos-debug-test
