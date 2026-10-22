.. _py-index:

***********************
Python on OLCF Systems
***********************

.. note::
    OLCF systems provide conda in the form of the ``miniforge3`` module.
    `Miniforge <https://github.com/conda-forge/miniforge>`__ behaves similarly to
    older Anaconda modules, but target the ``conda-forge`` channel by default.

Overview
========

In high-performance computing, `Python <https://www.python.org/>`__ is heavily
used to analyze scientific data on the system. Some users require specific
versions of Python or niche scientific packages to analyze their data, which
may further depend on numerous other Python packages. Because of all the
dependencies that some Python packages require, and all the types of data that
exist, it can be quite troublesome to get different Python installations to
"play nicely" with each-other, especially on an HPC system where the system
environment is complicated. "Virtual environments" help alleviate these issues
by isolating package installations into self-contained directory trees.

Although Python has a native virtual environment feature (``venv``), one
popular virtual environment manager is `Conda
<https://docs.conda.io/projects/conda/en/latest/index.html>`__, an open source
package and virtual environment manager. Conda allows users to easily install
different versions of binary software packages and any required libraries
appropriate for their computing platform.  The versatility of conda allows a
user to essentially build their own isolated Python environment, without having
to worry about clashing dependencies and other system installations of Python.
Conda is available on OLCF systems via `Miniforge <https://github.com/conda-forge/miniforge>`__.

For users interested in using Python with Jupyter, see our :doc:`Jupyter at OLCF
</services_and_applications/jupyter/overview>` page instead.

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
   sbcast_conda
   jupyter_envs
   ../analytics/pytorch_frontier
   ../analytics/jax

* :doc:`Conda Basics Guide </software/python/conda_basics>`: Goes over the basic workflow and commands of Conda **(Frontier/Riker/Lux)**
* :doc:`Installing mpi4py and h5py Guide </software/python/parallel_h5py>`: Teaches you how to install parallel-enabled h5py and mpi4py **(Frontier/Riker/Lux)**
* :doc:`Installing CuPy Guide </software/python/cupy>`: Teaches you how to install CuPy **(Frontier/Riker/Lux)**
* :doc:`Sbcast Conda Environments Guide </software/python/sbcast_conda>`: Teaches you how to ``sbcast`` your conda environments to speedup initialization **(Frontier)**
* :doc:`Jupyter Visibility Guide </software/python/jupyter_envs>`: Teaches you how to make your conda environments visible to Jupyter **(Frontier/Riker/Lux)**
* :doc:`PyTorch on Frontier </software/analytics/pytorch_frontier>`: Shows how to access PyTorch on Frontier **(Frontier)**
* :doc:`JAX </software/analytics/jax>`: Teaches you how to install JAX **(Frontier)**


.. note::
   For newer users to conda, it is highly recommended to view our :doc:`Conda
   Basics Guide </software/python/conda_basics>`, where a :ref:`conda-quick`
   list is provided.


.. _python-mods:

Module Usage
============


To start using Python, all you need to do is load the module:

.. tab-set::

   .. tab-item:: Frontier
      :sync: frontier

      .. code-block:: bash

         module load miniforge3/23.11.0-0

   .. tab-item:: Riker
      :sync: riker

      .. code-block:: bash

         module load miniforge3/25.3.1-0

   .. tab-item:: Lux
      :sync: lux

      .. code-block:: bash

         module load miniforge3/26.3.2-3

The ``miniforge3`` module functions with ``bash``, ``zsh``, ``tcsh``, and ``csh``.
Users encountering problems with other shell environments should reach out to help@olcf.ornl.gov for assistance.

.. note::
    When loading the default ``miniforge3`` module, you will be placed in the base environment.
    If you have any conda environments already active, this will output ``Deactivating conda environments``
    until you are deactivated to the base environment. This behavior is also seen when using ``module reset``
    and ``module purge``.

.. warning::
   When using the conda modules, do **NOT** run ``conda init``. This will end
   up hard-coding a conda installation into your shell configuration file (e.g.,
   ``.bashrc``, ``.bash_profile``, etc.) and could cause problems when switching
   between HPC systems.  If you have a code-block in your configuration file
   starting with ``>>> conda initialize >>>``, it is recommended to delete the entire block.


Base Environment
----------------

Loading the Python module on all systems will put you in a "base"
pre-configured environment. This option is recommended for users who do not
need custom environments and only require a Python installation. The
pre-installed package list in the base environment is inherently minimal and
users are encouraged to install packages for themselves in a different environment.

To see a full list of the packages installed in the base environment, use ``conda list``.

.. warning::
   It is not recommended to try to install new packages into the base
   environment.  Instead, you can either clone the base environment for yourself
   and install packages into the clone, or create a brand new (empty) environment
   and install packages into it.  An example for cloning the base environment is
   provided in :ref:`python-best-pract` below, while creating new environments
   is covered directly below in :ref:`python-custom-envs`. Although cloning is
   possible, in most scenarios it is recommended to start with a new environment.

.. _python-custom-envs:

Custom Environments
-------------------

You can also create your own custom environments after loading the Python
module. This option is recommended for users that require a different version
of Python than the default version available, or for users that want a personal
environment to manage specialized packages. This is possible via ``conda``
commands.

.. note::
   A more complete list of ``conda`` commands is provided in the :ref:`conda-quick`
   section of the :doc:`Conda Basics Guide </software/python/conda_basics>`.

To create and activate an environment:

.. tab-set::

   .. tab-item:: Frontier
      :sync: frontier

      .. code-block:: bash

         #1. Load the module
         module load miniforge3/23.11.0-0

         #2a. Create "my_env" with Python version X.Y at the desired path
         conda create -p /path/to/my_env python=X.Y

         #2b. Create "my_env" with Python version X.Y with a specific name (defaults to $HOME directory)
         conda create --name my_env python=X.Y

         #3. Activate "my_env"
         conda activate /path/to/my_env

   .. tab-item:: Riker
      :sync: riker

      .. code-block:: bash

         #1. Load the module
         module load miniforge3/25.3.1-0

         #2a. Create "my_env" with Python version X.Y at the desired path
         conda create -p /path/to/my_env python=X.Y

         #2b. Create "my_env" with Python version X.Y with a specific name (defaults to $HOME directory)
         conda create --name my_env python=X.Y

         #3. Activate "my_env"
         conda activate /path/to/my_env

   .. tab-item:: Lux
      :sync: lux

      .. code-block:: bash

         #1. Load the module
         module load miniforge3/26.3.2-3

         #2a. Create "my_env" with Python version X.Y at the desired path
         conda create -p /path/to/my_env python=X.Y

         #2b. Create "my_env" with Python version X.Y with a specific name (defaults to $HOME directory)
         conda create --name my_env python=X.Y

         #3. Activate "my_env"
         conda activate /path/to/my_env

.. note::
   For users interested in sharing their environment, it is highly recommended
   to create new environments in the "Project Home" directory
   (``/ccs/proj/<project_id>/<user_id>``). This space avoids purges and allows for
   potential collaboration within your project. It is also recommended, for
   convenience, that you use environment names that indicate the hostname, as
   virtual environments created on one system will not necessarily work on others.

It is always recommended to deactivate an environment before activating a new one.
Deactivating an environment can be achieved through:

.. tab-set::

   .. tab-item:: Frontier
      :sync: frontier

      .. code-block:: bash

         # Deactivate the current environment
         conda deactivate

   .. tab-item:: Riker
      :sync: riker

      .. code-block:: bash

         # Deactivate the current environment
         conda deactivate

   .. tab-item:: Lux
      :sync: lux

      .. code-block:: bash

         # Deactivate the current environment
         conda deactivate


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
specifying ``python2`` or ``python3`` as a best practice, or specifying the
full path to your Python installation.

Before jumping into batch scripts, remember to check out the :ref:`python-mods`
section first, which details the differences between Python modules and 
environments on our different systems.

Batch Scripts
-------------

On Frontier, Riker, and Lux, you are already on a compute node once you are in a
batch job.  Therefore, you only need to use ``srun`` if you plan to run
parallel-enabled Python, and you *do not* need to specify ``srun`` if you are
running a serial application.

.. code-block:: bash

   sbatch submit.sl

.. warning::
    When submitting a batch script or interactive job with the default ``miniforge3``
    module previously loaded, your environment will be deactivated and you will be
    returned to the base environment at the start of your job. In order to run with
    your prepared environment, be sure to ``conda activate`` it again in your job.


An example batch script for is provided below:

.. tab-set::

   .. tab-item:: Frontier
      :sync: frontier

      .. code-block:: bash

         #!/bin/bash
         #SBATCH -A <PROJECT_ID>
         #SBATCH -J python
         #SBATCH -N 1
         #SBATCH -p batch
         #SBATCH -t 0:05:00

         cd $SLURM_SUBMIT_DIR
         date

         module load miniforge3/23.11.0-0
         conda activate my_env

         python3 script.py


   .. tab-item:: Riker
      :sync: riker

      .. code-block:: bash

         #!/bin/bash
         #SBATCH -A <PROJECT_ID>
         #SBATCH -J python
         #SBATCH -N 1
         #SBATCH -p batch
         #SBATCH --exclusive
         #SBATCH -t 0:05:00

         cd $SLURM_SUBMIT_DIR
         date

         module load miniforge3/25.3.1-0
         conda activate my_env

         python3 script.py

      .. note::
          Here, ``--exclusive`` is used as an example. For guidelines on submitting shared-node jobs on Riker, please see the :ref:`riker-user-guide`.

   .. tab-item:: Lux
      :sync: lux

      .. code-block:: bash

         #!/bin/bash
         #SBATCH -A <PROJECT_ID>
         #SBATCH -J python
         #SBATCH -N 1
         #SBATCH -p batch
         #SBATCH --exclusive
         #SBATCH -t 0:05:00

         cd $SLURM_SUBMIT_DIR
         date

         module load miniforge3/26.3.2-3
         conda activate my_env

         python3 script.py

      .. note::
          Here, ``--exclusive`` is used as an example. For guidelines on submitting shared-node jobs on Lux, please see the :ref:`lux-user-guide`.


Interactive Jobs
----------------

To use Python in an interactive session:

.. tab-set::

   .. tab-item:: Frontier
      :sync: frontier

      .. code-block:: bash

         salloc -A <PROJECT_ID> -N 1 -t 0:05:00
         module load miniforge3/23.11.0-0
         conda activate my_env
         python3 script.py

   .. tab-item:: Riker
      :sync: riker

      .. code-block:: bash

         salloc -A <PROJECT_ID> -N 1 -t 0:05:00 -p batch --exclusive
         module load miniforge3/25.3.1-0
         conda activate my_env
         python3 script.py

      .. note::
          Here, ``--exclusive`` is used as an example. For guidelines on submitting shared-node jobs on Riker, please see the :ref:`riker-user-guide`.

   .. tab-item:: Lux
      :sync: lux

      .. code-block:: bash

         salloc -A <PROJECT_ID> -N 1 -t 0:05:00 -p batch --exclusive
         module load miniforge3/26.3.2-3
         conda activate my_env
         python3 script.py

      .. note::
          Here, ``--exclusive`` is used as an example. For guidelines on submitting shared-node jobs on Lux, please see the :ref:`lux-user-guide`.

When in an interactive job, if you want to use an interactive Python prompt and
``srun`` at the same time, use the ``--pty`` flag (useful when running with multiple tasks):

.. code-block:: bash

   srun --pty python3


.. _python-best-pract:

Best Practices
==============

* **Do not run conda activate or conda init**:

    When using the conda modules, do **NOT** run ``conda init``. This will end
    up hard-coding a conda installation into your shell configuration file (e.g.,
    ``.bashrc``, ``.bash_profile``, etc.) and could cause problems when switching
    between HPC systems.  If you have a code-block in your configuration file
    starting with ``>>> conda initialize >>>``, it is recommended to delete the entire block.
    Ignore any "deprecation" or "deprecated" messages about ``source activate``.

* **Specify or check your Python path**:

    It is always best to explicitly indicate which Python environment you're
    using before running scripts.  This can be done by using ``#!/path/to/your/python3``
    lines at the top of your Python scripts, by passing the Python path at
    execution time, or - at the very least - checking which environment you're in like so:

    .. code-block:: bash

       echo "Using this Python environment: $(which python3)"

    Having a line similar to the above in your batch scripts may help diagnose
    compute jobs that may be using the wrong environment.

* **Cloning an environment using conda**:

    If there is an existing environment you would like to use but want to
    modify without affecting the original, you can clone the environment for
    yourself and install packages into the clone.  To clone an environment, you
    must use the ``--clone <env_to_clone>`` flag when creating a new conda
    environment. An example for cloning the base environment into a specific
    directory called ``envs/frontier/`` in your "Project Home" on NFS is provided below:

    .. code-block:: bash

       conda create -p /ccs/proj/<project_id>/<user_id>/envs/frontier/baseclone-frontier --clone base
       conda activate /ccs/proj/<project_id>/<user_id>/envs/frontier/baseclone-frontier

* **Cloning the "base environment" using venv**:

    .. code-block:: bash

       python3 -m venv /path/to/new_env --system-site-packages

* **Environment locations (storage)**:

    For certain packages, having environments stored on NFS instead of a
    system's parallel filesystem (like Alpine or Orion) may cause performance issues.
    If you see slow initialization times, it may be worth creating your environment
    on the parallel filesystem instead (is subject to purge policies).

    For running Python at scale on Frontier, it may be worth moving your
    virtual environment to the NVMe Burst Buffer using ``sbcast`` (see our
    :doc:`/software/python/sbcast_conda` guide for more details).
    In general NVMe > Orion >> NFS on Frontier.

* **Adding known conda environment locations**:

    For a conda environment to be callable by a "name", it must be installed in
    one of the ``envs_dirs`` directories. The list of known directories can be seen
    by executing:

    .. code-block:: bash

       $ conda config --show envs_dirs

    On OLCF systems, the default location is your ``$HOME`` directory.  If you
    plan to frequently create environments in a different location other than the
    default (such as ``/ccs/proj/...``), then there is an option to add directories
    to the ``envs_dirs`` list.
  
    For example, to track conda environments in a subdirectory called ``frontier``
    in Project Home you would execute:

    .. code-block:: bash

       conda config --append envs_dirs /ccs/proj/<project_id>/<user_id>/envs/frontier

    This will create a ``.condarc`` file in your ``$HOME`` directory if you do not have
    one already, which will now contain this new envs_dirs location.  This will now
    enable you to use the ``--name env_name`` flag when using conda commands for
    environments stored in the ``frontier`` directory, instead of having to use the
    ``-p /ccs/proj/<project_id>/<user_id>/envs/frontier/env_name``
    flag and specifying the full path to the environment.  For example, you can do
    ``conda activate my_env`` instead of ``conda activate
    /ccs/proj/<project_id>/<user_id>/envs/frontier/my_env``.

* **Make note of and clean your pip cache location**:

    To avoid quota issues, it is highly recommended to occasionally clean your
    ``pip`` cache location.

    * To find where your cache location is, use:

        .. code-block:: bash

           pip cache info

    * To clean your cache, use:

        .. code-block:: bash

           pip cache purge

* **Clean your conda cache**:

    To avoid quota issues, it is highly recommended to occasionally clean your
    ``conda`` cache location (in your ``.conda`` directory). To do so, run:

    .. code-block:: bash

       conda clean -a

* **Deactivate your environments before running batch jobs**:

    To avoid ``$PATH`` issues, it is highly recommended to submit batch jobs or
    enter interactive jobs without an already activated environment -- so,
    deactivating your environment is recommended. Alternatively, you can submit
    your jobs from a fresh login shell.

* **Unbuffered input**:

    To enable unbuffered input when running Python jobs or scripts on our
    systems, it is recommended to use the ``-u`` flag. For example: 

    .. code-block:: bash

       python3 -u script.py


Additional Resources
====================

* `pip User Guide <https://pip.pypa.io/en/stable/user_guide/>`__
* `venv Documentation <https://docs.python.org/3/tutorial/venv.html>`__
* `Conda User Guide <https://docs.conda.io/projects/conda/en/latest/index.html>`__
* `Conda-forge Package List <https://conda-forge.org/packages/>`__
* `Using Pip In A Conda Environment <https://www.anaconda.com/blog/using-pip-in-a-conda-environment>`__

