*************************************************************************************
BlazingSQL
*************************************************************************************

Overview
========

`BlazingSQL <https://blazingsql.com/>`_ provides a high-performance distributed SQL engine in Python. Built on the RAPIDS GPU data science ecosystem, ETL massive datasets on GPUs. Complete documentation is available at the `official BlazingSQL documentation <https://docs.blazingsql.com/index.html>`_ website.

Getting Started
===============

BlazingSQL is available at OLCF via `Jupyter <https://docs.olcf.ornl.gov/services_and_applications/jupyter/overview.html#example-creating-a-conda-environment-for-rapids>`_ and via ``module load`` command in Summit. 

We recommend the use of Jupyter in example situations like:

- Python script preparation.
- Workload fits comfortably on a single GPU (NVIDIA V100 16GB).
- Interactive capabilities needed. 

whereas Summit is recommended in example situations like:

- Large workloads.
- Long runtimes on Summit's high memory nodes.
- Your Python script has support for multi-gpu/multi-node execution via dask-cuda.

Be aware of different OLCF's queues and scheduling policies to make best use of `regular <https://docs.olcf.ornl.gov/systems/summit_user_guide.html#job-priority-by-processor-count>`_ and `high memory <https://docs.olcf.ornl.gov/systems/summit_user_guide.html#batch-hm-queue-policy>`_ Summit nodes.

.. note::
    NVIDIA RAPIDS and BlazingSQL are shipped in the same module.


BlazingSQL on `Jupyter <https://docs.olcf.ornl.gov/services_and_applications/jupyter/overview.html>`_
=====================================================================================================

BlazingSQL is provided in Jupyter following  `these instructions <https://docs.olcf.ornl.gov/services_and_applications/jupyter/overview.html#example-creating-a-conda-environment-for-rapids>`_.

Note that Python scripts prepared on Jupyter can be deployed on Summit if they use the same RAPIDS version. Use ``!jupyter nbconvert --to script my_notebook.ipynb`` to convert notebook files to Python scripts.

BlazingSQL on Summit
====================

BlazingSQL is provided on Summit through the ``module load`` command:

.. code-block:: bash

    module load ums
    module load ums-gen119
    module load nvidia-rapids/0.18

The BlazingSQL module loads ``gcc/7.4.0``, ``cuda/10.1.243`` and ``python/3.7.0-anaconda3-5.3.0`` modules. For a complete list of available packages, use ``conda list`` command after loading these modules. 

Distributed execution
---------------------

Preliminaries
^^^^^^^^^^^^^

Running BlazingSQL multi-gpu/multi-node workloads requires a dask-cuda cluster. Setting up a dask-cuda cluster on Summit requires two components:

- `dask-scheduler <https://docs.dask.org/en/latest/setup/cli.html#dask-scheduler>`_.
- `dask-cuda-workers <https://dask-cuda.readthedocs.io/en/latest/worker.html#worker>`_.

Once the dask-cluster is running, the BlazingSQL script should perform five main tasks:
1. Create a dask client to connect to the dask-scheduler
2. Create a BlazingContext that takes in the dask client
3. Create some tables
4. Run queries
5. Shutting down the dask-cuda-cluster


Launching the dask-scheduler and dask-cuda-workers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
    module load nvidia-rapids/0.18
    
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

    echo "Done!"
   
Note twelve dask-cuda-workers are executed, one per each available GPU, ``--memory-limit`` is set to 82 GB and  ``--device-memory-limit`` is set to 16 GB. If using Summit's high-memory nodes ``--memory-limit`` can be increased and setting ``--device-memory-limit`` to 32 GB  and ``--rmm-pool-size`` to 30 GB or so is recommended. Also note it is recommeded to wait some seconds for the dask-scheduler and dask-cuda-workers to start. Finally, from the ``jsrun`` options, note the ``--smpiargs="-disable_gpu_hooks"`` flag is being used. Disabling gpu hooks allows non Spectrum MPI codes run with CUDA.

.. note::
    ``BSQL_*`` environment variables defines the behavior of BlazingContext. Refer to `BlazingContext options <https://docs.blazingsql.com/reference/python/api/blazingsql.BlazingContext.html>`_ for a full description. 


As mentioned earlier, the BlazingSQL code should perform five main tasks as shown in the following script. First, create a dask client to connect to the dask-scheduler; second create a BlazingContext that takes in the dask client; third create some tables; fourth run queries; fifth shutting down the dask-cuda-cluster.

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

Setting up Custom Environments
==============================

The RAPIDS environment is read-only. Therefore, users cannot install any additional packages that may be needed. If users need any additional conda or pip packages, they can clone the RAPIDS environment into their preferred directory and then add any packages they need.

Cloning the RAPIDS environment can be done with the next commands:

.. code-block:: bash

    module load ums
    module load ums-gen119
    module load nvidia-rapids/0.18

    conda create --clone /sw/summit/ums/gen119/nvrapids_0.18_gcc_7.4.0 -p <my_environment_path>

To activate the new environment you should still load the RAPIDS module first. This will ensure that all of the conda settings remain the same.

.. code-block:: bash

    module load ums
    module load ums-gen119
    module load nvidia-rapids/0.18

    source activate <my_environment_path>
