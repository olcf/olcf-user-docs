****
IonQ
****

Overview
========

IonQ offers access to trapped ion quantum computers and emulators,
accessible via their IonQ Quantum Cloud API. For the complete set of currently
available devices, qubit numbers, etc. see `IonQ Documentation <https://ionq.com/docs/>`__.
This guide describes how to use the system once you have access. For
instructions on how to gain access, see our :doc:`Quantum Access
</quantum/quantum_access>` page instead.


Connecting
==========

IonQ backends are available via the IonQ cloud interface via the API and also via many quantum Software Development Kits (SDK’s)

.. _ionq-cloud:

Cloud Access
------------

Users can access information about IonQ’s systems, view submitted jobs,
look up machine availability, and update job notification preferences via the `IonQ Cloud Console <https://cloud.ionq.com/jobs/>`__.

* Jupyter at OLCF: Access to the IonQ queues can also be obtained via `OLCF JupyterHub
  <https://jupyter-open.olcf.ornl.gov/>`__, a web-based interactive computing
  environment. See examples of common use case notebooks at `IonQ Notebook Samples <https://github.com/ionq-samples/>`__. 

.. _ionq-sdks:

.. _ionq-jobs:

Running Jobs & Queue Policies
=============================

Information on submitting jobs to IonQ systems, system availability,
checking job status, and tracking usage can be found via the `IonQ Cloud Console <https://cloud.ionq.com/jobs/>`__. 


.. note::
    A recommended workflow for running on IonQ's quantum computers is to
    utilize the emulator first, then run on one of the quantum computers. This is highlighted in the examples.



