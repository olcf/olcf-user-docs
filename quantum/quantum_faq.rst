
**************************
Frequently Asked Questions
**************************

How do quantum computers differ from classical computers? 
=========================================================

Conventional/classical computing utilizes information storage based on digital
devices storing “bits”, which are in either of two distinct states at a given
time, i.e. 0 or 1. Quantum computers utilize properties of quantum mechanics,
such as superposition and entanglement, in order to exceed certain capabilities
of classical computers. Superposition means that the units of information
storage can be in multiple states at the same time, and entanglement means the
states can depend on each other.  In quantum computing systems, information is
stored not using “bits”, but instead using “qubits”.

What is a qubit? 
================

A qubit (pronounced “cue-bit”, a portmanteau of “quantum bit”) is the physical
unit of quantum information in quantum computing. It is the quantum version of
a bit (itself a portmanteau of “binary digit”), consisting of a two-state
quantum mechanical system that can (like a classical bit) exist in one state,
`|0⟩`, or the other, `|1⟩`, but unlike the classical bit counterpart, a qubit
can also be in a quantum superposition of both states.

How do I access the OLCF quantum computing resources? 
=====================================================
Applications for both Quantum Computing projects and quantum user accounts can
be found on the :doc:`/quantum/quantum_access` page.

What happens after I apply for access to QCUP? 
==============================================

Applications are put through a merit review process, and you will be contacted
regarding the status of your application. See the user documentation page for
more details.

I formerly had access to quantum resources, but my backends/lattices/etc. have disappeared, what do I do? 
=========================================================================================================

If your account was established prior to July 5th, 2020, and was not through
the OLCF directly, your access to quantum resources has been removed, and you
will need to re-apply to an OLCF project.  Also, if your access to your OLCF
project or the project access itself has expired, you will also need to
reapply. Please contact help@olcf.ornl.gov for assistance.

I applied to a quantum computing resource via the vendor website, but don’t have access; what do I do? 
======================================================================================================

Making an account on the vendor website does not enable access to OLCF
projects; Access requires an account through an OLCF-affiliated website, and
applying for an OLCF quantum account (see above).

It says I have 0 credits, how do I get credits to run on the actual quantum hardware?
=====================================================================================

For most vendors, QCUP requires you to run on a simulator or emulator first to
verify expected usage for your experiment(s).  After verifying how many credits
you need through mock, simulation, or emulation runs, your project can then
request credits on the hardware.

To ensure the efficient use of resources, the following allocation policy is in effect:

* All credit or time requests must be submitted by the project's Principal
  Investigator (PI). Requests can be made through the Quantum Allocation
  Request form available under the "Allocations" section in
  `myOLCF <https://my.olcf.ornl.gov/login>`__ (select your QCUP project under
  "My Projects" after login). Alternatively, you may submit a request via the
  OLCF Help Ticket System at help@olcf.ornl.gov.

* Requests must include a technical justification that demonstrates an
  understanding of the resource requirements for the proposed quantum workload.
  Users must simulate their workloads using the appropriate simulator,
  emulator, or resource estimation tools provided by the vendor to estimate
  circuit depth, qubit usage, execution time, and other relevant metrics.

* Below are links to each vendor-specific instructions and policies:

  * :ref:`IBM Allocation Instructions <ibm-alloc>`
  * :ref:`Quantinuum Allocation Instructions <quantinuum-alloc>`
  * :ref:`IonQ Allocation Instructions <ionq-alloc>`
  * :ref:`IQM Allocation Instructions <iqm-alloc>`

For questions or assistance with preparing a request, contact help@olcf.ornl.gov.
