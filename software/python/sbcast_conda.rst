*************************
Sbcast Conda Environments
*************************

Slurm contains a utility called ``sbcast`` that takes a file and broadcasts it to each node’s node-local storage (i.e., /tmp, NVMe).
This is useful for sharing large input files, binaries and shared libraries, while reducing the overhead on shared file systems and overhead at startup.
On Frontier, this is highly recommended at scale if you have multiple shared libraries on Lustre/NFS file systems.
Because Python environments are typically built in this fashion, you may find *significant* initialization speedup on Frontier if you ``sbcast`` your environment to the NVMe (burst buffer) before running any Python scripts.
This guide walks through an example of how to ``tar`` up your conda environment using ``conda-pack`` and how to ``sbcast`` it to the NVMe on Frontier.

OLCF Systems this guide applies to:

* :doc:`Frontier </systems/frontier_user_guide>`

Installing Conda-Pack
=====================

Because conda environments are not relocatable, we must install a tool like ``conda-pack`` that will make relocation to the NVMe possible.
`Conda-Pack <https://conda.github.io/conda-pack/>`__ builds archives from original conda package sources and reproduces conda's own relocation logic.
To install ``conda-pack``, install it from the ``conda-forge`` channel like so:

.. code-block:: bash

   conda install conda-pack -c conda-forge

.. note::
   If ``conda-pack`` is unable to be installed in your production environment, you can install ``conda-pack`` in a separate environment instead and follow a similar workflow.

Installing ``conda-pack`` will let you use the ``conda pack`` command which can be used to pack your conda environment into a ``.tar.gz`` file:

.. code-block:: bash

   # Pack environment located at an explicit path into my_env.tar.gz
   conda pack --format tar.gz --n-threads -1 --prefix /explicit/path/to/my_env --output ./my_env.tar.gz

After packing your environment, it can then be moved to the NVMe using ``sbcast`` when in a compute job.
Packing your environment will also put a ``conda-unpack`` script into the same ``.tar.gz`` archive.
Extracting your ``.tar.gz`` file and activating your environment will allow you to use the ``conda-unpack`` command (script) which will clean up the prefixes of the **active** environment.
Unpacking your conda environment on the NVMe using ``conda-unpack`` will make your conda environment act as if it was installed on the NVMe originally.
The next section will show an example environment on Frontier that is relocated to the NVMe using ``sbcast``.

Example Usage on Frontier
=========================

In this example, we will create a new PyTorch environment and move it to the NVMe using ``conda-pack`` and ``sbcast``.

First, let's load our modules and setup the environment:

.. code-block:: bash

   # Loading the relevant modules
   module load PrgEnv-gnu/8.6.0
   module load rocm/6.2.4
   module load craype-accel-amd-gfx90a

   # Create your conda environment
   module load miniforge3/23.11.0-0
   conda create -p $MEMBERWORK/<PROJECT_ID>/torch_env python=3.10 -c conda-forge
   source activate $MEMBERWORK/<PROJECT_ID>/torch_env

   # Install PyTorch w/ ROCm 6.2 support from pre-compiled binary
   pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.2

   # Install Conda-Pack into your environment
   conda install conda-pack -c conda-forge


Next, let's pack our new conda environment:

.. code-block:: bash

   cd $MEMBERWORK/<PROJECT_ID>
   # use all cores available for packing
   conda pack --format tar.gz --n-threads -1 --prefix $MEMBERWORK/<PROJECT_ID>/torch_env --output ./torch_env.tar.gz 

Finally, let's run a compute job:

.. code-block:: bash

   sbatch --export=NONE submit.sbatch

Below is an example batch script that uses ``sbcast``, unpacks our environment, and runs an example Python script across 8 nodes:

.. code-block:: bash

   #!/bin/bash
   #SBATCH -A PROJECT_ID
   #SBATCH -J bcast_example
   #SBATCH -o %x-%j.out
   #SBATCH -t 00:05:00
   #SBATCH -N 8
   #SBATCH -C nvme

   date
   cd $SLURM_SUBMIT_DIR

   # Only necessary if submitting like: sbatch --export=NONE ... (recommended)
   # Do NOT include this line when submitting without --export=NONE
   unset SLURM_EXPORT_ENV

   # Setup modules
   module load PrgEnv-gnu/8.6.0
   module load rocm/6.2.4
   module load miniforge3/23.11.0-0
   module load craype-accel-amd-gfx90a

   ##### START OF SBCAST AND CONDA-UNPACK #####

   # Move a copy of the env to the NVMe on each node
   echo "copying torch_env to each node in the job"
   sbcast -pf ./torch_env.tar.gz /mnt/bb/${USER}/torch_env.tar.gz
   if [ ! "$?" == "0" ]; then
       # CHECK EXIT CODE. When SBCAST fails, it may leave partial files on the compute nodes, and if you continue to launch srun,
       # your application may pick up partially complete shared library files, which would give you confusing errors.
       echo "SBCAST failed!"
       exit 1
   fi

   # Untar the environment file (only need 1 task per node to do this)
   srun -N8 --ntasks-per-node 1 mkdir /mnt/bb/${USER}/torch_env
   echo "untaring torchenv"
   srun -N8 --ntasks-per-node 1 -c56 tar --use-compress-program=pigz -xf /mnt/bb/${USER}/torch_env.tar.gz -C  /mnt/bb/${USER}/torch_env

   # Unpack the env
   source activate /mnt/bb/${USER}/torch_env
   srun -N8 --ntasks-per-node 1 conda-unpack

   ##### END OF SBCAST AND CONDA-UNPACK #####

   # Run the Python script
   srun --unbuffered -l -N 8 -n 64 -c7 --ntasks-per-node=8 --gpus-per-node=8 --gpus-per-task=1 --gpu-bind=closest python3 example.py

   # Gather timings of each slurm jobstep
   sacct -j ${SLURM_JOBID} -o jobid%20,Start%20,elapsed%20

**The key parts of the above batch script are:**

* Using the ``#SBATCH -C nvme`` line makes sure that you'll get access to the NVMe (accessible at ``/mnt/bb/<userid>``)
* The ``sbcast`` line broadcasts the ``torch_env.tar.gz`` file to the NVMe on each node
* You must make a directory on each NVMe first before extracting the tar file to that directory on each node
* Unpacking the environment on each node's NVMe will make sure each node has access to the new "cleaned" environment

To show the benefit this method provides, let's see how it affects the timings of running our example script:

.. code-block:: python

   import os
   import torch
   import torch.distributed as dist

   def report_env():
       rocr_devices = os.getenv("ROCR_VISIBLE_DEVICES")
       hip_devices = os.getenv("HIP_VISIBLE_DEVICES")
       cuda_visible_devices = os.getenv("CUDA_VISIBLE_DEVICES")
       torch_version = torch.__version__
       cuda_available = torch.cuda.is_available()
       curr_device = torch.cuda.current_device()
       device_arch = str(torch.cuda.get_device_name(torch.cuda.current_device()))
       cuda_version = torch.version.cuda
       hip_version = torch.version.hip
       bf16_support = torch.cuda.is_bf16_supported()
       nccl_available = torch.distributed.is_nccl_available()
       nccl_version = torch.cuda.nccl.version()
       print(f"Torch version: {torch_version}")
       print(f"CUDA available: {cuda_available} ")
       print(f"CUDA version: {cuda_version} ")
       print(f"HIP  version: {hip_version} ")
       print(f"current device: {curr_device} ")
       print(f"device arch name: {device_arch} ")
       print(f"BF16 support: {bf16_support} ")
       print(f"NCCL available: {nccl_available} ")
       print(f"NCCL version: {nccl_version} ")
       print(f"ROCR_VISIIBLE_DEVICES: {rocr_devices} ")
       print(f"HIP_VISIBLE_DEVICES: {hip_devices} ")
       print(f"CUDA_VISIBLE_DEVICES: {cuda_visible_devices} ")

   def main():
       report_env()

   if __name__ == "__main__":
       main()

Here are the timings from the ``sbcast`` **NVMe** run:

.. code-block::

             JobID            Start               Elapsed
   --------------- ---------------- ---------------------
           jobid      .             00:01:17
     jobid.batch      .             00:01:17
    jobid.extern      .             00:01:17
         jobid.0      .             00:00:00 mkdir 
         jobid.1      .             00:00:39 untar
         jobid.2      .             00:00:03 conda unpack
         jobid.3      .             00:00:02 example.py



Here are the timings if the environment was never broadcast from **Orion**:

.. code-block::

             JobID            Start              Elapsed
   --------------- ---------------- --------------------
           jobid      .             00:00:57
     jobid.batch      .             00:00:57
    jobid.extern      .             00:00:57
         jobid.0      .             00:00:51 example.py

Here are the timings if the environment was stored on **NFS** and never broadcast:

.. code-block::

             JobID            Start              Elapsed
   --------------- ---------------- --------------------
           jobid      .             00:04:04
     jobid.batch      .             00:04:04
    jobid.extern      .             00:04:04
         jobid.0      .             00:03:56 example.py

The big takeaway is the execution time of ``example.py``, showing that NVMe > Orion >> NFS when it comes to where your conda environment is located before running the script.
Recall, this example was just at 8 nodes and would likely provide more benefit as the node count increases and when using more complex environments (and scripts).
Although extracting the ``tar.gz`` file introduces some overhead in the ``sbcast`` method, that overhead is small compared to the script initialization overhead in the Orion and NFS method when scaling up to higher node counts.

For more information on using ``sbcast`` on Frontier, please see the :doc:`Frontier User Guide </systems/frontier_user_guide>`.
