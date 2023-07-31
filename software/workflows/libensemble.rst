.. _workflows-libensemble:

***********
libEnsemble
***********


Overview
========

libEnsemble is a complete :ref:`Python<py-index>` toolkit for steering dynamic ensembles of calculations. 
Workflows are highly portable and detect/integrate heterogeneous resources with little effort. For instance,
libEnsemble can automatically detect, assign, and reassign allocated GPUs to ensemble members.

Users select or supply **generator** and **simulator** functions to express their ensembles; the generator
typically steers the ensemble based on prior simulator results. Such functions can also launch and monitor
external executables at any scale.


Installation
============

Begin by loading the ``python`` module::

  $ module load cray-python

libEnsemble is available on `PyPI <https://pypi.org/>`__, `conda-forge <https://conda-forge.org/>`__,
`the xSDK <https://xsdk.info/>`__, and `E4S <https://e4s-project.github.io/>`__. Most users install libEnsemble
via ``pip``::

  $ pip install libensemble

Installing libEnsemble in a virtual environment is highly recommended. See the :ref:`Python on OCLF Systems<py-index>` page 
for more information.

Examples
========

For a very simple example of using libEsemble 
see the `Simple Sine Tutorial <https://libensemble.readthedocs.io/en/main/tutorials/local_sine_tutorial.html>`__
on libEnsemble's `documentation <https://libensemble.readthedocs.io/en/main/index.html>`__.

For an example that runs a small ensemble with an application that offloads work to a GPU, see
this `GPU App Tutorial <https://libensemble.readthedocs.io/en/main/tutorials/forces_gpu_tutorial.html>`__.

Additional information on compiling/running the above sample GPU app is available `here <https://libensemble.readthedocs.io/en/main/platforms/frontier.html#example>`__.

Example Code
============

.. code-block:: python

    import numpy as np
    from tutorial_gen import gen_random_sample
    from tutorial_sim import sim_find_sine

    from libensemble.libE import libE
    from libensemble.tools import add_unique_random_streams

    libE_specs = {"nworkers": 4, "comms": "local"}

    gen_specs = {
        "gen_f": gen_random_sample,  # Our generator function
        "out": [("x", float, (1,))],  # gen_f output (name, type, size).
        "user": {
            "lower": np.array([-3]),  # random sampling lower bound
            "upper": np.array([3]),  # random sampling upper bound
            "gen_batch_size": 5,  # number of values gen_f will generate per call
        },
    }

    sim_specs = {
        "sim_f": sim_find_sine,  # Our simulator function
        "in": ["x"],  # Input field names. 'x' from gen_f output
        "out": [("y", float)],  # sim_f output. 'y' = sine('x')
    }

    persis_info = add_unique_random_streams({}, 5)  # Initialize manager/workers random streams

    exit_criteria = {"sim_max": 80}  # Stop libEnsemble after 80 simulations

    H, persis_info, flag = libE(sim_specs, gen_specs, exit_criteria, persis_info, libE_specs=libE_specs)


Job Submission
==============

libEnsemble can run on/across the compute nodes of Frontier using either Python's ``multiprocessing``
or MPI via ``mpi4py``. libEnsemble will detect available nodes and GPUs from the Slurm environment.

Start an interactive session::

  $ salloc --nodes=2 -A <project_id> --time=00:10:00

Within the session (``multiprocessing``, all processes on first node)::

  $ python my_libensemble_script.py --comms local --nworkers 8

Or (MPI, processes distributed)::

  $ srun -n 8 --ntasks-per-node=4 python my_libensemble_script.py