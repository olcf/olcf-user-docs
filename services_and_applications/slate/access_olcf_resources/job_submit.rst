####################
Batch Job Submission
####################


Batch job submission from containers is designed to work exactly like on a login
node for the cluster. The workload will need to be annotated in order to get the
necessary configuration injected at runtime.

.. csv-table::
  :header: "Cluster", "Annotation", "Value", "Schedulers"
  :widths: 5, 10, 5, 5

  "Marble", "ccs.ornl.gov/batchScheduler", "true", "Slurm, LSF"
  "Onyx", "ccs.ornl.gov/batchScheduler", "true", "LSF"

You can add the required annotations to any workload object such as a Pod, Deployment,
or a DeploymentConfig. Submitting a batch job from a container requires access to
the OLCF shared filesystems so that annotation is also included.

.. code:: yaml

  metadata:
    annotations:
      ccs.ornl.gov/batchScheduler: "true"
      ccs.ornl.gov/fs: olcf


Full example of a deployment using a base image provided by OLCF.

.. note::
  Batch job submission from containers uses SSH to access the submission host. If you
  use your own image you must install the **openssh client** package in your image.

.. code:: yaml

  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: test-jobsubmit
    annotations:
      ccs.ornl.gov/batchScheduler: "true"
      ccs.ornl.gov/fs: olcf
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
          image: "image-registry.openshift-image-registry.svc:5000/openshift/ccs-rhel7-base-amd64:latest"
          args:
          - cat
          stdin: true
          stdinOnce: true

The annotation will install wrappers into /usr/bin:

Slurm

- sbatch
- squeue

LSF

- bsub
- bjobs
