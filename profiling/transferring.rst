******************
Transferring Data
******************

Using common terminal tools
============================

In general, when transferring data into or out of the OLCF from the command
line, it's best to initiate the transfer from outside the OLCF. If moving many
small files, it can be beneficial to compress them into a single archive file,
then transfer just the one archive file. 

``scp`` and ``rsync`` are available for remote transfers.

* ``scp`` - secure copy (remote file copy program)

	* Sending a file to OLCF

	.. code::

   	   scp yourfile $USER@dtn.ccs.ornl.gov:/path/


	* Retrieving a file from OLCF

	.. code::

   	   scp $USER@dtn.ccs.ornl.gov:/path/yourfile .


	* Sending a directory to OLCF

	.. code::

   	   scp -r yourdirectory $USER@dtn.ccs.ornl.gov:/path/


* ``rsync`` - a fast, versatile, remote (and local) file-copying tool


	* Sync a directory named ``mydir`` from your local system to the OLCF

	.. code::

   	   rsync -avz mydir/ $USER@dtn.ccs.ornl.gov:/path/


	where:

  		* ``a`` is for archive mode\
  		* ``v`` is for verbose mode\
  		* ``z`` is for compressed mode\


	* Sync a directory from the OLCF to a local directory

	.. code::

   	   rsync -avz  $USER@dtn.ccs.ornl.gov:/path/dir/ mydir/

        * Transfer data and show progress while transferring

        .. code::

           rsync -avz --progress mydir/ $USER@dtn.ccs.ornl.gov:/path/

	* Include files or directories starting with T and exclude all others

        .. code::

           rsync -avz --progress --include 'T*' --exclude '*' mydir/ $USER@dtn.ccs.ornl.gov:/path/

	* If the file or directory exists at the target but not on the source, then delete it

        .. code::

           rsync -avz --delete $USER@dtn.ccs.ornl.gov:/path/ .

	* Transfer only the files that are smaller than 1MB

        .. code::

           rsync -avz --max-size='1m' mydir/ $USER@dtn.ccs.ornl.gov:/path/

	* If you want to verify the behavior is as intended, execute a dry-run

        .. code::

           rsync -avz --dry-run mydir/ $USER@dtn.ccs.ornl.gov:/path/

See the manual pages for more information:

.. code::

    $ man scp
    $ man rsync


* Differences:
	* ``scp`` cannot continue if it is interrupted. ``rsync`` can.
	* ``rsync`` is optimized for performance.
	* By default, ``rsync`` checks if the transfer of the data was successful.


Using Globus from your local machine
=====================================

Globus is most frequently used to facilitate data transfer between two
institutional filesystems. However, it can also be used to facilitate data
transfer involving an individual workstation or laptop. The following
instructions demonstrate creating a local Globus endpoint, and initiating a
transfer from it to the OLCF's Alpine GPFS filesystem.

- Visit https://www.globus.org/globus-connect-personal and Install Globus
  Connect Personal, it is available for Windows, Mac, and Linux.

- Make note of the endpoint name given during setup. In this example, the
  endpoint is *laptop_gmarkom*.

- When the installation has finished, click on the Globus icon and select *Web:
  Transfer Files* as below

.. image:: /images/globus_personal1.png
   :align: center

- Globus will ask you to login. If your institution does not have an
  organizational login, you may choose to either *Sign in with Google* or *Sign
  in with ORCiD iD*.

.. image:: /images/globus_google.png
   :align: center

- In the main Globus web page, select the two-panel view, then set the source
  and destination endpoints. (Left/Right order does not matter)

.. image:: /images/globus_laptop_summit.png
   :align: center

- Next, navigate to the appropriate source and destination paths to select the
  files you want to transfer. Click the "Start" button to begin the transfer.

.. image:: /images/globus_laptop_transfer.png
   :align: center

- An activity report will appear, and you can click on it to see the status of
  the transfer.

.. image:: /images/globus_laptop_activity.png
   :align: center


-  Various information about the transfer is shown in the activity report. You
   will receive an email once the transfer is finished, including if it fails
   for any reason.

.. image:: /images/globus_laptop_activity_done.png
   :align: center
