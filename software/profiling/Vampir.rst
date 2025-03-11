.. _vampir:

.. image:: /images/vampir_logo.png
   :width: 230px
   :height: 130px

************************************
Vampir
************************************

Overview
=========

Vampir is a software performance visualizer focused on highly-parallel applications. It presents a unified view on an application run
including the use of programming paradigms like MPI, SHMEM, OpenMP, PThreads, HIP, CUDA, OpenCL and OpenACC.
Vampir can also incorporate file I/O, hardware performance counters and other performance data sources.
Various interactive displays offer detailed insight into the performance behavior of the analyzed application.
Vampir's scalable analysis server and visualization engine enable interactive navigation of large amounts of performance data.

Score-P and TAU are two instrumentation and runtime-measurement tools that can generate OTF2 trace files for Vampir to visualize.
These support various instrumentation options including source level
instrumentation as well as compile/link time instrumentation.

See https://vampir.eu/ for details about Vampir.

Usage
=======

Vampir can be run a few different ways depending on a couple of factors. If you have a large trace file it
could benefit from utilizing VampirServer to process the trace file with the system's compute power
while connected to the Vampir GUI at the user-site. If the trace file is small enough (< ~1 GB), 
it would do just fine viewing on a login node.

.. _vamps:

``VampirServer`` is the backend software component that can run across multiple compute nodes taking advantage
of the machine's memory, this in turn provides an increase in performance for viewing large trace files i.e. >1GB.
*Note: VampirServer does not take advantage of GPU acceleration.*

The following sections will cover the 3 different methods for using Vampir.
For each method, you will need to enable `X11 forwarding <https://docs.olcf.ornl.gov/connecting/index.html#x11-forwarding>`_
on an OLCF machine to allow a GUI to be launched to a remote screen.
To do so, you can use the ``ssh -X`` (using option '-X ') as shown below

.. code::

   $ ssh -X <userid>@<machine>.olcf.ornl.gov
   # On Frontier: ssh -X <userid>@frontier.olcf.ornl.gov

Please visit this link if you need more information for different `ORNL Systems <https://docs.olcf.ornl.gov/systems/index.html>`_


Vampir on a Login Node
======================

.. image:: /images/vampir_login_gui.png
  :width: 280px
  :height: 125px

.. Note::

   Do not run Vampir on a login node for trace files > 1 GB! Please see the next 2 sections for running larger trace files.

After logging onto your machine with `X11 forwarding <https://docs.olcf.ornl.gov/connecting/index.html#x11-forwarding>`_, 
execute the series of commands below:

.. code::

   $ ssh -X <userid>@<machine>.olcf.ornl.gov
   ...
   <machine>$ module load vampir
   <machine>$ vampir &

Once the GUI pops up (might take a few seconds), you can load a file resident on the file system by
selecting ``Local File`` for file selection.

.. image:: /images/vampir_splash_screen_file_selection.png
   :width: 300px
   :height: 200px


Vampir Using VampirServer
=========================

.. image:: /images/vampir_login_node_connect_to_compute.png
   :width: 350px
   :height: 125px

.. Note::

   Please use this connection method for trace files larger than (> 1 GB), and see the next section :ref:`Vampir Tunneling to VampirServer <vamptunnel>` for an even more optimal solution.
   Attempting to visualize large trace files (> 1 GB) will be very slow over X11 forwarding and can cause decreased performance on the shared
   login nodes for other users

After connecting to your `ORNL System <https://docs.olcf.ornl.gov/systems/index.html>`_ using `X11 forwarding <https://docs.olcf.ornl.gov/connecting/index.html#x11-forwarding>`_
you will need to load the Vampir module and start the :ref:`VampirServer. <vamps>`

.. code::

   $ module load vampir
   $ vampirserver start -- -A <Account/Project_ID> -t <walltime in HH:MM:SS> -N <num of nodes>
   # Example: vampirserver start --  -A ABC123 -t 60 -N 1

.. _vampserpw:

Successful VampirServer startup messages should appear in terminal window. You will need this information!

.. code::

   [login_node]$ vampirserver start -- -A ABC123 -t 00:05:00 -N 1
   Launching VampirServer...
   Submitting to slurm a 1 node job with a walltime of 00:05:00...
   ...
   VampirServer 10.5.0 Professional (00a4a90a)
   Licensed to ORNL
   Running 4 analysis processes... (abort with vampirserver stop 19361)
   User: <USERID>
   Password: XXXXXXXXXXXX
   VampirServer <19361> listens on: frontier00018:30092


Launch the Vampir GUI
---------------------
.. code::

   $ vampir &

.. _vampauth:

Once the GUI has opened, you will need to connect to the :ref:`VampirServer <vamps>` using the
**Remote File** option as shown below. **If there is a 'recent files' window open, select 'open other'.**
Enter the ``node ID`` and the ``port`` number from above.
Select **Encrypted password** from the **Authentication** dropdown option.
Then press Connect.

.. image:: /images/vampir_open_remote_location.png
   :width: 800px
   :height: 300px

When the server authentication window pops up, you will need to enter the ``USERID``
and the :ref:`VampirServer password <vampserpw>` that was printed on the terminal screen.
Once authenticated, you will be able to navigate through the filesystem to your **.otf2** files

.. image:: /images/vampir_server_auth.png
   :width: 400px
   :height: 300px

.. _vamptunnel:


Vampir Tunneling to VampirServer
===========================================

.. image:: /images/vampir_reverse_connect_gui_to_compute.png
   :width: 350px
   :height: 125px

This connection method is more complex than the other 2 methods, however it also can provide a more optimal experience for very large trace files.  
The Vampir GUI client will be on your local machine and the server will be on the compute nodes.

.. Note::

   ``This method will require you to have a local copy of the Vampir GUI already installed on your machine.``

   If you do not have a local copy, please reach out to the help desk at help@olcf.ornl.gov for instructions on getting a local copy.

Similar to the previous methods outlined above, you will start by connecting to
your `ORNL System <https://docs.olcf.ornl.gov/systems/index.html>`_ using `X11
forwarding <https://docs.olcf.ornl.gov/connecting/index.html#x11-forwarding>`_
Once connected you will then need to start the :ref:`VampirServer. <vamps>`

.. code::

   $ module load vampir
   # Start the VampirServer
   $ vampirserver start -- -A <Account/Project_ID> -t <walltime in HH:MM:SS> -N <num of nodes>
   # Example: vampirserver start --  -A ABC123 -t 60 -N 1

Once you have successfully authenticated, you will need the information printed on the :ref:`terminal window. <vampserpw>`
That includes:

* Node ID
* Port Number
* password

Once the VampirServer is started, in a **fresh** terminal window on your **Local** machine you can then initiate the
port forward command. This will open a secure tunnel from your local machine to the backend server running VampirServer.

**Port Forwarding**

.. code::

   [local_machine]$ ssh -L <localport>:<Node ID>:<Remote port>  <USERID>@<SYSTEM>.olcf.ornl.gov

   # Example on Frontier: ssh -L 30000:frontier00018:30092 <USERID>@frontier.olcf.ornl.gov
   # Localhost port is 30000.  Vampirserver listens on frontier00018 at port 30092.

.. Note::

   The local port number can be any unused port number on your local machine...try a number between 30000-30030.
   To check if the port you picked is open run:

   .. code::

      $ netstat -ab | grep "<selected port number>"
      # This can take a minute to return anything. If nothing is returned, your selected port is open

After submitting the port forward command as seen above, it will ask for your login information to access the OLCF system. **Leave this terminal window open!**

**Launch the Vampir GUI on your local machine**

Similar to how we have connected Vampir to the VampirServer in the :ref:`previous section, <vampauth>` you will follow the same steps
**except** you will use ``localhost`` for the server name and your ``local machine port`` number you selected.
Press 'Connect' and this should open the authentication window where you will enter your UserID and the :ref:`VampirServer password <vampserpw>`
printed after a successful connection.

.. image:: /images/vampir_remote_local.png
   :width: 400px
   :height: 300px

Once the authentication step is complete, it should open up the remote filesystem for you to navigate to and load
your **.otf2** trace file.


Vampir GUI Demo
==================

Please see the 30-minute video below on `2023 Trace-Based Performance Analysis with
Score-P + Vampir <https://vimeo.com/858484450>`_ to get a brief introduction to
Vampir and Score-P. This recording is taken from the Frontier Training Workshop
(August 2023), Friday, August 25th, 2023, presented by Bill Williams,
TU-Dresden.

.. raw:: html

   <div style="padding:56.25% 0 0 0;position:relative;"><iframe src="https://player.vimeo.com/video/858484450?h=26f33f1775" style="position:absolute;top:0;left:0;width:100%;height:100%;" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe></div><script src="https://player.vimeo.com/api/player.js"></script>
   <p><a href="https://vimeo.com/858484450">2023 Trace-Based Performance Analysis with Score-P + Vampir</a> from <a href="https://vimeo.com/olcf">OLCF</a> on <a href="https://vimeo.com">Vimeo</a>.</p>
