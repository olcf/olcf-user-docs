*****
VisIt
*****

.. note:: VisIt 3.4.2 is now available on Andes.

Overview
========

VisIt is an interactive, parallel analysis and visualization tool for
scientific data. VisIt contains a rich set of visualization features so you can
view your data in a variety of ways. It can be used to visualize scalar and
vector fields defined on two- and three-dimensional (2D and 3D) structured and
unstructured meshes. Further information regarding VisIt can be found at the
links provided in the :ref:`visit-resources` section.

.. _visit-setup:

Installing and Setting Up Visit
===============================

VisIt uses a client-server architecture. You will obtain the best performance
by running the VisIt client on your local computer and running the server on
OLCF resources. VisIt for your local computer can be obtained here: 
`VisIt Installation <https://visit-dav.github.io/visit-website/>`__.  

Recommended VisIt versions on our systems:

* Andes: VisIt 3.3.3, 3.4.1, 3.4.2
* Frontier: VisIt 3.3.3

.. warning::
    Using a different version than what is listed above is not guaranteed to work properly.

For sample data and additional examples, explore the
`VisIt Data Archive <https://visit-dav.github.io/largedata/datarchives.html>`__
and various `VisIt Tutorials <https://visit-sphinx-github-user-manual.readthedocs.io/en/develop/tutorials/index.html>`__.
Supplementary test data can be found in your local installation in the ``data``
directory:

* Linux: ``/path/to/visit/data``
* macOS: ``/path/to/VisIt.app/Contents/Resources/data``
* Windows: ``C:\path\to\LLNL\VisIt x.y.z\data``

Additionally, check out our beginner friendly
`OLCF VisIt Tutorial <https://github.com/olcf/dva-training-series/tree/main/visit>`__
which uses Andes to visualize example datasets.

.. _visit-host-profiles:

Creating ORNL/OLCF Host Profiles
--------------------------------

The first time you launch VisIt (after installing), you will be prompted for a
remote host preference. Unfortunately, ORNL does not maintain that list
often, so the ORNL entry may be outdated. Click the “None” option instead.
Restart VisIt, and go to Options→Host Profiles. Select “New Host”

.. tab-set::

  .. tab-item:: Andes

      **For Andes:**

      - **Host nickname**: ``Andes`` (this is arbitrary)
      - **Remote hostname**: ``andes.olcf.ornl.gov`` (required)
      - **Host name aliases**: ``andes-login#g`` (required)
      - **Maximum Nodes**: Unchecked
      - **Maximum processors**: Unchecked (arbitrary)
      - **Path to VisIt Installation**: ``/sw/andes/visit`` (required)
      - **Username**: Your OLCF Username (required)
      - **Tunnel data connections through SSH**: Checked (required)

      Under the “Launch Profiles” tab create a launch profile. Most of these values
      are arbitrary

      - **Profile Name**: ``batch`` (arbitrary)
      - **Timeout**: 480 (arbitrary)
      - **Number of threads per task**: 0 (arbitrary, but not tested
        with OMP/pthread support)
      - **Additional arguments**: blank (arbitrary)

      Under the “Parallel” Tab:

      - **Launch parallel engine**: Checked (required)
      - Launch Tab:

          - **Parallel launch method**:
            ``sbatch/srun`` (required)
          - **Partition/Pool/Queue**: ``batch`` (required)
          - **Number of processors**: 1 (arbitrary, but
            high number may lead to OOM errors) (max for ``batch`` queue is 32)
          - **Number of nodes**: 1 (arbitrary)
          - **Bank/Account**: Your OLCF project to use (required)
          - **Time Limit**: 1:00:00 (arbitrary, ``HH:MM:SS``)
          - **Machine file**: Unchecked (required – Lets VisIt get
            the nodelist from the scheduler)
          - **Constraints**: Unchecked
      - Advanced tab – All boxes unchecked
      - GPU Acceleration

          - **Use cluster’s graphics cards**: Unchecked (even if using the ``gpu`` partition)

      Click “Apply” and make sure to save the settings (Options/Save Settings).
      Exit and re-launch VisIt.

      .. note::
          Users with large datasets may see a slight performance boost by
          using the high-memory ``gpu`` partition or by increasing
          the number of processors if memory is not an issue. See the
          :ref:`visit-modify-host` section below for how to add a ``gpu`` partition
          launch profile on Andes.

  .. tab-item:: Frontier

      **For Frontier:**

      - **Host nickname**: ``Frontier`` (this is arbitrary)
      - **Remote hostname**: ``frontier.olcf.ornl.gov`` (required)
      - **Host name aliases**: ``login#`` (required)
      - **Maximum Nodes**: Unchecked
      - **Maximum processors**: Unchecked (arbitrary)
      - **Path to VisIt Installation**: ``/sw/frontier/spack-envs/cpe23.12-cpu/opt/gcc-12.3/visit-3.3.3-lde2fkdwxnk43faw64qtcskjtwn54vsy/`` (required)
      - **Username**: Your OLCF Username (required)
      - **Tunnel data connections through SSH**: Checked (required)

      Under the “Launch Profiles” tab create a launch profile. Most of these values
      are arbitrary

      - **Profile Name**: ``batch`` (arbitrary)
      - **Timeout**: 480 (arbitrary)
      - **Number of threads per task**: 0 (arbitrary, but not tested
        with OMP/pthread support)
      - **Additional arguments**: blank (arbitrary)

      Under the “Parallel” Tab:

      - **Launch parallel engine**: Checked (required)
      - Launch Tab:

          - **Parallel launch method**:
            ``sbatch/srun`` (required)
          - **Partition/Pool/Queue**: ``batch`` (required)
          - **Number of processors**: 1 (arbitrary, but
            high number may lead to OOM errors) (max is 56)
          - **Number of nodes**: 1 (arbitrary)
          - **Bank/Account**: Your OLCF project to use (required)
          - **Time Limit**: 01:00:00 (arbitrary, ``HH:MM:SS``)
          - **Machine file**: Unchecked (required – Lets VisIt get
            the nodelist from the scheduler)
          - **Constraints**: Unchecked
      - Advanced tab – All boxes unchecked
      - GPU Acceleration

          - **Use cluster’s graphics cards**: Unchecked

      Click “Apply” and make sure to save the settings (Options/Save Settings).
      Exit and re-launch VisIt.

      .. note::
          If you want to use the ``debug`` QOS on Frontier, you can add ``-q debug``
          to the "Launcher arguments" section under the "Advanced" tab (make sure
          to also check the "Launcher arguments" box).


.. _visit-modify-host:

Modifying Host Profiles
-----------------------

See :ref:`visit-host-profiles` section above for creating your initial host profile.

To make changes to an *existing* host profile, do the following:

-  Go to "Options→Host Profiles".
-  The window will display the known hosts on the left, with the 
   settings for that host shown on the right in the "Host Settings" tab.
-  You can modify settings relevant to this host machine. For example,
   you can change the "Username" field if your OLCF username differs
   from your local computer username.
-  Once you have made your changes, press the "Apply" button, and then
   save the settings (Options/Save Settings).

Each host can have several launch profiles. A launch profile specifies how VisIt 
runs on a given host computer. To make changes to a host's launch profile, do
the following:

-  Go to "Options→Host Profiles".
-  Select the host in the left side of the window.
-  Select the "Launch Profiles" tab in the right side of the window.
   This will display the known launch profiles for this host.
-  Select a "Launch Profile" and the settings are displayed in the tabs
   below.
-  You can set your Project ID in the "Default Bank/Account" field in
   the "Parallel" tab.
-  You can change the queue used by modifying the "Partition/Pool/Queue"
   field in the "Parallel" tab.
-  Once you have made your changes, press the "Apply" button, and then
   save the settings (Options/Save Settings).

For example, this is how you would modify the Andes profile to use the ``gpu`` partition:

Under Andes' "Launch Profiles":

1. Click on "New Profile"
2. Name the profile something like "gpu" (arbitrary)
3. Click on "Parallel"
4. Check "Launch Parallel Engine"
5. Set "Launch Method" to ``sbatch/srun`` (required)
6. Set "Partition/Pool/Queue" to ``gpu`` (required)
7. Set default number of processors to 28 (max without hyperthreading) (arbitrary)
8. Set default number of nodes to 1 (arbitrary)
9. Set default "Bank/Account" to your OLCF project with Andes allocation
10. Set a default "Time Limit" in format of (``HH:MM:SS``)
11. Click "Apply"
12. At the top menu click on "Options"→"Save Settings"

.. _visit-remote-gui:

Remote GUI Usage
================

Once you have VisIt installed and set up on your local computer:

-  Open VisIt on your local computer.
-  Go to: "File→Open file" or click the "Open" button on the GUI.
-  Click the "Host" dropdown menu on the "File open" window that popped
   up and choose "ORNL\_Andes".
-  This will prompt you for your OLCF password, and connect you to Andes.
-  Navigate to the appropriate file.
-  Once you choose a file, you will be prompted for the number of nodes
   and processors you would like to use (remember that each node of Andes
   contains 32 processors, or 28 if using the high-memory GPU partition) 
   and the Project ID, which VisIt calls a "Bank" as shown below.

.. image:: /images/Visit_Andes_1.png
   :align: center

-  Once specified, the server side of VisIt will be launched, and you
   can interact with your data.

The above procedure can also be followed to connect to Frontier, with
the main difference being the number of available processors.
Both Andes and Frontier follow HH:MM:SS syntax for the time limit.

Please do not run VisIt's GUI client from an OLCF machine. You will get much 
better performance if you install a client on your workstation and launch 
locally. You can directly connect to OLCF machines from inside VisIt and 
access your data remotely.

.. _visit-command-line:

Command Line Example
====================

.. warning::
    Using VisIt via the command line should **always** result in a batch job, and
    should always be executed on a compute node -- never the login or launch nodes.

Although most users find better performance following the approach outlined in
:ref:`visit-remote-gui`, some users that don't require a GUI may find better
performance using VisIt's CLI in a batch job. An example for doing this on
OLCF systems is provided below.


**For Andes/Frontier (Slurm Script):**

.. tab-set::

  .. tab-item:: Andes

      .. code-block:: bash
        :linenos:

        #!/bin/bash
        #SBATCH -A XXXYYY
        #SBATCH -J visit_test
        #SBATCH -N 1
        #SBATCH -p gpu
        #SBATCH -t 0:05:00

        cd $SLURM_SUBMIT_DIR
        date

        module load visit

        visit -nowin -cli -v 3.4.2 -l srun -np 28 -nn 1 -s visit_example.py

  .. tab-item:: Frontier

      .. code-block:: bash
        :linenos:

        #!/bin/bash
        #SBATCH -A XXXYYY
        #SBATCH -J visit_test
        #SBATCH -N 1
        #SBATCH -p batch
        #SBATCH -t 0:05:00

        cd $SLURM_SUBMIT_DIR
        date

        module load cpe/23.12
        module load PrgEnv-gnu/8.5.0
        module load gcc-native/12.3
        module load visit

        visit -nowin -cli -v 3.3.3 -l srun -np 28 -nn 1 -s visit_example.py

Following one of the methods above will submit a batch job for five minutes to
either Andes or Frontier.  Once the batch job makes its way through
the queue, the script will launch VisIt version X.Y.Z (specified with the
**-v** flag, required on Andes) and execute a python script called
``visit_example.py`` (specified with the **-s** flag, required if using a
Python script). Note that the **-nowin -cli** options are also required, which
launches the CLI and tells VisIt to not launch the GUI. Although a Python
script is used for this example, not calling the **-s** flag will launch the
CLI in the form of a Python shell, which can be useful for interactive batch
jobs.  The **-np** and **-nn** flags represent the number of processors and
nodes VisIt will use to execute the Python script, while the **-l** flag
specifies the specific parallel method to do so (required). Execute ``visit
-fullhelp`` to get a list of all command line options.

The example script ``visit_example.py`` is detailed below and uses data
packaged with a standard VisIt installation (``tire.silo``). Although the
``tire.silo`` dataset does not need a large number of MPI tasks to render
quickly, users visualizing large datasets may find the syntax helpful outside
of this example, however a performance boost is not guaranteed. All users are
encouraged to test the effect of additional processors on their own data, as
rendering speeds can widely vary depending on the amount of MPI tasks utilized.
Users are highly encouraged to use this script (especially after system
upgrades) for testing purposes.

The following script renders a 3D pseudocolor plot of the temperature variable
from the ``tire.silo`` dataset:

.. code-block:: python
   :linenos:

   # visit_example.py:
   import sys

   # Open the file to visualize
   OpenDatabase("/sw/andes/visit/data/tire.silo")

   # Set options for output
   swa = SaveWindowAttributes()
   swa.outputToCurrentDirectory = 1      # Save images in current directory
   swa.fileName = "tire_pseudocolor"     # Image filename
   swa.family = 0                        # Do not append numbers to filename
   swa.format = swa.PNG                  # Save as PNG
   #swa.width = 1100                     # Image width (does not apply to screen capture)
   #swa.height = 1000                    # Image height (does not apply to screen capture)
   swa.resConstraint = swa.NoConstraint  # Do not force aspect ratio, use width and height
   swa.screenCapture = 1                 # Enable screen capture
   ResizeWindow(1, 1100, 1000)           # Setting Window 1's size (for screen capture)
   SetSaveWindowAttributes(swa)

   # Create a pseudocolor plot
   AddPlot("Pseudocolor", "temperature") # Plot type, variable name

   # Pseudocolor attributes settings
   PseudocolorAtts = PseudocolorAttributes()
   PseudocolorAtts.centering = PseudocolorAtts.Nodal  # Natural, Nodal, Zonal -- Nodal for smoothing
   PseudocolorAtts.colorTableName = "viridis_light"   # Set colormap
   PseudocolorAtts.invertColorTable = 1               # Invert colors
   SetPlotOptions(PseudocolorAtts)

   # Annotation attributes settings
   AnnotationAtts = AnnotationAttributes()
   AnnotationAtts.userInfoFlag = 0 # Turn off display of user information
   SetAnnotationAttributes(AnnotationAtts)

   # Set viewpoint
   vatts = View3DAttributes()
   vatts.viewNormal = (0.7, 0.1, 0.7)
   vatts.focus = (0, 0, 0)
   vatts.viewUp = (0, 1, 0)
   vatts.viewAngle = 30
   vatts.parallelScale = 82.9451
   vatts.nearPlane = -165.89
   vatts.farPlane = 165.89
   vatts.imagePan = (0, 0)
   vatts.imageZoom = 1
   vatts.perspective = 1
   vatts.eyeAngle = 2
   SetView3D(vatts)

   # Draw plots and save resulting image
   DrawPlots()
   SaveWindow()

   # Quit
   sys.exit(0)

.. image:: /images/Visit_example_1.png
   :align: center
   :width: 550px

If everything is working properly, the above image should be generated after
the batch job is complete. 

For users not interested in using screen capture, one would need to comment out
line 16 (or change the value to 0), and syntax for resizing the window is
displayed on lines 13 and 14 -- however saving the window in this manner on
OLCF systems has resulted in errors in the past.

All of the above can also be achieved in an interactive batch job through the
use of the ``salloc`` command on Andes or Frontier.
Recall that login nodes should *not* be used for memory- or compute-intensive
tasks, including VisIt.

.. _visit-troubleshooting:

Troubleshooting
===============

Scalable Render Request Failed when using VisIt (fixed Feb. 2022)
-----------------------------------------------------------------

Some users have encountered their compute engine exiting abnormally on Andes
after VisIt reaches 100% when drawing a plot, resulting in a "Scalable Render
Request Failed (VisItException)" error message. This message has also been
reported when users try to save plots, if VisIt was successfully able to draw.
The error seems to more commonly occur for users that are trying to visualize
large datasets.

VisIt developers have been notified, and at this time the current workaround is
to disable Scalable Rendering from being used. To do this, go to
Options→Rendering→Advanced and set the "Use Scalable Rendering" option to
"Never".

However, this workaround has been reported to affect VisIt's ability to save
images, as scalable rendering is utilized to save plots as image files (which
can result in another compute engine crash). To avoid this, screen capture must
be enabled. Go to File→"Set save options" and check the box labeled "Screen
capture".


As of February 2022, this issue on Andes has been fixed (must use VisIt 3.2.2 or higher).

SSH error after accepting passcode (duplicate host profile bug)
---------------------------------------------------------------

If you see an error similar to "The metadata server on host andes.olcf.ornl.gov
could not be launched or it could not connect back to your local computer" with
the specific error listed as "The reason for the exception was not described",
double check your host profiles. This bug may occur when you have two or more
host profiles that represent the same system (e.g., if you have two host
profiles that connect to andes.olcf.ornl.gov, but may have different settings /
usernames for both). This bug can affect both Frontier and Andes.

One solution is to change the host nickname of the duplicate host profile to
start with "Copy of".  For example, if my original host profile was named "ORNL
Andes", a proper duplicate should be named "Copy of ORNL Andes" (this is the
same nickname that would be generated when clicking the "Copy Host" button in
VisIt). After renaming, make sure to save your settings via "Options/Save
Settings" then close and restart VisIt.

Another solution is to delete all copies of a host profile (including the
original) and remake them. This can be achieved with the "Delete Host" button
in the Host Profiles window. Make sure to save your settings after deleting the
profiles, exit and restart VisIt, and then proceed with remaking your profiles. 

If none of the above solutions work for you, the final option would be to
delete the duplicate host profile entirely and just modify the settings of the
original when needed.

VisIt launch continues indefinitely after entering passcode
-----------------------------------------------------------

If the pop-up box called "metadata server launch progress" never goes away
after entering your passcode, you may need to check if you have enough storage
space available in your home directory (``/ccs/home/[user id]``). When
connecting to OLCF systems, VisIt creates some small temporary files in your
home directory that are unable to be created if you are over your quota (50 GB
is the default quota limit).

If the above does not apply to you, double check that you set up your host
profile exactly as how it is outlined in the :ref:`visit-host-profiles` section.
It may be helpful to delete and remake your host profile, but just remember
to always save your settings via "Options/Save Settings".

VisIt keeps asking for your password.
-------------------------------------

If VisIt keeps asking for your "Password" in the dialog box below, and you are
entering your correct PIN + RSA token code, you might need to select "Change
username" and then enter your OLCF username when prompted.

.. image:: /images/Visit_Andes_2.png
   :align: center

This will give you a new opportunity to enter your PIN + token code and your
username will appear in login request box as shown below. If you want you OLCF
username to be filled in by default, go to "Options→Host profiles" and enter it
under "Username".

.. image:: /images/Visit_Andes_3.png
   :align: center

VisIt will not connect when you try to draw an image.
-----------------------------------------------------

If VisIt will not connect to Andes or Frontier when you try to draw an image, you
should login to the system and check if a job is in the queue. To do this on
Andes or Frontier , enter ``squeue`` from the command line. Your VisIt job should appear in the queue.
If you see it in a state marked "PD" or "PEND" you should wait a bit longer to see
if it will start. If you do not see your job listed in the queue, check to make
sure your project ID is entered in your VisIt host profile. See the
:ref:`visit-modify-host` section for instructions.

Fatal Python error when launching the CLI
-----------------------------------------

If VisIt immediately crashes after launching it via the command line (like in a
batch script or interactive batch job) and displays a ``Fatal Python error:
initfsencoding: Unable to get the locale encoding`` error message, you should
specify a specific VisIt version with the **-v** flag when launching VisIt.
This is necessary even if you plan to use the default version of VisIt on the
system. See :ref:`visit-command-line` for proper syntax.

VisIt never asks for passcode then hangs
----------------------------------------

If VisIt never asks for your passcode and hangs after trying to connect to one
of our systems, then this means VisIt is unable to establish a proper
SSH connection. Here are a few different approaches to fix this issue:

* Double check your host profile, especially the "remote host name",
  "host name aliases", and "tunnel data connections through SSH" sections.
* If you are using a VPN (including GlobalProtect VPN), try turning it off.
* If you use multi-factor authentication (MFA4) with a smartcard or yubikey
  when connecting to our systems, this does not work with VisIt. VisIt only
  accepts RSA PIN+tokencodes, so you will have to change your SSH config
  settings (typically within a ``.ssh/config`` file) and temporarily turn
  off MFA4.

.. _visit-resources:

Additional Resources
====================

* The `OLCF VisIt Tutorial on Andes
  <https://github.com/olcf/dva-training-series/tree/main/visit>`__ is a
  beginner friendly tutorial for getting started on Andes with example datasets.
* The `VisIt User Manual <https://visit-sphinx-github-user-manual.readthedocs.io/en/develop/>`__ 
  contains all information regarding the CLI and the GUI.
* `Past VisIt Tutorials <https://www.visitusers.org/index.php?title=VisIt_Tutorial>`__ 
  are available on the Visit User's Wiki along with a set of 
  `Updated Tutorials <https://visit-sphinx-github-user-manual.readthedocs.io/en/develop/tutorials/index.html>`__ 
  available in the VisIt User Manual.
* Sample data not pre-packaged with VisIt can be found in the 
  `VisIt Data Archive <https://visit-dav.github.io/largedata/datarchives.html>`__.
* `Older VisIt Versions <https://wci.llnl.gov/simulation/computer-codes/visit/executables>`__ 
  with their release notes can be found on the old VisIt website, and
  `Newer Versions <https://visit-dav.github.io/visit-website/releases-as-tables/>`__ 
  can be found on the new VisIt website with release notes found on the
  `VisIt Blog <https://visit-dav.github.io/visit-website/blog/archive/>`__
  or `VisIt Github Releases <https://github.com/visit-dav/visit/releases>`__ page.
* Non-ORNL related bugs and issues in VisIt can be found and reported on
  `Github <https://github.com/visit-dav/visit/discussions>`__.
