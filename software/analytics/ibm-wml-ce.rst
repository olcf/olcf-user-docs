
*************************************************************************************
IBM Watson Machine Learning CE -> Open CE 
*************************************************************************************

Getting Started
===============

IBM Watson Machine Learning Community Edition (ibm-wml-ce) has been replaced by
Open-CE. The Open-CE environment is provided on Summit through the module
``open-ce``, which is built based on the `Open Cognitive Environment
<https://github.com/open-ce/open-ce>`_. Open-CE is a Python Anaconda
environment that is pre-loaded with many popular machine learning frameworks
and tuned to Summit's Power9+NVIDIA Volta hardware.

To access the latest analytics packages use the ``module load`` command:

.. code-block:: bash

    module load open-ce

Loading a specific version of the module is recommended to future-proof scripts
against software updates. The following commands can be used to find and load
specific module versions:

.. code-block:: bash

    [user@login2.summit ~]$ module avail open-ce

    ---------------------------------- /sw/summit/modulefiles/core -----------------------------------
    open-ce-olcf/1.5.2-py39-0         (D)    open-ce/1.5.0-py37-0    open-ce/1.5.2-py39-0
    open-ce-olcf/1.9.1-py39-ibm              open-ce/1.5.0-py38-0    open-ce/1.10.0-py39-ibm  (D)
    open-ce/1.4.0-py37-0                     open-ce/1.5.0-py39-0    open-ce/1.10.0-py311-ibm
    open-ce/1.4.0-py38-0                     open-ce/1.5.2-py37-0
    open-ce/1.4.0-py39-0                     open-ce/1.5.2-py38-0

    [user@login2.summit ~]$ module load open-ce/1.10.0-py39-ibm

As seen above, there are also different Python versions of each Open-CE release
available on Summit (indicated by ``-pyXY-`` in the module name, where "X" and
"Y" are the major and minor Python version numbers, respectively.)

.. note::

    For more information on loading modules, including loading specific verions,
    see: :ref:`environment-management-with-lmod`

Loading an Open-CE module will activate a conda environment which is pre-loaded
with the following packages, and their dependencies:

.. table::
    :widths: 20 40 40 40 40

    +--------------------+-----------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------+
    | Environment        | open-ce/1.4.0                                                                                 | open-ce/1.5.0                                                                                 | open-ce/1.5.2                                                                                 | open-ce/1.10.0                                                                                |
    +--------------------+-----------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------+
    | Package            | `Tensorflow 2.6.0 <https://github.com/open-ce/tensorflow-feedstock>`_                         | `Tensorflow 2.7.0 <https://github.com/open-ce/tensorflow-feedstock>`_                         | `Tensorflow 2.7.1 <https://github.com/open-ce/tensorflow-feedstock>`_                         | `Tensorflow 2.13.0 <https://github.com/open-ce/tensorflow-feedstock>`_                        |
    |                    +-----------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------+
    |                    | `PyTorch 1.9.0 <https://github.com/open-ce/pytorch-feedstock>`_                               | `PyTorch 1.10.0 <https://github.com/open-ce/pytorch-feedstock>`_                              | `PyTorch 1.10.2 <https://github.com/open-ce/pytorch-feedstock>`_                              | `PyTorch 2.0.1 <https://github.com/open-ce/pytorch-feedstock>`_                               |
    |                    +-----------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------+
    |                    | `Horovod 0.22.1 (NCCL Backend) <https://github.com/horovod/horovod>`_                         | `Horovod 0.23.0 (NCCL Backend) <https://github.com/horovod/horovod>`_                         | `Horovod 0.23.0 (NCCL Backend) <https://github.com/horovod/horovod>`_                         | `Horovod 0.28.0 (NCCL Backend) <https://github.com/horovod/horovod>`_                         |
    +--------------------+-----------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------+
    | Complete List      | `1.4.0 Software Packages <https://github.com/open-ce/open-ce/releases/tag/open-ce-v1.4.0>`_   | `1.5.0 Software Packages <https://github.com/open-ce/open-ce/releases/tag/open-ce-v1.5.0>`_   | `1.5.2 Software Packages <https://github.com/open-ce/open-ce/releases/tag/open-ce-v1.5.2>`_   | `1.10.0 Software Packages <https://github.com/open-ce/open-ce/releases/tag/open-ce-v1.10.0>`_ |
    +--------------------+-----------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------+

Comparing to IBM WML CE, `Open-CE <https://github.com/open-ce/open-ce>`_ no
longer has ``IBM DDL``, ``Caffe(IBM-enhanced)``, ``IBM SnapML``, ``Nvidia
Rapids, Apex`` packages, and TensorFlow and PyTorch are not compiled with IBM
Large Model Support (LMS). For standalone Keras users using Open-CE version
1.10.0, please ``pip install keras`` after ``module load open-ce``.

.. note::

    | WML-CE on Summit (`slides <https://www.olcf.ornl.gov/wp-content/uploads/2019/10/DDLonSummit.pdf>`__ | `recording <https://vimeo.com/377551223>`__) 
    | Scaling up deep learning application on Summit (`slides <https://www.olcf.ornl.gov/wp-content/uploads/2019/12/Scaling-DL-on-Summit.pdf>`__ | `recording <https://vimeo.com/391520479>`__) 
    | ML/DL on Summit (`slides <https://www.olcf.ornl.gov/wp-content/uploads/2020/02/MLDL-on-Summit-June2020.pdf>`__ | `recording <https://vimeo.com/427791205>`__)

Running Distributed Deep Learning Jobs
======================================

The IBM ``ddlrun`` tool has been deprecated. The recommended tool for
launching distributed deep learning jobs on Summit is ``jsrun``. When
launching distributed deep learning jobs the primary concern for most
distribution methods is that each process needs to have access to
all GPUs on the node it's running on. The following command should
correctly launch most DDL scripts:

``jsrun -r1 -g6 -a6 -c42 -bpacked:7  <SCRIPT>``

+----------------+------------------------------------------------------+
| Flags          |  Description                                         |
+================+======================================================+
| ``-r1``        | 1 resource set per host                              |
+----------------+------------------------------------------------------+
| ``-g6``        | 6 GPUs per resource set                              |
+----------------+------------------------------------------------------+
| ``-a6``        | 6 MPI tasks per resource set                         |
+----------------+------------------------------------------------------+
| ``-c42``       | 42 CPU cores per resource set                        |
+----------------+------------------------------------------------------+
| ``-bpacked:7`` | Binds each task to 7 contiguous CPU cores            |
+----------------+------------------------------------------------------+

Basic Distributed Deep Learning BSUB Script
-------------------------------------------

The following bsub script will run a distributed Tensorflow resnet50
training job across 2 nodes.

.. code-block:: bash
    :caption: script.bash

    #BSUB -P <PROJECT>
    #BSUB -W 0:10
    #BSUB -nnodes 2
    #BSUB -q batch
    #BSUB -J mldl_test_job
    #BSUB -o /ccs/home/<user>/job%J.out
    #BSUB -e /ccs/home/<user>/job%J.out

    module load open-ce

    jsrun -bpacked:7 -g6 -a6 -c42 -r1 python $CONDA_PREFIX/horovod/examples/tensorflow2_synthetic_benchmark.py

``bsub`` is used to launch the script as follows:

.. code-block:: bash

    bsub script.bash

For more information on ``bsub`` and job submission
please see: :ref:`running-jobs`.

For more information on ``jsrun`` please see:
:ref:`job-launcher-jsrun`.

Setting up Custom Environments
==============================

The Open-CE conda environments are read-only. Therefore, users cannot install
any additional packages that may be needed. If users need any additional conda
or pip packages, they can clone the Open-CE conda environment into their home
directory and then add any packages they need.

.. note::

    The conda environment includes a module revision number in its name, the
    'X' in ``open-ce-1.2.0-py38-X``. The name of the active environment can be
    found in the prompt string within the parentheses, or ``conda env list`` can be
    used to see what conda environments are available.

.. code-block:: console

    $ module load open-ce
    (open-ce-1.2.0-py38-X) $ conda create --name cloned_env --clone open-ce-1.2.0-py38-X
    (open-ce-1.2.0-py38-X) $ conda activate cloned_env
    (cloned_env) $

By default this should create the cloned environment in
``/ccs/home/${USER}/.conda/envs/cloned_env`` (unless you changed it, as
outlined in our :doc:`Python on OLCF Systems </software/python/index>` page).

To activate the new environment you should still load the module first. This
will ensure that all of the conda settings remain the same.

.. code-block:: console

    $ module load open-ce
    (open-ce-1.2.0-py38-X) $ conda activate cloned_env
    (cloned_env) $

Best Distributed Deep Learning Performance
==========================================

Performance Profiling
---------------------

There are several tools that can be used to profile the performance of a
deep learning job. Below are links to several tools that are available
as part of the open-ce module.

NVIDIA Profiling Tools
^^^^^^^^^^^^^^^^^^^^^^

The open-ce module contains the nvprof profiling tool. It can be used to
profile work that is running on GPUs. It will give information about when
different CUDA kernels are being launched and how long they take to complete.
For more information on using the NVIDA profiling tools on Summit, please see
these `slides <https://www.olcf.ornl.gov/wp-content/uploads/2019/08/NVIDIA-Profilers.pdf>`_.

Horovod Timeline
^^^^^^^^^^^^^^^^

Horovod comes with a tool called Timeline which can help analyze the performance
of Horovod. This is particularly useful when trying to scale a deep learning job
to many nodes. The Timeline tool can help pick various options that can improve
the performance of distributed deep learning jobs that are using Horovod. For
more information, please see `Horovod's documentation <https://github.com/horovod/horovod#horovod-timeline>`_.

PyTorch’s Autograd Profiler
^^^^^^^^^^^^^^^^^^^^^^^^^^^

PyTorch provides a builtin profiler that can be used to find bottlenecks
within a training job. It is most useful for profiling the performance of a job
running on a single GPU. For more information on using PyTorch's profiler, see
`PyTorch's documentation <https://pytorch.org/docs/stable/bottleneck.html#torch-utils-bottleneck>`_.


Reserving Whole Racks
---------------------

Most users will get good performance using LSF basic job submission, and
specifying the node count with ``-nnodes N``. However, users trying
to squeeze out the final few percent of performance can use the following
technique.

When making node reservations for DDL jobs, it can sometimes improve
performance to reserve nodes in a rack-contiguous manner.

In order to instruct BSUB to reserve nodes in the same rack, expert mode must
be used (``-csm y``), and the user needs to explicitly specify the reservation
string. For more information on Expert mode see: :ref:`easy_mode_v_expert_mode`

The following BSUB arguments and reservation string instruct ``bsub`` to
reserve 2 compute nodes within the same rack:

.. code-block:: bash

    #BSUB -csm y
    #BSUB -n 85
    #BSUB -R 1*{select[((LN)&&(type==any))]order[r15s:pg]span[hosts=1]cu[type=rack:pref=config]}+84*{select[((CN)&&(type==any))]order[r15s:pg]span[ptile=42]cu[type=rack:maxcus=1]}

``-csm y`` enables 'expert mode'.

``-n 85`` the total number of slots must be requested, as ``-nnodes`` is not
compatible with expert mode.

We can break the reservation string down to understand each piece.

1. The first term is needed to include a launch node in the reservation.

    .. code-block:: bash

        1*{select[((LN)&&(type==any))]order[r15s:pg]span[hosts=1]cu[type=rack:pref=config]}

2. The second term specifies how many compute slots and how many racks.

    .. code-block:: bash

        +84*{select[((CN)&&(type==any))]order[r15s:pg]span[ptile=42]cu[type=rack:maxcus=1]}

    * Here the ``84`` slots represents 2 compute nodes. Each compute node has 42 compute slots.

    * The ``maxcus=1`` specifies that the nodes can come from at most 1 rack.

Troubleshooting Tips
====================

Problems Distributing Pytorch with Multiple Data Loader Workers
---------------------------------------------------------------

Problem
^^^^^^^

It is common to encounter segmenation faults or deadlocks when running distributed
PyTorch scripts that make use of a DataLoader with multiple workers. A typical
segfault may look something like the following:

.. code-block:: python

    ERROR: Unexpected segmentation fault encountered in worker.
    Traceback (most recent call last):
    File "/gpfs/anaconda3/envs/powerai/lib/python3.7/site-packages/torch/utils/data/dataloader.py", line 724, in _try_get_data
        data = self._data_queue.get(timeout=timeout)
    File "/gpfs/anaconda3/envs/powerai/lib/python3.7/queue.py", line 179, in get
        self.not_empty.wait(remaining)
    File "/gpfs/anaconda3/envs/powerai/lib/python3.7/threading.py", line 300, in wait
        gotit = waiter.acquire(True, timeout)
    File "/gpfs/anaconda3/envs/powerai/lib/python3.7/site-packages/torch/utils/data/_utils/signal_handling.py", line 66, in handler
        _error_if_any_worker_fails()
    RuntimeError: DataLoader worker (pid 150462) is killed by signal: Segmentation fault.

    During handling of the above exception, another exception occurred:

    Traceback (most recent call last):
    File "pytorch_imagenet_resnet50.py", line 277, in <module>
        train(epoch)
    File "pytorch_imagenet_resnet50.py", line 169, in train
        for batch_idx, (data, target) in enumerate(train_loader):
    File "/gpfs/anaconda3/envs/powerai/lib/python3.7/site-packages/torch/utils/data/dataloader.py", line 804, in __next__
        idx, data = self._get_data()
    File "/gpfs/anaconda3/envs/powerai/lib/python3.7/site-packages/torch/utils/data/dataloader.py", line 761, in _get_data
        success, data = self._try_get_data()
    File "/gpfs/anaconda3/envs/powerai/lib/python3.7/site-packages/torch/utils/data/dataloader.py", line 737, in _try_get_data
        raise RuntimeError('DataLoader worker (pid(s) {}) exited unexpectedly'.format(pids_str))
    RuntimeError: DataLoader worker (pid(s) 150462) exited unexpectedly

Solution
^^^^^^^^

The solution is to change the multiprocessing start method to ``forkserver`` (Python 3 only) or
``spawn``. The ``forkserver`` method tends to give better performance. This `Horovod PR <https://github.com/horovod/horovod/pull/1824/files#diff-0647b0c2f82c66d4fb00785c12161f57>`_
has examples of changing scripts to use the ``forkserver`` method.

See the `PyTorch documentation <https://pytorch.org/docs/stable/notes/multiprocessing.html#cuda-in-multiprocessing>`_
for more information.
