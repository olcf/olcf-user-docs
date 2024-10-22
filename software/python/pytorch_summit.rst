*****************
PyTorch on Summit
*****************

PyTorch is an optimized tensor library for deep learning using GPUs and CPUs. This page outlines the how to run
PyTorch on Summit.

Summit
======

There are several ways to use PyTorch on Summit.

.. note::

    PyTorch is also available through the ``open-ce`` module
    (See :doc:`/software/analytics/ibm-wml-ce` for more information); however, the ``open-ce`` module provides a more
    complex environment that may not be needed.

Provided Conda Environment
--------------------------
This is the easiest way to use pytorch on Summit. Simply load the ``pytorch`` module on Summit:

.. code-block::

    module load pytorch

This module activates a pre-made conda environment. The limitation of this method is that you
will not be able to install extra packages in this environment.

.. note::

    You will also need to load the following modules, because they were used when building PyTorch for the environment.

    .. code-block::

        module load DefApps-2023
        module load gcc/11.2.0
        module load cuda/11.7.1
        module load magma/2.7.2-cuda117
        module load openblas/0.3.17-omp

    .. warning::

        You can change these modules if you need too but if you do PyTorch may not work. If you need different modules and
        they do not work with the provided environment you will have to :ref:`build-from-source`.

Install PyTorch with Pre-built Wheel
------------------------------------
This option is fairly easy and provides the most flexibility. In ``/sw/summit/pytorch/wheel_dist`` there are pre-built
wheel packages. To install one create a conda environment and use pip to install the correct package based on
Python version:

.. note::

    The wheel pacakges use the following namming convention
    ``torch-<pytorch version>+<git-commit>-<python version>-<python version>-linux_ppc64le.whl``
    (e.g. ``torch-2.3.0a0+giteba28a6-cp311-cp311-linux_ppc64le.whl`` is for python=3.11).

.. code-block::

    module load miniforge3/24.3.0-0
    conda create -p <env_path> python=x.yy
    source activate <env_path>
    pip install <wheel package>

This should install PyTorch in your environment. You can now install whatever packages you need on top of this.

.. note::

    You will also need to load the following modules, because they were used when building the wheel packages.

    .. code-block::

        module load DefApps-2023
        module load gcc/11.2.0
        module load cuda/11.7.1
        module load magma/2.7.2-cuda117
        module load openblas/0.3.17-omp

    .. warning::

        You can change these modules if you need too but if you do PyTorch may not work. If you need different modules and
        they do not work with the provided packages you will have to :ref:`build-from-source`.

.. _build-from-source:

Build from Source
-----------------
Below is the documented process that we used for our builds. This documentation is provided for your information
in case you would like to build PyTorch yourself; however, there is no guarantee that you will be able to build an
alternative version of PyTorch.

First load the necessary modules (you can play around with these as needed):

..  code-block::

    module load miniforge3/24.3.0-0
    module load DefApps-2023
    module load gcc/11.2.0
    module load cuda/11.7.1
    module load magma/2.7.2-cuda117
    module load openblas/0.3.17-omp

Create a conda environment and install dependencies:

.. code-block::

    conda create -p <env_path> python=x.yy
    source activate <env_path>
    conda install cmake ninja pyyaml typing_extensions numpy=1.26.4

Finally clone and build pytorch:

.. code-block::

    git clone --recursive https://github.com/pytorch/pytorch
    cd pytorch
    python3 setup.py install
    python3 setup.py bdist_wheel # use this command to create a wheel package in pytorch/dist

PyTorch should now be installed in the conda environment that you created.

Additional Resources
====================

* `PyTorch Install Docs <https://pytorch.org/get-started/locally>`__
* `PyTorch Build from Source Docs <https://github.com/pytorch/pytorch#from-source>`__
