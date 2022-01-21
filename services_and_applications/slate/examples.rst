
.. _slate_examples:

###########################
YAML Object Quick Reference
###########################

Examples of basic Kubernetes objects meant to be used as a reference for those familiar with Kubernetes.

CronJobs
--------

Basic Cronjob
^^^^^^^^^^^^^

.. code-block:: yaml

   apiVersion: batch/v1beta1
   kind: CronJob
   metadata:
   # Name of cronjob
     name: hello-openshift
   spec:
   # If the cronjob does not start in this time it will be marked as failed
     startingDeadlineSeconds: 10
     schedule: "*/1 * * * *"
     # Cronjobs create jobs every schedule above. This is the template for the job to be created
     jobTemplate:
     # The job creates a pod. This is the spec for the pod
       spec:
         template:
         # Container spec
           spec:
             containers:
             # Container name
             - name: hello-openshift
             # Container image
               image: image-registry.openshift-image-registry.svc:5000/openshift/ccs-rhel7-base-amd64
               tag: latest
               # Command to be run inside the container
               args:
                 - /bin/sh
                 - -c
                 - echo "hello openshift"
             restartPolicy: Never

Deployments and Stateful Sets
-----------------------------

Basic Deployment
^^^^^^^^^^^^^^^^

.. code-block:: yaml

   apiVersion: apps/v1
   kind: Deployment
   metadata:
     # deployment name
     name: test-pod-deployment
   spec:
     # number of replicas
     replicas: 3
     selector:
       # this sets the label the deployment is looking for
       matchLabels:
         app: test-pod
     template:
       metadata:
         # labels are how the deployments keep track of their objects. This sets a label on the pod
         labels:
           app: test-pod
       spec:
         containers:
           # container name
         - name: test-pod
           # using the base image
           image: "image-registry.openshift-image-registry.svc:5000/openshift/ccs-rhel7-base-amd64"
           # Generic command that will not return
           command: ["cat"]
           # Need a tty if we are to SSH. Need stdin for tty
           tty: true
           stdin: true

Basic Stateful Set
^^^^^^^^^^^^^^^^^^

.. code-block:: yaml

   apiVersion: apps/v1
   kind: StatefulSet
   metadata:
     # statefulset name
     name: test-pod-stateful-set
   spec:
     # number of replicas
     replicas: 3
     selector:
       # this sets the label the stateful set is looking for
       matchLabels:
         app: test-pod
     template:
       metadata:
         # labels are how the stateful set keep track of their objects. This sets a label on the pod
         labels:
           app: test-pod
       spec:
         containers:
           # container name
         - name: test-pod
           # using the base image
           image: "image-registry.openshift-image-registry.svc:5000/openshift/ccs-rhel7-base-amd64"
           # Generic command that will not return
           command: ["cat"]
           # Need a tty if we are to SSH. Need stdin for tty
           tty: true
           stdin: true

Pods
----

Basic Pod you can create and get a shell in
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml

   apiVersion: v1
   kind: Pod
   metadata:
     # Pod name
     name: test-pod
   spec:
     containers:
       # Container name
       - name: test-container
         # Using the base image
         image: "image-registry.openshift-image-registry.svc:5000/openshift/ccs-rhel7-base-amd64"
         # Generic command that will not return
         command: ["cat"]
         # Need a tty if we are to SSH. Need stdin for tty
         tty: true
         stdin: true

Pod that mounts a volume named test-pod-pvc
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml

   apiVersion: v1
   kind: Pod
   metadata:
     # Pod name
     name: test-pod
   spec:
     containers:
       # Container name
       - name: test-pod
         # Using the base image
         image: "image-registry.openshift-image-registry.svc:5000/openshift/ccs-rhel7-base-amd64"
         # Generic command that will not return
         command: ["cat"]
         # Need a tty if we are to SSH. Need stdin for tty
         tty: true
         stdin: true
         volumeMounts:
           # Where in the pod the volume will be mounted
           - mountPath: /etc/test-volume
             # What the volume was named
             name: test-pod-volume
     volumes:
         # Setting the name. What the volume will be referred to in the pod spec
       - name: test-pod-volume
         persistentVolumeClaim:
           # The name of the already created pvc that the volume will be bound to
           claimName: test-pod-pvc

The yaml that defines the PVC that is being mounted by the above pod can be found in the `Volumes <#volumes>`_ section

Roles and Rolebindings
----------------------

Role
^^^^

.. code-block:: yaml

   apiVersion: rbac.authorization.k8s.io/v1
   kind: Role
   metadata:
   # Role Name
     name: pod-reader
   rules:
   # "" indicates the core API group
   - apiGroups: [""]
   # What object the verbs apply to
     resources: ["pods"]
   # The API requests allowed on the above object
     verbs: ["get", "watch", "list"]

The verbs match to HTTP verbs against the API. A list of that matching `can be found here <https://kubernetes.io/docs/reference/access-authn-authz/authorization/#determine-the-request-verb>`_.

Rolebinding
^^^^^^^^^^^

.. code-block:: yaml

   apiVersion: rbac.authorization.k8s.io/v1
   # This role binding allows user "2jl" to read pods in the "default" namespace.
   # You need to already have a Role named "pod-reader" in that namespace.
   kind: RoleBinding
   metadata:
     # Name of the RoleBinding
     name: read-pods
     # Namespace for the RoleBinding
     namespace: default
   subjects:
   # You can specify more than one "subject"
   - kind: User
     name: 2jl
     apiGroup: rbac.authorization.k8s.io
   roleRef:
     # kind is what your binding is to. In this case a Role
     kind: Role
     # The Role you are binding the user to
     name: pod-reader
     apiGroup: rbac.authorization.k8s.io

Routes, Services and Nodeports
------------------------------

Route
^^^^^

.. code-block:: yaml

   apiVersion: route.openshift.io/v1
   kind: Route
   metadata:
   # Route Name
     name: test-route
   spec:
    # The URL. Must be unique across cluster.
     host: test-route-stf002platform-hello-openshift.apps.marble.ccs.ornl.gov
     tls:
     # redirects traffic from insecure port to secure port
       insecureEdgeTerminationPolicy: Redirect
       termination: edge
     to:
     # This is a route and thus points to a service
       kind: Service
     # name of the service to point to
       name: test-service

Service
^^^^^^^

.. code-block:: yaml

   apiVersion: v1
   kind: Service
   metadata:
   # Service name
     name: test-service
   spec:
     ports:
     # Port name
     - name: nginx
     # The port being exposed by the service to the Route
       port: 443
     # The port on the pod being exposed to the Service
       targetPort: 8080
       protocol: TCP
     selector:
     # A label that will match a pod
       app: test-route
     sessionAffinity: None
     # How the service is exposed. For routes the type would be ClusterIP
     type: ClusterIP

**Note** the above service is assuming that the pod is serving traffic on port 8080

NodePort
^^^^^^^^

.. code-block:: yaml

   apiVersion: v1
   kind: Service
   metadata:
     name: nodeport
   spec:
     ports:
     # The nodeport port
     - port: 8081
     # The port that will be exposed on all nodes in the cluster. Must be in range 30000-32767. Can be left blank and randomly assigned by system.
       nodePort: 322394
     # The port on the pod being exposed
       targetPort: 8080
       protocol: TCP
     selector:
       app: test-nodeport
     type: NodePort

Persistent Volume Claims
------------------------

Basic PVC
^^^^^^^^^

.. code-block:: yaml

   apiVersion: v1
   kind: PersistentVolumeClaim
   metadata:
     # The name of the claim
     name: test-pod-pvc
   spec:
     # The type of storage being requested. This can be blank and it will be
     # set to the default value, which is netapp-nfs, but it is good practice
     # to explictly declare it.
     storageClassName: netapp-nfs
     # how the volume can be accessed. ReadWriteMany, or RWX as it is abbreviated,
     # means the volume can be mounted as Read Write by multiple nodes
     accessModes:
     - ReadWriteMany
     resources:
       # the amount of storage being requested
       requests:
         storage: 1Gi


Basic VolumeSnapshot
^^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml

    apiVersion: snapshot.storage.k8s.io/v1beta1
    kind: VolumeSnapshot
    metadata:
      # Snapshot name
      name: pvc1-snap
    spec:
      source:
        # Persistent Volume to snapshot
        persistentVolumeClaimName: test-pod-pvc