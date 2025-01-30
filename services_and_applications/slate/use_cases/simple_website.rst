

-------------------------------
Build and Deploy Simple Website
-------------------------------

OpenShift has an integrated container image build service that users interact with through BuildConfig objects. BuildConfig's are very powerful, builds can be triggered by git repo or image tag pushes and connected into a pipeline to do automated deployments of newly built images. While powerful, these 
mechanisms can be cumbersome when starting out so we will be using a BuildConfig in a slightly simpler setup.

Creating the BuildConfig
^^^^^^^^^^^^^^^^^^^^^^^^

We will create a BuildConfig that will take a Binary (Local) source which will stream the contents of our local filesystem to the builder.

First, we will log into the cluster using the ``oc`` CLI tool

.. code-block:: text

   oc login https://api.<cluster>.ccs.ornl.gov

Next, we will create the ImageStream that the BuildConfig will push the completed image to. The ImageStream is a direct mapping to the image stored in the OpenShift integrated registry.

.. code-block:: text

   oc create imagestream local-image

Next, we will create the BuildConfig object

.. code-block:: yaml

   apiVersion: "build.openshift.io/v1"
   kind: "BuildConfig"
   metadata:
     name: "local-image"
   spec:
     output:
       to:
         kind: "ImageStreamTag"
         name: "local-image:latest"
     source:
       type: Binary
     strategy:
       type: dockerStrategy
       dockerStrategy: {}

Create a file with the above contents and instantiate the objects in Kubernetes

.. code-block:: text

   oc apply -f buildconfig.yaml

Create the Image
^^^^^^^^^^^^^^^^

We will create the directory along with our files:


* **Dockerfile** Describes our docker build
* **httpd.conf** Apache HTTPd does not work out of the box as non-root so we modify the default configuration file
* **index.html** Simple index.html page we will serve

.. code-block:: bash

   mkdir local-image
   cd local-image

   cat <<EOF > index.html
   Hello World!
   EOF

   cat <<EOF > httpd.conf
   ServerRoot "/etc/httpd"

   # Minimum modules needed
   LoadModule mpm_event_module modules/mod_mpm_event.so
   LoadModule log_config_module modules/mod_log_config.so
   LoadModule mime_module modules/mod_mime.so
   LoadModule dir_module modules/mod_dir.so
   LoadModule authz_core_module modules/mod_authz_core.so
   LoadModule unixd_module modules/mod_unixd.so

   TypesConfig /etc/mime.types

   PidFile /tmp/httpd.pid

   # Port to Listen on
   Listen *:8080

   DocumentRoot "/var/www/html"

   # Default file to serve
   DirectoryIndex index.html

   # Errors go to their own log
   ErrorLog /dev/stderr

   # Access log
   LogFormat "%h %l %u %t \"%r\" %>s %b" common
   CustomLog /dev/stdout common

   # Never change this block
   <Directory />
     AllowOverride None
     Require all denied
   </Directory>

   # Allow documents to be served from the DocumentRoot
   <Directory "/var/www/html">
       Options Indexes FollowSymLinks
       AllowOverride None
       Require all granted
   </Directory>
   EOF

   cat <<EOF > Dockerfile
   FROM rockylinux:latest
   RUN yum -y update
   RUN yum -y install httpd
   ADD index.html /var/www/html
   ADD httpd.conf /etc/httpd/conf/httpd.conf
   CMD ["/usr/sbin/httpd", "-DFOREGROUND"]
   EOF

Now let's create a Build from the BuildConfig and upload our current directory as the source for the build.

.. code-block:: text

   $ oc start-build local-image --from-dir=. --follow
   Uploading directory "." as binary input for the build ...
   ...
   Successfully built fe3e487fffe5
   Pushing image image-registry.openshift-image-registry.svc:5000/stf002platform/local-image:latest ...
   Push successful

Once that is complete, we can see that the image was uploaded to the integrated registry by getting the ImageStream object

.. code-block:: text

   $ oc get imagestream local-image
   NAME          DOCKER REPO                                                   TAGS     UPDATED
   local-image   image-registry.openshift-image-registry.svc:5000/stf002platform/local-image   latest   5 minutes ago

Deploy the Image
^^^^^^^^^^^^^^^^

Now that we have built a container image, we can deploy it with a Deployment object. Using the Docker Repo specified in the ImageStream we can create our deployment:

.. code-block:: yaml

   apiVersion: apps/v1
   kind: Deployment
   metadata:
     creationTimestamp: null
     labels:
       app: local-image
     name: local-image
   spec:
     replicas: 1
     selector:
       matchLabels:
         app: local-image
     strategy: {}
     template:
       metadata:
         creationTimestamp: null
         labels:
           app: local-image
       spec:
         containers:
         - image: "image-registry.openshift-image-registry.svc:5000/stf002platform/local-image:latest"
           imagePullPolicy: Always
           name: local-image
           resources: {}
   status: {}

Create a file with the above contents and instantiate the objects in Kubernetes

.. code-block:: text

   oc apply -f deployment.yaml

.. note:: 
   Snippet created with ``oc create deployment local-image --image image-registry.openshift-image-registry.svc:5000/stf002platform/local-image --dry-run -o yaml``

Now, once the Deployment controller creates a pod, we should be able to do a port forward and test that our web server is serving our index.html file

.. code-block:: text

   $ oc describe deployment local-image
   ...
   $ oc get pods -l app=local-image
   ...
   $ oc port-forward deployment/local-image 8080:8080
   Forwarding from [::1]:8080 -> 8080
   Forwarding from 127.0.0.1:8080 -> 8080

Since this is running the foreground, in a second terminal use ``curl`` to run the test:

.. code-block:: text
   
   $ curl localhost:8080
   Hello World!

or one could also use you web browser to verify the content.

Next Steps
^^^^^^^^^^

Can you modify the **index.html** page to display "Hello from (your name)"?

.. raw:: html

  <details>
  <summary><a>Stuck?</a></summary>

Modify **index.html** in your current directory

Start a new image build: oc start-build local-image --from-dir=. --follow

Get a list of pods running in your namespace: oc get pods

Delete the currently running pod: oc delete pod local-image-...

Alternative to deleting the pod, update the Deployment to trigger a new rollout: ``oc patch deployment local-image -p '{"spec":{"template":{"metadata":{"labels":{"date":"'`date +'%s'`'"}}}}}'``

.. raw:: html

  </details>



Teardown
^^^^^^^^

Once we are finished testing, we can delete everything

.. code-block:: text

   oc delete deployment local-image
   oc delete buildconfig local-image
   oc delete imagestream local-image
