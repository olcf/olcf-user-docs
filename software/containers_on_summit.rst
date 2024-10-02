.. _containers-on-summit:

********************
Containers on Summit
********************

Users can build container images with Podman, convert it to a SIF file, and run the
container using the Apptainer runtime. This page is intended for users with some
familiarity with building and running containers.

Basic Information
=================

Users will make use of two applications on Summit - Podman and Apptainer - in their
container build and run workflow. Both are available without needing to load any modules.

Podman is a container framework from Red Hat that functions as a drop in replacement for
Docker. On Summit, we will use Podman for building container images and converting them
into tar files for Apptainer to use. Podman makes use of Dockerfiles to describe the
images to be built. We cannot use Podman to run
containers as it doesn't properly support MPI on Summit, and Podman does not support
storing its container images on GPFS or NFS.

Due to Podman's lack of support for storage on GPFS and NFS, container images will be
built on the login nodes using the node-local NVMe on the login node. This NVMe is mounted
in ``/tmp/containers``. Users should treat this storage as temporary. Any data (container
image layers or otherwise) in this storage will be purged if the node is ever rebooted or
when it gets full.  So any images created with Podman need to be converted to tar files
using ``podman save`` and stored elsewhere if you wish to preserve your image.

.. note::
   The NVMes on the login nodes are not shared storage across all login nodes. Each login
   node is different with an independent NVMe. So you will not find the container layers
   built on one login node to appear in another login node. Every time you login to
   Summit, the load balancer may put you on a different login node than where you were
   working on building your container. Even if you try to stick to the same login node,
   the NVMes should be treated as temporary storage as they can be purged anytime, during
   a reboot or for some other reason. It is the user's responsibility to save any in
   progress or completed container image build as a tar file or sif file before you close
   a session.

Apptainer is a container framework from Sylabs. On Summit, we will use Apptainer
solely as the runtime. We will convert the tar files of the container images Podman
creates into sif files, store those sif files on GPFS, and run them with
Jsrun. Apptainer also allows building images but ordinary users cannot utilize that on
Summit due to additional permissions not allowed for regular users.

Users will be building and running containers on Summit without root permissions
i.e. containers on Summit are rootless.  This means users can get the benefits of
containers without needing additional privileges. This is necessary for a shared system
like Summit. And this is part of the reason why Docker doesn't work on Summit. Podman and
Apptainer provides rootless support but to different extents hence why users need to use
a combination of both.



Setup before Building
=====================

Users will need to set up a file in their home directory
``/ccs/home/<username>/.config/containers/storage.conf`` with the following content:
::

   [storage]
   driver = "overlay"
   graphroot = "/tmp/containers/<user>"
   
   [storage.options]
   additionalimagestores = [
   ]
   
   [storage.options.overlay]
   ignore_chown_errors = "true"
   mount_program = "/usr/bin/fuse-overlayfs"
   mountopt = "nodev,metacopy=on"
   
   [storage.options.thinpool]

``<user>`` in the ``graphroot = "/tmp/containers/<user>"`` in the above file should be
replaced with your username. This will ensure that Podman will use the NVMe mounted in ``/tmp/containers`` for storage during container image builds.


Build and Run Workflow 
=======================

As an example, let's build and run a very simple container image to demonstrate the workflow.

Building a Simple Image
-----------------------

- Create a directory called ``simplecontainer`` on home or GPFS and ``cd`` into it.
- Create a file named ``simple.dockerfile`` with the following contents.
  ::

     FROM quay.io/rockylinux/rockylinux:9-ubi
     RUN dnf -y install epel-release && dnf -y install fakeroot
     RUN fakeroot dnf upgrade -y && fakeroot dnf update -y
     RUN fakeroot dnf install -y wget hostname libevent
     ENTRYPOINT ["/bin/bash"]

.. note::
   You will notice the use of the fakeroot command when doing package installs with dnf. This is necessary as some some package installations require root permissions on container which the container builder does not have. So fakeroot allows dnf to think it is running as root and allows the installation to succeed.

.. note::
   Apptainer requires libevent installed in any container you build in order for it to work correctly with the jsrun job launcher.

- Build the container image with ``podman build --net=host -t simple -f simple.dockerfile .``.

  * The ``-t`` flag names the container image and the ``-f`` flag indicates the file to use for building the image.

.. note::
   Podman (v4.1.1) installed on Summit requires the ``--net=host`` option when building a container otherwise it will fail.

- Run ``podman image ls`` to see the list of images. ``localhost/simple`` should be among them. Any container created without an explicit url to a container registry in its name will automatically have the ``localhost`` prefix.
  ::

     REPOSITORY                     TAG          IMAGE ID      CREATED       SIZE
     localhost/simple               latest       2b636262ca8f  7 days ago    559 MB
     quay.io/rockylinux/rockylinux  9-ubi        03e38f9b275b  8 days ago    300 MB

- Convert this Podman container image into a tar file with ``podman save -o simple.tar localhost/simple``.
- Convert the tar file into a Apptainer sif file with  ``apptainer build --disable-cache simple.sif docker-archive://simple.tar``

.. note::
   You will also notice that we use rockylinux 9-ubi as our base image in the example. If you're planning on building a container image from scratch instead of using the OLCF MPI base image , use a rockylinux 9-ubi image with fakeroot installed as demonstrated above as your starting point (we talk about the OLCF MPI base image later in the :ref:`olcf-mpi-base-image` section). Ubuntu would be difficult to use as a starting point since ``apt-get`` requires root from the get-go, and you can't even do a ``apt-get -y fakeroot`` to get you started. Other distributions haven't been tested. Using rockylinux for this case for now is the most user friendly option).


Using a Container Registry to Build and Save your Images
--------------------------------------------------------

If you are familiar with using a container registry like DockerHub, you can use that to save your Podman container images
and use Apptainer to pull from the registry and build the sif file. Below, we will use DockerHub as the example but there are many
other container registries that you can use.

- Using the ``simple`` example from the previous section, build the container image with ``podman build --net=host -t docker.io/<username>/simple -f simple.dockerfile .`` where ``<username>`` is your user on DockerHub.

  - ``podman push`` uses the URL in the container image's name to push to the appropriate registry.

- Check if your image is created
  ::

     $ podman image ls
     REPOSITORY                         TAG      IMAGE ID      CREATED      SIZE
     docker.io/subilabrahamornl/simple  latest   e47dbfde3e99  3 hours ago  687 MB
     localhost/simple                   latest   e47dbfde3e99  3 hours ago  687 MB
     quay.io/rockylinux/rockylinux      9-ubi    03e38f9b275b  8 days ago   300 MB
     
- Run ``podman login docker.io`` and enter your account's username and password so that Podman is logged in to the container registry before pushing.

- Push the container image to the registry with ``podman push docker.io/<username>/simple``.

-  You can now create a Apptainer sif file with ``apptainer build --disable-cache --docker-login simple.sif docker://docker.io/<username>/simple``.

   - This will ask you to enter your Docker username and password again for Apptainer to download the image from Dockerhub and convert it to a sif file.

.. note::
   The reason we include the ``--disable-cache`` flag is because Apptainer's caching can
   fill up your home directory without you realizing it. And if the home directory is
   full, Apptainer builds will fail. If you wish to make use of the cache, you can set
   the environment variable
   ``APPTAINER_CACHEDIR=/tmp/containers/<user>/apptainercache`` or something like that
   so that the NVMe storage is used as the cache.

Running a Simple Container in a Batch Job
-----------------------------------------

As a simple example, we will run ``hostname`` with the Apptainer container.

- Create a file submit.lsf with the contents below.
  ::

     #!/bin/bash
     # Begin LSF Directives
     #BSUB -P STF007
     #BSUB -W 0:10
     #BSUB -q debug
     #BSUB -nnodes 1
     #BSUB -J simple_container_job
     #BSUB -o simple_container_job.%J
     #BSUB -e simple_container_job.%J

     jsrun -n2 apptainer exec ./simple.sif hostname

- Submit the job with ``bsub submit.lsf``. This should produce an output that looks like:
  ::

     h41n08
     h41n08

  Here, Jsrun starts 2 separate Apptainer container runtimes since we pass the -n2 flag to start two processes. Each Apptainer container runtime then loads the container image simple.sif and executes the ``hostname`` command from that container. If we had requested 2 nodes in the batch script and had run ``jsrun -n2 -r1 apptainer exec ./simple.sif hostname``, Jsrun would've started a Apptainer runtime on each node and the output would look something like 
  ::

     h41n08
     h41n09

.. note::
   You may encounter the following in your output ``INFO:    /etc/apptainer/ exists; cleanup by system administrator is not complete (see https://apptainer.org/docs/admin/latest/apptainer_migration.html)``. This is caused by the Apptainer project being renamed to Apptainer. Please ignore the above output. It should not affect any containers you run.

.. _olcf-mpi-base-image:

Running an MPI program with the OLCF MPI base image
--------------------------------------------------- 

Creating Apptainer containers that run MPI programs require a few additional steps. 

OLCF provides an MPI base image that you can use for MPI programs. You can pull it with Podman with ``podman pull code.ornl.gov:4567/olcfcontainers/olcfbaseimages/mpiimage-centos-cuda``


Let's build an simple MPI example container using the prebuilt MPI base image from the repository.

- Create a new directory ``mpiexample``.
- Create a file ``mpiexample.c`` with the following contents.
  ::

     #include <stdio.h>
     #include <mpi.h>
     
     int main (int argc, char *argv[])
     {
     int rank, size;
     MPI_Comm comm;
     
     comm = MPI_COMM_WORLD;
     MPI_Init (&argc, &argv);
     MPI_Comm_rank (comm, &rank);
     MPI_Comm_size (comm, &size);
     
     printf("Hello from rank %d\n", rank);
     
     MPI_Barrier(comm);
     MPI_Finalize();
     }

- Create a file named ``mpiexample.dockerfile`` with the following contents
  ::

     FROM code.ornl.gov:4567/olcfcontainers/olcfbaseimages/mpiimage-centos-cuda:latest
     RUN mkdir /app
     COPY mpiexample.c /app
     RUN cd /app && mpicc -o mpiexample mpiexample.c

- The MPI base image was compiled using the system gcc (v8.5.0).
  So run the following commands to build the Podman image and convert it to the Apptainer format.
  ::

     module purge
     module load DefApps
     module unload xl
     module -t list
     podman build --net=host -v $MPI_ROOT:$MPI_ROOT -f mpiexample.dockerfile -t mpiexample:latest .;
     podman save -o mpiexampleimage.tar localhost/mpiexample:latest;
     apptainer build --disable-cache mpiexampleimage.sif docker-archive://mpiexampleimage.tar;

- It's possible the ``apptainer build`` step might get killed due to reaching cgroup memory limit. To get around this, you can start an interactive job and build the apptainer image with
  ::

     jsrun -n1 -c42 -brs apptainer build --disable-cache mpiexampleimage.sif docker-archive://mpiexampleimage.tar;

  (remember to do the above in ``/gpfs`` or specify the full path for the sif file somewhere in GPFS. If you try to save the sif file in your home directory you will error out because NFS is read-only from the compute nodes).


- Create the following submit script submit.lsf. Make sure you replace the ``#BSUB -P STF007`` line with your own project ID.
  ::

     #BSUB -P STF007
     #BSUB -W 0:30
     #BSUB -nnodes 2
     #BSUB -J apptainer
     #BSUB -o apptainer.%J
     #BSUB -e apptainer.%J
     
     module purge
     module load DefApps
     module unload xl
     
     source /gpfs/alpine2/stf243/world-shared/containers/utils/requiredmpilibs.source
     
     jsrun -n 8 -r4  apptainer exec --bind $MPI_ROOT:$MPI_ROOT,/autofs/nccs-svm1_home1,/autofs/nccs-svm1_home1:/ccs/home mpiexampleimage.sif /app/mpiexample
     
     # uncomment the below to run the preinstalled osubenchmarks from the container.
     #jsrun -n 8 -r 4 apptainer exec --bind $MPI_ROOT:$MPI_ROOT,/autofs/nccs-svm1_home1,/autofs/nccs-svm1_home1:/ccs/home mpiexampleimage.sif /osu-micro-benchmarks-5.7/mpi/collective/osu_allgather


You can view the Dockerfiles used to build the MPI base image at the `code.ornl.gov
repository <https://code.ornl.gov/olcfcontainers/olcfbaseimages>`_. These Dockerfiles are
buildable on Summit yourself by cloning the repository and running the ``./build`` in the
individual directories in the repository. This allows you the freedom to modify these base
images to your own needs if you don't need all the components in the base images. You may
run into the cgroup memory limit when building so kill the podman process, log out, and
try running the build again if that happens when building.



Running a single node GPU program with the OLCF MPI base image
--------------------------------------------------------------

Apptainer provides the ability to access the GPUs from the containers, allowing you to containerize GPU programs. 
The OLCF provided MPI base image already has CUDA libraries preinstalled and can be used for CUDA programs as well. You can pull it with Podman with ``podman pull code.ornl.gov:4567/olcfcontainers/olcfbaseimages/mpiimage-centos-cuda``. 

.. note::
   The OLCF provided MPI base image currently has CUDA 11.7.1 and CuDNN 8.5. If these don't fit your needs, you can build your own base image by modifying the files from the `code.ornl.gov repository <https://code.ornl.gov/olcfcontainers/olcfbaseimages>`_.

Let's build an simple CUDA example container using the MPI base image from the repository.

- Create a new directory ``gpuexample``.

- Create a file ``cudaexample.cu`` with the following contents
  ::

     #include <stdio.h>
     #define N 1000
     
     __global__
     void add(int *a, int *b) {
         int i = blockIdx.x;
         if (i<N) {
             b[i] = 2*a[i];
         }
     }
     
     int main() {
         int ha[N], hb[N];
     
         int *da, *db;
         cudaMalloc((void **)&da, N*sizeof(int));
         cudaMalloc((void **)&db, N*sizeof(int));
     
         for (int i = 0; i<N; ++i) {
             ha[i] = i;
         }
     cudaMemcpy(da, ha, N*sizeof(int), cudaMemcpyHostToDevice);

     add<<<N, 1>>>(da, db);

     cudaMemcpy(hb, db, N*sizeof(int), cudaMemcpyDeviceToHost);

     for (int i = 0; i<N; ++i) {
         if(i+i != hb[i]) {
             printf("Something went wrong in the GPU calculation\n");
         }
     }
     printf("COMPLETE!");
          cudaFree(da);
          cudaFree(db);
      
          return 0;
     }


- Create a file named ``gpuexample.dockerfile`` with the following contents
  ::

     FROM code.ornl.gov:4567/olcfcontainers/olcfbaseimages/mpiimage-centos-cuda:latest
     RUN mkdir /app
     COPY cudaexample.cu /app
     RUN cd /app && nvcc -o cudaexample cudaexample.cu


- Run the following commands to build the container image with Podman and convert it to Apptainer
  :: 
     
     podman build --net=host -f gpuexample.dockerfile -t gpuexample:latest .;
     podman save -o gpuexampleimage.tar localhost/gpuexample:latest;
     apptainer build --disable-cache gpuexampleimage.sif docker-archive://gpuexampleimage.tar;


- It's possible the ``apptainer build`` step might get killed due to reaching cgroup memory limit. To get around this, you can start an interactive job and build the apptainer image with
  ::

     jsrun -n1 -c42 -brs apptainer build --disable-cache gpuexampleimage.sif docker-archive://gpuexampleimage.tar;

  (remember to do this in /gpfs or specify the full path for the sif file somewhere in
  GPFS. If you try to save the sif file in your home directory you will error out because
  NFS is read-only from the compute nodes).


- Create the following submit script submit.lsf. Make sure you replace the ``#BSUB -P
  STF007`` line with your own project ID.
  ::

     #BSUB -P STF007
     #BSUB -W 0:30
     #BSUB -nnodes 1
     #BSUB -J apptainer
     #BSUB -o apptainer.%J
     #BSUB -e apptainer.%J
     
     module unload spectrum-mpi

     jsrun -n 1 -c 1 -g 1 apptainer exec --nv gpuexampleimage.sif /app/cudaexample

  The ``--nv`` flag is needed to tell Apptainer to make use of the GPU.


Running a CUDA-Aware MPI program with the OLCF MPI base image
-------------------------------------------------------------

You can run containers with CUDA-aware MPI as well. CUDA-aware MPI allows transferring GPU
data with MPI without needing to copy the data over to CPU memory first. Read more
:ref:`CUDA-Aware MPI`.

.. note::
   Due to spectrum-mpi not supporting CUDA >=12 or gcc/12, the provided CUDA-Aware images were built with CUDA 11.7.1 and the system GCC (v8.5.0).
   Users are welcome to try and use newer versions of CUDA or GCC but they are not supported.

Let's build and run a container that will demonstrate CUDA-aware MPI. 

- Create a new directory ``cudaawarempiexample``.

- Run the below wget commands to obtain the example code and Makefile from the `OLCF
  tutorial example page <https://github.com/olcf-tutorials/MPI_ping_pong>`_.

  ::

     wget -O Makefile https://raw.githubusercontent.com/olcf-tutorials/MPI_ping_pong/master/cuda_aware/Makefile
     wget -O ping_pong_cuda_aware.cu https://raw.githubusercontent.com/olcf-tutorials/MPI_ping_pong/master/cuda_aware/ping_pong_cuda_aware.cu

- Create a file named ``cudaawarempiexample.dockerfile`` with the following contents
  ::

     FROM code.ornl.gov:4567/olcfcontainers/olcfbaseimages/mpiimage-centos-cuda:latest
     RUN mkdir /app
     COPY ping_pong_cuda_aware.cu Makefile /app
     RUN cd /app && make

- Run the following commands to build the container image with Podman and convert it to Apptainer
  :: 
     
     module purge
     module load DefApps
     module unload xl
     module load cuda/11.7.1
     module -t list
     podman build --net=host --build-arg mpi_root=$MPI_ROOT -v $MPI_ROOT:$MPI_ROOT -f cudaawarempiexample.dockerfile -t cudaawarempiexample:latest .;
     podman save -o cudaawarempiexampleimage.tar localhost/cudaawarempiexample:latest;
     apptainer build --disable-cache cudaawarempiexampleimage.sif docker-archive://cudaawarempiexampleimage.tar;


- It's possible the ``apptainer build`` step might get killed due to reaching cgroup memory limit. To get around this, you can start an interactive job and build the apptainer image with
  ::

     jsrun -n1 -c42 -brs apptainer build cudaawarempiexampleimage.sif docker-archive://cudaawarempiexampleimage.tar;

  (remember to do this in /gpfs or specify the full path for the sif file somewhere in
  GPFS. If you try to save the sif file in your home directory you will error out because
  NFS is read-only from the compute nodes).


- Create the following submit script submit.lsf. Make sure you replace the ``#BSUB -P STF007`` line with your own project ID.
  ::

     #BSUB -P STF007
     #BSUB -W 0:30
     #BSUB -nnodes 2
     #BSUB -J apptainer
     #BSUB -o apptainer.%J
     #BSUB -e apptainer.%J
     
     module purge
     module load DefApps
     module unload xl
     module load cuda/11.7.1
     
     source /gpfs/alpine2/stf243/world-shared/containers/utils/requiredmpilibs.source
     
     jsrun --smpiargs="-gpu" -n 2 -a 1 -r 1 -c 42 -g 6 apptainer exec --nv --bind $MPI_ROOT:$MPI_ROOT,/autofs/nccs-svm1_home1,/autofs/nccs-svm1_home1:/ccs/home cudaawarempiexampleimage.sif /app/pp_cuda_aware
 
 

  The ``--nv`` flag is needed to tell Apptainer to make use of the GPU.

Tips, Tricks, and Things to Watch Out For
=========================================

- Run ``podman system prune`` and then run ``podman image rm --force $(podman image ls
  -aq)`` several times to clean out all the dangling images and layers if you want to do a
  full reset.
- Sometimes you may want to do a full purge of your container storage area. Your user
  should own all the files in your ``/tmp/containers`` location. Recursively add write
  permissions to all files by running ``chmod -R +w /tmp/containers/<username>`` and then
  run ``rm -r /tmp/containers/<username>``.
- Sometimes you may need to kill your podman process because you may have gotten killed
  due to hitting cgroup limit. You can do so with ``pkill podman``, then log out and log
  back in to reset your cgroup usage.
- If you already have a "image.tar" file created with ``podman save`` from earlier that
  you are trying to replace, you will need to delete it first before running any other
  ``podman save`` to replace it. ``podman save`` won't overwrite the tar file for you.
- Not using the ``--disable-cache`` flag in your ``apptainer build`` commands could
  cause your home directory to get quickly filled by apptainer caching image data. You
  can set the cache to a location in ``/tmp/containers`` with ``export
  APPTAINER_CACHEDIR=/tmp/containers/<username>/apptainercache`` if you want to avoid
  using the ``--disable-cache`` flag.
- If you see an error that looks something like ``ERRO[0000] stat /run/user/16248: no such
  file or directory`` or ``Error: Cannot connect to the Podman socket, make sure there is
  a Podman REST API service running.: error creating tmpdir: mkdir /run/user/12341:
  permission denied``, try logging out and logging back in. If that fails, then after
  logging in run ``ssh login<number>`` where login<number> is the login node you are
  currently logged in to. If all else fails, write to the help@olcf.ornl.gov and we can
  see if the issue can be fixed from there.
- If you're trying to mount your home directory with ``--bind
  /ccs/home/<user>:/ccs/home/<user>`` in your ``apptainer exec`` command, it might not
  work correctly. ``/ccs/home/user`` is an alias to ``/autofs/nccs-svm1_home1/user`` or
  ``/autofs/nccs-svm1_home2/user``. You can find out which one is yours with ``stat
  /ccs/home/user`` and then mount your home directory with ``--bind
  /autofs/nccs-svm1_home1/user:/ccs/home/user`` to make ``/ccs/home/user`` visible within
  your container.
