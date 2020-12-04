.. _jupyter_overview:

**************************
Overview
**************************


Jupyter at OLCF
---------------

Jupyter is a powerful tool enabling reproducible research and teaching. Use it to create notebooks that contain both computer code and rich text elements (paragraphs, equations, figures, widgets, links). This allows you to create human-readable documents containing executable data analytics components, results, and descriptions.

JupyterLab
^^^^^^^^^^

JupyterLab is a web-based interactive development environment for Jupyter. It provide a way to use notebooks, text editors, terminals, and custom components together. You can configure and arrange the user interface to support a wide range of workflows in data science, scientific computing, and machine learning. 

The OLCF JupyterHub implementation will spawn you into a single-user JupyterLab environment.


Jupyter Hub
^^^^^^^^^^^

JupyterHub is the best way to serve Jupyter Labs for multiple users within a project. It is a multi-user Hub that spawns, manages, and proxies multiple selectable instances of the single-user JupyterLab server.

JupyterHub within OLCF works by first authenticating each user using NCCS LDAP authentication. The Hub will offer each user a selection of Lab images to launch, which will then be spun up automatically. Upon successfull authentication, your UID/GID/Groups are queried and built into the deployment of your personal JupyterLab. In addition, you will have access to your standard OLCF storage space(s) on NFS and GPFS.

Access
------

OLCF JupyterHub link: `https://jupyter.olcf.ornl.gov/ <https://jupyter.olcf.ornl.gov/>`__

The above link will present you with the page below. Please login with your OLCF account and PASSCODE.

.. image:: /images/jupyter/login.png


After succesfull authentication you will be presented with a choice of JupyterLab images (similar to the image below):

- CPU-Only
- GPU-Lab(s) with varying CUDA version

**NOTE: These GPU-enabled labs are limited. You may get get a message saying the resource is not schedulable, if all GPUs in the pool are occupied.**


.. image:: /images/jupyter/jupyterlab_images.png

**Select the lab you would like and click "Start".**

Once inside a lab, you will be presented with the default notebook/environment in the "launcher" page of the JupyterLab interface. You can read about the default environment more, below, in the "Conda Environments" section. In addtion, that section will show you how to create your own Conda Environments.

Once inside the JupyterLab, please take a moment to explore the interface.

To read more about the JupyterLab interface, in general, please check out this wonderful documentation: `JupyterLab Docs <https://jupyterlab.readthedocs.io/en/stable/user/interface.html>`__


CPU vs. GPU JupyterLab (Available Resources)
--------------------------------------------

Each single-user JupyterLab, spawned by OLCF's JupyterHub, gets these default resources:

- 16 CPU's
- 32GB Memory
- NCCS filesystem access (GPFS and NFS)

**NOTE: You have the same filesystem access as if you were on Summit, to both NFS and GPFS, as you will be working under your standard OLCF UID.**

The CPU-only JupyterLab is limited to the above resources.

The GPU-enabled JupyterLab will launch a notebook onto a resource containing a GPU (in addtion to the above resources). This allows you to experiment with GPU-enabled anaylytics from JupyterLab.

**NOTE: These GPU-enabled labs are limited. You may get get a message saying the resource is not schedulable, if all GPUs in the pool are occupied.**


Working within GPFS and NFS
---------------------------

To see the root of your filesystem access, within your JupyterLab interface, click this circled folder (you can traverse to your users spaces from there):

.. image:: /images/jupyter/directory_access.png

You should see **gpfs** and **ccs** - the "top" of GPFS amd NFS respectively.

Then, you can start a notebook in the directory of your choosing (relative to your user access). In the example image below, I have launched a notebook in my **/ccs/proj/<proj>/<uid>/** directory:

.. image:: /images/jupyter/directory_example.png

Another method of getting to the filesystem path of your choosing is selecting **File->"Open from Path"** and typing the desired path in the text box:

.. image:: /images/jupyter/open_file_path.png


Conda Environments
------------------

The base environment provides a few common data analysis libraries by default, including
Pytorch, Numpy, Pandas, Bokeh, Seaborn etc. To see the full list, open the Terminal from
the Launcher and type ``conda list``. The libraries in the base environment should
cover most use cases.

From the Terminal, you can install additional libraries with a simple ``conda install`` to
use in your current session. But these installed libraries won't persist across sessions
if your server is restarted. 



Creating your own Conda environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Setting up your own custom Conda environment is useful when the base environment doesn't provide what
you need and you want your installed libraries to persist across sessions. These custom
Conda environments need to be saved in a ``/ccs`` or ``/gpfs/alpine`` directory.

**Please note that GPFS is purged. Using /ccs/proj/ is recommended**

Let us look at an example with creating a custom environment that has Tensorflow.


Example: Creating a Conda environment for Tensorflow
====================================================

#. From the Launcher page in JupyterLab, click on Terminal.
#. Create a conda environment with  ``conda create -p /path/to/tensorflowenv python=3.7
   ipykernel``.
   
   * You need to use ``-p`` method if you want your environment to persist across Jupyter
     restarts. The path can be a location in ``/ccs`` or ``/gpfs/alpine`` that is writable
     by your user.
     
#. Activate the environment ``source activate /path/to/tensorflowenv``.
   
#. After activating, to make your created environment visible in JupyterLab, run ``python -m
   ipykernel install --user --name tensorflowenv --display-name tensorflowenv``. A
   kernelspec is created in your ``/ccs/home/<user>/.local/share/jupyter`` directory which
   JupyterLab reads to see which custom environments are available for it to use.
  
   * When you refresh the page and look at the Launcher, you will see buttons labelled
     ``tensorflowenv``. Clicking it will start a Notebook or Console running in your
     ``tensorflowenv`` environment.
     
#. Back in our Terminal, with our environment still activated, install Tensorflow with
   ``conda install tensorflow`` (or ``pip install tensorflow`` for the latest
   version). Now open a ``tensorflowenv`` notebook and type ``import tensorflow`` to check
   if the installation was successful.
#. If you restart the server, you will see that the ``tensorflowenv`` Notebook and Console
   buttons are still available. 
#. You can always install more libraries into your Conda environment as needed by opening
   the Terminal in JupyterLab again, activating the environment with ``source activate``
   and doing ``conda install`` or ``pip install``.


To delete your environment, you will need to delete it from the path where the environment
was created, as well as delete the corresponding directory from ``~/.local/share/jupyter/kernels``.

Example Jupyter Notebooks
-------------------------

Please check out our OLCF `Jupyter-Examples <https://github.com/olcf/jupyter-examples>`__ repository on GitHub.
