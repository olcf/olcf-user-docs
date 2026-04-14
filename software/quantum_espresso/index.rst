.. _quantum_espresso:

*****************************
Quantum ESPRESSO Introduction
*****************************

Overview
========

This document provides an introduction to the Quantum ESPRESSO software package installed on Frontier.
Quantum ESPRESSO is a plane-wave DFT code plus various utilities for electronic structure calculations
and materials modeling, and post-processing tools.

.. note::

    The current implementation of Quantum ESPRESSO is the 
    `GPU-enabled version <https://github.com/electronic-structure/q-e-sirius>`_ which utilizes the 
    `SIRIUS library <https://github.com/electronic-structure/SIRIUS>`_ for efficient GPU computations.
    This version is not the same as the standard CPU-only version of Quantum ESPRESSO, and is missing
    some functionality, but has much better performance characteristics.

**Currently installed version of Quantum ESPRESSO and its dependencies:**

+-----------------------------+--------+
| ``Quantum ESPRESSO-SIRIUS`` | 1.0.2  |
+=============================+========+
| SIRIUS Library              | 7.10.0 |
+-----------------------------+--------+

