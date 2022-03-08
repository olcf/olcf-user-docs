.. _workflows-mlflow:

******
MLflow
******


Overview
========

MLflow is an open source platform to manage the ML lifecycle, including
experimentation, reproducibility, deployment, and a central model registry. To
learn more about MLflow, refer to its `documentation <https://mlflow.org/docs/latest/index.html>`_.


MLflow on Summit
================

In order to use MLflow on Summit, use the MLflow module as shown below:

.. code-block:: console

    $ module load workflows
    $ module load mlflow/1.22.0

Now, MLflow should be available to use. Run the following command as quick verification:

.. code-block:: console

    $ mlflow --version

Further information about using MLflow may be found at the MLflow `website <https://mlflow.org>`_.
