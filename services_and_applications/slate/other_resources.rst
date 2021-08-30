.. _slate_other_resources:

******************************
Schedule Other Slate Resources
******************************

Beyond the standard CPU/Memory/Disk allocation, Slate also has other resources that can be allocated such as GPUs. Check with OLCF
support first to make sure that your project can schedule these resources.

GPUs
====

GPUs can be scheduled and made available directly in a pod. Kubernetes handles configuring the drivers in the container image.

.. warning::

  GPUs in Slate are still an experimental functionality, please reach out to OLCF support so we can better understand your use case

.. note::

  We are targeting use cases that need GPUs for long running services. For batch access to GPUs we recommend using the standard
  HPC clusters in NCCS

The Slate Marble cluster has nodes with three NVIDIA Tesla V100 GPUs per node available for scheduling so a single pod could
request from 1 to 3 GPUs

Pod Example
-----------

.. code-block:: yaml

  apiVersion: v1
  kind: Pod
  metadata:
    name: cuda-vector-add
  spec:
    restartPolicy: OnFailure
    containers:
      - name: cuda-vector-add
        # https://github.com/kubernetes/kubernetes/blob/v1.7.11/test/images/nvidia-cuda/Dockerfile
        image: "k8s.gcr.io/cuda-vector-add:v0.1"
        resources:
          limits:
            nvidia.com/gpu: 1 # requesting 1 GPU

In the above example we are requesting one GPU using the ``pod.spec.resources.limits`` 

Caveats
-------

* GPUs can only be specified in the ``.limits`` section
* Containers and Pods do not share GPUs, the allocation is for **exclusive use** of the requested GPUs
* Containers can request one or more GPUs

Upstream documentation
----------------------

* https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/
