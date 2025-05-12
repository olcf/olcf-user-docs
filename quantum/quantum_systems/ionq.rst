****
IonQ
****

Overview
========

IonQ offers access to trapped ion quantum computers and simulators,
accessible via their IonQ Quantum Cloud Console. 
This guide describes how to use the system once you have access. For
instructions on how to gain access, see our :doc:`Quantum Access
</quantum/quantum_access>` page instead.

IonQ systems
============
Currently accessible IonQ trapped-ion systems include Aria (#AQ 25) and Forte (#AQ 36).

IonQ measures overall system size and performance using application-based benchmarking to determine the number of 
`algorithmic qubits, or #AQ <https://ionq.com/resources/algorithmic-qubits-a-better-single-number-metric>`__. 
An #AQ of N is roughly defined as the size of the largest circuit you can successfully run with N qubits and N^2
two-qubit gates.

For up-to-date characterization of these systems (including 1Q and 2Q gate error rates, SPAM 
error rates, dephasing times, and gate times, updated weekly), refer to the Backends tab on the
`IonQ Cloud Console <https://cloud.ionq.com/backends/>`__ (requires IonQ login).
This information is also available `via the IonQ API <https://docs.ionq.com/user-manual/glossary#characterizations>`__.
More information is also available on IonQ's website `here <https://ionq.com/quantum-systems/compare>`__.

IonQ also provides access to a cloud-based simulator, which can be used with 
`noise models based on Aria and Forte <https://docs.ionq.com/guides/simulation-with-noise-models>`__. 
The simulator can be accessed and used in the same way as IonQ’s trapped-ion hardware systems.

Connecting
==========

IonQ systems can be accessed directly via the IonQ API, as well as through several 
different quantum Software Development Kits (SDKs). The IonQ Cloud Console also
provides information about IonQ's quantum systems and user-submitted jobs.

.. _ionq-cloud:

Cloud Access
------------

Users can access information about IonQ's systems, monitor submitted jobs,
and view job results via the `IonQ Cloud Console <https://cloud.ionq.com/jobs/>`__.

Jupyter at OLCF: Access to IonQ systems can also be obtained via `OLCF JupyterHub
<https://jupyter-open.olcf.ornl.gov/>`__, a web-based interactive computing
environment, with any of the Python SDKs listed below.

.. _ionq-api:

IonQ API
--------

IonQ's systems can be accessed directly via their IonQ Cloud Platform API,
using ``curl`` to submit requests formatted in their language-agnostic JSON
circuit representation.  The complete API documentation is located at
`docs.ionq.com <https://docs.ionq.com/api-reference/v0.3/introduction>`__.

.. _ionq-sdks:

Quantum SDKs
------------

IonQ supports several different quantum software development kits, including:

* `Qiskit <https://ionq.com/docs/get-started-with-qiskit>`__
* `Cirq <https://ionq.com/docs/get-started-with-cirq>`__
* `ProjectQ <https://ionq.com/docs/get-started-with-projectq-on-ionq-hardware>`__
* `PennyLane <https://docs.ionq.com/sdks/pennylane/index>`__
* `qBraid <https://docs.ionq.com/sdks/qbraid/index>`__
* `Pytket <https://ionq.com/resources/hello-many-worlds-in-7-quantum-languages#hello-pytket>`__
* `XACC <https://ionq.com/resources/hello-many-worlds-in-7-quantum-languages#hello-xacc>`__

IonQ's guides for getting started with each of these frameworks are linked in this list.
Additionally, example Jupyter notebooks can be found in their
`getting-started GitHub repository <https://github.com/ionq-samples/getting-started>`__.

.. _ionq-api-keys:

API Keys
--------

Submitting jobs to IonQ's simulator or hardware requires an IonQ API key, which can be 
generated from the `IonQ Cloud Console <https://cloud.ionq.com/settings/keys>`__.
IonQ API keys can only be viewed when they are generated, and IonQ recommends storing
each API key locally in an environment variable. Instructions for generating and 
storing IonQ API keys can be found 
`here <https://docs.ionq.com/guides/managing-api-keys#managing-api-keys>`__.


.. _ionq-jobs:

Running Jobs & Queue Policies
=============================

Information on system availability, job status, and usage can be found in the
`IonQ Cloud Console <https://cloud.ionq.com/jobs/>`__.

Jobs can be submitted to the IonQ simulator or hardware using the IonQ API or any 
of the SDKs listed above. Each approach has a slightly different syntax for connecting
to the IonQ Cloud Platform and specifying which system to use, as described in the
guides and documentation linked above.

.. note::
    A recommended workflow for running on IonQ's quantum computers is to
    utilize the simulator first, then run on one of the quantum computers. This is highlighted in the examples.

.. _ionq-alloc:

Allocations & Credit Usage
==========================

Usage of IonQ’s trapped-ion hardware systems is recorded in 2-qubit gate equivalents. Usage of IonQ’s cloud simulator,
including with hardware-based noise models, is unlimited and requires no credits to use.

Running a job on IonQ hardware requires IonQ Credits. In order to request an IonQ Credit allocation, please adhere to the following policy:

* Any request for credits must be submitted by the project Principle Investigator (PI) by logging into `myOLCF <https://my.olcf.ornl.gov>`__, select your QCUP project under "My Projects" after login, and use the `Quantum Allocation Request form <https://my.olcf.ornl.gov/allocations/quantumAllocation>`__ under the "Allocations" section. Alternatively, you can send a request through our help ticket system (help@olcf.ornl.gov).

* Requests for machine credits must be justified using results from the appropriate simulator to determine the appropriate amount needed. Requests without simulator-based justifications will be denied. Using `IonQ's Resource Estimator <https://ionq.com/programs/research-credits/resource-estimator>`__ is also highly recommended.

* Requests will be evaluated based on the provided technical justification, programmatic efficiency, and machine availability. The effective usage of prior allocations by the project will also be considered.

Users can obtain additional information about their allocation and credit usage by contacting help@olcf.ornl.gov.


.. _ionq-systems:

Checking System Availability & Capability
=========================================

The `Backends tab on the IonQ Cloud Console <https://cloud.ionq.com/backends>`__ 
shows the status, average time in queue, and applicable characterization data for 
each QPU and simulator.

Additionally, `status.ionq.co <https://status.ionq.co/>`__ provides the most up-to-date information about system status 
and outages, including more details about historical availability and queue time. Users can also sign up for system 
status notifications.

.. _ionq-resources:

Additional Resources
====================

IonQ's Resource Center provides additional `docs <https://ionq.com/resources?type=docs>`__ 
and `guides <https://ionq.com/resources?type=guide>`__, as well as examples and 
case studies, on topics including:

* `Best practices for using IonQ's fully-connected trapped-ion hardware <https://ionq.com/docs/best-practices-for-using-ionq-hardware>`__
* `Debiasing and sharpening (IonQ's default error mitigation technique) <https://ionq.com/resources/debiasing-and-sharpening>`__
* `Getting started with hardware noise model simulation <https://ionq.com/docs/get-started-with-hardware-noise-model-simulation>`__
* `Using IonQ's hardware-native gate set <https://ionq.com/docs/getting-started-with-native-gates>`__,
  including with `Qiskit <https://ionq.com/docs/using-native-gates-with-qiskit>`__,
  `Cirq <https://ionq.com/docs/using-native-gates-with-cirq>`__,
  and `Pennylane <https://ionq.com/docs/using-native-gates-with-pennylane>`__


The Resource Center also includes more in-depth courses with recorded lectures on quantum computing 
`hardware <https://ionq.com/resources/anthology/lecture-series-introduction-to-quantum-computers>`__ and
`programming <https://ionq.com/resources/anthology/lecture-series-introduction-to-quantum-programming>`__, 
focused on IonQ’s trapped-ion systems and their applications.



