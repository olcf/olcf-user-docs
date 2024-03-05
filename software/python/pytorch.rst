********
PyTorch
********
PyTorch is an optimized tensor library for deep learning using GPUs and CPUs. This page outlines the how to run
PyTorch on various OLCF systems.

Summit
======
There are three ways to use PyTorch on Summit.

Build from Source
-----------------
Below is the documented process that we used for our builds. This documentation is provided for your information
in case you would like to build PyTorch yourself; however, there is no guarantee that you will be able to build an
alternative version of PyTorch.

First load the necessary modules (you can play around with these as needed):

..  code-block::

    module load miniforge3/23.11.0
    module load DefApps-2023
    module load gcc/11.2.0
    module load cuda/11.7.1
    module load magma/2.7.2-cuda117
    module load openblas/0.3.17-omp

Create a conda environment and install dependencies:

.. code-block::

    conda create -p <env_path> python=x.yy
    source activate <env_path>
    conda install cmake ninja pyyaml typing_extensions numpy

Finally clone and build pytorch:

.. code-block::

    git clone --recursive https://github.com/pytorch/pytorch
    cd pytorch
    python3 setup.py install
    python3 setup.py bdist_wheel # use this command to create a wheel package in pytorch/dist

PyTorch should now be installed in the conda environment that you created.

Provided Conda Environment
--------------------------
This is the easiest way to use pytorch on Summit. Simply load the pytorch module on Summit:

.. code-block::

    module load pytorch

This module activates a pre-made conda environment. The limitation of this method is that you
will not be able to install extra packages in this environment.

Install PyTorch with Pre-build Wheel
------------------------------------
This option is fairly easy and provides the most flexibility. In `/sw/summit/pytorch/wheel_dist` there are pre-built
wheel packages. To install one create a conda environment and use pip to install the correct package based on PyTorch
& Python version:

.. code-block::

    conda create -p <env_path> python=x.yy
    source activate <env_path>
    pip install /sw/summit/pytorch/wheel_dist/torch-2.3.0a0+giteba28a6-cp311-cp311-linux_ppc64le.whl

This should install PyTorch in your environment. You can also install whatever packages you need on top of this.

Additional Resources
====================

* `PyTorch Install Docs <https://pytorch.org/get-started/locally>`__
* `PyTorch Build from Source Docs <https://github.com/pytorch/pytorch#from-source>`__