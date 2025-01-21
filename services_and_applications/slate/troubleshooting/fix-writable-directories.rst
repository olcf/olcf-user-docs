

Fix Container Image Permissions
-------------------------------

Running containers as non-root can be challenging when consuming container images from an upstream source
such as the Docker Hub since many images are built with the intention of running as root. You may encounter
this issue if your container enters a **CrashLoopBackoff** state, check the logs for the container and if
there are "Permission Denied" issues then you may need to fix directory permissions in the image.

Mount an EmptyDir Volume
^^^^^^^^^^^^^^^^^^^^^^^^

If the application needs access to a temporary space for doing something like generating a configuration file on launch you
can mount a EmptyDir volume in the PodSpec which will ensure that whatever user the container is running as will have access
to write to that directory.

.. code-block:: yaml

   apiVersion: apps/v1
   kind: Deployment
   metadata:
     creationTimestamp: null
     labels:
       app: foo
     name: foo
   spec:
     replicas: 1
     selector:
       matchLabels:
         app: foo
     strategy: {}
     template:
       metadata:
         creationTimestamp: null
         labels:
           app: foo
       spec:
         containers:
         - image: busybox
           name: busybox
           resources: {}
           volumeMounts:
           - name: workdir
             mountPath: /data
         volumes:
         - name: workdir
           emptyDir: {}
   status: {}

.. note::
  Generated with ``oc create deployment foo --image busybox --dry-run -o yaml`` and then modified with volume mounts

Build a New Image
^^^^^^^^^^^^^^^^^

If you need to run a container in a project and mount NCCS home and project areas, then we will need to build a new container
and modify permissions to allow it to access the filesystem of the image.

We will use OpenShift to build a new image based on the upstream one and change owner of the directories that need to be
writable during container execution. Here is an example ``Dockerfile`` which derives from an upstream image and changes ownership
of directories to the user id (UID) that the container will run as in the cluster.

For example, if we are using the UID ``63114`` for our NCCS project user and we need to write to ``/opt/application-data`` during
the runtime of the container image, we could do this:

.. code-block:: Dockerfile

   FROM upstream-image:tag
   USER 0
   RUN chown -R 63114 /opt/application-data
   USER 63114

We will use this ``Dockerfile`` to generate a BuildConfig and then build a new image in our project that has the correct permissions.

.. code-block::

   cat Dockerfile | oc new-build --dockerfile=- --to=my-image:tag

The build should start automatically, monitor it with ``oc logs bc/my-image -f``.

Now that we have a new image with our /opt/application-data directory owned by the right user, we can either update an existing
deployment or create a new one with the image.

Note that in the following example, I am updating the Deployment and setting the image of the container named ``containername`` and
``--source=istag`` says I am using a ImageStream tag. The ImageStream in my OpenShift project stf002 is ``stf002/my-image:mytag``.

.. code-block::

   # Update an existing deployment called my-application
   oc set image deploy/my-application containername=stf002/my-image:mytag --source=istag

   # Create a new deployment with the container
   oc new-app -i my-image
