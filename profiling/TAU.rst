.. _tau:

************************************
Tuning and Analysis Utilities (TAU)
************************************

TAU is a portable profiling and tracing toolkit that supports many programming languages. 
The instrumentation can be done by inserting in the source code using an automatic tool 
based on the Program Database Toolkit (PDT), on the compiler instrumentation, 
or manually using the instrumentation API.

TAU is installed with Program Database Toolkit (PDT) on Summit. PDT is a framework for analyzing source code written in several programming
languages. In this section, some approaches for profiling and tracing will be presented.

In the most cases, we need to use wrappers to recompile the application:

- For C: replace the compiler with tau_cc.sh
- For C++: replace the compiler with tau_cxx.sh
- For Fortran: replace the compiler with tau_f90.sh/tau_f77.sh

If you compile your application with non TAU wrapper, then you can profile some basic functionalities with *tau_exec*, for example:

..code::

	jsrun -n 4 –r 4 –a 1 –c 1 tau_exec -T mpi ./test

The above command profiles the MPI for the binary test which was not compiled with TAU wrapper.


TAU Enviroment Variables
------------------------

+----------------------+--------+------------------------------------------------------------------------------------------------------------+
|Variable  	       |Default | Description			     									     |
+======================+========+============================================================================================================+
|TAU_TRACE	       |    0   |Setting to 1 turns on tracing       									     |
+----------------------+--------+------------------------------------------------------------------------------------------------------------+
|TAU_CALLPATH          |    0   |Setting to 1 turns on callpath profiling							             |
+----------------------+--------+------------------------------------------------------------------------------------------------------------+
|TAU_TRACK_MEMORY_LEAKS|    0   |Setting to 1 turns on leak detection									     |
+----------------------+--------+------------------------------------------------------------------------------------------------------------+
|TAU_TRACK_HEAP        |    0   |Setting to 1 turns on heap memory routine entry/exit							     |
+----------------------+--------+------------------------------------------------------------------------------------------------------------+
|TAU_CALLPATH_DEPTH    |    2   |Specifies depth of callpath         		     							     |
+----------------------+--------+------------------------------------------------------------------------------------------------------------+
|TAU_TRACK_IO_PARAMS   |    0   |Setting 1 with -optTrackIO	     		     							     |
+----------------------+--------+------------------------------------------------------------------------------------------------------------+
|TAU_SAMPLING	       |    1   |Generates sample based profiles     		     							     |
+----------------------+--------+------------------------------------------------------------------------------------------------------------+
|TAU_COMM_MATRIX       |    0   |Setting to 1 generates communication matrix	    							     |
+----------------------+--------+------------------------------------------------------------------------------------------------------------+
|TAU_THROTTLE          |    1   |Setting to 0 turns off throttling, by default removes overhead       					     |
+----------------------+--------+------------------------------------------------------------------------------------------------------------+
|TAU_THROTTLE_NUMCALLS |100000  |Number of calls before testing throttling 								     |
+----------------------+--------+------------------------------------------------------------------------------------------------------------+
|TAU_THROTTLE_PERCALL  |    10  |If a routine is called more than 100000 times and it takes less than  10usec of inclusive time, throttle it |
+----------------------+--------+------------------------------------------------------------------------------------------------------------+
|TAU_COMPENSATE        |    10  |Setting to 1 enables runtime compensation of instrumentation overhead 					     |
+----------------------+--------+------------------------------------------------------------------------------------------------------------+
|TAU_PROFILE_FORMAT    |Profile |Setting to "merged" generates a single file, "snapshot" generates a snapshot per thread 		     |
+----------------------+--------+------------------------------------------------------------------------------------------------------------+
|TAU_METRICS           |  TIME  |Setting to a comma separated list (TIME:PAPI_TOT_INS)							     |
+----------------------+--------+------------------------------------------------------------------------------------------------------------+



TAU Compile-Time Environment Variables
---------------------------------------


+---------------------------+------------------------------------------------------------------------------+
|Variable                   |Description                                                                   |
+===========================+==============================================================================+
|-optVerbose                |    Turn on verbose debugging messages                                        |
+---------------------------+------------------------------------------------------------------------------+
|-optCompInst               |    Use compiler based instrumentation                                        |
+---------------------------+------------------------------------------------------------------------------+
|-optNoCompInst             |    Do not revert to compiler instrumentation if source instrumentation fails |
+---------------------------+------------------------------------------------------------------------------+
|-optTrackIO                |    Wrap POSIX I/O call and calculate vol/bw of I/O operations                |
+---------------------------+------------------------------------------------------------------------------+
|-optKeepFiles              |    Do not remove .pdb and .inst.* files                                      |
+---------------------------+------------------------------------------------------------------------------+
|-optPreProcess             |    Preprocess Fortran sources before instrumentation                         |
+---------------------------+------------------------------------------------------------------------------+
|-optTauSelectFile="<file>" |    Specify selective instrumentation file for tau_instrumentor               |
+---------------------------+------------------------------------------------------------------------------+
|-optTwauWrapFile="<file>"  |    Specify path to link_options.tau generated by tau_gen_wrapper             |
+---------------------------+------------------------------------------------------------------------------+
|-optHeaderInst             |    Enable instrumentation of headers                                         |
+---------------------------+------------------------------------------------------------------------------+
|-optLinking=""             |    Options passed to the linker                                              |
+---------------------------+------------------------------------------------------------------------------+
|-optCompile=""             |    Options passed to the compiler 					   |
+---------------------------+------------------------------------------------------------------------------+
|-optPdtF95Opts=""          |    Add options to the Fortran parser in PDT                                  |
+---------------------------+------------------------------------------------------------------------------+
|-optPdtF95Reset=""         |    Reset options for Fortran parser in PDT                    		   |
+---------------------------+------------------------------------------------------------------------------+
|-optPdtCOpts=""            |    Options for C parser in PDT                                               |
+---------------------------+------------------------------------------------------------------------------+
|-optPdtCXXOpts=""          |    Options for C++ parser in PDT                                             |
+---------------------------+------------------------------------------------------------------------------+

For the following examples, we'll use the MiniWeather application https://github.com/mrnorman/miniWeather

Prepare the application:
------------------------

.. code::

	git clone https://github.com/mrnorman/miniWeather.git
	cd miniWeather/c/
	cp Makefile.summit Makefile


Compile the application:
------------------------

We'll use the PGI compiler, this application supports serial, MPI, MPI+OpenMP, and MPI+OpenACC

.. code::

	module load pgi
	module load parallel-netcdf

- Different compilations:

.. code::

	make serial
	make mpi
	make openmp
	make openacc


In order to use TAU for each case, follow the instructions below:


Preparation
===========


- Edit the makefile and replace *mpic++* with *tau_cxx.sh*

- TAU works with makefiles to declare what programming models are expected from the application:
        The available makefiles are located inside TAU installation:

.. code::

        module show tau
        ---------------------------------------------------------------
           /sw/summit/modulefiles/core/tau/2.28.1:
        ---------------------------------------------------------------
        whatis("TAU 2.28.1 github ")
        setenv("TAU_DIR","/sw/summit/tau/tau2//ibm64linux")
        prepend_path("PATH","/sw/summit/tau/tau2//ibm64linux/bin")
        help([[https://www.olcf.ornl.gov/software_package/tau
        ]])


The available Makefiles are named with the used compiler and are located in:

.. code::

        ls /sw/summit/tau/tau2//ibm64linux/lib/Makefile.tau-pgi*
        /sw/summit/tau/tau2//ibm64linux/lib/Makefile.tau-pgi-papi-mpi-cupti-pdt-openmp-pgi
        /sw/summit/tau/tau2//ibm64linux/lib/Makefile.tau-pgi-papi-mpi-cupti-pdt-pgi
        /sw/summit/tau/tau2//ibm64linux/lib/Makefile.tau-pgi-papi-pdt-pgi
        /sw/summit/tau/tau2//ibm64linux/lib/Makefile.tau-pgi_memory_manager-papi-mpi-cupti-pdt-pgi


Instrumenting the serial version of MiniWeather:
================================================


- For a serial application we should not declare a Makefile with a programming model such as MPI, OpenMP. However, as the source code includes MPI header that are not excluded during the compilation of the serial version, we should declare a Makefile with MPI. Moreover, with TAU_OPTIONS below, we add options to the linker.

.. code::

	module load tau
	export TAU_MAKEFILE=/sw/summit/tau/tau2//ibm64linux/lib/Makefile.tau-pgi-papi-mpi-cupti-pdt-pgi
	export TAU_OPTIONS='-optLinking=-lpnetcdf -optVerbose'
	make serial

- Add to your submission script the TAU variables that you want to use (or uncomment the below). By default the TAU will apply profiling and not tracing.

.. code::

	#PAPI metrics
	#export TAU_METRICS=TIME:PAPI_TOT_INS:PAPI_TOT_CYC

	# Instrument the callpath
	export TAU_CALLPATH=1
	export TAU_CALLPATH_DEPTH=10

	#Activate tracing
	#export TAU_TRACE=1

	time jsrun -n 1 -r 1 -a 1 -c 1 -g 1  ./miniWeather_serial


- When the execution finishes, there is one folder for each TAU_METRICS declaration with the format MULTI__
	- If you do not declare the TAU_METRICS variable, then by default is used the TIME and the profiling files are not in a folder When the execution ends, there will be one file per process, called profile.X.Y.Z, in this case is just one file, called profile.0.0.0

- We can export a text file with some information through pprof tool or visualize through paraprof


.. code::

	pprof profile.0.0.0
	Reading Profile files in profile.*

	NODE 0;CONTEXT 0;THREAD 0:
	---------------------------------------------------------------------------------------
	%Time    Exclusive    Inclusive       #Call      #Subrs  Inclusive Name
        	      msec   total msec                          usec/call
	---------------------------------------------------------------------------------------
	100.0        0.038     1:10.733           1           1   70733442 .TAU application
	100.0            9     1:10.733           1        4654   70733404 int main(int, char **)
 	 97.1           15     1:08.668        4501       27006      15256 void perform_timestep(double *, double *, double *, double *, double)
	 97.1        1,167     1:08.653       27006       54012       2542 void semi_discrete_step(double *, double *, double *, double, int, double *, double *)
 	 48.4       34,240       34,240       13503           0       2536 void compute_tendencies_z(double *, double *, double *)
 	 46.9       33,199       33,199       13503           0       2459 void compute_tendencies_x(double *, double *, double *)
  	  2.5          224        1,752         151       33361      11608 void output(double *, double)
	  1.7        1,211        1,211         604         604       2006 MPI_File_write_at_all()
  	  0.4           36          250           1      100003     250708 void init(int *, char ***)
	...


	USER EVENTS Profile :NODE 0, CONTEXT 0, THREAD 0
	---------------------------------------------------------------------------------------
	NumSamples   MaxValue   MinValue  MeanValue  Std. Dev.  Event Name
	---------------------------------------------------------------------------------------
      	      1058    1.6E+05          4  9.134E+04  7.919E+04  MPI-IO Bytes Written
       	       454        284          4      5.947       13.2  MPI-IO Bytes Written : int main(int, char **) => void output(double *, double) => MPI_File_write_at()
       	       604    1.6E+05    1.6E+05    1.6E+05          0  MPI-IO Bytes Written : int main(int, char **) => void output(double *, double) => MPI_File_write_at_all()
              1058       9412     0.1818       3311       3816  MPI-IO Write Bandwidth (MB/s)
               454      1.856     0.1818     0.5083     0.1904  MPI-IO Write Bandwidth (MB/s) : int main(int, char **) => void output(double *, double) => MPI_File_write_at()
               604       9412      2.034       5799       3329  MPI-IO Write Bandwidth (MB/s) : int main(int, char **) => void output(double *, double) => MPI_File_write_at_all()
               755          8          8          8          0  Message size for all-reduce
               302  2.621E+05          4  1.302E+05  1.311E+05  Message size for broadcast
	---------------------------------------------------------------------------------------


- Explanation:
	- One one process was runnign as it is a seriial application, even MPI calls are executed from single thread.
        - The total execution time is 70.733 seconds and only 9 msec are the exclusive for the main routine and the rest are caused by subroutines
	- The exclusive time is the time caused by the mentioned routine and the inclusive is with the executin time from the subroutines 
	- The #Subrs is the number of the called subroutines
	- There is also information about the parallel I/O if any exists, the bytes and the bandwidth.


We will present paraprof tool for the MPI version of the MiniWeather.

Instrumenting the MPI version of MiniWeather:
================================================

- For the MPI version we should use a makefile with MPI. The conpilation could fail if the makefile supports MPI+OpenMP but the code doesn't include any OpenMP calls. Moreover, with TAU_OPTIONS below, we add options to the linker.

.. code::

        module load tau
        export TAU_MAKEFILE=/sw/summit/tau/tau2//ibm64linux/lib/Makefile.tau-pgi-papi-mpi-cupti-pdt-pgi
        export TAU_OPTIONS='-optLinking=-lpnetcdf -optVerbose'
        make mpi

- Add to your submission script the TAU variables that you want to use (or uncomment the below). By default the TAU will apply profiling and not tracing.

.. code::

        #PAPI metrics
        export TAU_METRICS=TIME:PAPI_TOT_INS:PAPI_TOT_CYC

        # Instrument the callpath
        export TAU_CALLPATH=1
        export TAU_CALLPATH_DEPTH=10

        #Activate tracing
        #export TAU_TRACE=1

        time jsrun -n 64 -r 8 -a 1 -c 1   ./miniWeather_mpi


- When the execution finishes, there is one folder for each TAU_METRICS declaration with the format MULTI__
        - If you do not declare the TAU_METRICS variable, then by default is used the TIME and the profiling files are not in a folder When the execution ends, there will be one file per process, called profile.X.Y.Z.

- In order to use paraprof to visualize the data, your ssh connection should support X11 forward.

- Pack the profiling data with a name that you want and execute paraprof

.. code::

	paraprof --pack name.ppk
	paraprof name.ppk

Paraprof
========

- The first window that opens shows the experiment and the used metrics (TIME, PAPI_FP_OPS, PAPI_TOT_INS, PAPI_TOT_CYC)

.. image:: /images/tau_paraprof_manager.png
   :align: center

- The second window that is automatic loaded, shows the TIME metric for each process (they are called nodes), each color is a different call. Each hoorizontal line is a process or Std.Dev./mean/max/min



.. image:: /images/tau_mpi_time.png
   :align: center


- Select Options -> Uncheck Stack Bars Toogether
	- It is easier to check the load imbalance across the processes

.. image:: /images/tau_mpi_stack_bars.png
   :align: center

- If you click on any color, then a new window opens with information about the specific routing

.. image:: /images/tau_mpi_click_color.png
   :align: center

- If you click on the label (node 0, node 1, max, etc.) you can see the value across each routine in your application.

.. image:: /images/tau_mpi_sort_time.png
   :align: center


- If you do right click on the label (node 0, node 1, max, etc.) you can select "Show Context Event Window" (with callpath activated) 

.. image:: /images/tau_mpi_context_event.png
   :align: center

- Options -> Show Derived Metric Panel, select the metrics and then operator and then click Apply. Then uncheck the Show Derived Metric

.. image:: /images/tau_mpi_derived_metric.png
   :align: center

- Click on the new metric, PAPI_TOT_INS/PAPI_TOT_CYC

.. image:: /images/tau_mpi_ipc.png
   :align: center

- Click on the label mean:

.. image:: /images/tau_mpi_mean_ipc.png
   :align: center

For the non-MPI routines/calls, the IPC that is lower than 1.5 means that there is a potential for performance improvement.

- Menu Windows -> 3D Visualization (3D demands OpenGL)
- Exclusive Time and Exclusive Floating operations


.. image:: /images/tau_mpi_3d_fp_ops.png
   :align: center

- Menu Windows -> 3D Visualization (3D demands OpenGL)
- Exclusive Time and Exclusive Total Instructions

.. image:: /images/tau_mpi_3d_tot_ins.png
   :align: center

You can explore the various options

Which loops consume most of the time?
=====================================

- Create a file called for example select.tau with the content:

.. code::

	BEGIN_INSTRUMENT_SECTION
	loops routine="#"
	END_INSTRUMENT_SECTION

Then declare the options

.. code::

	export TAU_OPTIONS="-optTauSelectFile=select.tau -optLinking=lpnetcdf -optVerbose"

- Do not forget to unset TAU_OPTIONS when not necessary
- Execute as previously


- Now you can see the duration of all the loops

.. image:: /images/tau_mpi_loops1.png
   :align: center


- Select Options -> Select Metric… -> Exclusive… -> PAPI_TOT_INS/PAPI_TOT_CYC

.. image:: /images/tau_mpi_loops2.png
   :align: center

The loops with less than 1.5 IPC can be improved.
