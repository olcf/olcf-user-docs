######################
Mount OLCF Filesystems
######################

OLCF shared filesystems can be mounted into a container running in Slate. The mountpoints
will be the same as a cluster node. The Kubernetes object will need to be annotated in order
to get the necessary configuration injected into the container at runtime.

.. csv-table::
  :header: "Cluster", "Annotation", "Value", "Mounts"
  :widths: 5, 8, 5, 25

  "Marble", "ccs.ornl.gov/fs", "alpine2", "/ccs/sw, /ccs/home, /ccs/sys, /ccs/proj, /gpfs/alpine2"
  "Marble", "ccs.ornl.gov/fs", "orion", "/ccs/sw, /ccs/home, /ccs/sys, /ccs/proj, /lustre/orion"
  "Marble", "ccs.ornl.gov/fs", "kronos", "/ccs/sw, /ccs/home, /ccs/sys, /ccs/proj, /nl/kronos"
  "Onyx", "ccs.ornl.gov/fs", "themis", "/ccsopen/sw, /ccsopen/home, /ccsopen/proj, /nl/themis"
  "Onyx", "ccs.ornl.gov/fs", "wolf2", "/ccsopen/sw, /ccsopen/home, /ccsopen/proj, /gpfs/wolf2"

For each of the following examples, replace "ccs.ornl.gov/fs=olcf" or "ccs.ornl.gov/fs: olcf" with an annotation from the above list.

If you already have a Deployment running you can add the annotation with the client

.. code:: bash

  oc annotate deployment web ccs.ornl.gov/fs=olcf

.. warning::
  You cannot annotate an existing pod because the injection happens at pod creation time

  .. pull-quote::

    Annotating a pod not managed by a deployment with ``oc annotate pod test ccs.ornl.gov/fs=olcf``
    will not work. Instead delete the pod and add the annotation to the metadata and recreate it.

You can also add the annotations to any workload object's YAML such as a Pod, Deployment,
or DeploymentConfig.

.. code:: yaml

  kind: Deployment
  metadata:
    annotations:
      ccs.ornl.gov/fs: olcf
  ---
  kind: DeploymentConfig
  metadata:
    annotations:
      ccs.ornl.gov/fs: olcf
  ---
  kind: Pod
  metadata:
    annotations:
      ccs.ornl.gov/fs: olcf

Full example of a deployment mounting the OLCF shared filesystems:

.. code:: yaml

  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: test-fs
    annotations:
      ccs.ornl.gov/fs: olcf
  spec:
    replicas: 1
    selector:
      matchLabels:
        app: test-fs
    template:
      metadata:
        labels:
          app: test-fs
      spec:
        containers:
        - name: test-fs
          image: busybox:latest
          args:
          - cat
          stdin: true
          stdinOnce: true

.. note::
  There are no requirements in the container image in order to mount OLCF filesystems

The following annotations have been retired and should no longer be used in workloads in OpenShift.

.. csv-table::
  :header: "Cluster", "Annotation", "Value", "Mounts"
  :widths: 5, 8, 5, 25

  "Marble", "ccs.ornl.gov/fs", "olcf", "/ccs/sw, /ccs/home, /ccs/sys, /ccs/proj, /gpfs/alpine"
  "Onyx", "ccs.ornl.gov/fs", "ccsopen", "/ccsopen/sw, /ccsopen/home, /ccsopen/proj, /gpfs/wolf"

