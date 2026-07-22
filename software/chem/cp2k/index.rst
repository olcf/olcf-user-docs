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

----

Package Details
================

+-----------------------------+---------+--------------------------------------------------------------+
| Application or Library      | Version | Short Description                                            |
+=============================+=========+==============================================================+
| CP2K                        | 2026.1  | Quantum chemistry and molecular simulations                  |
+-----------------------------+---------+--------------------------------------------------------------+
| DBCSR                       | 2.9.1   | Sparse matrix operations library                             |
+-----------------------------+---------+--------------------------------------------------------------+
| SIRIUS                      | 7.10.0  | Plane-wave DFT library                                       |
+-----------------------------+---------+--------------------------------------------------------------+
| ROCm                        | 7.0.2   | AMD GPU runtime                                               |
+-----------------------------+---------+--------------------------------------------------------------+
| Cray MPICH                  | 9.1.0   | MPI implementation for parallel execution                    |
+-----------------------------+---------+--------------------------------------------------------------+

----

Usage
=====

To use CP2K, load the required modules:

.. code-block:: bash

    module load gcc-native/14.2
    module load cray-mpich/9.1.0
    module load rocm/7.0.2
    module load cp2k/2026.1-gpu-mpi-omp

Beginner's Guide
================

For new users of CP2K, an illustration of the workflow for a Quickstep DFT energy calculation
is provided below. Let us use a single water molecule as an example.

0. Prepare a working directory.
********************************
Before running a calculation, we need a working directory with the necessary input files and
basis sets. Your project directory is a good place to start. For example, if your project
directory is ``/lustre/orion/<project id>``, you might create a working directory named
``cp2k-water-example`` in the scratch space like:

.. code-block:: bash

    mkdir -p /lustre/orion/<project id>/scratch/cp2k-water-example
    cd /lustre/orion/<project id>/scratch/cp2k-water-example

1. Prepare the input file (``input.in``).
******************************************
Now, we need an input file which describes the system and the calculation parameters. A simple
input file for a single water molecule might look like this:

.. code-block:: bash

    &GLOBAL                                     ! calculation-wide settings
        PROJECT water                           ! a name for the calculation, used for output files
        RUN_TYPE ENERGY                         ! request a single-point energy calculation
        PRINT_LEVEL LOW
    &END GLOBAL
    &FORCE_EVAL                                 ! settings for evaluating energy and forces
        METHOD Quickstep                        ! use the Quickstep GPW/GAPW method
        &DFT
            BASIS_SET_FILE_NAME BASIS_MOLOPT    ! basis set file location
            POTENTIAL_FILE_NAME GTH_POTENTIALS  ! pseudopotential file location
            &MGRID
                CUTOFF 300                       ! plane-wave cutoff energy in Ry
            &END MGRID
            &XC
                &XC_FUNCTIONAL PBE               ! exchange-correlation functional
                &END XC_FUNCTIONAL
            &END XC
        &END DFT
        &SUBSYS
            &CELL
                ABC 8.0 8.0 8.0                  ! cell dimensions in Angstrom
            &END CELL
            &COORD                               ! atomic positions in Angstrom
                O   0.000  0.000  0.000
                H   0.757  0.586  0.000
                H  -0.757  0.586  0.000
            &END COORD
            &KIND O
                BASIS_SET DZVP-MOLOPT-GTH        ! basis set for oxygen
                POTENTIAL GTH-PBE-q6             ! pseudopotential for oxygen
            &END KIND
            &KIND H
                BASIS_SET DZVP-MOLOPT-GTH        ! basis set for hydrogen
                POTENTIAL GTH-PBE-q1             ! pseudopotential for hydrogen
            &END KIND
        &END SUBSYS
    &END FORCE_EVAL

Note that the ``!`` symbol followed by text indicates a comment.

2. Prepare the basis sets and pseudopotentials.
************************************************

A Quickstep calculation requires the ``BASIS_MOLOPT`` and ``GTH_POTENTIALS`` data files
referenced by ``BASIS_SET_FILE_NAME`` and ``POTENTIAL_FILE_NAME``. These files are provided
as part of the module and the environment variable ``CP2K_DATA_DIR`` points to their location.

3. Prepare the job submission script.
**************************************
To submit the calculation to the queue, we need a job submission script, like:

.. code-block:: bash

    #!/bin/bash
    #SBATCH -A <project id>
    #SBATCH -J water-scf
    #SBATCH -N 1
    #SBATCH -p batch
    #SBATCH -o %x-%j.out
    #SBATCH -t 10:00

    module load gcc-native/14.2
    module load cray-mpich/9.1.0
    module load rocm/7.0.2
    module load cp2k/2026.1-gpu-mpi-omp

    srun -N 1 -n 8 -c 7 --gpus-per-task=1 --gpu-bind=closest cp2k.psmp -i input.in > output.log

Here, we request 1 node, with 8 MPI ranks each bound to one GPU and 7 OpenMP threads, for 10
minutes. This example calculation only takes about one minute, so the requested time is
sufficient. Adjust the resource requests and walltime as needed for larger systems.

4. Submit the job to the queue with ``sbatch``.
*************************************************
Now we are ready to submit the job. Use the ``sbatch`` command to submit the job script to the
queue:

.. code-block:: bash

    sbatch <submit script>

Once in the queue, you can check the job status with ``squeue -u <username>``. Once the job
starts running, the output will be written to the file ``output.log`` as specified in the
submit script.

Congratulations! You have successfully run a Quickstep DFT energy calculation with CP2K on
Frontier. You can now analyze the output file and explore the results.

----

Helpful Links
=============

- CP2K home: https://www.cp2k.org
- User manual: https://manual.cp2k.org/trunk/
- In-depth review of CP2K features: https://pubs.acs.org/doi/10.1021/acs.jpcb.5c05851
