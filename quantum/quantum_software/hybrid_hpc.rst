.. _hybrid-hpc:

*******************************
Quantum Software on HPC Systems
*******************************

Overview
========

This page describes how a user can successfully install specific quantum
software tools to run on select OLCF HPC systems. This allows a user to utilize
our systems to run a simulator, or even as a "frontend" to a vendor's quantum
machine ("backend").

For most of these instructions, we use conda environments. For more detailed
information on how to use Python modules and conda environments on OLCF
systems, see our :doc:`Python on OLCF Systems page</software/python/index>`, 
and our :doc:`Conda Basics guide </software/python/conda_basics>`.

Example Python scripts for each QCUP vendor are located at our new :doc:`/quantum/hello_qcup` page.

.. note::
   Working installations are **not** limited to versions shown below.
   Versions for libraries listed below are what was tested most recently.

Qiskit
======

`Qiskit <https://quantum.cloud.ibm.com/docs/guides>`__ is open-source software for
working with quantum computers at the level of circuits, pulses, and
algorithms.
Installing Qiskit provides access to the IBM Quantum backends by default, but
installing additional provider plugins enables access to other vendors' backends as well.

IBM Quantum
-----------

Installing ``qiskit`` and ``qiskit-ibm-runtime`` provides access to IBM Quantum backends.
Since cloud-based simulators have been deprecated, installing ``qiskit-aer`` enables access to local simulators.

See these links for more information:

* `<https://quantum.cloud.ibm.com/docs/guides/install-qiskit>`__
* `<https://quantum.cloud.ibm.com/docs/guides/hello-world>`__
* `<https://quantum.cloud.ibm.com/docs/guides/local-testing-mode>`__
* `<https://quantum.cloud.ibm.com/docs/guides/execution-modes>`__

.. tab-set::

    .. tab-item:: Andes
       :sync: andes

        .. code-block:: bash

            module load gcc/9.3.0
            module load miniforge3/24.11.3-2
            conda create -n ENV_NAME python=3.11 -c conda-forge
            conda activate ENV_NAME
            conda install qiskit=1.2.0 qiskit-ibm-runtime=0.28.0 qiskit-aer=0.14.2 psutil -c conda-forge

    .. tab-item:: Frontier
       :sync: frontier

        .. code-block:: bash

            module load PrgEnv-gnu/8.6.0
            module load miniforge3/23.11.0-0
            conda create -n ENV_NAME python=3.11 -c conda-forge
            conda activate ENV_NAME
            conda install qiskit=1.4.1 qiskit-ibm-runtime=0.36.1 qiskit-aer=0.16.2 psutil -c conda-forge


Qiskit IonQ Provider
--------------------

The ``qiskit-ionq`` extension can be installed to access IonQ QPUs through Qiskit.

See these links for more information:

* `<https://docs.ionq.com/>`__
* `<https://ionq.com/resources>`__
* `<https://ionq.com/resources/anthology/developers/hello-many-worlds-in-7-quantum-languages>`__
* `<https://docs.ionq.com/guides/managing-api-keys>`__
* `<https://docs.ionq.com/guides/sdks/qiskit>`__

.. tab-set::

    .. tab-item:: Andes
       :sync: andes

        .. code-block:: bash

            module load gcc/9.3.0
            module load miniforge3/24.11.3-2
            conda create -n ENV_NAME python=3.11 numpy=1.26.4 scipy -c conda-forge
            conda activate ENV_NAME
            pip install qiskit==1.2.0 qiskit-ionq==0.5.4 --no-cache-dir

    .. tab-item:: Frontier
       :sync: frontier

        .. code-block:: bash

            module load PrgEnv-gnu/8.6.0
            module load miniforge3/23.11.0-0
            conda create -n ENV_NAME python=3.11 -c conda-forge
            conda activate ENV_NAME
            pip install qiskit==1.4.1 qiskit-ionq==0.5.12 --no-cache-dir


IQM Qiskit Plugin
-----------------

The ``qiskit-iqm`` plugin can be installed to access IQM's backends through Qiskit.

See these links for more information:

* `<https://docs.iqm.tech/iqm-client/user_guide_qiskit.html>`__

.. tab-set::

    .. tab-item:: Andes
       :sync: andes

        .. code-block:: bash

            module load gcc/9.3.0
            module load miniforge3/24.11.3-2
            conda create -n ENV_NAME python=3.11 -c conda-forge
            conda activate ENV_NAME
            pip install qiskit-iqm==15.5 --no-cache-dir

    .. tab-item:: Frontier
       :sync: frontier

        .. code-block:: bash

            module load PrgEnv-gnu/8.6.0
            module load miniforge3/23.11.0-0
            conda create -n ENV_NAME python=3.11 -c conda-forge
            conda activate ENV_NAME
            pip install qiskit-iqm==17.5 --no-cache-dir



PennyLane
=========

`PennyLane <https://pennylane.ai/>`__ is a cross-platform Python
library for programming quantum computers.  Its differentiable programming
paradigm enables the execution and training of quantum programs on various
backends.

General information of how to install and use PennyLane can be found here:

* `<https://docs.pennylane.ai/en/stable/introduction/pennylane.html>`__
* `<https://pennylane.ai/qml/demonstrations/>`__
* `<https://pennylane.ai/install/>`__
* `<https://docs.pennylane.ai/en/stable/index.html>`__

.. tab-set::

    .. tab-item:: Andes
       :sync: andes

        .. code-block:: bash

            module load gcc/9.3.0
            module load miniforge3/24.11.3-2
            conda create -n ENV_NAME python=3.11 pennylane -c conda-forge
            conda activate ENV_NAME

    .. tab-item:: Frontier
       :sync: frontier

        On Frontier, PennyLane can be built with the `Lightning Kokkos Simulator <https://docs.pennylane.ai/projects/lightning/en/latest/lightning_kokkos/device.html>`__.
        This allows PennyLane to use MPI and AMD GPUs on Frontier for distributed simulation.

        Recipe for building PennyLane Lightning Kokkos with ROCm 7.1.1 (also known to work with ROCm 6.2.4, 6.4.2, and 7.0.2):

        .. code-block:: bash

            # Load modules
            module load PrgEnv-amd/8.7.0
            module load cpe/26.03
            module load miniforge3/23.11.0-0
            module load amd/7.1.1 rocm/7.1.1
            module load cmake ninja

            # Because using a non-default CPE module
            export LD_LIBRARY_PATH=$CRAY_LD_LIBRARY_PATH:$LD_LIBRARY_PATH

            # Create initial conda env
            conda create -n ENV_NAME python=3.12 -c conda-forge
            conda activate ENV_NAME

            # Download Kokkos
            wget https://github.com/kokkos/kokkos/archive/refs/tags/5.1.0.tar.gz
            tar -xvf 5.1.0.tar.gz
            cd kokkos-5.1.0/

            # Install Kokkos (choose an installation path)
            export KOKKOS_INSTALL_PATH=<install-path>
            cmake -S . -B build -G Ninja \
                -DCMAKE_BUILD_TYPE=Release \
                -DCMAKE_INSTALL_PREFIX=$KOKKOS_INSTALL_PATH \
                -DCMAKE_CXX_STANDARD=20 \
                -DCMAKE_CXX_COMPILER=hipcc \
                -DBUILD_SHARED_LIBS:BOOL=ON \
                -DBUILD_TESTING:BOOL=ON \
                -DKokkos_ENABLE_SERIAL:BOOL=ON \
                -DKokkos_ENABLE_HIP:BOOL=ON \
                -DKokkos_ARCH_AMD_GFX90A:BOOL=ON \
                -DKokkos_ENABLE_COMPLEX_ALIGN:BOOL=OFF \
                -DKokkos_ENABLE_EXAMPLES:BOOL=OFF \
                -DKokkos_ENABLE_TESTS:BOOL=OFF \
                -DKokkos_ENABLE_LIBDL:BOOL=OFF

            cmake --build build && cmake --install build
            export CMAKE_PREFIX_PATH=$KOKKOS_INSTALL_PATH

            # Clone PennyLane Lightning Repo
            cd
            git clone https://github.com/PennyLaneAI/pennylane-lightning.git
            cd pennylane-lightning

            # skip following step if using "main" development branch for latest features
            git checkout v0.45.0

            # Install dependencies
            python -m pip install --group base

            # First, install PennyLane
            # change "v0.45.0" to "main" if using main development branch for latest features
            # version must match pennylane-lightning
            pip install git+https://github.com/PennyLaneAI/pennylane.git@v0.45.0

            # Next, install PennyLane Lightning
            PL_BACKEND="lightning_qubit" python scripts/configure_pyproject_toml.py
            CMAKE_ARGS="-DCMAKE_CXX_COMPILER=CC" pip install . -vv

            # Extra MPI flags for optimized inter-GPU communication
            export MPI_EXTRA_LINKER_FLAGS="${CRAY_XPMEM_POST_LINK_OPTS} -lxpmem ${PE_MPICH_GTL_DIR_amd_gfx90a} ${PE_MPICH_GTL_LIBS_amd_gfx90a}"

            # CMAKE variables for building Lightning-Kokkos with MPI
            export CMAKE_ARGS="-DENABLE_MPI=ON -DCMAKE_CXX_COMPILER=hipcc"

            # Lastly, install PennyLane Lightning-Kokkos with MPI support
            PL_BACKEND="lightning_kokkos" python scripts/configure_pyproject_toml.py
            python -m pip install . -vv

        .. note::
            Different compilers and optimization flags dramatically affect performance of Lightning-Kokkos.
            We observed significant performance degradation when compiling with ``amdclang++`` and ``CMAKE_BUILD_TYPE`` set to ``RelWithDebugInfo``.
            For optimal results, we recommend using either ``hipcc`` in general, or ``amdclang++`` with ``CMAKE_BUILD_TYPE`` specifically set to ``Release``.

        .. warning::
            At runtime, you'll need to have these environment variables set: ``MPICH_GPU_SUPPORT_ENABLED=1`` and ``HSA_ENABLE_PEER_SDMA=0``


Pytket
======

The tket framework is a software platform for the development and execution of gate-level quantum computation, providing state-of-the-art performance in circuit compilation.
`Pytket <https://tket.quantinuum.com/api-docs/>`__ is a python module for interfacing with tket, and installing the `Quantinuum pytket extension <https://cqcl.github.io/pytket-quantinuum/api/>`__ allows pytket circuits to be executed on Quantinuum's quantum devices.

For more information please see:

* `<https://tket.quantinuum.com/api-docs/>`__
* `<https://cqcl.github.io/pytket-quantinuum/api/>`__
* `<https://tket.quantinuum.com/api-docs/getting_started.html>`__
* `<https://docs.quantinuum.com/h-series/trainings/getting_started/pytket_quantinuum/pytket_quantinuum.html>`__

.. tab-set::

    .. tab-item:: Andes
       :sync: andes

        .. code-block:: bash

            module load gcc/9.3.0
            module load miniforge3/24.11.3-2
            conda create -n ENV_NAME python=3.11 numpy=1.26.4 -c conda-forge
            conda activate ENV_NAME
            pip install pytket==1.31.1 pytket-quantinuum==0.37.0 scipy --no-cache-dir

    .. tab-item:: Frontier
       :sync: frontier

        .. code-block:: bash

            module load PrgEnv-gnu/8.6.0
            module load miniforge3/23.11.0-0
            conda create -n ENV_NAME python=3.11 -c conda-forge
            conda activate ENV_NAME
            pip install pytket==1.41.0 qnexus==0.11.0 --no-cache-dir



Batch Jobs
==========

Although lightweight code can be run on the login nodes, more computationally
intensive code should be run on the compute nodes through the use of a batch
job.  See the relevant :doc:`HPC System Guide </systems/index>` for more examples
and best practices when running on the compute nodes for a given system.

For the compute nodes to be able to access external URLs (e.g., trying to
connect to IBM backends), you'll have to use proxy settings in your batch
script:

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

To submit a batch script:

.. code-block:: bash

    $ sbatch submit.sl


Below are example batch scripts for running on Andes and Frontier:

.. tab-set::

    .. tab-item:: Andes
       :sync: andes

        .. code-block:: bash

            #!/bin/bash
            #SBATCH -A ABC123
            #SBATCH -J job_name
            #SBATCH -N 1
            #SBATCH -t 0:05:00
            #SBATCH -p batch

            cd $SLURM_SUBMIT_DIR
            date

            # Set proxy settings so compute nodes can reach internet (required when not using a simulator)
            export all_proxy=socks://proxy.ccs.ornl.gov:3128/
            export ftp_proxy=ftp://proxy.ccs.ornl.gov:3128/
            export http_proxy=http://proxy.ccs.ornl.gov:3128/
            export https_proxy=http://proxy.ccs.ornl.gov:3128/
            export no_proxy='localhost,127.0.0.0/8,*.ccs.ornl.gov'

            # Load python module and virtual environment
            module load miniforge3/24.11.3-2
            conda activate ENV_NAME

            # For software like Qiskit,PennyLane,Pytket
            #python3 script.py


    .. tab-item:: Frontier
       :sync: frontier

        .. code-block:: bash

            #!/bin/bash
            #SBATCH -A ABC123
            #SBATCH -J job_name
            #SBATCH -N 1
            #SBATCH -t 0:05:00
            #SBATCH -p batch

            cd $SLURM_SUBMIT_DIR
            date

            # Set proxy settings so compute nodes can reach internet (required when not using a simulator)
            export all_proxy=socks://proxy.ccs.ornl.gov:3128/
            export ftp_proxy=ftp://proxy.ccs.ornl.gov:3128/
            export http_proxy=http://proxy.ccs.ornl.gov:3128/
            export https_proxy=http://proxy.ccs.ornl.gov:3128/
            export no_proxy='localhost,127.0.0.0/8,*.ccs.ornl.gov'

            # Load python module and virtual environment
            module load miniforge3/23.11.0-0
            conda activate ENV_NAME

            # For PennyLane Lightning Kokkos
            #export MPICH_GPU_SUPPORT_ENABLED=1
            #export HSA_ENABLE_PEER_SDMA=0

            # For software like Qiskit,PennyLane,Pytket
            #srun ... python3 script.py


.. note::
     The ``socks`` proxy specification depends on implementation.
     Packages that depend on ``httpx`` will need ``httpx[socks]`` and the following change:

     .. code-block:: bash

         # specify socks version
         export all_proxy=socks5://proxy.ccs.ornl.gov:3128/



