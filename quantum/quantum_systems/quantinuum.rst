**********
Quantinuum
**********

Overview
========
Quantinuum offers access to trapped ion quantum computers and emulators, accessible via their API and User Portal. For the complete set of currently available devices, qubit numbers, etc. see the *Quantinuum Systems User Guide* under the *Examples* tab on the `Quantinuum User Portal <https://um.qapi.quantinuum.com/>`__. 

This guide describes how to use the system once you have access. For
instructions on how to gain access, see our :doc:`Quantum Access
</quantum/quantum_access>` page instead.

Features
--------
The complete set of Quantinuum System Model H1’s hardware specifications and operations, can be found in the *Quantinuum System Model H1 Product Data Sheet* on the `Quantinuum User Portal <https://um.qapi.quantinuum.com/>`__. Features include, but are not limited to:

* N ≥ 12 qubit trapped-ion based quantum computer

* All-to-all connectivity

* Laser based quantum gates

* Linear trap Quantum Charge-Coupled Device (QCCD) architecture with three or more parallel gate zones

* Mid-circuit measurement conditioned circuit branching

* Qubit reuse after mid-circuit measurement

* Native gate set: single-qubit rotations, two-qubit ZZ-gates


Connecting
==========

.. _quantinuum-local:

Locally via OpenQASM or pyket 
-----------------------------
Users are able to submit jobs that run remotely on Quantinuum’s systems from a local python development environment. Directions for setting up the python environment and getting started in a notebook locally as well as additional examples utilizing conditional logic and mid-circuit measurement are found under the *Examples* tab on the `Quantinuum User Portal <https://um.qapi.quantinuum.com/>`__. 

Running Jobs & Queue Policies
=============================
Information on submitting jobs to Quantinuum systems, the queue policies, availability, checking job status, tracking usage, analyzing results, and data retention can be found in the *Quantinuum Systems User Guide* under the *Examples* tab on the `Quantinuum User Portal <https://um.qapi.quantinuum.com/>`__. A recommended workflow for running on Quantinuum’s quantum computers is to utilize the syntax checker first, run on the emulator, then run on one of the quantum computers. This is highlighted in the examples.


