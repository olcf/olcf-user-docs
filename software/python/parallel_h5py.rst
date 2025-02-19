**************************
Installing mpi4py and h5py
**************************

.. note::
   For ``venv`` users only interested in installing ``mpi4py``, the ``pip``
   command in this guide is still accurate.

Overview
========

This guide teaches you how to build a personal, parallel-enabled version of h5py and how to write an HDF5 file in parallel using mpi4py and h5py.

In this guide, you will: 

* Learn how to install mpi4py
* Learn how to install parallel h5py
* Test your build with Python scripts

OLCF Systems this guide applies to: 

* :doc:`Frontier </systems/frontier_user_guide>`
* :doc:`Andes </systems/andes_user_guide>`

**Guide last tested with:**

+------------+----------+------------+
| ``python`` | ``h5py`` | ``mpi4py`` |
+============+==========+============+
|  3.11.11   |  3.13.0  |   4.0.3    |
+------------+----------+------------+

.. note::
   Working installations are **not** limited to what is shown above.
   Versions listed in the above table are what was tested most recently.

Parallel HDF5
=============

Scientific simulations generate large amounts of data (about 100 Terabytes per day for some applications).
Because of how large some datafiles may be, it is important that writing and reading these files is done as fast as possible.
Less time spent doing input/output (I/O) leaves more time for advancing a simulation or analyzing data.

One of the most utilized file types is the Hierarchical Data Format (HDF), specifically the HDF5 format.
`HDF5 <https://www.hdfgroup.org/solutions/hdf5/>`__ is designed to manage large amounts of data and is built for fast I/O processing and storage.
An HDF5 file is a container for two kinds of objects: "datasets", which are array-like collections of data, and "groups", which are folder-like containers that hold datasets and other groups.

There are various tools that allow users to interact with HDF5 data, but we will be focusing on `h5py <https://docs.h5py.org/en/stable/>`__ -- a Python interface to the HDF5 library.
h5py provides a simple interface to exploring and manipulating HDF5 data as if they were Python dictionaries or NumPy arrays.
For example, you can extract specific variables through slicing, manipulate the shapes of datasets, and even write completely new datasets from external NumPy arrays.

Both HDF5 and h5py can be compiled with MPI support, which allows you to optimize your HDF5 I/O in parallel.
MPI support in Python is accomplished through the `mpi4py <https://mpi4py.readthedocs.io/en/stable/>`__ package, which provides complete Python bindings for MPI.
Building h5py against mpi4py allows you to write to an HDF5 file using multiple parallel processes, which can be helpful for users handling large datasets in Python.
h5Py is available after loading the default Python module on either Frontier or Andes, but it has not been built with parallel support.

Setting Up the Environment
==========================

.. warning::
   Before setting up your environment, you must exit and log back in so that you have a fresh login shell.
   This is to ensure that no previously activated environments exist in your ``$PATH`` environment variable.

Building h5py from source is highly sensitive to the current environment variables set in your profile.
Because of this, it is extremely important that all the modules and environments you plan to load are done in the correct order, so that all the environment variables are set correctly.

First, load the gnu compiler module (most Python packages assume GCC), hdf5 module (necessary for h5py), and the python module (allows you to create a new environment):

.. tab-set::

   .. tab-item:: Andes
      :sync: andes

      .. code-block:: bash

         module load gcc/9.3.0
         module load hdf5/1.10.7
         module load miniforge3/23.11.0-0

   .. tab-item:: Frontier
      :sync: frontier

      .. code-block:: bash

         module load PrgEnv-gnu/8.6.0
         module load cray-hdf5-parallel/1.12.2.11
         module load miniforge3/23.11.0-0

.. note::
   If you're just interested in ``mpi4py`` and not ``h5py``, then you don't need to load the ``hdf5`` module.

Loading a python module puts you in a "base" environment, but you need to create a new environment using the ``conda create`` command:

.. tab-set::

   .. tab-item:: Andes
      :sync: andes

      .. code-block:: bash

         conda create -n h5pympi-andes python=3.11 numpy -c conda-forge

   .. tab-item:: Frontier
      :sync: frontier

      .. code-block:: bash

         conda create -n h5pympi-frontier python=3.11 numpy -c conda-forge

NumPy is installed ahead of time because h5py depends on it.

After following the prompts for creating your new environment, you can now activate it:

.. tab-set::

   .. tab-item:: Andes
      :sync: andes

      .. code-block:: bash

         source activate h5pympi-andes

   .. tab-item:: Frontier
      :sync: frontier

      .. code-block:: bash

         source activate h5pympi-frontier


Installing mpi4py
=================

Now that you have a fresh environment, you will next install mpi4py into your new environment using ``pip``:

.. tab-set::

   .. tab-item:: Andes
      :sync: andes

      .. code-block:: bash

         MPICC="mpicc -shared" pip install --no-cache-dir --no-binary=mpi4py mpi4py

   .. tab-item:: Frontier
      :sync: frontier

      .. code-block:: bash

         MPICC="cc -shared" pip install --no-cache-dir --no-binary=mpi4py mpi4py

The ``MPICC`` flag ensures that you are using the correct C wrapper for MPI on the system.
If everything goes well, you should see a "Successfully installed mpi4py" message.

Installing h5py
===============

Next, install h5py:

.. tab-set::

   .. tab-item:: Andes
      :sync: andes

      .. code-block:: bash

         HDF5_MPI="ON" CC=mpicc HDF5_DIR=${OLCF_HDF5_ROOT} pip install --no-cache-dir --no-binary=h5py h5py

   .. tab-item:: Frontier
      :sync: frontier

      .. code-block:: bash

         HDF5_MPI="ON" CC=cc HDF5_DIR=${HDF5_ROOT} pip install --no-cache-dir --no-binary=h5py h5py

The ``HDF5_MPI`` flag is the key to telling pip to build h5py with parallel support, while the ``CC`` flag makes sure that you are using the correct C wrapper for MPI.
When the installation finishes, you will see a "Successfully installed h5py" message.

Testing parallel h5py
=====================

Test your build by trying to write an HDF5 file in parallel using 42 MPI tasks.

First, change directories to your scratch area:

.. code-block:: bash

   cd $MEMBERWORK/<YOUR_PROJECT_ID>
   mkdir h5py_test
   cd h5py_test

Let's test that mpi4py is working properly first by executing the example Python script "hello_mpi.py":

.. code-block:: python

   # hello_mpi.py
   from mpi4py import MPI

   comm = MPI.COMM_WORLD      # Use the world communicator
   mpi_rank = comm.Get_rank() # The process ID (integer 0-41 for a 42-process job)

   print('Hello from MPI rank %s !' %(mpi_rank))

To do so, submit a job to the batch queue:

.. tab-set::

   .. tab-item:: Andes
      :sync: andes

      .. code-block:: bash

         sbatch --export=NONE submit_hello.sl

   .. tab-item:: Frontier
      :sync: frontier

      .. code-block:: bash

         sbatch --export=NONE submit_hello.sl


Example "submit_hello" batch script:

.. tab-set::

   .. tab-item:: Andes
      :sync: andes

      .. code-block:: bash

         #!/bin/bash
         #SBATCH -A <PROJECT_ID>
         #SBATCH -J mpi4py
         #SBATCH -N 1
         #SBATCH -p gpu
         #SBATCH -t 0:05:00

         # Only necessary if submitting like: sbatch --export=NONE ... (recommended)
         # Do NOT include this line when submitting without --export=NONE
         unset SLURM_EXPORT_ENV

         cd $SLURM_SUBMIT_DIR
         date

         module load gcc/9.3.0
         module load hdf5/1.10.7
         module load miniforge3/23.11.0-0

         source activate h5pympi-andes

         srun -n42 python3 hello_mpi.py

   .. tab-item:: Frontier
      :sync: frontier

      .. code-block:: bash

         #!/bin/bash
         #SBATCH -A <PROJECT_ID>
         #SBATCH -J mpi4py
         #SBATCH -N 1
         #SBATCH -p batch
         #SBATCH -t 0:05:00

         # Only necessary if submitting like: sbatch --export=NONE ... (recommended)
         # Do NOT include this line when submitting without --export=NONE
         unset SLURM_EXPORT_ENV

         cd $SLURM_SUBMIT_DIR
         date

         module load PrgEnv-gnu/8.6.0
         module load cray-hdf5-parallel/1.12.2.11
         module load miniforge3/23.11.0-0

         source activate h5pympi-frontier

         srun -n42 python3 hello_mpi.py

If mpi4py is working properly, in ``mpi4py.<JOB_ID>.out`` you should see output similar to:

.. code-block::

   Hello from MPI rank 21 !
   Hello from MPI rank 23 !
   Hello from MPI rank 28 !
   Hello from MPI rank 40 !
   Hello from MPI rank 0 !
   Hello from MPI rank 1 !
   Hello from MPI rank 32 !
   .
   .
   .

If you see this, great, it means that mpi4py was built successfully in your environment.

Finally, let's see if you can get these tasks to write to an HDF5 file in parallel using the "hdf5_parallel.py" script:

.. code-block:: python

   # hdf5_parallel.py
   from mpi4py import MPI
   import h5py

   comm = MPI.COMM_WORLD      # Use the world communicator
   mpi_rank = comm.Get_rank() # The process ID (integer 0-41 for a 42-process job)
   mpi_size = comm.Get_size() # Total amount of ranks

   with h5py.File('output.h5', 'w', driver='mpio', comm=MPI.COMM_WORLD) as f:
       dset = f.create_dataset('test', (42,), dtype='i')
       dset[mpi_rank] = mpi_rank

   comm.Barrier()

   if (mpi_rank == 0):
       print('42 MPI ranks have finished writing!')

The MPI tasks are going to write to a file named "output.h5", which contains a dataset called "test" that is of size 42 (assigned to the "dset" variable in Python).
Each MPI task is going to assign their rank value to the "dset" array in Python, so you should end up with a dataset that contains 0-41 in ascending order.

Time to execute "hdf5_parallel.py" by submitting "submit_h5py" to the batch queue:

.. tab-set::

   .. tab-item:: Andes
      :sync: andes

      .. code-block:: bash

         sbatch --export=NONE submit_h5py.sl

   .. tab-item:: Frontier
      :sync: frontier

      .. code-block:: bash

         sbatch --export=NONE submit_h5py.sl

Example "submit_h5py" batch script:

.. tab-set::

   .. tab-item:: Andes
      :sync: andes

      .. code-block:: bash

         #!/bin/bash
         #SBATCH -A <PROJECT_ID>
         #SBATCH -J h5py
         #SBATCH -N 1
         #SBATCH -p gpu
         #SBATCH -t 0:05:00

         # Only necessary if submitting like: sbatch --export=NONE ... (recommended)
         # Do NOT include this line when submitting without --export=NONE
         unset SLURM_EXPORT_ENV

         cd $SLURM_SUBMIT_DIR
         date

         module load gcc/9.3.0
         module load hdf5/1.10.7
         module load miniforge3/23.11.0-0

         source activate h5pympi-andes

         srun -n42 python3 hdf5_parallel.py

   .. tab-item:: Frontier
      :sync: frontier

      .. code-block:: bash

         #!/bin/bash
         #SBATCH -A <PROJECT_ID>
         #SBATCH -J h5py
         #SBATCH -N 1
         #SBATCH -p batch
         #SBATCH -t 0:05:00

         # Only necessary if submitting like: sbatch --export=NONE ... (recommended)
         # Do NOT include this line when submitting without --export=NONE
         unset SLURM_EXPORT_ENV

         cd $SLURM_SUBMIT_DIR
         date

         module load PrgEnv-gnu/8.6.0
         module load cray-hdf5-parallel/1.12.2.11
         module load miniforge3/23.11.0-0

         source activate h5pympi-frontier

         srun -n42 python3 hdf5_parallel.py


Provided there are no errors, you should see "42 MPI ranks have finished writing!" in your output file, and there should be a new file called "output.h5" in your directory.
To see explicitly that the MPI tasks did their job, you can use the ``h5dump`` command to view the dataset named "test" in output.h5:

.. code-block:: bash

   $ h5dump output.h5

   HDF5 "output.h5" {
   GROUP "/" {
      DATASET "test" {
         DATATYPE  H5T_STD_I32LE
         DATASPACE  SIMPLE { ( 42 ) / ( 42 ) }
         DATA {
         (0): 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
         (19): 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34,
         (35): 35, 36, 37, 38, 39, 40, 41
         }
      }
   }
   }

If you see the above output, then the build was a success!

Additional Resources
====================

* `h5py Documentation <https://docs.h5py.org/en/stable/>`__
* `mpi4py Documentation <https://mpi4py.readthedocs.io/en/stable/>`__
* `HDF5 Support Page <https://support.hdfgroup.org/>`__
