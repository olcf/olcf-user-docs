Spectral Library
----------------

Spectral is a portable and transparent middleware library to enable use of the node-local burst buffers for accelerated application output on Summit. It is used to transfer files from node-local NVMe back to the parallel GPFS file system without the need of the user to interact during the job execution. Spectral runs on the isolated core of each reserved node, so it does not occupy resources and based on some parameters the user could define which folder to be copied to the GPFS. In order to use Spectral, the user has to do the following steps in the submission script:

#. Request Spectral resources instead of NVMe
#. Declare the path where the files will be saved in the node-local NVMe (PERSIST_DIR)
#. Declare the path on GPFS where the files will be copied (PFS_DIR)
#. Execute the script spectral_wait.py when the application is finished in order to copy the files from NVMe to GPFS

The following table shows the differences of executing an application on GPFS, NVMe, and NVMe with Spectral. This example is using one compute node. We copy the executable and input file for the NVMe cases but this is not always necessary, it depends on the application, you could execute the binary from the GPFS and save the output files on NVMe, In the table is the execution command of the binary and take the data back in case that the Spectral library is not used. Adjust your parameters to copy, if necessary, the executable and input files on all the NVMes devices.

+--------------------------------------+----------------------------------------------+----------------------------------------------+
|*Using GPFS* 			       | *Using NVMe*                                 | *Using NVME with Spectral library*           |
+--------------------------------------+----------------------------------------------+----------------------------------------------+
|``#!/bin/bash``		       | ``#!/bin/bash``                              | ``#!/bin/bash``                              |
+--------------------------------------+----------------------------------------------+----------------------------------------------+
|``#BSUB -P xxx``		       |``#BSUB -P xxx``                              |``#BSUB -P xxx``                              |
+--------------------------------------+----------------------------------------------+----------------------------------------------+
|``#BSUB -J NAS-BTIO``		       |``#BSUB -J NAS-BTIO``                         |``#BSUB -J NAS-BTIO``                         |
+--------------------------------------+----------------------------------------------+----------------------------------------------+
|``#BSUB -o nasbtio.o%J``	       |``#BSUB -o nasbtio.o%J``                      |``#BSUB -o nasbtio.o%J``                      |
+--------------------------------------+----------------------------------------------+----------------------------------------------+
|``#BSUB -e nasbtio.e%J``	       |``#BSUB -e nasbtio.e%J``                      |``#BSUB -e nasbtio.e%J``                      |
+--------------------------------------+----------------------------------------------+----------------------------------------------+
|``#BSUB -W 10``		       |``#BSUB -W 10``                               |``#BSUB -W 10``                               |
+--------------------------------------+----------------------------------------------+----------------------------------------------+
|``#BSUB -nnodes 1``		       |``#BSUB -nnodes 1``                           |``#BSUB -nnodes 1``                           |
+--------------------------------------+----------------------------------------------+----------------------------------------------+
| 				       |``#BSUB -alloc_flags nvme``                   |``#BSUB -alloc_flags spectral``               |
+--------------------------------------+----------------------------------------------+----------------------------------------------+
| 				       |                                              |``module load spectral``                      |
+--------------------------------------+----------------------------------------------+----------------------------------------------+
| 				       |                                              |``export PERSIST_DIR=${BBPATH}``              |
+--------------------------------------+----------------------------------------------+----------------------------------------------+
| 				       |                                              |``export PFS_DIR=$PWD/spect/``                |
+--------------------------------------+----------------------------------------------+----------------------------------------------+
| 				       |``export BBPATH=/mnt/bb/$USER/``              |``export BBPATH=/mnt/bb/$USER/``              |
+--------------------------------------+----------------------------------------------+----------------------------------------------+
| 				       |``jsrun -n 1 cp btio ${BBPATH}``              |``jsrun -n 1 cp btio ${BBPATH}``              |
+--------------------------------------+----------------------------------------------+----------------------------------------------+
| 				       |``jsrun -n 1 cp input* ${BBPATH}``            |``jsrun -n 1 cp input* ${BBPATH}``            |
+--------------------------------------+----------------------------------------------+----------------------------------------------+
|``jsrun -n 1 -a 16 -c 16 -r 1 ./btio``|``jsrun -n 1 -a 16 -c 16 -r 1 ${BBPATH}/btio``|``jsrun -n 1 -a 16 -c 16 -r 1 ${BBPATH}/btio``|
+--------------------------------------+----------------------------------------------+----------------------------------------------+
| ``ls -l``			       | ``jsrun -n 1 ls -l ${BBPATH}/``	      | ``jsrun -n 1 ls -l ${BBPATH}/``		     |
+--------------------------------------+----------------------------------------------+----------------------------------------------+
| 				       |``jsrun -n 1 cp ${BBPATH}/* .``               |``spectral_wait.py``                          |
+--------------------------------------+----------------------------------------------+----------------------------------------------+


You could observe that with Spectral library there is no reason to explicitly ask for the data to be copied to GPFS as it is done automatically through the spectral_wait.py script. Also a a log file called spectral.log will be created with information on the files that were copied.
