***
VMD
***

Overview
========

`VMD <https://www.ks.uiuc.edu/Research/vmd/>`__ is a powerful tool for examining, rendering, and interpreting the structural and dynamic properties of biological molecules, 
including proteins, nucleic acids, and membrane systems. VMD supports visualization of molecular structures from standard 
Protein Data Bank (PDB) file formats, making it accessible for a broad range of molecular systems. To represent atomic and molecular 
features, VMD offers numerous visualization techniques — from basic geometric primitives to more sophisticated representations like 
space-filling models, bond depictions, secondary structure cartoons, and ribbon diagrams. 

A key strength of VMD is its ability to process and visualize time-resolved molecular dynamics simulations, allowing researchers to track molecular behavior over 
computational time steps. Notably, VMD can function as a visual interface to external simulation engines, such as GROMACS, enabling real-time 
display and playback of molecular behavior as simulations run on remote computational resources.

Setting Up VMD
==============

VMD is installed on Andes as a loadable module. You do not need to install VMD locally; however, it is possible to download VMD
for free at: `VMD Download <https://www.ks.uiuc.edu/Development/Download/download.cgi?PackageName=VMD>`__. 
The list of currently available VMD versions on Andes are as follows:

* ``vmd/1.9.3``

GUI Usage
=========

You should not run VMD on an Andes login node. Instead, it is recommended you obtain an interactive job and use X11 forwarding to visualize the VMD rendering locally.
The recommended workflow is as follows:

1. Obtain a GPU compute node: ``salloc -N 1 -t 15 -A [account] -p gpu``.
2. Once a GPU node is obtained, open a 2nd terminal and jump to the allocated compute node with X11 forwarding enabled: 

    .. code-block:: none

        ssh -X -J user@andes.olcf.ornl.gov user@andes-gpu#.olcf.ornl.gov

3. Load the `vmd` module: ``module load vmd``.
4. From the command line, run the ``vmd`` command with a structure optionally provided: ``vmd protein.pdb``

    * To load a trajectory, you can run a similar command but provide your trajectory file as the second input: 
    
    .. code::

        vmd solvated_protein.gro solvated_protein.xtc

5. A VMD graphical window should open on your local workstation where you are free to manipulate and render your image or trajectories.

.. note::

    When running from the compute node, VMD should inform you that 4 K80 accelerators are being initialized. If you see a warning that no accelerators are detected,
    you may have submitted to the batch partition or are running on a login node.

Interactive Molecular Dynamics
==============================

.. tip::

    Don't have your own readily available GROMACS files? Check out our example here: https://github.com/olcf/andes_imd_gromacs.git

VMD enables the option to perform in-situ visualizations of a running GROMACS/NAMD simulation. This can be done to visualize real-time updates from your
simulation or to interactively manipulate the molecules at runtime. The following outlines how to perform interactive molecular dynamics
on Andes using GROMACS.

1. Prerequisite:

    * The input (\*.mdp) file must have the ``IMD-group`` parameter defined. ``IMD-group = System`` can be used to define the whole system. Otherwise, a specific group can be listed to avoid, for example, water molecules from being manipulated.
    * Add the ``-imdwait -imdpull -imdterm -imdport 0`` flags when launching your production job. For example, 

    .. code-block:: none

        gmx mdrun -deffnm nvt -imdwait -imdpull -imdterm -imdport 0

2. Launch an interactive job on Andes ``salloc -N 1 -t 15 -A <project_id> -p gpu``
3. Open a 2nd terminal window and jump to the allocated compute node with X11 forwarding enabled: 

.. code-block:: none
    
    ssh -X -J user@andes.olcf.ornl.gov user@andes-gpu#.olcf.ornl.gov

4. In the first terminal, run your GROMACS simulation and wait until you're prompted that IMD is waiting for a connection.
5. In the second terminal (the jump), load the vmd module and an appropriate molecule file ``module load vmd; vmd solvated_box.gro`` (**NOTE**: you must load a coordinate file before attempting IMD)
6. In the VMD window, navigate to ``Extensions`` -> ``Simulation`` -> ``IMD Connect (NAMD)``.
7. In the ``IMD Connection`` window:

    * Hostname is the compute node your job is running on (e.g., ``andes-gpu1.olcf.ornl.gov`` if that's what was allocated).
    * Port can found in terminal 1 with your running GROMACS simulation. E.g., "IMD: Listening for IMD connection on port 41125" -> you'd put 41125.



Additional Resources
====================

* `<https://www.ks.uiuc.edu/Research/vmd/>`__ - VMD Homepage
* `<https://www.rcsb.org>`__ - RCSB Protein Data Bank