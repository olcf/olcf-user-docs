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
calculations: the Quickstep method for mixed Gaussian and plane-wave (GPW) and Gaussian and augmented plane-wave
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
| ROCm                        | 7.0.2   | AMD GPU runtime                                              |
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
is provided below. Let us use a system of 32 water molecules as an example.

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
input file for 32 water molecules might look like this:

.. code-block:: bash

    &GLOBAL
        PROJECT H2O-32
        RUN_TYPE ENERGY
    &END GLOBAL

    &FORCE_EVAL
        METHOD QS                                               ! Quickstep method for mixed Gaussian and plane-wave calculations
        &DFT
            BASIS_SET_FILE_NAME GTH_BASIS_SETS                  ! The name of the file containing the basis sets
            POTENTIAL_FILE_NAME POTENTIAL                       ! The name of the file containing the pseudopotentials
            &MGRID
                CUTOFF 280                                      ! Plane-wave cutoff energy in Ry
            &END MGRID
            &SCF
                SCF_GUESS ATOMIC                                ! Initial guess for the SCF procedure
            &END SCF
            &XC
                &XC_FUNCTIONAL PBE                              ! Exchange-correlation functional
                &END XC_FUNCTIONAL
            &END XC
        &END DFT
        &SUBSYS
            &CELL
                ABC 9.8528 9.8528 9.8528                        ! Cell dimensions in Angstroms
            &END CELL
            # 32 H2O (TIP5P,1bar,300K) a = 9.8528
            &COORD                                              ! Atomic coordinates
                O       2.280398       9.146539       5.088696
                O       1.251703       2.406261       7.769908
                O       1.596302       6.920128       0.656695
                O       2.957518       3.771868       1.877387
                O       0.228972       5.884026       6.532308
                O       9.023431       6.119654       0.092451
                O       7.256289       8.493641       5.772041
                O       5.090422       9.467016       0.743177
                O       6.330888       7.363471       3.747750
                O       7.763819       8.349367       9.279457
                O       8.280798       3.837153       5.799282
                O       8.878250       2.025797       1.664102
                O       9.160372       0.285100       6.871004
                O       4.962043       4.134437       0.173376
                O       2.802896       8.690383       2.435952
                O       9.123223       3.549232       8.876721
                O       1.453702       1.402538       2.358278
                O       6.536550       1.146790       7.609732
                O       2.766709       0.881503       9.544263
                O       0.856426       2.075964       5.010625
                O       6.386036       1.918950       0.242690
                O       2.733023       4.452756       5.850203
                O       4.600039       9.254314       6.575944
                O       3.665373       6.210561       3.158420
                O       3.371648       6.925594       7.476036
                O       5.287920       3.270653       6.155080
                O       5.225237       6.959594       9.582991
                O       0.846293       5.595877       3.820630
                O       9.785620       8.164617       3.657879
                O       8.509982       4.430362       2.679946
                O       1.337625       8.580920       8.272484
                O       8.054437       9.221335       1.991376
                H       1.762019       9.820429       5.528454
                H       3.095987       9.107088       5.588186
                H       0.554129       2.982634       8.082024
                H       1.771257       2.954779       7.182181
                H       2.112148       6.126321       0.798136
                H       1.776389       7.463264       1.424030
                H       3.754249       3.824017       1.349436
                H       3.010580       4.524142       2.466878
                H       0.939475       5.243834       6.571945
                H       0.515723       6.520548       5.877445
                H       9.852960       6.490366       0.393593
                H       8.556008       6.860063      -0.294256
                H       7.886607       7.941321       6.234506
                H       7.793855       9.141028       5.315813
                H       4.467366       9.971162       0.219851
                H       5.758685      10.102795       0.998994
                H       6.652693       7.917443       3.036562
                H       6.711966       7.743594       4.539279
                H       7.751955       8.745180      10.150905
                H       7.829208       9.092212       8.679343
                H       8.312540       3.218330       6.528858
                H       8.508855       4.680699       6.189990
                H       9.742249       1.704975       1.922581
                H       8.799060       2.876412       2.095861
                H       9.505360       1.161677       6.701213
                H       9.920117      -0.219794       7.161006
                H       4.749903       4.186003      -0.758595
                H       5.248010       5.018415       0.403676
                H       3.576065       9.078451       2.026264
                H       2.720238       9.146974       3.273164
                H       9.085561       4.493058       9.031660
                H       9.215391       3.166305       9.749133
                H       1.999705       2.060411       1.927796
                H       1.824184       0.564565       2.081195
                H       7.430334       0.849764       7.438978
                H       6.576029       1.537017       8.482885
                H       2.415851       1.576460       8.987338
                H       2.276957       0.099537       9.289499
                H       1.160987       1.818023       4.140602
                H       0.350256       2.874437       4.860741
                H       5.768804       2.638450       0.375264
                H       7.221823       2.257514       0.563730
                H       3.260797       5.243390       5.962382
                H       3.347848       3.732214       5.988196
                H       5.328688       9.073059       5.982269
                H       5.007063       9.672150       7.334875
                H       4.566850       6.413356       3.408312
                H       3.273115       7.061666       2.963521
                H       3.878372       7.435003       6.843607
                H       3.884673       6.966316       8.283117
                H       5.918240       3.116802       5.451335
                H       5.355924       2.495093       6.711958
                H       5.071858       7.687254      10.185667
                H       6.106394       7.112302       9.241707
                H       1.637363       5.184910       4.169264
                H       0.427645       4.908936       3.301903
                H       9.971698       7.227076       3.709104
                H      10.647901       8.579244       3.629806
                H       8.046808       5.126383       2.213838
                H       7.995317       4.290074       3.474723
                H       1.872601       7.864672       7.930401
                H       0.837635       8.186808       8.987268
                H       8.314696      10.115534       2.212519
                H       8.687134       8.667252       2.448452
            &END COORD
            &KIND H
                BASIS_SET TZV2P-GTH                             ! Basis set for hydrogen
                POTENTIAL GTH-PBE-q1                            ! Pseudopotential for hydrogen
            &END KIND
            &KIND O
                BASIS_SET TZV2P-GTH                             ! Basis set for oxygen  
                POTENTIAL GTH-PBE-q6                            ! Pseudopotential for oxygen
            &END KIND
        &END SUBSYS
    &END FORCE_EVAL

Note that the ``!`` symbol followed by text indicates a comment.

2. Prepare the basis sets and pseudopotentials.
************************************************

A Quickstep calculation requires the ``BASIS_MOLOPT`` and ``GTH_POTENTIALS`` data files
referenced by ``BASIS_SET_FILE_NAME`` and ``POTENTIAL_FILE_NAME``. These files are provided
as part of the module and the environment variable ``CP2K_DATA_DIR`` points to their location.
So, the user does not need to download the standard basis sets or pseudopotentials. The user
can simply use the available ones by specifying in the input file:

.. code-block:: bash

    BASIS_SET_FILE_NAME GTH_BASIS_SETS
    POTENTIAL_FILE_NAME POTENTIAL

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
