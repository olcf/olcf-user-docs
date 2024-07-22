*******************
PyTorch on Frontier
*******************

PyTorch is a library for Python programs that pairs well with HPC resources and facilitates building DL projects.
PyTorch emphasizes the flexibility and human-readableness of Python and allows deep learning models to be expressed in a similar manner.
Compared to other frameworks and libraries, it is one of the more "beginner friendly" ML/DL packages due to its dynamic and familiar "Pythonic" nature.
PyTorch is also useful when GPUs are involved because of its strong GPU acceleration ability.
On Frontier, PyTorch is able to take advantage of the many AMD GPUs available on the system.

This guide outlines installation and running best practices for PyTorch on Frontier.

OLCF Systems this guide applies to:

* Frontier

Installing PyTorch
==================

In general, installing either the "stable" or "nightly" wheels of PyTorch>=2.1.0 listed on `Pytorch's Website <https://pytorch.org/get-started/locally/>`__ works well on Frontier.
When navigating the install instructions on their website, make sure to indicate "Linux", "Pip", and "ROCm" for accurate install instructions.
Let's follow those instructions to install the stable wheel of ``pytorch2.2.2+rocm5.7``. 

First, load your modules:

.. code-block:: bash

   module load PrgEnv-gnu/8.5.0
   module load miniforge3/23.11.0-0
   module load rocm/5.7.1
   module load craype-accel-amd-gfx90a
 
Next, create and activate a conda environment that we will install ``torch`` into:

.. code-block:: bash

   conda create -p /path/to/my_env python=3.10
   source activate /path/to/my_env

Finally, install PyTorch:

.. code-block:: bash

   pip3 install torch==2.2.2 torchvision==0.17.2 torchaudio==2.2.2 --index-url https://download.pytorch.org/whl/rocm5.7
   
You should now be ready to use PyTorch on Frontier!

For older or more specific wheels to install, take a look at these links:

* https://pytorch.org/get-started/previous-versions/
* https://download.pytorch.org/whl/torch/
* https://download.pytorch.org/whl/nightly/torch/

However, note that older versions of the PyTorch pre-compiled wheels will be less likely to work properly on Frontier (especially versions older than v2.1.0).
For users interested in older versions of PyTorch, or for those needing to install special configurations, you may need to install PyTorch from source instead.
If you need to install from source, take a look at AMD's PyTorch+ROCm fork on github: https://github.com/ROCm/pytorch .
If you're having trouble installing from source, feel free to submit a ticket to help@olcf.ornl.gov .

Optional: Install mpi4py
------------------------

Although ``mpi4py`` isn't required in general (you can accomplish the same task using system environment variables), it acts as a nice convenience when needing to set various MPI parameters when using PyTorch for distributed training.

.. code-block:: bash

   MPICC="cc -shared" pip install --no-cache-dir --no-binary=mpi4py mpi4py


Example Usage
-------------

We adapted the ``multinode.py`` `DDP tutorial <https://github.com/pytorch/examples/tree/main/distributed/ddp-tutorial-series>`__ to work with SLURM, ``mpi4py``, and to use 1 GPU per MPI task.
Utilizing all the GPUs on the node in this manner means there will be 8 tasks per node.
Because we are enforcing 1 GPU per task, each MPI task only sees device ``0`` in PyTorch.
Even if the *physical* GPU ID on Frontier is different, and even though there are 8 GCDs (GPUs) on a node, **the torch device in this case is still 0** due to a task only being mapped to one GPU.

The adapted script ``multinode_olcf.py`` is below:

.. code-block:: python

   #multinode_olcf.py
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

       from mpi4py import MPI
       import os
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

To run the python script, an example batch script is given below:

.. code-block:: bash

   #!/bin/bash
   #SBATCH -A PROJECT_ID
   #SBATCH -J ddp_test
   #SBATCH -o logs/ddp_test-%j.o
   #SBATCH -e logs/ddp_test-%j.e
   #SBATCH -t 00:05:00
   #SBATCH -p batch
   #SBATCH -N 2

   # Only necessary if submitting like: sbatch --export=NONE ... (recommended)
   # Do NOT include this line when submitting without --export=NONE
   unset SLURM_EXPORT_ENV

   # Load modules
   module load PrgEnv-gnu/8.5.0
   module load rocm/5.7.1
   module load craype-accel-amd-gfx90a
   module load miniforge3/23.11.0-0

   # Activate your environment
   source activate /path/to/my_env

   # Get address of head node
   export MASTER_ADDR=$(hostname -i)

   # Needed to bypass MIOpen, Disk I/O Errors
   export MIOPEN_USER_DB_PATH="/tmp/my-miopen-cache"
   export MIOPEN_CUSTOM_CACHE_DIR=${MIOPEN_USER_DB_PATH}
   rm -rf ${MIOPEN_USER_DB_PATH}
   mkdir -p ${MIOPEN_USER_DB_PATH}

   # Run script
   srun -N2 -n16 -c7 --gpus-per-task=1 --gpu-bind=closest python3 -W ignore -u ./multinode_olcf.py 2000 10 --master_addr=$MASTER_ADDR --master_port=3442

As mentioned on our :doc:`/software/python/index` page, submitting batch scripts like below is recommended when using conda environments:

.. code-block:: bash

   sbatch --export=NONE batch_script.sl

After running the script, you will have successfully used PyTorch to train on 16 different GPUs for 2000 epochs and save a training snapshot.
Depending on how long PyTorch takes to initialize, the script should complete in 10-20 seconds.
If the script is able to utilize any cache (e.g., if you ran the script again in the same compute job), then it should complete in approximately 5 seconds.

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


Torchrun
--------

Please avoid using ``torchrun`` if possible.
It is recommended to use ``srun`` to handle the task mapping instead.
On Frontier, the use of ``torchrun`` significantly impacts the performance of your code.
Initial tests have shown that a script which normally runs on order of 10 seconds can take up to 10 minutes to run when using ``torchrun`` -- over an order of magnitude worse!
Additionally, nesting ``torchrun`` within ``srun`` (i.e., ``srun torchrun ...``) does not help, as the two task managers will clash.

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

To build the plugin on Frontier (using rocm 5.7.1 as an example):

.. code-block:: bash

   rocm_version=5.7.1

   # Load modules
   module load PrgEnv-gnu/8.5.0
   module load rocm/$rocm_version
   module load craype-accel-amd-gfx90a
   module load gcc-native/12.3
   module load cray-mpich/8.1.28
   module load libtool
   libfabric_path=/opt/cray/libfabric/1.15.2.0

   # Download the plugin repo
   git clone --recursive https://github.com/ROCmSoftwarePlatform/aws-ofi-rccl
   cd aws-ofi-rccl

   # Build the plugin
   ./autogen.sh
   export LD_LIBRARY_PATH=/opt/rocm-$rocm_version/hip/lib:$LD_LIBRARY_PATH
   PLUG_PREFIX=$PWD

   CC=hipcc CFLAGS=-I/opt/rocm-$rocm_version/rccl/include ./configure \
   --with-libfabric=$libfabric_path --with-rccl=/opt/rocm-$rocm_version --enable-trace \
   --prefix=$PLUG_PREFIX --with-hip=/opt/rocm-$rocm_version/hip --with-mpi=$MPICH_DIR

   make
   make install

   # Reminder to export the plugin to your path
   echo $PLUG_PREFIX
   echo "Add the following line in the environment to use the AWS OFI RCCL plugin"
   echo "export LD_LIBRARY_PATH="$PLUG_PREFIX"/lib:$""LD_LIBRARY_PATH"

.. note::
   RCCL library location varies based on ROCm version.

   * Before 6.0.0: ``/opt/rocm-${version}/rccl/lib`` or ``/opt/rocm-${version}/rccl/include``
   * After 6.0.0: ``/opt/rocm-${version}/lib`` or ``/opt/rocm-${version}/include``

Once the plugin is installed, you must include it in your ``LD_LIBRARY_PATH`` when running applications to use it:

.. code-block:: bash

   export LD_LIBRARY_PATH=${PATH TO THE PLUGIN}/lib/:${LD_LIBRARY_PATH}


More information about RCCL, the plugin, and profiling its effect on Frontier applications can be found `here <https://www.olcf.ornl.gov/wp-content/uploads/OLCF_AI_Training_0417_2024.pdf>`__.


Environment Variables
---------------------

When running with the NCCL (RCCL) backend, there are specific environment variables that you should test to see how it affects your application's performance.
Some variables to try are:

.. code-block:: bash

   NCCL_NET_GDR_LEVEL=3   # Can improve performance, but remove this setting if you encounter a hang/crash.
   NCCL_ALGO=TREE or RING # May see performance difference with either setting. (should not need to use this, but can try)
   NCCL_CROSS_NIC=1       # On large systems, this NCCL setting has been found to improve performance
   NCCL_DEBUG=info        # For debugging only (warning: generates a large amount of messages)


..
  Flash-attention (future section)
  ---------------

Troubleshooting
===============

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

c10d Socket Warnings
--------------------

When using PyTorch and DDP, you may get warning messages like this:

.. code-block:: bash

   [W socket.cpp:697] [c10d] The client socket cannot be initialized to connect to [frontierXYZ.frontier.olcf.ornl.gov]:3442
   (errno: 97 - Address family not supported by protocol).

Messages like above are harmless and it does not affect PyTorch+DDP when you're using the NCCl/RCCL backend.
Context: After PyTorch v1.x, when using tcp to initialize PyTorch DDP, the deault is to use IPv6 addresses; PyTorch falls back to use IPv4 if IPv6 does not work.

Dataset Cache
-------------

The default cache directory is in your ``$HOME`` directory, so you may run into quota issues if datasets get too large or if you have multiple datasets cached at that location.
Some packages let you indicate where you want your dataset cache to be stored.
For example, to manage your Hugging Face cache, you can change it from ``~/.cache/huggingface/datasets`` to:

.. code-block:: bash

   export HF_DATASETS_CACHE="/path/to/another/directory"

It is recommended to move your cache directory to another location if you're seeing quota issues; however, if you store your cache directory on Orion, be mindful that data stored on Orion is subject to purge policies if data is not accessed often.

Additional Resources
====================

* `PyTorch: Getting Started <https://pytorch.org/get-started/locally/>`__
* `PyTorch ROCm Repository <https://github.com/ROCm/pytorch>`__
* `AI Training Series Repository <https://github.com/olcf/ai-training-series>`__ (specifically the AI for Science at Scale scripts)
* `Enhancing PyTorch Performance on Frontier with the RCCL OFI-Plugin <https://www.olcf.ornl.gov/wp-content/uploads/OLCF_AI_Training_0417_2024.pdf>`__ seminar slides

