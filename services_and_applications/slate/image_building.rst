.. _slate_image_building:

**************
Image Building
**************

Building an image in Openshift is the act of transferring a set of input parameters into an object. That object is 
typically an image. Openshift contains all of the necessary components to build a Docker image or a piece of source
code an image that will run in a container.

Build Types
-----------

Docker
^^^^^^

A Docker build is achieved by linking to a source repository that contains a docker image and all of the necessary
Docker artifacts. A build is then triggered through the standard ``$ docker build`` command. More specific documentation
on docker builds `can be found here <https://docs.docker.com/engine/reference/commandline/build/>`_.

S2I
^^^

Source to image (S2I) is a tool to build docker formatted container images. This is accomplished by injecting source code
into a container image and then building a new image. The new image will contain the source code ready to run,
via the ``$ docker run`` command inside the newly built image. 

Examples
--------

Building From Git Repository in GUI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using the S2I model of building images, it is possible to have your source hosted on a git repository and then pulled and
built by Openshift.


#. 
   Click on the newly created project and then on the blue **Add to Project** button on the center of the page.

#. 
   Here you will have the option to select from a number of container images. Select the one that matches the source code in the git repository that you will be using. In this example we'll be using Python.

#. 
   Using the drop down menu select the version of the language that your source is written in and click **Select**.

#. 
   Then input the repo that contains the repository you wish to use.

#. 
   Openshift will automatically pull and build your source. If you make a change and need an updated build simply navigate to the **build** option on the menu to the left and select your project and click **Start Build** in the upper right.

Creating a BuildConfig from the CLI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The first step to creating the the build is to create a build config. This is done in one of three ways depending on
how your code is structured. If you have a git repository already configured and it is public then the command

.. code-block::

   oc new-build .

will create your build config from that repository. 

If you have a public git repository that isn't already configured then you can create the build config by running

.. code-block::

   oc new-build <URL TO YOUR GIT REPOSITORY>

If you have a private git repository then your build config will be created by running the command:

.. code-block::
   
   $ oc new-build <URL TO YOUR GIT REPOSITORY> --source-secret=yoursecret

Follows is an example of creating a build for a public git repository:

.. code-block::

   $ oc new-build https://github.com/sclorg/django-ex
   --> Found image 1ce91f1 (7 months old) in image stream "openshift/python" under tag "3.5" for "python"

       Python 3.5
       ----------
       Python 3.5 available as docker container is a base platform for building and running various Python
       3.5 applications and frameworks. Python is an easy to learn, powerful programming language. It has
       efficient high-level data structures and a simple but effective approach to object-oriented
       programming. Python's elegant syntax and dynamic typing, together with its interpreted nature, make
       it an ideal language for scripting and rapid application development in many areas on most
       platforms.

       Tags: builder, python, python35, rh-python35

       * The source repository appears to match: python
       * A source build using source code from https://github.com/sclorg/django-ex will be created
         * The resulting image will be pushed to image stream "django-ex:latest"
         * Use 'start-build' to trigger a new build

   --> Creating resources with label build=django-ex ...
       imagestream "django-ex" created
       buildconfig "django-ex" created
   --> Success
       Build configuration "django-ex" created and build triggered.
       Run 'oc logs -f bc/django-ex' to stream the build progress.

What happens is that ``oc`` pulls in the provided repository, in this example Django, and automatically configures
everything needed to build the image. You should now be able to go to the Openshift web GUI and under the **builds**
tab see your newly built build. 

Now, since everything has been configured, you can click the **Start Build** button in the upper right hand side of the
Web GUI anytime that you need to make another build. You can also start a another build from the command line with
either:

.. code-block:: 

   oc start-build <buildconfig_name>

Or, if you would like to receive logs from the build:

.. code-block:: 

   oc start-build <buildconfig_name> --follow

.. note::
  It is perfectly normal for a build to take a few minutes to complete.

Using A Dockerfile
^^^^^^^^^^^^^^^^^^

Using a Dockerfile inside of Openshift works in the same way that ``$ docker build``  works outside of Openshift. If
all that is needed for your build is a Dockerfile. From within the directory containing the Dockerfile you can run:

.. code-block:: bash

   $ oc new-build . --name example
   --> Found image 224765a (3 months old) in image stream "buildexample/openjdk" under tag "8-alpine" for "openjdk:8-alpine"

       * A Docker build using binary input will be created
         * The resulting image will be pushed to image stream "example:latest"
         * A binary build was created, use 'start-build --from-dir' to trigger a new build

   --> Creating resources with label build=example ...
       imagestream "example" created
       buildconfig "example" created
   --> Success

That will create a new build config, from that build config you can then use your app by running the ``start-build`` command
with the name of the newly created build config.

.. code-block:: bash


   $ oc start-build example --from-file=./Dockerfile
     Uploading file "Dockerfile" as binary input for the build ...
     build "example-1" started

.. note::
  In the above example ``example`` was the name of the build config.

Additionally, if there are artifacts that need to be included in your build, a directory containing those artifacts can
be used by passing the ``--from-dir`` flag to the ``start-build`` command like so:

.. code-block:: bash


   $ oc start-build example --from-dir=./sampledir
     Uploading directory "sampledir" as binary input for the build ...
     build "django-5" started

Using a Local Image
^^^^^^^^^^^^^^^^^^^

There might be an image built locally that you would like to have in your OpenShift project. It is possible to add this 
image to your project by adding it to the Docker registry of the cluster that your project is on.

First, copy your login token. We will need this for the next step.

.. code-block:: 

   oc login https://api.<cluster>.ccs.ornl.gov --token=<COPY THIS TOKEN>

Next, log into the Docker registry. Use your copied token when prompted for your password. Upon succesful login, a message 
saying so will appear.

.. code-block:: 

   docker login -u <NCCS USERNAME> registry.apps.<cluster>.ccs.ornl.gov

Now, find the repository and tag information of the local image you want to add to the registry and tag it accordingly.

.. code-block:: bash

   $ docker images
   REPOSITORY                                TAG                 IMAGE ID            CREATED             SIZE
   example:5000/streams                      v3.1.4              fd7673fdbe30        3 weeks ago         1.95GB

The command to tag your image is:

.. code-block:: 

   docker tag example:5000/streams:v3.1.4 registry.apps.<cluster>.ccs.ornl.gov/<namespace>/<image>:<tag>

Lastly, the image needs to be pushed to the registry.

.. code-block:: 

   docker push registry.apps.<cluster>.ccs.ornl.gov/<namespace>/<image>:<tag>

OpenShift has an integrated container registry that can be accessed from outside the cluster to
push and pull images as well as run containers.

Logging into the Registry Externally
------------------------------------

.. note::
  This assumes that you have Docker installed locally. Installing Docker is outside of the scope of this documentation.

First you have to log into OpenShift

.. code-block:: text

   oc login https://api.<cluster>.ccs.ornl.gov --username=loginName

where the loginName is your username for the cluster. Next you can use your token to log into the integrated registry.

.. code-block:: text

   docker login -u user -p $(oc whoami -t) registry.apps.<cluster>.ccs.ornl.gov

Then you can push and pull from the integrated registry. In the following example we will pull
**busybox:latest** from Docker Hub and push it to our namespace in the integrate registry.

.. code-block:: text

   $ docker pull busybox:latest
   latest: Pulling from library/busybox
   ee153a04d683: Pull complete
   Digest: sha256:9f1003c480699be56815db0f8146ad2e22efea85129b5b5983d0e0fb52d9ab70
   Status: Downloaded newer image for busybox:latest
   docker.io/library/busybox:latest

   $ docker tag busybox:latest registry.apps.marble.ccs.ornl.gov/stf002platform/busybox:latest

   $ docker push registry.apps.marble.ccs.ornl.gov/stf002platform/busybox:latest
   The push refers to repository [registry.apps.marble.ccs.ornl.gov/stf002platform/busybox]
   0d315111b484: Pushed
   latest: digest: sha256:895ab622e92e18d6b461d671081757af7dbaa3b00e3e28e12505af7817f73649 size: 527

   $ oc get is busybox
   NAME      DOCKER REPO                                               TAGS     UPDATED
   busybox   image-registry.openshift-image-registry.svc:5000/stf002platform/busybox   latest   5 seconds ago

.. note::
  When tagging an image, you must use the format ``registry.apps.<cluster>.ccs.ornl.gov/<namespace>/<image>`` where:


* :term:`Cluster` is the name of the OpenShift cluster
* :term:`Namespace` is the name of the Kubernetes namespace you are using (Use ``oc status`` to see what
  OpenShift Project/Kubernetes Namespace you are currently in)
* :term:`Image` is the name of the image you want to push

Once you push the image into the registry, a OpenShift ImageStream will be automatically created
