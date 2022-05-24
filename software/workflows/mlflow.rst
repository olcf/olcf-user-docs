.. _workflows-mlflow:

******
MLflow
******


Overview
========

MLflow is an open source platform to manage the Machine Learning (ML) lifecycle, including
experimentation, reproducibility, deployment, and a central model registry. To
learn more about MLflow, please refer to its
`documentation <https://mlflow.org/docs/latest/index.html>`_.


Prerequisites
================

In order to use MLflow on Summit, load the module as shown below:

.. code-block:: console

    $ module load workflows
    $ module load mlflow/1.22.0

Run the following command to verify that MLflow is available:

.. code-block:: console

    $ mlflow --version
    mlflow, version 1.22.0


Hello world!
============

To run this MLflow demo on Summit, you will create a directory with two files and then
submit a batch job to LSF from a Summit login node.

First, create a directory ``mlflow-example`` to contain two files. The first will be
named ``MLproject``:

.. code-block:: yaml

    name: demo

    entry_points:
      main:
        command: "python3 demo.py"

The second will be named ``demo.py``:

.. code-block:: python

    import mlflow
  
    print("MLflow Version:", mlflow.version.VERSION)
    print("Tracking URI:", mlflow.tracking.get_tracking_uri())

    with mlflow.start_run() as run:
        print("Run ID:", run.info.run_id)
        print("Artifact URI:", mlflow.get_artifact_uri())
        with open("hello.txt", "w") as f:
            f.write("Hello world!")
            mlflow.log_artifact("hello.txt")

Finally, create an LSF batch script called ``mlflow_demo.lsf``, and
change ``abc123`` to match your own project identifier:

.. code-block:: bash

    #BSUB -P abc123
    #BSUB -W 10
    #BSUB -nnodes 1

    #BSUB -J mlflow_demo
    #BSUB -o mlflow_demo.o%J
    #BSUB -e mlflow_demo.e%J

    module load git
    module load workflows
    module load mlflow/1.22.0

    jsrun -n 1 mlflow run ./mlflow-example --no-conda

Finally, submit the batch job to LSF by executing the following command from a
Summit login node:

.. code-block:: console

    $ bsub mlflow_demo.lsf

Congratulations! Once the job completes, you will be able to check the standard
output files to find the tracking and artifact directories.
