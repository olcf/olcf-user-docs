.. _scorep:

*****************************************************************************
Scalable Performance Measurement Infrastructure for Parallel Codes (Score-P)
*****************************************************************************

The Score-P instrumenting tool is a scalable and easy-to-use tool suite for profiling, event tracing, 
and online analysis of HPC applications. It has been created in the German BMBF project SILC and
the US DOE project PRIMA. Score-P is developed under a BSD 3-Clause License and governed by a meritocratic governance model.

Webpage: https://www.vi-hps.org/projects/score-p/
Email: support@score-p.org

Score-P is installed with `Program Database Toolkit (PDT)
<https://www.cs.uoregon.edu/research/pdt/home.php>`_ on Summit. PDT is a
framework for analyzing source code written in several programming languages.
Moreover, `Performance Application Programming Interface (PAPI)
<https://icl.utk.edu/papi/>`_ is supported. PAPI counters are used to assess
the CPU performance. In this section, some approaches for profiling and tracing
will be presented.

Automatic Source Code Instrumentation
=====================================

Prefix method
~~~~~~~~~~~~~
.. code::

	CC  = scorep <options> gcc
	CXX = scorep <options> g++ 
	F90 = scorep <options> gfortran

.. code::

	CC = gcc
	..
	tager: target.c
		corep <options> $(CC) -o $@ $^


Wrapper method
~~~~~~~~~~~~~~

.. code::

	SCOREP_WRAPPER=off cmake -DCMAKE_C_COMPILER=scorep-gcc -DCMAKE_CXX_COMPILER=scorep-g++

.. code::

	SCOREP_WRAPPER=off ../configure CC=scorep-gcc CXX=scorep-g++ --disable-dependency-tracking

.. code::

	make SCOREP_WRAPPER_INSTRUMENTER_FLAGS=<options>



Instrumentation Overview
~~~~~~~~~~~~~~~~~~~~~~~~~


The following Score-P options are useful .

+-------------------------+------------------------+----------------+-----------------------------+
| Type of Instrumentation | Instrumenter Switch    | Default value  | Instrumented routines       |
+=========================+========================+================+=============================+
| MPI	                  | | \\-\\-mpp=mpi        | (auto)         | configured by install       |
|                         | | \\-\\-mpp=none       |                |                             |
+-------------------------+------------------------+----------------+-----------------------------+
| SHMEM     		  | | \\-\\-mpp=shmem      | (auto)         | configured by install       |  
|                         | | \\-\\-mpp=none       |                |                             |
+-------------------------+------------------------+----------------+-----------------------------+
| OpenCL    		  | | \\-\\-opencl         | enabled        | configured by install       | 
|                         | | \\-\\-noopencl       |                |                             |
+-------------------------+------------------------+----------------+-----------------------------+
| OpenACC                 | | \\-\\-openacc        | enabled        | configured by install       |  
|                         | | \\-\\-noopenacc      |                |                             |
+-------------------------+------------------------+----------------+-----------------------------+
| CUDA                    | | \\-\\-cuda           | enabled        | configured by install       |
|                         | | \\-\\-nocuda         |                |                             |
+-------------------------+------------------------+----------------+-----------------------------+
| OpenMP                  | | \\-\\-thread=omp/    | (auto)         | all parallel constructs     |
|                         | | \\-\\-thread=none    |                |                             |
|                         | | \\-\\-openmp         |                |                             |
|                         | | \\-\\-noopenmp       |                |                             |
+-------------------------+------------------------+----------------+-----------------------------+
| Pthread                 | | \\-\\-thread=pthread | (auto)         | basic Pthread library calls |
+-------------------------+------------------------+----------------+-----------------------------+
| Compiler                | | \\-\\-compiler       | enabled        | all                         |
|                         | | \\-\\-nocompiler     |                |                             |
+-------------------------+------------------------+----------------+-----------------------------+
| PDT                     | | \\-\\-pdt            | disabled       | all                         |
|                         | | \\-\\-nopdt          |                |                             |
+-------------------------+------------------------+----------------+-----------------------------+
| POMP2                   | | \\-\\-pomp           | disabled       | manually annotated          |
|                         | | \\-\\-nopomp         |                |                             |
+-------------------------+------------------------+----------------+-----------------------------+
| Manual                  | | \\-\\-user           | disabled       | manually annotated          |
|                         | | \\-\\-nouser         |                |                             |
+-------------------------+------------------------+----------------+-----------------------------+



Run-Time Environment Variables
==============================

The following Score-P environment variables may be useful in job submission scripts. See Score-P manual for more information.

+---------------------------------------+----------------------------------+-------------------------------------------------------------------------------------------------------------+
| Variable                		| Default 			   | Description                                                                                                 |
+=======================================+==================================+=============================================================================================================+
| SCOREP_ENABLE_PROFILING 		| TRUE   			   | Enable profiling                                                                                            |
+---------------------------------------+----------------------------------+-------------------------------------------------------------------------------------------------------------+
| SCOREP_ENABLE_TRACING   		| FALSE   			   | Enable tracing                                                                                              |
+---------------------------------------+----------------------------------+-------------------------------------------------------------------------------------------------------------+
| SCOREP_VERBOSE          		| FALSE   			   | Activate verbose mode                                                                                       |
+---------------------------------------+----------------------------------+-------------------------------------------------------------------------------------------------------------+
| SCOREP_TOTAL_MEMORY     		| 16000k  			   | Total memory in bytes per process to be consumed by the measurement system                                  |
+---------------------------------------+----------------------------------+-------------------------------------------------------------------------------------------------------------+
| SCOREP_EXPERIMENT_DIRECTORY           | directory based on current time  | Declare the path with the directory for the data to be saved                                                |
+---------------------------------------+----------------------------------+-------------------------------------------------------------------------------------------------------------+
| SCOREP_OVERWRITE_EXPERIMENT_DIRECTORY |   TRUE    			   | Overwrite an existing experiment directory                                                                  |
+---------------------------------------+----------------------------------+-------------------------------------------------------------------------------------------------------------+
| SCOREP_EXECUTABLE      		|    ""    			   | Full path to the executable if Score-P cannot find it                                                       |
+---------------------------------------+----------------------------------+-------------------------------------------------------------------------------------------------------------+
| SCOREP_PROFILING_MAX_CALLPATH_DEPTH   |    30    			   | Maximum depth of the calltree                                                                               |
+---------------------------------------+----------------------------------+-------------------------------------------------------------------------------------------------------------+
| SCOREP_FILTERING_FILE  		|   ""    			   | A filename with the filter rules                                                                            |
+---------------------------------------+----------------------------------+-------------------------------------------------------------------------------------------------------------+
| SCOREP_METRIC_PAPI      		| ""  				   | PAPI metric names to measure                                                                                |
+---------------------------------------+----------------------------------+-------------------------------------------------------------------------------------------------------------+
| SCOREP_METRIC_PAPI_PER_PROCESS   	|   ""   			   | List of requested PAPI metric names that will be recorded only by first thread of a process                 |
+---------------------------------------+----------------------------------+-------------------------------------------------------------------------------------------------------------+
| SCOREP_MPI_ENABLE_GROUPS 		|  default   			   | |  Options to be declared:				                                                         |
|			   		|				   | |  **all** All MPI functions										 |
|                       		|       			   | |  **cg** Communication and group management 								 |
|                       		|       			   | |  **coll** Collective functions 										 |
|                       		|       			   | |  **default** Includes cg, coll, env, io, p2p, rma, topo, xnonblock 					 |
|                       		|       			   | |  **env** Environmental management   									 |
|                       		|       			   | |  **err** MPI Error handling 										 |
|                       		|       			   | |  **ext** External interface functions 									 |
|                       		|       			   | |  **io** MPI file I/O 											 |
|                       		|       			   | |  **p2p** Peer-to-perr communication 									 |
|                       		|       			   | |  **misc** Miscellaneous 											 |
|                       		|       			   | |  **perf** PControl 											 |
|                       		|       			   | |  **rma** One sided communication 									 |
|                       		|       			   | |  **spawn** Process management 										 |
|                       		|       			   | |  **topo** Topology 											 |
|                       		|       			   | |  **type** MPI datatype functions 								 	 |
|                       		|       			   | |  **xnonblock** Ectended non-blocking events 								 |
|                       		|       			   | |  **xreqtest** Test events for uncompleted requests 							 |
|                       		|       			   | |  **none/no** Disable feature 										 |
+---------------------------------------+----------------------------------+-------------------------------------------------------------------------------------------------------------+
| SCOREP_MPI_MEMORY_RECORDING    	| FALSE 			   |Enable tracing of memory allocations done by calls to MPI_ALLOC_MEM and MPI_FREE_MEM, requires the MISC group|
+---------------------------------------+----------------------------------+-------------------------------------------------------------------------------------------------------------+
| SCOREP_MPI_ONLINE_ANALYSIS  		|  FALSE   			   | Enable online MPI wait states analysis                                                                      |
+---------------------------------------+----------------------------------+-------------------------------------------------------------------------------------------------------------+
| SCOREP_CUDA_ENABLE  			|  no   			   | |  Options to be declared:                                                      				 |
|                        		|    				   | |  **runtime** CUDA runtime API										 |
|                       		|       			   | |  **driver** CUDA driver API 										 |
|                       		|       			   | |  **kernel** CUDA kernels 										 |
|                       		|       			   | |  **kernel_serial** Serialized kernel recording 								 |
|                       		|       			   | |  **kernel_counter** Fixed CUDA kernel metrics   								 |
|                       		|       			   | |  **memcpy** CUDA memory copies 										 |
|                       		|       			   | |  **sync** Record implicit and explicit CUDA synchronization 						 |
|                       		|       			   | |  **idle** GPU compute idle time 										 |
|                       		|       			   | |  **pure_idle** GPU idle time (memory copies are not idle) 						 |
|                       		|       			   | |  **gpumemusage** Record CUDA memory (de)allocations as a counter						 |
|                                       |                                  | |  **references** Record references between CUDA activities						 |
|                                       |                                  | |  **flushatexit** Flush CUDA activity buffer at program exit						 |
|                                       |                                  | |  **default/yes/1**  includes runtime, kernel, memcpy							 |
|                                       |                                  | |  **none/no** Disable feature                                                                              |
+---------------------------------------+----------------------------------+-------------------------------------------------------------------------------------------------------------+
| SCOREP_CUDA_BUFFER  			|  1M   			   | Total memory in bytes for the CUDA record buffer                                                       	 |
+---------------------------------------+----------------------------------+-------------------------------------------------------------------------------------------------------------+
| SCOREP_OPENACC_ENABLE  		|  no   			   |   |   Options to be declared:                                                     				 |
|                        		|       			   |   |   **regions** OpenACC regions										 |
|                       		|       			   |   |   **wait** OpenACC wait operations 									 |
|                       		|       			   |   |   **enqueue** OpenACC enqueue operations 								 |
|                       		|       			   |   |   **device_alloc** OpenACC device memory allocations 							 |
|                       		|       			   |   |   **kernel_properties** Record kernel properties such as the kernel name, gang, worker and vector size  |
|                       		|       			   |   |   **variable_names** Record variable names for OpenACC data allocation and enqueue upload/download 	 |
|                       		|       			   |   |   **default/yes/1** OpenACC regions,enqueue and wait operations 					 |
|                       		|       			   |   |   **none/no** Disable feature 										 |
+---------------------------------------+----------------------------------+-------------------------------------------------------------------------------------------------------------+
| SCOREP_MEMORY_RECORDING  		|  FALSE   			   | Memory (de)allocations are recorded via libc/C++ API                                                        |
+---------------------------------------+----------------------------------+-------------------------------------------------------------------------------------------------------------+

MiniWeather Example Application
================================

Getting the source code
-----------------------

- Connect to Summit and navigate to your project space
- For the following examples, we'll use the MiniWeather application:
  https://github.com/mrnorman/miniWeather

.. code::

	$ git clone https://github.com/mrnorman/miniWeather.git
	$ cd miniWeather/c/
	$ cp Makefile.summit Makefile


Compile the application
------------------------

- We'll use the PGI compiler; this application supports serial, MPI, MPI+OpenMP,
  and MPI+OpenACC

.. code::

	$ module load pgi
	$ module load parallel-netcdf

- Different compilations for Serial, MPI, MPI+OpenMP, and MPI+OpenACC:

.. code::

	$ make serial
	$ make mpi
	$ make openmp
	$ make openacc


Below, we'll look at using Score-P to profile each case.


Modifications
-------------

- Edit the makefile and replace ``mpic++`` with ``scorep --mpp=mpi mpic++``. 
- TAU works with special TAU makefiles to declare what programming models are
  expected from the application:


Instrumenting the serial version of MiniWeather
-----------------------------------------------

For a serial application, we should not use a Makefile with a programming
model such as MPI or OpenMP. However, as the source code for this **specific**
case includes MPI headers that are not excluded during the compilation of the
serial version, we should declare a Makefile with MPI. 

- Edit the makefile and replace ``mpic++`` with ``scorep --mpp=mpi mpic++``

.. code::

	$ module load scorep/6.0_r14595
	$ make serial

If there were no MPI headers, you should edit the Makefile with:

``scorep --mpp=none g++``

If you want to add PDT, then use the option ``--pdt``

