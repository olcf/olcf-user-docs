.. _quantum_espresso:

****************
Quantum ESPRESSO
****************

.. contents:: On this page
   :local:
   :depth: 2

Overview
========

Quantum ESPRESSO is a plane-wave electronic structure code and associated post-processing tools. Among
its capabilities are density functional theory (DFT) calculations and molecular dynamics simulations.

.. note::

    The current implementation of Quantum ESPRESSO is the 
    `GPU-enabled version <https://github.com/electronic-structure/q-e-sirius>`_ which utilizes the 
    `SIRIUS library <https://github.com/electronic-structure/SIRIUS>`_ for efficient GPU computations.
    This version is not the same as the standard CPU-only version of Quantum ESPRESSO, and is missing
    some functionality, but has much better plane-wave DFT performance.

----

Package Details
===============

+-----------------------------+---------+--------------------------------------------------------------+
| Application or Library      | Version | Short Description                                            | 
+=============================+=========+==============================================================+
| Quantum ESPRESSO-SIRIUS     | 1.0.2   | Electronic structure calculations and utilities              |  
+-----------------------------+---------+--------------------------------------------------------------+
| SIRIUS                      | 7.10.0  | Plane-wave DFT library                                       |
+-----------------------------+---------+--------------------------------------------------------------+
| ROCm                        | 7.0.2   | AMD GPU runtime                                              |
+-----------------------------+---------+--------------------------------------------------------------+
| Cray MPICH                  | 9.1.0   | MPI implementation for parallel execution                    |
+-----------------------------+---------+--------------------------------------------------------------+

----

Using Quantum ESPRESSO
======================

To use Quantum ESPRESSO, load the required modules first:

.. code-block:: bash

    module load gcc-native/14.2
    module load cray-mpich/9.1.0
    module load rocm/7.0.2
    module load q-e-sirius/1.0.2

then invoke the executable with ``srun``:

.. code-block:: bash

    srun <srun options> pw.x -in input.in > output.out

A typical submit script for a plane-wave DFT calculation utilizing one node with 8 MPI ranks, 
each bound to one GPU and 7 OpenMP threads, would look like this:

.. code-block:: bash

    #!/bin/bash
    #SBATCH -A <project id>
    #SBATCH -J <job name>
    #SBATCH -N 1
    #SBATCH -p batch
    #SBATCH -o %x-%j.out
    #SBATCH -t <walltime limit>

    module load gcc-native/14.2
    module load cray-mpich/9.1.0
    module load rocm/7.0.2
    module load q-e-sirius/1.0.2

    srun -N 1 -n 8 -c 7 --gpus-per-task=1 --gpu-bind=closest pw.x -in <input>.in > <output>.out

----

Beginner's Guide
================

For new users of Quantum ESPRESSO, an illustration of the workflow for a plane-wave DFT calculation 
is provided below.

1. Prepare the input file (``input.in``).
2. Prepare the pseudopotentials.
3. Prepare the job submission script.
4. Submit the job to the queue with ``sbatch``. 

----

Helpful Links
=============

- Documentation: https://www.quantum-espresso.org/documentation/package-specific-documentation
- Quantum ESPRESSO input generator: https://qeinputgenerator.materialscloud.io
- Standard solid-state pseudopotentials: https://legacy.materialscloud.org/discover/sssp/table/efficiency
