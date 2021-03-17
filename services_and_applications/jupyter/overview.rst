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

All members of currently enabled OLCF projects have access to the OLCF JupyterHub and JupyterLab.

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


Working within GPFS and NFS (Launching a notebook)
--------------------------------------------------

To see the root of your filesystem access, within your JupyterLab interface, click this circled folder (you can traverse to your users spaces from there):

.. image:: /images/jupyter/directory_access.png

You should see **gpfs** and **ccs** - the "top" of GPFS amd NFS respectively.

Then, you can start a notebook in the directory of your choosing (relative to your user access). 

To do so, traverse the filesystem to your desired path and then click the "Python 3" notebook in the launcher page. This will launch the default notebook environment and store the notebook in your current path. 

**NOTE:  Any notebooks saved in the root location won't be persisted across sessions. Make sure you are saving your work in a location in /ccs or /gpfs where you have write access.**

In the example image below, I have launched a notebook in my **/ccs/proj/<proj>/<uid>/** directory (the notebook filename is "Untitled.ipynb" - you can rename yours):

.. image:: /images/jupyter/directory_example.png

Another method of getting to the filesystem path of your choosing is selecting **File->"Open from Path"** and typing the desired path in the text box:

.. image:: /images/jupyter/open_file_path.png


Conda environments and custom notebooks
---------------------------------------

The base environment provides a few common data analysis libraries by default, including
Pytorch, Numpy, Pandas, Bokeh, Seaborn etc. To see the full list, open the Terminal from
the Launcher and type ``conda list``. The libraries in the base environment should
cover most use cases. This base environment is provided to the default "Python 3" notebook, visible in the 
JupyterLab "Launcher" page.

From the Jupyter Terminal, you can install additional libraries with a simple ``conda install`` to
use in your current session. But these installed libraries won't persist across sessions
if your server is restarted.

Since conda's dependency concretizer has sometimes problems to extend existing environments with new
libraries, you can also use the `mamba <https://github.com/mamba-org/mamba>`__ package manager. Just
install it with ``conda install -c conda-forge mamba`` and replace ``conda`` with ``mamba`` calls.


Creating your own Conda environment and notebook entry
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Setting up your own custom Conda environment is useful when the base environment doesn't provide what
you need and you want your installed libraries to persist across sessions. These custom
Conda environments need to be saved in a ``/ccs`` or ``/gpfs/alpine`` directory.

**NOTE**: Please note that **GPFS is purged**. Using /ccs/proj/ is recommended

Let us look at an example, which creates a custom environment that has RAPIDS installed (https://rapids.ai/start.html).

At the end of this example you will have a "rapids" notebook visible in the JuptyerLab "Launcher" page. We will make the RAPIDS environment persistent by 
building it at /ccs/proj/<YOUR_UID>/rapids. 


Example: Creating a Conda environment for RAPIDS
=================================================

#. From the Launcher page in JupyterLab, click on Terminal.
#. Create a conda environment with ``conda create -p /ccs/proj/<YOUR_PROJECT_ID>/<YOUR_UID>/rapids -c rapidsai -c nvidia -c conda-forge \``
   ``-c defaults rapids-blazing=0.17 python=3.7 cudatoolkit=10.2``
   
     * **NOTE**: The ``conda create`` command above **assumes you are using** ``CUDA 10`` JuptyerLab environment.
   
     * You need to use ``-p`` method if you want your environment to persist across Jupyter
       restarts. The path can be a location in ``/ccs`` or ``/gpfs/alpine`` that is writable
       by your user.
     
#. Activate the environment ``source activate /ccs/proj/<YOUR_PROJECT_ID>/<YOUR_UID>/rapids``.

     * **NOTE**: It is **recommended to use** ``source activate`` instead of ``conda activate``, even though
       the ``conda create`` process recommends ``conda activate`` at it's completion. Using ``conda activate`` requires modification
       of the ``.bashrc`` file, which is not covered here. 
   
#. After activating, to make your created environment visible in JupyterLab, run ``python -m
   ipykernel install --user --name rapids --display-name rapids``. A
   kernelspec is created in your ``/ccs/home/<YOUR_UID>/.local/share/jupyter`` directory which
   JupyterLab reads to see which custom environments are available for it to use.
  
     * When you refresh the page and look at the Launcher, you will see buttons labelled
       ``rapids``. Clicking it will start a Notebook or Console running in your
       ``rapids`` environment.

   
   .. image:: /images/jupyter/rapids_notebook_image.png
     

#. Now open a ``rapids`` notebook to check if the installation was successful. In the below image, I created a notebook called *rapids-test* in my NFS 
   project space and did a very basic cuDF operation on some example data (in  the red circle, you can see I am using the created "rapids" environment/kernel):

   
   ..  image:: /images/jupyter/cudf_rapids_test.png


#. If restart the server or lose your session, you will see that the ``rapids`` Notebook and Console
   buttons are still available after coming back. 
#. You can always install more libraries into your Conda environment as needed by opening
   the Terminal in JupyterLab again, activating the environment with ``source activate``
   and doing ``conda install`` or ``pip install``.


To delete your environment, you will need to delete it from the path where the environment
was created, as well as delete the corresponding directory from ``~/.local/share/jupyter/kernels``.

You may follow these general steps to create and install packages within an any environment you decide to create. The main componentes to accomplish this, using a terminal session, are: 
 
 - *conda create -p /path/to/env*
 - *source activate /path/to/env*
 - *python -m ipykernel install --user --name <env-name> --display-name <env-name>*
 - *install packages with conda or pip in the activate environment*


Manually stopping your JupyterLab session
-----------------------------------------

All JupyterLab sessions expire and termninate if they are left idle for an 1-hour. 

If you would like to terminate your session manually though, to select a different JupyterLab image for instance (going from CPU to GPU-enabled, or vice versa), you can do so by going to **File -> Hub Control Panel -> Stop Server**. 

This will take a few seconds to shutdown, then you can restart and reselect a provided JupyterLab image from the menu.

Things to be aware of
---------------------

- All notebooks have an idle time limit of 1-hour. After 1-hour of idle time, your JupyterLab session will terminate. You may restart your session though.
- To persist a notebook and conda environment, it is highly recommended to use your NFS project space (/ccs/proj/<project-id>/<uid>/).
- The GPU-labs are limited resources. There is no guarantee of a GPU being readily available for JupyterLab. Please use the more readily accessible CPU-Labs, unless you absolutely need a GPU.

Example Jupyter Notebooks
-------------------------

Please check out our OLCF `Jupyter-Examples <https://github.com/olcf/jupyter-examples>`__ repository on GitHub.
