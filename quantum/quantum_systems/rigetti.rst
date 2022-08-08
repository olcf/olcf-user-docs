.. _rigetti-guide:

*******
Rigetti
*******

Overview
========

Rigetti currently offers access to their systems via their Quantum Cloud
Services (QCS).  With QCS, Rigetti's quantum processors (QPUs) are tightly
integrated with classical computing infrastructure and made available to you
over the cloud. Rigetti also provides users with quantum computing example
algorithms for optimization, quantum system profiling, and other applications.

A list of available Rigetti systems/QPUs, along with their performance statistics,
can be found on the `Rigetti Systems Page <https://qcs.rigetti.com/qpus>`__.

In addition to the :ref:`rigetti-running` section below, a general workflow
overview of how programs are run with Rigetti's QCS can be found on Rigetti's
`How Programs Are Built & Run Guide
<https://docs.rigetti.com/qcs/guides/how-programs-are-built-and-run>`__.

The guide below describes how to use the system(s) once you have access.
For instructions on how to gain access, see our :doc:`Quantum Access
</quantum/quantum_access>` page instead.

Connecting
==========

Access to the Rigetti Quantum Computing queue and simulators can be obtained
via multiple methods -- either through the :ref:`cloud <rigetti-cloud>` or 
:ref:`locally <rigetti-local>`.

.. _rigetti-cloud:

Cloud Access
------------

Rigetti provides system access via a cloud-based JupyterLab development
environment: `<https://docs.rigetti.com/qcs/getting-started/jupyterlab-ide>`__.  From
there, users can access a JupyterLab server loaded with Rigetti's PyQuil
programming framework, Rigetti's Forest Software Development Kit, and
associated program examples and tutorials.  This is the method that allows
access to Rigetti's QPU's directly, as opposed to simulators. 

.. _rigetti-local:

Locally via Forest SDK
----------------------

Users are able to install Rigetti software locally for the purpose of
development using a provided Quantum Virtual Machine, or QVM, an implementation
of a quantum computer simulator that can run Rigetti's Quil programs.  This can
be done via two methods:

* Installing manually: `<https://docs.rigetti.com/qcs/getting-started/installing-locally>`__

* Docker: `<https://hub.docker.com/r/rigetti/forest>`__

.. _rigetti-running:

Running Jobs
============

Reservations
------------

All jobs run on Rigetti's systems are submitted via system reservation.  This
can be done either by using Rigetti's QCS dashboard to schedule the
reservation, or via interacting with the QCS via the Command Line Interface
(CLI).  Scheduled reservations can be viewed and/or cancelled via either
method, either in the dashboard or from the CLI.  

* To submit a reservation via the QCS dashboard: `<https://docs.rigetti.com/qcs/guides/reserving-time-on-a-qpu#using-the-qcs-dashboard>`__

* To submit a reservation via the QCS CLI, and installation instructions: `<https://docs.rigetti.com/qcs/guides/using-the-qcs-cli>`__

Submitting Jobs
---------------

Accessing the Rigetti QPU systems can only be done during a user's reservation
window.  To submit a job, users must have JupyterHub access to the system.  QVM
jobs can be run without network access in local environments.  Jobs are
compiled via Quilc and submitted via pyQuil (see :ref:`Software Section <rigetti-soft>` below) in a python environment
or Jupyter notebook. 

Allocations & Credit Usage
==========================

Running a job on the Aspen-M-1 and Aspen-11 systems requires Rigetti credits, which are exchanged for system reservation time.  Users are initially allocated credits equivalent to 60 minutes of reservation time at the beginning of a project, but requests for increased allocations should be submitted (with a brief explanation) to help@olcf.ornl.gov and will be reviewed by the QRUC.

Data Storage Policies
=====================

Any work saved in your QCS JupyterLab will be saved and maintained.  

.. _rigetti-soft:

Software
========

* Quil: The Rigetti-developed quantum instruction/assembly language: `<https://pyquil-docs.rigetti.com/en/stable/compiler.html>`__
* Quil-T: an extension of Quil with enhanced control of microwave input signals, gate definitions and pulse parameters: `<https://pyquil-docs.rigetti.com/en/stable/quilt.html>`__
* Forest SDK: Rigetti-provided software tools for writing quantum programs in Quil, compiling and running them. 

  * PyQuil: PyQuil is a Python library for writing and running quantum programs using Quil: `<https://pyquil-docs.rigetti.com/en/stable/>`__

  * Quilc: Quilc is an optional optimizing compiler for Rigetti QPU code deployment: `<https://pyquil-docs.rigetti.com/en/v2.1.1/quilc-man.html>`__

Additional Resources
====================

* `Rigetti's Documention <https://docs.rigetti.com/qcs/>`__

* `Rigetti System Performance Data <https://qcs.rigetti.com/qpus/>`__
