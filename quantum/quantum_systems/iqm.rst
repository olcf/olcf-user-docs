.. _iqm-guide:

***
IQM
***

Overview
========

IQM provides access to quantum computing resources through their cloud platform, 
IQM Resonance. Users can execute quantum algorithms on IQM's quantum computers, 
such as the 20 qubit Garnet and the 6 qubit Deneb systems, using multiple supported
software frameworks. IQM's quantum processors are made up of superconducting
transmon qubits, utilizing multiple topologies. 

This guide describes how to use the systems once you have access. For
instructions on how to gain access, see our :doc:`Quantum Access
</quantum/quantum_access>` page instead.

.. _iqm-connecting:

Connecting
==========

Users can access information about IQM's systems, view upcoming queue
availability, view job history, and access training resources on their Resonance dashboard at
`<https://resonance.meetiqm.com/>`__. 


.. _iqm-jobs:

Running Jobs & Queue Policies
=============================

Users can submit jobs to IQM backends both ia a timeslot (reservation) system as well as via a pay-as-you-go queue system. 

In timeslot mode, your project is assigned specific quantum computer access periods that must be
booked in advance. During these slots, access is exclusive to your project. The Resonance
dashboard's "Upcoming Timeslots" section lists the schedule. Jobs can be submitted anytime but
remain in a "waiting" state until the next active timeslot. An upcoming booked timeslot is
required to submit jobs in this mode. For instructions on booking a timeslot see `here <https://www.iqmacademy.com/tutorials/resonance/>`__.

In pay-as-you-go mode, allocation used is based on the QPU-reserved seconds your job uses. Jobs
enter a global queue and run during designated pay-as-you-go windows, which may shift due to
dedicated timeslot bookings. You can check your job's queue position, estimated runtime, and cost
in the "Jobs" section of the Resonance dashboard. In light of this, for specific execution times, 
time-critical applications, or iterative algorithms, IQM recommends users consider using timeslots. 


Allocations & Usage Limits
--------------------------
Running a job on the IQM hardware requires IQM credits. So as to make the most efficient use of
credits, the following allocation policy is in effect:

* Any request for credits must be submitted by the project Principle Investigator (PI) to help@olcf.ornl.gov

* Requests for machine credits must be justified using results from the emulator to determine the appropriate amount needed. Requests without emulator-based justifications will be denied.

* Requests will be evaluated based on the provided technical justification, programmatic efficiency, and machine availability. The effective usage of prior allocations by the project will also be considered.

IQM API
--------

To prepare jobs for submission, see the guide `How to run my first algorithm <https://resonance.meetiqm.com/docs>`__
and the video tutorial for this on `<https://www.iqmacademy.com/tutorials/resonance/>`__ 
to walk through this process in detail.

Jupyter at OLCF: Access to IQM systems can also be obtained via `OLCF JupyterHub
<https://jupyter-open.olcf.ornl.gov/>`__, a web-based interactive computing
environment.

.. _iqm-api-keys:

API Keys
--------

Submitting jobs to IQM's hardware backends requires an IQM API key, which can be
generated from on their Resonance dashboard at `<https://resonance.meetiqm.com/>`__.
IQM API keys can only be viewed when they are generated, and IQM recommends storing
each API key locally in an environment variable. Instructions for generating and
storing IQM API keys can be found `here <https://resonance.meetiqm.com/docs>`__.

Submitting Jobs
---------------

Once you have obtained an allocation, you can can request a timeslot with credits via help@olcf.ornl.gov or 
use the pay-as-you-go option. Usage pricing, circuit limits, and shot limits for each of the available 
computers is listed on the resonance dashboard when you click on either of the backends.

With your IQM API key, users submit job to a given backend's URL: e.g. for garnet: 
General URL: https://cocos.resonance.meetiqm.com/garnet
Timeslot URL: https://cocos.resonance.meetiqm.com/garnet:timeslot
Mock URL (emulator/syntax checker): https://cocos.resonance.meetiqm.com/garnet:mock


Checking System Availability
============================

Current status listing and scheduled maintenance for IQM's quantum resources can be found under the 
availability tab `here <https://resonance.meetiqm.com/docs>`__.

.. _iqm-soft:

Software
========

* `IQM's Qiskit-on-IQM  Documentation <https://iqm-finland.github.io/qiskit-on-iqm/user_guide.html#/>`__


Additional Resources
====================

* For a complete list of IQM's available tutorials on the foundations of quantum computing, applications, and algorithms,
see `here <https://www.iqmacademy.com/tutorials/>`__


