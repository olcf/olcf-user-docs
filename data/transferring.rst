******************
Transferring Data
******************

Data Transfer
===============


Using well know terminal tools
------------------------------

Overall, when you want to transfer data from outside OLCF to inside, or the opposite, with a terminal command,
start the transfer from outside OLCF. Moreover, if you have many small files, then better compress them into one
archive file and transfer this file. However, everything depends on the total size, maybe better to split to a few large files

``scp`` and ``rsync`` are available on Summit for remote transfers.

* SCP 

	* Sending a file to OLCF:

	.. code::

   	   scp yourfile $USER@dtn.ccs.ornl.gov:/path/


	* Retrieving a file from OLCF

	.. code::

   	   scp $USER@dtn.ccs.ornl.gov:/path/yourfile .


	* Sending a directory to OLCF:

	.. code::

   	   scp -r yourdirectory $USER@dtn.ccs.ornl.gov:/path/


* Rsync


	* Sync a folder called mydir from your local system to OLCF:

	.. code::

   	   rsync -avz mydir/ $USER@dtn.ccs.ornl.gov:/path/


	where:

  		* a is for archive mode\
  		* v is for verbose mode\
  		* z is for compressed mode\

	If any file exists already, then only it's difference will be sent

	* Sync a folder from OLCF to a local folder

	.. code::

   	   rsync -avz  $USER@dtn.ccs.ornl.gov:/path/dir/ mydir/

	* Transfer data over shh for secure connection

        .. code::

           rsync -avze ssh  mydir/ $USER@dtn.ccs.ornl.gov:/path/

        * Transfer data over shh for secure connection and show progress while transferring

        .. code::

           rsync -avze ssh --progress mydir/ $USER@dtn.ccs.ornl.gov:/path/

	* Include files or directories starting with T and exclude the rest ones

        .. code::

           rsync -avze ssh --progress --include 'T*' --exclude '*' mydir/ $USER@dtn.ccs.ornl.gov:/path/

	* If the file or directory exists at the targer but not not on the source, then delete it

        .. code::

           rsync -avz --delete $USER@dtn.ccs.ornl.gov:/path/ .

	* Transfer only the files that are smaller than 1MB

        .. code::

           rsync -avz --max-size='1m' mydir/ $USER@dtn.ccs.ornl.gov:/path/

	* If you are not sure if the command could create some problems, execute a dry-run

        .. code::

           rsync -avz --dry-run mydir/ $USER@dtn.ccs.ornl.gov:/path/

For more informaiton execute:

.. code::

   man scp
   man rsync


How to use Globus from my laptop
--------------------------------

Many users would like to transfer their data from or to Summit through Globus,
but their institute does not provide a globus infrastructure. In the following
instructions, you can learn how to create your own Globus endpoint. We don't
know if or when globus will not support this approach anymore.

  Follow these steps:

- Visit https://www.globus.org/globus-connect-personal and Install Globus
  Connect Personal, it is available foe Windows, Mac, and Linux

- Selecting the appropriate link there are detailed instructions about the
  installation, for example, for Mac:
  https://docs.globus.org/how-to/globus-connect-personal-mac/
- Remember the name of the endpoint that you declared, in this example, the
  endpoint is *laptop_gmarkom*

- When the installation has finished, click on the globus icon and select *Web:
  Transfer Files* as below

.. image:: /images/globus_personal1.png
   :align: center

- Globus will ask you to login, choose the *Sign in with Google*

.. image:: /images/globus_google.png
   :align: center

- Now you are in the main globus web page, we select two panels (up right), we
  declare left the endpoint of the laptop and on the right the *OLCF DTN* (the
  order does not matter) and

.. image:: /images/globus_laptop_summit.png
   :align: center

- Then navigate to the appropriate paths to select the files you want to tranfer

.. image:: /images/globus_laptop_transfer.png
   :align: center

- Then an activity report will appear and you can click on it to see
   the status. When the transfer is finished or failed, you will receive
   an email

.. image:: /images/globus_laptop_activity.png
   :align: center


-  You can see the status when you click to the activity report

.. image:: /images/globus_laptop_activity_done.png
   :align: center
