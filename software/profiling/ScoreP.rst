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
~~~~~~~~~~~~~~~~~~~~~~~

- Connect to Summit and navigate to your project space
- For the following examples, we'll use the MiniWeather application:
  https://github.com/mrnorman/miniWeather

.. code::

	$ git clone https://github.com/mrnorman/miniWeather.git
	$ cd miniWeather/c/
	$ cp Makefile.summit Makefile


Compile the application
~~~~~~~~~~~~~~~~~~~~~~~

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


Instrumenting the serial version of MiniWeather
-----------------------------------------------

For a serial application, we should not use a Makefile with a programming
model such as MPI or OpenMP. However, as the source code for this **specific**
case includes MPI headers that are not excluded during the compilation of the
serial version, we should declare a Makefile with MPI. 

- Edit the makefile and replace ``mpic++`` with ``scorep --mpp=mpi mpic++``

.. code::

	$ module load scorep/6.0
	$ make serial

If there were no MPI headers, you should edit the Makefile with:

``scorep --mpp=none g++``

However, as there are MPI headers, we need to declare 

``scorep --mpp=mpi mpic++``

If you want to add PDT, then use the option ``--pdt``

Add to your submission script the Score-P variables that you want to use (or
uncomment them below). By default the Score-P will apply profiling, and not apply tracing.

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


- We can see that 98.2% of the execution time is spent on user functions and only 1.4% on MPI as there is no real MPI calls on serial code, just some calls are not excluded.


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


Instrumenting the MPI version of MiniWeather
--------------------------------------------

Profiling
~~~~~~~~~

For the MPI version, we should use a makefile with MPI. 
Edit the Makefile and declare the compiler for CC.

``scorep --mpp=mpi --pdt mpic++``

.. code::

        $ module load pgi
        $ module load parallel-netcdf
        $ module load scorep/6.0
        $ make mpi

Add to your submission script the Score-P variables that you want to use (or
uncomment them below). By default, the Score-P will apply profiling, and not
tracing.

.. code::

        module load scorep/6.0
        #PAPI metrics

	export SCOREP_METRIC_PAPI=PAPI_TOT_INS,PAPI_TOT_CYC,PAPI_FP_OPS
	export SCOREP_MPI_ENABLE_GROUPS=ALL
	export SCOREP_TOTAL_MEMORY=20MB

        jsrun -n 64 -r 8 -a 1 -c 1 ./miniWeather_mpi

- A new folder is created and we check the results

.. code::

	cd scorep-20191211_1647_1910918433289249
	scorep-score -r profile.cubex > profile.txt
        less profile.txt

	Estimated aggregate size of event trace:                   1071MB
	Estimated requirements for largest trace buffer (max_buf): 17MB
	Estimated memory requirements (SCOREP_TOTAL_MEMORY):       19MB
	(hint: When tracing set SCOREP_TOTAL_MEMORY=19MB to avoid intermediate flushes
 	or reduce requirements using USR regions filters.)

	flt     type max_buf[B]     visits time[s] time[%] time/visit[us]  region
        	 ALL 17,631,831 26,151,351 2624.21   100.0         100.35  ALL
        	 MPI 12,130,086 12,559,329 1908.82    72.7         151.98  MPI
        	 USR  3,249,298  7,822,166  618.97    23.6          79.13  USR
        	 COM  2,343,978  5,769,792   96.41     3.7          16.71  COM
     	      SCOREP         41         64    0.01     0.0          92.71  SCOREP

        	 MPI  4,806,000  3,456,000   13.67     0.5           3.95  MPI_Isend
        	 MPI  4,806,000  3,456,000   11.84     0.5           3.43  MPI_Irecv
        	 MPI  1,404,000  3,456,000  109.38     4.2          31.65  MPI_Waitall
        	 COM  1,404,000  3,456,000   45.78     1.7          13.25  void semi_discrete_step(double *, double *, double *, double, int, double *, double *)
        	 USR    702,000  1,728,000  317.84    12.1         183.94  void compute_tendencies_x(double *, double *, double *)
        	 COM    702,000  1,728,000   31.13     1.2          18.01  void set_halo_values_x(double *)
        	 USR    702,000  1,728,000    3.57     0.1           2.07  void set_halo_values_z(double *)
        	 USR    702,000  1,728,000  289.24    11.0         167.39  void compute_tendencies_z(double *, double *, double *)

- Now that we use MPI, we can observe that 72.7% of the total execution time was MPI calls, there were almost 3.5 million MPI_Isend/MPI_Irecv calls
- Moreover in the first line we are informed that if we activate tracing, the size will be close to 1GB and the miinimum requirement for the memory (SCOREP_TOTAL_MEMORY) that we use already.
- The profile.cubex file can be opened with the cube tool but will present this later


Tracing
~~~~~~~

- You need to activate the tracing variable in tour submission script

.. code::

	export SCOREP_ENABLE_TRACING=true

- Now the new scorep directory includes a file called ``traces.otf2`` and a sub-directory with traces. You can use Vampir to open the otf2 file. 
- For detailed information about using Vampir on Summit and the builds available, please see the `Vampir Software Page <https://www.olcf.ornl.gov/software_package/vampir/>`__.


Instrumenting the MPI+OpenMP version of MiniWeather
----------------------------------------------------


 - Execute the MPI+OpenMP version

Edit the Makefile and declare the compiler for CC.

 ``scorep --mpp=mpi --thread=omp --pdt mpic++``

 .. code::

         $ module load pgi
         $ module load parallel-netcdf
         $ module load scorep/6.0
         $ make openmp

 Add to your submission script the Score-P variables that you want to use (or
 uncomment them below). By default, the Score-P will apply profiling, and not
 tracing.

 .. code::

         module load scorep/6.0

         #PAPI metrics
         export SCOREP_METRIC_PAPI=PAPI_TOT_INS,PAPI_TOT_CYC,PAPI_FP_OPS

         export SCOREP_MPI_ENABLE_GROUPS=ALL
         export SCOREP_TOTAL_MEMORY=20MB
	 export OMP_NUM_THREADS=8

	 jsrun -n 64 -r 8 -a 1 -c 8 "-b packed:8" ./miniWeather_mpi_openmp


- A new folder is created and we check the results

 .. code::

         cd scorep-20191212_1359_1949859062811255
         scorep-score -r profile.cubex > profile.txt
         less profile.txt

	Estimated aggregate size of event trace:                   5GB
	Estimated requirements for largest trace buffer (max_buf): 306MB
	Estimated memory requirements (SCOREP_TOTAL_MEMORY):       322MB
	(hint: When tracing set SCOREP_TOTAL_MEMORY=322MB to avoid intermediate flushes
	 or reduce requirements using USR regions filters.)

 	 flt    type  max_buf[B]      visits time[s] time[%] time/visit[us]  region
          	 ALL 319,855,935 101,660,439 1533.97   100.0          15.09  ALL
        	 OMP 300,410,136  94,018,752 1033.35    67.4          10.99  OMP
        	 MPI  12,130,086   3,141,969  446.00    29.1         141.95  MPI
        	 COM   4,449,978   2,738,448   48.89     3.2          17.85  COM
        	 USR   2,865,694   1,761,254    5.73     0.4           3.25  USR
     	      SCOREP          41          16    0.00     0.0          94.38  SCOREP

        	 OMP  37,584,000   6,912,000   29.55     1.9           4.28  !$omp parallel @miniWeather_mpi_openmp.cpp:213
         	 OMP  18,792,000   3,456,000   15.06     1.0           4.36  !$omp parallel @miniWeather_mpi_openmp.cpp:291
        	 OMP  18,792,000   3,456,000   14.71     1.0           4.26  !$omp parallel @miniWeather_mpi_openmp.cpp:322
        	 OMP  18,792,000   3,456,000   15.10     1.0           4.37  !$omp parallel @miniWeather_mpi_openmp.cpp:236
        	 OMP  18,792,000   3,456,000   14.72     1.0           4.26  !$omp parallel @miniWeather_mpi_openmp.cpp:267
        	 OMP  18,792,000   3,456,000   15.00     1.0           4.34  !$omp parallel @miniWeather_mpi_openmp.cpp:369
		 ...
     	         OMP   5,616,000   3,456,000  278.62    18.2          80.62  !$omp for @miniWeather_mpi_openmp.cpp:236		

- We can observe that OpenMP consumes the 67.4% of the execution tiime and which OMP pragma occupies more time and which line.
- Moreover, the traces now would be 5GB and the memory reuquirements are 322MB per process.

Instrumenting the MPI+OpenACC version of MiniWeather
----------------------------------------------------


 - Edit the Makefile and declare the compiler for CC.

  ``scorep --mpp=mpi --cuda --openacc --pdt mpic++``

  .. code::

          $ module load pgi
          $ module load parallel-netcdf
          $ module load scorep/6.0
          $ make openacc

  Add to your submission script the Score-P variables that you want to use (or
  uncomment them below). By default, the Score-P will apply profiling, and not
  tracing.


  .. code::

           module load scorep/6.0

           #PAPI metrics
           export SCOREP_METRIC_PAPI=PAPI_TOT_INS,PAPI_TOT_CYC,PAPI_FP_OPS

           export SCOREP_MPI_ENABLE_GROUPS=ALL
           export SCOREP_TOTAL_MEMORY=20MB
	   export SCOREP_OPENACC_ENABLE=default

           jsrun -n 6 -r 3 --smpiargs="-gpu" -g 1 ./miniWeather_mpi_openacc


- A new folder is created and we check the results

  .. code::

	  cd scorep-20191217_1015_2906378202661
          scorep-score -r profile.cubex > profile.txt
          less profile.txt

	  Estimated aggregate size of event trace:                   350MB
	  Estimated requirements for largest trace buffer (max_buf): 62MB
	  Estimated memory requirements (SCOREP_TOTAL_MEMORY):       64MB
          (hint: When tracing set SCOREP_TOTAL_MEMORY=64MB to avoid intermediate flushes
          or reduce requirements using USR regions filters.)

	 flt     type max_buf[B]     visits time[s] time[%] time/visit[us]  region
          	  ALL 64,183,583 12,509,267  269.54   100.0          21.55  ALL
     	      OPENACC 40,727,960  8,723,760   64.95    24.1           7.45  OPENACC
                  MPI 12,130,086  1,180,019  170.57    63.3         144.55  MPI
                  USR  6,875,518  1,578,564    5.19     1.9           3.29  USR
                  COM  4,449,978  1,026,918   28.83    10.7          28.07  COM
               SCOREP         41          6    0.00     0.0          93.51  SCOREP

         	  MPI  4,806,000    324,000    1.65     0.6           5.10  MPI_Isend
         	  MPI  4,806,000    324,000    1.29     0.5           3.98  MPI_Irecv
         	  USR  3,410,394    783,342    1.74     0.6           2.22  void hydro_const_theta(double, double &, double &)
         	  USR  3,410,394    783,342    3.41     1.3           4.36  void injection(double, double, double &, double &, double &, double &, double &, double &)
         	  MPI  1,404,000    324,000   11.63     4.3          35.91  MPI_Waitall
         	  COM  1,404,000    324,000    5.22     1.9          16.10  void semi_discrete_step(double *, double *, double *, double, int, double *, double *)
     	      OPENACC  1,404,000    324,000    2.56     0.9           7.90  acc_download@miniWeather_mpi_openacc.cpp:370
     	      OPENACC  1,404,000    324,000    2.72     1.0           8.41  acc_upload@miniWeather_mpi_openacc.cpp:380
     	      OPENACC  1,404,000    324,000    2.32     0.9           7.16  acc_wait@miniWeather_mpi_openacc.cpp:380
     	      OPENACC  1,404,000    324,000    1.60     0.6           4.94  acc_data_enter@miniWeather_mpi_openacc.cpp:220
     	      OPENACC  1,404,000    324,000    2.85     1.1           8.79  acc_compute@miniWeather_mpi_openacc.cpp:220
     	      OPENACC  1,404,000    324,000    2.71     1.0           8.36  acc_launch_kernel@miniWeather_mpi_openacc.cpp:220


- The OpenACC consumes 24.1% of the total execution time 
- We are going to trace the MPI+OpenACC version and we'll adjust the buffer size
- The new submission script will be like the following:

  .. code::

            module load scorep/6.0

            #PAPI metrics
            export SCOREP_METRIC_PAPI=PAPI_TOT_INS,PAPI_TOT_CYC,PAPI_FP_OPS

            export SCOREP_MPI_ENABLE_GROUPS=ALL
            export SCOREP_TOTAL_MEMORY=70MB
            export SCOREP_OPENACC_ENABLE=default
	    export SCOREP_ENABLE_TRACING=true
            export SCOREP_ENABLE_PROFILING=false

            jsrun -n 6 -r 3 --smpiargs="-gpu" -g 1 ./miniWeather_mpi_openacc

- We always declare the SCOREP_TOTAL_MEMORY few MBs over the recommended value just to be sure

Vampir
======

- Conenct to a new terminal with X11 forwarding (-X or -Y)
- Load the vampir module and execute it

.. code::

	module load vampir
	vampir &

- Select "Open Other..." if your trace is not already in the list, then "Local File", go to the folder that the files traces.otf2 is located, select it and click "Open"
- This is the main view

.. image:: /images/vampir_main_view.png
   :align: center

- The red area is the Charts bar and the buttons open various Charts 
- The blue area is the Zoom bar and the colors represent different functionalities that we'll see later
- The orange area is the Timeline Chart and the view can change with the addition of other charts
- The yellow area includes different windows about Function Summary, Contect View, and Function Legend. From the Function Summary we can understand in what commands the colors of the Timeline Chart correspond.

- We can zoom either by selecting an area with the mouse from the Zoom bar or the Timeline chart. This way we observe better if there is something wrong with our code.

.. image:: /images/vampir_zoom.png
   :align: center


- By selecting the Chart of Process Timeline (see arrow) we have the following Chart added 

.. image:: /images/vampir_process_timeline.png
   :align: center

- In this case we can see process 0 and the call stack (7 levels) and if we navigate over the colors with the mouse you can get more information under the Contect View.
- The black circles mean burst messages from MPI.
- The yellow trriangles are related to IO operations


- If we execute right click on the chart area and then "Set Mode" -> "Exclusive", we can see the exclusive time spent on each layer 

.. image:: /images/vampir_process_timeline_exclusive.png
   :align: center

- This way we know in which layer to check for any performance issue.
- Moreover, from the options we can check which process is analyzed.


- Add Summary Timeline by clicking the option that the arrow below indicates

.. image:: /images/vampir_process_summary_timeline.png
   :align: center

- In the new chart we can observe the exclusive time per function group for all the processes. It is clear that in some parts MPI consumes the most of the time and in other parts, OpenACC and CUDA calls.
- We can see various options by right click the mouse cursor on the chart area.


- Add Counter Data Timeline by clicking the option that the arrow below indicates

.. image:: /images/vampir_counter_data_timeline.png
   :align: center

- The new chart will show the first PAPI metric that we declared in the variable **SCOREP_METRIC_PAPI** and we can zoom to see more details
- Moreover, depednign on the architecture some emtrics can indicate more details about the computational efficiency across the timeline
- In this case we see the Flops and with mextri number of operations per second.


- If we execute right click and "Select Metric" then we have the following options

.. image:: /images/vampir_counter_select_metric.png
   :align: center

- By selecting "MPI Latencies" we have the following, which represents the duration of individual MPI calls

.. image:: /images/vampir_counter_mpi_latencies.png
   :align: center

- We can observe if some MPI calls take significant time more than other ones to identify bottlenecks.

- By selecting "Message Data Rate" we have the following, which represents the bytes per second exchanged

.. image:: /images/vampir_counter_message_data_rates.png
   :align: center

- We can close a chart be mocing a mouse over the uper right corner (see arrow) in case we want to add another chart 


- By selecting "Add Performance Radar" (see arrow below) we have the following

.. image:: /images/vampir_performance_radar.png
   :align: center

- This shows for all the processes the Flop operations

- If we execute right click "Set Metric" ->  " Message Data Rate"

.. image:: /images/vampir_performance_radar_menu.png
   :align: center

- We get this chart where with a glimpse of the view we can observe which processes outperform or not compared to other ones. Of course, in some cases this could be considered as expected, depending on the implementation.

.. image:: /images/vampir_performance_radar_data_rate.png
   :align: center

- Select "Add IO Timeline" (see arrow below)

.. image:: /images/vampir_io_timeline.png
   :align: center

- We can see per file all the IO operations, open, write, etc.


- Select "Add Message Summary" (see arrow below) 

.. image:: /images/vampir_message_summary.png
   :align: center

- Down on the right, there is a new chart which shows the number of the messages per message size (12.5	KiB)
- We can change the metric as seen below with right click of the mouse on the corresponding chart area

.. image:: /images/vampir_message_summary_menu.png
   :align: center


- Select "Add Process Summary" (see arrow below)

.. image:: /images/vampir_process_summary.png
   :align: center

- The process summary is usefull to observe the load balance between the processes with a glimpse 

- As we see that process 0 performs different operations, we create 2 clusters with the following procedure

.. image:: /images/vampir_process_summary_menu.png
   :align: center
.. image:: /images/vampir_set_cluster.png
   :align: center
.. image:: /images/vampir_prrocess_sumamry_2_clusters.png
   :align: center

- We can clearly observe the differences between the two groups 


- Select "Add Communication Matrix View" (see arrow below)

.. image:: /images/vampir_communication_matrix.png
   :align: center 

- We can observe the number of the messages exchanged between the threads and their properties as sender/receiver

- By selecting the following menu we can see the maximum message size

.. image:: /images/vampir_communication_matrix_max_message.png
   :align: center

- This is usefull to know how the MPI communication performs based on the eager/rendezvous modes

- By selecting the following menu we can see the maximum transfer time to see which threads perform slower

.. image:: /images/vampir_communication_matrix_max_time.png
   :align: center

- By selecting the following menu we can see the minimum data rate for the communication

.. image:: /images/vampir_communication_matrix_min_data_rate.png
   :align: center


- Select "Add I/O Summary" (see arrow below)

.. image:: /images/vampir_io_summary.png
   :align: center

- We can see the I/O operations per each file

- We select from the menu the operations type to see also the numbers per operation type

.. image:: /images/vampir_io_summary_operations.png
   :align: center

- Select "Add Call Tree" (see arrow below)

.. image:: /images/vampir_call_tree.png
   :align: center

- Now we can see the call tree and the duration for each call

Advanced Topics
===============

Disable instrumentation of OpenMP group
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the instrumentation overhead is coming from one OpenMP call, which is not related to performance analysis, such as OpenMP atomic call, we can compile 
the application thus to disable the instrumentation of specific OpenMP group calls. Score-P is using Opari2 to instrument OpenMP and hybrid codes. The pattern is

.. code::

  --opari=<parameter-list>

To disable OpenMP directive, group, etc:

.. code::
  
  --opari=--disable=omp[:directive|group,...]

Thus we compile an MPI+OpenMP application as follows:

.. code::

   make PREP="scorep --mpp=mpi --thread=omp --opari="--disable=omp:atomic" "

where ``$PREP`` is declared in the Makefile 

The OpenMP atomic call will be executed, but it will not be instrumented, thus if this call causes the overhead, it will be decreased.

Fix compilation issue
~~~~~~~~~~~~~~~~~~~~~
