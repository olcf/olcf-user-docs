.. _ibm-quantum-guide:

***********
IBM Quantum
***********

Overview
========

IBM Quantum Services provides access to more than 20 currently available
quantum systems (known as backends).  IBM's quantum processors are made up of
superconducting transmon qubits, and users can utilize these systems via the
universal, gate-based, circuit model of quantum computation.  Additionally,
users have access to 5 different types of simulators, simulating from 32 up to
5000 qubits to represent different aspects of the quantum backends. 

This guide describes how to use the system once you have access. For
instructions on how to gain access, see our :doc:`Quantum Access
</quantum/quantum_access>` page instead.

.. _ibm-connecting:

Connecting
==========

Access to the IBM Quantum Computing queues, reservations, and simulators can be
obtained via multiple methods -- either through the :ref:`cloud <ibm-cloud>` or 
:ref:`locally <ibm-local>`.

.. _ibm-cloud:

Cloud Access
------------

Users can access information about IBM Quantum's systems, view queue
information, and submit jobs on their cloud dashboard at
`<https://quantum-computing.ibm.com>`__. The cloud dashboard allows access to
IBM Quantum's graphical circuit builder, Quantum Composer, IBM's Quantum Lab,
and associated program examples.  A Jupyterlab server is provisioned with IBM
Quantum's Qiskit programming framework for job submission.

.. _ibm-local:

Locally via Qiskit
------------------

IBM Quantum provides Qiskit (Quantum Information Software Kit for Quantum
Computation) for working with OpenQASM and the IBM Q quantum processors.
Qiskit allows users to build quantum circuits, compile them for a particular
backend, and run the compiled circuits as jobs. Additional information on using
Qiskit is available at `<https://qiskit.org/learn/>`__ and in our 
:ref:`Software Section <ibm-soft>` below.

As opposed to using IBM's JupyterLab server (described in :ref:`Cloud Access <ibm-cloud>` above), 
users are able to install IBM Quantum Qiskit locally via two methods: 

* Installing manually: `<https://qiskit.org/documentation/stable/0.24/install.html>`__.
  This option allows for building locally and executing jobs via a python virtual
  environment.

* Docker: `<https://www.ibm.com/cloud/learn/docker>`__ or `<https://hub.docker.com/u/ibmq>`__ 

.. _ibm-jobs:

Running Jobs & Queue Policies
=============================

User can submit jobs to IBM Quantum backends both via a fair-sharing queue
system as well as via priority reservation system.  As discussed below, the
dynamic fair-sharing queue system determines the queuing order of jobs so as to
fairly balance system time between access providers, of which the OLCF QCUP is
only one.  Because of this, the order of when a user's job in the fair-share
queue will run varies dynamically, and can't be predicted. In light of this,
for time-critical applications or iterative algorithms, IBM Quantum recommends
users consider making a priority reservation. 

Fair-Share Queue Policy
-----------------------

When jobs are submitted on IBM Quantum backends, the jobs enter into the 
"fair-share" queuing system, in which jobs run in a dynamically calculated
order so as to provide fair sharing among all users of the device, to prevent
individual projects or users from monopolizing a given backend.  

All OLCF users have access to the "premium" (>=20 qubits) and "open" (<20
qubit) devices.  Since most of the open devices are shared with the public,
queue times will often be longer than the queues for the larger devices.

Submitting Jobs
---------------

Jobs are compiled and submitted via Qiskit in a Python virtual environment or
Jupyter notebook (see :ref:`Cloud Access <ibm-cloud>` and 
:ref:`Local Access <ibm-local>` sections above). 

* Circuit jobs comprise jobs of constructed quantum circuits and algorithms
  submitted to backends in IBM Quantum fair-share queue.

* Program jobs utilize a pre-compiled quantum program utilizing the Qiskit
  Runtime framework.

Allocations & Usage Limits
--------------------------

Because of the queuing method described above, users have no set allocation.
Job throughput is only limited via the dynamic queue.

There is a time limit on program-wide usage of reservable systems (see below).  

Reservations & Sessions
-----------------------

.. warning::
   IBM Quantum will be retiring reservations on Apr. 1st. Reservations will be replaced by sessions.

In addition to the fair-share queue, users may request a backend reservation
for a certain period of time by contacting help@olcf.ornl.gov. If the
reservation is granted, the reserved backend will be blocked from general use
for a specified period of time, and the user will have sole use of the
backend for that period.

There is a limited number of minutes per month that can be reserved on each
device. Reservations are supported on these devices with these monthly
allocations:

  * ibmq_kolkata, 2400 minutes per month

In order to make the most efficient use of reservation allocations:

* Reservations requests must be submitted to the project Principle Investigator
  (PI) to help@olcf.ornl.gov

* Requests for reservations must include technical justification.  

* Once submitted, requests will be sent to the Quantum Resource Utilization 
  Council (QRUC) for consideration.

A session in Qiskit Runtime is a tool designed for running multiple jobs in sequence more effectively.
It streamlines the process by grouping jobs together, reducing the wait times often associated with individually queued jobs. 
For more information on sessions can be found here:
`<https://docs.quantum.ibm.com/run/sessions>`__

.. warning::
     Please note, starting a session by using the /jobs endpoint will no longer be supported after March 31, 2024.
     After this date, qiskit-ibm-runtime version 0.20.0 or later, or qiskit-ibm-provider version 0.10.0 or later must be used to start a session. 
     If you are calling the API directly, use the /sessions endpoint instead. Refer to this documentation for information about using the Qiskit IBM Runtime API:
     `<https://docs.quantum.ibm.com/api/runtime>`__ 

Checking System Availability & Capability
=========================================

Current status listing, scheduled maintenance, and system capabilities for IBM
Quantum's quantum resources can be found here:
`<https://quantum-computing.ibm.com/services?services=systems>`__

.. _ibm-soft:

Software
========

* Qiskit documentation is available at `<https://qiskit.org/documentation/>`__

* Qiskit Terra is the foundational module set upon which the rest of Qiskit's
  features are built; for more information, see:
  `<https://qiskit.org/documentation/apidoc/terra.html>`__

* Qiskit Aer is IBM Quantum's package for simulating quantum circuits, with
  different backends for specific types of simulation

  * Simulator backends currently available: `<https://quantum-computing.ibm.com/services?services=simulators>`__

Additional Resources
====================

* `IBM's Documentation <https://quantum-computing.ibm.com/docs/>`__

* `IBM Quantum Insider <https://thequantuminsider.com/2022/11/09/ibm-quantum-computing/>`__
