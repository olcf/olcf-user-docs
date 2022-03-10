###########
IBM Quantum
###########

Introduction to IBM Quantum Computing
=========================================

IBM Quantum Services provides access to more than 20 currently available quantum systems (known as backends).  IBM's quantum processors are made up of superconducting transmon qubits, and users can utilize these systems via the universal, gate-based, circuit model of quantum computation.  Additionally, users have access to 5 different types of simulators, simulating from 32 up to 5000 qubits to represent different aspects of the quantum backends.

Connecting
=========================================

Access to the IBM Quantum Computing queues, reservations, and simulators can be obtained via multiple methods.

* Cloud access: users can access information about IBM Quantum's systems, view queue information, and submit jobs on their cloud dashboard, found here: https://quantum-computing.ibm.com. The cloud dashboard allows access to IBM Quantum's graphical circuit builder, Quantum Composer, and IBM's Quantum Lab, a Jupyterlab server is provisioned with IBM Quantum's Qiskit programming framework (see Software, below), and associated program examples and tutorials. 

* Users are able to install IBM Quantum Qiskit locally via two methods: 

  * Installing locally: https://qiskit.org/documentation/stable/0.24/install.html. This option allows for building locally and executing jobs via a python virtual environment.  

  * Docker: https://www.ibm.com/cloud/learn/docker or https://hub.docker.com/u/ibmq 

Running Jobs & Queue Policies
=========================================

User can submit jobs to IBM Quantum backends both via a fair-sharing queue system as well as via priority reservation system.  As discussed below, the dynamic fair-sharing queue system determines the queuing order of jobs so as to fairly balance system time between access providers, of which the OLCF QCUP is only one.  Because of this, the order of when a user's job in the fair-share queue will run varies dynamically, and can't be predicted. In light of this, for time-critical applications or iterative algorithms, IBM Quantum recommends users consider making a priority reservation. 

Fair-Share Queue Policy
------------------------------

* When jobs are submitted on IBM Quantum backends, the jobs enter into the "fair-share" queuing system, in which jobs run in a dynamically calculated order so as to provide fair sharing among all users of the device, to prevent individual projects or users from monopolizing a given backend.  

* All OLCF users have access to the "premium" (>=20 qubits) and "open" (<20 qubit) devices.  Since most of the opne devices are shared with the public, queue times will often be longer than the queues for the larger devices.

Allocations & Usage Limits
------------------------------

* Because of this queuing method, users have no set allocation.  Job throughput is only limited via the dynamic queue.
* There is a time limit on program-wide usage of reservable systems (see below).  

Reservations
------------------------------

* In addition to the fair-share queue, users may request a backend reservation for a certain period of time by contacting help@olcf.ornl.gov. If the reservation is granted, the reserved backend will be blocked from general use for a specified period of time, and the user will have sole use of the backend for that period.

* There is a limited number of minutes per month that can be reserved on each device. Reservations are supported on these devices with these monthly allocations:

  * ibmq_toronto, 1800 minutes per month 

  * ibmq_jakarta, 720 minutes per month

  * ibmq_lagos, 720 minutes per month

  * ibmq_perth, 720 minutes per month

Submitting Jobs
------------------------------

Jobs are compiled and submitted via Qiskit (see below) in a Python virtual environment or Jupyter notebook. 

* Circuit jobs comprise jobs of constructed quantum circuits and algorithms submitted to backends in IBM Quantum fair-share queue.

* Program jobs utilize a pre-compiled quantum program utilizing the Qiskit Runtime framework. 

Software
=========================================

IBM Quantum provides Qiskit (Quantum Information Software Kit for Quantum Computation) for working with OpenQASM and the IBM Q quantum processors.  Qiskit allows users to build quantum circuits, compile them for a particular backend, and run the compiled circuits as jobs. Additional information on using Qiskit is available at https://qiskit.org/learn/.

* Qiskit Terra is the foundational module set upon which the rest of Qiskit's features are built; for more information, see: https://qiskit.org/documentation/apidoc/terra.html

* Qiskit Aer is IBM Quantum's package for simulating quantum circuits, with different backends for specific types of simulation

  * Simulator backends currently available: https://quantum-computing.ibm.com/services?services=simulators


Checking System Availability & Capability
=========================================

Current status listing, scheduled maintenance, and system capabilities for IBM Quantum's quantum resources can be found here: https://quantum-computing.ibm.com/services?services=systems

