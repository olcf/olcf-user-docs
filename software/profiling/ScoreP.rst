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

However, as there are MPI headers, we need to declare 

``scorep --mpp=mpi mpic++``

If you want to add PDT, then use the option ``--pdt``

Add to your submission script the Score-P variables that you want to use (or
uncomment them below). By default the TAU will apply profiling, and not apply tracing.

.. code::

        #PAPI metrics
	export SCOREP_METRIC_PAPI=PAPI_TOT_INS,PAPI_TOT_CYC,PAPI_FP_OPS

	export SCOREP_MPI_ENABLE_GROUPS=ALL
	export SCOREP_TOTAL_MEMORY=20MB

        time jsrun -n 1 -r 1 -a 1 -c 1 -g 1  ./miniWeather_serial


- When the execution finishes, one directory is created named ``scorep-<date>_<time>_<runid>``

- For example we can see the contents of the created directory:

.. code::

	ls scorep-20191210_1435_1862594527919600
	MANIFEST.md
	profile.cubex
	scorep.cfg

- Check the performance data

.. code::

	cd scorep-20191210_1435_1862594527919600
	scorep-score -r profile.cubex > profile.txt
	less profile.txt

	Estimated aggregate size of event trace:                   1057kB
	Estimated requirements for largest trace buffer (max_buf): 1057kB
	Estimated memory requirements (SCOREP_TOTAL_MEMORY):       4097kB
	(hint: When tracing set SCOREP_TOTAL_MEMORY=4097kB to avoid intermediate flushes
	 or reduce requirements using USR regions filters.)

	flt     type max_buf[B] visits time[s] time[%] time/visit[us]  region
        	ALL  1,081,567 35,754   70.08   100.0        1959.93  ALL
         	MPI    964,448 31,250    0.98     1.4          31.36  MPI
         	USR    117,026  4,501   68.79    98.2       15283.49  USR
         	COM         52      2    0.30     0.4      152111.97  COM
      	      SCOREP        41      1    0.00     0.0          65.14  SCOREP

         MPI    655,200 25,200    0.05     0.1           1.83  MPI_Get_address
         USR    117,026  4,501   68.79    98.2       15283.49  perform_timestep(double*, double*, double*, double*, double)
         MPI     60,400    604    0.45     0.6         739.90  MPI_File_write_at_all
         MPI     51,340    755    0.00     0.0           3.49  MPI_Allreduce
         MPI     45,400    454    0.01     0.0          13.39  MPI_File_write_at


- We can see that 98.2% of the execution time is spent on user functions and only 1.4% on MPI.


Explanation
~~~~~~~~~~~

+-------------------------+----------------------------------------------------+
| Score-P Region Type Key |  Description	   			       |
+=========================+====================================================+
| COM                     | user functions found on callstack to other regions |
+-------------------------+----------------------------------------------------+
| CUDA                    | CUDA API & kernels     			       |
+-------------------------+----------------------------------------------------+
| MEMORY                  | Memory alloc/dealloc     			       |
+-------------------------+----------------------------------------------------+
| MPI                     | All MPI functions                                  |
+-------------------------+----------------------------------------------------+
| OMP                     | OpenMP constructs      			       |
+-------------------------+----------------------------------------------------+
| OPENACC                 | OpenACC API & kernels  			       |
+-------------------------+----------------------------------------------------+
| PTHREAD                 | all pthread functions     			       |
+-------------------------+----------------------------------------------------+
| SCOREP                  | Score-P instrumentation 			       |
+-------------------------+----------------------------------------------------+
| SHMEM                   | All SHMEM functions     			       |
+-------------------------+----------------------------------------------------+
| USR                    | User fucntions not found in COM   		       |
+-------------------------+----------------------------------------------------+


We can observe the percentage of each type consumes during the execution of the serial version of MiniWeather


- Repeat the previous procedure but activate PDT, instead of  ``scorep --mpp=mpi mpic++``, declare ``scorep --mpp=mpi --pdt mpic++``

- The the output of the profiling data are:

.. code::

	Estimated aggregate size of event trace:                   13MB
	Estimated requirements for largest trace buffer (max_buf): 13MB
	Estimated memory requirements (SCOREP_TOTAL_MEMORY):       15MB
	(hint: When tracing set SCOREP_TOTAL_MEMORY=15MB to avoid intermediate flushes
	 or reduce requirements using USR regions filters.)

	flt     type max_buf[B]  visits time[s] time[%] time/visit[us]  region
        	 ALL 13,197,645 501,757   71.84   100.0         143.19  ALL
         	 USR 12,229,152 470,352   70.12    97.6         149.08  USR
         	 MPI    964,448  31,250    1.03     1.4          32.86  MPI
        	 COM      4,004     154    0.70     1.0        4535.33  COM
     	      SCOREP         41       1    0.00     0.0          81.92  SCOREP

         USR  4,975,282 191,357    0.38     0.5           2.00  void hydro_const_theta(double, double &, double &)
         USR  4,975,282 191,357    0.75     1.0           3.92  void injection(double, double, double &, double &, double &, double &, double &, double &)
         USR    702,156  27,006    1.34     1.9          49.50  void semi_discrete_step(double *, double *, double *, double, int, double *, double *)
         MPI    655,200  25,200    0.05     0.1           1.84  MPI_Get_address
         USR    351,078  13,503   33.22    46.2        2460.04  void compute_tendencies_x(double *, double *, double *) 
         USR    351,078  13,503    0.05     0.1           3.74  void set_halo_values_x(double *)
         USR    351,078  13,503    0.04     0.1           3.26  void set_halo_values_z(double *)
         USR    351,078  13,503   34.23    47.6        2535.23  void compute_tendencies_z(double *, double *, double *)
         USR    117,026   4,501    0.10     0.1          22.31  void perform_timestep(double *, double *, double *, double *, double)

- We can see more insight details for each routine of the code.


