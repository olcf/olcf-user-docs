.. _burst_buffer:

Burst Buffer
=============

NVMe (XFS)
----------

Each compute node on Summit has a \ **N**\ on-\ **V**\ olatile
**Me**\ mory (NVMe) storage device, colloquially known as a "Burst
Buffer" with theoretical performance peak of 2.1 GB/s for writing and
5.5 GB/s for reading. Starting September 24th, 100GB of each NVMe will be reserved for 
NFS cache to help speed access to common libraries. Users will have access to 
an 1500 GB partition of each NVMe. The NVMes could be used to reduce the time that applications
wait for I/O. Using an SSD drive per compute node, the burst buffer will
be used to transfers data to or from the drive before the application
reads a file or after it writes a file. The result will be that the
application benefits from native SSD performance for a portion of its
I/O requests. Users are not required to use the NVMes. Data can also be
written directly to the parallel filesystem.

.. figure:: /images/nvme_arch.jpg
   :align: center

   The NVMes on Summitdev are local to each node.

Current NVMe Usage
~~~~~~~~~~~~~~~~~~

Tools for using the burst buffers are still under development.
Currently, the user will have access to a writeable directory on each
node's NVMe and then explicitly move data to and from the NVMes with
posix commands during a job. This mode of usage only supports
writing file-per-process or file-per-node. It does not support automatic
"n to 1" file writing, writing from multiple nodes to a single file.
After a job completes the NVMes are trimmed, a process
that irreversibly deletes data from the devices, so all desired data
from the NVMes will need to be copied back to the parallel filesystem
before the job ends. This largely manual mode of usage will not be the
recommended way to use the burst buffer for most applications because
tools are actively being developed to automate and improve the NVMe
transfer and data management process. Here are the basic steps for using
the BurstBuffers in their current limited mode of usage:


#. Modify your application to write to /mnt/bb/$USER, a directory that will be created on each NVMe.

#. Modify either your application or your job submission script to copy the desired data from /mnt/bb/$USER back to the parallel filesystem before the job ends.

#. Modify your job submission script to include the ``-alloc_flags NVME``  bsub option. Then on each reserved Burst Buffer node will be available a directory called /mnt/bb/$USER.

#. Submit your bash script or run the application.

#. Assemble the resulting data as needed.

Interactive Jobs Using the NVMe
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The NVMe can be setup for test usage within an interactive job as
follows:

.. code:: 

    bsub -W 30 -nnodes 1 -alloc_flags "NVME" -P project123 -Is bash

The ``-alloc_flags NVME`` option will create a directory
called /mnt/bb/$USER on each requested node's NVMe. The ``/mnt/bb/$USER``
directories will be writeable and readable until the interactive job
ends. Outside of a job ``/mnt/bb/`` will be empty and you will not be able
to write to it.

NVMe Usage Example
~~~~~~~~~~~~~~~~~~

The following example illustrates how to use the burst buffers (NVMes)
by default on Summit. This example uses a hello_world bash script,
called test_nvme.sh, and its submission script, check_nvme.lsf. It is
assumed that the files are saved in the user's Lustre scratch area,
/gpfs/alpine/scratch/$USER/projid, and that the user is operating from
there as well. Do not forget that for all the commands on NVMe, it is
required to use jsrun. **Job submssion script: check_nvme.lsf.** This
will submit a job to run on one node.

.. code:: 

    #!/bin/bash
    #BSUB -P project123
    #BSUB -J name_test
    #BSUB -o nvme_test.o%J
    #BSUB -W 2
    #BSUB -nnodes 1
    #BSUB -alloc_flags NVME

    #Declare your project in the variable
    projid=xxxxx
    cd /gpfs/alpine/scratch/$USER/$projid

   #Save the hostname of the compute node in a file
   jsrun -n 1 echo $HOSTNAME > test_file

   #Check what files are saved on the NVMe, always use jsrun to access the NVMe devices
   jsrun -n 1 ls -l /mnt/bb/$USER/

   #Copy the test_file in your NVMe
   jsrun -n 1 cp test_file /mnt/bb/$USER/

   #Delete the test_file from your local space
   rm test_file

   #Check again what the NVMe folder contains
   jsrun -n 1 ls -l /mnt/bb/$USER/

   #Output of the test_file contents
   jsrun -n 1 cat /mnt/bb/$USER/test_file

   #Copy the file from the NVMe to your local space
   jsrun -n 1 cp /mnt/bb/$USER/test_file .

   #Check the file locally
   ls -l test_file

To run this example: ``bsub ./check_nvme.lsf``.   We could include all the
commands in a script and call this file as jsrun argument in order to
avoid changing numbers of processes for all the jsrun calls. You can see
in the table below the differences of a submission script for executing
an application on GPFS and NVMe. In this case we copy the binary and the
input file on NVMe, but this depends on the application as it is not
always necessary, we can execute the binary on the GPFS and write/read
the data from NVMe if it is supported by the application.

.. role:: raw-html(raw)
    :format: html
     


+---------------------------------------+------------------------------------------------+
| *Using GPFS*          		| *Using NVMe*         				 |
+---------------------------------------+------------------------------------------------+
|               	``#!/bin/bash`` |``#!/bin/bash`` 	     			 |
+---------------------------------------+------------------------------------------------+
| 	 	       ``#BSUB -P xxx`` | ``#BSUB -P xxx``  		   	         |
+---------------------------------------+------------------------------------------------+
|	  	   ``#BSUB -J NAS-BTIO``|``#BSUB -J NAS-BTIO``  			 |
+---------------------------------------+--------------+---------------------------------+
|   	       ``#BSUB -o nasbtio.o%J`` |``#BSUB -o nasbtio.o%J`` 	                 |
+---------------------------------------+---------------+--------------------------------+
|               ``#BSUB -e nasbtio.e%J``|``#BSUB -e nasbtio.e%J``   			 |
+---------------------------------------+------------------------------------------------+
|			``#BSUB -W 10`` |``#BSUB -W 10``    		 	         |
+---------------------------------------+------------------------------------------------+
|		     ``#BSUB -nnodes 1``|``#BSUB -nnodes 1``  	 		 	 |
+---------------------------------------+------------------------------------------------+
| 		    			|``#BSUB -alloc_flags nvme`` 			 |
|					+------------------------------------------------+	
| 	            			|``export BBPATH=/mnt/bb/$USER/``		 |
|					+------------------------------------------------+
| 		    			|``jsrun -n 1 cp btio ${BBPATH}``		 |
|					+------------------------------------------------+
| 		    			|``jsrun -n 1 cp input* ${BBPATH}``		 |
|					+------------------------------------------------+
|``jsrun -n 1 -a 16 -c 16 -r 1 ./btio`` |``jsrun -n 1 -a 16 -c 16 -r 1 ${BBPATH}/btio``  |
|					+------------------------------------------------+
|``ls -l``		`		|``jsrun -n 1 ls -l ${BBPATH}/``		 |
|					+------------------------------------------------+
|					|``jsrun -n 1 cp ${BBPATH}/* .``		 |
+---------------------------------------+------------------------------------------------+

When a user occupies more than one compute node, then is using more NVMe
and the I/O can scale linear. For example in the following plot you can
observe the scalability of the IOR benchmark on 2048 compute nodes on
Summit where the write performance achieves 4TB/s and the read 11,3 TB/s


.. image:: /images/nvme_ior_summit.png
   :align: center

Remember that by default NVMe support one file per MPI
process up to one file per compute node. If users desire a single file
as output from data staged on the NMVe they will need to construct it.
Tools to save automatically checkpoint files from NVMe to GPFS as also
methods that allow automatic n to 1 file writing with NVMe staging are
under development.   Tutorials about NVME:   Burst Buffer on Summit
(`slides <https://www.olcf.ornl.gov/wp-content/uploads/2018/12/summit_workshop_BB_markomanolis.pdf>`__,
`video <https://vimeo.com/306890779>`__) Summit Burst Buffer Libraries
(`slides <https://www.olcf.ornl.gov/wp-content/uploads/2018/12/summit_workshop_BB_zimmer.pdf>`__,
`video <https://vimeo.com/306891012>`__). Below is presented the Spectral library.

