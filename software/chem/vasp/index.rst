.. _vasp:

****
VASP
****

.. contents:: On this page
   :local:
   :depth: 2

Overview
========

VASP (Vienna Ab initio Simulation Package) is a plane-wave electronic structure code. Among
its capabilities are density functional theory (DFT) calculations and ab initio molecular
dynamics simulations.

.. note::

    VASP is licensed software. OLCF cannot provide access to VASP unless you or your
    organization hold a valid license. To gain access to the centrally installed module,
    contact User Assistance through the support portal with proof of your license (for
    example, a copy of your VASP license agreement or confirmation from the VASP team), and
    you will be added to the ``vasp`` Unix group that controls access to the software and its
    documentation.

----

Package Details
================

+-----------------------------+---------+-------------------------------------------------------------------+
| Application or Library      | Version | Short Description                                                 |
+=============================+=========+===================================================================+
| VASP                        | 6.6.1   | Electronic structure calculations and ab initio molecular dynamics|
+-----------------------------+---------+-------------------------------------------------------------------+
| ROCm                        | 6.4.2   | AMD GPU runtime.                                                  |
+-----------------------------+---------+-------------------------------------------------------------------+
| Cray MPICH                  | 9.0.1   | MPI implementation for parallel execution                         |
+-----------------------------+---------+-------------------------------------------------------------------+

----

Usage
=====

To use VASP, load the required modules:

.. code-block:: bash

    module load vasp/6.6.0-gpu

If the module is not visible with ``module avail vasp``, you have not yet been added to the
``vasp`` Unix group. See the note above for how to request access.

Beginner's Guide
================

For new users of VASP, an illustration of the workflow for a plane-wave DFT calculation is
provided below. Let us use the silicon crystal primitive cell as an example.

0. Prepare a working directory.
********************************
Before running a calculation, we need a working directory with the necessary input files and
pseudopotentials. Your project directory is a good place to start. For example, if your
project directory is ``/lustre/orion/<project id>``, you might create a working directory
named ``vasp-silicon-example`` in the scratch space like:

.. code-block:: bash

    mkdir -p /lustre/orion/<project id>/scratch/vasp-silicon-example
    cd /lustre/orion/<project id>/scratch/vasp-silicon-example

1. Prepare the input files.
****************************
A VASP calculation requires four input files: ``INCAR``, ``POSCAR``, ``POTCAR``, and
``KPOINTS``.

``INCAR`` (calculation parameters and settings):

.. code-block:: bash

    SYSTEM = Silicon primitive cell     ! a name for the calculation
    ISTART = 0                          ! start from scratch, no previous wavefunction
    ICHARG = 2                          ! construct initial charge density from atomic charges
    ENCUT  = 300                        ! plane-wave cutoff energy in eV
    EDIFF  = 1E-6                       ! convergence threshold for self-consistency (eV)
    ISMEAR = 0                          ! Gaussian smearing of partial occupancies
    SIGMA  = 0.05                       ! smearing width in eV

``POSCAR`` (lattice geometry and atomic positions):

.. code-block:: bash

    Silicon primitive cell
    5.43
    0.0 0.5 0.5
    0.5 0.0 0.5
    0.5 0.5 0.0
    Si
    2
    Direct
    0.00 0.00 0.00
    0.25 0.25 0.25

``KPOINTS`` (Brillouin zone sampling):

.. code-block:: bash

    Automatic mesh
    0
    Gamma
    4 4 4
    0 0 0

``POTCAR`` (pseudopotentials): see the next step.

2. Prepare the pseudopotentials.
*********************************

A VASP calculation requires a ``POTCAR`` file, which is a concatenation of pseudopotential
files for each atomic species in the order they appear in ``POSCAR``. Pseudopotentials distributed
with VASP are located in ``$VASP_POTENTIALS_DIR/<functional>/<element>`` where ``<functional>``
can be ``LDA`` or ``PBE``. Each directory contains element directories containing the corresponding 
``POTCAR`` file. For the silicon example,
concatenate the silicon pseudopotential into a file named ``POTCAR`` in the working directory:

.. code-block:: bash

    cat $VASP_POTENTIALS_DIR/PBE/Si/POTCAR > POTCAR

If your system has multiple species, concatenate their ``POTCAR`` files in the same order the
species appear in ``POSCAR``.

3. Prepare the job submission script.
**************************************
To submit the calculation to the queue, we need a job submission script, like:

.. code-block:: bash

    #!/bin/bash
    #SBATCH -A <project id>
    #SBATCH -J Si2-scf
    #SBATCH -N 1
    #SBATCH -p batch
    #SBATCH -o %x-%j.out
    #SBATCH -t 10:00

    module load vasp/6.6.0-gpu

    srun -N 1 -n 1 -c 1 --gpus-per-task=1 --gpu-bind=closest vasp_std > output.log

Here, we request 1 node, with 1 MPI rank, 1 CPU core, and 1 GPU for 10 minutes. This example
calculation only takes about one minute, so the requested time is sufficient. Adjust the
resource requests and walltime as needed for larger systems.

4. Submit the job to the queue with ``sbatch``.
*************************************************
Now we are ready to submit the job. Use the ``sbatch`` command to submit the job script to the
queue:

.. code-block:: bash

    sbatch <submit script>

Once in the queue, you can check the job status with ``squeue -u <username>``. Once the job
starts running, VASP writes its results to several output files, including ``OUTCAR`` (a
detailed log of the calculation) and ``vasprun.xml`` (a structured summary suitable for
post-processing), in addition to the ``output.log`` file specified in the submit script.

Congratulations! You have successfully run a plane-wave DFT calculation with VASP on Frontier.
You can now analyze the output files and explore the results.

----

Helpful Links
=============

- VASP home: https://www.vasp.at
- VASP documentation wiki: https://www.vasp.at/wiki/index.php/The_VASP_Manual
- VASP forum (support and troubleshooting): https://www.vasp.at/forum/
