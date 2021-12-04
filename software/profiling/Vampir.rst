.. _vampir:

.. image:: /images/vampir_logo.png
   :align: left
   :width: 230px
   :height: 130px

|
|
|
|
|
|

************************************
Vampir
************************************

Overview
=========

Vampir is a software performance visualizer focused on highly parallel applications. It presents a unified view on an application run
including the use of programming paradigms like MPI, OpenMP, PThreads, CUDA, OpenCL and OpenACC.
It also incorporates file I/O, hardware performance counters and other performance data sources.
Various interactive displays offer detailed insight into the performance behavior of the analyzed application.
Vampir's scalable analysis server and visualization engine enable interactive navigation of large amounts of performance data.
Score-P and TAU generate OTF2 trace files for Vampir to visualize.


Usage
=======

Vampir can be run a few different ways depending on a couple of factors. If you have a large trace file it
would benefit from utilizing VampirServer to process the trace file with the systems compute power
while reverse connected to the Vampir GUI. If the trace file is small enough, it would do just fine viewing on a
login node or your local machine.

.. _vamps:

``Vampirserver`` is the backend software component that can run across multiple compute nodes taking advantage
of the machines memory, this in turn provides a peak performance for viewing large trace files.

.. Note:: Vampirserver does not take advantage of GPU components


This page will go through the 3 different types of connections available for using Vampir on Summit.

For logging onto Summit you will need to specify ``-X`` as part of your ``SSH`` command, this will
activate the `x11 forwarding <https://docs.olcf.ornl.gov/connecting/index.html#x11-forwarding>`_ so you can launch a GUI on Summit. Please visit this link if you need more
information for logging onto `Summit <https://docs.olcf.ornl.gov/systems/summit_user_guide.html#connecting>`_

.. code::

   $ ssh -X <USERID>@summit.olcf.ornl.gov


Vampir on a Login Node
======================

.. Warning::

   Running Vampir on a login node is best suited for small trace files.


.. image:: /images/vampir_login_gui.png
   :align: left
   :width: 280px
   :height: 125px

|
|
|
|
|
|

After logging onto Summit, execute the series of commands below:

.. code::

   $ module load vampir

   $ vampir &

From here you can load a file resident on the file system.

.. image:: /images/vampir_splash_screen_file_selection.png
   :align: left
   :width: 300px
   :height: 200px

|
|
|
|
|
|
|
|
|




Vampir Using Vampirserver
=========================


.. Tip::

   This connection method is the better option for larger trace files


.. image:: /images/vampir_login_node_connect_to_compute.png
   :align: left
   :width: 350px
   :height: 125px

|
|
|
|
|
|

After connecting to `Summit <https://docs.olcf.ornl.gov/systems/summit_user_guide.html#connecting>`_ you will need to load the Vampir module
and start the :ref:`Vampirserver. `<vamps>`

.. code::

   $ module load vampir

   $ vampirserver start -- -P <projectID> -w <walltime> -q <queue>

   #Example: vampirserver start -- -P 123456 -w 60 -q debug

.. _vampserpw:

.. attention:: Successful Vampirserver startup message should appear in terminal window. You will need this information!

 | [Test@login5.summit ~]$ vampirserver start  - - -P 123456 -w 60 -q debug
 | Launching VampirServer...
 | Submitting LSF batch job (this might take a while)...
 | Warning: more than 1 task/rank assigned to a core
 | VampirServer 9.11.1 OLCF (4626dba5)
 | Licensed to ORNL
 | Running 4 analysis processes... (abort with vampirserver stop 10102)
 | User: Test
 | Password: XXXXXXXXXXXX
 | VampirServer <10102> listens on: h50n05:30040

----------------------------------------------------------------------


Launch the Vampir GUI
---------------------
.. code::

   $ vampir &

.. _vampauth:

Once the GUI has opened, you will need to connect to the Vampirserver using the
``Remote File`` option as shown below. **If there is a 'recent files' window open, select 'open other'.**
Enter the ``node ID`` and the ``port`` number and press 'Connect'.


.. image:: /images/vampir_open_remote_location.png
   :align: left
   :width: 800px
   :height: 300px

|
|
|
|
|
|
|
|
|
|
|
|
|

When the server authentication window pops up, you will need to enter your ``USERID``
& the :ref:`Vampirserver password <vampserpw>` that was printed on the terminal screen. Once authenticated, you will be able to navigate through the filesystem to your **.otf2** files

.. image:: /images/vampir_server_auth.png
   :align: left
   :width: 400px
   :height: 300px


|
|
|
|
|
|
|
|
|
|
|
|
|
|

Vampir Tunneling to Vampirserver
===========================================

.. image:: /images/vampir_reverse_connect_gui_to_compute.png
   :align: left
   :width: 350px
   :height: 125px

|
|
|
|
|
|

.. Tip::

   This connection method is more complex than the other 2 methods, however it also can provide a more optimal experience for very large trace files.



.. attention::

   ``This method will require you to have a local copy of the Vampir GUI already installed on your machine.``

   If you do not have a local copy, please reach out to the help desk at help@olcf.ornl.gov for instructions on getting a local copy.

Similar to the previous methods outlined above, you will start by connecting to `Summit <https://docs.olcf.ornl.gov/systems/summit_user_guide.html#connecting>`_.
Once connected you will then need to start the :ref:`Vampirserver. <vamps>`

.. code::

   $ module load vampir

   #Start the VampirServer

   $ vampirserver start -- -P <projectID> -w <walltime> -q <queue>

After the Vampirserver is started successfully, you will need the information printed on the :ref:`terminal window. <vampserpw>`
That includes:

* Node ID
* Port Number
* password


Once the Vampirsever is started, in a **fresh** terminal window on your **Local** machine you can then initiate the
port forward command. This will open a secure tunnel from your local machine to the backend server running Vampirserver.

**Port Forwarding**

.. code::

   SSH -L <localport>:<Node ID>:<Remote port>  <USERID>$summit.olcf.ornl.gov

.. tip::

   The local port number can be any unused port number on your local machine...try a number between30000-30030.

   To check if the port you picked is open run:

   .. code::

      $ netstat -ab | grep "<selected port number>"

    #This can take a minute to return anything. If nothing is returned, your selected port is open

After submitting the port forward command, it will ask for your login password to access Summit. **Leave this terminal window open!**

**Launch the Vampir GUI on your local machine**

Similar to how we have connected Vampir to the Vampirserver in the :ref:`previous section, <vampauth>` you will follow the same steps
**except** you will use ``localhost`` for the server name and your ``local machine port`` number you selected.
Press 'Connect' and this should open the authentication window where you will enter your UserID and the :ref:`Vampirserver password <vampserpw>`
printed after a successful connection.

.. image:: /images/vampir_remote_local.png
   :align: left
   :width: 400px
   :height: 300px

|
|
|
|
|
|
|
|
|
|
|
|
|

Once the authentication step is complete, it should open up the remote filesystem for you to navigate to and load
your **.otf2** trace file.

Vampir GUI Demo
==================

Please see the provided video below to get a brief demo of the Vampir GUI provided by TU-Dresden and presented by Ronny Brendel.

.. Tip:: You can skip ahead to around the 22 minute mark!

.. raw:: html

   <div style="padding:56.25% 0 0 0;position:relative;"><iframe src="https://player.vimeo.com/video/285908215?h=26f33f1775" style="position:absolute;top:0;left:0;width:100%;height:100%;" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe></div><script src="https://player.vimeo.com/api/player.js"></script>
   <p><a href="https://vimeo.com/285908215">2018 Score-P / Vampir Workshop</a> from <a href="https://vimeo.com/olcf">OLCF</a> on <a href="https://vimeo.com">Vimeo</a>.</p>
   <p>This recording is from the 2018 Score-P / Vampir workshop that took place at ORNL on August 17, 2018. In the video, Ronny Brendel gives an introduction to the Score-P and Vampir tools, which are often used together to collect performance profiles/traces from an application and visualize the results.</p>
