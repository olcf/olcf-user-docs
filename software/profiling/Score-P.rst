.. _scorep:

*******
Score-P
*******

The Score-P (Scalable Performance Measurement Infrastructure for Parallel
Codes) instrumenting tool is a scalable and easy-to-use tool suite for
profiling, event tracing, and online analysis of HPC applications. It has been
created in the German BMBF project SILC and the US DOE project PRIMA. Score-P
is developed under a BSD 3-Clause License and governed by a meritocratic
governance model.

| Website: https://www.vi-hps.org/projects/score-p/
| Email: support@score-p.org

Score-P is installed with `Program Database Toolkit (PDT)
<https://www.cs.uoregon.edu/research/pdt/home.php>`_ on Summit. PDT is a
framework for analyzing source code written in several programming languages.
Moreover, `Performance Application Programming Interface (PAPI)
<https://icl.utk.edu/papi/>`_ is supported. PAPI counters are used to assess
CPU performance. In this section, some approaches for profiling and tracing
will be presented.

Automatic Source Code Instrumentation
=====================================

Prefix method
~~~~~~~~~~~~~

In this approach we have to edit the Makefile and add the corresponding commands declarations.

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

In this approach we do not need to edit any file as we use CMake. Some times only one of the methods works.

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
| MPI                     | | ``--mpp=mpi``        | (auto)         | configured by install       |
|                         | | ``--mpp=none``       |                |                             |
+-------------------------+------------------------+----------------+-----------------------------+
| SHMEM                   | | ``--mpp=shmem``      | (auto)         | configured by install       |  
|                         | | ``--mpp=none``       |                |                             |
+-------------------------+------------------------+----------------+-----------------------------+
| OpenCL                  | | ``--opencl``         | enabled        | configured by install       | 
|                         | | ``--noopencl``       |                |                             |
+-------------------------+------------------------+----------------+-----------------------------+
| OpenACC                 | | ``--openacc``        | enabled        | configured by install       |  
|                         | | ``--noopenacc``      |                |                             |
+-------------------------+------------------------+----------------+-----------------------------+
| CUDA                    | | ``--cuda``           | enabled        | configured by install       |
|                         | | ``--nocuda``         |                |                             |
+-------------------------+------------------------+----------------+-----------------------------+
| OpenMP                  | | ``--thread=omp``/    | (auto)         | all parallel constructs     |
|                         | | ``--thread=none``    |                |                             |
|                         | | ``--openmp``         |                |                             |
|                         | | ``--noopenmp``       |                |                             |
+-------------------------+------------------------+----------------+-----------------------------+
| Pthread                 | | ``--thread=pthread`` | (auto)         | basic Pthread library calls |
+-------------------------+------------------------+----------------+-----------------------------+
| Compiler                | | ``--compiler``       | enabled        | all                         |
|                         | | ``--nocompiler``     |                |                             |
+-------------------------+------------------------+----------------+-----------------------------+
| PDT                     | | ``--pdt``            | disabled       | all                         |
|                         | | ``--nopdt``          |                |                             |
+-------------------------+------------------------+----------------+-----------------------------+
| POMP2                   | | ``--pomp``           | disabled       | manually annotated          |
|                         | | ``--nopomp``         |                |                             |
+-------------------------+------------------------+----------------+-----------------------------+
| Manual                  | | ``--user``           | disabled       | manually annotated          |
|                         | | ``--nouser``         |                |                             |
+-------------------------+------------------------+----------------+-----------------------------+



Run-Time Environment Variables
==============================

The following Score-P environment variables may be useful in job submission scripts. See Score-P manual for more information.

+---------------------------------------+----------------------------------+-------------------------------------------------------------------------------------------------------------+
| Variable                              | Default                          | Description                                                                                                 |
+=======================================+==================================+=============================================================================================================+
| SCOREP_ENABLE_PROFILING               | TRUE                             | Enable profiling                                                                                            |
+---------------------------------------+----------------------------------+-------------------------------------------------------------------------------------------------------------+
| SCOREP_ENABLE_TRACING                 | FALSE                            | Enable tracing                                                                                              |
+---------------------------------------+----------------------------------+-------------------------------------------------------------------------------------------------------------+
| SCOREP_VERBOSE                        | FALSE                            | Activate verbose mode                                                                                       |
+---------------------------------------+----------------------------------+-------------------------------------------------------------------------------------------------------------+
| SCOREP_TOTAL_MEMORY                   | 16000k                           | Total memory in bytes per process to be consumed by the measurement system                                  |
+---------------------------------------+----------------------------------+-------------------------------------------------------------------------------------------------------------+
| SCOREP_EXPERIMENT_DIRECTORY           | directory based on current time  | Declare the path with the directory for the data to be saved                                                |
+---------------------------------------+----------------------------------+-------------------------------------------------------------------------------------------------------------+
| SCOREP_OVERWRITE_EXPERIMENT_DIRECTORY | TRUE                             | Overwrite an existing experiment directory                                                                  |
+---------------------------------------+----------------------------------+-------------------------------------------------------------------------------------------------------------+
| SCOREP_EXECUTABLE                     | ""                               | Full path to the executable if Score-P cannot find it                                                       |
+---------------------------------------+----------------------------------+-------------------------------------------------------------------------------------------------------------+
| SCOREP_PROFILING_MAX_CALLPATH_DEPTH   | 30                               | Maximum depth of the calltree                                                                               |
+---------------------------------------+----------------------------------+-------------------------------------------------------------------------------------------------------------+
| SCOREP_FILTERING_FILE                 | ""                               | A filename with the filter rules                                                                            |
+---------------------------------------+----------------------------------+-------------------------------------------------------------------------------------------------------------+
| SCOREP_METRIC_PAPI                    | ""                               | PAPI metric names to measure                                                                                |
+---------------------------------------+----------------------------------+-------------------------------------------------------------------------------------------------------------+
| SCOREP_METRIC_PAPI_PER_PROCESS        | ""                               | List of requested PAPI metric names that will be recorded only by first thread of a process                 |
+---------------------------------------+----------------------------------+----------------+--------------------------------------------------------------------------------------------+
| SCOREP_MPI_ENABLE_GROUPS              | default                          |  **Value**     | **Description**                                                                            |
|                                       |                                  +----------------+--------------------------------------------------------------------------------------------+
|                                       |                                  |  ``all``       | All MPI functions                                                                          |
|                                       |                                  +----------------+--------------------------------------------------------------------------------------------+
|                                       |                                  |  ``cg``        | Communication and group management                                                         |
|                                       |                                  +----------------+--------------------------------------------------------------------------------------------+
|                                       |                                  |  ``coll``      | Collective functions                                                                       |
|                                       |                                  +----------------+--------------------------------------------------------------------------------------------+
|                                       |                                  |  ``default``   | Includes cg, coll, env, io, p2p, rma, topo, xnonblock                                      |
|                                       |                                  +----------------+--------------------------------------------------------------------------------------------+
|                                       |                                  |  ``env``       | Environmental management                                                                   |
|                                       |                                  +----------------+--------------------------------------------------------------------------------------------+
|                                       |                                  |  ``err``       | MPI Error handling                                                                         |
|                                       |                                  +----------------+--------------------------------------------------------------------------------------------+
|                                       |                                  |  ``ext``       | External interface functions                                                               |
|                                       |                                  +----------------+--------------------------------------------------------------------------------------------+
|                                       |                                  |  ``io``        | MPI file I/O                                                                               |
|                                       |                                  +----------------+--------------------------------------------------------------------------------------------+
|                                       |                                  |  ``p2p``       | Peer-to-perr communication                                                                 |
|                                       |                                  +----------------+--------------------------------------------------------------------------------------------+
|                                       |                                  |  ``misc``      | Miscellaneous                                                                              |
|                                       |                                  +----------------+--------------------------------------------------------------------------------------------+
|                                       |                                  |  ``perf``      | PControl                                                                                   |
|                                       |                                  +----------------+--------------------------------------------------------------------------------------------+
|                                       |                                  |  ``rma``       | One sided communication                                                                    |
|                                       |                                  +----------------+--------------------------------------------------------------------------------------------+
|                                       |                                  |  ``spawn``     | Process management                                                                         |
|                                       |                                  +----------------+--------------------------------------------------------------------------------------------+
|                                       |                                  |  ``topo``      | Topology                                                                                   |
|                                       |                                  +----------------+--------------------------------------------------------------------------------------------+
|                                       |                                  |  ``type``      | MPI datatype functions                                                                     |
|                                       |                                  +----------------+--------------------------------------------------------------------------------------------+
|                                       |                                  |  ``xnonblock`` | Ectended non-blocking events                                                               |
|                                       |                                  +----------------+--------------------------------------------------------------------------------------------+
|                                       |                                  |  ``xreqtest``  | Test events for uncompleted requests                                                       |
|                                       |                                  +----------------+--------------------------------------------------------------------------------------------+
|                                       |                                  |  ``none/no``   | Disable feature                                                                            |
+---------------------------------------+----------------------------------+----------------+--------------------------------------------------------------------------------------------+
| SCOREP_MPI_MEMORY_RECORDING           | FALSE                            |Enable tracing of memory allocations done by calls to MPI_ALLOC_MEM and MPI_FREE_MEM, requires the MISC group|
+---------------------------------------+----------------------------------+-------------------------------------------------------------------------------------------------------------+
| SCOREP_MPI_ONLINE_ANALYSIS            |  FALSE                           | Enable online MPI wait states analysis                                                                      |
+---------------------------------------+----------------------------------+---------------------+---------------------------------------------------------------------------------------+
| SCOREP_CUDA_ENABLE                    | no                               |  **Value**          | **Description**                                                                       |
|                                       |                                  +---------------------+---------------------------------------------------------------------------------------+
|                                       |                                  |  ``runtime``        | CUDA runtime API                                                                      |
|                                       |                                  +---------------------+---------------------------------------------------------------------------------------+
|                                       |                                  |  ``driver``         | CUDA driver API                                                                       |
|                                       |                                  +---------------------+---------------------------------------------------------------------------------------+
|                                       |                                  |  ``kernel``         | CUDA kernels                                                                          |
|                                       |                                  +---------------------+---------------------------------------------------------------------------------------+
|                                       |                                  |  ``kernel_serial``  | Serialized kernel recording                                                           |
|                                       |                                  +---------------------+---------------------------------------------------------------------------------------+
|                                       |                                  |  ``kernel_counter`` | Fixed CUDA kernel metrics                                                             |
|                                       |                                  +---------------------+---------------------------------------------------------------------------------------+
|                                       |                                  |  ``memcpy``         | CUDA memory copies                                                                    |
|                                       |                                  +---------------------+---------------------------------------------------------------------------------------+
|                                       |                                  |  ``sync``           | Record implicit and explicit CUDA synchronization                                     |
|                                       |                                  +---------------------+---------------------------------------------------------------------------------------+
|                                       |                                  |  ``idle``           | GPU compute idle time                                                                 |
|                                       |                                  +---------------------+---------------------------------------------------------------------------------------+
|                                       |                                  |  ``pure_idle``      | GPU idle time (memory copies are not idle)                                            |
|                                       |                                  +---------------------+---------------------------------------------------------------------------------------+
|                                       |                                  |  ``gpumemusage``    | Record CUDA memory (de)allocations as a counter                                       |
|                                       |                                  +---------------------+---------------------------------------------------------------------------------------+
|                                       |                                  |  ``references``     | Record references between CUDA activities                                             |
|                                       |                                  +---------------------+---------------------------------------------------------------------------------------+
|                                       |                                  |  ``flushatexit``    | Flush CUDA activity buffer at program exit                                            |
|                                       |                                  +---------------------+---------------------------------------------------------------------------------------+
|                                       |                                  |  ``default/yes/1``  | Includes runtime, kernel, memcpy                                                      |
|                                       |                                  +---------------------+---------------------------------------------------------------------------------------+
|                                       |                                  |  ``none/no``        | Disable feature                                                                       |
+---------------------------------------+----------------------------------+---------------------+---------------------------------------------------------------------------------------+
| SCOREP_CUDA_BUFFER                    |  1M                              | Total memory in bytes for the CUDA record buffer                                                            |
+---------------------------------------+----------------------------------+-----------------------+-------------------------------------------------------------------------------------+
| SCOREP_OPENACC_ENABLE                 | no                               |  **Value**            | **Description**                                                                     |
|                                       |                                  +-----------------------+-------------------------------------------------------------------------------------+
|                                       |                                  | ``regions``           | OpenACC regions                                                                     |
|                                       |                                  +-----------------------+-------------------------------------------------------------------------------------+
|                                       |                                  | ``wait``              | OpenACC wait operations                                                             |
|                                       |                                  +-----------------------+-------------------------------------------------------------------------------------+
|                                       |                                  | ``enqueue``           | OpenACC enqueue operations                                                          |
|                                       |                                  +-----------------------+-------------------------------------------------------------------------------------+
|                                       |                                  | ``device_alloc``      | OpenACC device memory allocations                                                   |
|                                       |                                  +-----------------------+-------------------------------------------------------------------------------------+
|                                       |                                  | ``kernel_properties`` | Record kernel properties such as the kernel name, gang, worker and vector size      |
|                                       |                                  +-----------------------+-------------------------------------------------------------------------------------+
|                                       |                                  | ``variable_names``    | Record variable names for OpenACC data allocation and enqueue upload/download       |
|                                       |                                  +-----------------------+-------------------------------------------------------------------------------------+
|                                       |                                  | ``default/yes/1``     | OpenACC regions,enqueue and wait operations                                         |
|                                       |                                  +-----------------------+-------------------------------------------------------------------------------------+
|                                       |                                  | ``none/no``           | Disable feature                                                                     |
+---------------------------------------+----------------------------------+-----------------------+-------------------------------------------------------------------------------------+
| SCOREP_MEMORY_RECORDING               |  FALSE                           | Memory (de)allocations are recorded via libc/C++ API                                                        |
+---------------------------------------+----------------------------------+-------------------------------------------------------------------------------------------------------------+

Example Application: MiniWeather
================================

We'll use the open-source `MiniWeather
<https://github.com/mrnorman/miniWeather>`_ application to demonstrate the
capabilities of Score-P.

Get the Source Code 
~~~~~~~~~~~~~~~~~~~

.. code::

    $ git clone https://github.com/mrnorman/miniWeather.git
    $ cd miniWeather/c/build

Compile the Application
~~~~~~~~~~~~~~~~~~~~~~~

MiniWeather supports several build modes:  serial, MPI, MPI+OpenMP, and
MPI+OpenACC. In order to compile the application, we'll be using the PGI
toolchain, and bring into our environment both ``cmake`` and a parallel
installation of ``NetCDF``. 

.. code::

    $ module load pgi parallel-netcdf cmake
    $ ./cmake_summit_pgi.sh


After the compilation ends, there will be the executables called `serial`, `openacc`, `mpi`, `openmp`

Below, we'll look at using Score-P to profile each case.


Modifications
-------------

- Edit the makefile and replace ``mpic++`` with ``scorep --mpp=mpi mpic++``. 


Instrumenting the Serial Version of MiniWeather
-----------------------------------------------

For a serial application, we should not use a Makefile with a programming
model such as MPI or OpenMP. However, as the source code for this **specific**
case includes MPI headers that are not excluded during the compilation of the
serial version, we should declare a Makefile with MPI. 

- Edit the `cmake_summit_pgi.sh` and replace

.. code::

	cmake -DCMAKE_CXX_COMPILER=mpicxx

with

.. code::

	SCOREP_WRAPPER=off cmake -DCMAKE_CXX_COMPILER=scorep-mpicxx


and execute

.. code::

    $ module load pgi
    $ module load parallel-netcdf
    $ module load scorep/6.0
    $ make serial SCOREP_WRAPPER_INSTRUMENTER_FLAGS="--mpp=mpi

If there were no MPI headers, you should edit the `cmake_summit_pgi.sh` with:

.. code::

	cmake -DCMAKE_CXX_COMPILER=scorep-pgc++

and execute:

.. code::

	make serial

If you want to add PDT, then use the option ``--pdt`` in the variable ``SCOREP_WRAPPER_INSTRUMENTER_FLAGS``

Add to your submission script the Score-P variables that you want to use (or
uncomment them below). By default the Score-P will apply profiling, and not apply tracing.

.. code::

        #PAPI metrics
    	export SCOREP_METRIC_PAPI=PAPI_TOT_INS,PAPI_TOT_CYC,PAPI_FP_OPS

    	export SCOREP_MPI_ENABLE_GROUPS=ALL
    	export SCOREP_TOTAL_MEMORY=20MB

        time jsrun -n 1 -r 1 -a 1 -c 1  ./serial


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


      Estimated aggregate size of event trace:                   7kB
      Estimated requirements for largest trace buffer (max_buf): 7kB
      Estimated memory requirements (SCOREP_TOTAL_MEMORY):       4097kB
           (hint: When tracing set SCOREP_TOTAL_MEMORY=4097kB to avoid intermediate flushes
           or reduce requirements using USR regions filters.)

     flt     type max_buf[B] visits time[s] time[%]   time/visit[us]  region
              ALL      6,529    207  236.20   100.0       1141082.26  ALL
              USR      3,952    152  232.24    98.3       1527889.57  USR
              MPI      2,484     52    0.36     0.2          6946.01  MPI
              COM         52      2    3.60     1.5       1801772.87  COM
           SCOREP         41      1    0.00     0.0            74.15  SCOREP

              USR      3,926    151  232.24    98.3       1538006.62  perform_timestep(double*, double*, double*, double*, double)
              MPI        476      7    0.00     0.0            17.75  MPI_Allreduce
              MPI        400      4    0.00     0.0           163.35  MPI_File_write_at
              MPI        400      4    0.07     0.0         16440.27  MPI_File_write_at_all
              MPI        234      9    0.00     0.0             2.34  MPI_Comm_rank
              MPI        138      2    0.07     0.0         33626.38  MPI_File_open
              MPI        136      2    0.00     0.0             6.75  MPI_Bcast


- We can see that 98.3% of the execution time is spent on user functions and only 1.4% on MPI as there is no real MPI calls on serial code, just some calls are not excluded.


Explanation
~~~~~~~~~~~

+-------------------------+----------------------------------------------------+
| Score-P Region Type Key |  Description                                       |
+=========================+====================================================+
| COM                     | User functions found on callstack to other regions |
+-------------------------+----------------------------------------------------+
| CUDA                    | CUDA API and kernels                               |
+-------------------------+----------------------------------------------------+
| MEMORY                  | Memory alloc/dealloc                               |
+-------------------------+----------------------------------------------------+
| MPI                     | All MPI functions                                  |
+-------------------------+----------------------------------------------------+
| OMP                     | OpenMP constructs                                  |
+-------------------------+----------------------------------------------------+
| OPENACC                 | OpenACC API & kernels                              |
+-------------------------+----------------------------------------------------+
| PTHREAD                 | all pthread functions                              |
+-------------------------+----------------------------------------------------+
| SCOREP                  | Score-P instrumentation                            |
+-------------------------+----------------------------------------------------+
| SHMEM                   | All SHMEM functions                                |
+-------------------------+----------------------------------------------------+
| USR                     | User fucntions not found in COM                    |
+-------------------------+----------------------------------------------------+


We can observe the percentage of each type consumes during the execution of the serial version of MiniWeather


- Repeat the previous procedure but activate PDT, instead of  ``--mpp=mpi``, declare ``--mpp=mpi --pdt``

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


- Edit the `cmake_summit_pgi.sh` and replace

.. code::

        cmake -DCMAKE_CXX_COMPILER=mpicxx

with

.. code::

        SCOREP_WRAPPER=off cmake -DCMAKE_CXX_COMPILER=scorep-mpicxx


and execute


.. code::

        $ module load pgi
        $ module load parallel-netcdf
        $ module load scorep/6.0
        $ make mpi SCOREP_WRAPPER_INSTRUMENTER_FLAGS="--mpp=mpi"

Add to your submission script the Score-P variables that you want to use (or
uncomment them below). By default, the Score-P will apply profiling, and not
tracing.

.. code::

    #PAPI metrics

    export SCOREP_METRIC_PAPI=PAPI_TOT_INS,PAPI_TOT_CYC,PAPI_FP_OPS
    export SCOREP_MPI_ENABLE_GROUPS=ALL
    export SCOREP_TOTAL_MEMORY=20MB

    jsrun -n 64 -r 8 -a 1 -c 1 ./mpi

- A new folder is created and we check the results

.. code::

       cd scorep-20191211_1647_1910918433289249
       scorep-score -r profile.cubex > profile.txt
       less profile.txt


       Estimated aggregate size of event trace:                   12MB
       Estimated requirements for largest trace buffer (max_buf): 188kB
       Estimated memory requirements (SCOREP_TOTAL_MEMORY):       4097kB
            (hint: When tracing set SCOREP_TOTAL_MEMORY=4097kB to avoid intermediate flushes
            or reduce requirements using USR regions filters.)

       flt     type max_buf[B]  visits time[s] time[%] time/visit[us]  region
                ALL    192,445 188,754  338.19   100.0        1791.71  ALL
                MPI    188,400 178,834   96.73    28.6         540.87  MPI
                COM      3,978   9,792  241.45    71.4       24657.66  COM
             SCOREP         41      64    0.00     0.0          75.47  SCOREP
                USR         26      64    0.01     0.0         205.46  USR

                MPI     80,634  57,984    0.25     0.1           4.38  MPI_Irecv
                MPI     80,634  57,984    0.32     0.1           5.55  MPI_Isend
                MPI     23,556  57,984    5.57     1.6          96.01  MPI_Waitall
                COM      3,926   9,664  237.29    70.2       24554.25  perform_timestep(double*, double*, double*, double*, double)
                MPI        476     448   15.71     4.6       35071.16  MPI_Allreduce
                MPI        400       4    0.00     0.0         753.39  MPI_File_write_at
                MPI        400     256    1.31     0.4        5113.83  MPI_File_write_at_all




- Now that we use MPI, we can observe that 28.6% of the total execution time was MPI calls, there were almost 160 thousand MPI_Isend/MPI_Irecv calls
- Moreover in the first line we are informed that if we activate tracing, the size will be close to 12 MB and the minimum requirement for the memory (SCOREP_TOTAL_MEMORY) that we use already.
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


- Prepare the MPI+OpenMP version


- Edit the `cmake_summit_pgi.sh` and replace

.. code::

        cmake -DCMAKE_CXX_COMPILER=mpicxx

with

.. code::

        SCOREP_WRAPPER=off cmake -DCMAKE_CXX_COMPILER=scorep-mpicxx


- Compile the code

 .. code::

         $ module load pgi
         $ module load parallel-netcdf
         $ module load scorep/6.0
         $ make openmp SCOREP_WRAPPER_INSTRUMENTER_FLAGS="--mpp=mpi --thread=omp"

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

         jsrun -n 32 -r 4 -a 1 -c 8 -b packed:8 ./openmp


- A new folder is created and we check the results

 .. code::

    cd scorep-20191212_1359_1949859062811255
    scorep-score -r profile.cubex > profile.txt
    less profile.txt

    Estimated aggregate size of event trace:                   147MB
    Estimated requirements for largest trace buffer (max_buf): 5MB
    Estimated memory requirements (SCOREP_TOTAL_MEMORY):       21MB
    (hint: When tracing set SCOREP_TOTAL_MEMORY=322MB to avoid intermediate flushes
     or reduce requirements using USR regions filters.)

     flt    type  max_buf[B]      visits time[s] time[%] time/visit[us]  region
             ALL  4,799,561    3,312,370  314.15   100.0          94.84  ALL
             OMP  4,540,296    3,135,744  279.71    89.0          89.20  OMP
             MPI    188,400       89,426   32.50    10.3         363.39  MPI
             COM     70,798       87,136    1.93     0.6          22.16  COM
          SCOREP         41           32    0.00     0.0          91.94  SCOREP
             USR         26           32    0.01     0.0         241.39  USR

             OMP    630,576      231,936    1.04     0.3           4.47  !$omp parallel @miniWeather_mpi_openmp.cpp:232
             OMP    315,288      115,968    0.52     0.2           4.49  !$omp parallel @miniWeather_mpi_openmp.cpp:310
             OMP    315,288      115,968    0.52     0.2           4.48  !$omp parallel @miniWeather_mpi_openmp.cpp:346
             OMP    315,288      115,968    0.52     0.2           4.52  !$omp parallel @miniWeather_mpi_openmp.cpp:255
             OMP    315,288      115,968    0.52     0.2           4.47  !$omp parallel @miniWeather_mpi_openmp.cpp:286
             OMP    315,288      115,968    0.52     0.2           4.51  !$omp parallel @miniWeather_mpi_openmp.cpp:375

         ...

- We can observe that OpenMP consumes the 89% of the execution tiime and which OMP pragma occupies more time and which line.
- Moreover, the traces now would be 147 MB and the memory reuquirements are 21 MB per process.

Instrumenting the MPI+OpenACC version of MiniWeather
----------------------------------------------------


- Edit the `cmake_summit_pgi.sh` and replace

.. code::

        cmake -DCMAKE_CXX_COMPILER=mpicxx

with

.. code::

        SCOREP_WRAPPER=off cmake -DCMAKE_CXX_COMPILER=scorep-mpicxx

- Compile the application

.. code::

          $ module load pgi
          $ module load parallel-netcdf
          $ module load scorep/6.0
          $ make openacc SCOREP_WRAPPER_INSTRUMENTER_FLAGS="--mpp=mpi --cuda --openacc"


Add to your submission script the Score-P variables that you want to use (or
uncomment them below). By default, the Score-P will apply profiling, and not
tracing.

- Part of the submission script

.. code::

           module load scorep/6.0

           #PAPI metrics
           export SCOREP_METRIC_PAPI=PAPI_TOT_INS,PAPI_TOT_CYC,PAPI_FP_OPS

           export SCOREP_MPI_ENABLE_GROUPS=ALL
           export SCOREP_TOTAL_MEMORY=20MB
           export SCOREP_OPENACC_ENABLE=default

           jsrun -n 6 -r 3 --smpiargs="-gpu" -g 1 ./openacc


- A new folder is created and we check the results

  .. code::

       cd scorep-20191217_1015_2906378202661
       scorep-score -r profile.cubex > profile.txt
       less profile.txt


       Estimated aggregate size of event trace:                   6MB
       Estimated requirements for largest trace buffer (max_buf): 864kB
       Estimated memory requirements (SCOREP_TOTAL_MEMORY):       4097kB
            (hint: When tracing set SCOREP_TOTAL_MEMORY=4097kB to avoid intermediate flushes
            or reduce requirements using USR regions filters.)

       flt     type max_buf[B]  visits time[s] time[%] time/visit[us]  region
                ALL    884,435 177,402   12.52   100.0          70.60  ALL
            OPENACC    625,196 144,276    1.97    15.7          13.64  OPENACC
                MPI    188,400  16,782    3.67    29.3         218.60  MPI
                COM     70,772  16,332    6.89    55.0         421.72  COM
             SCOREP         41       6    0.00     0.0          82.79  SCOREP
                USR         26       6    0.00     0.0          16.78  USR

                MPI     80,634   5,436    0.02     0.2           4.06  MPI_Irecv
                MPI     80,634   5,436    0.03     0.3           6.10  MPI_Isend
                MPI     23,556   5,436    0.15     1.2          27.79  MPI_Waitall
                COM     23,556   5,436    0.09     0.7          15.82  semi_discrete_step(double*, double*, double*, double, int, double*, double*)
            OPENACC     23,556   5,436    0.06     0.5          11.56  acc_download@miniWeather_mpi_openacc.cpp:395
            OPENACC     23,556   5,436    0.05     0.4           9.02  acc_upload@miniWeather_mpi_openacc.cpp:405
            OPENACC     23,556   5,436    0.04     0.3           7.44  acc_wait@miniWeather_mpi_openacc.cpp:405
            OPENACC     23,556   5,436    0.03     0.2           4.88  acc_data_enter@miniWeather_mpi_openacc.cpp:240




- The OpenACC consumes 15.7% of the total execution time 
- We are going to trace the MPI+OpenACC version and we'll adjust the buffer size
- The new submission script will be like the following:

  .. code::

            module load scorep/6.0

            #PAPI metrics
            export SCOREP_METRIC_PAPI=PAPI_TOT_INS,PAPI_TOT_CYC,PAPI_FP_OPS

            export SCOREP_MPI_ENABLE_GROUPS=ALL
            export SCOREP_TOTAL_MEMORY=5MB
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

- Down on the right, there is a new chart which shows the number of the messages per message size (12.5 KiB)
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
   :scale: 50%
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

- In some cases compiling a hybrid application with Score-P fails with errors as observed below

.. image:: /images/scorep_error.png

In this case there is a problem with the file ``main.opari.cu``

Execute manually the command that failed in order to extract the file ``main.opari.cu`` in this case.

If we compare the files ``main.cu`` and ``main.opari.cu`` there is no such line ``#include <omp.h>``, when you add this line, 
compile again manually this file and continue with the rest of the compilation.

Filtering
~~~~~~~~~

It is common when a user profiles an application and analyze the file ``profile.cubex`` observes that the execution time is 
significantly higher but also the trace file size when tracing is activated is quite big to be analyzed efficiently.

For example, we have the following output:


.. image:: /images/scorep_filtering.png


We can see that when tracing is activated, the total event trace buffer would be 193 GB. Moreover, the user regions are 
``USR``occupies more than 3 billion bytes for the trace buffer. As this region area doesn't include any communication, 
it could be excluded from the instrumentation. We select the functions with caption USR and where their ``time[%]`` is 
more than half percent including the ones with many visits. In this example, we choose many USR functions. 
We create a file called for example, ``exclude.filt`` with content:

.. image:: /images/scorep_filter_functions.png
   :scale: 50 %

We declare the ``SCOREP_REGION_NAMES_BEGIN`` to declare that below are the regions. The option ``EXCLUDE`` means exclude them, and
the ``SCOREP_REGION_NAMES_END`` defines when the list finishes. 

Then define the environment variable ``SCOREP_FILTERING_FILE`` to the ``exclude.filt``

.. image:: /images/scorep_filtering_results.png

Now the prediction for the event trace buffer would be 7 GB, almost 28 times smaller; also, the execution time overhead from 49% went down to 7%.
