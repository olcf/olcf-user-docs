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

        .. code-block:: bash

            module load gcc/9.3.0
            module load python
            conda create -n ENV_NAME python=3.11 -c conda-forge
            source activate ENV_NAME
            conda install qiskit=1.2.0 qiskit-ibm-runtime=0.28.0 qiskit-aer=0.14.2 psutil -c conda-forge

    .. tab-item:: Frontier

        .. code-block:: bash

            module load PrgEnv-gnu/8.6.0
            module load miniforge3/23.11.0-0
            conda create -n ENV_NAME python=3.11 -c conda-forge
            source activate ENV_NAME
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

        .. code-block:: bash

            module load gcc/9.3.0
            module load python
            conda create -n ENV_NAME python=3.11 numpy=1.26.4 scipy -c conda-forge
            source activate ENV_NAME
            pip install qiskit==1.2.0 qiskit-ionq==0.5.4 --no-cache-dir

    .. tab-item:: Frontier

        .. code-block:: bash

            module load PrgEnv-gnu/8.6.0
            module load miniforge3/23.11.0-0
            conda create -n ENV_NAME python=3.11 -c conda-forge
            source activate ENV_NAME
            pip install qiskit==1.4.1 qiskit-ionq==0.5.12 --no-cache-dir


IQM Qiskit Plugin
-----------------

The ``qiskit-iqm`` plugin can be installed to access IQM's backends through Qiskit.

See these links for more information:

* `<https://iqm-finland.github.io/qiskit-on-iqm/user_guide.html>`__

.. tab-set::

    .. tab-item:: Andes

        .. code-block:: bash

            module load gcc/9.3.0
            module load python
            conda create -n ENV_NAME python=3.11 -c conda-forge
            source activate ENV_NAME
            pip install qiskit-iqm==15.5 --no-cache-dir

    .. tab-item:: Frontier

        .. code-block:: bash

            module load PrgEnv-gnu/8.6.0
            module load miniforge3/23.11.0-0
            conda create -n ENV_NAME python=3.11 -c conda-forge
            source activate ENV_NAME
            pip install qiskit-iqm==17.5 --no-cache-dir


PyQuil/Forest SDK (Rigetti)
===========================

`Quil <https://pyquil-docs.rigetti.com/en/stable/compiler.html>`__ is the
Rigetti-developed quantum instruction/assembly language.
`PyQuil <https://pyquil-docs.rigetti.com/en/stable/>`__ is a Python library for
writing and running quantum programs using Quil.

Installing pyQuil requires installing the Forest SDK. To quote Rigetti:
"pyQuil, along with quilc, the QVM, and other libraries, make up what is called
the Forest SDK". Because we don't have Docker functionality and due to normal
users not having sudo privileges, this means that you will have to install the
SDK via the "bare-bones" method. The general info below came from:

* `<https://pyquil-docs.rigetti.com/en/stable/>`__
* `<https://docs.rigetti.com/qcs>`__
* `<https://docs.rigetti.com/qcs/getting-started/set-up-your-environment/installing-locally>`__
* `<https://pyquil-docs.rigetti.com/en/stable/getting_started.html#run-your-first-program>`__

The bare-bones installation only contains the executable binaries and manual
pages, and doesn’t contain any of the requisite dynamic libraries. As such,
installation doesn’t require administrative or sudo privileges. This method of
installation requires one, through whatever means, to install shared libraries
for BLAS, LAPACK, libffi, and libzmq3. Some download methods are listed here:

* Lapack (with BLAS) download: `<http://www.netlib.org/lapack/>`__
* libffi download:

    * Older versions: `<https://sourceware.org/ftp/libffi/>`__
    * Newer: `<https://github.com/libffi/libffi/releases/>`__

* ZMQ download: `<https://github.com/zeromq/libzmq/releases>`__
* Forest SDK download: `<https://qcs.rigetti.com/sdk-downloads>`__

PyQuil - Installing Dependencies
--------------------------------

Below is an example script that will download, build, and install all dependencies for pyQuil.
**Before running the script, make sure to have these modules loaded:**

.. tab-set::

    .. tab-item:: Andes

        .. code-block:: bash

            module load gcc/9.3.0 cmake

    .. tab-item:: Frontier

        .. code-block:: bash

            module load PrgEnv-gnu/8.6.0 cmake

.. warning::
   By default this will install the libraries into your ``$HOME`` directory.
   Also note that you will be prompted where to install the Forest SDK while the script is executing (just press enter to stick with the default ``$HOME`` location when prompted).

.. code-block:: bash

    #!/bin/bash

    set -e

    WORKDIR=${HOME}/quil_build_dir
    mkdir -p ${WORKDIR} && cd ${WORKDIR}

    VERSION_LAPACK="3.10.0"
    VERSION_LIBFFI="3.4.6"
    VERSION_ZEROMQ="4.3.5"
    VERSION_FOREST="2.23.0"

    URL_LAPACK="https://github.com/Reference-LAPACK/lapack/archive/refs/tags/v${VERSION_LAPACK}.tar.gz"
    URL_LIBFFI="https://github.com/libffi/libffi/releases/download/v3.4.6/libffi-${VERSION_LIBFFI}.tar.gz"
    URL_ZEROMQ="https://github.com/zeromq/libzmq/releases/download/v4.3.5/zeromq-${VERSION_ZEROMQ}.tar.gz"
    URL_FOREST="https://downloads.rigetti.com/qcs-sdk/forest-sdk-${VERSION_FOREST}-linux-barebones.tar.bz2"

    NAME_LAPACK="lapack-${VERSION_LAPACK}"
    NAME_LIBFFI="libffi-${VERSION_LIBFFI}"
    NAME_ZEROMQ="zeromq-${VERSION_ZEROMQ}"
    NAME_FOREST="forest-sdk-${VERSION_FOREST}-linux-barebones"

    MACHINE=$(uname -m)

    INSTALL_DIR_LAPACK=$HOME/rigetti/${NAME_LAPACK}_${MACHINE}
    INSTALL_DIR_LIBFFI=$HOME/rigetti/${NAME_LIBFFI}_${MACHINE}
    INSTALL_DIR_ZEROMQ=$HOME/rigetti/${NAME_ZEROMQ}_${MACHINE}
    INSTALL_DIR_FOREST=$HOME/rigetti/forest-sdk_${VERSION_FOREST}-linux-barebones

    # download and unzip the dependencies if they don't exist
    pyquil_lib_get() {
            local gz_name="${1}.tar.gz"
            if [[ -f "${gz_name}" ]]; then
                    # continue
                    echo "${1} already downloaded"
            else
                    curl -L -o "${gz_name}" "${2}"
            fi

            if [[ -d "${1}" ]]; then
                    echo "${1} already unzipped"
            else
                    tar -xf "$gz_name"
            fi

    }

    pyquil_lib_get $NAME_LAPACK $URL_LAPACK
    pyquil_lib_get $NAME_LIBFFI $URL_LIBFFI
    pyquil_lib_get $NAME_ZEROMQ $URL_ZEROMQ

    if [[ -f "${NAME_FOREST}.tar.bz2" ]]; then
            echo "forest already downloaded"
    else
            curl -L -o "${NAME_FOREST}.tar.bz2" "${URL_FOREST}"
    fi

    if [[ -d "${NAME_FOREST}" ]]; then
            echo "forest already unzipped"
    else
            tar -xf "${NAME_FOREST}.tar.bz2"
    fi

    # install zmq
    cd $NAME_ZEROMQ
    ./configure --prefix="${INSTALL_DIR_ZEROMQ}/" --with-libsodium=no
    make
    make install
    cd $WORKDIR

    # install libffi
    cd $NAME_LIBFFI
    ./configure --prefix=$INSTALL_DIR_LIBFFI
    make
    make install
    mkdir -p $INSTALL_DIR_LIBFFI/include
    cp include/ffi*.h $INSTALL_DIR_LIBFFI/include/
    # only necessary when using libffi==3.4
    if [[ ! -f "$INSTALL_DIR_LIBFFI/lib64/libffi.so.6" ]]; then
            ln -s $INSTALL_DIR_LIBFFI/lib64/libffi.so.8 $INSTALL_DIR_LIBFFI/lib64/libffi.so.6
    fi
    cd $WORKDIR

    # install lapack
    cd $NAME_LAPACK
    mkdir -p build
    cd build
    cmake \
            -DBUILD_SHARED_LIBS=ON \
            -DCMAKE_INSTALL_LIBDIR=$INSTALL_DIR_LAPACK \
            -DCMAKE_Fortran_COMPILER=gfortran \
            -DCMAKE_C_COMPILER=gcc \
            ..

    cmake --build . -j --target install
    cd $WORKDIR

    # install forest sdk
    cd $NAME_FOREST
    ./${NAME_FOREST}.run

    echo ""
    echo "Export these variables before running pyquil, the qvm, or quilc:"
    echo "export LD_LIBRARY_PATH=\"${INSTALL_DIR_LAPACK}:\$LD_LIBRARY_PATH\""
    echo "export LD_LIBRARY_PATH=\"${INSTALL_DIR_LIBFFI}/lib64:\$LD_LIBRARY_PATH\""
    echo "export LD_LIBRARY_PATH=\"${INSTALL_DIR_ZEROMQ}/lib:\$LD_LIBRARY_PATH\""
    echo "export PATH=\"${INSTALL_DIR_FOREST}:\$PATH\""
    echo ""

    echo "You can clean up and remove ${WORKDIR} if desired"


To verify your installation, try calling ``quilc`` and ``qvm`` (after exporting your ``$PATH`` and ``$LD_LIBRARY_PATH`` with your newly installed libraries):

.. code-block:: bash

    $ quilc --version
    1.23.0 [e6c0939]
    $ qvm --version
    1.17.1 [cf3f91f]

Finally, you are ready to install pyQuil:

.. tab-set::

    .. tab-item:: Andes

        .. code-block:: bash

            module load gcc/9.3.0
            module load python
            conda create -n ENV_NAME python=3.11 numpy=1.26.4 scipy -c conda-forge
            source activate ENV_NAME
            pip install pyquil==4.14.2 pyquil-grpc-web==4.14.2 typing_extensions --no-cache-dir

    .. tab-item:: Frontier

        .. code-block:: bash

            module load PrgEnv-gnu/8.6.0
            module load miniforge3/23.11.0-0
            conda create -n ENV_NAME python=3.11 numpy=1.26.4 scipy -c conda-forge
            source activate ENV_NAME
            pip install pyquil==4.14.2 pyquil-grpc-web==4.14.2 typing_extensions --no-cache-dir


PyQuil - Setting up Servers
---------------------------

Now that everything is installed properly, the rest of the instructions follow
`Rigetti's Documentation <https://docs.rigetti.com/qcs/getting-started/set-up-your-environment/installing-locally#start-the-compiler-and-qvm>`__ .

With the way pyQuil works, you need to launch its compiler server, launch the
virtual machine / simulator QVM server, and then launch your pyQuil Python
program on the same host. Running a Python script will ping and utilize both
the compiler and QVM servers. As a proof of concept, this has been done on a
single login node and the steps are outlined below.

Using your already created ``ENV_NAME`` virtual environment (outlined above):

.. code-block:: bash

    (ENV_NAME)$ quilc -P -S > quilc.log 2>&1 & qvm -S > qvm.log 2>&1 & python3 script.py ; kill $(jobs -p)


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

On our systems, the install method is relatively simple:

.. tab-set::

    .. tab-item:: Andes

        .. code-block:: bash

            module load gcc/9.3.0
            module load python
            conda create -n ENV_NAME python=3.11 pennylane -c conda-forge
            source activate ENV_NAME

    .. tab-item:: Frontier

        .. code-block:: bash

            module load PrgEnv-gnu/8.6.0
            module load miniforge3/23.11.0-0
            conda create -n ENV_NAME python=3.11 pennylane -c conda-forge
            source activate ENV_NAME

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

        .. code-block:: bash

            module load gcc/9.3.0
            module load python
            conda create -n ENV_NAME python=3.11 numpy=1.26.4 -c conda-forge
            source activate ENV_NAME
            pip install pytket==1.31.1 pytket-quantinuum==0.37.0 scipy --no-cache-dir

    .. tab-item:: Frontier

        .. code-block:: bash

            module load PrgEnv-gnu/8.6.0
            module load miniforge3/23.11.0-0
            conda create -n ENV_NAME python=3.11 -c conda-forge
            source activate ENV_NAME
            pip install pytket==1.41.0 qnexus==0.11.0 --no-cache-dir

CUDA-Q
======

`CUDA-Q <https://github.com/NVIDIA/cuda-quantum>`__ is a software development
kit for quantum and integrated quantum-classical programming. It consists of
the CUDA-Q intermediate representation and compiler toolchain, language
expressions in Python and C++, and the ability to execute jobs either on GPUs
accelerated via cuQuantum or QPUs spanning superconducting, ion traps,
photonics, and other qubit modalities. As high-performance computing (HPC)
trends towards heterogeneous architectures, CUDA-Q enables a dynamic workflow
with a kernel-based programming model allowing users to offload onto various
backends leading to scalable hybrid applications.

Additionally, CUDA-Q is interoperable with modern parallel programming models
such as MPI, OpenMP, etc., allowing it to leverage parallelization within and
across classical compute nodes. CUDA Quantum also has a user-friendly Python
API. We will present results from simulations that leverage the multi-node
multi-gpu simulations in quantum chemistry, quantum condensed matter physics,
high energy physics, quantum machine learning, computational fluid dynamics at
scale.

For more information please see:

- Documentation: `<https://nvidia.github.io/cuda-quantum/latest/index.html>`__
- GitHub Repository: `<https://github.com/NVIDIA/cuda-quantum>`__
- General Workshops Repository: `<https://github.com/cudaq-libraries/workshops/tree/202408-cudaq>`__
- ORNL (Ascent) Workshop: `<https://github.com/justinlietz/ornl-cudaq-workshop>`__

    - `Recording <https://vimeo.com/1002774302>`__
    - `Slides <https://www.olcf.ornl.gov/wp-content/uploads/OLCF-CUDA-Q-Training.pdf>`__

CUDA-Q is available on Summit via the ``cudaq`` module.

.. tab-set::

    .. tab-item:: Summit

        .. code-block:: bash

            module use /gpfs/alpine2/world-shared/stf007/msandov1/modulefiles
            module load cudaq/0.8.0


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


When using Python environments with SLURM, it is always recommended to submit a
batch script using the ``export=NONE`` flag to avoid ``$PATH`` issues and use
``unset SLURM_EXPORT_ENV`` in your job script (before calling ``srun``);
however, this means that previously set environment variables are **NOT**
passed into the batch job, so you will have to set them again (and load modules
again) if they are required by your workflow. Alternatively, you can try
submitting your batch script from a fresh login shell.

.. code-block:: bash

    $ sbatch --export=NONE submit.sl


Below are example batch scripts for running on Andes and Frontier:

.. tab-set::

    .. tab-item:: Andes

        .. code-block:: bash

            #!/bin/bash
            #SBATCH -A ABC123
            #SBATCH -J job_name
            #SBATCH -N 1
            #SBATCH -t 0:05:00
            #SBATCH -p batch

            unset SLURM_EXPORT_ENV

            cd $SLURM_SUBMIT_DIR
            date

            # Set proxy settings so compute nodes can reach internet (required when not using a simulator)
            export all_proxy=socks://proxy.ccs.ornl.gov:3128/
            export ftp_proxy=ftp://proxy.ccs.ornl.gov:3128/
            export http_proxy=http://proxy.ccs.ornl.gov:3128/
            export https_proxy=http://proxy.ccs.ornl.gov:3128/
            export no_proxy='localhost,127.0.0.0/8,*.ccs.ornl.gov'

            # Load python module and virtual environment
            module load python
            source activate ENV_NAME

            # For software like Qiskit,PennyLane,Pytket
            #python3 script.py

            # For pyQuil
            #export LD_LIBRARY_PATH="/ccs/home/YOUR_USERNAME/lapackblas:$LD_LIBRARY_PATH"
            #export LD_LIBRARY_PATH="/ccs/home/YOUR_USERNAME/ffi/lib64:$LD_LIBRARY_PATH"
            #export LD_LIBRARY_PATH="/ccs/home/YOUR_USERNAME/zmq/lib:$LD_LIBRARY_PATH"
            #export PATH="/ccs/home/YOUR_USERNAME/rigetti/forest-sdk_2.23.0-linux-barebones:$PATH"
            #quilc -P -S > quilc.log 2>&1 & qvm -S > qvm.log 2>&1 & python3 script.py ; kill $(jobs -p)

    .. tab-item:: Frontier

        .. code-block:: bash

            #!/bin/bash
            #SBATCH -A ABC123
            #SBATCH -J job_name
            #SBATCH -N 1
            #SBATCH -t 0:05:00
            #SBATCH -p batch

            unset SLURM_EXPORT_ENV

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
            source activate ENV_NAME

            # For software like Qiskit,PennyLane,Pytket
            #python3 script.py

            # For pyQuil
            #export LD_LIBRARY_PATH="/ccs/home/YOUR_USERNAME/lapackblas:$LD_LIBRARY_PATH"
            #export LD_LIBRARY_PATH="/ccs/home/YOUR_USERNAME/ffi/lib64:$LD_LIBRARY_PATH"
            #export LD_LIBRARY_PATH="/ccs/home/YOUR_USERNAME/zmq/lib:$LD_LIBRARY_PATH"
            #export PATH="/ccs/home/YOUR_USERNAME/rigetti/forest-sdk_2.23.0-linux-barebones:$PATH"
            #quilc -P -S > quilc.log 2>&1 & qvm -S > qvm.log 2>&1 & python3 script.py ; kill $(jobs -p)




