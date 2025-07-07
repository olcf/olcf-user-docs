.. _iqm-guide:

***
IQM
***

Overview
========

IQM provides access to quantum computing resources through their cloud platform, 
IQM Resonance. Users can execute quantum algorithms on IQM's quantum computers, 
such as the 54 qubit Emerald and the 20 qubit Garnet systems, using multiple supported
software frameworks. IQM's quantum processors are made up of superconducting
transmon qubits, utilizing multiple topologies. 

This guide describes how to use the systems once you have access. For
instructions on how to gain access, see our :doc:`Quantum Access
</quantum/quantum_access>` page instead.

Available Systems
=================

For a list of currently available systems, along with demos for each system, please see `IQM's QPU page <https://www.iqmacademy.com/qpu/>`__.

.. _iqm-connecting:

Connecting
==========

Users can access information about IQM's systems, view upcoming queue
availability, view job history, and access training resources on their Resonance dashboard at
`<https://resonance.meetiqm.com/>`__. 


.. _iqm-jobs:

Running Jobs & Queue Policies
=============================

Users can submit jobs to IQM backends both via a timeslot (reservation) system as well as a pay-as-you-go queue system. 

In timeslot mode, your project is assigned specific quantum computer access periods that must be
booked in advance. During these slots, access is exclusive to your project. The Resonance
dashboard's "Availability" section lists the schedule. Jobs can be submitted anytime but
remain in a "waiting" state until the next active timeslot. An upcoming booked timeslot is
required to submit jobs in this mode.

In pay-as-you-go mode, allocation used is based on the QPU-reserved seconds your job uses. Jobs
enter a global queue and run during designated pay-as-you-go windows, which may shift due to
dedicated timeslot bookings. You can check your job's queue position, estimated runtime, and final cost
in the "Jobs" section of the Resonance dashboard. In light of this, for specific execution times, 
time-critical applications, or iterative algorithms, IQM recommends users consider using timeslots. 

Project/Team Roles
------------------

The IQM equivalent to an OLCF project is an IQM "Team". The PI of a given
project is assigned the ``Scheduler`` role, while all other members are given the
``User`` role.

* **By default, only OLCF project PI's have the ability to book timeslots for
  their IQM Team via the Scheduler role.** If other members of the Team
  require the ``Scheduler`` role, please contact help@olcf.ornl.gov.

* Team members with the ``User`` role cannot view or manage credit balances
  and cannot book timeslots, but can run jobs as long as there are credits
  available for their Team or if a timeslot was booked by their PI.

See :ref:`iqm-alloc` for details on how to receive credits for your Team.

For more details on the capabilities of roles on a Team, please refer to the
"User Roles" subsection in the "Organization Management" section at
https://resonance.meetiqm.com/docs


.. _iqm-alloc:

Allocations & Usage Limits
--------------------------
Running a job on the IQM hardware requires IQM credits. So as to make the most efficient use of
credits, the following allocation policy is in effect:

* Any request for credits must be submitted by the project Principle Investigator (PI) by logging into `myOLCF <https://my.olcf.ornl.gov>`__, select your QCUP project under "My Projects" after login, and use the `Quantum Allocation Request form <https://my.olcf.ornl.gov/allocations/quantumAllocation>`__ under the "Allocations" section. Alternatively, you can send a request through our help ticket system (help@olcf.ornl.gov).

* Requests for machine credits must be justified using an emulator/mock backend and `IQM's Resource Calculator <https://www.iqmacademy.com/qpu/resourceCalculator/>`__. For justifying the pay-as-you-go method, we recommend using the Resource Calculator in combination with the credits per second pricing information listed in the "Quantum Computers" section on the resonance dashboard for a given backend.

* Requests will be evaluated based on the provided technical justification, programmatic efficiency, and machine availability. The effective usage of prior allocations by the project will also be considered.

IQM API
--------

To prepare jobs for submission, see the guide `How to run my first algorithm <https://resonance.meetiqm.com/docs>`__
and the video tutorial for this on `<https://www.iqmacademy.com/tutorials/resonance/>`__ 
to walk through this process in detail.

Jupyter at OLCF: If you do not want to install Jupyter yourself, users can leverage `OLCF's JupyterHub
<https://jupyter-open.olcf.ornl.gov/>`__ service to help create a python environment to access IQM systems.

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

Once you have been granted credits (process detailed in :ref:`iqm-alloc`), you
can use a timeslot (if booked by your PI) or use the pay-as-you-go option.
Usage pricing, circuit limits, and shot limits for each of the available
computers is listed on the resonance dashboard when you click on either of the
backends in the "Quantum Computers" section.

With your IQM API key, users submit job to a given backend's URL: e.g. for garnet: 

* General URL: ``https://cocos.resonance.meetiqm.com/garnet`` (can only be used for pay-as-you-go)
* Timeslot URL: ``https://cocos.resonance.meetiqm.com/garnet:timeslot`` (can only be used for timeslots)
* Mock URL: ``https://cocos.resonance.meetiqm.com/garnet:mock`` (syntax checker -- if available)

.. note::
   
   The mock system is only for testing your algorithm. It will compile your code for the instruments of an IQM quantum computer. However, as no actual instruments are connected to the Mock environment, it will only yield random results – this is not a simulator. See `fake and facade backends <https://docs.meetiqm.com/iqm-client/user_guide_qiskit.html#simulation>`__ for an alternative option.


Checking System Availability
============================

Current status listing and scheduled maintenance for IQM's quantum resources can be found under the 
availability tab `here <https://resonance.meetiqm.com/>`__.

.. _iqm-soft:

Software
========

* `IQM Client Documentation <https://docs.meetiqm.com/iqm-client/index.html>`__
* `IQM's Qiskit-on-IQM  Documentation <https://docs.meetiqm.com/iqm-client/user_guide_qiskit.html>`__


Additional Resources
====================

* For a complete list of IQM's available tutorials on the foundations of quantum computing, applications, and algorithms, see `here <https://www.iqmacademy.com/tutorials/>`__
* `IQM's Resource Calculator <https://www.iqmacademy.com/qpu/resourceCalculator/>`__


