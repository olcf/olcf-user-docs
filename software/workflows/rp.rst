.. _workflows-rp:

***********************
Radical Pilot (RP)
***********************


Overview
========

Scientific productivity can be enhanced through workflow management tools, relieving large High Performance
Computing (HPC) system users from the tedious tasks of scheduling and designing the complex
computational execution of scientific applications. This user documentation page presents several examples on 
the usage of ensemble workflow tools to accelerate science using the Frontier supercomputing system. 
This page presents the coupling, porting and installation of Radical-Cybertools on two applications: Chroma 
and NAMD. The content of this page is adapated from a technical report where additional information and detail
can be found: https://www.osti.gov/biblio/2575304

Introduction
=============

This guide provides summary guidance efor OLCF users implementing the RADICAL-Pilot (RP) workflow tool on Frontier.
The source `techincal report <https://www.osti.gov/biblio/2575304>`__ offers additional comprehensive technical and scientific 
guidelines for adopting and configuring RP on the Frontier supercomputer, complementing RP's platform-specific documentation.
The report includes essential information on data management strategies and OLCF ensemble policies, while highlighting
solutions and multi-track capabilities for installation and usability.

RP is an ensemble tool that leverages Python-based scripts for efficient job launching, scheduling, error
management, and resource allocation. Its application-agnostic design provides customizable workflows
for domain-specific requirements. RP's multi-level metadata management system organizes execution data
in structured directories. 

RP demonstrates exceptional error reporting capabilities, enabling rapid job relaunch and preventing execution
hangs during ensemble operations. Its efficient restart options maintain minimal overhead across
our flagship applications detailed in this document. Previous publications on OLCF systems confirm RP's
established portability as a versatile ensemble tool Titov et al. 2024; Titov et al. 2022; Merzky et al. 2021;
Merzky, Turilli, and Jha 2022; Turilli et al. 2021.

Installation of the RADICAL-Pilot Tool
======================================

Frontier supports Python virtual environment usage:

.. code-block:: console

    $ export PYTHONNOUSERSITE=True
    $ module load cray-python
    $ python3 -m venv ve.rp
    $ source ve.rp/bin/activate

Subsequently, install RP in the newly created and activated virtual environment:

.. code-block:: console

    $ pip install radical.pilot

The latest versions of RCT tools are within development branches, and include the latest fixes, updates and
new features. These versions are considered unstable and they are optional for users, but could be installed if desired:

.. code-block:: console

    $ pip install git+https://github.com/radical-cybertools/radical.utils.git@devel
    $ pip install git+https://github.com/radical-cybertools/radical.gtod.git@devel
    $ pip install git+https://github.com/radical-cybertools/radical.pilot.git@devel

Run the command ``radical-stack`` to verify the success of the installation. This should print the corresponding Python
and RP versions that have been installed.

Running Overview
^^^^^^^^^^^^^^^^

A RP application (i.e., Python application using RP as a pilot-based runtime system) can be launched as
a regular Python script: ``python rp_app.py``. To keep it running in the background the following command is recommended.
``nohup python rp_app.py > OUTPUT 2>&1 </dev/null &``

This Frontier-compatible example pilot description describes the requested resources (e.g., nodes, runtime, allocation):

.. code-block:: python3

    import radical.pilot as rp
    pd = rp.PilotDescription( {
	    'resource' : 'ornl.frontier',
	    'project' : 'XYZ000',
	    'nodes' : 1,
	    # OR 'cores' (CPU slots) and 'gpus' (GPU slots) could be provided-
	    # it is an old approach , and it still will be converted into nodes
	    # 'cores' : 64,
	    # 'gpus' : 8 ,
	    'runtime' : 15, # in minutes)
	    'queue' : 'debug'
    } )

Applications
============

The following examples follow the work presented and published at the International Conference for High
Performance Computing, Networking, Storage, and Analysis (SC24) with title “Ensemble Simulations on
Leadership Computing Systems”, Georgiadou A. et al. DOI 10.1109/SCW63240.2024.00059 Georgiadou
et al. 2024

CHROMA
------

The repository for this example can be reached here: https://github.com/olcf/workflow-examples

.. code-block:: console

    $ git clone https://github.com/olcf/workflow-examples.git
    $ cd chroma_rp
    $ ./compile_chroma/build_stack.sh

The user will be required to edit the ``setup_tasks_example.py`` and ``chroma_rp.py`` to your desired workflow
as necessary.

Then run:

.. code-block:: console

    $ python chroma_rp.py

The necessary edits in ``chroma_rp.py`` from the repository are annotated below:

.. code-block:: python3

    #!/usr/bin/env python3

    __author__    = 'Henry Monge-Camacho'
    __email__     = 'mongecamachj@ornl.gov'

    import os
    import radical.pilot as rp
    import radical.utils as ru
    from setup_tasks_example import *
    import sys

    import queue

    os.environ['RADICAL_PROFILE'] = 'TRUE'
    os.environ['RADICAL_LOG_LVL'] = 'DEBUG'

    tasks_finished_queue= queue.Queue()

    def task_state_cb(task, state):
        if state not in rp.FINAL:
            # ignore all non-finished state return
            tasks_finished_queue.put([
                task.uid, # register call back that will track for repo rt=ru.Reporter(name='radical.pilot')
                transitions,
                task.state
            ])
            # task states

    report = ru.Reporter(name='radical.pilot')
    report.title('Getting Started (RP version %s)' % rp.version)

    N_NODES = 2

    PILOT_DESCRIPTION = {
        'resource' : 'ornl.frontier',
        'project'  : 'project', #TODO: include your project ID here
        'nodes'    : N_NODES,
        'cores'    : 48*N_NODES,
        'gpus'     : 8*N_NODES,
        'runtime'  : 20,
    }


    # Define paths
    os.environ['RADICAL_SMT'] = '1'
    session = rp.Session()

    #Create the tasks to run

    LattExtentInSpace=4
    LattExtentInTime=8
    Configurations=5
    tasks, priorities=make_ensemble_tasks(
        LattExtentInSpace,
        LattExtentInTime,
        Configurations,
        session.uid,
        '/path/to/test' # TODO: include output file location here
    )

    def main():
        try:
            pmgr = rp.PilotManager(session=session)

            pilot = pmgr.submit_pilots(rp.PilotDescription(PILOT_DESCRIPTION))
            client_sandbox = ru.Url(pilot.client_sandbox).path + '/' + session.uid
            pilot_sandbox  = ru.Url(pilot.pilot_sandbox).path

            print('client sandbox: %s' % client_sandbox)
            print('pilot  sandbox: %s' % pilot_sandbox)

            tmgr = rp.TaskManager(session=session)
            pilot.wait(rp.PMGR_ACTIVE)
            tmgr.add_pilots(pilot)

            #No dependencies? Turn on next 4 lines
            tmgr.submit_tasks(tasks)
            #tmgr.wait_tasks()
            #for task in sub_tasks:
            #   print('%s: %s' % (task.uid, task.state))

            #Dependencies Turn on next line
            # Enable call for dependency runs
            tmgr.register_callback(task_state_cb)
            launch_tasks(tmgr, tasks)

            report.progress_done()
            report.header('finalize')

        finally:
            print(datetime.now().strftime("%H:%M:%S"))
            session.close(download=True)


    if __name__ == '__main__':
        main()


NAMD
----

This example calculates the free energy of charging an ion for illustrating the use of NAMD
within Radical Pilot. The example finds the electrostatic contribution to the free energy of charging a Na+ ion in 
water. It will use the SPC/E water model and the Na+ parameters from Hummer et al.Hummer, Pratt, and García
1996. The accompanying archive collects all the work necessary for running the ensemble calculation.

Simulation task
^^^^^^^^^^^^^^^

For the free energy of charging, and solely to demonstrate running multiple simultaneous jobs, we use a
7-point Gauss-Legendre quadrature. The ion charges are scaled to specify the appropriate sampling points
(7 in total) Hummer and Szabo 1996, and the jobs are collected in appropriately labeled directories Tomar
et al. 2016.

Setting up the job

Run ``bash SetUpCharging.sh`` to set up the different cases of the ensemble.

Running RADICAL-Pilot
^^^^^^^^^^^^^^^^^^^^^

The Python script ``rp_simulation_SMT1.py`` has the details to launch the RADICAL-Pilot (RP) runs. Notice
RP is running with with modifications to the default behavior, namely using one thread per core. (In
general, running NAMD with only thread per core proves more efficient.) 

To use only one thread per core
on Frontier, create in your `$(HOME)/.radical/pilot/configs` directory the following `resource_ornl.json`
file. Number of enabled threads per core is controlled by parameter `smt` (Simultaneous Multithreading).
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
^^^^^^^^

The analysis uses a non-GPU version of the NAMD code, but the ensemble calculation follows the same
logic: ``python rp_analysis_SMT1.py``.

Collecting the results
^^^^^^^^^^^^^^^^^^^^^^

The ``bash ProcessPair.sh`` scripts should process all the pair ``.log`` files and print out the estimated free energy of
charging.

Expected result
^^^^^^^^^^^^^^^

If all the runs were successful, you should find that a hydration free energy value of about-95 kcal/mol.
The above procedure can be easily modified to launch other calculations that could benefit from ensemble
computing.
