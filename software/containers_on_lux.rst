:tocdepth: 3

.. _containers-on-lux:

*****************
Containers on Lux
*****************

Apptainer v1.5.3 is installed on Lux. Apptainer can be used for both building
and running containers on Lux. The main user documentation on how to use Apptainer
can be found `here <https://apptainer.org/docs/user/main/index.html>`__. This section of our documentation
will only cover any additional info that you might need to build and run containers correctly
on Lux, as well as any useful examples.


.. note::

   If you find something that you were doing on Lux is no longer working, check back here to see if
   the documentation has been updated with new instructions, otherwise let us know at
   help@olcf.ornl.gov. And `contributions to the documentation are always welcome
   <https://docs.olcf.ornl.gov/contributing/index.html>`_!



Examples for Building and Running Containers
--------------------------------------------

These examples will walk you through the common things you need to know on how to use 
containers on Lux. Some of the examples will refer to files in the
`olcf_containers_examples Github repository <https://github.com/olcf/olcf_containers_examples/>`_.

Building and running a container image from a base Linux distribution for MPI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Lux provides both OpenMPI 5.x and MPICH 5.x as options for MPI runtimes. In this example 
This example will walk through building up a container image with MPICH 5.0.1 and ROCm 7.14.1 for a GPU aware MPI code.

* Clone the ``olcf_containers_examples`` repository

  ::

     git clone https://github.com/olcf/olcf_containers_examples/

* Navigate to ``lux/gpu_aware_mpi_example``
* In that directory, the ``ubuntumpich501rocm7141_minimal.def`` is an Apptainer definition file that will build a container image with MPICH 5.0.1 and ROCm 7.14.1, along with copying the ``ping_pong_gpu_aware.cpp`` file from the directory into the container image, and then compiling it.


* If you would like to inspect and make changes to the definition file to modify what the container has, feel free to do so. Inspect the definition file to understand how we build MPICH and ROCm inside the container.
  * We are installing MPICH 5.0.1 in the container to match the mpich/5.0.1 module available on Lux.

* To build the container image (the SIF file), run

  ::

     apptainer build ubuntumpich501rocm7141_minimal.sif ubuntumpich501rocm7141_minimal.def

* Apptainer builds the container image in the SIF file format. Unlike Podman, Apptainer gives you a single file for your image that you can later run as your container.

* Submit the ``submit.sbatch`` job script to launch the container with srun and run the
  ``ping_pong_gpu_aware.exe`` that was built in the container to perform the ping-pong communication
  across two nodes. This batch script has a few sruns:
  * One will run an MPI program that sends messages back and forth between two MPI processes on the same node.
  * The remaining will run the same MPI program across two MPI processes across two nodes.
  * Remember to replace the ``#SBATCH -Astf007`` with your project ID.
  * If you inspect the ``submit.sbatch`` file, you will see some modules being loaded as well as some environment variables being set. Read the comment above each for the explanations. These environment variables are required in order to run containerized MPI applications with Apptainer, with communication performance close to native and to provide GPU aware MPI.


Pushing your Apptainer image to an OCI Registry supporting ORAS (e.g. DockerHub)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

One of the benefits of containers is their portability that enables easy transfer between
computing environments. Thus, after building containers on Lux and other OLCF
systems, a way to distribute them is by pushing the image to an OCI container registry. An
Apptainer image (a SIF file) is not an OCI image so it cannot be pushed to Dockerhub or
another OCI registry as an OCI image. It can be pushed to an OCI registry that supports
`ORAS <https://oras.land/docs/>`_ as an OCI artifact instead. In this section, we
highlight and provide an example of pushing the container image we built to DockerHub as
an OCI artifact. We will use our opensusempich342rocm571.sif image from the section above
in this example.

* First, create an account and then a repository on DockerHub to hold your image.
* Ensure you are logged in to DockerHub from apptainer. To login, run

  ::

    apptainer registry login --username <your dockerhub username> oras://registry-1.docker.io

* Push the image by running

  ::

    apptainer push <path to your sif file>/ubuntumpich501rocm724.sif  oras://registry-1.docker.io/<your docker username>/<your repo name:tag>

* Using ``oras://`` tells Apptainer to push the image to given registry as an OCI
  artifact. Not all OCI registries support ORAS. See `ORAS Adopters page <https://oras.land/adopters/>`_ for list.

.. note::
   An Apptainer image that you push this way to Dockerhub or some other registry CANNOT be used by Docker or Podman. Apptainer images are not compatible
   with Docker or Podman. You can only use it with Apptainer.

.. todo:

   Building an image on top of an existing image (local, docker image, OCI artifact)
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
   In building container images, we often have to build on an existing image. This could be a local image in ones working directory, an OCI image from an OCI registry, or Apptainer SIF file that was stored as an OCI artifact in an OCI registry. One of the benefits of building images on top of existing images is simplified and easy to follow definition files instead of single and large ones.
   
   This example will look at building a container image for testing collective communications for GPUs using RCCL. The image will be built on top of an existing image that builds ROCM and MPICH since both are required for RCCL. Specifically, MPICH 3.4.2 since Cray-mpich is compatible with it.
   
   
   * Navigate to ``frontier/containers_on_frontier_docs/rccltests`` of the previously cloned github repo.
   * The Apptainer definition file for building the RCCL container image is rcclmpich342rocm624.def.
   
     * This builds on the existing opensusempich342rocm624.sif image from a previous example. Hence, MPICH 3.4.2 and ROCm 6.2.4 are used in this image.
     * To specify that we are building this container image off the existing opensusempich342rocm624.sif image, we indicate next to the Bootstrap Keyword (under the definition file Header), localimage, for image in your workdir.
   
       ::
   
         Bootstrap: localimage
         From: ../gpu_aware_mpi_example/opensusempich342rocm624.sif
   
   * At this stage, follow the steps in the Building a container image section above for building and running the RCCL container. 
   
   .. note::
      ``docker`` and ``oras`` are other options you can specify for the ``Bootstrap`` keyword
      for images in an OCI registry like DockerHub or Quay, and for SIF files stored as OCI
      artifacts in OCI registries, respectively.
      ::
   
         Bootstrap: docker
         From: quay.io/opensuse/opensuse:15.6
   
      ::
   
         Bootstrap: oras
         From: docker.io/subilabrahamornl/opensusempich342rocm624:latest

      
Using Podman to build images and converting them to Apptainer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note::
   If you wish to use Podman, you need subuid/subgid mappings turned on for your user account. Open a help ticket by
   emailing help@olcf.ornl.gov to request this first. Your Podman images will not build otherwise. After confirming
   subuid/subgid mappings are implemented, you can log out or run ``podman system migrate`` for the changes to take
   place.

* Lux has support for building images with Podman (which functions the same as Docker). Podman supports building containers with Dockerfiles. In order to build with Podman, you must first create a file called ``storage.conf`` in ``$HOME/.config/containers`` with the appropriate settings. Run the below snippet on your command line to create the file.

    ::

       mkdir -p $HOME/.config/containers
       cat > $HOME/.config/containers/storage.conf <<EOF
       [storage]
       driver = "overlay"
       graphroot = "/tmp/${USER}-containers"
       rootless_storage_path = "/tmp/${USER}-containers"
       
       [storage.options]
       pull_options = {use_hard_links = "true", enable_partial_images = "true"}
       
       
       [storage.options.vfs]
       ignore_chown_errors = "true"
       EOF


* Once this file is created, try creating a Podman image with the Dockerfile below. 

   .. code::

      FROM ubuntu:latest
      RUN apt-get -y update && apt-get -y upgrade && apt-get -y install vim


* Build the Podman image with ``podman build --network host -t localhost/example:latest .``
* Convert the image into a tar file with ``podman save -o example.tar localhost/example:latest``
* Then convert this tar file into an Apptainer SIF file with ``apptainer build example.sif docker-archive://example.tar``


.. warning::

   * You need to convert your Podman image to the Apptainer SIF format in order to run it. We don't
     support running your container with Podman directly.
   * The Podman containers you build only exist on the login node you are on. So if you log out,
     make sure you log back in to the same login node to access your containers.
   * Since the containers are stored in /tmp, there is no guarantee they will be preserved. They can
     be deleted at any time. Make
     sure to save them to a remote registry or convert them to the Apptainer SIF format to save them
     somewhere else on the filesystem.
   * The ``--network host`` flag is required with ``podman build`` to build containers on the
     Lux login node. It will run into errors otherwise.


      

.. todo:

   Sample Applications
   -------------------
   
   Some examples of containerizing and running specific applications on Lux can be seen 
   in the  `olcf_container_examples repository
   <https://github.com/olcf/olcf_containers_examples/tree/main/frontier/sample_apps/>`__ . If you have
   suggestions for other examples you would like to see, or would like to contribute one yourself, feel
   free to open an issue or pull request on the Github page above. 


AMD DockerHub AI/ML Workload Containers on Lux
---------------------------------------------------
AMD has optimized several AI/ML frameworks to provide support on AMD hardware. Some of these frameworks are specifically equiped with ROCM backend to ensure support on AMD GPUs while others are merely equiped for standard AMD64 CPU architectures.

To ensure optimal performance on Lux, we recommend users utilize the AMD optimized AI/ML workloads from the AMD DockerHub. We demonstrate here how to access and build those images on Lux as well as tips/tricks in running the images. We focus on PyTorch, Tensorflow and Jax.

Building and Running the AMD DockerHub AI/ML Images on Lux
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
We highlight the process of building and running AMD DockerHub PyTorch, Tensorflow and Jax images on Lux. Since AMD releases several versions of these frameworks, we focus on the latest releases only for this documentation.

.. tab-set::

   .. tab-item:: PyTorch
      :sync: apptainer

      .. code:: bash

         apptainer pull pytorch_latest.sif docker://rocm/pytorch-nightly:latest

   .. tab-item:: Tensorflow
      :sync: apptainer

      .. code:: bash

         apptainer pull tensorflow_latest.sif docker://rocm/tensorflow:latest

   .. tab-item:: Jax
      :sync: apptainer

      .. code:: bash

         apptainer pull jax_latest.sif docker://rocm/jax-community:latest


The `olcf_containers_examples <https://github.com/olcf/olcf_containers_examples>`__ repository has
examples demonstrating how to use these containers on Lux. You can see an example for AMD
Pytorch container `here <https://github.com/olcf/olcf_containers_examples/tree/main/lux/pytorch/amdrocmregistry>`__


.. important::

    While OLCF demonstrates the build and usage of these container images on Lux, the images and their content are managed by AMD on their dockerhub repository.

Some Restrictions and Tips
--------------------------

* If you get an error like ``FATAL:   While performing build: conveyor failed to get: while fetching library image: cached file hash(sha256:247d71d79a3be5d59c5b83eba3210ebed215fc5da16c556445ffbe797bbe1494) and expected hash(sha256:d0c01238c6c344a460076367063fda56f8fb32569aae782c408f8d20d0920757) does not match`` when pulling an Apptainer image from an ORAS registry, try passing the flag ``--disable-cache`` flag to the ``apptainer build`` or ``apptainer pull`` command. You can also set the ``APPTAINER_CACHEDIR`` environment variable to a directory in ``/tmp``, which will also solve the problem.

.. todo:

   Debugging Applications Running in Apptainer
   -------------------------------------------
   
   
   Debugging an MPI application running in a container is a bit more complex than debugging a regular
   application. You can't directly launch a container running an MPI application with a
   debugging tool like `gdb4hpc
   <https://cpe.ext.hpe.com/docs/latest/debugging-tools/gdb4hpc/guides/getting-started.html>`__ or with
   `Linaro Forge <https://docs.olcf.ornl.gov/software/debugging/index.html#linaro-forge-ddt>`__. This
   is because the tool will start a debug session of the Apptainer runtime itself rather than the MPI
   application it is running. 
   
   There are two ways around this - using gdbserver from within the container to launch one MPI task
   (while the rest are launched normally), or attaching to the already running MPI tasks with Linaro
   Forge after the application is launched. 
   
   For the instructions below, we will be using the debugging example in the `olcf_containers_examples
   <https://github.com/olcf/olcf_containers_examples>`__ repository. Make sure you clone the repository and
   navigate to the ``frontier/containers_on_frontier_docs/debugging`` directory. Build the container
   image with ``apptainer build bcastandlammps.sif bcastandlammps.def``.
   
   
   
   Using gdbserver to debug a single MPI task
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   In this method, we are launching an containerized MPI application with multiple MPI ranks, but one
   of the ranks is started with a tool called ``gdbserver``. This sets up a debugging server that
   ``gdb`` can connect to and step through that particular rank. All the other ranks will progress as
   normal until they are blocked by communication to the rank being debugged, or an MPI barrier
   affecting all ranks. Once that is crossed, the other ranks will continue on again.
   
   The disadvantage here is that
   this is not as fully featured as a special purpose HPC debugger like Linaro Forge or gdb4hpc. You will
   not be able to switch between different ranks of your program on the fly to debug them. You can only
   debug the rank you launched with gdbserver.
   
   The below example uses a 2 node job, but it generalizes to larger jobs.
   
   1. Start a 2-node interactive job e.g. ``salloc -t 00:50:00 -A gen107 -N2 -qdebug``. Make note of
      the nodelist (run ``srun hostname | sort`` to print the list in the terminal). You will be sshing into
      the node running rank 0 later, which is usually the first node on the list.
   2. Load the container modules
   
      ::
   
        module load olcf-container-tools
        module load apptainer-enable-mpi
        module load apptainer-enable-gpu
   
   3. Modify ``launchapp.sh`` to your needs. In this example you can either debug the simple
      ``mpi_bcast`` program or LAMMPS. Comment out the lines with the program you don't want to run and
      uncomment the lines for the program you do want to run. 
   
      * ``launchapp.sh`` starts rank 0 with gdbserver and the rest of the ranks normally. You can
        change which rank is being debugged by changing the value of 0 in ``$SLURM_PROCID -eq 0`` in
        ``launchapp.sh``.
   
   4. Launch the MPI program with srun in a container
   
      ::
   
        srun -N2 -n16 --gpus-per-task=1 --gpu-bind=closest --unbuffered apptainer exec bcastandlammps.sif ./launchapp.sh
   
      You should see a message like ``Listening on port 2345``. The gdbserver is listening to that port
      on the first node in your allocation.
   
   5. In a new terminal, SSH into the first node in the nodelist and navigate to your work directory.
   6. In the new terminal, Start an apptainer shell with the container image with ``apptainer shell
      bcastandlammps.sif``, and run gdb within this container that we can then connect to the
      gdbserver.
      
      ::
   
        apptainer shell bcastandlammps.sif
        Apptainer> gdb
        (gdb) target remote 0.0.0.0:2345
   
      This is connecting to the gdbserver instance that was started. You should now be able to use
      regular gdb commands to step through your code.
   
   
   
   Using Linaro Forge to attach to an already running MPI application running from containers
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
   `OLCF supports Linaro Forge on Lux
   <https://docs.olcf.ornl.gov/software/debugging/index.html#linaro-forge-ddt>`__ . Forge's reverse
   connect feature is what is recommended for debugging regular MPI applications. However, reverse connect
   cannot be applied for a containerized MPI application. 
   
   Instead, we can use Linaro Forge to attach to the running containerized MPI ranks after the job is
   started. A process running in Apptainer is not isolated and is visible as a regular process.
   
   .. warning::
   
     Any application you want to debug must be present in the host filesystem i.e. you need to
     start a shell with ``apptainer shell`` with your container, navigate to where your source code is
     located on Lustre or in your home directory, and compile it there. Your source and application
     cannot be built as part of your container image build and stored in your image if you wish to debug it with Forge.
   
   Initial Setup
   """""""""""""
   
   
   
   Follow the steps from our `Linaro Forge DDT documentation
   <https://docs.olcf.ornl.gov/software/debugging/index.html#linaro-forge-ddt>`__ upto but not
   including the last 'Reverse Connect' section.
   
   .. note::
      
      If you wish to use the ROCm debugging feature of DDT, you need to load a rocm module in your
      ``linaro.bsh`` file. This is the file you created when you were following the steps earlier on
      the Linaro Forge documentation page for setting up Linaro Forge usage, where you set the
      ALLINEA_CONFIG_DIR and ALLINEA_REVERSE_CONNECT_DIR environment variables. So you should now have
      a file in your home directory named ``/ccs/home/<user>/linaro.bsh`` with the below contents.    
   
      :: 
        
        module load rocm
        export ALLINEA_CONFIG_DIR=<Somewhere on the Filesystem that can be accessed by the compute nodes i.e. /lustre/orion/<project>>
        export ALLINEA_REVERSE_CONNECT_DIR=<Somewhere on the Filesystem that can be accessed by the compute nodes i.e. /lustre/orion/<project>>
   
      This is necessary because DDT relies on the presence of ``rocgdb`` in your PATH. ``rocgdb`` is
      made available in your PATH when the rocm module is loaded. When Forge connects to Lux with
      Remote Launch, it runs your ``linaro.bsh`` file (provided its path was specified in the Remote
      Script box in the Remote Launch Settings when you first configured Linaro Forge to connect to Lux). So
      loading the rocm module in ``linaro.bsh`` will make sure that ``rocgdb`` is now available for Forge
      DDT to use.
   
   In your terminal logged into Lux:
   
   1. Navigate to the ``debugging`` directory in the ``olcf_containers_examples`` repository you cloned
   2. Start a 2 node interactive job e.g. ``salloc -t 00:50:00 -A gen107 -N2 -qdebug``
   3. Run the following commands to to set up modules and create a ``hostlist`` file (this will create a file with the list of hosts in your allocation. We will be making use of this in the Forge client application).
   
      ::
        
        module reset
        module load olcf-container-tools
        module load apptainer-enable-mpi
        module load apptainer-enable-gpu
        module load linaro-forge
        
        export ALLINEA_CONFIG_DIR=<some directory>
        export ALLINEA_REVERSE_CONNECT_DIR=<some directory>
        
        srun hostname > hostlist
   
   The values for ``ALLINEA_CONFIG_DIR`` and ``ALLINEA_REVERSE_CONNECT_DIR`` should be the same as what
   you set when following the initial setup steps.
   
   4. Start an apptainer shell with ``apptainer shell -e bcastandlammps.sif`` (The ``-e`` flag will
      make sure the host's environment is not inherited into the running container. The application needs to be compiled and linked
      with only the container's own environment to emulate how it would be compiled within a container
      build).
   5. In the apptainer shell, compile the ``mpi_bcast.c`` file in the current directory with ``mpicc -g -O0 -o mpi_bcast
      mpi_bcast.c`` (remember that we need to do this because the source and the application needs to
      exist on the host's filesystem even if the container is running it).
   6. Exit the apptainer shell.
   
   
   Debugging the application
   """""""""""""""""""""""""
   
   1. Make sure you have Linaro Forge client open on your workstation and connected to Lux through the Remote Launch dropdown.
   2. In your terminal running the interactive job
   
      ::
   
        srun --unbuffered -N2 -n4 apptainer exec bcastandlammps.sif ./mpi_bcast
   
      This will run the ``mpi_bcast`` executable from the current directory, but it is running within the
      container with access to the container environment.
   
   3. Switch to your Linaro Forge desktop client. Make sure you are connected to Lux through the
      Remote Launch option.
   4. Click on 'ATTACH' in the desktop client.
   5. In the window that opens, click on the 'Change MPI...' button. This will open the System Settings
      window. From the MPI/UPC Implementation dropdown, select 'none' . Click on OK.
   6. Click on the "Choose Hosts..." button. In the window that opens, click on the "Import..." button.
      This will open a directory picker where you can navigate Lux's directory tree. Navigate to
      your current working directory (i.e. the directory from where you ran ``srun``). Select the
      ``hostlist`` file you created earlier and click "Open". This will populate the list of hosts.
   7. Select the checkboxes for all the hosts, then click on OK.
   8. Click on the tab named "list of all processes" (The "Automatically-detected jobs" tab will detect the
      apptainer runtime running under srun, which is not what we want. We actually want the MPI program that is running under
      the container).
   9. Select "ROCm" under the "debug GPU" option selection if you need to do GPU debugging (make sure you have ``module load rocm``
      in your ``/ccs/home/<user>/linaro.bsh`` file. If that wasn't already set before you connected to Lux with
      Remote Launch, you will need to close Linaro Forge and reconnect).
   10. In the "Filter for process names containing:" textbox, type in "bcast" to list only the ``mpi_bcast`` processes. Select the items whose "Process name" or "Executable" is the name of the ``mpi_bcast`` executable. Do not select anything that references ``srun`` or ``apptainer``.
   
      .. figure:: /images/forge_container_process_select.png
          :align: center
          :width: 800
   
   11. Click on "Attach to Selected Processes". Forge will now start connecting to the processes. The
       execution of the application will pause once Forge is connected.
   12. You will now get the main Linaro DDT window. You may see a message here saying "Missing
       debugging information". This is not an issue.
   13. In the navigation tree on the left, click on "Sources", find the source file you want to examine
       and set breakpoints where you want to. Then click on the "Play" button (the green triangle
       button) on the toolbar at the top of the window. DDT will now progress the application across
       all processes till it hits the breakpoint.
   14. You should now be able to use DDT to debug your application.
   
   
   .. note::
   
      If you encounter errors along the way, the best thing is to close Linaro Forge and retry. That
      usually lets things proceed.

