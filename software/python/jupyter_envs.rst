:tocdepth: 3

******************
Jupyter Visibility
******************

Instead of making conda environments on our :doc:`OLCF Jupyter Service </services_and_applications/jupyter/overview>` itself, it is highly recommended to create environments on the HPC systems themselves and then expose them to Jupyter.
This guide will walk you through how to create a custom environment that can then be used with Jupyter (both our service or a local installation).

OLCF Systems this guide applies to: 

* :doc:`Frontier </systems/frontier_user_guide>`
* :doc:`Riker </systems/riker_user_guide>`
* :doc:`Lux </systems/lux_user_guide>`

Making your Environment Visible to Jupyter
==========================================

Although this guide starts from a new environment, existing environments can follow the same steps (ignoring environment creation) to accomplish the same goal.

First, let's load the relevant Python module along with the gnu compiler module (most Python packages assume GCC during installation):

.. tab-set::

   .. tab-item:: Frontier
      :sync: frontier

      .. code-block:: bash

         module load PrgEnv-gnu/8.6.0
         module load miniforge3/23.11.0-0

   .. tab-item:: Riker
      :sync: riker

      .. code-block:: bash

         module load gcc/14.2
         module load miniforge3/25.3.1-0

   .. tab-item:: Lux
      :sync: lux

      .. code-block:: bash

         module load gcc/14.4.0
         module load miniforge3/26.3.2-3

Next, create your environment and activate it:

.. tab-set::

   .. tab-item:: Frontier
      :sync: frontier

      .. code-block:: bash

         conda create -p /path/to/your/jupyter_env_frontier python=3.13
         conda activate /path/to/your/jupyter_env_frontier

   .. tab-item:: Riker
      :sync: riker

      .. code-block:: bash

         conda create -p /path/to/your/jupyter_env_riker python=3.13
         conda activate /path/to/your/jupyter_env_riker

   .. tab-item:: Lux
      :sync: lux

      .. code-block:: bash

         conda create -p /path/to/your/jupyter_env_lux python=3.13
         conda activate /path/to/your/jupyter_env_lux

.. note::

   Installing Python version 3.13 was just used as an example and is not required.

Next, install ``ipykernel`` which we will use to install a "Kernel" of your environment so that it can be used on Jupyter:

.. tab-set::

   .. tab-item:: Frontier
      :sync: frontier

      .. code-block:: bash

         pip install ipykernel

   .. tab-item:: Riker
      :sync: riker

      .. code-block:: bash

         pip install ipykernel

   .. tab-item:: Lux
      :sync: lux

      .. code-block:: bash

         pip install ipykernel

Finally, let's use ``ipykernel`` to expose your environment to Jupyter:

.. tab-set:: 

   .. tab-item:: Frontier
      :sync: frontier

      .. code-block:: bash 

         ipython kernel install --user --name=jupyter_env_frontier

   .. tab-item:: Riker
      :sync: riker

      .. code-block:: bash

         ipython kernel install --user --name=jupyter_env_riker

   .. tab-item:: Lux
      :sync: lux

      .. code-block:: bash

         ipython kernel install --user --name=jupyter_env_lux

.. note::

   Alternatively, you can do something like ``python -m ipykernel install --user --name jupyter_env``

If successful, you should see something like ``Installed kernelspec jupyter_env in ~/.local/share/jupyter/kernels/jupyter_env``

That is the final step and you should now be able to use your custom environment's kernel on JupyterLab.
You can either choose to launch new notebooks on Jupyter with this kernel or switch the kernels of existing notebooks to this environment's kernel instead.

Note that if you ever need to delete the environment, you would also need to delete the corresponding kernel (e.g., ``~/.local/share/jupyter/kernels/jupyter_env``) to completely remove it from Jupyter's cache.

For more information on how to use OLCF's JupyterLab, please see :doc:`Jupyter at OLCF </services_and_applications/jupyter/overview>` page.
