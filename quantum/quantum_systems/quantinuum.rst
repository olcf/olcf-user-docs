**********
Quantinuum
**********

Overview
========

Quantinuum offers access to trapped ion quantum computers and emulators, accessible via their API and Quantinuum Nexus user portal.
For the complete set of currently available devices, qubit numbers, etc. see the *Backends* tab on `Nexus <https://nexus.quantinuum.com/backends>`__. 

This guide describes how to use the system once you have access.
For instructions on how to gain access, see our :doc:`Quantum Access </quantum/quantum_access>` page instead.

Quantinuum's documentation for both Nexus and the Quantinuum Systems can be found here: https://docs.quantinuum.com/

Features
--------

The complete set of Quantinuum System Model H2 and Helios hardware specifications and operations, can be found in their `Quantinuum Systems User Guide <https://docs.quantinuum.com/systems/user_guide/hardware_user_guide/access.html>`__.

Features include, but are not limited to:

* All-to-all connectivity

* Laser based quantum gates

* Linear trap Quantum Charge-Coupled Device (QCCD) architecture with four or more parallel gate zones

* Mid-circuit measurement conditioned circuit branching

* Qubit reuse after mid-circuit measurement

* Native gate set: single-qubit rotations, two-qubit ZZ-gates, parametrized angle ZZ gate


Connecting
==========

.. _quantinuum-cloud:

Cloud Access
------------

Users can access information about Quantinuum's systems, view submitted jobs, look up machine availability, and update job notification preferences on `Quantinuum Nexus <https://nexus.quantinuum.com/>`__. 


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

Locally
-------

Users can submit jobs that run remotely on Quantinuum's systems from a local python development environment.
Directions for setting up the python environment and getting started in a notebook locally, as well as additional examples are found on the `Quantinuum Systems Getting Started page <https://docs.quantinuum.com/systems/trainings/helios/getting_started/index.html>`__, the `Nexus Getting Started page <https://docs.quantinuum.com/nexus/trainings/getting_started.html>`__, and the `Guppy Getting Started page <https://docs.quantinuum.com/guppy/getting_started.html>`__.

.. _quantinuum-jobs:

Running Jobs & Queue Policies
=============================

Information on submitting jobs to Quantinuum Systems, system availability, checking job status, and tracking usage can be found in Quantinuum's `Workflow page <https://docs.quantinuum.com/systems/user_guide/hardware_user_guide/workflow.html>`__.

Users have access to the Syntax Checkers (SC endpoints) to check program syntax, and to the Quantinuum System H2 and Helios emulators, which returns actual results back as if users submitted code to the real quantum hardware.

.. note::
   A recommended workflow for running on Quantinuum's quantum computers is to utilize a syntax checker first, run on an emulator, then run on one of the quantum computers.

.. _quantinuum-quotas:

Default Quotas
==============

Due to limited resources, the default quotas are enforced:

* ``H2-1SC``, ``H2-2SC``, ``Helios-1SC`` : Unlimited
* ``H2-1``, ``H2-2``, ``Helios-1`` : 0
* ``H2-1E``, ``H2-2E``, ``Helios-1E`` : Unlimited
* **Nexus Simulation Time**: 6000 s
* **Nexus Compilation Time**: 6000 s
* **Nexus Storage**: 500 MB
* **Nexus Lab**: First come, first served (total 500 hours shared among all QCUP users)

As noted :ref:`below<quantinuum-alloc>`, quotas can be raised by sending a request to help@olcf.ornl.gov with sufficient justification.
To see your current usage or quotas in Quantinuum Nexus (e.g., how many HQC credits you have available), navigate to the `Organization section of your Account Settings <https://nexus.quantinuum.com/settings/organization>`__.

.. note::
   For resources that have "Unlimited" quota, the dashboard may make it seem like you do not have access to those resources; however, you do. If you have problems accessing those resources, please reach out to help@olcf.ornl.gov.


.. _quantinuum-alloc:

Allocation Policies & Credit Usage
==================================

Running a job on Quantinuum Systems hardware requires Quantinuum Hardware Quantum Credits (HQCs).
Additional information on credit usage for Quantinuum endpoints can be found in the `System Workflow page <https://docs.quantinuum.com/systems/user_guide/hardware_user_guide/workflow.html#tracking-usage-with-hardware-quantum-credits-hqcs>`__ and the `System Operation page <https://docs.quantinuum.com/systems/user_guide/hardware_user_guide/operation.html>`__ in the Quantinuum Systems User Guide.

* Any request for credits must be submitted by the project Principle Investigator (PI) by logging into `myOLCF <https://my.olcf.ornl.gov>`__, select your QCUP project under "My Projects" after login, and use the `Quantum Allocation Request form <https://my.olcf.ornl.gov/allocations/quantumAllocation>`__ under the "Allocations" section. Alternatively, you can send a request through our help ticket system (help@olcf.ornl.gov).

* Requests for machine credits must be justified using results from the emulator to determine the appropriate amount needed. Requests without emulator-based justifications will be denied.

* Requests will be evaluated based on the provided technical justification, programmatic efficiency, and machine availability. The effective usage of prior allocations by the project will also be considered.

* Allocations will be granted on a monthly basis to maximize the availability of the Quantinuum devices. Please note that allocations do not carry over to the next month and must be consumed in the month granted. **Credits reset on the first day of every month.**

* To ensure efficient utilization of our hardware resources, allocations will be considered for two phases:

    #. The first 3 weeks of the month (credits granted at the beginning of the month): ensured resource is available for your request
    #. The last week of the month (credits granted the last full week of the month): resource may become unavailable due to high demand, at which point request for time in future months is expected

Allocation requests for the following month must be submitted no later than the 25th of the preceding month.
The uptime schedule is available by navigating to a specific backend in Nexus (e.g., for H2-1: https://nexus.quantinuum.com/backends/Quantinuum/H2-1 ).

Software
========

Guppy is a quantum-first programming language embedded in python. It provides state-of-the art features for utilizing the complete set of Helios features available.

For more information, see the following links:

* `Guppy documentation <https://docs.quantinuum.com/guppy/getting_started.html>`__
* `qnexus documentation <https://docs.quantinuum.com/nexus/>`__

Additional Resources
====================

* `Nexus Status Page <https://nexus-status.quantinuum.com/>`__ : Where you can automatically receive future maintenance announcements, reminders, incidents, and unplanned outage notifications.
 
