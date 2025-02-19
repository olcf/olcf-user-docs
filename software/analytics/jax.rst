***
JAX
***

`JAX <https://jax.readthedocs.io/en/latest/>`__ is a Python library for accelerator-oriented array computation and program transformation, designed for high-performance numerical computing and large-scale machine learning.
JAX provides a familiar NumPy-style API that can execute on either CPUs, GPUs, or TPUs.

OLCF Systems this guide applies to:

* :doc:`Frontier </systems/frontier_user_guide>`


**Guide last tested with:**

+------------+-------------------------+
| ``python`` | .. centered:: ``jax``   |
+============+=========================+
|  3.11.11   |  0.4.35                 |
+------------+-------------------------+


Setting up the environment
==========================

.. warning::
   Before setting up your environment, you must exit and log back in so that you have a fresh login shell.
   This is to ensure that no previously activated environments exist in your ``$PATH`` environment variable.

First, load the correct modules:

.. tab-set::

   .. tab-item:: Frontier
      :sync: frontier

      .. code-block:: bash

         module load PrgEnv-gnu/8.6.0
         module load rocm/6.2.4 # may work with ROCm 6.0.0 and 6.1.x
         module load craype-accel-amd-gfx90a
         module load miniforge3/23.11.0-0

Loading a python module puts you in a "base" environment, but you need to create a new environment using the ``conda create`` command:

.. tab-set::

   .. tab-item:: Frontier
      :sync: frontier

      .. code-block:: bash

         conda create -n jax_env-frontier python=3.11 numpy scipy -c conda-forge
         source activate jax_env-frontier

.. note::
   NumPy and Scipy are installed ahead of time, but you can instead install those with ``pip`` later if desired.

Installing JAX
==============

Building JAX involves two steps:

#. Installing ``jaxlib`` and any GPU (CUDA/ROCm) plugins.
#. Installing the literal ``jax`` package.

Now that you have a fresh environment, we will install things into your new environment using ``pip``.

.. tab-set::

   .. tab-item:: Frontier
      :sync: frontier

      .. code-block:: bash

         # Install the ROCm plugins
         pip install jax-rocm60-pjrt==0.4.35 jax-rocm60-plugin==0.4.35 --no-cache-dir

         # Install JAX (will also install jaxlib)
         pip install jax==0.4.35 --no-cache-dir


Testing JAX
===========

To test your ``jax`` install, try running their ``mnist_classifier`` example (on a compute node):

.. code-block:: bash

   # Start an interactive job
   salloc -A PROJECT_ID -N1 -t 10

   # Enable the proxy server (allows compute node to download datasets)
   export all_proxy=socks://proxy.ccs.ornl.gov:3128/
   export ftp_proxy=ftp://proxy.ccs.ornl.gov:3128/
   export http_proxy=http://proxy.ccs.ornl.gov:3128/
   export https_proxy=http://proxy.ccs.ornl.gov:3128/
   export no_proxy='localhost,127.0.0.0/8,*.ccs.ornl.gov'

   # Get and run the example
   mkdir test_dir/
   cd test_dir/
   git clone https://github.com/google/jax.git jax
   cp jax/examples/datasets.py .
   cp jax/examples/mnist_classifier.py .
   sed -i -e 's/from examples //' mnist_classifier.py
   python3 -c 'import jax; print(jax.devices())' # verify that the GPU is accessible
   python3 mnist_classifier.py # run the example training

Running that example, you should see something similar to:

.. code-block:: text

   Starting training...
   Epoch 0 in 5.14 sec
   Training set accuracy 0.8719666600227356
   Test set accuracy 0.8804999589920044
   Epoch 1 in 0.20 sec
   Training set accuracy 0.8979166746139526
   Test set accuracy 0.9031999707221985
   Epoch 2 in 0.19 sec
   Training set accuracy 0.9092666506767273
   Test set accuracy 0.9142999649047852
   Epoch 3 in 0.18 sec
   Training set accuracy 0.9170666933059692
   Test set accuracy 0.9220999479293823
   Epoch 4 in 0.20 sec
   Training set accuracy 0.9226666688919067
   Test set accuracy 0.9279999732971191
   Epoch 5 in 0.18 sec
   Training set accuracy 0.9271833300590515
   Test set accuracy 0.9297999739646912
   Epoch 6 in 0.19 sec
   Training set accuracy 0.9323500394821167
   Test set accuracy 0.9328999519348145
   Epoch 7 in 0.18 sec
   Training set accuracy 0.9357166886329651
   Test set accuracy 0.9364999532699585
   Epoch 8 in 0.18 sec
   Training set accuracy 0.9387500286102295
   Test set accuracy 0.9393999576568604
   Epoch 9 in 0.18 sec
   Training set accuracy 0.942550003528595
   Test set accuracy 0.9419999718666077

Additional Resources
====================

* `ROCm JAX docs <https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/3rd-party/jax-install.html>`__
* `Installing JAX from source <https://jax.readthedocs.io/en/latest/developer.html>`__
* `ROCm JAX fork <https://github.com/ROCm/jax/releases>`__
* `JAX User Guide <https://jax.readthedocs.io/en/latest/user_guides.html#user-guides>`__
