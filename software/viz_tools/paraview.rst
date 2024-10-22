********
ParaView
********


Overview
========

`ParaView <http://paraview.org>`__ is an open-source, multi-platform data
analysis and visualization application. ParaView users can quickly build
visualizations to analyze their data using qualitative and quantitative
techniques. The data exploration can be done interactively in 3D or
programmatically using ParaView’s batch processing capabilities. Further
information regarding ParaView can be found at the links provided in the
:ref:`paraview-resources` section.

ParaView was developed to analyze extremely large datasets using distributed
memory computing resources. The OLCF provides ParaView server installs on Andes,
Summit, and Frontier to facilitate large scale distributed visualizations.
The ParaView server may be used in a headless batch processing
mode or be used to drive a ParaView GUI client running on your local machine.

For a tutorial of how to get started with ParaView on OLCF systems, see our 
`ParaView on Frontier tutorial <https://github.com/olcf/dva-training-series/tree/main/paraview_2024>`__.
The tutorial walks through visualizing examples on Frontier, but applies to other OLCF systems as well.

An older tutorial using Andes can be found here: `ParaView at OLCF 2022 <https://github.com/olcf/dva-training-series/tree/main/paraview>`__

.. _paraview-install-setup:

Installing and Setting Up ParaView
==================================

Although in a single machine setup both the ParaView client and server run on
the same host, this need not be the case. It is possible to run a local
ParaView client to display and interact with your data while the ParaView
server runs in an Andes, Summit, or Frontier batch job, allowing interactive analysis of very large data sets.

You will obtain the best performance by running the ParaView client on your
local computer and running the server on OLCF resources with the same version
of ParaView. It is highly recommended to check the available ParaView versions
using ``module avail paraview`` on the system you plan to connect ParaView to.
Precompiled ParaView binaries for Windows, macOS, and Linux can be downloaded
from `Kitware <https://www.paraview.org/download/>`__.

Recommended ParaView versions on our systems:

* **Summit**: ParaView 5.9.1, 5.10.0, 5.11.0 (via the ``DefApps-2023`` module)
* **Andes**: ParaView 5.9.1, 5.10.0, 5.11.0, 5.12.1
* **Frontier**: ParaView 5.12.1 (via the UMS032 module)

.. warning::
    Using a different version than what is listed above is not guaranteed to work properly.

We offer two rendering modes of the ParaView API on our systems: OSMesa and
EGL.  OSMesa is intended for use on regular compute nodes, whereas EGL is
intended for use on GPU enabled nodes. When running interactively, you **do not**
need to download or install anything special to use the EGL or OSMesa versions,
as you'll be able to choose between those options when connecting to the system
(see :ref:`paraview-gui` below). If instead you're running in batch mode on the
command line (see :ref:`paraview-command-line` below), you can choose between
the rendering options by loading its corresponding module on the system you're
connected to. For example, to see these modules on specific OLCF systems:

.. tab-set::

   .. tab-item:: Andes
      :sync: andes

      .. code-block:: bash

         $ module -t avail paraview

         /sw/andes/modulefiles/core:
         paraview/5.9.1-egl
         paraview/5.9.1-osmesa
         paraview/5.10.0-egl
         paraview/5.10.0-osmesa
         paraview/5.11.0-egl
         paraview/5.11.0-osmesa
         paraview/5.12.1-egl
         paraview/5.12.1-osmesa

   .. tab-item:: Frontier
      :sync: frontier

      .. code-block:: bash

         $ module load ums
         $ module load ums032
         $ module load dav-sdk
         $ module -t avail paraview

         /sw/frontier/ums/ums032/modules:
         paraview/5.12.1-rocm
         paraview/5.12.1

   .. tab-item:: Summit
      :sync: summit

      .. code-block:: bash

         $ module load DefApps-2023 #only necessary on Summit
         $ module -t avail paraview

         /sw/summit/modulefiles/core:
         paraview/5.9.1-egl
         paraview/5.9.1-osmesa
         paraview/5.10.0-egl
         paraview/5.10.0-osmesa
         paraview/5.11.0-egl
         paraview/5.11.0-osmesa

      .. warning::
          On Summit, you **must** load ``DefApps-2023`` first.


.. note::
    The EGL mode seems to work better with larger datasets and is generally
    recommended over OSMesa on our systems. However, we encourage users to try both
    options and see which version works best for their data.

After installing, you must give ParaView the relevant server information to be
able to connect to OLCF systems (comparable to VisIt's system of host
profiles). The following provides an example of doing so. Although several
methods may be used, the one described should work in most cases.

.. warning::
    For macOS clients, it is necessary to install `XQuartz
    (X11) <https://www.xquartz.org/>`__ to get a command prompt
    in which you will securely enter your OLCF credentials.

    For Windows clients, it is necessary to install PuTTY to
    create an ssh connection in step 2.


**Step 1: Save the following servers.pvsc file to your local computer**

.. tab-set::

   .. tab-item:: Andes
      :sync: andes

      .. code-block::

            <Servers>
              <Server name="ORNL andes" resource="csrc://localhost">
                <CommandStartup>
                  <Options>
                    <Option name="HOST" label="Server host" save="true">
                      <String default="andes.olcf.ornl.gov"/>
                    </Option>
                    <Option name="HEADLESS_API" label="Server headless API" save="true">
                      <Enumeration default="osmesa">
                        <Entry value="osmesa" label= "OSMesa" />
                        <Entry value="egl" label= "EGL" />
                      </Enumeration>
                    </Option>
                    <Option name="USER" label="Server username" save="true">
                      <String default="YOURUSERNAME"/>
                    </Option>
                    <Switch name="PV_CLIENT_PLATFORM">
                      <Case value="Apple">
                        <Set name="TERM_PATH" value="/opt/X11/bin/xterm" />
                        <Set name="TERM_ARG1" value="-T" />
                        <Set name="TERM_ARG2" value="ParaView" />
                        <Set name="TERM_ARG3" value="-e" />
                        <Set name="SSH_PATH" value="ssh" />
                      </Case>
                      <Case value="Linux">
                        <Set name="TERM_PATH" value="xterm" />
                        <Set name="TERM_ARG1" value="-T" />
                        <Set name="TERM_ARG2" value="ParaView" />
                        <Set name="TERM_ARG3" value="-e" />
                        <Set name="SSH_PATH" value="ssh" />
                      </Case>
                      <Case value="Windows">
                        <Set name="TERM_PATH" value="cmd" />
                        <Set name="TERM_ARG1" value="/C" />
                        <Set name="TERM_ARG2" value="start" />
                        <Set name="TERM_ARG3" value="" />
                        <Set name="SSH_PATH" value="plink.exe" />
                      </Case>
                      <Case value="Unix">
                        <Set name="TERM_PATH" value="xterm" />
                        <Set name="TERM_ARG1" value="-T" />
                        <Set name="TERM_ARG2" value="ParaView" />
                        <Set name="TERM_ARG3" value="-e" />
                        <Set name="SSH_PATH" value="ssh" />
                      </Case>
                    </Switch>
                    <Option name="PV_SERVER_PORT" label="Server port ">
                      <Range type="int" min="1025" max="65535" step="1" default="random"/>
                    </Option>
                    <Option name="NUM_NODES" label="Number of compute nodes" save="true">
                      <Range type="int" min="1" max="512" step="1" default="2"/>
                    </Option>
                    <Option name="NUM_MPI_TASKS" label="Total number of MPI tasks" save="true">
                      <Range type="int" min="1" max="16384" step="1" default="2"/>
                    </Option>
                    <Option name="NUM_CORES_PER_MPI_TASK" label="Number of cores per MPI task" save="true">
                      <Range type="int" min="1" max="28" step="1" default="1"/>
                    </Option>
                    <Option name="PROJECT" label="Project to charge" save="true">
                      <String default="cscXXX"/>
                    </Option>
                    <Option name="MINUTES" label="Number of minutes to reserve" save="true">
                      <Range type="int" min="1" max="240" step="1" default="30"/>
                    </Option>
                  </Options>
                  <Command exec="$TERM_PATH$" delay="5">
                    <Arguments>
                      <Argument value="$TERM_ARG1$"/>
                      <Argument value="$TERM_ARG2$"/>
                      <Argument value="$TERM_ARG3$"/>
                      <Argument value="$SSH_PATH$"/>
                      <Argument value="-t"/>
                      <Argument value="-R"/>
                      <Argument value="$PV_SERVER_PORT$:localhost:$PV_SERVER_PORT$"/>
                      <Argument value="$USER$@$HOST$"/>
                      <Argument value="/sw/andes/paraview/pvsc/ORNL/login_node.sh"/>
                      <Argument value="$NUM_NODES$"/>
                      <Argument value="$MINUTES$"/>
                      <Argument value="$PV_SERVER_PORT$"/>
                      <Argument value="$PV_VERSION_FULL$"/>
                      <Argument value="$HEADLESS_API$"/>
                      <Argument value="/sw/andes/paraview/pvsc/ORNL/andes.cfg"/>
                      <Argument value="PROJECT=$PROJECT$"/>
                      <Argument value="NUM_MPI_TASKS=$NUM_MPI_TASKS$"/>
                      <Argument value="NUM_CORES_PER_MPI_TASK=$NUM_CORES_PER_MPI_TASK$"/>
                    </Arguments>
                  </Command>
                </CommandStartup>
              </Server>
            </Servers>

   .. tab-item:: Frontier
      :sync: frontier

      .. code-block::

            <Servers>
              <Server name="ORNL frontier (UMS)" resource="csrc://frontier.olcf.ornl.gov">
                <CommandStartup>
                  <Options>
                    <Option name="HEADLESS_API" label="Accelerated Compute" save="true">
                      <Enumeration default="rocm">
                        <Entry value="rocm" label= "ROCm" />
                        <Entry value="none" label= "None" />
                      </Enumeration>
                    </Option>
                    <Option name="USER" label="Server username" save="true">
                      <String default="YOURUSERNAME"/>
                    </Option>
                    <Option name="PV_SERVER_PORT" label="Server port ">
                      <Range type="int" min="1025" max="65535" step="1" default="random"/>
                    </Option>
                    <Option name="NUM_NODES" label="Number of compute nodes" save="true">
                      <Range type="int" min="1" max="512" step="1" default="2"/>
                    </Option>
                    <Option name="NUM_MPI_TASKS" label="Total number of MPI tasks" save="true">
                      <Range type="int" min="1" max="16384" step="1" default="2"/>
                    </Option>
                    <Option name="NUM_CORES_PER_MPI_TASK" label="Number of cores per MPI task" save="true">
                      <Range type="int" min="1" max="28" step="1" default="1"/>
                    </Option>
                    <Option name="PROJECT" label="Project to charge" save="true">
                      <String default="cscXXX"/>
                    </Option>
                    <Option name="PARTITION" label="Partition (queue)" save="true">
                      <String default="batch"/>
                    </Option>
                    <Option name="MINUTES" label="Number of minutes to reserve" save="true">
                      <Range type="int" min="1" max="240" step="1" default="30"/>
                    </Option>
                  </Options>
                  <SSHCommand exec="/sw/frontier/ums/ums032/pvsc/ORNL/login_node.sh" timeout="0" delay="5">
                    <SSHConfig user="$USER$">
                      <Terminal/>
                      <PortForwarding local="$PV_SERVER_PORT$"/>
                    </SSHConfig>
                    <Arguments>
                      <Argument value="$NUM_NODES$"/>
                      <Argument value="$MINUTES$"/>
                      <Argument value="$PV_SERVER_PORT$"/>
                      <Argument value="$PV_VERSION_FULL$"/>
                      <Argument value="$HEADLESS_API$"/>
                      <Argument value="/sw/frontier/ums/ums032/pvsc/ORNL/frontier.cfg"/>
                      <Argument value="PROJECT=$PROJECT$"/>
                      <Argument value="PARTITION=$PARTITION$"/>
                      <Argument value="NUM_MPI_TASKS=$NUM_MPI_TASKS$"/>
                      <Argument value="NUM_CORES_PER_MPI_TASK=$NUM_CORES_PER_MPI_TASK$"/>
                    </Arguments>
                  </SSHCommand>
                </CommandStartup>
              </Server>
            </Servers>

   .. tab-item:: Summit
      :sync: summit

      .. code-block::

            <Servers>
              <Server name="ORNL summit" resource="csrc://localhost">
                <CommandStartup>
                  <Options>
                    <Option name="HOST" label="Server host" save="true">
                      <String default="summit.olcf.ornl.gov"/>
                    </Option>
                    <Option name="HEADLESS_API" label="Server headless API" save="true">
                      <Enumeration default="osmesa">
                        <Entry value="osmesa" label= "OSMesa" />
                        <Entry value="egl" label= "EGL" />
                      </Enumeration>
                    </Option>
                    <Option name="USER" label="Server username" save="true">
                      <String default="YOURUSERNAME"/>
                    </Option>
                    <Switch name="PV_CLIENT_PLATFORM">
                      <Case value="Apple">
                        <Set name="TERM_PATH" value="/opt/X11/bin/xterm" />
                        <Set name="TERM_ARG1" value="-T" />
                        <Set name="TERM_ARG2" value="ParaView" />
                        <Set name="TERM_ARG3" value="-e" />
                        <Set name="SSH_PATH" value="ssh" />
                      </Case>
                      <Case value="Linux">
                        <Set name="TERM_PATH" value="xterm" />
                        <Set name="TERM_ARG1" value="-T" />
                        <Set name="TERM_ARG2" value="ParaView" />
                        <Set name="TERM_ARG3" value="-e" />
                        <Set name="SSH_PATH" value="ssh" />
                      </Case>
                      <Case value="Windows">
                        <Set name="TERM_PATH" value="cmd" />
                        <Set name="TERM_ARG1" value="/C" />
                        <Set name="TERM_ARG2" value="start" />
                        <Set name="TERM_ARG3" value="" />
                        <Set name="SSH_PATH" value="plink.exe" />
                      </Case>
                      <Case value="Unix">
                        <Set name="TERM_PATH" value="xterm" />
                        <Set name="TERM_ARG1" value="-T" />
                        <Set name="TERM_ARG2" value="ParaView" />
                        <Set name="TERM_ARG3" value="-e" />
                        <Set name="SSH_PATH" value="ssh" />
                      </Case>
                    </Switch>
                    <Option name="PV_SERVER_PORT" label="Server port ">
                      <Range type="int" min="1025" max="65535" step="1" default="random"/>
                    </Option>
                    <Option name="NUM_NODES" label="Number of compute nodes" save="true">
                      <Range type="int" min="1" max="100" step="1" default="1"/>
                    </Option>
                    <Option name="NRS" label="Number of resource sets (RS)" save="true">
                      <Range type="int" min="1" max="202400" step="1" default="1"/>
                    </Option>
                    <Option name="TASKS_PER_RS" label="Number of MPI tasks (ranks) per RS" save="true">
                      <Range type="int" min="1" max="42" step="1" default="1"/>
                    </Option>
                    <Option name="CPU_PER_RS" label="Number of CPUs (cores) per RS" save="true">
                      <Range type="int" min="1" max="42" step="1" default="1"/>
                    </Option>
                    <Option name="GPU_PER_RS" label="Number of GPUs per RS" save="true">
                      <Range type="int" min="0" max="6" step="1" default="0"/>
                    </Option>
                    <Option name="PROJECT" label="Project to charge" save="true">
                      <String default="cscXXX"/>
                    </Option>
                    <Option name="MINUTES" label="Number of minutes to reserve" save="true">
                      <Range type="int" min="1" max="240" step="1" default="30"/>
                    </Option>
                  </Options>
                  <Command exec="$TERM_PATH$" delay="5">
                    <Arguments>
                      <Argument value="$TERM_ARG1$"/>
                      <Argument value="$TERM_ARG2$"/>
                      <Argument value="$TERM_ARG3$"/>
                      <Argument value="$SSH_PATH$"/>
                      <Argument value="-t"/>
                      <Argument value="-R"/>
                      <Argument value="$PV_SERVER_PORT$:localhost:$PV_SERVER_PORT$"/>
                      <Argument value="$USER$@$HOST$"/>
                      <Argument value="/sw/summit/paraview/pvsc/ORNL/login_node.sh"/>
                      <Argument value="$NUM_NODES$"/>
                      <Argument value="$MINUTES$"/>
                      <Argument value="$PV_SERVER_PORT$"/>
                      <Argument value="$PV_VERSION_FULL$"/>
                      <Argument value="$HEADLESS_API$"/>
                      <Argument value="/sw/summit/paraview/pvsc/ORNL/summit.cfg"/>
                      <Argument value="PROJECT=$PROJECT$"/>
                      <Argument value="NRS=$NRS$"/>
                      <Argument value="TASKS_PER_RS=$TASKS_PER_RS$"/>
                      <Argument value="CPU_PER_RS=$CPU_PER_RS$"/>
                      <Argument value="GPU_PER_RS=$GPU_PER_RS$"/>
                    </Arguments>
                  </Command>
                </CommandStartup>
              </Server>
            </Servers>

.. note::  
    Although they can be separate files, all OLCF server 
    configurations can be combined and saved into one file following the hierarchy 
    ``<Servers><Server name= >...<\Server><Server name= >...<\Server><\Servers>``.

**Step 2: Launch ParaView on your Desktop and Click on File -> Connect**

Start ParaView and then select ``File/Connect`` to begin.

.. image:: /images/paraview_step1a_Andes.png
   :align: center

**Step 3: Import Servers**

Click Load Servers button and find the servers.pvsc file

.. image:: /images/paraview_step2a_Andes.png
   :align: center

.. note::  
    The ``Fetch Servers`` button fetches
    `Official Kitware Server Configurations <https://www.paraview.org/files/pvsc>`__.
    Summit, Andes, and Frontier configurations can be imported through this method, but are
    not guaranteed to be supported in future updates. Users may use these at their own risk.

After successfully completing the above steps, you should now be able to
connect to either Andes, Summit, or Frontier.

.. _paraview-gui:

Remote GUI Usage
================

After setting up and installing ParaView, you can connect to OLCF systems
remotely to visualize your data interactively through ParaView's GUI. To do so,
go to File→Connect and select either ORNL Andes, ORNL Summit, or ORNL Frontier
(provided they were successfully imported -- as outlined in :ref:`paraview-install-setup`).
Next, click on Connect and change the values in the Connection Options box.

.. image:: /images/paraview_step2a_Andes_2.png
   :align: center

A dialog box follows, in which you must enter in your username and project
allocation, the number of nodes to reserve and a duration to reserve them for.
This is also where you can choose between the OSMesa and EGL (ROCm for Frontier)
rendering options via the "Server headless API" box.

.. image:: /images/paraview_step2b_Andes.png
   :align: center

When you click OK, a windows command prompt or ``xterm`` pops up. In this
window enter your credentials at the OLCF login prompt.

.. image:: /images/paraview_step2c_Andes.png
   :align: center

When your job reaches the top of the queue, the main window will be returned to
your control. At this point you are connected and can open files that reside
there and visualize them interactively.

Creating a Python Trace
-----------------------

One of the most convenient tools available in the GUI is the ability to convert
(or "trace") interactive actions in ParaView to Python code. Users that repeat
a sequence of actions in ParaView to visualize their data may find the Trace
tool useful. The Trace tool creates a Python script that reflects most actions
taken in ParaView, which then can be used by either PvPython or PvBatch
(ParaView's Python interfaces) to accomplish the same actions. See section
:ref:`paraview-command-line` for an example of how to run a Python script using
PvBatch on Andes and Summit.

To start tracing from the GUI, click on Tools→Start Trace. An options window
will pop up and prompt for specific Trace settings other than the default. Upon
starting the trace, any time you modify properties, create filters, open files,
and hit Apply, etc., your actions will be translated into Python syntax. Once
you are finished tracing the actions you want to script, click Tools→Stop
Trace. A Python script should then be displayed to you and can be saved.

.. _paraview-command-line:

Command Line Example
====================

.. warning::
    Using ParaView via the command line should **always** be done through a
    batch job, and should always be executed on a compute node -- never the 
    login or launch nodes.

ParaView can be controlled through Python without opening the ParaView GUI. To
do this on OLCF systems, one must use a batch script in combination with
PvBatch (one of the Python interfaces available in ParaView). PvBatch accepts
commands from Python scripts and will run in parallel using MPI. Example
batch scripts, along with a working Python example, are provided below.

.. tab-set::

  .. tab-item:: Andes
     :sync: andes

      .. code-block:: bash
        :linenos:

        #!/bin/bash
        #SBATCH -A XXXYYY
        #SBATCH -J para_test
        #SBATCH -N 1
        #SBATCH -p batch
        #SBATCH -t 0:05:00

        cd $SLURM_SUBMIT_DIR
        date

        module load paraview/5.12.1-osmesa

        srun -n 28 pvbatch para_example.py

  .. tab-item:: Frontier
     :sync: frontier

      .. code-block:: bash
        :linenos:

        #!/bin/bash
        #SBATCH -A XXXYYY
        #SBATCH -J para_test
        #SBATCH -N 1
        #SBATCH -p batch
        #SBATCH -t 0:05:00

        cd $SLURM_SUBMIT_DIR
        date

        module load ums
        module load ums032
        module load dav-sdk
        module load paraview/5.12.1

        srun -n 28 pvbatch para_example.py

  .. tab-item:: Summit
     :sync: summit

      .. code-block:: bash
        :linenos:

        #!/bin/bash
        #BSUB -P XXXYYY
        #BSUB -W 00:05
        #BSUB -nnodes 1
        #BSUB -J para_test
        #BSUB -o para_test.%J.out
        #BSUB -e para_test.%J.err

        cd $LSB_OUTDIR
        date

        module load DefApps-2023
        module load paraview/5.11.0-osmesa

        # Set up flags for jsrun
        export NNODES=$(($(cat $LSB_DJOB_HOSTFILE | uniq | wc -l)-1))
        export NCORES_PER_NODE=28
        export NGPU_PER_NODE=0
        export NRS_PER_NODE=1
        export NMPI_PER_RS=28
        export NCORES_PER_RS=$(($NCORES_PER_NODE/$NRS_PER_NODE))
        export NGPU_PER_RS=$(($NGPU_PER_NODE/$NRS_PER_NODE))
        export NRS=$(($NNODES*$NRS_PER_NODE))

        jsrun -n ${NRS} -r ${NRS_PER_NODE} -a ${NMPI_PER_RS} -g ${NGPU_PER_RS} -c ${NCORES_PER_RS} pvbatch para_example.py

.. warning::
    If you plan on using the EGL version of the ParaView module (e.g.,
    paraview/5.12.1-egl), then you must be connected to the GPUs. On Andes,
    this is done by using the gpu partition via ``#SBATCH -p gpu``, while 
    on Summit the ``-g`` flag in the ``jsrun`` command must be greater 
    than zero.

Submitting one of the above scripts will submit a job to the batch partition
for five minutes using 28 MPI tasks across 1 node. As rendering speeds and
memory issues widely vary for different datasets and MPI tasks, users are
encouraged to find the optimal amount of MPI tasks to use for their data. Users
with large datasets may also find a slight increase in performance by using the
gpu partition on Andes, or by utilizing the GPUs on Summit. Once the batch job
makes its way through the queue, the script will launch the loaded ParaView
module (specified with ``module load``) and execute a python script called
``para_example.py`` using PvBatch. The example python script is detailed below,
and users are highly encouraged to use this script (especially after version
upgrades) for testing purposes.

The following script renders a 3D sphere colored by the ID (rank) of each MPI task:

.. code-block:: python
   :linenos:

   # para_example.py:
   from paraview.simple import *

   # Add a polygonal sphere to the 3D scene
   s = Sphere()
   s.ThetaResolution = 128                        # Number of theta divisions (longitude lines)
   s.PhiResolution = 128                          # Number of phi divisions (latitude lines)

   # Convert Proc IDs to scalar values
   p = ProcessIdScalars()                         # Apply the ProcessIdScalars filter to the sphere

   display = Show(p)                              # Show data
   curr_view = GetActiveView()                    # Retrieve current view

   # Generate a colormap for Proc Id's
   cmap = GetColorTransferFunction("ProcessId")   # Generate a function based on Proc ID
   cmap.ApplyPreset('Viridis (matplotlib)')       # Apply the Viridis preset colors
   #print(GetLookupTableNames())                  # Print a list of preset color schemes

   # Set Colorbar Properties
   display.SetScalarBarVisibility(curr_view,True) # Show bar
   scalarBar = GetScalarBar(cmap, curr_view)      # Get bar's properties
   scalarBar.WindowLocation = 'Any Location'       # Allows free movement
   scalarBar.Orientation = 'Horizontal'           # Switch from Vertical to Horizontal
   scalarBar.Position = [0.15,0.80]               # Bar Position in [x,y]
   scalarBar.LabelFormat = '%.0f'                 # Format of tick labels
   scalarBar.RangeLabelFormat = '%.0f'            # Format of min/max tick labels
   scalarBar.ScalarBarLength = 0.7                # Set length of bar

   # Render scene and save resulting image
   Render()
   SaveScreenshot('pvbatch-test.png',ImageResolution=[1080, 1080])

.. warning:: For older versions of ParaView (e.g., ``5.9.1``), line 23 should be ``'AnyLocation'`` (no space).

.. image:: /images/paraview_example_1.png
   :align: center
   :width: 540px

If everything is working properly, the above image should be generated after
the batch job is complete.

All of the above can also be achieved in an interactive batch job through the
use of the ``salloc`` command on Andes and Frontier, or the ``bsub -Is`` command on Summit.
Recall that login nodes should *not* be used for memory- or compute-intensive tasks, including ParaView.

Troubleshooting
===============

Process failed to start connection issue (or DISPLAY not set)
-------------------------------------------------------------

If ParaView is unable to connect to our systems after trying to initiate a
connection via the GUI and you see a "The process failed to start. Either the
invoked program is missing, or you may have insufficient permissions to invoke
the program" error, make sure that you have XQuartz (X11) installed.

For macOS clients, it is necessary to install `XQuartz (X11)
<https://www.xquartz.org/>`__ to get a command prompt in which you will
securely enter your OLCF credentials.

After installing, if you see a "Can't open display" or a "DISPLAY is not set"
error, try restarting your computer. Sometimes XQuartz doesn't function
properly if the computer was never restarted after installing.

ParaView crashes when using the EGL API module via command line
---------------------------------------------------------------

If ParaView crashes when using the EGL version of the ParaView module via the
command line and raises errors about OpenGL drivers or features, this is most
likely due to not being connected to any GPUs.

Double check that you are either running on the GPU partition on Andes (i.e.,
``-p gpu``), or that you have ``-g`` set to a value greater than zero in your
``jsrun`` command on Summit.

If problems persist and you do not need EGL, try using the OSMesa version of
the module instead (e.g., paraview/5.9.1-osmesa instead of paraview/5.9.1-egl).

Default Andes module not working with PvBatch or PvPython (Aug. 31, 2021)
-------------------------------------------------------------------------

A ``command not found`` error occurs when trying to execute either PvBatch or
PvPython after loading the default ParaView module on Andes. To fix this, you
must load the equivalent ParaView module ending in "pyapi" instead (i.e.,
``module load paraview/5.9.1-py3-pyapi`` instead of ``module load
paraview/5.9.1-py3``). 

Alternatively, the ParaView installations in ``/sw/andes/paraview`` (i.e., the
paraview/5.9.1-egl and paraview/5.9.1-osmesa modules) can also be loaded to
avoid this issue.

.. _paraview-resources:

Additional Resources
====================

* The `ParaView on Frontier tutorial <https://github.com/olcf/dva-training-series/tree/main/paraview_2024>`__ highlights
  how to get started on OLCF systems with example datasets.
* The `Official ParaView User's Guide <https://docs.paraview.org/en/latest/>`__
  and the `Python API Documentation <https://www.paraview.org/paraview-docs/latest/python/>`__
  contain all information regarding the GUI and Python interfaces.
* A full list of `ParaView Documentation <https://www.paraview.org/resources/>`__
  can be found on ParaView's website.
* The `ParaView Wiki <https://www.paraview.org/Wiki/ParaView>`__
  contains extensive information about all things ParaView.
* Tutorials can be found on the ParaView Wiki at 
  `The ParaView Tutorial <https://www.paraview.org/Wiki/The_ParaView_Tutorial>`__ and
  `SNL ParaView Tutorials <https://www.paraview.org/Wiki/SNL_ParaView_Tutorials>`__.
* `Sample Data <https://www.paraview.org/download/>`__ not pre-packaged with 
  ParaView can be found on the ParaView download page under the Data section. 
* `Specific ParaView Versions <https://www.paraview.org/download/>`__ and their
  `Release Notes <https://www.paraview.org/Wiki/ParaView_Release_Notes>`__ 
  can be found on the ParaView website and ParaView Wiki, respectively.
* Non-ORNL related bugs and issues in ParaView can be found and reported on
  `Discourse <http://discourse.paraview.org/>`__.
