.. _hello-qcup:

******************
Hello QCUP Scripts
******************

Overview
========

This page contains example "Hello World!" scripts for each Quantum Computing User Program (QCUP) vendor.
Although a given vendor may have various access options (see :doc:`/quantum/quantum_systems/index`), this page showcases how to run jobs in a local **scripting environment**.

.. warning::
   Installation instructions for the software packages needed to run each script are not provided here.
   Example ``pip`` and ``conda`` syntax for each package can be found on our :doc:`Quantum Software on HPC Systems Page </quantum/quantum_software/hybrid_hpc>`.


IBM Quantum 
===========

`Qiskit <https://docs.quantum.ibm.com/>`__ provides access to the IBM backends.

For more information please see:

* `<https://docs.quantum.ibm.com/start/install>`__
* `<https://docs.quantum.ibm.com/start/hello-world>`__
* `<https://docs.quantum.ibm.com/verify/local-testing-mode>`__
* `<https://docs.quantum.ibm.com/guides/execution-modes>`__

.. list-table:: Latest script tests
   :widths: 25 25 25 25
   :header-rows: 1

   * - ``python``
     - ``qiskit``
     - ``qiskit-ibm-runtime``
     - ``qiskit-aer``
   * - 3.11.9
     - 1.2.0
     - 0.28.0
     - 0.14.2

.. note::

   Your IBMQ API Token is listed on your IBM dashboard at `<https://quantum-computing.ibm.com/>`__.

.. tab-set::

   .. tab-item:: Remote Backend

      .. code-block:: python

         from qiskit import QuantumCircuit, transpile
         from qiskit_ibm_runtime import QiskitRuntimeService, Session, SamplerV2 as Sampler
         import time

         # Save / Load Credentials (csc431 used as example project)
         QiskitRuntimeService.save_account(channel="ibm_quantum", token="API TOKEN GOES HERE", overwrite=True)
         service = QiskitRuntimeService(channel="ibm_quantum", instance="ibm-q-ornl/ornl/csc431")

         # Get backend (csc431 used as example project)
         #backend = service.backend("backend_name_here", instance="ibm-q-ornl/ornl/csc431")
         backend = service.least_busy(simulator=False, operational=True)

         # Build circuit
         circuit = QuantumCircuit(2, 2)
         circuit.h(0)
         circuit.cx(0, 1)
         circuit.measure([0,1], [0,1])
         compiled_circuit = transpile(circuit, backend)

         # Submit job
         sampl = Sampler(mode=backend)
         job = sampl.run([compiled_circuit],shots=1000)

         # Wait for job to complete
         while str(job.status()) != "DONE":
             print("Job status is", job.status() )
             time.sleep(30)
         print("Job status is", job.status() )

         # Gather results
         result = job.result()
         probs = result[0].data.c.get_counts()

         print('PubResult: ',result[0])
         print("\nProbabilities for 00 and 11 are:",probs)

         # Draw the circuit
         print(circuit.draw())

   .. tab-item:: Local Simulator

      .. code-block:: python

         from qiskit import QuantumCircuit, transpile
         from qiskit_ibm_runtime import Session, SamplerV2 as Sampler
         from qiskit_ibm_runtime.fake_provider import FakeManilaV2
         from qiskit_aer import AerSimulator

         # Get local backend
         #backend = FakeManilaV2()
         backend = AerSimulator()

         # Build circuit
         circuit = QuantumCircuit(2, 2)
         circuit.h(0)
         circuit.cx(0, 1)
         circuit.measure([0,1], [0,1])
         compiled_circuit = transpile(circuit, backend)

         # Run the sampler job locally using AerSimulator or "Fake" Backend.
         # Session syntax is supported but ignored because local mode doesn't support sessions.
         with Session(backend=backend) as session:
             sampler = Sampler(mode=session)
             result = sampler.run([compiled_circuit],shots=1000).result()

         probs = result[0].data.c.get_counts()

         print('PubResult: ',result[0])
         print("\nProbabilities for 00 and 11 are:",probs)

         # Draw the circuit
         print(circuit.draw())

After running the above script(s), you should see something similar to:

.. code-block::

    Probabilities for 00 and 11 are: [{0: 0.51, 3: 0.49}]
         ┌───┐     ┌─┐   
    q_0: ┤ H ├──■──┤M├───
         └───┘┌─┴─┐└╥┘┌─┐
    q_1: ─────┤ X ├─╫─┤M├
              └───┘ ║ └╥┘
    c: 2/═══════════╩══╩═
                    0  1 


Quantinuum
==========

The tket framework is a software platform for the development and execution of gate-level quantum computation, providing state-of-the-art performance in circuit compilation.
`Pytket <https://tket.quantinuum.com/api-docs/>`__ is a python module for interfacing with tket, and installing the `Quantinuum pytket extension <https://cqcl.github.io/pytket-quantinuum/api/>`__ allows pytket circuits to be executed on Quantinuum's quantum devices.

For more information please see:

* `<https://tket.quantinuum.com/api-docs/>`__
* `<https://cqcl.github.io/pytket-quantinuum/api/>`__
* `<https://tket.quantinuum.com/api-docs/getting_started.html>`__
* `<https://github.com/CQCL/pytket-quantinuum/tree/main/examples>`__

.. list-table:: Latest script tests
   :widths: 33 33 34
   :header-rows: 1

   * - ``python``
     - ``pytket``
     - ``pytket-quantinuum``
   * - 3.11.9
     - 1.31.1
     - 0.37.0

.. code-block:: python

   from pytket.circuit import Circuit
   from pytket.extensions.quantinuum import QuantinuumBackend
   from pytket.backends import ResultHandle
   from pytket.backends.backendresult import BackendResult
   import json
   import time

   # Build the circuit
   circuit = Circuit(2, name="Bell Test")
   circuit.H(0)
   circuit.CX(0, 1)
   circuit.measure_all()

   # Choose your machine and login (e.g., H1-1E and CSC431 group)
   machine = "H1-1E"
   backend = QuantinuumBackend(device_name=machine, group="CSC431")
   backend.login()

   # Status of desired machine
   print(machine, "status:", QuantinuumBackend.device_state(device_name=machine))

   # List available devices
   print([x.device_name for x in QuantinuumBackend.available_devices()])

   # Compile circuit
   compiled_circuit = backend.get_compiled_circuit(circuit, optimisation_level=0)
   n_shots = 100

   # Estimate the cost (H1-1SC, H2-1SC are syntax checkers for H1-1 and H2-1)
   # Causes problems when on an HPC compute node w/ proxy settings -- advised to run separately on login node w/o proxy
   #backend.cost(compiled_circuit, n_shots=n_shots, syntax_checker="H1-1SC")

   # Run the circuit
   handle = backend.process_circuit(compiled_circuit, n_shots=n_shots)
   print(handle)

   # Save your job handle
   with open("pytket_example_job_handle.json", "w") as file:
       json.dump(str(handle), file)

   # Check status of job (loop is necessary on an HPC compute node w/ proxy settings or else timeouts occur)
   while str( backend.circuit_status(handle).status ) != "StatusEnum.COMPLETED":
       status = backend.circuit_status(handle)
       print("Job status is", status.status )
       time.sleep(10)
   status = backend.circuit_status(handle)
   print("Job status is", status )

   # Retrieve and print results
   with open("pytket_example_job_handle.json") as file:
       handle_str = json.load(file)
   handle = ResultHandle.from_str(handle_str)
   result = backend.get_result(handle)
   print(result.get_distribution())
   print(result.get_counts())

   # Save results
   with open("pytket_example.json", "w") as file:
       json.dump(result.to_dict(), file)

   # Not necesary here, but including syntax
   # Load results
   with open("pytket_example.json") as file:
       data = json.load(file)
   result = BackendResult.from_dict(data)

After running the above script, you should see something similar to:

.. code-block::

    {(0, 0): 0.57, (1, 1): 0.43}
    Counter({(0, 0): 57, (1, 1): 43})


IonQ
====

IonQ has many pathways to accessing their quantum backends.
Although the script below uses the `Qiskit IonQ Provider <https://docs.ionq.com/guides/sdks/qiskit>`__ , details on how to use Cirq, PennyLane, XACC, and more can be found in the `IonQ Documentation <https://docs.ionq.com/introduction>`__ .
One useful resource that showcases multiple access pathways is their `Hello Many Worlds <https://ionq.com/resources/anthology/developers/hello-many-worlds-in-7-quantum-languages>`__ tutorial.

For more information please see:

* `<https://docs.ionq.com/>`__
* `<https://ionq.com/resources>`__
* `<https://ionq.com/resources/anthology/developers/hello-many-worlds-in-7-quantum-languages>`__
* `<https://docs.ionq.com/guides/managing-api-keys>`__
* `<https://docs.ionq.com/guides/sdks/qiskit>`__

.. list-table:: Latest script tests
   :widths: 33 33 34
   :header-rows: 1

   * - ``python``
     - ``qiskit``
     - ``qiskit-ionq``
   * - 3.11.9
     - 1.2.0
     - 0.5.4

.. code-block:: python

    from qiskit import QuantumCircuit
    from qiskit_ionq import IonQProvider
    import os

    # Set your credentials (can also set this externally)
    os.environ["IONQ_API_KEY"] = "API KEY GOES HERE"

    # Load your IonQ credentials and list backends
    provider = IonQProvider()
    print(provider.backends())

    # Run on "ionq_simulator", "ionq_qpu", "simulator", "qpu.harmony", "qpu.aria-1", "qpu.aria-2"
    backend = provider.get_backend("simulator")

    # Create a basic Bell State circuit:
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])

    # Run the circuit on IonQ's platform:
    job = backend.run(qc, shots=10000)

    # Print results
    print(job.get_counts())
    print(job.get_probabilities())

After running the above script, you should see something similar to:

.. code-block::

    {'00': 4933, '11': 5067}
    {'00': 0.5, '11': 0.5}


Rigetti
=======

`PyQuil <https://pyquil-docs.rigetti.com/en/stable/>`__ allows you to build and execute Quil programs to run on Rigetti QPUs and QVMs.
To target QPUs/QVMs locally in a scripting environment, you'll need to `install the Quil SDK locally <https://docs.rigetti.com/qcs/getting-started/set-up-your-environment/installing-locally>`__.
An example of how to install the Quil SDK at OLCF in an HPC environment is shown on our :doc:`Quantum Software on HPC Systems Page </quantum/quantum_software/hybrid_hpc>`.

For more information please see:

* `<https://pyquil-docs.rigetti.com/en/stable/>`__
* `<https://docs.rigetti.com/qcs>`__
* `<https://docs.rigetti.com/qcs/getting-started/set-up-your-environment/installing-locally>`__
* `<https://pyquil-docs.rigetti.com/en/stable/getting_started.html#run-your-first-program>`__

.. note::
   To be able to authenticate to Rigetti via the CLI, you'll first need to download your API keys from `<https://qcs.rigetti.com/auth/token>`__.

.. list-table:: Latest script tests
   :widths: 50 50
   :header-rows: 1

   * - ``python``
     - ``pyquil``
   * - 3.11.9
     - 4.14.2

.. code-block:: python

   from pyquil import get_qc, Program
   from pyquil.gates import H, CNOT, MEASURE
   from pyquil.quilbase import Declare
   import time
   # Set up your Quantum Quil Program (in this case, a "Bell State")
   program = Program(
       Declare("ro", "BIT", 2),
       H(0),
       CNOT(0, 1),
       MEASURE(0, ("ro", 0)),
       MEASURE(1, ("ro", 1)),
   ).wrap_in_numshots_loop(10)

   # Request your QVM or QPU (e.g., Ankaa-2 QVM)
   qc = get_qc("Ankaa-2-qvm")

   # Compile, run, and print results
   # NOTE When using actual QPUs:
   # Have run into timeout issues when trying to query results too quickly after compiling when commands are on separate lines
   # But in theory they can be on separate lines (just may need to play around with the timeout parameter)
   print( qc.run( qc.compile(program) ).get_register_map().get("ro") )

With the way pyQuil works, you need to launch its compiler server, launch the virtual machine / simulator QVM server, and then launch your pyQuil Python program on the same host.
Running a Python script will ping and utilize both the compiler and QVM servers.

Thus, the script can be run like this:

.. code-block:: bash

   (ENV_NAME)$ quilc -P -S > quilc.log 2>&1 & qvm -S > qvm.log 2>&1 & python3 script.py ; kill $(jobs -p)

After running the above script, you should see something similar to:

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


