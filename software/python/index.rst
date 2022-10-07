
***********************
Python on OLCF Systems
***********************

.. warning::
    Currently, Crusher and Frontier do **NOT** have Anaconda/Conda modules.
    To use conda, you will have to download and install Miniconda on your own
    (see `Miniconda Documentation <https://docs.conda.io/en/latest/miniconda.html>`__).
    Alternatively, you can use Python's inherent virtual environments ``venv``
    feature with the ``cray-python`` module instead.  For more details on ``venv``, 
    see `Python's Official Documentation <https://docs.python.org/3/tutorial/venv.html>`__.
    Contact help@olcf.ornl.gov if conda is required for your workflow, or if you
    have any issues.

Overview
========

In high-performance computing, `Python <https://www.python.org/>`__ is heavily
used to analyze scientific data on the system. Some users require specific
versions of Python or niche scientific packages to analyze their data, which
may further depend on numerous other Python packages. Because of all the
dependencies that some Python packages require, and all the types of data that
exist, it can be quite troublesome to get different Python installations to
"play nicely" with each-other, especially on an HPC system where the system
environment is complicated. `Conda
<https://conda.io/projects/conda/en/latest/index.html>`__, a package and
virtual environment manager from the `Anaconda <https://www.anaconda.com/>`__
distribution, helps alleviate these issues.

Conda allows users to easily install different versions of binary software
packages and any required libraries appropriate for their computing platform.
The versatility of conda allows a user to essentially build their own isolated
Python environment, without having to worry about clashing dependencies and
other system installations of Python. Conda is available on OLCF systems, and
loading the default Python module loads an Anaconda Python distribution.
Loading this distribution automatically puts you in a "base" conda environment,
which already includes packages that one can use for simulation, analysis, and
machine learning.

For users interested in using Python with Jupyter, see our :doc:`Jupyter at OLCF
</services_and_applications/jupyter/overview>` page instead.

For users interested in using the machine learning ``open-ce`` module (formerly
``ibm-wml-ce``) on Summit, see our :doc:`/software/analytics/ibm-wml-ce` page.

.. _python-guides:

OLCF Python Guides
==================

Below is a list of guides created for using Python on OLCF systems.

.. toctree::
   :maxdepth: 1
   :hidden:  
 
   conda_basics
   parallel_h5py
   cupy

* :doc:`Conda Basics Guide </software/python/conda_basics>`: Goes over the basic workflow and commands of Conda
* :doc:`Installing Parallel h5py Guide </software/python/parallel_h5py>`: Teaches you how to install parallel-enabled h5py and mpi4py
* :doc:`Installing CuPy Guide </software/python/cupy>`: Teaches you how to install CuPy

.. note::
   For newer users to conda, it is highly recommended to view our :doc:`Conda
   Basics Guide </software/python/conda_basics>`, where a :ref:`conda-quick`
   list is provided.

Module Usage
============

To start using Python, all you need to do is load the module:

.. code-block:: bash

   $ module load python

Base Environment
----------------

Loading the Python module on all systems will put you in a "base"
pre-configured conda environment. This option is recommended for users who do
not need custom environments, and only require packages that are already
installed in the base environment. This option is also recommended for users
that just need a Python interpreter or standard packages like NumPy, Scipy, and
Matplotlib. 

To see a full list of the packages installed in the base environment, use
``conda list``. A small preview from Summit is provided below:

.. code-block:: bash

   $ module load python
   $ conda list

   # packages in environment at /sw/summit/python/3.8/anaconda3/2020.07-rhel8:
   #
   # Name                    Version                   Build  Channel
   _ipyw_jlab_nb_ext_conf    0.1.0                    py38_0  
   _libgcc_mutex             0.1                        main  
   alabaster                 0.7.12                     py_0  
   anaconda                  2020.07                  py38_0  
   anaconda-client           1.7.2                    py38_0  
   anaconda-project          0.8.4                      py_0  
   asn1crypto                1.3.0                    py38_0  
   astroid                   2.4.2                    py38_0  
   astropy                   4.0.1.post1      py38h7b6447c_1
   .
   .
   .  

.. warning::
   It is not recommended to try to install new packages into the base environment.
   Instead, you can clone the base environment for yourself and install packages
   into the clone. To clone an environment, you must use the ``--clone
   <env_to_clone>`` flag when creating a new conda environment. An example for
   cloning the base environment is provided in :ref:`python-best-pract` below.

Custom Environment
------------------

You can also create your own custom conda environment after loading the Python
module. This option is recommended for users that require a different version
of Python than the default version available, or for users that want a personal
environment to manage specialized packages.

.. note::
   A more complete list of commands is provided in the :ref:`conda-quick`
   section of the :doc:`Conda Basics Guide </software/python/conda_basics>`.

To create and activate an environment in a **specific location** using Python
version X.Y, use the ``-p`` flag:

.. code-block:: bash

   $ module load python
   $ conda create -p /path/to/my_env python=X.Y
   $ source activate /path/to/my_env

To create and activate an environment with a **specific name** using Python
version X.Y, use the ``--name`` flag (by default, this creates the environment
in your ``$HOME`` directory):

.. code-block:: bash

   $ module load python
   $ conda create --name my_env python=X.Y
   $ source activate my_env

.. note::
   It is highly recommended to create new environments in the "Project Home"
   directory (``/ccs/proj/<project_id>/<user_id>``). This space avoids purges,
   allows for potential collaboration within your project, and works better with
   the compute nodes. It is also recommended, for convenience, that you use
   environment names that indicate the hostname, as virtual environments created
   on one system will not necessarily work on others.

It is always recommended to deactivate an environment before activating a new one.
Deactivating an environment can be achieved through:

.. code-block:: bash

   $ source deactivate # deactivates the current environment

How to Run
==========

.. warning::
   Remember, at larger scales both your performance and your fellow users'
   performance will suffer if you do not run on the compute nodes. It is always
   highly recommended to run on the compute nodes (through the use of a batch job
   or interactive batch job).

The OS-provided Python is no longer accessible as ``python`` (including
variations like ``/usr/bin/python`` or ``/usr/bin/env python``); rather, you 
must specify it as ``python2`` or ``python3``. If you are using python from one 
of the module files rather than the version in ``/usr/bin``, this change should
not affect how you invoke python in your scripts, although we encourage
specifying ``python2`` or ``python3`` as a best practice.

Summit
------

Batch Script - Summit
^^^^^^^^^^^^^^^^^^^^^

To use Python on a Summit compute node, you **must** use ``jsrun``, even if
running in serial.

Additionally, ``$PATH`` issues are known to occur after having loaded multiple
conda environments before submitting a batch script. Therefore, it is
recommended to use a fresh login shell before submission. The ``-L`` flag for
``bsub`` ensures that no previously set environment variables are passed into
the batch job.

.. code-block:: bash

   $ bsub -L $SHELL submit.lsf

This means you will have to load your modules and activate your environment
inside the batch script. An example batch script for Summit is provided below:

.. code-block:: bash

   #!/bin/bash
   #BSUB -P PROJECT_ID
   #BSUB -W 00:05
   #BSUB -nnodes 1
   #BSUB -J python
   #BSUB -o python.%J.out
   #BSUB -e python.%J.err

   cd $LSB_OUTDIR
   date

   module load python
   source activate my_env

   jsrun -n1 -r1 -a1 -c1 python3 script.py

Interactive Job - Summit
^^^^^^^^^^^^^^^^^^^^^^^^

To use Python in an interactive session on Summit:

.. code-block:: bash

   $ module load python
   $ bsub -W 0:05 -nnodes 1 -P <PROJECT_ID> -Is $SHELL
   $ source activate my_env
   $ jsrun -n1 -r1 -a1 -c1 python3 script.py

Andes
-----

Batch Script - Andes
^^^^^^^^^^^^^^^^^^^^

On Andes, you are already on a compute node once you are in a batch job.
Therefore, you only need to use ``srun`` if you plan to run parallel-enabled
Python.

Similar to Summit (see above), ``$PATH`` issues are known to occur if not
submitting from a fresh login shell, which can result in the wrong conda
environment being detected. To avoid this, you must use the ``--export=NONE``
flag, which ensures that no previously set environment variables are passed
into the batch job:

.. code-block:: bash

   $ sbatch --export=NONE submit.sl

This means you will have to load your modules and activate your environment
inside the batch script. An example batch script for Andes is provided below:

.. code-block:: bash

   #!/bin/bash
   #SBATCH -A <PROJECT_ID>
   #SBATCH -J python
   #SBATCH -N 1
   #SBATCH -p batch
   #SBATCH -t 0:05:00

   cd $SLURM_SUBMIT_DIR
   date

   module load python
   source activate my_env

   python3 script.py

Interactive Job - Andes
^^^^^^^^^^^^^^^^^^^^^^^

To use Python in an interactive session on Andes:

.. code-block:: bash

   $ module load python
   $ salloc -A <PROJECT_ID> -N 1 -t 0:05:00
   $ source activate my_env
   $ python3 script.py

.. _python-best-pract:

Best Practices
==============

* Cloning the base environment:

    It is not recommended to try to install new packages into the base
    environment. Instead, you can clone the base environment for yourself and
    install packages into the clone. To clone an environment, you must use the
    ``--clone <env_to_clone>`` flag when creating a new conda environment. An
    example for cloning the base environment into a specific directory called
    ``conda_envs/summit/`` in your "Project Home" on Summit is provided below:

    .. code-block:: bash

       $ conda create -p /ccs/proj/<project_id>/<user_id>/conda_envs/summit/baseclone-summit --clone base
       $ source activate /ccs/proj/<project_id>/<user_id>/conda_envs/summit/baseclone-summit

* Environment locations:

    It is highly recommended to create new environments in the "Project Home"
    directory (``/ccs/proj/<project_id>/<user_id>``). This space avoids purges,
    allows for potential collaboration within your project, and works better with
    the compute nodes. It is also recommended, for convenience, that you use
    environment names that indicate the hostname, as virtual environments created
    on one system will not necessarily work on others.

* Adding known environment locations:

    For a conda environment to be callable by a "name", it must be installed in
    one of the ``envs_dirs`` directories. The list of known directories can be seen
    by executing:

    .. code-block:: bash

       $ conda config --show envs_dirs

    On OLCF systems, the default location is your ``$HOME`` directory.  If you
    plan to frequently create environments in a different location other than the
    default (such as ``/ccs/proj/...``), then there is an option to add directories
    to the ``envs_dirs`` list.
  
    For example, to track conda environments in a subdirectory called ``summit``
    in Project Home you would execute:

    .. code-block:: bash

       $ conda config --append envs_dirs /ccs/proj/<project_id>/<user_id>/conda_envs/summit

    This will create a ``.condarc`` file in your ``$HOME`` directory if you do not have
    one already, which will now contain this new envs_dirs location.  This will now
    enable you to use the ``--name env_name`` flag when using conda commands for
    environments stored in the ``summit`` directory, instead of having to use the
    ``-p /ccs/proj/<project_id>/<user_id>/conda_envs/summit/env_name``
    flag and specifying the full path to the environment.  For example, you can do
    ``source activate my_env`` instead of ``source activate
    /ccs/proj/<project_id>/<user_id>/conda_envs/summit/my_env``.

