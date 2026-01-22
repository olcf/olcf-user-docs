.. _hello-qcup:

******************
Hello QCUP Scripts
******************

Overview
========

This page contains example "Hello World!" scripts for each Quantum Computing User Program (QCUP) vendor.
Although a given vendor may have various access options (see :doc:`/quantum/quantum_systems/index`), this page showcases how to run jobs in a local **scripting environment**.

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
   * - 3.12.12
     - 2.3.0
     - 0.45.0
     - 0.17.2

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

The tket framework is a software platform for the development and execution of gate-level quantum computation, providing state-of-the-art performance in circuit compilation.

Quantinuum Nexus is a cloud-based quantum computing platform accessed via the ``qnexus`` Python package. Nexus offers users automated job and resource managment, as well as cloud storage and visibility of job resources.

Guppy is a quantum programming language that is fully embedded into Python. It allows you to write high-level hybrid quantum programs with classical control flow and mid-circuit measurements using Pythonic syntax.

For more information please see:

* `Getting started with tket <https://docs.quantinuum.com/tket/user-guide/>`__
* `Getting started with qnexus <https://docs.quantinuum.com/nexus/trainings/notebooks/basics/getting_started.html>`__
* `Getting started with Guppy <https://docs.quantinuum.com/guppy/getting_started.html>`__

.. tab-set::

   .. tab-item:: Model H2 (pytket)

        .. list-table:: Latest script tests
            :widths: 33 33 34
            :header-rows: 1

            * - ``python``
              - ``pytket``
              - ``qnexus``
            * - 3.12.12
              - 2.11.0
              - 0.39.0

        .. code-block:: python

            from pytket import Circuit
            import qnexus as qnx
            import uuid

            ##### Nexus Details #####

            # Select the backend here:
            MACHINE = "H2-1E"

            # Login to Nexus
            # qnx.login() # interactive login via browser
            qnx.login_with_credentials() # login via python prompt

            # Setup a dummy suffix for this job
            unique_suffix = uuid.uuid1()

            # Nexus contains all jobs in projects. Setup a new project called "Hello-QCUP"
            project = qnx.projects.get_or_create("Hello-QCUP")
            qnx.context.set_active_project(project)

            # Get simulator and emulator devices
            device_df = qnx.devices.get_all(nexus_hosted=False).df()
            print("Available Quantinuum Devices:",[device for device in device_df['device_name'].tolist()])

            # Get simulator and emulator devices specifically hosted on Nexus
            device_df = qnx.devices.get_all(nexus_hosted=True).df()
            print("Available Nexus Devices: \n", device_df)

            # Make and upload circuit
            my_circuit_ref = qnx.circuits.upload(
                name=f"Hello-QCUP-{unique_suffix}",
                circuit=Circuit(2).H(0).CX(0, 1).measure_all(),
                project=project,
            )

            # Compile on Nexus

            compile_job_ref = qnx.start_compile_job(
                programs=[my_circuit_ref],
                name=f"Hello-QCUP-compile-{unique_suffix}",
                optimisation_level=1,
                backend_config=qnx.QuantinuumConfig(device_name=f"{MACHINE}"),
                project=project,
                skip_intermediate_circuits=False,  # Store compiled circuits
            )

            # Block until the job is complete
            qnx.jobs.wait_for(compile_job_ref)

            compiled_circuits = [item.get_output() for item in qnx.jobs.results(compile_job_ref)]

            # Execute on Nexus

            execute_job_ref = qnx.start_execute_job(
                programs=compiled_circuits,
                name=f"Hello-QCUP-execute-{unique_suffix}",
                n_shots=[100] * len(compiled_circuits),
                backend_config=qnx.QuantinuumConfig(device_name=f"{MACHINE}"),
                project=project,
            )

            # Block until the job is complete
            # Default timeout is 900 seconds
            qnx.jobs.wait_for(execute_job_ref, timeout=900.0)

            # If you ever need to get `execute_job_ref` manually from Nexus (i.e., if your script timed out before the job completed)
            # You can retrieve the job reference like so:
            # execute_job_ref = qnx.client.jobs.get(id='PASTE JOB ID FROM NEXUS HERE')

            # Retrieve a ExecutionResultRef for every Circuit that was run
            execute_job_result_refs = qnx.jobs.results(execute_job_ref, allow_incomplete=True)

            # Get the results of the execution
            result = execute_job_result_refs[0].download_result()
            result.get_counts()

        After running the above script, you should see something similar to:

        .. code-block::

            Counter({(0, 0): 57, (1, 1): 43})
    
   .. tab-item:: Helios (Guppy)
        
        .. list-table:: Latest script tests
            :widths: 25 25 25 25
            :header-rows: 1
        
            * - ``python``
              - ``pytket``
              - ``qnexus``
              - ``guppylang``
            * - 3.12.12
              - 2.11.0
              - 0.39.0
              - 0.21.6

        .. code-block:: python

            from guppylang import guppy
            from guppylang.std.builtins import owned, result
            from guppylang.std.quantum import cx, h, measure, qubit, x, z

            import qnexus as qnx
            import uuid
            import numpy as np

            ##### Nexus Details #####

            # Select the backend here:
            # Options: "Helios-1", "Helios-1E", "Helios-1E-lite", "Selene", "SelenePlus"
            MACHINE = "Helios-1E"

            # Login to Nexus
            # qnx.login() # interactive login via browser
            qnx.login_with_credentials() # login via python prompt

            # Setup a dummy suffix for this job
            unique_suffix = uuid.uuid1()

            # Nexus contains all jobs in projects. Setup a new project called "Hello-QCUP"
            project = qnx.projects.get_or_create("Hello-QCUP")
            qnx.context.set_active_project(project)

            # Get simulator and emulator devices
            device_df = qnx.devices.get_all(nexus_hosted=False).df()
            print("Available Quantinuum Devices:",[device for device in device_df['device_name'].tolist()])

            # Get simulator and emulator devices specifically hosted on Nexus
            device_df = qnx.devices.get_all(nexus_hosted=True).df()
            print("Available Nexus Devices: \n", device_df)

            ##### Circuit Definition #####
            @guppy
            def teleport(src: qubit @owned, tgt: qubit) -> None:
                """Teleports the state in `src` to `tgt`."""
                # Create ancilla and entangle it with src and tgt
                tmp = qubit()
                h(tmp)
                cx(tmp, tgt)
                cx(src, tmp)

                # Apply classical corrections
                h(src)
                if measure(src):
                    z(tgt)
                if measure(tmp):
                    x(tgt)

            ##### Define Function to Call Circuit #####
            @guppy
            def teleport_one_state() -> None:
                src = qubit()
                tgt = qubit()

                # Let's teleport the |1> state
                x(src)
                teleport(src, tgt)

                result("teleported", measure(tgt))

            ##### Running Locally on Emulator #####
            sim_result = teleport_one_state.emulator(n_qubits=3).stabilizer_sim().with_seed(2).run()
            print('Local Results: \n', list(sim_result.results))

            ##### Compile and Upload to Nexus #####

            # HUGR programs only for Helios devices
            hugr_binary = teleport_one_state.compile()


            ref_hugr = qnx.hugr.upload(
                hugr_binary, 
                name=f"repeat-until-success-{unique_suffix}"
            )

            # checks against syntax checker Helios-1SC
            prediction = qnx.hugr.cost(
                programs=[ref_hugr], 
                n_shots=[10]
            )

            ##### System Configurations #####
            match MACHINE:
                case "Helios-1":
                    # Quantinuum Device (measured via HQCs)
                    config = qnx.QuantinuumConfig(
                        device_name="Helios-1",
                        max_cost=np.ceil(prediction),
                        compiler_options={'max-qubits': 3}
                    )

                case "Helios-1E":
                    # Quantinuum Device (measured via HQCs)
                    config = qnx.QuantinuumConfig(
                        device_name="Helios-1E",
                        max_cost=np.ceil(prediction),
                        compiler_options={'max-qubits': 3}
                    )

                case "Helios-1E-lite":
                    # Nexus Device (measured via execution time)
                    config = qnx.models.HeliosConfig(
                        system_name="Helios-1E-lite",
                        emulator_config=qnx.models.HeliosEmulatorConfig(n_qubits=3)
                    )

                case "Selene":
                    # Nexus Device (measured via execution time)
                    # Selene Simulators Options: StatevectorSimulator, StabilizerSimulator, CoinflipSimulator, ClassicalReplaySimulator
                    # Selene Runtime Options: SimpleRuntime
                    # Selene Error Model Options: NoErrorModel, DepolarizingErrorModel
                    # SEED IS OPTIONAL
                    config = qnx.SeleneConfig(
                        n_qubits=3,
                        runtime={"type": "SimpleRuntime", "seed": "42"},
                        error_model={"type": "NoErrorModel", "seed": "42"},
                        simulator={"type": "StabilizerSimulator", "seed": "42"}
                    )

                case "SelenePlus":
                    # Nexus Device (measured via execution time)
                    # SelenePlus Simulators Options: StatevectorSimulator, StabilizerSimulator, MatrixProductStateSimulator, CoinflipSimulator, ClassicalReplaySimulator
                    # SelenePlus Runtime Options: SimpleRuntime, HeliosRuntime
                    # SelenePlus Error Model Options: NoErrorModel, DepolarizingErrorModel, QSystemErrorModel, HeliosCustomErrorModel
                    # SEED IS OPTIONAL
                    config = qnx.SelenePlusConfig(
                        n_qubits=3,
                        runtime={"type": "HeliosRuntime", "seed": "42"},
                        error_model={"type": "HeliosCustomErrorModel", "seed": "42"},
                        simulator={"type": "StatevectorSimulator", "seed": "42"}
                    )

                case _:
                    raise ValueError(f"Unsupported MACHINE selection: {MACHINE}")

            ##### Running the Job Remotely #####

            result_ref = qnx.start_execute_job(
                programs=[ref_hugr],
                n_shots=[10],
                backend_config=config,
                name=f"Hello-QCUP-{unique_suffix}"
            )

            qnx.jobs.wait_for(result_ref)
            print(result_ref)
            job_result = qnx.jobs.results(result_ref)[0].download_result()
            print('Remote Results: \n', job_result)

        After running the above script, you should see something similar to:

        .. code-block::

            QsysResult(results=[QsysShot(entries=[['teleported', 1]])

IonQ
====

IonQ has many pathways to accessing their quantum backends.
Although the script below uses the `Qiskit IonQ Provider <https://docs.ionq.com/sdks/qiskit>`__ , details on how to use Cirq, PennyLane, XACC, and more can be found in the `IonQ Documentation <https://docs.ionq.com>`__ .

For more information please see:

* `<https://docs.ionq.com/>`__
* `<https://ionq.com/resources>`__
* `<https://docs.ionq.com/guides/managing-api-keys>`__
* `<https://docs.ionq.com/sdks/qiskit>`__

.. list-table:: Latest script tests
   :widths: 33 33 34
   :header-rows: 1

   * - ``python``
     - ``qiskit``
     - ``qiskit-ionq``
   * - 3.12.12
     - 2.3.0
     - 1.0.2

.. code-block:: python

    from qiskit import QuantumCircuit
    from qiskit_ionq import IonQProvider
    import os

    # Set your credentials (can also set this externally)
    os.environ["IONQ_API_KEY"] = "API KEY GOES HERE"

    # Load your IonQ credentials and list backends
    provider = IonQProvider()
    print(provider.backends())

    # Run on "simulator", "qpu.aria-1", "qpu.forte-1", "qpu.forte-enterprise-1"
    backend = provider.get_backend("simulator")
    #backend.set_options(noise_model="forte-1") # Optional: set a noise model for a simulator

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

* `<https://docs.meetiqm.com/iqm-client/user_guide_qiskit.html>`__

.. note::

   Your IQM API Token is listed on your IQM Resonance dashboard at `<https://resonance.meetiqm.com/>`__.

.. list-table:: Latest script tests
   :widths: 33 33 34
   :header-rows: 1

   * - ``python``
     - ``qiskit``
     - ``iqm-client``
   * - 3.12.12
     - 2.1.2
     - 33.0.3

.. code-block:: python

    from iqm.qiskit_iqm import IQMProvider, transpile_to_IQM
    from qiskit import QuantumCircuit


    # Authentication token (alternatively can set the IQM_TOKEN environment variable)
    api_token = "PUT TOKEN HERE"

    # Backend to connect to (e.g., Emerald's algorithm checker)
    provider = IQMProvider("https://resonance.meetiqm.com/", quantum_computer="emerald:mock", token=api_token)

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
    backend = provider.get_backend()

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
