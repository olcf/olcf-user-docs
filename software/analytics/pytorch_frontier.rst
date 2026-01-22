*******************
PyTorch on Frontier
*******************

PyTorch is a library for Python programs that pairs well with HPC resources and facilitates building deep learning (DL) projects.
PyTorch emphasizes the flexibility and human-readableness of Python and allows DL models to be expressed in a similar manner.
Compared to other frameworks and libraries, it is one of the more "beginner friendly" ML/DL packages due to its dynamic and familiar "Pythonic" nature.
PyTorch is also useful when GPUs are involved because of its strong GPU acceleration ability.
On Frontier, PyTorch is able to take advantage of the many AMD GPUs available on the system.

This guide outlines installation and running best practices for PyTorch on Frontier.

OLCF Systems this guide applies to:

* :doc:`Frontier </systems/frontier_user_guide>`

Table of Contents:
==================

* :ref:`Installing PyTorch <install>`
   * :ref:`Optional: install mpi4py <install-mpi>`
* :ref:`Example Usage <example>`
   * :ref:`Multinode scripts <ex-code>`
   * :ref:`Batch script <ex-batch>`
* :ref:`Best Practices <practices>`
* :ref:`PyTorch Geometric <torch-geo>`
* :ref:`Flash Attention <flash-attn>`
* :ref:`Troubleshooting <troubleshoot>`
* :ref:`Additional Resources <resources>`


.. _install:

Installing PyTorch
==================

In general, installing either the "stable" or "nightly" wheels of PyTorch>=2.1.0 listed on `Pytorch's Website <https://pytorch.org/get-started/locally/>`__ works on Frontier; however, more recent PyTorch versions typically have better ROCm integration and support.
When navigating the install instructions on PyTorch's website, make sure to indicate "Linux", "Pip", and "ROCm" for accurate install instructions.
Let's follow those instructions to install a stable wheel of torch 2.8.0 with ROCm 6.4.1 (the current recommended version on Frontier).

First, load your modules:

.. code-block:: bash

   module load PrgEnv-gnu/8.6.0
   module load miniforge3/23.11.0-0
   module load rocm/6.4.1
   module load craype-accel-amd-gfx90a
 
Next, create and activate a conda environment that we will install ``torch`` into:

.. code-block:: bash

   conda create -p /path/to/my_env python=3.12 -c conda-forge
   conda activate /path/to/my_env

Finally, install PyTorch:

.. code-block:: bash

   pip install torch==2.8.0 torchvision==0.23.0 torchaudio==2.8.0 --index-url https://download.pytorch.org/whl/rocm6.4
   
You should now be ready to use PyTorch on Frontier!

For older or more specific wheels to install, take a look at these links:

* https://pytorch.org/get-started/previous-versions/
* https://download.pytorch.org/whl/torch/
* https://download.pytorch.org/whl/nightly/torch/

However, note that older versions of the PyTorch pre-compiled wheels will be less likely to work properly on Frontier (especially versions older than v2.1.0).
For users interested in older versions of PyTorch, or for those needing to install special configurations, you may need to install PyTorch from source instead.
If you need to install from source, take a look at AMD's PyTorch+ROCm fork on github: https://github.com/ROCm/pytorch .
If you're having trouble installing from source, feel free to submit a ticket to help@olcf.ornl.gov .

.. _install-mpi:

Optional: Install mpi4py
------------------------

Although ``mpi4py`` isn't required in general (you can accomplish the same task using system environment variables), it acts as a nice convenience when needing to set various MPI parameters when using PyTorch for distributed training.
This is taken from our :doc:`/software/python/parallel_h5py` guide:

.. code-block:: bash

   # Unloading ROCm before building mpi4py prevents potential library linking issues
   # When running, and after building mpi4py, you CAN have the ROCm module loaded
   module unload rocm

   MPICC="cc -shared" pip install --no-cache-dir --no-binary=mpi4py mpi4py

.. note::
   The below example uses ``mpi4py``

.. _example:

Example Usage
-------------

We adapted the ``multinode.py`` `DDP tutorial <https://github.com/pytorch/examples/tree/main/distributed/ddp-tutorial-series>`__ and simplified AMD's `microbenchmarking script <https://github.com/ROCm/pytorch-micro-benchmarking>`__ to work with SLURM, ``mpi4py``, and to use 1 GPU per MPI task.
Utilizing all the GPUs on the node in this manner means there will be 8 tasks per node.
Because we are enforcing 1 GPU per task, each MPI task only sees device ``0`` in PyTorch.
Even if the *physical* GPU ID on Frontier is different, and even though there are 8 GCDs (GPUs) on a node, **the torch device in this case is still 0** due to a task only being mapped to one GPU.

.. _ex-code:

Both scripts below use ``DistributedDataParallel`` and can run across multiple nodes.

.. dropdown:: multinode_olcf.py

    .. code-block:: python

       #multinode_olcf.py
       from mpi4py import MPI
       import torch
       import torch.nn.functional as F
       from torch.utils.data import Dataset, DataLoader

       import torch.multiprocessing as mp
       from torch.utils.data.distributed import DistributedSampler
       from torch.nn.parallel import DistributedDataParallel as DDP

       import torch.distributed as dist

       import os


       class MyTrainDataset(Dataset):
           def __init__(self, size):
               self.size = size
               self.data = [(torch.rand(20), torch.rand(1)) for _ in range(size)]

           def __len__(self):
               return self.size

           def __getitem__(self, index):
               return self.data[index]


       class Trainer:
           def __init__(
               self,
               model: torch.nn.Module,
               train_data: DataLoader,
               optimizer: torch.optim.Optimizer,
               save_every: int,
               snapshot_path: str,
               local_rank: int,
               world_rank: int,

           ) -> None:
               self.local_rank = local_rank
               self.global_rank = global_rank

               self.model = model.to(self.local_rank)
               self.train_data = train_data
               self.optimizer = optimizer
               self.save_every = save_every
               self.epochs_run = 0
               self.snapshot_path = snapshot_path
               if os.path.exists(snapshot_path):
                   print("Loading snapshot")
                   self._load_snapshot(snapshot_path)

               self.model = DDP(self.model, device_ids=[self.local_rank])

           def _load_snapshot(self, snapshot_path):
               loc = f"cuda:{self.local_rank}"
               snapshot = torch.load(snapshot_path, map_location=loc)
               self.model.load_state_dict(snapshot["MODEL_STATE"])
               self.epochs_run = snapshot["EPOCHS_RUN"]
               print(f"Resuming training from snapshot at Epoch {self.epochs_run}")

           def _run_batch(self, source, targets):
               self.optimizer.zero_grad()
               output = self.model(source)
               loss = F.cross_entropy(output, targets)
               loss.backward()
               self.optimizer.step()

           def _run_epoch(self, epoch):
               b_sz = len(next(iter(self.train_data))[0])
               print(f"[GPU{self.global_rank}] Epoch {epoch} | Batchsize: {b_sz} | Steps: {len(self.train_data)}")
               self.train_data.sampler.set_epoch(epoch)
               for source, targets in self.train_data:
                   source = source.to(self.local_rank)
                   targets = targets.to(self.local_rank)
                   self._run_batch(source, targets)

           def _save_snapshot(self, epoch):
               snapshot = {
                   "MODEL_STATE": self.model.module.state_dict(),
                   "EPOCHS_RUN": epoch,
               }
               torch.save(snapshot, self.snapshot_path)
               print(f"Epoch {epoch} | Training snapshot saved at {self.snapshot_path}")

           def train(self, max_epochs: int):
               for epoch in range(self.epochs_run, max_epochs):
                   self._run_epoch(epoch)
                   if self.local_rank == 0 and epoch % self.save_every == 0:
                       self._save_snapshot(epoch)


       def load_train_objs():
           train_set = MyTrainDataset(2048)  # load your dataset
           model = torch.nn.Linear(20, 1)  # load your model
           optimizer = torch.optim.SGD(model.parameters(), lr=1e-3)
           return train_set, model, optimizer


       def prepare_dataloader(dataset: Dataset, batch_size: int):
           return DataLoader(
               dataset,
               batch_size=batch_size,
               pin_memory=True,
               shuffle=False,
               sampler=DistributedSampler(dataset)
           )


       def main(save_every: int, total_epochs: int, batch_size: int, local_rank: int, world_rank: int, snapshot_path: str = "snapshot.pt"):    
           dataset, model, optimizer = load_train_objs()
           train_data = prepare_dataloader(dataset, batch_size)

           trainer = Trainer(model, train_data, optimizer, save_every, snapshot_path, local_rank, global_rank)

           trainer.train(total_epochs)

           dist.destroy_process_group()


       if __name__ == "__main__":
           import argparse
           parser = argparse.ArgumentParser(description='simple distributed training job')
           parser.add_argument('total_epochs', type=int, help='Total epochs to train the model')
           parser.add_argument('save_every', type=int, help='How often to save a snapshot')
           parser.add_argument('--batch_size', default=32, type=int, help='Input batch size on each device (default: 32)')
           parser.add_argument("--master_addr", type=str, required=True)
           parser.add_argument("--master_port", type=str, required=True)

           args = parser.parse_args()

           num_gpus_per_node = torch.cuda.device_count()
           print ("num_gpus_per_node = " + str(num_gpus_per_node), flush=True)

           comm = MPI.COMM_WORLD
           world_size = comm.Get_size()
           global_rank = rank = comm.Get_rank()
           local_rank = int(rank) % int(num_gpus_per_node) # local_rank and device are 0 when using 1 GPU per task
           backend = None
           os.environ['WORLD_SIZE'] = str(world_size)
           os.environ['RANK'] = str(global_rank)
           os.environ['LOCAL_RANK'] = str(local_rank)
           os.environ['MASTER_ADDR'] = str(args.master_addr)
           os.environ['MASTER_PORT'] = str(args.master_port)
           os.environ['NCCL_SOCKET_IFNAME'] = 'hsn0'

           dist.init_process_group(
               backend="nccl",
               #init_method="tcp://{}:{}".format(args.master_addr, args.master_port),
               init_method='env://',
               rank=rank,
               world_size=world_size,
           )

           torch.cuda.set_device(local_rank)

           main(args.save_every, args.total_epochs, args.batch_size, local_rank, global_rank)

.. dropdown:: microbench_olcf.py

    .. code-block:: python

        #microbench_olcf.py
        import torch
        import torchvision
        import time
        import argparse
        import os
        import copy
        import csv
        from mpi4py import MPI

        def forwardbackward(inp, optimizer, network, target, step=0, opt_step=1):
            if step % opt_step == 0:
                optimizer.zero_grad()
            
            out = network(inp)
            # If using HuggingFace model outputs logits, we need to extract them
            if hasattr(out, 'logits'):
                logits = out.logits
            else:
                logits = out
            loss_fn = torch.nn.CrossEntropyLoss().to(device="cuda")

            loss = loss_fn(logits, target)
                
            loss.backward()
            if (step + 1) % opt_step == 0:
                optimizer.step()
                optimizer.zero_grad()


        def run_benchmarking(local_rank, global_rank, world_size, params):
            batch_size = params.batch_size
            iterations = params.iterations

            net = torchvision.models.resnet50
            network = net().to(device="cuda")

            param_copy = network.parameters()

            ## MLPerf Setting
            sgd_opt_base_learning_rate = 0.01
            sgd_opt_weight_decay = 0.0001
            sgd_opt_momentum = 0.9

            optimizer = torch.optim.SGD(param_copy, lr = sgd_opt_base_learning_rate, momentum = sgd_opt_momentum, weight_decay=sgd_opt_weight_decay)

            devices_to_run_on = [local_rank]
            print (f"Rank {global_rank} running on device: {devices_to_run_on}")
            network = torch.nn.parallel.DistributedDataParallel(network, device_ids=devices_to_run_on)
            batch_size = int(batch_size / world_size)

            inp = torch.randn(batch_size, 3, 224, 224, device="cuda")

            # number of classes is 1000 for imagenet
            target = torch.randint(0, 1000, (batch_size,), device="cuda")

            forward_fn = forwardbackward
            network.train()

            ## warmup.
            if global_rank == 0:
                print (f"running forward and backward for warmup.")
            for i in range(2):
                forward_fn(inp, optimizer, network, target, step=0, opt_step=args.opt_step)

            time.sleep(1)
            torch.cuda.synchronize()

            ## benchmark.
            if global_rank == 0:
                print (f"running the benchmark..")
            
            tm = time.time()
            with torch.autograd.profiler.emit_nvtx(enabled=False):
                for i in range(iterations):
                    forward_fn(inp, optimizer, network, target, step=i, opt_step=args.opt_step)
            torch.cuda.synchronize()

            tm2 = time.time()
            time_per_batch = (tm2 - tm) / iterations
            throughput = batch_size / time_per_batch

            dtype = 'FP32'

            result = None
            if not args.output_dir:
                args.output_dir = "."

            print (f"Rank {global_rank} finished: Mini batch size: {batch_size}, Throughput: {throughput}, Time per mini-batch: {time_per_batch}")

            min_time = comm.reduce(time_per_batch,op=MPI.MIN, root=0)
            max_time = comm.reduce(time_per_batch,op=MPI.MAX, root=0)
            avg_time = comm.reduce(time_per_batch,op=MPI.SUM, root=0) # prep for avg later
            tot_thru = comm.reduce(throughput,op=MPI.SUM, root=0)

            time.sleep(3)
            if global_rank == 0:
                print ("")
                print ("--------Overall Summary--------")
                print (f"Num devices: {world_size}")
                print (f"Dtype: {dtype}")
                print (f"Mini batch size [img] : {batch_size*world_size}")
                print (f"Mini batch size [img/gpu] : {batch_size}")
                print (f"Total Throughput [img/sec] : {tot_thru}")
                print (f"Time per mini-batch [sec] : Min: {min_time}, Max: {max_time}, Avg: {avg_time/world_size}")
                result = {
                    "GPUs": world_size,
                    "Mini batch size [img]": batch_size * world_size,
                    "Mini batch size [img/gpu]": batch_size,
                    "Total Throughput [img/sec]": tot_thru,
                    "Min Time [sec]": min_time,
                    "Max Time [sec]": max_time,
                    "Avg Time [sec]": avg_time/world_size
                }
            
            csv_filename = f"{args.output_dir}/benchmark_summary.csv"
            file_exists = os.path.isfile(csv_filename)
            if result:
                with open(csv_filename, "a", newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    if not file_exists:
                        writer.writerow(result.keys())
                    writer.writerow(result.values())
                print(f"Benchmark result saved to {csv_filename}")


        if __name__ == '__main__':
            parser = argparse.ArgumentParser()
            parser.add_argument("--batch-size" , type=int, required=False, default=64, help="Batch size (will be split among devices used by this invocation)")
            parser.add_argument("--iterations", type=int, required=False, default=20, help="Iterations")
            parser.add_argument("--opt-step", type=int, required=False, default=1, help="Optimizer update step")
            parser.add_argument("--output-dir", type=str, default="", help="assign output directory name.")
            parser.add_argument("--master_addr", type=str, required=True)
            parser.add_argument("--master_port", type=str, required=True)

            args = parser.parse_args()

            num_gpus_per_rank = torch.cuda.device_count()

            comm = MPI.COMM_WORLD
            world_size = comm.Get_size()
            global_rank = rank = comm.Get_rank()
            local_rank = int(rank) % int(num_gpus_per_rank) # local_rank and device are 0 when using 1 GPU per task
            backend = None
            os.environ['WORLD_SIZE'] = str(world_size)
            os.environ['RANK'] = str(global_rank)
            os.environ['LOCAL_RANK'] = str(local_rank)
            os.environ['MASTER_ADDR'] = str(args.master_addr)
            os.environ['MASTER_PORT'] = str(args.master_port)
            os.environ['NCCL_SOCKET_IFNAME'] = 'hsn0'

            torch.distributed.init_process_group(
                backend="nccl",
                #init_method=f"tcp://{args.master_addr}:{args.master_port}",
                init_method='env://',
                rank=global_rank,
                world_size=world_size,
            )

            print (f"Rank {global_rank} GPUs Visible: {num_gpus_per_rank}", flush=True)

            torch.cuda.set_device(local_rank) # local_rank and device are 0 when using 1 GPU per task

            run_benchmarking(local_rank,global_rank,world_size,copy.deepcopy(args))

            torch.distributed.destroy_process_group()

.. _ex-batch:

To run the python scripts, an example batch script is given below:

.. dropdown:: Batch Script

    .. code-block:: bash

       #!/bin/bash
       #SBATCH -A PROJECT_ID
       #SBATCH -J ddp_test
       #SBATCH -o logs/ddp_test-%j.o
       #SBATCH -e logs/ddp_test-%j.e
       #SBATCH -t 00:05:00
       #SBATCH -p batch
       #SBATCH -N 2

       # Load modules
       module load PrgEnv-gnu/8.6.0
       module load rocm/6.4.1
       module load craype-accel-amd-gfx90a
       module load miniforge3/23.11.0-0

       # Activate your environment
       conda activate /path/to/my_env

       # Get address of head node
       export MASTER_ADDR=$(hostname -i)

       # Needed to bypass MIOpen, Disk I/O Errors
       export MIOPEN_USER_DB_PATH="/tmp/my-miopen-cache"
       export MIOPEN_CUSTOM_CACHE_DIR=${MIOPEN_USER_DB_PATH}
       rm -rf ${MIOPEN_USER_DB_PATH}
       mkdir -p ${MIOPEN_USER_DB_PATH}

       # Run script
       #srun -N2 -n16 -c7 --gpus-per-task=1 --gpu-bind=closest python3 -W ignore -u ./multinode_olcf.py 2000 10 --master_addr=$MASTER_ADDR --master_port=3442
       #srun -N2 -n16 -c7 --gpus-per-task=1 --gpu-bind=closest python3 -W ignore -u ./microbench_olcf.py --batch-size 1024 --master_addr=$MASTER_ADDR --master_port=3442

As mentioned on our :doc:`/software/python/index` page, submitting batch scripts like below is recommended when using conda environments:

.. code-block:: bash

   sbatch batch_script.sl

After running the script, you will have successfully used PyTorch to train on 16 different GPUs for 2000 epochs and save a training snapshot.
Depending on how long PyTorch takes to initialize, the script should complete in 10-20 seconds.
If the script is able to utilize any cache (e.g., if you ran the script again in the same compute job), then it should complete in approximately 5 seconds.

.. _practices:

Best Practices
==============

Master Address and Sockets
--------------------------

We highly recommend setting ``MASTER_ADDR`` and ``NCCL_SOCKET_IFNAME`` when assigning host addresses:

.. code-block:: bash

   export MASTER_ADDR=$(hostname -i)
   export NCCL_SOCKET_IFNAME=hsn0

There are different Master Ports you can use, but we typically recommend using port 3442 for ``MASTER_PORT``:

.. code-block:: bash

   export MASTER_PORT=3442

Setting the variables above are of utmost importance when using multiple nodes.


Torchrun and Other Distributed PyTorch Launchers
------------------------------------------------

Distributed PyTorch launchers such as ``torchrun (DDP)`` often lack the flexibility to map tasks to GPUs as per the non-trivial NUMA domains of the :ref:`frontier-nodes`. Consequently, users have often reported subpar performance when using these tools.
It is recommended to use ``srun`` to handle the task mapping instead, and to avoid such launchers if possible.
On Frontier, the use of ``torchrun`` has been know to significantly impact the performance of some applications; however, if your application is strongly tied to ``torchrun``, you can try testing it with your application at your own risk. 
Initial tests have shown that a script which normally runs on order of 10 seconds can take up to 10 minutes to run when using ``torchrun`` -- over an order of magnitude worse!
Additionally, nesting ``torchrun`` within ``srun`` (i.e., ``srun torchrun ...``) does not help, as the two task managers will clash.

In either scenario, it is useful for the user to know if their distributed learning program is making use of the node resources in the most optimal manner possible. This can be done using `numa_api <https://github.com/ashesh2512/numa_api>`_.
This library is used to test process ID (PID) bindings within a Python program.
Using the `numactl <https://github.com/numactl/numactl>`_ library, it determines the core affinity for every PID. Based on the cores, it then suggests the most optimal GPU based on the NUMA domains described in :ref:`frontier-nodes`.
For instructions on installation and use, you can refer to `numa_api's README <https://github.com/ashesh2512/numa_api/blob/main/README.md>`_.

Running a Python script with the launch options ``srun -N1 -n8 -c7 --gpus-per-task=1 --gpu-bind=closest`` results in the following output. Note that this is consistent with the NUMA domains described in the :ref:`frontier-nodes`

.. code-block:: bash

   core affinity for PID 1132004: 1 2 3 4 5 6 7
   Suggested GPU for PID 1132004: 4
  
   core affinity for PID 1132006: 17 18 19 20 21 22 23
   Suggested GPU for PID 1132006: 2
  
   core affinity for PID 1132008: 33 34 35 36 37 38 39
   Suggested GPU for PID 1132008: 6

   core affinity for PID 1132009: 41 42 43 44 45 46 47
   Suggested GPU for PID 1132009: 7

In contrast, using ``srun --gpus-per-task=8 --gpu-bind=closest torchrun --nproc_per_node=8 --nnodes=1 --rdzv-id=$SLURM_JOBID --rdzv-backend=c10d --rdzv-endpoint=$MASTER_ADDR:3440`` results in the following output, i.e., here ``torchrun`` launches each task on the same core resulting in subpar performance. Note, the GPU suggestions printed by ``numa_api`` are based on the NUMA regions associated with the cores in :ref:`frontier-nodes`.

.. code-block:: bash

   core affinity for PID 884147: 1
   Suggested GPU for PID 884147: 4

   core affinity for PID 884145: 1
   Suggested GPU for PID 884145: 4

   core affinity for PID 884146: 1
   Suggested GPU for PID 884146: 4

   core affinity for PID 884141: 1
   Suggested GPU for PID 884141: 4

Note, the GPU suggestions reported by ``numa_api`` reflect the NUMA domains associated with those cores, as detailed in :ref:`frontier-nodes`. These suggestions are intended only for verification, helping the user confirm whether processes are using the most optimal GPUs relative to their NUMA domains. They should **not** be used as direct inputs to ``torch.cuda.set_device``, since they may further degrade performance based on the actual core affinities of the running tasks, as in the case above. In the case above, the correct approach would be to figure out how to launch the distributed Python launcher such that each PID is associated with a different NUMA domain. Instead, OLCF recommends using `srun` for simplicity.

Environment Location
--------------------

Where your PyTorch environment is stored on Frontier makes a big difference in performance.
Although NFS locations avoid purge policies, environments stored on NFS (e.g., ``/ccs/home/`` or ``/ccs/proj/``) initialize and run PyTorch slower than other locations.
Storing your environment on Lustre does perform faster than NFS, but still can be slow to initialize (especially at scale).
It is highly recommended to move your environment to the NVMe using ``sbcast``.
Although using ``sbcast`` introduces some overhead, in the long run it is much faster at initializing PyTorch and other libraries in general.
More information on how to use ``sbcast`` and ``conda-pack`` to move your environment to the NVMe can be found on our :doc:`/software/python/sbcast_conda` guide.

In a nutshell: NVMe > Orion >> NFS.

AWS-OFI-RCCL Plugin
-------------------

The `AWS-OFI-RCCL plugin <https://github.com/ROCm/aws-ofi-rccl>`__ enables using libfabric as a network provider while running AMD's RCCL based applications.
This plugin can be built and used by common ML/DL libraries like PyTorch to increase performance when running on AMD GPUs.

To build the plugin on Frontier (using ROCm 6.2.4 as an example):

.. code-block:: bash

   rocm_version=6.2.4

   # Load modules
   module load PrgEnv-gnu/8.6.0
   module load rocm/$rocm_version
   module load craype-accel-amd-gfx90a
   module load gcc-native/13.2
   module load cray-mpich/8.1.31
   libfabric_path=/opt/cray/libfabric/1.22.0

   # Download the plugin repo
   git clone --recursive https://github.com/ROCmSoftwarePlatform/aws-ofi-rccl
   cd aws-ofi-rccl

   # Build the plugin
   ./autogen.sh
   export LD_LIBRARY_PATH=/opt/rocm-$rocm_version/hip/lib:$LD_LIBRARY_PATH
   PLUG_PREFIX=$PWD

   CC=hipcc CFLAGS=-I/opt/rocm-$rocm_version/include ./configure \
   --with-libfabric=$libfabric_path --with-rccl=/opt/rocm-$rocm_version --enable-trace \
   --prefix=$PLUG_PREFIX --with-hip=/opt/rocm-$rocm_version/hip --with-mpi=$MPICH_DIR

   make
   make install

   # Reminder to export the plugin to your path
   echo $PLUG_PREFIX
   echo "Add the following line in the environment to use the AWS OFI RCCL plugin"
   echo "export LD_LIBRARY_PATH="$PLUG_PREFIX"/lib:$""LD_LIBRARY_PATH"

.. warning::
   RCCL library location varies based on ROCm version.

   * Before 6.0.0: ``/opt/rocm-${version}/rccl/lib`` or ``/opt/rocm-${version}/rccl/include``
   * After 6.0.0: ``/opt/rocm-${version}/lib`` or ``/opt/rocm-${version}/include``

Once the plugin is installed, you must include it in your ``LD_LIBRARY_PATH`` when running applications to use it:

.. code-block:: bash

   export LD_LIBRARY_PATH=${PATH TO THE PLUGIN}/lib/:${LD_LIBRARY_PATH}


To avoid a possible deadlock between RCCL and the default libfabric memory registration cache monitor (`memhooks`), before running you should set either

.. code-block:: bash

   export FI_MR_CACHE_MONITOR=kdreg2

or

.. code-block:: bash

   export FI_MR_CACHE_MONITOR=userfaultfd


More information about RCCL, the plugin, and profiling its effect on Frontier applications can be found `here <https://www.olcf.ornl.gov/wp-content/uploads/OLCF_AI_Training_0417_2024.pdf>`__.


Environment Variables
---------------------

When running with the NCCL (RCCL) backend, there are many environment variables that can affect your application's performance. These environment variables are recommended by HPE and AMD on Frontier for best performance at scale:

.. code-block:: bash

   FI_MR_CACHE_MONITOR=kdreg2     # Required to avoid a deadlock.
   FI_CXI_DEFAULT_CQ_SIZE=131072  # Ask the network stack to allocate additional space to process message completions.
   FI_CXI_DEFAULT_TX_SIZE=2048    # Ask the network stack to allocate additional space to hold pending outgoing messages.
   FI_CXI_RX_MATCH_MODE=hybrid    # Allow the network stack to transition to software mode if necessary. 

   NCCL_NET_GDR_LEVEL=3           # Typically improves performance, but remove this setting if you encounter a hang/crash.
   NCCL_CROSS_NIC=1               # On large systems, this NCCL setting has been found to improve performance
   NCCL_SOCKET_IFNAME=hsn0        # NCCL/RCCL will use the high speed network to coordinate startup.

RCCL and NCCL are highly configurable with environment variables. Some other variables to try are:

.. code-block:: bash

   NCCL_ALGO=TREE or RING # May see performance difference with either setting. (should not need to use this, but can try)
   NCCL_DEBUG=info        # For debugging only (warning: generates a large amount of messages)

Alternative Rendezvous Protocol
---------------------------------

On Frontier it is possible to configure the network to use a different protocol for rendezvous messages that improves RCCL performance at large scales. 
This alternative protocol may negatively impact MPI performance, so it is best used for jobs that mostly use RCCL for communication.

To use the alternative protocol you need to both add the flag ``--network=disable_rdzv_get`` to your Slurm allocation request and set the environment variable ``FI_CXI_RDZV_PROTO=alt_read``.
You can add these to your batch scripts for your jobs:

.. code-block:: bash

   #SBATCH --network=disable_rdzv_get

   export FI_CXI_RDZV_PROTO=alt_read

For more information on this alternative protocal and HPE's recommendations for running RCCL on Slingshot networks, see `here <https://support.hpe.com/hpesc/public/docDisplay?docId=dp00004854en_us&docLocale=en_US>`__.


.. _torch-geo:

PyTorch Geometric
=================

`PyTorch Geometric <https://pytorch-geometric.readthedocs.io/en/latest/>`__ (also known as ``PyG`` or ``torch_geometric``) is a library built upon PyTorch to easily write and train Graph Neural Networks (GNNs).
Assuming you already have a working PyTorch installation (see above), install instructions for the ``torch_geometric`` suite of libraries on Frontier are provided below:

.. code-block:: bash

   # Activate your virtual environment
   conda activate /path/to/my_env

   # Install some build tools
   pip install ninja packaging

   # Install PyG libraries (latest version tests in comments)
   MAX_JOBS=16 pip install torch-geometric # v2.6.1
   MAX_JOBS=16 pip install torch-cluster # v1.6.3
   MAX_JOBS=16 pip install torch-spline-conv # v1.2.2

   git clone --recursive https://github.com/rusty1s/pytorch_sparse # v0.6.18
   cd pytorch_sparse
   CC=gcc CXX=g++ MAX_JOBS=16 python3 setup.py bdist_wheel
   pip install dist/*.whl
   cd ..

   git clone --recursive https://github.com/rusty1s/pytorch_scatter # v2.1.2
   cd pytorch_scatter
   CC=gcc CXX=g++ MAX_JOBS=16 python3 setup.py bdist_wheel
   pip install dist/*.whl
   cd ..

.. _flash-attn:

Flash Attention
===============

In addition to PyTorch's internal implementation of FlashAttention, some users may find it beneficial to build the external, `standalone version of FlashAttention <https://github.com/ROCm/flash-attention>`__.
To install the ``flash-attn`` library on Frontier:

.. code-block:: bash

   # Activate your virtual environment
   conda activate /path/to/my_env

   # Install some build tools
   pip install ninja packaging

   # Retrieve the FA repo
   git clone https://github.com/ROCm/flash-attention
   cd flash-attention/
   git checkout v2.7.4-cktile
   git submodule init
   git submodule update

   # Build the flash-attn wheel
   python3 setup.py bdist_wheel

   # Install flash-attn
   pip install dist/*.whl

To test if your installation was successful, you can run this small script:

.. code-block:: python

   import torch
   from flash_attn import flash_attn_func

   q = torch.randn([1, 4096, 8, 128]).cuda().half()
   k = torch.randn([1, 4096, 8, 128]).cuda().half()
   v= torch.randn([1, 4096, 8, 128]).cuda().half()

   result = flash_attn_func(q, k, v, causal=True)
   print(result.shape)


.. _troubleshoot:

Troubleshooting
===============

MPICH mpi4py Errors
-------------------

If you see ``mpich`` error messages indicating a given rank isn't confined to a single NUMA node or domain like this:

.. code-block:: bash

   MPICH ERROR: Unable to use a NIC_POLICY of 'NUMA'. Rank 4 is not confined to a single NUMA node.  There are 4 numa_nodes detected (rc=0).
   MPICH ERROR [Rank 0] [job id 2853270.0] [Fri Dec 13 13:41:36 2024] [frontier05084] - Abort(2665871) (rank 0 in comm 0): Fatal error in PMPI_Init_thread: Other MPI error, error stack:
   MPIR_Init_thread(170).................:
   MPID_Init(501)........................:
   MPIDI_OFI_mpi_init_hook(580)..........:
   open_fabric(1519).....................:
   MPIDI_CRAY_ofi_nic_assign_policy(3548):
   MPIDI_CRAY_ofi_get_nic_index(1801)....: OFI invalid value for environment variable

and you are sure you are mapping your cores correctly via ``srun``, try importing ``mpi4py`` **before** ``torch``.
A recent update in PyTorch broke importing ``mpi4py`` after ``torch``.
If you still see these errors, please contact ``help@olcf.ornl.gov`` for other workarounds (because it's likely not a PyTorch issue).


Proxy Settings
--------------

By default, the compute nodes are closed off from the internet.
If you need access for certain use-cases (e.g., need to download a checkpoint or pre-trained model) you can go through our proxy server.
Set these environment variables in your batch script if needed:

.. code-block:: bash

   export all_proxy=socks://proxy.ccs.ornl.gov:3128/
   export ftp_proxy=ftp://proxy.ccs.ornl.gov:3128/
   export http_proxy=http://proxy.ccs.ornl.gov:3128/
   export https_proxy=http://proxy.ccs.ornl.gov:3128/
   export no_proxy='localhost,127.0.0.0/8,*.ccs.ornl.gov'

.. note::
    The ``socks`` proxy specification depends on implementation.
    Packages that depend on ``httpx`` will need ``httpx[socks]`` and the following change:

    .. code-block:: bash

        # specify socks version
        export all_proxy=socks5://proxy.ccs.ornl.gov:3128/


c10d Socket Warnings
--------------------

When using PyTorch and DDP, you may get warning messages like this:

.. code-block:: bash

   [W socket.cpp:697] [c10d] The client socket cannot be initialized to connect to [frontierXYZ.frontier.olcf.ornl.gov]:3442
   (errno: 97 - Address family not supported by protocol).

Messages like above are harmless and it does not affect PyTorch+DDP when you're using the NCCl/RCCL backend.
Context: After PyTorch v1.x, when using tcp to initialize PyTorch DDP, the default is to use IPv6 addresses; PyTorch falls back to use IPv4 if IPv6 does not work.

Dataset Cache
-------------

The default cache directory is in your ``$HOME`` directory, so you may run into quota issues if datasets get too large or if you have multiple datasets cached at that location.
Some packages let you indicate where you want your dataset cache to be stored.
For example, to manage your Hugging Face cache, you can change it from ``~/.cache/huggingface/datasets`` to:

.. code-block:: bash

   export HF_DATASETS_CACHE="/path/to/another/directory"

It is recommended to move your cache directory to another location if you're seeing quota issues; however, if you store your cache directory on Orion, be mindful that data stored on Orion is subject to purge policies if data is not accessed often.

.. _resources:

Additional Resources
====================

* `PyTorch: Getting Started <https://pytorch.org/get-started/locally/>`__
* `PyTorch ROCm Repository <https://github.com/ROCm/pytorch>`__
* `AI Training Series Repository <https://github.com/olcf/ai-training-series>`__ (specifically the AI for Science at Scale scripts)
* `Enhancing PyTorch Performance on Frontier with the RCCL OFI-Plugin <https://www.olcf.ornl.gov/wp-content/uploads/OLCF_AI_Training_0417_2024.pdf>`__ seminar slides

