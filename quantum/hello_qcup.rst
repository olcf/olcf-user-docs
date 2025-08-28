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

`Qiskit <https://quantum.cloud.ibm.com/docs/guides>`__ provides access to the IBM backends.

For more information please see:

* `<https://quantum.cloud.ibm.com/docs/guides/install-qiskit>`__
* `<https://quantum.cloud.ibm.com/docs/guides/hello-world>`__
* `<https://quantum.cloud.ibm.com/docs/guides/local-testing-mode>`__
* `<https://quantum.cloud.ibm.com/docs/guides/execution-modes>`__

.. list-table:: Latest script tests
   :widths: 25 25 25 25
   :header-rows: 1

   * - ``python``
     - ``qiskit``
     - ``qiskit-ibm-runtime``
     - ``qiskit-aer``
   * - 3.12.0
     - 2.1.2
     - 0.41.1
     - 0.17.1

.. note::

   You can create an IBMQ API Token from your IBM Cloud dashboard at `<https://quantum.cloud.ibm.com/>`__,
   or view previously created tokens at `<https://cloud.ibm.com/iam/apikeys>`__.

   Additionally, you will need a Cloud Resource Name (CRN) for your IBM Quantum project.
   You can find this on the "Instances" page in your IBM Quantum dashboard at `<https://quantum.cloud.ibm.com/instances>`__.

.. tab-set::

   .. tab-item:: Remote Backend

      .. code-block:: python

         from qiskit import QuantumCircuit, transpile
         from qiskit_ibm_runtime import QiskitRuntimeService, Session, SamplerV2 as Sampler
         import time

         # Save / Load Credentials
         QiskitRuntimeService.save_account(channel="ibm_cloud", token="API TOKEN GOES HERE", overwrite=True, instance="CRN GOES HERE")
         service = QiskitRuntimeService(channel="ibm_cloud", instance="CRN GOES HERE")

         # Get backend
         #backend = service.backend("backend_name_here")
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

.. note::
    
    The platform that ``pytket-quantinuum`` serves is being depreciated March 31, 2025 and will be replaced by Quantinuum Nexus.
    ``pytket-quantinuum`` will continue to function, but won't be able to target new Quantinuum Nexus devices.

The tket framework is a software platform for the development and execution of gate-level quantum computation, providing state-of-the-art performance in circuit compilation.
`Pytket <https://tket.quantinuum.com/api-docs/>`__ is a python module for interfacing with tket, and installing the `Quantinuum pytket extension <https://cqcl.github.io/pytket-quantinuum/api/>`__ allows pytket circuits to be executed on Quantinuum's quantum devices.

Quantinuum Nexus is a cloud-based quantum computing platform accessed via the ``qnexus`` Python package. Nexus offers users automated job and resource managment, as well as cloud storage and visibility of job resources.

For more information please see:

* `<https://tket.quantinuum.com/api-docs/>`__
* `<https://cqcl.github.io/pytket-quantinuum/api/>`__
* `<https://tket.quantinuum.com/api-docs/getting_started.html>`__
* `<https://docs.quantinuum.com/h-series/trainings/getting_started/pytket_quantinuum/pytket_quantinuum.html>`__

.. tab-set::

   .. tab-item:: Extensions

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
    
   .. tab-item:: Nexus
        
        .. list-table:: Latest script tests
            :widths: 33 33 33
            :header-rows: 1
        
            * - ``python``
              - ``pytket``
              - ``qnexus``
            * - 3.11.11
              - 1.41.0
              - 0.11.0

        .. code-block:: python

            from pytket.circuit import Circuit
            import qnexus as qnx
            import datetime
            import time

            # Choose your machine and login (e.g., H1-1E)
            machine = "H1-1E"

            # Login using username and password.
            qnx.login_with_credentials()

            # Nexus contains all jobs in projects. Setup a new project called "Nexus-Test"
            project = qnx.projects.get_or_create(name="Nexus-Test")
            qnx.context.set_active_project(project)

            # Get simulator and emulator devices
            device_df = qnx.devices.get_all(nexus_hosted=False).df()
            print("Available Quantinuum Devices:",[device for device in device_df['device_name'].tolist()])

            # Get simulator and emulator devices specifically hosted on Nexus
            device_df = qnx.devices.get_all(nexus_hosted=True).df()
            print("Available Nexus Devices:",[device for device in device_df['device_name'].tolist()])

            # All job names must be unique within a Nexus project.
            jobname_suffix = datetime.datetime.now().strftime("%Y_%m_%d-%H-%M-%S")

            # Create a configuration to target the desired machine with a specific group (e.g., STF007)
            config = qnx.QuantinuumConfig(device_name=machine, user_group="STF007")

            # Build the circuit
            circuit = Circuit(2, name="Bell Test")
            circuit.H(0)
            circuit.CX(0, 1)
            circuit.measure_all()


            # It is required that all circuits be uploaded to the nexus database
            # before compilation/execution jobs can be used.

            ref = qnx.circuits.upload(circuit=circuit, name=f"Bell-Test-{jobname_suffix}")

            # Compile job
            ref_compile_job = qnx.start_compile_job(
                    circuits=[ref],
                    backend_config=config,
                    optimisation_level=2,
                    name=f"Bell-compiliation-{jobname_suffix}"
                    )

            #Further operations must be blocked while a job is running.
            print("Compile job status:", qnx.jobs.status(ref_compile_job).status)
            qnx.jobs.wait_for(ref_compile_job,timeout=600.0)
            print("Compile job status:", qnx.jobs.status(ref_compile_job).status)    

            # Get the compiled circuit.
            ref_compiled_circuit = qnx.jobs.results(ref_compile_job)[0].get_output()
            compiled_circuit = ref_compiled_circuit.download_circuit()

            # Execute the job.
            ref_execute_job = qnx.start_execute_job(
                    circuits=[ref_compiled_circuit],
                    n_shots=[100],
                    backend_config=config,
                    name=f"Bell-execute-{jobname_suffix}"
                    )

            # Get job status and halt further operations while job runs.

            print("Execute job status:", qnx.jobs.status(ref_execute_job).status)
            qnx.jobs.wait_for(ref_execute_job,timeout=600.0)[0]
            print("Execute job status:", qnx.jobs.status(ref_execute_job).status)

            # Get results.
            ref_result = qnx.jobs.results(ref_execute_job)[0]
            backend_results = ref_result.download_result()
            print(backend_results.get_distribution())
            print(backend_results.get_counts())

            # Logout
            qnx.client.auth.logout()

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



IQM
===

An IQM+Qiskit plugin provides access to IQM backends.

For more information please see:

* `<https://iqm-finland.github.io/qiskit-on-iqm/user_guide.html>`__

.. note::

   Your IQM API Token is listed on your IQM Resonance dashboard at `<https://resonance.meetiqm.com/>`__.

.. list-table:: Latest script tests
   :widths: 33 33 34
   :header-rows: 1

   * - ``python``
     - ``qiskit``
     - ``qiskit-iqm``
   * - 3.11.11
     - 1.1.2
     - 15.5

.. code-block:: python

    from iqm.qiskit_iqm import IQMProvider, transpile_to_IQM
    from qiskit import QuantumCircuit

    # Backend to connect to (e.g., Garnet's algorithm checker)
    server_url = "https://cocos.resonance.meetiqm.com/garnet:mock"

    # Authentication token (alternatively can set the IQM_TOKEN environment variable)
    api_token = "PUT TOKEN HERE"

    SHOTS = 100

    # Define quantum circuit
    num_qb = 5
    qc = QuantumCircuit(num_qb)

    qc.h(0)
    for qb in range(1, num_qb):
        qc.cx(0, qb)
    qc.barrier()
    qc.measure_all()

    # Initialize backend
    backend = IQMProvider(server_url, token=api_token).get_backend()

    # Transpile circuit
    qc_transpiled = transpile_to_IQM(qc, backend)
    print(qc_transpiled.draw(output="text"))

    # Run circuit
    job = backend.run(qc_transpiled, shots=SHOTS)
    print(job.result().get_counts())


After running the above script, you should see something similar to:

.. code-block::

    {'10101': 25, '11111': 23, '01010': 24, '00000': 28}

.. note::

   The mock system used here is only for testing your algorithm. It will compile your code for the instruments of an IQM quantum computer. However, as no actual instruments are connected to the Mock environment, it will only yield random results – this is not a simulator. See `facade backends <https://iqm-finland.github.io/qiskit-on-iqm/user_guide.html#running-a-quantum-circuit-on-a-facade-backend>`__ for an alternative option.
