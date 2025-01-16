.. _Scorep_v1:

.. image:: /images/Scorep_logo.png
   :align: left
   :width: 200px
   :height: 100px

|
|
|
|
|


Score-P
*******


Overview
========

The `Score-P  <https://www.vi-hps.org/projects/score-p>`__ measurement infrastructure is a highly
scalable and easy-to-use tool suite for profiling, event tracing, and online analysis of HPC
applications. Score-P supports analyzing C, C++ and Fortran applications that make use of multi
processing (MPI, SHMEM), thread parallelism (OpenMP, PThreads) and accelerators (CUDA, OpenCL,
OpenACC) and combinations. It works in combination with Periscope, Scalasca, Vampir, and Tau.


Usage
=====

Steps in a typical Score-P workflow to run on Summit:

1. Login to :ref:`Summit <connecting-to-olcf>`: ``ssh <user_id>@summit.olcf.ornl.gov``
2. Instrument your code with Score-P
3. Perform a measurement run with profiling enabled
4. Perform a profile analysis with CUBE or cube_stat
5. Use ``scorep-score`` to define a filter
6. Perform a measurement run with tracing enabled and the filter applied
7. Perform in-depth analysis on the trace data with Vampir

Instrumentation
===============


To instrument your code, you need to compile the code using the Score-P instrumentation command (``scorep``), which is added as a prefix to your compile statement.
In most cases the Score-P instrumentor is able to automatically detect the programming paradigm from the set of compile and link options given to the compiler.
Some cases will, however, require some additional link options within the compile statement e.g. CUDA instrumentation.

Below are some basic examples of the different instrumentation scenarios:

.. Note::

   You will need to unload the ``darshan-runtime`` module. In `some` instances you may need to unload the ``xalt`` and ``xl`` modules.

   .. code::

      $ module unload darshan-runtime

.. dropdown:: Serial

    .. tab-set::

        .. tab-item:: C

            .. code-block:: bash

                $ module unload darshan-runtime
                $ module load scorep
                $ module load gcc
                $ scorep gcc -c test.c
                $ scorep gcc -o test test.o

        .. tab-item:: C++

            .. code-block:: bash

                $ module unload darshan-runtime
                $ module load scorep
                $ module load gcc
                $ scorep g++ -c test.cpp main.cpp
                $ scorep g++ -o test test.o main.o

        .. tab-item:: Fortran

            .. code-block:: bash

                $ module unload darshan-runtime
                $ module load scorep
                $ module load gcc
                $ scorep gfortran -c test_def.f90 test.f90 main.f90
                $ scorep gfortran -o test test_def.o test.o main.o



.. dropdown:: MPI

    .. tab-set::

        .. tab-item:: C

            .. code-block:: bash

                  $ module unload darshan-runtime
                  $ module load scorep
                  $ module load spectrum-mpi
                  $ module load gcc
                  $ scorep mpicc -c test.c main.c
                  $ scorep mpicc -o test test.o main.o

        .. tab-item:: C++

            .. code-block:: bash

                  $ module unload darshan-runtime
                  $ module load scorep
                  $ module load spectrum-mpi
                  $ module load gcc
                  $ scorep mpiCC -c test.cpp main.cpp
                  $ scorep mpiCC -o test test.o main.o

        .. tab-item:: Fortran

            .. code-block:: bash

                $ module unload darshan-runtime
                $ module load gcc
                $ module load Scorep
                $ scorep mpifort -c test.f90
                $ scorep mpifort -o test test.o


.. dropdown:: MPI + OpenMP

    .. tab-set::

        .. tab-item:: C

            .. code-block:: bash

                  $ module unload darshan-runtime
                  $ module load scorep
                  $ module load gcc
                  $ scorep mpicc -fopenmp -c test.c main.c
                  $ scorep mpicc -fopenmp -o test test.o main.o

        .. tab-item:: C++

            .. code-block:: bash

                  $ module unload darshan-runtime
                  $ module load scorep
                  $ module load gcc
                  $ scorep mpiCC -fopenmp -c test.cpp main.cpp
                  $ scorep mpiCC -fopenmp -o test test.o main.o

        .. tab-item:: Fortran

            .. code-block:: bash

                  $ module unload darshan-runtime
                  $ module load scorep
                  $ module load gcc
                  $ scorep mpifort -pthread -fopenmp -c test.f90
                  $ scorep mpifort -pthread -fopenmp -o test test.o

.. dropdown:: CUDA

    In some cases e.g. **CUDA** applications, Score-P needs to be made aware of the programming paradigm in order to do the correct instrumentation.

    .. code-block:: bash

        $ module unload darshan-runtime xl
        $ module load nvhpc
        $ module load cuda
        $ module load scorep/<version-number>-papi
        $ scorep --cuda --user nvc++ -cuda -L${OLCF_CUDA_ROOT}/lib64 -c test.c
        $ scorep --cuda --user nvc++ -cuda -L${OLCF_CUDA_ROOT}/lib64 -o test test.o


Makefiles
---------

Setting ``PREP = scorep`` variable within a Makefile will allow for instrumentation control while using
``make``

Additionaly, one can add other Score-P options within the ``PREP`` variable e.g. ``--cuda``

.. code::

   ##Sample Makefile:

   CCOMP  = nvc++
   CFLAGS =
   PREP = scorep --cuda

   INCLUDES  = -I<Path to Includes>/include ##If needed
   LIBRARIES = -L<Path to Libraries>/lib64 ##If needed

   test: test.o
      $(PREP) $(CCOMP) $(CFLAGS) $(LIBRARIES) test.o -o test

   test.o: test.c
      $(PREP) $(CCOMP) $(CFLAGS) $(INCLUDES) -c test.c

   .PHONY: clean

   clean:
      rm -f test *.o

CMake / Autotools
-----------------

For CMake and Autotools based build systems, it is recommended to use the scorep-wrapper script
instances. The intended usage of the wrapper instances is to replace the application's compiler and
linker with the corresponding wrapper at configuration time so that they will be used at build time.
As the Score-P instrumentation during the CMake or configure steps is likely to fail, the wrapper script allows for disabling the instrumentation by setting the variable ``SCOREP_WRAPPER=off``.


For CMake and Autotools based builds it is recommended to configure in the following way(s):

.. code::

   #Example for CMake

   $ SCOREP_WRAPPER=off cmake .. \
        -DCMAKE_C_COMPILER=scorep-gcc \
        -DCMAKE_CXX_COMPILER=scorep-g++ \
        -DCMAKE_Fortran_COMPILER=scorep-ftn

.. code::

   #Example for autotools

   $ SCOREP_WRAPPER=off  ../configure \
        CC=scorep-gcc \
        CXX=scorep-g++ \
        FC=scorep--ftn \
        --disable-dependency-tracking

.. Note::

   ``SCOREP_WRAPPER=off`` disables the instrumentation only in the environment of the ``configure`` or ``cmake`` command. Subsequent calls to ``make`` are not affected and will instrument the application as expected.

For more detailed information on using Score-P with CMake or Autotools visit `Score-P <https://scorepci.pages.jsc.fz-juelich.de/scorep-pipelines/docs/scorep-4.1/html/scorepwrapper.html>`_


.. Note::

  To see all available options for instrumentation:

  .. code::

     $ scorep --help

|

Measurement
===========

Once the code has been instrumented, it is time to begin the measurement run of the newly compiled code. The measurement calls will gather information during the runtime of the code where this information will be stored for later analysis.

By default Score-P is configured to run with profiling set to **true** and tracing set to **false**. Measurement types are configured via environment variables.

.. code::

   ##Environment variable setup examples

   export SCOREP_ENABLE_TRACING=true

You can check what current Score-P environment variables are set:

.. code::

   $ scorep-info config-vars --full

   #Output

   SCOREP_ENABLE_PROFILING
   Description: Enable profiling
         Type: Boolean
         Default: true

   SCOREP_ENABLE_TRACING
   Description: Enable tracing
         Type: Boolean
         Default: false

   SCOREP_VERBOSE
   Description: Be verbose
         Type: Boolean
         Default: false

    .....


Profiling
=========

To generate a profile run of your instrumented code on Summit, you will first need to get a node allocation
using a batch script or an interactive job; Additionaly you will need to load modules ``otf2`` and ``cubew``:

.. code::

   $ module load otf2
   $ module load cubew

.. Admonition:: Example Batch Script

  .. code::

     #!/bin/bash
     # Begin LFS Directives
     #BSUB -P ABC123        #Project Account
     #BSUB -W 3:00          #Walltime
     #BSUB -nnodes 1        #Number of Nodes
     #BSUB -J RunSim123     #Job Name
     #BSUB -o RunSim123.%J  #Job System Out
     #BSUB -e RunSim123.%J  #Job System Error Out

     cd <path to instrumented code>

     jsrun -n 1 ./<binary to run>

For more information on launching jobs on Summit, please see the Running Jobs section of the Summit User Guide.

The output files generated when the profile measurement runs are successful will be placed in a folder uniquely named:

.. code::

   $ scorep-yyyymmdd_hhmm_<Unique ID created>

A file will be placed within the above mentioned folder with the name ``profile.cubex``. This type of file can be analyzed using a tool called `Cube <http://apps.fz-juelich.de/scalasca/releases/cube/4.3/docs/CubeGuide.pdf>`_ developed by Scalasca.

For a more detailed description of profiling measurements with Score-P, please visit the `ScorepP_Profiling <https://scorepci.pages.jsc.fz-juelich.de/scorep-pipelines/docs/scorep-4.1/html/measurement.html>`_ homepage.


Tracing
=======

To run a tracing measurement, we will need to enable this through the environment variable ``SCOREP_ENABLE_TRACING``:

.. code::

   $ export SCOREP_ENABLE_TRACING=true


Since tracing measurements acquire significantly more output data than profiling, we need to design a filter to remove some of the most visited calls within your instrumented code. There is a tool developed by Score-P that allows us to estimate the size of the trace file (OTF2) based on information attained from the profiling generated cube file.

To gather the needed information to design a filter file, first run ``scorep-score``:

.. code::

   $ scorep-score -r <profile cube dir>/profile.cubex

.. Admonition:: Output scorep-score generated Example:

  .. code::

     Estimated aggregate size of event trace:                   40GB
     Estimated requirements for largest trace buffer (max_buf): 10GB
     Estimated memory requirements (SCOREP_TOTAL_MEMORY):       10GB
     (warning: The memory requirements can not be satisfied by Score-P to avoid
     intermediate flushes when tracing. Set SCOREP_TOTAL_MEMORY=4G to get the
     maximum supported memory or reduce requirements using USR regions filters.)

     Flt type      max_buf[B]         visits  time[s]  time[%]  time/visit[us]      region
          ALL  10,690,196,070  1,634,070,493  1081.30    100.0            0.66         ALL
          USR  10,666,890,182  1,631,138,069   470.23     43.5            0.29         USR
          OMP      22,025,152      2,743,808   606.80     56.1          221.15         OMP
          COM       1,178,450        181,300     2.36      0.2           13.04         COM
          MPI         102,286          7,316     1.90      0.2          260.07         MPI

          USR   3,421,305,420    522,844,416   144.46     13.4            0.28  matmul_sub
          USR   3,421,305,420    522,844,416   102.40      9.5            0.20  matvec_sub

The first line of the output gives an estimation of the total size of the trace, aggregated over all processes. This information is useful for estimating the space required on disk. In the given example, the estimated total size of the event trace is 40GB. The second line prints an estimation of the memory space required by a single process for the trace. Since flushes heavily disturb measurements, the memory space that Score-P reserves on each process at application start must be large enough to hold the process’ trace in memory in order to avoid flushes during runtime.

In addition to the trace, Score-P requires some additional memory to maintain internal data structures. Thus, it provides also an estimation for the total amount of required memory on each process. The memory size per process that Score-P reserves is set via the environment variable ``SCOREP_TOTAL_MEMORY``. In the given example the per process memory is about 10GB. When defining a filter, it is recommended to exclude short, frequently called functions from measurement since they require a lot of buffer space (represented by a high value under ``max_tbc``) but incur a high measurement overhead. MPI functions and OpenMP constructs cannot be filtered. Thus, it is usually a good approach to exclude regions of type USR starting at the top of the list until you reduced the trace to your needs. The example below excludes the functions ``matmul_sub`` and ``matvec_sub`` from the trace:

.. code::

   $ cat scorep.filter
   SCOREP_REGION_NAMES_BEGIN
    Exclude
      matmul_sub
      matvec_sub
   SCOREP_REGION_NAMES_END

One can check the effects of the filter by re-running the ``scorep-score`` command:

.. code::

   $ scorep-score <profile cube dir>/profile.cubex -f scorep.filter

To apply the filter to your measurement run, you must specify this in an environment variable called
``SCOREP_FILTERING_FILE``:

.. code::

   $ export SCOREP_FILTERING_FILE=scorep.filter

Now you are ready to submit your instrumented code to run with tracing enabled. This measurement will generate files of the form ``traces.otf``.
The ``.otf2`` file format can be analyzed by a tool called `Vampir <https://docs.olcf.ornl.gov/software/profiling/Vampir.html>`_ .

`Vampir <https://docs.olcf.ornl.gov/software/profiling/Vampir.html>`_ provides a visual GUI to
analyze the ``.otf2`` trace file generated with Score-P.

.. Note::

   Small trace files can be viewed locally on your machine if you have the Vampir client downloaded,
   otherwise they can be viewed locally on Summit. For large trace files, it is strongly recommended to run
   ``vampirserver`` reverse-connected to a local copy of the Vampir client. See the :ref:`vamptunnel` section for more details.

Manual Instrumentation
======================

In addition to automatically profiling and tracing functions, there is also a way to manually instrument a specific region in the source code. To do this, you will need to add the ``--user`` flag to the ``scorep`` command when compiling:

.. code::

   $ scorep --user gcc -c test.c
   $ scorep --user gcc -o test test.o

Now you can manually instrument Score-P to the source code as seen below:

.. tab-set::

   .. tab-item:: C,C++

      .. code::
         
         #include <scorep/SCOREP_User.h>

         void foo() {
            SCOREP_USER_REGION_DEFINE(my_region)
            SCOREP_USER_REGION_BEGIN(my_region, "foo", SCOREP_USER_REGION_TYPE_COMMON)
         // do something
         SCOREP_USER_REGION_END(my_region)
         }


   .. tab-item:: Fortran

      .. code::
         
         #include <scorep/SCOREP_User.inc>

         subroutine foo
            SCOREP_USER_REGION_DEFINE(my_region)
            SCOREP_USER_REGION_BEGIN(my_region, "foo", SCOREP_USER_REGION_TYPE_COMMON)
            ! do something
            SCOREP_USER_REGION_END(my_region)
         end subroutine foo


In this case, "my_region" is the handle name of the region which has to be defined with ``SCOREP_USER_REGION_DEFINE``. Additionally, "foo" is the string containing the region's unique name (this is the name that will show up in Vampir) and ``SCOREP_USER_REGION_TYPE_COMMON`` identifies the type of the region. Make note of the header files seen in the above example that are needed to include the Score-P macros. See the `Score-P User Adapter <https://scorepci.pages.jsc.fz-juelich.de/scorep-pipelines/docs/scorep-6.0/html/group__SCOREP__User.html>`_ page for more user configuration options.  

Below are some examples of manually instrumented regions using phase and loop types: 

.. code::
   
   #include <scorep/SCOREP_User.h>
   
   SCOREP_USER_REGION_DEFINE(sum_hdl)
   SCOREP_USER_REGION_BEGIN(sum_hdl, "sum", SCOREP_USER_REGION_TYPE_PHASE)
   if (x < 1){
      //do calculation
   }
   else{
      //do other calculation
   }
   SCOREP_USER_REGION_END(sum_hdl)

.. code::

   #include <scorep/SCOREP_User.h>
   
   SCOREP_USER_REGION_DEFINE(calculation_hdl)
   SCOREP_USER_REGION_BEGIN(calculation_hdl, "my_calculations", SCOREP_USER_REGION_TYPE_LOOP)
   #pragma omp parallel for ...
      for (int i=0; i <num; i++){
         //do calculation
      }
   SCOREP_USER_REGION_END(calculation_hdl)

The regions "sum" and "my_calculations" in the above examples would then be included in the profiling and tracing runs and can be analysed with Vampir. For more details, refer to the Advanced Score-P training in the :ref:`training-archive`.

Score-P Demo Video
==================

Please see the provided video below to watch a brief demo of using Score-P provided by TU-Dresden and presented by Ronny Brendel.

.. raw:: html

   <div style="padding:56.25% 0 0 0;position:relative;"><iframe src="https://player.vimeo.com/video/285908215?h=26f33f1775" style="position:absolute;top:0;left:0;width:100%;height:100%;" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe></div><script src="https://player.vimeo.com/api/player.js"></script>

   <p><a href="https://vimeo.com/285908215">2018 Score-P / Vampir Workshop</a> from <a href="https://vimeo.com/olcf">OLCF</a> on <a href="https://vimeo.com">Vimeo</a>.</p>

This recording is from the 2018 Score-P / Vampir workshop that took place at ORNL on August 17, 2018. In the video, Ronny Brendel gives an introduction to the Score-P and Vampir tools, which are often used together to collect performance profiles/traces from an application and visualize the results.
