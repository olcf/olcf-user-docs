*************************************************************************************
NVIDIA RAPIDS
*************************************************************************************

Overview
========

`RAPIDS <https://rapids.ai/>`_ is a suite of libraries to execute end-to-end data science and analytics pipelines on GPUs. RAPIDS utilizes NVIDIA CUDA primitives for low-level compute optimization through user-friendly Python interfaces. An overview of the RAPIDS libraries available at OLCF is given next.

cuDF
----

cuDF is a Python GPU DataFrame library (built on the Apache Arrow columnar memory format) for loading, joining, aggregating, filtering, and otherwise manipulating data.

cuML
----

cuML is a suite of libraries that implement machine learning algorithms and mathematical primitives functions that share compatible APIs with other RAPIDS projects.

cuGraph
-------

cuGraph is a GPU accelerated graph analytics library, with functionality like NetworkX, which is seamlessly integrated into the RAPIDS data science platform.

dask-cuda
---------

dask-cuda extends Dask where it is necessary to scale up and scale out RAPIDS workflows.

cuCIM
-----

cuCIM is a GPU accelerated n-dimensional image processing and image I/O library. It has a similar API to scikit-image.

In addition to NVIDIA supported libraries, the RAPIDS modules also includes:


CuPy
----

Preferred Networks' CuPy is a NumPy-compatible, open source mathematical library. While CuPy is not a library under the RAPIDS framework, it is compatible with RAPIDS and dask-cuda for memory management and multi-GPU, multi-node workload distribution.

Complete documentation is available at the `official RAPIDS documentation <https://docs.rapids.ai/api>`_ and `CuPy's documentation <https://docs.cupy.dev/en/stable/overview.html>`_ websites.

BlazingSQL
----------

`BlazingSQL <https://blazingsql.com/>`_ is an open source community effort that provides a GPU accelerated and distributed SQL engine in Python. No database needed, BlazingSQL can operate directly on tabular data. Full documentation is available at the `official BlazingSQL documentation <https://docs.blazingsql.com/index.html>`_ website.

Getting Started
===============

RAPIDS is available at OLCF via `Jupyter <https://docs.olcf.ornl.gov/services_and_applications/jupyter/overview.html#example-creating-a-conda-environment-for-rapids>`__ and via ``module load`` command in Summit. 

We recommend the use of Jupyter in example situations like:

- Python script preparation.
- Workload fits comfortably on a single GPU (NVIDIA V100 16GB).
- Interactive capabilities needed. 

whereas Summit is recommended in example situations like:

- Large workloads.
- Long runtimes on Summit's high memory nodes.
- Your Python script has support for multi-gpu/multi-node execution via dask-cuda.
- Your Python script is single GPU but requires `simultaneous job steps <https://docs.olcf.ornl.gov/systems/summit_user_guide.html?highlight=jsrun%20steps#simultaneous-job-steps>`_.

RAPIDS on `Jupyter <https://docs.olcf.ornl.gov/services_and_applications/jupyter/overview.html>`_
=================================================================================================

RAPIDS is provided in Jupyter following  `these instructions <https://docs.olcf.ornl.gov/services_and_applications/jupyter/overview.html#example-creating-a-conda-environment-for-rapids>`_.

Note that Python scripts prepared on Jupyter can be deployed on Summit if they use the same RAPIDS version. Use ``!jupyter nbconvert --to script my_notebook.ipynb`` to convert notebook files to Python scripts.

RAPIDS on Summit
================

RAPIDS is provided on Summit through the ``module load`` command:

.. code-block:: bash

    module load ums
    module load ums-gen119
    module load nvidia-rapids/21.08

Due different dependecies, cuCIM is available on Summit as a separate module using the next commands:

.. code-block:: bash

    module load ums
    module load ums-gen119
    module load nvidia-rapids/cucim_21.08

.. note::
    | The RAPIDS and cuCIM modules loads ``gcc/9.3.0`` and ``cuda/11.0.3`` modules. For a complete list of available packages, use ``conda list`` command.
    | After Summit's OS upgrade on August 7th, 2021. Older RAPIDS modules were deprecated.


RAPIDS basic execution
----------------------

As an example, the following LSF script will run a single-GPU RAPIDS script in one Summit node:

.. code-block:: bash

    #BSUB -P <PROJECT>
    #BSUB -W 0:05
    #BSUB -nnodes 1
    #BSUB -q batch
    #BSUB -J rapids_test
    #BSUB -o rapids_test_%J.out
    #BSUB -e rapids_test_%J.out

    module load ums
    module load ums-gen119
    module load nvidia-rapids/21.08

    jsrun --nrs 1 --tasks_per_rs 1 --cpu_per_rs 1 --gpu_per_rs 1 --smpiargs="-disable_gpu_hooks" \ 
          python $CONDA_PREFIX/examples/cudf/cudf_test.py

From the ``jsrun`` options, note the ``--smpiargs="-disable_gpu_hooks"`` flag is being used. Disabling gpu hooks allows non Spectrum MPI codes run with CUDA.

Note the "RAPIDS basic execution" option is for illustrative purposes and not recommended to run RAPIDS on Summit since it underutilizes resources. If your RAPIDS code is single GPU, consider `Jupyter <https://docs.olcf.ornl.gov/services_and_applications/jupyter/overview.html#example-creating-a-conda-environment-for-rapids>`__ or the concurrent job steps option.

Simultaneous job steps with RAPIDS
----------------------------------

In cases when a set of time steps need to be processed by single-GPU RAPIDS codes and each time step fits comfortably in GPU memory, it is recommended to execute `simultaneous job steps <https://docs.olcf.ornl.gov/systems/summit_user_guide.html?highlight=jsrun%20steps#simultaneous-job-steps>`_.

The following script provides a general pattern to run job steps simultaneously with RAPIDS:

.. code-block:: bash

    #BSUB -P <PROJECT>
    #BSUB -W 0:05
    #BSUB -nnodes 1
    #BSUB -q batch
    #BSUB -J rapids_test
    #BSUB -o rapids_test_%J.out
    #BSUB -e rapids_test_%J.out

    module load ums
    module load ums-gen119
    module load nvidia-rapids/21.08

    jsrun --nrs 1 --tasks_per_rs 1 --cpu_per_rs 1 --gpu_per_rs 1 --smpiargs="-disable_gpu_hooks" \ 
          python /my_path/my_rapids_script.py dataset_part01 &
    jsrun --nrs 1 --tasks_per_rs 1 --cpu_per_rs 1 --gpu_per_rs 1 --smpiargs="-disable_gpu_hooks" \ 
          python /my_path/my_rapids_script.py dataset_part02 &
    jsrun --nrs 1 --tasks_per_rs 1 --cpu_per_rs 1 --gpu_per_rs 1 --smpiargs="-disable_gpu_hooks" \ 
          python /my_path/my_rapids_script.py dataset_part03 &
    ...
    wait

Be aware of different OLCF's queues and scheduling policies to make best use of `regular <https://docs.olcf.ornl.gov/systems/summit_user_guide.html#job-priority-by-processor-count>`_ and `high memory <https://docs.olcf.ornl.gov/systems/summit_user_guide.html#batch-hm-queue-policy>`_ Summit nodes.

Distributed RAPIDS execution
----------------------------

Preliminaries
^^^^^^^^^^^^^

Running RAPIDS multi-gpu/multi-node workloads requires a dask-cuda cluster. Setting up a dask-cuda cluster on Summit requires two components:

- `dask-scheduler <https://docs.dask.org/en/latest/setup/cli.html#dask-scheduler>`_.
- `dask-cuda-workers <https://docs.rapids.ai/api/dask-cuda/stable/api.html#worker>`_.

Once the dask-cluster is running, the RAPIDS script should perform four main tasks. First, connect to the dask-scheduler; second, wait for all workers to start; third, do some computation, and fourth, shutdown the dask-cuda-cluster.

Reference of multi-gpu/multi-node operation with cuDF, cuML, cuGraph is available in the next links:

- `10 Minutes to cuDF and Dask-cuDF <https://docs.rapids.ai/api/cudf/stable/10min.html#>`_.
- `cuML's Multi-Node, Multi-GPU Algorithms <https://docs.rapids.ai/api/cuml/stable/api.html#multi-node-multi-gpu-algorithms>`_.
- `Multi-GPU with cuGraph <https://docs.rapids.ai/api/cugraph/stable/dask-cugraph.html>`_.

Launching the dask-scheduler and dask-cuda-workers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following script will run a dask-cuda cluster on two compute nodes, then it executes a Python script.

.. code-block:: bash

    #BSUB -P <PROJECT>
    #BSUB -W 0:05
    #BSUB -alloc_flags "gpumps smt4 NVME"
    #BSUB -nnodes 2
    #BSUB -J rapids_dask_test_tcp
    #BSUB -o rapids_dask_test_tcp_%J.out
    #BSUB -e rapids_dask_test_tcp_%J.out

    PROJ_ID=<project>

    module load ums
    module load ums-gen119
    module load nvidia-rapids/21.08

    SCHEDULER_DIR=$MEMBERWORK/$PROJ_ID/dask
    WORKER_DIR=/mnt/bb/$USER

    if [ ! -d "$SCHEDULER_DIR" ]
    then
        mkdir $SCHEDULER_DIR
    fi

    SCHEDULER_FILE=$SCHEDULER_DIR/my-scheduler.json

    echo 'Running scheduler'
    jsrun --nrs 1 --tasks_per_rs 1 --cpu_per_rs 1 --smpiargs="-disable_gpu_hooks" \
          dask-scheduler --interface ib0 \
                         --scheduler-file $SCHEDULER_FILE \
                         --no-dashboard --no-show &

    #Wait for the dask-scheduler to start
    sleep 10

    jsrun --rs_per_host 6 --tasks_per_rs 1 --cpu_per_rs 2 --gpu_per_rs 1 --smpiargs="-disable_gpu_hooks" \
          dask-cuda-worker --nthreads 1 --memory-limit 82GB --device-memory-limit 16GB --rmm-pool-size=15GB \
                           --interface ib0 --scheduler-file $SCHEDULER_FILE --local-directory $WORKER_DIR \
                           --no-dashboard &

    #Wait for WORKERS
    sleep 10 

    WORKERS=12

    python -u $CONDA_PREFIX/examples/dask-cuda/verify_dask_cuda_cluster.py $SCHEDULER_FILE $WORKERS

    wait

    #clean DASK files
    rm -fr $SCHEDULER_DIR

    echo "Done!"
   
Note twelve dask-cuda-workers are executed, one per each available GPU, ``--memory-limit`` is set to 82 GB and  ``--device-memory-limit`` is set to 16 GB. If using Summit's high-memory nodes ``--memory-limit`` can be increased and setting ``--device-memory-limit`` to 32 GB  and ``--rmm-pool-size`` to 30 GB or so is recommended. Also note it is recommeded to wait some seconds for the dask-scheduler and dask-cuda-workers to start.

As mentioned earlier, the RAPIDS code should perform four main tasks as shown in the following script. First, connect to the dask-scheduler; second, wait for all workers to start; third, do some computation, and fourth, shutdown the dask-cuda-cluster.

.. code-block:: bash
    
    import sys
    from dask.distributed import Client

    def disconnect(client, workers_list):
        client.retire_workers(workers_list, close_workers=True)
        client.shutdown()

    if __name__ == '__main__':

        sched_file = str(sys.argv[1]) #scheduler file
        num_workers = int(sys.argv[2]) # number of workers to wait for

        # 1. Connects to the dask-cuda-cluster
        client = Client(scheduler_file=sched_file)
        print("client information ",client)
        
        # 2. Blocks until num_workers are ready
        print("Waiting for " + str(num_workers) + " workers...")
        client.wait_for_workers(n_workers=num_workers)

        
        workers_info=client.scheduler_info()['workers']
        connected_workers = len(workers_info)
        print(str(connected_workers) + " workers connected")

        # 3. Do computation
        # ...
        # ...

        # 4. Shutting down the dask-cuda-cluster
        print("Shutting down the cluster")
        workers_list = list(workers_info)
        disconnect (client, workers_list)

Setting up Custom Environments
==============================

The RAPIDS environment is read-only. Therefore, users cannot install any additional packages that may be needed. If users need any additional conda or pip packages, they can clone the RAPIDS environment into their preferred directory and then add any packages they need.

Cloning the RAPIDS environment can be done with the next commands:

.. code-block:: bash

    module load ums
    module load ums-gen119
    module load nvidia-rapids/21.08

    conda create --clone nvrapids_21.08_gcc_9.3.0 -p <my_environment_path>

To activate the new environment you should still load the RAPIDS module first. This will ensure that all of the conda settings remain the same.

.. code-block:: bash

    module load ums
    module load ums-gen119
    module load nvidia-rapids/21.08

    conda activate <my_environment_path>

   
BlazingSQL Distributed Execution
================================

Running BlazingSQL multi-gpu/multi-node workloads requires a dask-cuda cluster as explained earlier. 

The following script will run a dask-cuda cluster on two compute nodes, then it executes a Python script running BlazingSQL.

.. code-block:: bash
    
    #BSUB -P ABC123
    #BSUB -W 0:05
    #BSUB -alloc_flags "gpumps smt4 NVME"
    #BSUB -nnodes 2
    #BSUB -q batch
    #BSUB -J bsql_dask
    #BSUB -o bsql_dask_%J.out
    #BSUB -e bsql_dask_%J.out
    
    PROJ_ID=abc123
    
    module load ums
    module load ums-gen119
    module load nvidia-rapids/21.08
    
    SCHEDULER_DIR=$MEMBERWORK/$PROJ_ID/dask
    BSQL_LOG_DIR=$MEMBERWORK/$PROJ_ID/bsql
    WORKER_DIR=/mnt/bb/$USER
    
    mkdir -p $SCHEDULER_DIR
    mkdir -p $BSQL_LOG_DIR
    
    SCHEDULER_FILE=$SCHEDULER_DIR/my-scheduler.json
    
    echo 'Running scheduler'
    jsrun --nrs 1 --tasks_per_rs 1 --cpu_per_rs 2 --smpiargs="-disable_gpu_hooks" \
          dask-scheduler --interface ib0 --scheduler-file $SCHEDULER_FILE \
                         --no-dashboard --no-show &
              
    #Wait for the dask-scheduler to start
    sleep 10

    jsrun --rs_per_host 6 --tasks_per_rs 1 --cpu_per_rs 2 --gpu_per_rs 1 --smpiargs="-disable_gpu_hooks" \
          dask-cuda-worker --nthreads 1 --memory-limit 82GB --device-memory-limit 16GB --rmm-pool-size=15GB \
                           --death-timeout 60  --interface ib0 --scheduler-file $SCHEDULER_FILE --local-directory $WORKER_DIR \
                           --no-dashboard &

    #Wait for WORKERS
    sleep 10

    export BSQL_BLAZING_LOGGING_DIRECTORY=$BSQL_LOG_DIR
    export BSQL_BLAZING_LOCAL_LOGGING_DIRECTORY=$BSQL_LOG_DIR

    python -u $CONDA_PREFIX/examples/blazingsql/bsql_test_multi.py $SCHEDULER_FILE

    wait

    #clean LOG files
    rm -fr $SCHEDULER_DIR
    rm -fr $BSQL_LOG_DIR

.. note::
    ``BSQL_*`` environment variables defines the behavior of BlazingContext. Refer to `BlazingContext options <https://docs.blazingsql.com/reference/python/api/blazingsql.BlazingContext.html>`_ for a full description.

Once the dask-cluster is running, the BlazingSQL script should perform five main tasks:

#. Create a dask client to connect to the dask-scheduler.
#. Create a BlazingContext that takes in the dask client.
#. Create some tables.
#. Run queries.
#. Shutting down the dask-cuda-cluster.

This is exemplified in the next script:

.. code-block:: bash

    import sys
    import cudf
    from dask.distributed import Client
    from blazingsql import BlazingContext


    def disconnect(client, workers_list):
        client.retire_workers(workers_list, close_workers=True)
        client.shutdown()

    if __name__ == '__main__':

        sched_file = str(sys.argv[1]) #scheduler file

        # 1. Create a dask client to connect to the dask-scheduler
        client = Client(scheduler_file=sched_file)
        print("client information ",client)

        workers_info=client.scheduler_info()['workers']
        connected_workers = len(workers_info)
        print(str(connected_workers) + " workers connected")

        # 2. Create a BlazingContext that takes in the dask client
        # you want to set `allocator='existing'` if you are launching the dask-cuda-worker with an rmm memory pool
        bc = BlazingContext(dask_client = client, network_interface='ib0', allocator='existing')

        # 3. Create some tables
        bc.create_table('my_table','/data/file*.parquet')

        # 4. Run queries
        ddf = bc.sql('select count(*) from my_table')
        print(ddf.head())

        # 5. Shutting down the dask-cuda-cluster
        print("Shutting down the cluster")
        workers_list = list(workers_info)
        disconnect (client, workers_list)

.. note::
    Consult this `example <https://docs.blazingsql.com/index.html#usage>`_ for single gpu usage. Then, follow RAPIDS' basic or simultaneous execution LFS scripts.
