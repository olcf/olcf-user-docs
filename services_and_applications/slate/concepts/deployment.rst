.. _slate_deployment_config:

---------------------------------
DeploymentConfigs and Deployments
---------------------------------

On top of Kubernetes ReplicationControllers, OpenShift gives us even more support for software
lifecycle with *DeploymentConfigs*. A DeploymentConfig creates a ReplicationController and has the added
benefit of controlling how new deployments get triggered and deployed.

*DeploymentConfig* comprise 3 objects:


* A *DeploymentConfig*
* One or more *ReplicationControllers*
* One or more pods

Creating a DeploymentConfig
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Below is an example DeploymentConfig:

.. code-block:: yaml

   apiVersion: v1
   kind: DeploymentConfig
   metadata:
     name: my-app
   spec:
     replicas: 5
     selector:
       name: my-app
     template: { ... }
     triggers:
       - type: ConfigChange
       imageChangeParams:
         automatic: true
         containerNames:
         - my-app
         from:
           kind: ImageStreamTag
           name: my-app:latest
       - type: ImageChange
     strategy:
       type: Rolling
     paused: false
     revisionHistoryLimit: 2
     minReadySeconds: 0

Let's look at the individual parts of this definition, under ``spec``.


* 
  ``replicas`` - the number of replicas to be passed down to the ReplicationController

* 
  ``selector`` - the selector to determine which pods are managed by the ReplicationController

* 
  ``template`` - a pod definition

* 
  ``triggers`` - see :ref:`slate_deployment_triggers`

* 
  ``strategy`` - see :ref:`slate_deployment_strategies`

* 
  ``paused`` - set this to ``true`` to pause a deployment config. This disables all triggers and can be used
  to make multiple changes to the pod template before rolling it out.

* 
  ``revisionHistoryLimit`` - the number of old revisions of ReplicationControllers to keep around.
  This can be used to have a rollback plan in case of a bad deployment.

* 
  ``minReadySeconds`` - number of seconds after the readiness check succeeds that the pod is considered
  "available". By default, this is 0 and may be omitted.

.. _slate_deployment_triggers:

Triggers
~~~~~~~~

Triggers are a method for automating the creation of new deployment processes in response to certain
events.

There are 2 types of triggers:


#. 
   ``ConfigChange``
   This trigger results in a new ReplicationController whenever the pod template in the deployment config changes.

#. 
   ``ImageChange``
   This trigger results in a new ReplicationController whenever the content of an image stream tag
   changes (or in other words, when a new version of the image is pushed). You can set the ``automatic``
   field to false to pause this trigger.


Creating Deployments
^^^^^^^^^^^^^^^^^^^^

Here is an example completed DeploymentConfig.

.. code-block:: yaml

   apiVersion: v1
   kind: DeploymentConfig
   metadata:
     name: recreate-example
   spec:
     replicas: 2
     selector:
       deploymentconfig: recreate-example
     strategy:
       # We set the type of strategy to Recreate, which means that it will be scaled down prior to being scaled up
       type: Recreate
     template:
       metadata:
         labels:
           deploymentconfig: recreate-example
       spec:
         containers:
         - image: openshift/deployment-example:v1
           name: deployment-example
           ports:
           - containerPort: 8080
             protocol: TCP
       triggers:
       - type: ConfigChange
       - imageChangeParams:
           automatic: true
           containerNames:
           - deployment-example
           from:
             kind: ImageStreamTag
             name: recreate-example:latest
         type: ImageChange

As with other objects in OpenShift, you can create this DeploymentConfig with ``oc create -f {FILE_NAME}``.

Once created, you can start a new deployment process with the command

.. code-block::

   oc rollout latest dc/{NAME}

This will begin a new deployment. To get basic information about the available revisions, run

.. code-block::

   oc rollout history dc/{NAME}

You can view a specific revision with

.. code-block::

   oc rollout history dc/{NAME} --revision=1

For more detailed information about a DeploymentConfig, use

.. code-block::

   oc describe dc {NAME}

To cancel a running deployment, run

.. code-block::

   oc deploy --cancel dc/{NAME}

.. note::
  Cancellation of a running deployment is a best-effort operation. The deployment may still
  complete before the cancellation comes into effect. The DeploymentConfig will be rolled back
  by scaling up the previous ReplicationController.

To roll back a deployment, run

.. code-block::

   oc rollout undo dc/{NAME}

Web Interface
^^^^^^^^^^^^^

When using the web interface, DeploymentConfigs should automatically get created when deploying a
new project, whether with S2I or from an image template. To edit a DeploymentConfig, from the
sidebar, go to ``Applications``\ , then ``Deployments``.


.. image:: /images/slate/DeploymentMenu.png
   :target: /images/slate/DeploymentMenu.png
   :alt: Deployment Menu


Select your DeploymentConfig out of the list, and go to the ``Configure`` tab (in this case, I
have a mongodb DeploymentConfig)


.. image:: /images/slate/deployConfig.png
   :target: /images/slate/deployConfig.png
   :alt: Deployment Config


To edit this configuration, click ``Actions`` in the upper right hand corner, then ``Edit``.


.. image:: /images/slate/editDeploy.png
   :target: /images/slate/editDeploy.png
   :alt: Edit Deployment Config


On this page, you can set the strategy type and parameters. You can also edit the YAML configurations
directly by clicking the ``Actions`` button and then ``Edit YAML``.


.. image:: /images/slate/editDeployYAML.png
   :target: /images/slate/editDeployYAML.png
   :alt: Edit Deployment YAML


.. _slate_deployment_strategies:

Deployment Strategies 
^^^^^^^^^^^^^^^^^^^^^

A *deployment strategy* is a method for upgrading an application. The goal of deployment strategies is
to make an update with no downtime to the end users.

The two most common values here will be ``Rolling`` and ``Recreate``. The default is ``Rolling``.

Since the end user usually will be accessing an application with a `route <../../networking/routes.md>`_\ , the
deployment strategy can focus on deployment configuration features. Here are a few examples of the
deployment configuration based strategies.

.. note::
  All of the below strategies use readiness checks to determine if a new pod is ready for use. If
  any readiness check fails, the deployment configuration will continue to try to run the pod until it
  times out. The default timeout is ``10m``. This value can be set in ``dc.spec.strategy.params.TimeoutSeconds``

The default strategy, if omitted, is ``Rolling``

Rolling Strategy
~~~~~~~~~~~~~~~~

A rolling deployment slowly replaces instances of the previous version with instances of the new
version. This deployment waits for new pods to become ready before scaling down the old replication
controller. This strategy is easily aborted and reverted.

A rolling deployment is best used when you want to take no downtime during an update, but you know your
application can support having old and new code running at the same time.

Here is an example Rolling deployment:

.. code-block:: yaml

   strategy:
     type: Rolling
     rollingParams:
       updatePeriodSeconds: 1
       intervalSeconds: 1
       timeoutSeconds: 120
       maxSurge: "20%"
       maxUnavailable: "10%"
       pre: {}
       post: {}

Let's take a look at the ``rollingParams``\ :


* 
  ``updatePeriodSeconds`` - The time to wait between pod updates. The default is ``1``.

* 
  ``intervalSeconds`` - The time to wait between getting the deployment status. The default is ``1``.

* 
  ``timeoutSeconds`` - The time to wait before automatically rolling back to the previous deployment.
  The default is ``600``

* 
  ``maxSurge`` and ``maxUnavailable`` - ``maxUnavailable`` is the maximum number of pods that can be unavailable
  during the update. ``maxSurge`` is the number of pods that can be scheduled above the original number
  of pods. Both values can be set to either a percentage (\ ``20%``\ ) or a positive integer (\ ``2``\ ). The default
  value for both is ``25%``.

  These values can be used to tune a deployment for speed or availability. If you want to maintain full
  capacity, set ``maxUnavailable`` to 0. The ``maxSurge`` value can be used to speed up the scale up. Note
  that you still must stay below your project's pod quota.

* 
  ``pre`` and ``post`` are :ref:`slate_lifecycle_hooks`

A Rolling strategy follows this sequence:


#. Execute the ``pre`` lifecycle hook
#. Scale up the new replication controller based on ``maxSurge``.
#. Scale down the old replication controller based on ``maxUnavailable``.
#. Repeat the scaling until the new replication controller has the desired replica count and the old
   replication controller has 0.
#. Execute the ``post`` lifecycle hook

.. note::
  During the scale down, the strategy waits for pods to become "ready" to determine if scaling down
  more will affect availability. If the new pods don't become "ready", the deployment will eventually
  time out and revert to the old deployment.

Recreate Strategy
~~~~~~~~~~~~~~~~~

A recreate deployment scales the previous deployment down to 0 before starting the new deployment.
This is best used when a downtime is acceptable, and your application cannot handle having the old
and new versions running at the same time.

Here is an example recreate deployment:

.. code-block:: yaml

   strategy:
     type: Recreate
     recreateParams:
       pre: {}
       mid: {}
       post: {}

``pre``\ , ``mid``\ , and ``post`` are :ref:`slate_lifecycle_hooks`

The recreate strategy follows this sequence:


#. Execute the ``pre`` lifecycle hook
#. Scale down the old deployment to 0 replicas.
#. Execute the ``mid`` lifecycle hook
#. Scale up the new deployment to the number of desired replicas.
#. Execute the ``post`` lifecycle hook

Custom Strategy
~~~~~~~~~~~~~~~

Rolling and Recreate strategies do not cover every case, and some applications may require more in-depth
deployment strategies. OpenShift has provided us with a Custom Strategy, so that we can have full control
over a deployment if needed. Here is an example of a basic custom strategy:

.. code-block:: yaml

   strategy:
     type: Custom
     customParams:
       image: my-app/strategy
       command: [ "command", "arg1" ]
       environment:
         - name: ENV_1
           value: VALUE_1

In this example the image ``my-app/strategy`` provides the deployment behavior. The ``command``
array simply overrides the ``CMD`` directive from the image's ``Dockerfile`` (obviously, you can leave this
out to run the Dockerfile's ``CMD``\ ). The ``environment`` variables are added to the environment of the
strategy process.

.. note::
  The replica count of the new deployment will start at 0. It is the responsibility of the strategy
  image to make the new deployment active.

See the `OpenShift page on Advanced Deployment Strategies <https://docs.openshift.org/latest/dev_guide/deployments/advanced_deployment_strategies.html>`_
for more examples of the Custom strategy.

Custom Strategies with ``customParams``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Alternatively, you can leverage the existing deployment strategies and inject custom deployment logic.
This is done with the ``customParams`` parameter. With this, you can provide custom shell script logic.
Using this, you do not have to supply a custom deployer container image. Here is an example:

.. code-block:: yaml

   strategy:
     type: Rolling
     customParams:
       command:
       - /bin/sh
       - -c
       - |
         set -e
         openshift-deploy --until=50%
         echo Halfway there
         openshift-deploy
         echo Complete

This will result in the following:

.. code-block::

   Started deployment #2
   --> Scaling up custom-deployment-2 from 0 to 2, scaling down custom-deployment-1 from 2 to 0 (keep 2 pods available, don't exceed 3 pods)
       Scaling custom-deployment-2 up to 1
   --> Reached 50% (currently 50%)
   Halfway there
   --> Scaling up custom-deployment-2 from 1 to 2, scaling down custom-deployment-1 from 2 to 0 (keep 2 pods available, don't exceed 3 pods)
       Scaling custom-deployment-1 down to 1
       Scaling custom-deployment-2 up to 2
       Scaling custom-deployment-1 down to 0
   --> Success
   Complete

.. _slate_lifecycle_hooks:

Lifecycle Hooks
^^^^^^^^^^^^^^^

*Lifecycle Hooks* allow behavior to be injected into the deployment process.

Both the Recreate and Rolling strategies support lifecycle hooks.

Lifecycle Hooks have 2 options:


#. ``failurePolicy`` - defines the action the strategy should take when a hook fails, can be one of
   ``Abort``\ , ``Retry``\ , or ``Ignore``.
#. ``execNewPod`` - the pod to execute, see the example below

Here is an example lifecycle hook:

.. code-block:: yaml

   pre:
     failurePolicy: Abort
     execNewPod:
       containerName: helloworld
       command: [ "/usr/bin/command", "arg1", "arg2" ]
       env:
         - name: CUSTOM_VAR1
           value: custom_value1
       volumes:
         - data

In the above example, the ``containerName`` refers to one of the container's in the
deployment's pod ``template``.

The ``command`` overrides the docker ``ENTRYPOINT`` for the image.

``env`` refers to environment variables to be sent to the container.

``volumes`` is an optional set of volume references for the container.

More Advanced Deployment Strategies with Routes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

While some strategies leverage features of DeploymentConfigs, others leverage features of
*routes*. If you haven't read the docs on :ref:`slate_services`
or :ref:`slate_routes`, read those first before trying these more advanced strategies.

Since routes are intended for HTTP and HTTPS traffic, these strategies are best used for web applications.

Blue-Green Deployment
~~~~~~~~~~~~~~~~~~~~~

*Blue-green deployments* are defined as running two versions of an application at the same time, then
moving traffic from the old production version (the green version) to the new production version (the
blue version). You could use a `Rolling Deployment Strategy <#rolling-strategy>`_ for this, but for the
sake of showing how route-based deployments work, we'll use a route.

.. note::
  ⚠️ WARNING: Blue-green deployment requires that your application can handle both old and new versions
  running at the same time. Be sure to think about your application and if it can handle this. For example, if the
  new version of the software changes how a certain field in a database is read and written, then the old
  version of the software won't be able to read the database changes, and your production instance could
  break. This is known as "N-1 compatibility" or "backward compatibility".


#. 
   Create two copies of your application, one for the old service (green) and one for the new (blue)

   .. code-block::

       oc new-app my-app:v1 --name=my-app-green
       oc new-app my-app:v2 --name=my-app-blue

#. 
   Create a route which points to the old service (this is assuming your application)

   .. code-block::

       oc create route edge --service=my-app-green --name=my-app

#. 
   Browse to your project at my-app.{PROJECT}.granite.ccs.ornl.gov and verify that the v1 version
    is displayed.

#. 
   Edit the route and change the service name to ``my-app-blue``

   .. code-block::

       oc patch route/my-app -p '{"spec":{"to":{"name":"my-app-blue"}}}'

#. 
   Verify the change has taken effect by refreshing your browser until you see the new version.

A/B Deployment
~~~~~~~~~~~~~~

*A/B Deployments* are a popular way to try a new version of an application with a small subset of users
in the production environment. With this strategy, you can specify that the older version gets most
of the user requests while a limited fraction of users get sent to the new version. Since you can
control the amount of users which get sent to the new version, you can gradually increase the volume
of requests to the new version and eventually stop using the old version. Remember that deployment
configurations don't do any autoscaling of pods, so you may have to adjust the number of pod replicas
for each version to deal with the increased/decreased load.

.. note::
  As with blue-green deployment, A/B deployments require that your application has N-1 compatibility.

To set up an A/B environment:


#. 
   Create the two applications and give them different names

   .. code-block::

       oc new-app my-app:v1 --name=my-app-a
       oc new-app my-app:v2 --name=my-app-b

#. 
   Create a route to the ``A`` service (assuming the ``my-app`` configuration contains a service)

   .. code-block::

       oc create route edge --service=my-app-a --name=my-app

#. 
   Browse to the application at ``my-app.{PROJECT}.{CLUSTER}.ccs.ornl.gov`` to verify that you see the ``A`` version. 
#. 
   Edit the route to include the second service with ``alternateBackends``
    (see the `routes <../../networking/routes.md>`_ for more information)

   .. code-block::

       oc edit route my-app
       ...
       metadata:
           name: my-app
           annotations:
               haproxy.router.openshift.io/balance: roundrobin
       spec:
           host: my-app.{PROJECT}.{CLUSTER}.ccs.ornl.gov
           to:
               kind: Service
               name: my-app-a
               weight: 10
           alternateBackends:
             - kind: Service
               name: my-app-b
               weight: 15

    In the above example, ``my-app-a`` will get 10/25, or 2/5 of the requests, and ``my-app-b`` will get
    15/25, or 3/5

Kubernetes Deployments
^^^^^^^^^^^^^^^^^^^^^^

DeploymentConfigs, described above, are an object type added to OpenShift on top of Kubernetes. Since the advent of
DeploymentConfigs, upstream Kubernetes has added its own similar object, called Deployments. Both will work on OpenShift,
and they have similar features. Here is an example.

For more information on Kubernetes Deployments, see the `official doc <https://kubernetes.io/docs/concepts/workloads/controllers/deployment/>`_


Example
~~~~~~~

.. code-block:: yaml

   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: nginx-deployment
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: nginx
     template:
       metadata:
         labels:
           app: nginx
       spec:
         containers:
         - name: nginx
           image: nginx:latest
