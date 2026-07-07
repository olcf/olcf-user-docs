####################
Batch Job Submission
####################

Overview
========

Batch job submission from containers is designed to work exactly like on a login
node for the cluster. The workload will need to be annotated in order to get the
necessary configuration injected at runtime.

.. csv-table::
  :header: "Cluster", "Annotation", "Value", "Schedulers"
  :widths: 5, 10, 5, 5

  "Marble", "ccs.ornl.gov/batchScheduler", "true", "Slurm"
  "Onyx", "ccs.ornl.gov/batchScheduler", "true", "Slurm"

You can add the required annotations to any workload object such as a Pod, Deployment,
or a DeploymentConfig. Submitting a batch job from a container requires access to
the OLCF shared filesystems so that annotation is also included.

.. code:: yaml

  metadata:
    annotations:
      ccs.ornl.gov/batchScheduler: "true"
      ccs.ornl.gov/fs: orion


Deployment Example
==================

Full example of a deployment using a base image provided by OLCF.

.. note::
  Batch job submission from containers uses SSH to access the submission host. If you
  use your own image you must install the **openssh client** package in your image.


Marble
------

.. code:: yaml

  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: test-jobsubmit
    annotations:
      ccs.ornl.gov/batchScheduler: "true"
      ccs.ornl.gov/fs: orion
  spec:
    replicas: 1
    selector:
      matchLabels:
        app: test-jobsubmit
    template:
      metadata:
        labels:
          app: test-jobsubmit
      spec:
        containers:
        - name: test-jobsubmit
          # this image was chosen because it has openSSH installed, please build your own image with openSSH for production use
          image: "linuxserver/openssh-server:latest"
          command: ["/bin/sh","-c"]
          args:
          - cat
          tty: true
          stdin: true

Onyx
----

.. code:: yaml

  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: test-jobsubmit
    annotations:
      ccs.ornl.gov/batchScheduler: "true"
      ccs.ornl.gov/fs: wolf2
  spec:
    replicas: 1
    selector:
      matchLabels:
        app: test-jobsubmit
    template:
      metadata:
        labels:
          app: test-jobsubmit
      spec:
        containers:
        - name: test-jobsubmit
          # this image was chosen because it has openSSH installed, please build your own image with openSSH for production use
          image: "linuxserver/openssh-server:latest"
          command: ["/bin/sh","-c"]
          args:
          - cat
          tty: true
          stdin: true


Additional Information
======================

The annotation will install wrappers into /usr/bin:

Slurm

- sbatch
- squeue

LSF

- bsub
- bjobs
