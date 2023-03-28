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

Currently, Crusher and Frontier do **NOT** have Anaconda/Conda modules.  To use
conda, you will have to download and install Miniconda on your own
(see `Miniconda Documentation <https://docs.conda.io/en/latest/miniconda.html>`__).
Alternatively, you can use Python's inherent virtual environments ``venv``
feature with the ``cray-python`` module instead, which is what we use below.
For more details on ``venv``, see `Python's Official Documentation
<https://docs.python.org/3/tutorial/venv.html>`__.  Contact help@olcf.ornl.gov
if conda is required for your workflow, or if you have any issues.

.. warning::

    Currently, the install steps listed below only work for our x86_64 based
    systems (Andes, Crusher, Frontier, etc.). The steps can be explored on Summit,
    but -- due to Summit's Power architecture -- is not recommended or guaranteed
    to work.

.. note::

    Both Qiskit and pyQuil can live in the same Python environment if desired.
    However, as this may not always be the case, it is highly recommened to use
    separate environments if possible or test if packages still function after
    modifying your environment.


Qiskit
======

`Qiskit <https://qiskit.org/documentation/>`__ is open-source software for
working with quantum computers at the level of circuits, pulses, and
algorithms.

Installing Qiskit provides access to the IBM backends. Due to the simple nature
of installing Qiskit, most of this info was taken directly from their documentation.
See these links for more details:

* `<https://qiskit.org/documentation/getting_started.html>`__
* `<https://qiskit.org/documentation/intro_tutorial1.html>`__
* `<https://github.com/Qiskit/qiskit-ibmq-provider#configure-your-ibm-quantum-credentials>`__
* `<https://quantum-computing.ibm.com/lab/docs/iql/manage/account/ibmq>`__

.. tabbed:: Andes

    .. code-block:: bash

        $ module load python
        $ source activate base
        $ conda create -n ENV_NAME python=3.9 # works for python 3.7, 3.8, 3.9 (minimal support for 3.10)
        $ conda activate ENV_NAME
        $ pip install numpy qiskit matplotlib --no-cache-dir

.. tabbed:: Crusher

    .. code-block:: bash

        ## Load cray-python module
        $ module load cray-python

        ## Create a virtual environment called ENV_NAME
        $ python3 -m venv ENV_NAME

        ## Activate the virtual environment
        $ source ENV_NAME/bin/activate

        ## Install numpy, qiskit, matplotlib
        (ENV_NAME)$ python3 -m pip install numpy qiskit matplotlib --no-cache-dir


Qiskit - Code Example
---------------------

Below is a simple code example to test if things installed properly.  Note that
methods for either using Qiskit as a simulator or on an actual IBM backend
(lines 10 through 29) are listed.

.. note::

    Your IBMQ API Token is listed on your IBM dashboard at `<https://quantum-computing.ibm.com/>`__ .

.. code-block:: python
    :linenos:

    import numpy as np
    import time
    from qiskit import IBMQ
    from qiskit import QuantumCircuit, transpile
    from qiskit.providers.aer import QasmSimulator
    from qiskit.visualization import plot_histogram
    from qiskit.providers.jobstatus import JobStatus
     
     
    #### IF YOU HAVE AN IBMQ ACCOUNT (using an actual backend) #####
     
    # Add your IBMQ account credentials (found on IBM dashboard)
    IBMQ.save_account('API_TOKEN_GOES_HERE') # only needs to be run once
    IBMQ.load_account()
     
    # List your IBM "providers" (similar to OLCF projects)
    print(IBMQ.providers())
     
    # Set the provider you want to use
    # Note: 'ibm-q' hub (the default IBM hub) does not require a "project", but the 'ibm-q-ornl' hub (the ORNL QCUP hub) does
    my_provider = IBMQ.get_provider(hub='ibm-q-ornl', project='csc431')
     
    # List your available "backends" from the set provider (the actual machines)
    print(my_provider.backends())
     
    # Set the machine you want to use (must be listed in above printout)
    backend = my_provider.get_backend('ibmq_qasm_simulator')
     
    ######################################
     
    # Use Aer's qasm_simulator (works even without IBMQ account, don't have to wait in a queue)
    backend = QasmSimulator()
     
    # Create a Quantum Circuit acting on the q register
    circuit = QuantumCircuit(2, 2)
     
    # Add a H gate on qubit 0
    circuit.h(0)
     
    # Add a CX (CNOT) gate on control qubit 0 and target qubit 1
    circuit.cx(0, 1)
     
    # Map the quantum measurement to the classical bits
    circuit.measure([0,1], [0,1])
     
    # compile the circuit down to low-level QASM instructions
    # supported by the backend (not needed for simple circuits)
    compiled_circuit = transpile(circuit, backend)
     
    # Execute the circuit on the qasm simulator
    job = backend.run(compiled_circuit, shots=1000)
     
    # Make a "waiting in queue" message
    while job.status() is not JobStatus.DONE:
        print("Job status is", job.status() )
        time.sleep(30)
     
    print("Job status is", job.status() )
     
    # Grab results from the job
    result = job.result()
     
    # Returns counts
    counts = result.get_counts(compiled_circuit)
    print("\nTotal count for 00 and 11 are:",counts)
     
    # Draw the circuit
    print(circuit.draw())

.. note::

    Although the above script shows you how to use your IBMQ account
    credentials to reach an IBM backend (lines 10-29), the above code instead runs
    using the built-in QASM simulator by default so that you don't have to wait in
    a queue. To use the actual IBM machines, you would just comment out line number
    32.


After running the above script using your Qiskit environment, you should
see something like this:

.. code-block::

    Job status is JobStatus.DONE
     
    Total count for 00 and 11 are: {'11': 491, '00': 509}
         ┌───┐     ┌─┐  
    q_0: ┤ H ├──■──┤M├───
         └───┘┌─┴─┐└╥┘┌─┐
    q_1: ─────┤ X ├─╫─┤M├
              └───┘ ║ └╥┘
    c: 2/═══════════╩══╩═
                    0  1


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

* `<https://pyquil-docs.rigetti.com/en/stable/start.html>`__
* `<https://docs.rigetti.com/qcs/getting-started/installing-locally>`__

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

Below are example instructions for installing the above packages into your ``$HOME`` directory.
Versions may vary.

.. warning::

    Newer versions than those used in the install instructions below are
    known to work on Andes; however, on Crusher, newer versions of libffi than
    3.2.1 are known to cause problems.

.. tabbed:: Andes

    .. code-block:: bash

        $ module load gcc cmake

.. tabbed:: Crusher

    .. code-block:: bash

        $ module swap PrgEnv-cray PrgEnv-gnu
        $ module load cmake


.. code-block:: bash

    # INSTALLING LAPACK (also installs BLAS)
    $ cd
    $ mkdir pack_temp/
    $ cd pack_temp/
    $ cp ../lapack-3.10.0.tar.gz .
    $ tar -xvf lapack-3.10.0.tar.gz
    $ cd lapack-3.10.0/
    $ mkdir build
    $ cd build/
    $ cmake -DBUILD_SHARED_LIBS=ON -DCMAKE_INSTALL_LIBDIR=$HOME/lapackblas ..
    $ cmake --build . -j --target install
     
    # INSTALLING LIBFFI
    $ cd
    $ mkdir ffi_temp/
    $ cd ffi_temp/
    $ cp ../libffi-3.2.1.tar.gz .
    $ tar -xvf libffi-3.2.1.tar.gz
    $ cd libffi-3.2.1
    $ ./configure --prefix=$HOME/ffi/
    $ make
    $ make install
    # The lines below may not be necessary if the "include" directory already exists (required for libffi3.2.1)
    $ cd $HOME/ffi/
    $ mkdir include
    $ cd include
    $ cp $HOME/ffi_temp/libffi-3.2.1/include/ffi*.h .
     
    # INSTALLING ZMQ
    $ cd
    $ mkdir zmq_temp/
    $ cd zmq_temp/
    $ cp ../zeromq-4.1.4.tar.gz .
    $ tar -xvf zeromq-4.1.4.tar.gz
    $ cd zeromq-4.1.4/
    $ ./configure --prefix=$HOME/zmq/ --with-libsodium=no
    $ make
    $ make install
     
    # INSTALLING FOREST SDK (installs quilc and qvm)
    $ cd
    $ mkdir forest_temp/
    $ cd forest_temp/
    $ cp ../forest-sdk-2.23.0-linux-barebones.tar.bz2 .
    $ tar -xvf forest-sdk-2.23.0-linux-barebones.tar.bz2
    $ cd forest-sdk-2.23.0-linux-barebones/
    $ ./forest-sdk-2.23.0-linux-barebones.run # /ccs/home/YOUR_USERNAME/rigetti/ when prompted
     
    # EXPORT PATHS (can add to .bashrc / .bash_profile if desired)
    $ export LD_LIBRARY_PATH="/ccs/home/YOUR_USERNAME/lapackblas:$LD_LIBRARY_PATH"
    $ export LD_LIBRARY_PATH="/ccs/home/YOUR_USERNAME/ffi/lib64:$LD_LIBRARY_PATH"
    $ export LD_LIBRARY_PATH="/ccs/home/YOUR_USERNAME/zmq/lib:$LD_LIBRARY_PATH"
    $ export PATH="/ccs/home/YOUR_USERNAME/rigetti/forest-sdk_2.23.0-linux-barebones:$PATH"
     
    # VERIFY QUILC / QVM INSTALL
     
    $ quilc —-version
    1.23.0 [e6c0939]
    $ qvm —-version
    1.17.1 [cf3f91f]

    # If QUILC / QVM errors and is unable to find libffi.so.6 (e.g., you have libffi.so.8)
    # This workaround is NOT recommended, and should only be used as a LAST RESORT:
    #$ ln -s $HOME/ffi/lib64/libffi.so.8 $HOME/ffi/lib64/libffi.so.6


Feel free to remove the ``[package name]_temp`` build directories once you
verify that the libraries were installed correctly.

Finally, you are ready to install pyQuil:

.. tabbed:: Andes

    .. code-block:: bash

        $ module load python
        $ source activate base
        $ conda create -n ENV_NAME python=3.9 # pyQuil requires Python version 3.7, 3.8, or 3.9
        $ conda activate ENV_NAME
        $ pip install pyquil --no-cache-dir

.. tabbed:: Crusher

    .. code-block:: bash

        ## Load cray-python module
        $ module load cray-python

        ## Create a virtual environment called ENV_NAME
        $ python3 -m venv ENV_NAME

        ## Activate the virtual environment
        $ source ENV_NAME/bin/activate

        ## Install pyquil
        (ENV_NAME)$ python3 -m pip install pyquil --no-cache-dir


PyQuil - Setting up Servers
---------------------------

Now that everything is installed properly, the rest of the instructions follow
`Rigetti's Documentation <https://docs.rigetti.com/qcs/getting-started/installing-locally#start-the-compiler-and-qvm>`__ .

With the way pyQuil works, you need to launch its compiler server, launch the
virtual machine / simulator QVM server, and then launch your pyQuil Python
program on the same host. Running a Python script will ping and utilize both
the compiler and QVM servers. As a proof of concept, this has been done on a
single login node and the steps are outlined below.

Using your already created ``ENV_NAME`` virtual environment (outlined above):

.. code-block:: bash

    (ENV_NAME)$ quilc -P -S > quilc.log 2>&1 & qvm -S > qvm.log 2>&1 & python3 script.py ; kill $(jobs -p)

.. note::

    Before trying to run the code example below, remember to set the relevant
    PATHs to your ``ffi``, ``zmq``, ``lapack``, and ``forest-sdk`` installations if
    you have not already exported them (outlined above).


PyQuil - Code Example
---------------------

Below is a simple code to test if packages installed properly.
Context for this example: `<https://pyquil-docs.rigetti.com/en/latest/start.html#run-your-first-program>`__

.. code-block:: python
    :linenos:

    from pyquil import get_qc, Program
    from pyquil.gates import H, CNOT, MEASURE
    from pyquil.quilbase import Declare
     
    # Set up your Quantum Quil Program (in this case, a "Bell State")
    program = Program(
        Declare("ro", "BIT", 2),
        H(0),
        CNOT(0, 1),
        MEASURE(0, ("ro", 0)),
        MEASURE(1, ("ro", 1)),
    ).wrap_in_numshots_loop(10)
     
    # Set up your QVM
    qc = get_qc("2q-qvm") # Ask for a QVM with two qubits and generic topology
     
    # Compile and Run (pings your Quilc and QVM servers)
    print(qc.run(qc.compile(program)).readout_data.get("ro"))


After running the above script, you should see something similar to this:

.. code-block::

    [[1 1]
     [0 0]
     [1 1]
     [0 0]
     [1 1]
     [0 0]
     [1 1]
     [1 1]
     [1 1]
     [0 0]]


PennyLane
=========

`PennyLane <https://pennylane.ai/index.html>`__ is a cross-platform Python
library for programming quantum computers.  Its differentiable programming
paradigm enables the execution and training of quantum programs on various
backends.

General information of how to install and use PennyLane can be found here:

* `<https://docs.pennylane.ai/en/stable/introduction/pennylane.html>`__
* `<https://pennylane.ai/qml/demos_getting-started.html>`__
* `<https://pennylane.ai/install.html>`__

On our systems, the install method is relatively simple:

.. tabbed:: Andes

    .. code-block:: bash

        $ module load python
        $ source activate base
        $ conda create -n ENV_NAME python=3.9 pennylane -c conda-forge
        $ conda activate ENV_NAME

.. tabbed:: Crusher

    .. code-block:: bash

        ## Load cray-python module
        $ module load cray-python

        ## Create a virtual environment called ENV_NAME
        $ python3 -m venv ENV_NAME

        ## Activate the virtual environment
        $ source ENV_NAME/bin/activate

        ## Install pennylane
        (ENV_NAME)$ python3 -m pip install pennylane --upgrade --no-cache-dir


PennyLane - Code Example
------------------------

.. code-block:: python
    :linenos:

    import pennylane as qml
    from pennylane import numpy as np

    dev1 = qml.device("default.qubit", wires=1)

    @qml.qnode(dev1)
    def circuit(phi1, phi2):
        qml.RX(phi1, wires=0)
        qml.RY(phi2, wires=0)
        return qml.expval(qml.PauliZ(0))

    def cost(x, y):
        return np.sin(np.abs(circuit(x,y))) - 1

    print(circuit(0.54, 0.12))

After running the python script, if everything installed properly, you should get something like:

.. code-block::

    0.8515405859048367


Batch Jobs
==========

Although lightweight code can be run on the login nodes, more computationally
intensive code should be run on the compute nodes through the use of a batch
job.  See the relevant :doc:`System Guide </systems/index>` for more examples
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

.. warning::

    These settings currently do not work for pyQuil; thus, when running pyQuil
    on the compute nodes, you are unable to connect to Rigetti's machines and can
    only run local simulators. To be able to connect to Rigetti's machines, you'll
    have to run on the login nodes instead.


When using Python environments with SLURM, it is always recommended to submit a
batch script using the ``export=NONE`` flag to avoid ``$PATH`` issues and use
``unset SLURM_EXPORT_ENV`` in your job script (before calling ``srun``);
however, this means that previously set environment variables are **NOT**
passed into the batch job, so you will have to set them again (and load modules
again) if they are required by your workflow. Alternatively, you can try
submitting your batch script from a fresh login shell.

.. code-block:: bash

    $ sbatch --export=NONE submit.sl


Below are example batch scripts for running on Andes and Crusher:

.. tabbed:: Andes

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
        # Currently, does not work properly with pyQuil
        export all_proxy=socks://proxy.ccs.ornl.gov:3128/
        export ftp_proxy=ftp://proxy.ccs.ornl.gov:3128/
        export http_proxy=http://proxy.ccs.ornl.gov:3128/
        export https_proxy=http://proxy.ccs.ornl.gov:3128/
        export no_proxy='localhost,127.0.0.0/8,*.ccs.ornl.gov'

        # Load python module and virtual environment
        module load python
        source activate base
        conda activate ENV_NAME

        # For software like Qiskit and PennyLane
        #python3 script.py

        # For pyQuil
        #export LD_LIBRARY_PATH="/ccs/home/YOUR_USERNAME/lapackblas:$LD_LIBRARY_PATH"
        #export LD_LIBRARY_PATH="/ccs/home/YOUR_USERNAME/ffi/lib64:$LD_LIBRARY_PATH"
        #export LD_LIBRARY_PATH="/ccs/home/YOUR_USERNAME/zmq/lib:$LD_LIBRARY_PATH"
        #export PATH="/ccs/home/YOUR_USERNAME/rigetti/forest-sdk_2.23.0-linux-barebones:$PATH"
        #quilc -P -S > quilc.log 2>&1 & qvm -S > qvm.log 2>&1 & python3 script.py ; kill $(jobs -p)

.. tabbed:: Crusher

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
        # Currently, does not work properly with pyQuil
        export all_proxy=socks://proxy.ccs.ornl.gov:3128/
        export ftp_proxy=ftp://proxy.ccs.ornl.gov:3128/
        export http_proxy=http://proxy.ccs.ornl.gov:3128/
        export https_proxy=http://proxy.ccs.ornl.gov:3128/
        export no_proxy='localhost,127.0.0.0/8,*.ccs.ornl.gov'

        # Load python module and virtual environment
        module load cray-python
        source $HOME/ENV_NAME/bin/activate

        # For software like Qiskit and PennyLane
        #python3 script.py

        # For pyQuil
        #export LD_LIBRARY_PATH="/ccs/home/YOUR_USERNAME/lapackblas:$LD_LIBRARY_PATH"
        #export LD_LIBRARY_PATH="/ccs/home/YOUR_USERNAME/ffi/lib64:$LD_LIBRARY_PATH"
        #export LD_LIBRARY_PATH="/ccs/home/YOUR_USERNAME/zmq/lib:$LD_LIBRARY_PATH"
        #export PATH="/ccs/home/YOUR_USERNAME/rigetti/forest-sdk_2.23.0-linux-barebones:$PATH"
        #quilc -P -S > quilc.log 2>&1 & qvm -S > qvm.log 2>&1 & python3 script.py ; kill $(jobs -p)


    .. note::

        The above assumes you created your Python ``venv`` ``ENV_NAME`` in your ``$HOME`` directory.


