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

Usage
=====

To use Quantum ESPRESSO, load the required modules:

.. code-block:: bash

    module load gcc-native/14.2
    module load cray-mpich/9.1.0
    module load rocm/7.0.2
    module load q-e-sirius/1.0.2

Beginner's Guide
================

For new users of Quantum ESPRESSO, an illustration of the workflow for a plane-wave DFT calculation 
is provided below. Let us use the silicon crystal primitive cell as an example.

0. Prepare a working directory.
*******************************
Before running a calculation, we need a working directory with the necessary input files and pseudopotentials.
Your project directory is a good place to start. For example, if your project directory is
``/lustre/orion/<project id>``, you might create a working directory named ``qe-silicon-example`` in the scratch
space like:

.. code-block:: bash

    mkdir -p /lustre/orion/<project id>/scratch/qe-silicon-example
    cd /lustre/orion/<project id>/scratch/qe-silicon-example


1. Prepare the input file (``input.in``).
*****************************************
Now, we need an input file which describes the system and the calculation parameters. A simple input file for a
silicon primitive cell might look like this:

.. code-block:: bash

    &control                                    ! calculation parameters and settings
        calculation = 'scf'                     ! request a self-consistent field energy calculation
        prefix = 'silicon'                      ! a name for the calculation, used for output files
        outdir = './tmp'                        ! directory for temporary files
        pseudo_dir = '.'                        ! directory where pseudopotential files are located
    /
    &system                                     ! chemical system parameters
        ibrav = 2                               ! Bravais lattice index for face-centered cubic lattice: only one lattice parameter is needed
        celldm(1) = 10.26                       ! The lattice parameter A in atomic units (1 Bohr = 0.529177 Angstroms)
        nat = 2                                 ! Number of atoms in the unit cell
        ntyp = 1                                ! Number of types of atoms
        ecutwfc = 30.0                          ! Plane-wave cutoff energy in Ry
    /
    &electrons
        conv_thr = 1.0d-8                       ! Convergence threshold for self-consistency
    /
    ATOMIC_SPECIES
        Si 28.0855 Si.pbe-n-kjpaw_psl.1.0.0.UPF ! Element, atomic mass, and pseudopotential file
    ATOMIC_POSITIONS crystal                    ! Defining positions in crystal coordinates
        Si 0.00 0.00 0.00
        Si 0.25 0.25 0.25
    K_POINTS automatic                          ! k-point grid for Brillouin zone sampling
        4 4 4 1 1 1                             ! 4x4x4 grid with no shift

Note that the ``!`` symbol followed by text indicates a comment.

2. Prepare the pseudopotentials.
********************************

A plane-wave DFT calculation requires pseudopotential (PP) files for each type of atom in the system.
Download the PP file and place it in the working directory (as specified by ``pseudo_dir '.'`` in the input file). Alternatively, you can
collect your PP files in a central directory and point to it with the ``pseudo_dir`` variable.

3. Prepare the job submission script.
*************************************
To submit the calculation to the queue, we need a job submission script, like:

.. code-block:: bash

    !!/bin/bash
    !SBATCH -A <project id>
    !SBATCH -J Si2-scf
    !SBATCH -N 1
    !SBATCH -p batch
    !SBATCH -o %x-%j.out
    !SBATCH -t 10:00

    module load gcc-native/14.2
    module load cray-mpich/9.1.0
    module load rocm/7.0.2
    module load cray-hdf5-parallel/1.14.3.9
    module load q-e-sirius/1.0.2

    srun -N 1 -n 1 -c 1 --gpus-per-task=1 --gpu-bind=closest pw.x -in input.in > output.log

Here, we request 1 node, with 1 MPI rank, 1 CPU core, and 1 GPU for 10 minutes. This example calculation
only takes about one minute, so the requested time is sufficient. Adjust the resource requests and walltime
as needed for larger systems.


4. Submit the job to the queue with ``sbatch``. 
***********************************************
Now we are ready to submit the job. Use the ``sbatch`` command to submit the job script to the queue:

.. code-block:: bash

    sbatch <submit script>

Once in the queue, you can check the job status with ``squeue -u <username>``. Once the job starts running,
the output will be written to the file ``output.log`` as specified in the submit script.

Congratulations! You have successfully run a plane-wave DFT calculation with Quantum ESPRESSO on Frontier. 
You can now analyze the output file and explore the results.

----

Helpful Links
=============

- Documentation: https://www.quantum-espresso.org/documentation/package-specific-documentation
- Quantum ESPRESSO input generator: https://qeinputgenerator.materialscloud.io
- Standard solid-state pseudopotentials: https://legacy.materialscloud.org/discover/sssp/table/efficiency
