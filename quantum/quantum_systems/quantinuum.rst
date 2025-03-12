**********
Quantinuum
**********

.. note::
   Quantinuum has launched a new cloud-based platform called `Quantinuum Nexus <https://docs.quantinuum.com/nexus/user_guide/concepts/concepts.html>`__.
   Instructions for accessing Nexus will be sent to QCUP users in January 2025.
   QCUP users should transition to Nexus for a newer user dashboard experience.
   See the :ref:`quantinuum-nexus` section for more details.

Overview
========

Quantinuum offers access to trapped ion quantum computers and emulators, accessible via their API and User Portal.
For the complete set of currently available devices, qubit numbers, etc. see the *Quantinuum Systems User Guide* under the *Examples* tab on the legacy `Quantinuum User Portal <https://um.qapi.quantinuum.com/>`__ or the *Backends* tab on `Nexus <https://nexus.quantinuum.com/backends>`__. 

This guide describes how to use the system once you have access.
For instructions on how to gain access, see our :doc:`Quantum Access </quantum/quantum_access>` page instead.

Quantinuum's documentation for both Nexus and the H-Series devices can be found here: https://docs.quantinuum.com/

Features
--------

The complete set of Quantinuum System Model H1 and Model H2 hardware specifications and operations, can be found in their `H-Series User Guide <https://docs.quantinuum.com/h-series/user_guide/hardware_user_guide/access.html>`__.

Features include, but are not limited to:

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

Users can access information about Quantinuum's systems, view submitted jobs, look up machine availability, and update job notification preferences on the cloud dashboard on the legacy `Quantinuum User Portal <https://um.qapi.quantinuum.com/>`__ or `Quantinuum Nexus <https://nexus.quantinuum.com/>`__. 


.. _quantinuum-nexus:

Quantinuum Nexus
^^^^^^^^^^^^^^^^

Quantinuum has launched a new cloud-based platform called `Quantinuum Nexus <https://www.quantinuum.com/blog/introducing-quantinuum-nexus-our-all-in-one-quantum-computing-platform>`__.

* `Quantinuum Nexus User Guide <https://docs.quantinuum.com/nexus/user_guide/concepts/concepts.html>`__
* `Video tutorial <https://vimeo.com/1037971233/d7856494fa>`__ on transitioning to Nexus

OLCF JupyterHub
^^^^^^^^^^^^^^^

If you do not want to install Jupyter yourself, users can leverage `OLCF's JupyterHub <https://jupyter-open.olcf.ornl.gov/>`__ service to help create a python environment to access Quantinuum systems.

.. _quantinuum-local:

Locally via pytket 
------------------

Users are able to submit jobs that run remotely on Quantinuum's systems from a local python development environment.
Directions for setting up the python environment and getting started in a notebook locally as well as additional examples utilizing conditional logic and mid-circuit measurement are found under the *Examples* tab on the legacy `Quantinuum User Portal <https://um.qapi.quantinuum.com/>`__ or Quantinuum's H-Series `Getting Started page <https://docs.quantinuum.com/h-series/trainings/getting_started/getting_started_index.html>`__.

.. _quantinuum-jobs:

Running Jobs & Queue Policies
=============================

Information on submitting jobs to Quantinuum systems, system availability, checking job status, and tracking usage can be found in Quantinuum's `H-Series Workflow <https://docs.quantinuum.com/h-series/user_guide/hardware_user_guide/workflow.html>`__ and `Getting Started <https://docs.quantinuum.com/h-series/trainings/getting_started/getting_started_index.html>`__ pages.

Users have access to the API validator to check program syntax, and to the Quantinuum System Model H1 and H2 emulators, which returns actual results back as if users submitted code to the real quantum hardware.

.. note::
   A recommended workflow for running on Quantinuum's quantum computers is to utilize the syntax checker first, run on the emulator, then run on one of the quantum computers.

.. _quantinuum-quotas:

Default Quotas
==============

Due to limited amount of resources, the default quotas are enforced:

* ``H1-1SC``, ``H2-1SC`` : Unlimited
* ``H1-1E`` : Unlimited
* ``H1-1``, ``H2-1``, ``H2-2`` : 0
* ``H2-1E``, ``H2-2E`` : 2000

As noted :ref:`below<quantinuum-alloc>`, quotas can be raised by sending a request to help@olcf.ornl.gov with sufficient justification.
To see your current usage or quotas in Quantinuum Nexus (e.g., how many HQC credits you have available), navigate to the `Organization section of your Account Settings <https://nexus.quantinuum.com/settings/organization>`__.

.. note::
   For resources that have "Unlimited" quota, the dashboard may make it seem like you do not have access to those resources; however, you do. If you have problems accessing those resources, please reach out to help@olcf.ornl.gov.


.. _quantinuum-alloc:

Allocations & Credit Usage
==========================

Running a job on the System Model H1 family and System Model H2 hardware requires Quantinuum Credits.
Additional information on credit usage for H-Series devices can be found in the `H-Series User Guide <https://docs.quantinuum.com/h-series/user_guide/hardware_user_guide/system_operation.html#estimating-circuit-time>`__.

* Any request for credits must be submitted by the project Principle Investigator (PI) to help@olcf.ornl.gov

* Requests for machine credits must be justified using results from the emulator to determine the appropriate amount needed. Requests without emulator-based justifications will be denied.

* Requests will be evaluated based on the provided technical justification, programmatic efficiency, and machine availability. The effective usage of prior allocations by the project will also be considered.

* Allocations will be granted on a monthly basis to maximize the availability of the H1 family and H2 machines. Please note that allocations do not carry over to the next month and must be consumed in the month granted. **Credits reset on the first day of every month.**
 
* Allocation requests requiring 20 qubits and fewer will be considered for H1 family machines, and allocation requests requiring 21 or more qubits will be considered for H2.

Allocation requests for the following month must be submitted no later than the 25th of the preceding month.
The uptime schedule is available on the *Calendar* tab of the legacy `Quantinuum User Portal <https://um.qapi.quantinuum.com/>`__, or by navigating to a specific backend in Nexus (e.g., for H1-1: https://nexus.quantinuum.com/backends/Quantinuum/H1-1 ).

Software
========

The TKET framework is a software platform for the development and execution of gate-level quantum computation, providing state-of-the-art performance in circuit compilation.
It was created and is maintained by Quantinuum.
The toolset is designed to extract the most out of the available NISQ devices of today and is platform-agnostic.

The ``pytket`` package is a python module for interfacing with tket (available for python 3.10+).
The ``pytket-quantinuum`` package is a python client enabling access to Quantinuum Systems, which is an alternative job submission tool to ``qnexus`` -- the python client to Quantinuum Nexus.

For more information, see the following links:

* `pytket documentation <https://tket.quantinuum.com/api-docs/>`__
* `pytket-quantinuum documentation <https://tket.quantinuum.com/extensions/pytket-quantinuum/>`__
* `qnexus documentation <https://docs.quantinuum.com/nexus/>`__

.. warning::
   Please note that the platform ``pytket-quantinuum`` serves is being replaced by Quantinuum Nexus and will be deprecated **March 31, 2025**. After this date, ``pytket-quantinuum`` will not be compatible with Quantinuum Nexus. For guidance on how to access H-Series through Nexus, please use the `qnexus <https://pypi.org/project/qnexus/>`__ Python package and the `Nexus Getting Started guide <https://docs.quantinuum.com/nexus/trainings/getting_started.html>`__.

Additional Resources
====================

* `Nexus Status Page <https://nexus-status.quantinuum.com/>`__ : Where you can automatically receive future maintenance announcements, reminders, incidents, and unplanned outage notifications.
 
