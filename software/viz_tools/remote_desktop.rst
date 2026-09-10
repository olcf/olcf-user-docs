********************
Remote Desktop Tools
********************

Overview
========

Remote desktop tools let you run a full graphical desktop session on an HPC system and display it on your local machine through SSH tunneling or dedicated "viewer" software.
VNC is a common option for this workflow and is often more effective than X11 forwarding for visualization and other GUI-based applications that do not have a remote client/server mode (e.g., :doc:`/software/viz_tools/vmd`).
Additionally, this lets you launch the desired application directly on the compute node, allowing it to use native GPU hardware and rendering features that may be unavailable or not enabled when using applications in their remote client/server modes (e.g., :doc:`/software/viz_tools/visit`).

The examples below show how to use VNC and other remote desktop tools for remote visualization on our Riker visualization cluster.

.. warning::
    For macOS clients, it is necessary to install `XQuartz (X11) <https://www.xquartz.org/>`__ to allow x11 forwarding.
    For Windows clients, it is necessary to install either PuTTY or an X client like Xming.

Remote Visualization using VNC
==============================

The below example is how to use VNC on Riker.

.. dropdown:: test-vnc.sh

    .. code::

        #!/bin/sh

        what()
        {
           hostname
        }
        echo "Starting vncserver"

        vncserver :1 -geometry 1920x1080 -depth 24

        echo
        echo
        echo "**************************************************************************"
        echo "Instructions"
        echo
        echo "In a new terminal, open a tunneling connection with $(what) and port 5901"
        echo
        echo "example:"
        echo "   localsystem: ssh -L 5901:$(what):5901 ${USER}@riker.olcf.ornl.gov "
        echo
        echo "**************************************************************************"
        echo
        echo

        export DISPLAY=:1

        module load visit
        visit
        vncserver -kill :1

Step 1 (local system)
---------------------

Install a vncviewer (`turbovnc <https://github.com/TurboVNC/turbovnc/releases>`__, `tigervnc <https://github.com/TigerVNC/tigervnc/releases>`__, etc.) on your local machine.
When running vncviewer for the first time, it will ask to set a password for this and future vnc sessions.

Step 2 (terminal 1)
-------------------

From an Riker connection launch a batch job and execute the below ``test-vnc.sh`` script to start the vncserver and run an executable (e.g., VisIt):

#. localsytem: ``ssh -X username@riker.olcf.ornl.gov``
#. riker: ``salloc -A <project_id> -p gpu -t 1:00:00 -N 1 --exclusive --x11=batch``
#. riker: ``./test-vnc.sh`` (e.g., on ``riker-gpu1``)

.. code::

    $ ./test-vnc.sh

    You will require a password to access your desktops.

    Password:
    Verify:

    New 'riker-gpu1:1 (username)' desktop is riker-gpu1:1

    Creating default startup script /ccs/home/username/.vnc/xstartup
    Creating default config /ccs/home/username/.vnc/config
    Starting applications specified in /ccs/home/username/.vnc/xstartup
    Log file is /ccs/home/username/.vnc/riker-gpu1:1.log



    **************************************************************************
    Instructions

    In a new terminal, open a tunneling connection with riker-gpu1 and port 5901

    example:
         localsystem: ssh -L 5901:riker-gpu1:5901 username@riker.olcf.ornl.gov

    **************************************************************************


Step 3 (terminal 2)
-------------------

In a second terminal on your local system open a tunneling connection following the instructions given by the vnc start-up script (e.g., for ``riker-gpu1``):

-  localsystem: ``ssh -L 5901:riker-gpu1:5901 username@riker.olcf.ornl.gov``

Step 4 (local system)
---------------------

Launch the vncviewer. When you launch the vncviewer that you downloaded you will need to specify ``localhost:5901``.
You will also set a password for the initial connection or enter the created password for subsequent connections.


.. Remote Visualization using Nice DCV (GPU nodes only)
.. ----------------------------------------------------

.. .. note::
..    Nice DCV is back online and working on Andes again. If you see issues email help@olcf.ornl.gov

.. Step 1 (terminal 1)
.. ^^^^^^^^^^^^^^^^^^^

.. Launch an interactive job:

.. .. code::

..      localsytem: ssh username@andes.olcf.ornl.gov
..      andes: salloc -A <project_id> -p gpu -t 60:00 -N 1 --exclusive -M andes --constraint=DCV

.. Run the following commands:

.. .. code::

..     $ xinit &
..     $ export DISPLAY=:0
..     $ dcv create-session --gl-display :0 mySessionName
..     $ hostname  // will be used to open a tunneling connection with this node
..     $ andes-gpuN

.. Step 2 (terminal 2)
.. ^^^^^^^^^^^^^^^^^^^

.. Open a tunneling connection with gpu node ``N``, given by hostname:

.. .. code::

..     localsystem: ssh username@andes.olcf.ornl.gov -L 8443:andes-gpuN:8443

.. Open your web browser using the following link and use your credentials to
.. access OLCF systems: ``https://localhost:8443`` When finished, kill the dcv
.. session in first terminal:

.. .. code::

..     $ dcv close-session mySessionName
..     $ kill %1
