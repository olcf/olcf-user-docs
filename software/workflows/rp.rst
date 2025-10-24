.. _workflows-rp:

***********************
Radical Pilot (RP)
***********************


Overview
========

Scientific productivity can be enhanced through workflow management tools, relieving large High Performance
Computing (HPC) system users from the tedious tasks of scheduling and designing the complex
computational execution of scientific applications. This report presents a study on the usage of ensemble
workflow tools to accelerate science using the Frontier supercomputing systems. This technical report
aims to connect science domain simulations using Oak Ridge Leadership Computing Facility (OLCF) supercomputing
platforms with ensemble workflow methods in order to accelerate HPC-enabled discovery
and boost scientific impact. We present the coupling, porting and installation of Radical-Cybertools on
two applications: Chroma and NAMD. https://www.osti.gov/biblio/2575304

Introduction
=============

This technical guide provides guidance for OLCF users implementing RP workflow tool on Frontier. As
the guidelines and software matures and evolves, our team will deliver biannual updates to the policies and
best practices. The document offers comprehensive technical and scientific guidelines for adopting and
configuring RP on the Frontier supercomputer, complementing RP's platform-specific documentation. We
include essential information on data management strategies and OLCF ensemble policies, while highlighting
our solutions and multi-track capabilities for installation and usability.

RP is an ensemble tool that leverages Python-based scripts for efficient job launching, scheduling, error
management, and resource allocation. Its application-agnostic design provides customizable workflows
for domain-specific requirements. RP's multi-level metadata management system organizes execution data
in structured directories. While workflow tools often struggle to adapt to specific production systems and
facility policies this technical paper addresses platform heterogeneity by documenting our experience integrating,
porting, and running RP on Frontier.

RP demonstrates exceptional error reporting capabilities, enabling rapid job relaunch and preventing execution
hangs during ensemble operations. Its efficient restart options maintain minimal overhead across
our flagship applications detailed in this document. Previous publications on OLCF systems confirm RP's
established portability as a versatile ensemble tool Titov et al. 2024; Titov et al. 2022; Merzky et al. 2021;
Merzky, Turilli, and Jha 2022; Turilli et al. 2021.

INSTALLATION OF THE RADICAL-PILOT TOOL
======================================

Workflow management is a strategic approach that assists organizing and optimizing model runs on large
heterogeneous High Performance Computing (HPC) systems. At OLCF we cater to these workflow needs
and feature demands by providing complex workflow tools with state-of-the-art management capabilities.
RADICAL-Pilot has showcased the ability to simplify the computational runs on Frontier and is widely
used across platforms and scientific groups. The source materials from the developers reside here:
https://radicalpilot.readthedocs.io/en/stable/supported/frontier.html

A user's guide is provided to encapsulate directions and practices on installing the RADICAL-Cybertools
stack (RCT) on Frontier with the pip install command. OLCF supports Python virtual environment usageincluded
with instructions for the execution environment- by creating a virtual environment with venv:

.. code-block:: console

    $ export PYTHONNOUSERSITE=True
    $ module load cray−python/3.11.7
    $ python3 −m venv ve.rp
    $ source ve.rp/bin/activate

Subsequently, install RP in the activated corresponding virtual environment:

.. code-block:: console

    $ pip install radical.pilot

An alternate way to install RP manually is the following user-based installation method for Frontier:

.. code-block:: console

    $ module load cray−python/3.11.7
    $ python −m venv ve.rp
    $ source ve.rp/bin/activate
    $ pip install −U pip

Use the pip install –user pip command if any errors appear. Passing the –user option to python
-m pip install will install a package just for the current user, rather than for all users of the system.

The latest versions of RCT tools are within development branches, and include the latest fixes, updates and
new features. These versions are considered unstable and they are optional for users.

.. code-block:: console

    $ pip install git+https://github.com/radical-cybertools/radical.utils.git@devel
    $ pip install git+https://github.com/radical-cybertools/radical.gtod.git@devel
    $ pip install git+https://github.com/radical-cybertools/radical.pilot.git@devel

Run the command ``radical-stack`` to verify the success of the installation.
RP application (i.e., Python application using RP as a pilot-based runtime system) can be launched as
a regular Python script: ``python rp_app.py`` (or ``./rp_app.py`` if it includes a corresponding shebang,
e.g., #!/usr/bin/env python). To keep it running in the background the following command is recommended.
``nohup python rp_app.py > OUTPUT 2>&1 </dev/null &``

Example of a pilot description in the RP application is presented below. That information is used to make a
job submission, thus it includes the amount of requested resources (i.e., node x hours) and the type of a
batch system for a submission (this is pulled from the predefined configuration).

.. code-block:: python3

    import radical.pilot as rp
    pd = rp.PilotDescription( {
	    'resource' : 'ornl.frontier',
	    'project' : 'XYZ000',
	    'nodes' : 1,
	    # OR 'cores' (CPU slots) and 'gpus' (GPU slots) could be provided−
	    # it is an old approach , and it still will be converted into nodes
	    # 'cores' : 64,
	    # 'gpus' : 8 ,
	    'runtime' : 15, # in minutes)
	    'queue' : 'debug'
    } )

APPLICATIONS
============

An assortment of scientific applications is included in the following section with the RP tool coupling and
Frontier establishment guidelines along with run-time examples. We showcase applications with and with-
out dependencies on their execution path to cover the various instances of application coupling with di-
verse needs. The dependencies' example is covered under the building guidelines for the Chroma Lattice-
QCD code. The repository for this example can be reached here: https://github.com/henrymonge/chroma_rp.

Each application example that follows entails a guide for the modules required and the tasks' setup. The
RP setup reads through all the application specific details and the OLCF user will be required to edit the
setup_tasks_example.py script to create the individual tasks.

This technical recipe follows the work presented and published at the International Conference for High
Performance Computing, Networking, Storage, and Analysis (SC24) with title “Ensemble Simulations on
Leadership Computing Systems”, Georgiadou A. et al. DOI 10.1109/SCW63240.2024.00059 Georgiadou
et al. 2024

CHROMA

.. code-block:: python3

    #!/usr/bin/env python3

    __author__= 'Henry Monge−Camacho'
    __email__ = 'mongecamachj@ornl.gov'

    import os
    import  radical.pilot as rp
    import radical.utils as ru

    from setup_tasks_example import sys

    import queue
    # import *
    os.environ[ 'RADICAL_PROFILE' ]= 'TRUE'
    os.environ[ 'RADICAL_LOG_LVL' ]= 'DEBUG'
    tasks_finished_queue= queue.Queue()

    def task_state_cb(task, state):
        if state not in rp.FINAL:
            # ignore all non−finished state return
            tasks_finished_queue.put([
                task.uid, # register call back that will track for repo rt=ru.Reporter(name='radical.pilot')
                transitions,
                task.state
            ])
            # task states

    report.title('Getting Started(RP version %s )' % rp.version)
    N_NODES= 2

    PILOT_DESCRIPTION= {
        'resource': 'ornl.frontier',
        'project': 'project',
        'nodes': N_NODES,
        'cores': 48*N_NODES,
        'gpus' : 8*N_NODES,
        'runtime' : 20,
    }

    # Define paths
    os.environ['RADICAL_SMT']= '1'
    session= rp.Session()

    # Create the tasks to run
    LattExtentInSpace=4
    LattExtentInTime=8
    Configurations=5
    tasks, priorities=make_ensemble_tasks(
        LattExtentInSpace,
        LattExtentInTime,
        Configurations,
        Session.uid,
        '/path/to/test'
    )

    def main():
        if True:
            try:
                pmgr= rp.PilotManager(session= session)

                pilot= pmgr.submit_pilots(rp.PilotDescription(PILOT_DESCRIPTION))
                client_sandbox= ru.Url(pilot.client_sandbox).path+'/'+session.uid
                pilot_sandbox= ru.Url(pilot.pilot_sandbox).path
                print('clientprint('pilot sandbox: s'%client_sandbox) sandbox: %s'%pilot_sandbox)

                tmgr= rp.TaskManager(session=session)
                pilot.wait(rp.PMGR_ACTIVE)
                tmgr.add_pilots(pilot)

                #No dependencies? Turn #sub_tasks= on next 4 lines
                tmgr.submit_tasks(tasks)

                # tmgr.wait_tasks()
                # for task in sub_tasks:
                # print('% s : %s ' % (task.uid, task.state))


                # Dependencies Turn on next two lines
                # Enable call for dependency runs
                tmgr.register_callback(task_state_cb)
                launch_tasks(tmgr, tasks)
                report.progress_done()
                report.header('finalize')
            finally:
                print(datetime.now().strftime('%H:%M:%S'))
                session.close(download=True)

    if __name__== '__main__':
        main()

NAMD

We use the example of calculating the free energy of charging an ion for illustrating the use of NAMD
within Radical Pilot. We find the electrostatic contribution to the free energy of charging a Na+ ion in wa-
ter. We use the SPC/E water model and the Na+ parameters from Hummer et al.Hummer, Pratt, and García
1996. The accompanying archive collects all the work necessary for running the ensemble calculation.

Simulation task

For the free energy of charging, and solely to demonstrate running multiple simultaneous jobs, we use a
7-point Gauss-Legendre quadrature. The ion charges are scaled to specify the appropriate sampling points
(7 in total) Hummer and Szabo 1996, and the jobs are collected in appropriately labeled directories Tomar
et al. 2016.

Setting up the job

Run ``bash SetUpCharging.sh`` to set up the different cases of the ensemble.

Running RADICAL-Pilot

The Python script rp_simulation_SMT1.py has the details to launch the RADICAL-Pilot (RP) runs. Notice
that we are running RP with modifications to the default behavior, namely using one thread per core. (In
general, running NAMD with only thread per core proves more efficient.) To use only one thread per core
on Frontier, create in your $(HOME)/.radical/pilot/configsthe following "resource_ornl.json"
file. Number of enabled threads per core is controlled by parameter smt(Simultaneous Multithreading).
Also, RP follows the default setting of Frontier SLURM core specialization, which reserves one core from
each L3 cache region, leaving 56 allocatable cores out of the available 64.

.. code-block:: python3

    {
        'frontier':{
            ''system_architecture''
        }
        :{
            'smt': 1,
            'blocked_cores':[ 0, 8, 16, 24, 32, 40, 48, 56]
        }
    }

The ensemble calculation can then be launched as ``python rp_simulation_SMT1.py``.

Analysis

The analysis uses a non-GPU version of the NAMD code, but the ensemble calculation follows the same
logic. Simply do ``python rp_analysis_SMT1.py``.

Collecting the results

The ``bash ProcessPair.sh`` should process all the pair . log files and print out the estimated free energy of
charging. As a further check of the results, in the directory Reference we have provided the estimates from
simulations that exclusively used the CPU (on a MacBook pro laptop). Running the ProcessPair .sh script
inside that Reference directory should print out the results obtained on the Mac.

Expected result

If all the runs were successful, you should find that a hydration free energy value of about−95 kcal/mol.
The above procedure can be easily modified to launch other calculations that could benefit from ensemble
computing.
