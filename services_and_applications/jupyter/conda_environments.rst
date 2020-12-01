
Conda environments
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
