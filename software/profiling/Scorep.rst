.. _Scorep_v1:

.. image:: /images/Scorep_logo.png
   :width: 200px
   :height: 100px

|

Score-P
*******


Overview
========

The goal of `Score-P <https://www.vi-hps.org/projects/score-p>`__ is to simplify
the analysis of high performance computing software and enable developers to
find performance problems.  The Score-P measurement infrastructure is a highly
scalable and easy-to-use tool suite for profiling, event tracing, and online
analysis of HPC applications. Score-P supports analyzing C, C++ and Fortran
applications that make use of multi-processing (MPI, SHMEM), thread parallelism
(OpenMP, PThreads) and accelerators (HIP, CUDA, OpenCL, OpenACC, OpenMP-offload)
and combinations of these. It works in combination with Scalasca, Vampir, TAU
and Periscope, generating traces in OTF2 format (Vampir, Scalasca, TAU) and
profiles in CUBE4 and TAU formats.

See https://www.vi-hps.org/projects/score-p/ for details about Score-P.  

Usage
=====

Steps in a typical Score-P workflow to run on an OLCF machine (e.g. Frontier or
Andes). (`More info about OLCF Systems
<https://docs.olcf.ornl.gov/systems/index.html>`_). 

1. :ref:`Connect to an OLCF system <connecting-to-olcf>`: ``ssh <user_id><machine>.olcf.ornl.gov``
2. Instrument your code with Score-P
3. Perform a measurement run with profiling enabled
4. Perform a profile analysis with CUBE or cube_stat
5. Use ``scorep-score`` to define a filter
6. Perform a measurement run with tracing enabled and the filter applied
7. Perform in-depth analysis on the trace data with Vampir

Instrumentation
===============

To instrument your code, you need to re-compile the code using the Score-P instrumentation command (``scorep``) added as a prefix to your compile statement.
In most cases the Score-P instrumentor is able to automatically detect the programming paradigm from the set of compile and link options given to the compiler.
Some cases may, however, require some additional link options within the compile statement e.g. ROCm HIP or CUDA instrumentation.

.. Note::

   You will need to unload the ``darshan-runtime`` module if it is loaded. 
   In `some` instances you may need to unload the ``xalt`` and ``xl`` modules.   

   .. code-block:: bash

      $ module unload darshan-runtime


Get a list of available versions of Score-P and select the one you want to use.   
   
.. code-block:: bash

   # Find available scorep modules 
   $ module spider scorep
   ...
   # Returned choices on Frontier: scorep-gcc-amd, scorep-amd, scorep-amdclang, scorep-cray

   # Unload the darshan-runtime module if it is loaded
   $ module unload darshan-runtime

   # Load the desired version, e.g.: Score-P with GNU compiler
   $ module load scorep-gcc-amd

   # If you want to see how scorep was configured
   # module show scorep-gcc-amd

   # Getting information on scorep flags
   $ scorep --help

   # Info about compiler wappers (e.g. scorep-amdclang, scorep-mpicc, etc)
   $ scorep-wrapper --help 

Below are some basic examples of the different ways to instrument your code with Score-P. The examples below are for the GNU compiler, but the same principles apply to other compilers (e.g. Intel, Cray, etc).

.. code-block:: bash

   # Prepend compile and link commands with scorep
   # scorep <COMPILER/LINKER> mytestcode.ext
   # scorep <scorep-options> <COMPILER/LINKER> <options> mytestcode.ext

   # For C (similar for C++, Fortran)
   $ scorep gcc -c test.c
   $ scorep gcc -o test test.o

   # For Fortran
   $ scorep gfortran -c test.f90
   $ scorep gfortran -o test test.o

   # For MPI (using mpicc, mpiCC, mpifort as needed)
   $ module load <mpi-module>
   $ scorep mpicc -c test.c   # Use -fopenmp and -pthread as needed
   $ scorep mpicc -o test test.o

   # For GPU code (ROCM, CUDA, etc)
   # The scorep wrapper will usually autodetect the GPU compiler, 
   # but you can force it with --hip, --cuda, etc
   # Using ROCm HIP
   $ scorep --hip hipcc -L${OLCF_CUDA_ROOT}/lib64 -c test.c
   # Using CUDA
   $ scorep --cuda --user nvc++ -cuda -L${OLCF_CUDA_ROOT}/lib64 -c test.c


CMake / Autotools Instrumentation
---------------------------------

CMake and Autotools based build systems run a number of small
configuration-tests to probe the system, and these configuration-tests will
often fail if scorep is used as above.  To get around this, use the provided
``scorep-wrapper`` scripts (e.g. ``scorep-gcc``, ``scorep-mpicc``) together with the
variable ``SCOREP_WRAPPER=off``. This switches the scorep-wrapper off during the
configuration time, but ``scorep`` still gets used at application build time.
For more detailed information on using Score-P with CMake or Autotools visit
`Score-P
<https://scorepci.pages.jsc.fz-juelich.de/scorep-pipelines/docs/scorep-4.1/html/scorepwrapper.html>`_

For CMake and Autotools based builds, run configure in the following way:

.. code-block:: bash

   # Get information on the scorep-wrapper scripts
   $ scorep-wrapper --help

   # Example for CMake build generation with GNU compiler-wrappers
   $ SCOREP_WRAPPER=off cmake .. 
        -DCMAKE_C_COMPILER=scorep-gcc \
        -DCMAKE_CXX_COMPILER=scorep-g++ \
        -DCMAKE_Fortran_COMPILER=scorep-ftn

   # Example for autotools with GNU compiler-wrappers
   $ SCOREP_WRAPPER=off ../configure \
        CC=scorep-gcc \
        CXX=scorep-g++ \
        FC=scorep-ftn \
        --disable-dependency-tracking


Makefile Instrumentation
------------------------

Setting a flag variable, such as ``PREP = scorep`` variable within a Makefile
will simplify enabling and disabling instrumentation control while using
``make``.  Additionally, one can add other Score-P options within the ``PREP``
variable e.g. ``--hip``.  To disable the instrumentation, simply set the
``PREP`` variable to an empty string.  Below is an example of a Makefile that
uses Score-P with ROCm HIP.

.. code-block:: makefile

   ## Makefile for Score-P with ROCm HIP

   CC = hipcc
   CFLAGS =
   PREP = scorep --hip

   INCLUDES  = -I<Path to Includes>/include # if needed
   LIBRARIES = -L<Path to Libraries>/lib64 # if needed

   test: test.o
      $(PREP) $(CC) $(CFLAGS) $(LIBRARIES) test.o -o test

   test.o: test.c
      $(PREP) $(CC) $(CFLAGS) $(INCLUDES) -c test.c

   .PHONY: clean

   clean:
      rm -f test *.o


Measurement
===========

Once the code has been instrumented, it is time to begin the measurement runs.
The measurement calls will gather information during the execution and store for
later analysis.

By default Score-P is configured to run with profiling set to **true** and
tracing set to **false**. Measurement types are configured via environment
variables and the default values can be checked using the ``scorep-info``
command. The environment variables can be set in your batch script or
interactively.

.. code-block:: bash

   # Environment variable examples
   $ export SCOREP_ENABLE_TRACING=true

   # Check what current Score-P environment variables are set:
   $ scorep-info config-vars --full
   # Output of scorep-info config-vars
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
---------

To generate a profile run of your instrumented code on a compute node, you will
first need to get a node allocation using a batch script or an interactive job.
Additionally you will need to load the ``otf2`` and ``cubew`` modules.

.. code-block:: bash

   $ module load otf2
   $ module load cubew

For more information on launching batch jobs on Frontier, please see the
`Running Jobs section of the Frontier User Guide
<https://docs.olcf.ornl.gov/systems/frontier_user_guide.html#running-jobs>`_.
Here is an example batch script to run a profiling measurement on Frontier:

.. Admonition:: Example Batch Script for Frontier

   .. code-block:: bash

      #!/bin/bash
      #SBATCH -A ABC123       # Project account
      #SBATCH -t 1:00:00      # Walltime
      #SBATCH -p batch        # Queue
      #SBATCH -N 1            # Number of nodes
      #SBATCH -J MyJobName    # Job Name
      #SBATCH -o %x-%j.out    # Job output file

      cd <path to my ScoreP instrumented executable>

      export SCOREP_ENABLE_PROFILING=true
      export SCOREP_ENABLE_TRACING=false
      export SCOREP_EXPERIMENT_DIRECTORY=executable_scorep_outdir

      srun -n 1 ./<executable>


By default, the output files generated when the profile measurement runs are
successful will be placed in a folder named ``scorep-yyyymmdd_hhmm_uniqueid``. A
preferred folder name can be set using the ``SCOREP_EXPERIMENT_DIRECTORY`` env
variable. After the profile run, the folder will contain a file with the name
``profile.cubex``. The ``.cubex`` file can be analyzed using a presentation tool
called `Cube
<http://apps.fz-juelich.de/scalasca/releases/cube/4.3/docs/CubeGuide.pdf>`_
developed by Scalasca. 

For a more detailed description of profiling measurements with Score-P, please
visit the `ScorepP_Profiling
<https://scorepci.pages.jsc.fz-juelich.de/scorep-pipelines/docs/scorep-4.1/html/measurement.html>`_
homepage.


Tracing
-------

Since tracing measurements acquire significantly more output data than
profiling, we need to design a filter to remove some of the most visited calls
within your instrumented code. There is a tool developed by Score-P,
``scorep-score`` that allows us to estimate the size of the trace file (OTF2)
based on information attained from the profiling generated ``cubex`` file.

To gather the needed information to design a filter file, first run
``scorep-score`` on the generated profile file:

.. code-block:: bash

   $ scorep-score -r <profile cube dir>/profile.cubex

.. Admonition:: Output scorep-score generated example:

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

.. code-block:: bash

   $ cat scorep.filter
   SCOREP_REGION_NAMES_BEGIN
    Exclude
      matmul_sub
      matvec_sub
   SCOREP_REGION_NAMES_END

One can check the effects of the filter by re-running the ``scorep-score``
command with the new filter file.

.. code-block:: bash

   $ scorep-score <profile cube dir>/profile.cubex -f scorep.filter

Now you are ready to submit a batch request with your instrumented code to run
with tracing enabled. To run a tracing measurement, we will need to enable the
environment variable ``SCOREP_ENABLE_TRACING``.   To apply the filter to your
measurement run, you must specify this in an environment variable called
``SCOREP_FILTERING_FILE``.

.. code-block:: bash

   $ export SCOREP_ENABLE_TRACING=true
   $ export SCOREP_FILTERING_FILE=scorep.filter

This measurement will generate files of the form ``traces.otf``. The ``.otf2``
file format can be analyzed by a tool called `Vampir
<https://docs.olcf.ornl.gov/software/profiling/Vampir.html>`_ , that provides a
visual GUI to analyze the ``.otf2`` trace file generated with Score-P.

.. Note::

   Small trace files can be downloaded and viewed locally on your machine if you
   have the Vampir client downloaded, or they can be viewed on your local
   machine using a remote X-display from the OLCF machine. 
   
   For large trace files, it is strongly recommended to run ``vampirserver`` on
   the OLCF machine, reverse-connected to a Vampir client on your local machine.
   See the :ref:`vamptunnel` section for more details.

Manual Instrumentation
======================

In addition to automatically profiling and tracing functions, there is also a way to manually instrument a specific region in the source code. To do this, you will need to add the ``--user`` flag to the ``scorep`` command when compiling:

.. code-block:: bash

   $ scorep --user gcc -c test.c
   $ scorep --user gcc -o test test.o

Now you can manually instrument Score-P within the source code as seen below:

.. tab-set::

   .. tab-item:: C/C++

      .. code-block:: c
         
         #include <scorep/SCOREP_User.h>

         void foo() {
            SCOREP_USER_REGION_DEFINE(my_region)
            SCOREP_USER_REGION_BEGIN(my_region, "foo", SCOREP_USER_REGION_TYPE_COMMON)
            // do the work of foo here
            SCOREP_USER_REGION_END(my_region)
         }


   .. tab-item:: Fortran

      .. code-block:: fortran
         
         #include <scorep/SCOREP_User.inc>

         subroutine foo
            SCOREP_USER_REGION_DEFINE(my_region)
            SCOREP_USER_REGION_BEGIN(my_region, "foo", SCOREP_USER_REGION_TYPE_COMMON)
            ! do the work of foo here
            SCOREP_USER_REGION_END(my_region)
         end subroutine foo


In this case, "my_region" is the handle name of the region which has to be defined with ``SCOREP_USER_REGION_DEFINE``. Additionally, "foo" is the string containing the region's unique name (this is the name that will show up in Vampir) and ``SCOREP_USER_REGION_TYPE_COMMON`` identifies the type of the region. Make note of the header files seen in the above example that are needed to include the Score-P macros. See the `Score-P User Adapter <https://scorepci.pages.jsc.fz-juelich.de/scorep-pipelines/docs/scorep-6.0/html/group__SCOREP__User.html>`_ page for more user configuration options.  

Below are some examples of manually instrumented regions using phase and loop types: 

.. code-block:: c
   
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

.. code-block:: c

   #include <scorep/SCOREP_User.h>
   
   SCOREP_USER_REGION_DEFINE(calculation_hdl)
   SCOREP_USER_REGION_BEGIN(calculation_hdl, "my_calculations", SCOREP_USER_REGION_TYPE_LOOP)
   #pragma omp parallel for ...
      for (int i=0; i <num; i++){
         //do calculation
      }
   SCOREP_USER_REGION_END(calculation_hdl)

The regions "sum" and "my_calculations" in the above examples would then be included in the profiling and tracing runs and can be analysed with Vampir. For more details, refer to the Advanced Score-P training in the :ref:`training-archive`.

Score-P and Vampir Demo
=======================

Please see the 30-minute video below on `2023 Trace-Based Performance Analysis with
Score-P + Vampir <https://vimeo.com/858484450>`_ to get a brief introduction to
Vampir and Score-P. This recording is taken from the Frontier Training Workshop
(August 2023), Friday, August 25th, 2023, presented by Bill Williams,
TU-Dresden.

You can watch the video here: https://vimeo.com/858484450

.. raw:: html

   <div style="padding:56.25% 0 0 0;position:relative;"><iframe src="https://player.vimeo.com/video/858484450?h=26f33f1775" style="position:absolute;top:0;left:0;width:100%;height:100%;" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe></div><script src="https://player.vimeo.com/api/player.js"></script>
   <p><a href="https://vimeo.com/858484450">2023 Trace-Based Performance Analysis with Score-P + Vampir</a> from <a href="https://vimeo.com/olcf">OLCF</a> on <a href="https://vimeo.com">Vimeo</a>.</p>


.. .. raw:: html

.. .. raw:: html

..    <div style="padding:56.25% 0 0 0;position:relative;"><iframe src="https://player.vimeo.com/video/285908215?h=26f33f1775" style="position:absolute;top:0;left:0;width:100%;height:100%;" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe></div><script src="https://player.vimeo.com/api/player.js"></script>

..    <p><a href="https://vimeo.com/285908215">2018 Score-P / Vampir Workshop</a> from <a href="https://vimeo.com/olcf">OLCF</a> on <a href="https://vimeo.com">Vimeo</a>.</p>

.. This recording is from the 2018 Score-P / Vampir workshop that took place at ORNL on August 17, 2018. In the video, Ronny Brendel gives an introduction to the Score-P and Vampir tools, which are often used together to collect performance profiles/traces from an application and visualize the results.
