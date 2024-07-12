**********
Quantinuum
**********

.. warning::
    New allocation policy in effect Oct. 1st 2022, see :ref:`quantinuum-alloc` section.

Overview
========

Quantinuum offers access to trapped ion quantum computers and emulators,
accessible via their API and User Portal. For the complete set of currently
available devices, qubit numbers, etc. see the *Quantinuum Systems User Guide* under the *Examples* tab on the `Quantinuum User Portal <https://um.qapi.quantinuum.com/>`__. 

This guide describes how to use the system once you have access. For
instructions on how to gain access, see our :doc:`Quantum Access
</quantum/quantum_access>` page instead.

Features
--------

The complete set of Quantinuum System Model H1 and Model H2 hardware specifications and
operations, can be found in the *Quantinuum System Model H1 Product Data Sheet* and the 
*Quantinuum System Model H2 Product Data Sheet* on the `Quantinuum User Portal <https://um.qapi.quantinuum.com/>`__. Features include, but are not limited to:

* All-to-all connectivity

* Laser based quantum gates

* Linear trap Quantum Charge-Coupled Device (QCCD) architecture with three or more parallel gate zones

* Mid-circuit measurement conditioned circuit branching

* Qubit reuse after mid-circuit measurement

* Native gate set: single-qubit rotations, two-qubit ZZ-gates


Connecting
==========

.. _quantinuum-cloud:

Cloud Access
------------

Users can access information about Quantinuum's systems, view submitted jobs,
look up machine availability, and update job notification preferences on the
cloud dashboard on the `Quantinuum User Portal <https://um.qapi.quantinuum.com/>`__. 

* Jupyter at OLCF: Access to the Quantinuum queues can also be obtained via `OLCF JupyterHub
  <https://jupyter-open.olcf.ornl.gov/>`__, a web-based interactive computing
  environment.

.. _quantinuum-local:

Locally via OpenQASM or pyket 
-----------------------------

Users are able to submit jobs that run remotely on Quantinuum's systems from a
local python development environment. Directions for setting up the python
environment and getting started in a notebook locally as well as additional
examples utilizing conditional logic and mid-circuit measurement are found
under the *Examples* tab on the `Quantinuum User Portal <https://um.qapi.quantinuum.com/>`__. 

.. _quantinuum-jobs:

Running Jobs & Queue Policies
=============================

Information on submitting jobs to Quantinuum systems, system availability,
checking job status, and tracking usage can be found in the *Quantinuum Systems User Guide* under the *Examples* tab on the `Quantinuum User Portal <https://um.qapi.quantinuum.com/>`__.

Users have access to the API validator to check program syntax, and to the
Quantinuum System Model H1 emulator, which returns actual results back as if
users submitted code to the real quantum hardware.

.. note::
    A recommended workflow for running on Quantinuum's quantum computers is to
    utilize the syntax checker first, run on the emulator, then run on one of the
    quantum computers. This is highlighted in the examples.

.. _quantinuum-alloc:

Allocations & Credit Usage
==========================

Running a job on the System Model H1 family and System Model H2 hardware requires Quantinuum
Credits. Additional information on credit usage can be found in the *Quantinuum Systems User Guide* under the
*Examples* tab on the `Quantinuum User Portal <https://um.qapi.quantinuum.com/>`__.
Due to increased demand and to make the most efficient use of credits, the following allocating policy will go into effect starting October 1st 2022:

* Any request for credits must be submitted by the project Principle Investigator (PI) to help@olcf.ornl.gov

* Requests for machine credits must be justified using results from the emulator to determine the appropriate amount needed. Requests without emulator-based justifications will be denied.

* Requests will be evaluated based on the provided technical justification, programmatic efficiency, and machine availability. The effective usage of prior allocations by the project will also be considered.

* Allocations will be granted on a monthly basis to maximize the availability of the H1 family and H2 machines. Please note that allocations do not carry over to the next month and must be consumed in the month granted.
 
* Allocation requests requiring 20 qubits and fewer will be considered for H1 family machines, and allocation requests requiring 21 or more qubits will be considered for H2.

Allocation requests for the following month must be submitted no later than the 25th of the preceding month.  The uptime schedule is available on the *Calendar* tab of the `Quantinuum User Portal <https://um.qapi.quantinuum.com/>`__. 

Due to hardware emulation complexity, jobs using greater than 29 qubits for statevector emulation are likely to experience significantly slowed execution times. 

Software
========

The TKET framework is a software platform for the development and execution of
gate-level quantum computation, providing state-of-the-art performance in
circuit compilation. It was created and is maintained by Quantinuum. The
toolset is designed to extract the most out of the available NISQ devices of
today and is platform-agnostic.

In python, the ``pytket`` package is available for python 3.8+. The ``pytket``
and ``pytket-quantinuum`` packages are included as part of the installation
instructions on `Quantinuum's User Portal <https://um.qapi.quantinuum.com/>`__.

For more information on TKET, see the following links:

* TKET documentation is available at `<https://cqcl.github.io/pytket/manual/manual_intro.html>`__

* An introduction to quantum compilation with TKET is available at `<https://github.com/CalMacCQ/tket_blog/blob/main/blog1_intro_to_qc.ipynb>`__

* For a video introduction to TKET, see `<https://www.youtube.com/watch?v=yXKSpvgAtrk>`__




