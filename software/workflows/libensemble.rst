.. _workflows-libensemble:

***********
libEnsemble
***********


Overview
========

`libEnsemble <https://github.com/Libensemble/libensemble>`__ is a complete :ref:`Python<py-index>` toolkit for
steering dynamic ensembles of calculations. Workflows are highly portable and detect/integrate heterogeneous
resources with little effort. For instance, libEnsemble can automatically detect, assign, and reassign allocated
processors and GPUs to ensemble members.

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
see this `Simple Tutorial <https://libensemble.readthedocs.io/en/main/tutorials/local_sine_tutorial.html>`__
on libEnsemble's `documentation <https://libensemble.readthedocs.io/en/main/index.html>`__.

For an example that runs a small ensemble with an application that offloads work to a GPU, see
this `GPU App Tutorial <https://libensemble.readthedocs.io/en/main/tutorials/forces_gpu_tutorial.html>`__.

Additional information on compiling/running the above sample GPU app is available `here <https://libensemble.readthedocs.io/en/main/platforms/frontier.html#example>`__.

See `this video <https://www.youtube.com/watch?v=H2fmbZ6DnVc>`__ for an example dynamic-resources workflow on Frontier.

Example Code
============

.. code-block:: python
  :linenos:

  import numpy as np

  from libensemble import Ensemble
  from libensemble.gen_funcs.sampling import uniform_random_sample
  from libensemble.sim_funcs.six_hump_camel import six_hump_camel
  from libensemble.specs import ExitCriteria, GenSpecs, SimSpecs
  from libensemble.tools import add_unique_random_streams

  if __name__ == "__main__":

      sampling = Ensemble(parse_args=True)
      sampling.sim_specs = SimSpecs(
          sim_f=six_hump_camel,
          inputs=["x"],
          outputs=[("f", float)],
      )

      sampling.gen_specs = GenSpecs(
          gen_f=uniform_random_sample,
          outputs=[("x", float, (2,))],
          user={
              "gen_batch_size": 500,
              "lb": np.array([-3, -2]),
              "ub": np.array([3, 2]),
          },
      )

      sampling.persis_info = add_unique_random_streams({}, sampling.nworkers + 1)
      sampling.exit_criteria = ExitCriteria(sim_max=101)
      sampling.run()
      sampling.save_output(__file__)

      if sampling.is_manager:
          print("Some output data:\n", sampling.H[["x", "f"]][:10])


Job Submission
==============

Upon initialization, libEnsemble will detect available nodes and GPUs from the Slurm environment, and 
allocate those resources towards application-launches.

Start an interactive session::

  $ salloc --nodes=2 -A <project_id> --time=00:10:00

Within the session (``multiprocessing`` comms, all processes on first node)::

  $ python my_libensemble_script.py --comms local --nworkers 9

