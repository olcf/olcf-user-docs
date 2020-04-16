
*************************************************************************************
IBM Watson Machine Learning CE
*************************************************************************************

Getting Started
===============

IBM Watson Machine Learning Community Edition is provided on Summit
through the module ``ibm-wml-ce``.

To access the IBM WML CE packages use the ``module load`` command:

.. code-block:: bash

    module load ibm-wml-ce

Loading a specific version of the module is recommended to future-proof
scripts against software updates. The following commands can be used to
find and load specific module versions:

.. code-block:: bash

    [user@login2.summit ~]$ module avail ibm-wml-ce

    ------------------------- /sw/summit/modulefiles/core --------------------------
    ibm-wml-ce/1.6.1-1    ibm-wml-ce/1.6.2-0    ibm-wml-ce/1.6.2-3
    ibm-wml-ce/1.6.1-2    ibm-wml-ce/1.6.2-1    ibm-wml-ce/1.7.0-1 (D)
    ibm-wml-ce/1.6.1-3    ibm-wml-ce/1.6.2-2
    ...
    [user@login2.summit ~]$ module load ibm-wml-ce/1.6.2-3

For more information on loading modules, including loading specific verions,
see: :ref:`environment-management-with-lmod`

This will activate a conda environment which is pre-loaded with the following
packages, and their dependencies:

.. table::
    :widths: 20 40 40 35

    +--------------------+--------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------+
    | IBM WML CE Version | ibm-wml-ce/1.6.1                                                                                                               | ibm-wml-ce/1.6.2                                                                                                                | ibm-wml-ce/1.7.0                                                                                                                    +
    +--------------------+--------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------+
    | Package            | `IBM DDL 1.4.0 <https://www.ibm.com/support/knowledgecenter/SS5SF7_1.6.1/navigation/wmlce_getstarted_ddl.html>`_               | `IBM DDL 1.5.0 <https://www.ibm.com/support/knowledgecenter/SS5SF7_1.6.2/navigation/wmlce_getstarted_ddl.html>`_                | `IBM DDL 1.5.1 <https://www.ibm.com/support/knowledgecenter/SS5SF7_1.7.0/navigation/wmlce_getstarted_ddl.html>`_                    +
    |                    +--------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------+
    |                    | `Tensorflow 1.14 <https://www.ibm.com/support/knowledgecenter/SS5SF7_1.6.1/navigation/wmlce_getstarted_tensorflow.html>`_      | `Tensorflow 1.15 <https://www.ibm.com/support/knowledgecenter/SS5SF7_1.6.2/navigation/wmlce_getstarted_tensorflow.html>`_       | `Tensorflow 2.1 <https://www.ibm.com/support/knowledgecenter/SS5SF7_1.7.0/navigation/wmlce_getstarted_tensorflow.html>`_            +
    |                    +--------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------+
    |                    | `Pytorch 1.1.0 <https://www.ibm.com/support/knowledgecenter/SS5SF7_1.6.1/navigation/wmlce_getstarted_pytorch.html>`_           | `Pytorch 1.2.0 <https://www.ibm.com/support/knowledgecenter/SS5SF7_1.6.2/navigation/wmlce_getstarted_pytorch.html>`_            | `Pytorch 1.3.1 <https://www.ibm.com/support/knowledgecenter/SS5SF7_1.7.0/navigation/wmlce_getstarted_pytorch.html>`_                +
    |                    +--------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------+
    |                    | `Caffe(IBM-enhanced) 1.0.0 <https://www.ibm.com/support/knowledgecenter/SS5SF7_1.6.1/navigation/wmlce_getstarted_caffe.html>`_ | `Caffe (IBM-enhanced) 1.0.0 <https://www.ibm.com/support/knowledgecenter/SS5SF7_1.6.2/navigation/wmlce_getstarted_caffe.html>`_ | `Caffe (IBM-enhanced) 1.0.0 <https://www.ibm.com/support/knowledgecenter/SS5SF7_1.7.0/navigation/wmlce_getstarted_caffe.html>`_     +
    |                    +--------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------+
    |                    | `Horovod @9f87459 (IBM-DDL Backend) <https://github.com/horovod/horovod>`_                                                     | `Horovod v0.18.2 (IBM-DDL Backend) <https://github.com/horovod/horovod>`_                                                       | `Horovod v0.19 (NCCL Backend) <https://www.ibm.com/support/knowledgecenter/SS5SF7_1.7.0/navigation/wmlce_getstarted_horovod.html>`_ |
    +--------------------+--------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------+
    | Complete List      | `1.6.1 Software Packages <https://www.ibm.com/support/knowledgecenter/SS5SF7_1.6.1/navigation/wmlce_software_pkgs.html>`_      | `1.6.2 Software Packages <https://www.ibm.com/support/knowledgecenter/SS5SF7_1.6.2/navigation/wmlce_software_pkgs.html>`_       | `1.7.0 Software Packages <https://www.ibm.com/support/knowledgecenter/SS5SF7_1.7.0/navigation/wmlce_software_pkgs.html>`_           |
    +--------------------+--------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------+

.. note::

    WML-CE was the topic of the October 2019 User Conference Call, presented by
    Bryant Nelson and Brad Nemanich of IBM.
    (`slides <https://www.olcf.ornl.gov/wp-content/uploads/2019/10/DDLonSummit.pdf>`__ | `recording <https://vimeo.com/377551223>`__)

Running DDL Jobs
================

IBM DDL provides a tool called ``ddlrun`` which facilitates the launching of
DDL jobs on Summit. When called inside of a ``bsub`` script, ``ddlrun`` will
automatically distribute the training job across all the compute hosts in the
reservation. ``ddlrun`` automatically selects default arguments optimized
for performance.

Basic DDL BSUB Script
---------------------

The following bsub script will run a distributed Tensorflow resnet50
training job across 2 nodes.

.. code-block:: bash
    :caption: script.bash

    #BSUB -P <PROJECT>
    #BSUB -W 0:10
    #BSUB -nnodes 2
    #BSUB -q batch
    #BSUB -J ddl_test_job
    #BSUB -o /ccs/home/<user>/job%J.out
    #BSUB -e /ccs/home/<user>/job%J.out

    module load ibm-wml-ce

    ddlrun python $CONDA_PREFIX/horovod/examples/tensorflow2_synthetic_benchmark.py

``bsub`` is used to launch the script as follows:

.. code-block:: bash

    bsub script.bash

For more information on ``bsub`` and job submission
please see: :ref:`running-jobs`.

Verbose mode
^^^^^^^^^^^^

Using the verbose flag (``-v``) with ``ddlrun`` displays much more debugging
information. This should be the first step to troubleshoot errors when
launching a distributed job.

Setting up Custom Environments
==============================

The IBM-WML-CE conda environment is read-only. Therefore, users
cannot install any additional packages that may be needed. If users need
any additional conda or pip packages, they can clone the IBM-WML-CE
conda environment into their home directory and then add any packages they
need.

.. note::

    The conda environment includes a module revision number, the 'X' in
    ``ibm-wml-ce-1.7.0-X``. The name of the active environment can be found in
    the prompt string, or ``conda env list`` can be used to see what conda
    environments are available.

.. code-block:: console

    $ module load ibm-wml-ce
    (ibm-wml-ce-1.7.0-X) $ conda create --name cloned_env --clone ibm-wml-ce-1.7.0-X
    (ibm-wml-ce-1.7.0-X) $ conda activate cloned_env
    (cloned_env) $

By default this should create the cloned environment in
``/ccs/home/${USER}/.conda/envs/cloned_env``.

To activate the new environment you should still load the module first. This
will ensure that all of the conda settings remain the same.

.. code-block:: console

    $ module load ibm-wml-ce
    (ibm-wml-ce-1.7.0-X) $ conda activate cloned_env
    (cloned_env) $

Best DDL Performance
====================

Most users will get good performance using LSF basic job submission, and
specifying the node count with ``-nnodes N``. However, users trying
to squeeze out the final few percent of performance can use the following
techniques.

Reserving Whole Racks
---------------------

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

Example
===================

The following graph shows the scaling performance of the
``tf_cnn_benchmarks`` implementation of the Resnet50 model
running on Summit during initial benchmark testing.

.. figure:: /images/ibm_wml_ddl_resnet50.png
   :align: center

   Figure 1. Performance Scaling of IBM DDL on Summit

The following LSF script can be used to reproduce the results for 144 nodes:

.. code-block:: bash

    #BSUB -P <PROJECT>
    #BSUB -W 1:00
    #BSUB -csm y
    #BSUB -n 6049
    #BSUB -R "1*{select[((LN) && (type == any))] order[r15s:pg] span[hosts=1] cu[type=rack:pref=config]}+6048*{select[((CN) && (type == any))] order[r15s:pg] span[ptile=42] cu[type=rack:maxcus=8]}"
    #BSUB -q batch
    #BSUB -J <PROJECT>
    #BSUB -o /ccs/home/user/job%J.out
    #BSUB -e /ccs/home/user/job%J.out

    module load ibm-wml-ce/1.6.2-2

    ddlrun --nodes 18 --racks 4 --aisles 2 python $CONDA_PREFIX/tf_cnn_benchmarks/tf_cnn_benchmarks.py \
        --variable_update=horovod\
        --model=resnet50 \
        --num_gpus=1 \
        --batch_size=256 \
        --num_batches=100 \
        --num_warmup_batches=10 \
        --data_name=imagenet \
        --allow_growth=True \
        --use_fp16

Troubleshooting Tips
--------------------

Full command
^^^^^^^^^^^^

The output from ``ddlrun`` includes the exact command used to launch the
distributed job. This is useful if a user wants to see exactly what ``ddlrun``
is doing. The following is the first line of the output from the above script:

.. code-block:: console

    $ module load ibm-wml-ce
    (ibm-wml-ce-1.6.1-1) $ ddlrun python $CONDA_PREFIX/tf_cnn_benchmarks/tf_cnn_benchmarks.py --variable_update=ddl --model=resnet50
    + /autofs/nccs-svm1_sw/summit/.swci/1-compute/opt/spack/20180914/linux-rhel7-ppc64le/xl-16.1.1-3/spectrum-mpi-10.3.0.1-20190611-aqjt3jo53mogrrhcrd2iufr435azcaha/bin/mpirun \
      -x LSB_JOBID -x PATH -x PYTHONPATH -x LD_LIBRARY_PATH -x LSB_MCPU_HOSTS -x NCCL_LL_THRESHOLD=0 -x NCCL_TREE_THRESHOLD=0 \
      -disable_gdr -gpu --rankfile /tmp/DDLRUN/DDLRUN.xoObgjtixZfp/RANKFILE -x "DDL_OPTIONS=-mode p:6x2x1x1 " -n 12 \
      -mca plm_rsh_num_concurrent 12 -x DDL_HOST_PORT=2200 -x "DDL_HOST_LIST=g28n14:0,2,4,6,8,10;g28n15:1,3,5,7,9,11" bash \
      -c 'source /sw/summit/ibm-wml-ce/anaconda-base/etc/profile.d/conda.sh && conda activate /sw/summit/ibm-wml-ce/anaconda-base/envs/ibm-wml-ce-1.6.1-1 \
      > /dev/null 2>&1 && python /sw/summit/ibm-wml-ce/anaconda-base/envs/ibm-wml-ce-1.6.1-1/ddl-tensorflow/examples/mnist/mnist-env.py'
    ...

Problems Distributing Pytorch with Multiple Data Loader Workers
---------------------

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
