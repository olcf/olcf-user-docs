.. _cp2k:

****
CP2K
****

.. contents:: On this page
   :local:
   :depth: 2

Overview
========

CP2K is a quantum chemistry and solid state physics software package that performs atomistic simulations of
solid state, liquid, molecular, and biological systems. It provides two main methods for electronic structure
calculations: the Quickstep method for Gaussian and plane-wave (GPW) and Gaussian and augmented plane-wave
(GAPW) calculations, and SIRIUS for plane-wave DFT calculations. Both methods are GPU-accelerated and can
be used as the basis for ab-initio molecular dynamics simulations.

Package Details
===============

+-----------------------------+---------+--------------------------------------------------------------+
| Application or Library      | Version | Short Description                                            |
+=============================+=========+==============================================================+
| CP2K                        | 2026.1  | Quantum chemistry and molecular simulations                  |
+-----------------------------+---------+--------------------------------------------------------------+
| DBCSR                       | 2.9.1   | Sparse matrix operations library                             |
+-----------------------------+---------+--------------------------------------------------------------+
| SIRIUS                      | 7.10.0  | Plane-wave DFT library                                       |
+-----------------------------+---------+--------------------------------------------------------------+
| ROCm                        | 7.0.2   | AMD GPU runtime                                              |
+-----------------------------+---------+--------------------------------------------------------------+
| Cray MPICH                  | 9.1.0   | MPI implementation for parallel execution                    |
+-----------------------------+---------+--------------------------------------------------------------+

Using CP2K
==========

To use CP2K, load the required modules first:

.. code-block:: bash

    module load gcc-native/14.2
    module load cray-mpich/9.1.0
    module load rocm/7.0.2
    module load cp2k/2026.1-gpu-mpi-omp

then invoke the executable with ``srun``:

.. code-block:: bash

    srun <srun options> cp2k.psmp -i input.in > output.out

A typical submit script for a calculation utilizing one node with 8 MPI ranks, 
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
    module load cp2k/2026.1-gpu-mpi-omp

    srun -N 1 -n 8 -c 7 --gpus-per-task=1 --gpu-bind=closest cp2k.psmp -i <input>.in > <output>.out

Links
=====

- CP2K home: https://www.cp2k.org
- User manual: https://manual.cp2k.org/trunk/
- In-depth review of CP2K features: https://pubs.acs.org/doi/10.1021/acs.jpcb.5c05851
