.. _ibm-quantum-guide:

***********
IBM Quantum
***********

Overview
========

IBM's quantum processors are made up of superconducting transmon qubits, and
users can utilize these systems via the universal, gate-based, circuit model of
quantum computation.

This guide describes how to use the system once you have access. For
instructions on how to gain access, see our :doc:`Quantum Access
</quantum/quantum_access>` page instead.

.. _ibm-connecting:

Connecting
==========

Access to the IBM Quantum Computing queues can be obtained via multiple methods
-- either through the :ref:`cloud <ibm-cloud>` or :ref:`locally <ibm-local>`.

.. _ibm-cloud:

Cloud Access
------------

Users can access information about IBM Quantum's systems, view queue
information, and submit jobs on their cloud dashboard at
`<https://quantum.cloud.ibm.com/>`__. The cloud dashboard allows access to
IBM Quantum's graphical circuit builder, Quantum Composer, and associated
program examples.

.. _ibm-local:

Locally via Qiskit
------------------

IBM Quantum provides Qiskit (Quantum Information Software Kit for Quantum
Computation) for working with OpenQASM and the IBM Q quantum processors.
Qiskit allows users to build quantum circuits, compile them for a particular
backend, and run the compiled circuits as jobs. Additional information on using
Qiskit is available at `<https://qiskit.org/learn/>`__ and in our 
:ref:`Software Section <ibm-soft>` below.

Users are able to install IBM Quantum's Qiskit locally like so: 

* Installing manually: `<https://quantum.cloud.ibm.com/docs/en/guides/install-qiskit>`__.
  This option allows for building locally and executing jobs via a python virtual
  environment.


.. _ibm-jobs:

Running Jobs & Queue Policies
=============================

User can submit jobs to IBM Quantum backends both via a fair-sharing queue
system as well as via priority sessions system.  As discussed below, the
dynamic fair-sharing queue system determines the queuing order of jobs so as to
fairly balance system time between access providers, of which the OLCF QCUP is
only one.  Because of this, the order of when a user's job in the fair-share
queue will run varies dynamically, and can't be predicted. In light of this,
for time-critical applications or iterative algorithms, IBM Quantum recommends
users consider using sessions. 

Fair-Share Queue Policy
-----------------------

When jobs are submitted on IBM Quantum backends, the jobs enter into the 
"fair-share" queuing system, in which jobs run in a dynamically calculated
order so as to provide fair sharing among all users of the device, to prevent
individual projects or users from monopolizing a given backend.  

All OLCF users have access to the "premium" (>=20 qubits) devices in the Washington DC (us-east) region.


Allocations & Usage Limits
--------------------------

* **Project allocations have a default limit of 100 minutes during a moving 28-day window**.
* Minutes are shared across all users on a given project and across all backends.
* Usage greater than 10 minutes will see a slight priority reduction in the queue, but will still be able to use up to 100 minutes by default. If you notice the queue reduction after 10 minutes being an issue, reach out to help@olcf.ornl.gov with justification for the higher-throughput need.
* Once a project reaches the 100 minute usage limit, no jobs will be able to run until minutes are freed up on the project (see :ref:`example <ibm-window>`  below).
* **A higher usage limit greater than 100 minutes is possible (see information below)**

If you are planning to use a large allocation (over 100 minutes), please send a usage request to our Quantum Resource Utilization Council (QRUC) by logging into `myOLCF <https://my.olcf.ornl.gov>`__, select your QCUP project under "My Projects" after login, and use the `Quantum Allocation Request form <https://my.olcf.ornl.gov/allocations/quantumAllocation>`__ under the "Allocations" section.
Alternatively, you can send a request through our help ticket system (help@olcf.ornl.gov).
**Special requests must be submitted by a project PI with sufficient computational and scientific justification.**
QRUC will evaluate the merit of your request, and if approved, can get you the additional time you need for your work.

.. note::
   Approved usage over 100 minutes won't see the same priority reduction seen in the 10-100 minute range.

For more information on how job priority is affected based on your limit, please see `<https://quantum.cloud.ibm.com/docs/guides/fair-share-scheduler#fair-share-scheduler>`__.

.. _ibm-window:

The 28-day rolling window
^^^^^^^^^^^^^^^^^^^^^^^^^

The new 28-day rolling window only considers usage in a given 28 days.
Every new day, the window "rolls" by 1 day, which effectively erases usage run on the specific day 29 days ago.
Any past usage that has fallen out of the new window is no longer accounted for, thus freeing up usage on the project.
If no past usage falls out of the new window (i.e., no jobs were run specifically 29 days ago), then no minutes get freed up.

Example window
""""""""""""""

Example for a project that has a 1000 minute limit in the ``10/18-11/15`` window.
For simplicity, let's just say in this example that they aren't running any new jobs right now, and have only run jobs in the past.

The "current" ``10/18-11/15`` window:

* 100 minutes used on 10/18
* 10 minutes used on 10/22
* 500 minutes used on 10/24

A total of 610 minutes out of 1000 limit.

Tomorrow's window ``10/19-11/16``:

* 10 minutes used on 10/22
* 500 minutes used on 10/24

A total of 510 minutes out of 1000 limit (100 minutes "freed" up because they fell out of the rolling window).

The next window ``10/20-11/17``:

* 10 minutes used on 10/22
* 500 minutes used on 10/24

Still 510 minutes accounted for since no "new" past usage rolled out of the window.

The takeaway is that if I run a job on Day XYZ, then I won't get those minutes back until 29 days from Day XYZ.
Until then, they will be accounted for in a given window and count toward the minute limit for a project.


Submitting Jobs
---------------

Jobs are compiled and submitted via Qiskit in a Python virtual environment or
Jupyter notebook (see :ref:`Cloud Access <ibm-cloud>` and
:ref:`Local Access <ibm-local>` sections above).

* Circuit jobs comprise jobs of constructed quantum circuits and algorithms
  submitted to backends in IBM Quantum fair-share queue.

* Program jobs utilize a pre-compiled quantum program utilizing the Qiskit
  Runtime framework.


Sessions
--------

A session in Qiskit Runtime is a tool designed for running multiple jobs in sequence more effectively.
It streamlines the process by grouping jobs together, reducing the wait times often associated with individually queued jobs. 
For more information on sessions can be found here:
`<https://quantum.cloud.ibm.com/docs/en/guides/run-jobs-session>`__


Checking System Availability & Capability
=========================================

Current status listings and system capabilities for IBM
Quantum's quantum resources can be found here:
`<https://quantum.cloud.ibm.com/computers>`__

.. note::
    The IBM Quantum cloud platform allocates OLCF users all QPUs in the Washington DC (us-east) region.
    If you would like access to QPUs in the Frankfurt region, please submit a help ticket to help@olcf.ornl.gov.


.. _ibm-soft:

Software
========

* Qiskit documentation is available at `<https://quantum.cloud.ibm.com/docs/guides>`__

* `Qiskit Aer <https://qiskit.github.io/qiskit-aer/>`__ is IBM Quantum's package for simulating quantum circuits, with
  different backends for specific types of simulation

Additional Resources
====================

* `IBM's Documentation <https://quantum.cloud.ibm.com/docs>`__
* `IBM's Announcements Page <https://quantum.cloud.ibm.com/announcements>`__ : Includes service alerts (retirements, downtimes) and product updates. 
