.. _minio_example:

******************************************
MinIO Object Store (On an NCCS Filesystem)
******************************************

`MinIO <https://min.io/>`_ is a high-performance software-defined object
storage suite that enables the ability to easily deploy cloud-native data
infrastructure for various data workloads. In this example, we are deploying a
simple, standalone implementation of MinIO on our cloud-native platform, Slate
(:ref:`slate_overview`).

This service will only be accessible from inside of ORNL's network.

If your project requires an externally facing service available to the
Internet, please contact `User Assistance
<https://www.olcf.ornl.gov/for-users/>`_ by submitting a help ticket. There is
a process to get such approval.

We hope this provides a starting point for more robust implementations of
MinIO, if your workload/project benefits from that. In addition, it gives
insight into some of the core building blocks for establishing your own,
different, applications on Slate.

This example deployment of MinIO enables two possible configurations (which we
configure in the following sections):

 - MinIO running on a NCCS filesystem (GPFS or NFS - exposing filesystem project
   space through the MinIO GUI).
 - MinIO running on a dedicated volume, allocated automatically from the NetApp
   storage server, isolated to the MinIO server.

It is important to note that we are also launching MinIO in standalone mode,
which is a single MinIO server instance. MinIO also supports distributed mode
for more robust implementations, but we are not setting that up in this
example.

For this example to work, it is **required to have a project "automation user"**
setup for the NCCS filesystem integration. Please contact `User Assistance
<https://www.olcf.ornl.gov/for-users/>`_ by submitting a help ticket if you
are unsure about the automation user setup for your project.

This is not meant to be a production deployment, but a way for users to gain
familiarity with building an application targeting Slate.

Getting Started
---------------

It is assumed you have already gone through :ref:`slate_getting_started` and
established the :ref:`helm_prerequisite`. Please do that before attempting to
deploy anything on Slate's clusters.

This example uses Helm version 3 to deploy a MinIO standalone Helm chart on
Slate's `Marble <https://console-openshift-console.apps.marble.ccs.ornl.gov/>`_
Cluster. This is the cluster in OLCF's Moderate enclave, the same enclave as
Frontier.

To start, clone the `slate helm examples repository
<https://code.ornl.gov/ryu/slate_helm_examples>`_ , containing the MinIO
standalone Helm chart, and navigate into the ``charts`` directory:

.. code-block:: bash

    $ git clone https://code.ornl.gov/ryu/slate_helm_examples.git && cd slate_helm_examples/charts

If you are interested in the details of this Helm chart, please look at the
minio-standalone chart's `README
<https://code.ornl.gov/ryu/slate_helm_examples/-/blob/master/charts/minio-standalone/README.md>`_.

Next, log into Marble with the ``oc`` CLI tool by running this command on your
local machine:

.. code-block:: bash

   $ oc login https://api.marble.ccs.ornl.gov --username=loginName

where the loginName is your username for the cluster. You should see output confirming your login. It will also name your available
project spaces on Marble.

To list your available project spaces run this command:

.. code-block:: bash

   $ oc projects

Finally, confirm Helm works by running this command on your local machine:

.. code-block:: bash

   $ helm ls

You should get some output similar to this (although, you may not have any applications listed, if you have not deployed any):

.. code-block:: bash

  NAME                            	NAMESPACE	REVISION	UPDATED                             	STATUS  	CHART                 	APP VERSION
  gitlab-runner-for-slate-examples	stf007   	9       	2020-05-18 11:31:08.3245 -0400 EDT  	deployed	gitlab-runner-0.16.1  	12.10.2    
  rprout-minio-standalone         	stf007   	1       	2020-05-20 10:52:34.353245 -0400 EDT	deployed	minio-standalone-1.0.0

Configure Your Deployment
-------------------------

Where you cloned the `slate_helm_examples
<https://code.ornl.gov/ryu/slate_helm_examples>`_ repository, in the
'slate_helm_examples/charts/minio-standalone` directory, you will see a
`values.yaml` file. This file containes variables for the Helm chart
deployment. 

This is how we configure your instance of the MinIO application. All of these
changes will be to your local copy of `values.yaml`.

Here is what it looks like:

.. code-block:: bash

  # This can be used to provide variables to your chart. 
  # Below are the current configurable variables.
  minio:
    resources:
      requests:
        cpu: 2
        memory: 1Gi
      limits:
        cpu: 2
        memory: 1Gi
    # Change this to reflect <your_uid>, this must be unique: <your_uid>-minio-standalone.apps.marble.ccs.ornl.gov
    host: rprout-minio-standalone.apps.marble.ccs.ornl.gov
    # Change this to create unique app name
    name: rprout-minio-standalone
    # Set this to "disbled" to not use OLCF fileystem. If "disabled" it will use a volume isolated to the MinIO Pod.
    use_olcf_fs: enabled
    # This is the OLCF file system path MinIO will server out of, if "enabled" above.
    olcf_mount: /ccs/proj/stf007/minio-test
    # Amount of storage to use, if use_olcf_fs is "disabled"
    pvc_storage: 3Gi
    # Change this to reflect <your-project-namespace>, this will be the output of the `oc project` command.
    network_policy_namespace: <your-project-namespace>

What do you need to consider?

- What should I name my ``host`` value? (This will be the URL in which you access
  your MinIO instance)
- What should I name my application? (This is the ``name`` value and should be
  unique to you or your project)
- Do I want MinIO to run on an OLCF filesytem? (It can run on NFS or GPFS
  project spaces. If you do not run it on an OLCF filesystem it uses an
  isolated volume dedicated to the MinIO server)

What do you need to configure?

- ``host`` (Set the URL of your application)
- ``name`` (Set the name of your application)
- ``use_olcf_fs`` (Controls if NCCS filesystems are used or not - ``enabled`` or ``disabled``)
- ``olcf_mount`` (Set the mount path to your project directory (i.e., ``/ccs/proj/<projectID>/minio/``))
- ``pvc_storage`` (Set the quota for your dedicated storage if ``use_olcf_fs`` is ``disabled``)
- ``network_policy_namespace`` (Set the network policy's namespace to your project name, this will be the output of the ``oc project`` command)


Create the MinIO Application's Secret Tokens
--------------------------------------------

The below is not provided in the above configuration, but it must be done for
the MinIO application to start properly.

These are the root credentials referenced `here
<https://docs.min.io/docs/minio-server-configuration-guide.html>`_.

To establish these credentials in our Marble project, allowing our MinIO
deployment to use them, we need to create a ``secret-token.yaml`` file and
apply it to our project.

Create this example ``secret-token.yaml`` file locally:

.. code-block:: bash

    apiVersion: v1
    kind: List
    metadata: {}
    items:
    - apiVersion: v1
      kind: Secret
      metadata:
        # The <name-of-your-app> piece can be found in the values.yaml file at 'minio.name'. You can set the name of your app.
        # Keep the "-access-key" part appended to the name.
        name: <name-of-your-app>-access-key
      stringData:
        SECRET_TOKEN: <your_choice>
    - apiVersion: v1
      kind: Secret
      metadata:
        # Keep the '-secret-key' part appended to the name.
        # Note: <your_choice> below must be a string
        # Ex: SECRET_TOKEN: "your_choice_string"
        name: <name-of-your-app>-secret-key
      stringData:
        SECRET_TOKEN: <your_choice>

Replace ``<name-of-your-app>`` with the ``name`` value you put in your
``values.yaml`` file.

Replace ``<your-choice>`` with strings of your choice (the access-key length
should be at least 3, and the secret-key must be at least 8 characters). These
will be the ``SECRET_TOKEN`` values.

Once your ``secret-token.yaml`` file is set, you can apply it to your Marble
project/namespace with this command (assumes you are logged into Marble's CLI):

.. code-block:: bash

  $ oc apply -f secret-token.yaml

You should get output similar to this:

.. code-block:: bash

  secret "rprout-test-minio-access-key" created
  secret "rprout-test-minio-secret-key" created

These values are picked up as environment variables from the
``templates/minio-standalone-deployment.yaml`` file.

It is recommended to keep the ``secret-token.yaml`` file safe, locally, and not
in a repository if unencrypted. 

Installing the MinIO Standalone Application
-------------------------------------------

At this point we are ready to install our minio-standalone chart in our Marble
project namespace.

To list your available project spaces run this command:

.. code-block:: bash

   $ oc projects

Check list:

- You have the ``oc`` CLI Tool.
- You have Helm version 3.
- You are logged into Marble, with the ``oc`` CLI Tool, and in the correct Marble project.
- You have configured your ``values.yaml`` file.
- You have created your MinIO Application's Secret Tokens and applied them to the Marble project you are logged into.
- You are in the ``slate_helm_examples/charts`` directory, within your local copy of the `slate helm examples repository <https://code.ornl.gov/ryu/slate_helm_examples>`_.

If you checked the above off, you can install the MinIO chart, into your Marble project, with this command:

.. code-block:: bash

  $ helm install <your application name> minio-standalone/ --namespace <your marble project namespace>

Replace ``<your application name>`` with the ``name`` value in your
``values.yaml`` file.

Replace ``<your marble project>`` with your proper Marble project space. This
is from the output of the ``oc projects`` command.

The output, if successful, should be something similar to this:

.. code-block:: bash

  NAME: rprout-minio-standalone
  LAST DEPLOYED: Wed May 20 10:35:43 2020
  NAMESPACE: stf007
  STATUS: deployed
  REVISION: 1
  TEST SUITE: None

This is also a good time to log into the `Marble GUI
<https://console-openshift-console.apps.marble.ccs.ornl.gov/>`_. You can see
the Pod/Deployment/Route/Service/Secrets we created with the chart.

Paths to each in the GUI panel:

- Workloads->Pods
- Workloads->Deployments
- Workloads->Secrets
- Networking->Services
- Networking->Routes
- Storage->Persistent Volume Claims (only applicable if you disabled
  ``use_olcf_fs`` in ``values.yaml``)

Use the MinIO Standalone Application
------------------------------------

After a few minutes, the URL to your MinIO server will become available. 

You can reach it by going to the URL you put for the ``host`` value in your
``values.yaml`` file.

You can also go to it by logging into the `Marble GUI
<https://console-openshift-console.apps.marble.ccs.ornl.gov/>`_. Once logged
in, go to Networking->Routes and click the URL in the "Location" column of your
MinIO applications row.

You will be greeted with the NCCS SSO page. Continue through that with your
normal NCCS login credentials. 

After the NCCS login, you will be greeted with MinIO's login page. Here you
will enter the access-key and secret-key you created with the
``secret-token.yaml`` file.

At this point, you should be inside the MinIO Browser.

Depending on you how configured your deployment, this could be your NFS or GPFS
project space or an isolated volume dedicated/isolated to this MinIO server.

Within the GUI you can create buckets and upload/download data. If you are
running this on NFS or GPFS the bucket will map to a directory.

.. note::
  This application runs as the **automation user** ID, setup for your
  project. Anyone who logs into the MinIO app, runs as that user. If you are
  integrated with an NCCS filesystem, any file uploaded through MinIO will be
  owned by that user. If you plan to run something like this for your OLCF
  project, it is recommended to create a directory in the ``$PROJWORK``
  space.

Deleting the MinIO Standalone Application
-----------------------------------------

To delete this installation, just run this Helm command:

.. code-block:: bash

  $ helm delete <your-application-name>

You can get your deployed applications with this Helm command:

.. code-block:: bash

  $ helm ls
