.. _helm_examle:

*************************
Deploy Packages with Helm
*************************

`Helm <https://helm.sh>`_ is the OLCF preferred package manager for Kubernetes. There are a variety of upstream
applications that can be installed with helm, such as databases, web frontends, and monitoring tools. Helm has "packages" called "charts", which can essentially be thought of as kubernetes object templates. You can pass in values which helm uses to fill in these templates, and create the objects (pods, deployments, services, etc)

Follow :ref:`helm_prerequisite` for installing Helm.

One nice feature of helm is that it uses the underlying authentication credentials to kubernetes, so once you login with
``oc login``\ , the helm client will authenticate automatically.

By default, helm doesn't have any chart repositories, so let's add the upstream ``stable`` repository.

.. code-block::

   helm repo add stable https://charts.helm.sh/stable

Now you can install helm charts with ``helm install stable/<package_name>``. You can think of this command as a parallel to running ``yum install`` on a RHEL/CentOS-based system, or ``apt install`` on a debian-based system.

Install MySQL with Helm
^^^^^^^^^^^^^^^^^^^^^^^

For an example, let's install a basic mysql database, with a release named ``mysql``.

Setting Values
~~~~~~~~~~~~~~

You could simply run ``helm install mysql stable/mysql``\ , and an basic mysql deployment would be created with default values. However, we probably want to customize this deployment a bit. Let's take a look at the `documentation for the mysql helm chart <https://github.com/helm/charts/tree/master/stable/mysql>`_.

Under the "Configuration" section, there is a large list of all the variables you can provide the chart, as well as their default values. Let's say we want to customize our mysql resource utilization as well as using a block volume instead of the default NFS volume for persistent storage. We'll also add a `NodePort service <https://docs.olcf.ornl.gov/services_and_applications/slate/networking/nodeport.html>`_ in order to access our new database from outside the cluster.

There are two ways to set values for ``helm install``\ :


#. Pass in individual values one-by-one with ``--set``.
#. Pass in a group of values within a file with ``--values``.

In this example, we'll be using the latter method. Let's create a file called ``values.yaml`` with the following values:

.. note::
  You may need to adjust the persistence > size value down depending on the storage quotas set for your project. Your project quotas can be found at ``https://quotas.CLUSTER.ccs.ornl.gov``, where CLUSTER is replaced with the cluster you are running on (Marble/Onyx).

.. code-block::

   persistence:
     size: 20Gi
     storageClass: "netapp-block"
   initContainer:
     resources:
       requests:
         cpu: 100m
         memory: 10Mi
       limits:
         cpu: 300m
         memory: 100Mi
   resources:
     requests:
       cpu: 2
       memory: 2Gi
     limits:
       cpu: 4
       memory:4Gi
   service:
     type: NodePort

Now mysql can be installed with these values by running ``helm install mysql stable/mysql --values values.yaml --namespace <project_name>``

.. note::
  It is possible to quickly install with ``--set`` instead of writing a values file if the default values are mostly adequate. For example, if only persistent storage size and storageClass need to be changed from the default values, this could be done by running ``helm install mysql stable/mysql --set persistence.size="20Gi" --set persistence.storageClass="netapp-block"``. Note that you can pass multiple values by passing ``--set`` multiple times.

After Installation
~~~~~~~~~~~~~~~~~~

To see all deployed helm charts in a namespace, along with their status, run ``helm list --namespace <project_name>``.
From the above example, this command will show the new mysql deployment, with ``mysql`` under ``NAME``.

You can run ``helm status <release_name> --namespace <project_name>`` in order to get information about the deployment. In this example, our release name is ``mysql``. Running this command for our ``mysql`` installation will give us information on how to connect and authenticate to our newly created database. 

The output of ``helm status`` will differ from chart to chart, as this output is customizable by the chart itself. If the output has ``kubectl`` commands to run, ``kubectl`` can be replaced with ``oc``.

Finding New Charts
^^^^^^^^^^^^^^^^^^

Running ``helm search hub`` will search `the Helm Hub <https://hub.helm.sh/>`_\ , which has a wide variety of publicly available charts. For example, if a wordpress installation is desired, you could run:

.. code-block::

   $ helm search hub wordpress
   URL                                                 CHART VERSION   APP VERSION DESCRIPTION
   https://hub.helm.sh/charts/bitnami/wordpress        7.6.7           5.2.4       Web publishing platform for building blogs and ...
   https://hub.helm.sh/charts/presslabs/wordpress-...  v0.6.3          v0.6.3      Presslabs WordPress Operator Helm Chart
   https://hub.helm.sh/charts/presslabs/wordpress-...  v0.7.1          v0.7.1

Note that this searches much more than the ``stable`` repo we added above, so you may need to add another repo with ``helm repo add``. Be sure to run ``helm repo update`` before installing new charts, to make sure the charts are up to date.

You can also search only the repos that you have added to your local client with ``helm search repo``.

Writing Charts
^^^^^^^^^^^^^^

It is also possible to write your own charts for helm, if you have an application that can be deployed to many namespaces or that could benefit from templating objects. How to write charts is outside the scope of this documentation, but the `upstream docs <https://helm.sh/docs/topics/charts/>`_ are a great place to start.
