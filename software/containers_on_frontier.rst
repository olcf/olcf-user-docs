.. _containers-on-frontier:

**********************
Containers on Frontier
**********************

Apptainer v1.3.6 is installed on Frontier. Apptainer can be used for both building
and running containers on Frontier. The main user documentation on how to use Apptainer
can be found `here <https://apptainer.org/docs/user/main/index.html>`__. This section of our documentation
will only cover any additional info that you might need to build and run containers correctly
on Frontier, as well as any useful examples.


.. note::
   This documentation is not currently stable and will change over time as we add more examples and as the best practices for containers evolve. If you find something
   that you were doing on Frontier is no longer working, check back here to see if the documentation has been
   updated with new instructions. And `contributions to the documentation are always welcome <https://docs.olcf.ornl.gov/contributing/index.html>`_!



Examples for Building and Running Containers
--------------------------------------------

These examples will walk you through the common things you need to know on how to use 
containers on Frontier. Some of the examples will refer to files in the
`olcf_containers_examples Github repository <https://github.com/olcf/olcf_containers_examples/>`_.

Building and running a container image from a base Linux distribution for MPI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example will walk through building up a container image with OpenSUSE 15.4, MPICH 3.4.2, and ROCm 5.7.1
for a GPU aware MPI code.

* Clone the ``olcf_containers_examples`` repository

  ::

     git clone https://github.com/olcf/olcf_containers_examples/

* Navigate to ``frontier/containers_on_frontier_docs/gpu_aware_mpi_example``
* In that directory, the ``opensusempich342rocm571.def`` is an Apptainer definition file that will build a container image with MPICH 3.4.2 and ROCm 5.7.1, along with copying the ``ping_pong_gpu_aware.cpp`` file from the directory into the container image, and then compiling it.

  * If you would like to inspect and make changes to the definition file to modify what the container has, feel free to do so. Inspect the definition file to understand how we build MPICH and ROCm inside the container.
  * MPICH 3.4.2 is required to be installed in your container image and build your MPI application with it if you want to run MPI on Frontier with containers. This is because cray-mpich is based on MPICH 3.4.2 and is ABI compatible. Later in the job script we will be mounting the Cray MPICH libraries into the container so that the application in the container will link and use those libraries. This is necessary for native performance.

* To build the container image (the SIF file), run
  ::

     apptainer build opensusempich342rocm624.sif opensusempich342rocm624.def


  * Apptainer builds the container image in the SIF file format. Unlike Podman, Apptainer gives you a single file for your image that you can later run as your container.

* Submit the ``submit.sbatch`` job script to launch the container with srun and run the ``ping_pong_gpu_aware.exe`` that was built in the container to perform the ping-pong communication across two nodes.

  * Remember to replace the ``#SBATCH -Astf007`` with your project ID.
  * If you inspect the ``submit.sbatch`` file, you will see some modules being loaded as well as some environment variables being set. Read the comment above each for the explanations. These environment variables are required in order to run containerized MPI applications with Apptainer, with communication performance close to native and to provide GPU aware MPI.


Pushing your Apptainer image to an OCI Registry supporting ORAS (e.g. DockerHub)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

One of the benefits of containers is their portability that enables easy transfer between
computing environments. Thus, after building containers on Frontier and other OLCF
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

    apptainer push <path to your sif file>/opensusempich342rocm624.sif  oras://registry-1.docker.io/<your docker username>/<your repo name:tag>

* Using ``oras://`` tells Apptainer to push the image to given registry as an OCI
  artifact. Not all OCI registries support ORAS. See `ORAS Adopters page <https://oras.land/adopters/>`_ for list.

.. note::
   An Apptainer image that you push this way to Dockerhub or some other registry CANNOT be used by Docker or Podman. Apptainer images are not compatible
   with Docker or Podman. You can only use it with Apptainer.

Building an image on top of an existing image (local, docker image, OCI artifact)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In building container images, we often have to build on an existing image. This could be a local image in ones working directory, an OCI image from an OCI registry, or Apptainer SIF file that was stored as an OCI artifact in an OCI registry. One of the benefits of building images on top of existing images is simplified and easy to follow definition files instead of single and large ones.

This example will look at building a container image for testing collective communications for GPUs using RCCL. The image will be built on top of an existing image that builds ROCM and MPICH since both are required for RCCL. Specifically, MPICH 3.4.2 since Cray-mpich is based on it.


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
      From: docker.io/subilabrahamornl/ope1nsusempich342rocm624:latest

OLCF Base Images & Apptainer Modules
-------------------------------------
To assist the container workflow on Frontier, OLCF provides some base container images and apptainer modules to
simplify the process. The following sections document them and provide an `Example Workflow`_.

Base Images
^^^^^^^^^^^

Due to licensing, OLCF is currently not able to provide containers with the Cray Programming Environment (CPE)
installed in them; However, we do provide a set of base container images that seek to be ABI
(Application Binary Interface) compatible. Users can download these images and build their software off-site.
When users are ready to run their containers on Frontier they can bind in CPE and run their software.

.. important::

    While OLCF seeks to make these containers compatible with CPE the compatibility is NOT guaranteed. We build the images
    with `Velocity <https://olcf.github.io/velocity/>`_. The image definitions can be found `here <https://github.com/olcf/velocity-images>`__.

.. attention::

    Due to upstream vulnerabilities from software and operating systems some provided images cannot pass required
    security scans. In these cases the image will be temporarily unavailable. We are sorry for any inconvenience that
    this causes. Users are welcome to build there own images using our build tool
    `Velocity <https://olcf.github.io/velocity/>`_ and `image definitions <https://github.com/olcf/velocity-images>`_.

.. tab-set::

   .. tab-item:: Apptainer & Singularity
      :sync: apptainer

      .. code:: bash

         apptainer pull docker://savannah.ornl.gov/olcf-container-images/cpe:<tag>

      .. code:: bash

         singularity pull docker://savannah.ornl.gov/olcf-container-images/cpe:<tag>

   .. tab-item:: Podman & Docker
      :sync: podman

      .. code:: bash

         podman pull savannah.ornl.gov/olcf-container-images/cpe:<tag>

      .. code:: bash

         docker pull savannah.ornl.gov/olcf-container-images/cpe:<tag>


.. tab-set::

   .. tab-item:: CPE/23.12
      :sync: cpe_23_12

      **Contents:**

      +---------------------------------------------------+----------------------------------------------------+
      | GNU                                               | CLANG                                              |
      +===================================================+====================================================+
      | **gcc@12.3.0** + **mpich@3.4.3** + **rocm@5.7.1** | **llvm@17.0.6** + **mpich@3.4.3** + **rocm@5.7.1** |
      +---------------------------------------------------+----------------------------------------------------+

      **Tags:**

      - ``23.12_gnu_ubuntu``
      - ``23.12_gnu_opensuse``
      - ``23.12_gnu_rockylinux``
      - ``23.12_clang_ubuntu``
      - ``23.12_clang_opensuse``
      - ``23.12_clang_rockylinux``

   .. tab-item:: CPE/24.03
      :sync: cpe_24_03

      **Contents:**

      +---------------------------------------------------+----------------------------------------------------+
      | GNU                                               | CLANG                                              |
      +===================================================+====================================================+
      | **gcc@13.2.0** + **mpich@3.4.3** + **rocm@6.0.3** | **llvm@17.0.6** + **mpich@3.4.3** + **rocm@6.0.3** |
      +---------------------------------------------------+----------------------------------------------------+

      **Tags:**

      - ``24.03_gnu_ubuntu``
      - ``24.03_gnu_opensuse``
      - ``24.03_gnu_rockylinux``
      - ``24.03_clang_ubuntu``
      - ``24.03_clang_opensuse``
      - ``24.03_clang_rockylinux``

   .. tab-item:: CPE/24.07
      :sync: cpe_24_07

      **Contents:**

      +---------------------------------------------------+----------------------------------------------------+
      | GNU                                               | CLANG                                              |
      +===================================================+====================================================+
      | **gcc@13.2.0** + **mpich@3.4.3** + **rocm@6.1.3** | **llvm@18.1.8** + **mpich@3.4.3** + **rocm@6.1.3** |
      +---------------------------------------------------+----------------------------------------------------+

      **Tags:**

      - ``24.07_gnu_ubuntu``
      - ``24.07_gnu_opensuse``
      - ``24.07_gnu_rockylinux``
      - ``24.07_clang_ubuntu``
      - ``24.07_clang_opensuse``
      - ``24.07_clang_rockylinux``

   .. tab-item:: CPE/24.11
      :selected:
      :sync: cpe_24_11

      **Contents:**

      +---------------------------------------------------+----------------------------------------------------+
      | GNU                                               | CLANG                                              |
      +===================================================+====================================================+
      | **gcc@13.2.0** + **mpich@3.4.3** + **rocm@6.2.4** | **llvm@18.1.8** + **mpich@3.4.3** + **rocm@6.2.4** |
      +---------------------------------------------------+----------------------------------------------------+

      **Tags:**

      - ``24.11_gnu_ubuntu``
      - ``24.11_gnu_opensuse``
      - ``24.11_gnu_rockylinux``
      - ``24.11_clang_ubuntu``
      - ``24.11_clang_opensuse``
      - ``24.11_clang_rockylinux``

   .. tab-item:: CPE/25.03
      :sync: cpe_25_03

      **Contents:**

      +---------------------------------------------------+----------------------------------------------------+
      | GNU                                               | CLANG                                              |
      +===================================================+====================================================+
      | **gcc@14.2.0** + **mpich@3.4.3** + **rocm@6.3.1** | **llvm@19.1.7** + **mpich@3.4.3** + **rocm@6.3.1** |
      +---------------------------------------------------+----------------------------------------------------+

      **Tags:**

      - ``25.03_gnu_ubuntu``
      - ``25.03_gnu_opensuse``
      - ``25.03_gnu_rockylinux``
      - ``25.03_clang_ubuntu``
      - ``25.03_clang_opensuse``
      - ``25.03_clang_rockylinux``

Apptainer Modules
^^^^^^^^^^^^^^^^^
.. warning::

    The modules described in this section are experimental!

To make the use of apptainer easier, OLCF provides some modules that automatically bind in the needed libraries to run
apptainer with the host mpi and rocm. To access these modules load ``olcf-container-tools``. You should then see two
modules ``apptainer-enable-mpi`` and ``apptainer-enable-gpu``.

Example Workflow
^^^^^^^^^^^^^^^^
To see how one might use these containers and modules we have an example of building and running lammps. You can
find examples for cpu and gpu lammps runs `here <https://github.com/olcf/olcf_containers_examples/tree/main/frontier/containers_on_frontier_docs/apptainer_wrappers_lammps>`__.
Clone the git repo onto Frontier (or any ``x86_64`` machine), navigate to the correct folder and run:

.. code-block::

    apptainer build lammps.sif lammps.def

After the image is built, transfer it to Frontier if it's on another machine, and run it by submitting the
``submit.slurm`` batch script that accompanies it.

.. warning::

   The modules should be loaded only for running, such as in an interactive or batch job. They should not be loaded before ``apptainer build`` due to environment variables
   it sets that interfere with the build process. If you load the modules and try to do an ``apptainer build``, you might encounter
   an error like
   ::

        FATAL:   container creation failed: mount hook function failure: mount /opt/cray->/opt/cray error: while mounting /opt/cray: destination /opt/cray doesn't exist in container



Sample Applications
-------------------

Some examples of containerizing and running specific applications on Frontier can be seen 
in the  `olcf_container_examples repository
<https://github.com/olcf/olcf_containers_examples/tree/main/frontier/sample_apps/>`__ . If you have
suggestions for other examples you would like to see, or would like to contribute one yourself, feel
free to open an issue or pull request on the Github page above. 

Some Restrictions and Tips
--------------------------

* Some packages (like ``openssh`` on an OpenSUSE container) cannot currently be installed during your container build. This is because containers are restricted to a single user id and group id. Some package installs might try to create a new user inside the container with the ``useradd`` command, which will fail. So you will need to find workarounds or alternatives for any packages that try to do this.
* The ``cray-mpich-abi`` module does not provide ``libmpicxx.so``, only ``libmpi.so`` and ``libmpifort.so``. As a hacky solution in case your application in the container needs ``libmpicxx.so`` from the host, you can create a symlink named ``libmpicxx.so`` somewhere that links to ``${CRAY_MPICH_DIR}/lib/libmpi_cray.so`` and then mount that symlink into the container (while making sure the ``${CRAY_MPICH_DIR}/lib`` location is already mounted in the container).
* If you get an error like ``FATAL:   While performing build: conveyor failed to get: while fetching library image: cached file hash(sha256:247d71d79a3be5d59c5b83eba3210ebed215fc5da16c556445ffbe797bbe1494) and expected hash(sha256:d0c01238c6c344a460076367063fda56f8fb32569aae782c408f8d20d0920757) does not match`` when pulling an Apptainer image from an ORAS registry, try passing the flag ``--disable-cache`` flag to the ``apptainer build`` or ``apptainer pull`` command. You can also set the ``APPTAINER_CACHEDIR`` environment variable to a directory in ``/tmp``, which will also solve the problem.
