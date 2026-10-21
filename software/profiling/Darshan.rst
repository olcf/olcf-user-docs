:tocdepth: 3

*******
Darshan
*******

Overview
--------

Darshan is a lightweight I/O characterization tool for HPC applications. It records concise application-level file use, access patterns, and I/O statistics during job execution. 
Darshan generates a log file for each instrumented application run, which can be summarized using command-line tools or analyzed in-depth using Python packages. Darshan profiling
requires zero code changes and minimal-to-no setup on OLCF systems. By default, if your code was instrumented with the Darshan-runtime library, the log files can be found at ``/lustre/orion/darshan/frontier/YYYY/M/D/``.

Darshan can instrument applications at compile time or, for dynamically linked executables, at runtime using ``LD_PRELOAD``.
If using one of the Cray-provided compiler wrappers (e.g., ``cc``, ``CC``, or ``ftn``), the darshan-runtime library may automatically be linked during compilation. 
You can verify if your executable is already linked to darshan-runtime by running ``ldd`` on your executable and looking for ``libdarshan.so*``.

Darshan provides insight into I/O statistics for POSIX, STDIO, MPI-IO, and HDF5 file access patterns. Additionally, you can visualize per-rank I/O activity
and easily compare I/O performance as you scale your application.

.. note::

    HDF5 profiling is not enabled on any OLCF-provided darshan-runtime module. If you are interested in using Darshan to profile
    HDF5 I/O, please see the Darshan installation `instructions <https://darshan.readthedocs.io/en/latest/darshan-runtime/doc/darshan-runtime.html#:~:text=library-,Conventional%20installation,-%EF%83%81>`_
    or reach out to help@olcf.ornl.gov for build instructions.

Usage
-----

If using a Cray-provided compiler, darshan-runtime will automatically be linked during compilation. The specific version of Darshan
that is linked depends on the ``cce`` module that is used. Darshan does automatic profiling of your code at runtime, with more advanced
I/O profiling metrics provided by the :ref:`runtime_config`.

If you have a dynamic executable that is not compiled with the Darshan library, the system-provided Darshan library can still be enabled by
preloading the library files like so ``LD_PRELOAD="$OLCF_DARSHAN_RUNTIME_ROOT/lib/libdarshan.so" "$LIBFABRIC_PATH/libfabric.so"``.

.. warning::
    
    To prevent runtime errors, it may be required to ``LD_PRELOAD`` libfabric.so with the Darshan library file. The ``$LIBFABRIC_PATH``
    can be discovered by running ``module show libfabric`` and grabbing the full path to the libfabric.so file under the ``$LD_LIBRARY_PATH``
    given by the ``module show`` output.

.. _runtime_config:

Runtime Configuration
---------------------

The full list of runtime configuration variables that can modify Darshan profiling behavior can be found at the 
`Darshan Runtime Configuration <https://darshan.readthedocs.io/en/latest/darshan-runtime/doc/darshan-runtime.html#:~:text=Darshan%20library%20config%20settings>`_ documentation page.
A non-exhaustive list of Darshan variables that OLCF users may find useful include:

+-----------------------------------------+-----------------------------------------------------------------------------+
| Environment Variable                    | Description                                                                 |
+=========================================+=============================================================================+
| ``DARSHAN_ENABLE_NONMPI=1``             | Enables profiling of non-MPI applications (e.g., OpenMP-only or Python)     | 
+-----------------------------------------+-----------------------------------------------------------------------------+
| ``DARSHAN_INTERNAL_TIMING=1``           | Prints Darshan startup and finalize cost to stderr.                         |
+-----------------------------------------+-----------------------------------------------------------------------------+
| ``DARSHAN_MOD_ENABLE=<csv>``            | Controls which modules are used for profiling. Options include              |
|                                         | ``LUSTRE``, ``POSIX``, ``STDIO``, ``MPI-IO``, ``DXT_POSIX``, ``DXT_MPIIO``, |
|                                         | ``H5F``, ``H5D``                                                            |
+-----------------------------------------+-----------------------------------------------------------------------------+
| ``DXT_ENABLE_IO_TRACE=1``               | Enables Darshan extended tracing for finer I/O profiling.                   |
|                                         | Deprecated in some Darshan versions in favor of ``DARSHAN_MOD_ENABLE``      |
+-----------------------------------------+-----------------------------------------------------------------------------+
| ``DARSHAN_CONFIG_PATH=<config_path>``   | A custom Darshan config file will be used for additional Darshan            |
|                                         | configuration option. Note: some runtime configurations can only            |
|                                         | be enabled in this file (e.g., ``MAX_RECORDS``).                            |
+-----------------------------------------+-----------------------------------------------------------------------------+ 

.. warning::

    Caution should be exercised when ``LD_PRELOAD``'ing Darshan and using ``DARSHAN_ENABLE_NONMPI=1``. This will create
    a Darshan log for every command that is executed after this configuration is enabled. E.g., unintentionally creating logs
    for bash commands like ``ls``. Therefore, it is recommended ``DARSHAN_ENABLE_NONMPI=1`` be set on the launch line only and **not**
    enabled globally in the environment.

    ✅ ``DARSHAN_ENABLE_NONMPI=1 srun -N 10 -ntasks-per-node=8 -c 7 example.py``

    ❌ ``export DARSHAN_ENABLE_NONMPI=1``


Analysis
--------

Darshan-util
^^^^^^^^^^^^

You can access a suite of command line tools to analyze Darshan logs quickly and easily by loading the ``darshan-util`` module. 
The primary tool of interest is ``darshan-parser`` which simply takes a Darshan log file as input. The default output behavior
for ``darshan-parser`` is to print job metadata, mounted filesystems, and file access statics for every I/O event that occurred during application runtime.
This information is quite verbose and is best used for a programmatic post-processing workflows. For full-details about the sub-fields
of the ``darshan-parser`` output, please see the `documentation <https://darshan.readthedocs.io/en/latest/darshan-util/doc/darshan-util.html#:~:text=Guide%20to%20darshan%2Dparser%20output>`_.
Instead, it is recommended to use ``darshan-parser`` with one of the summary flags such as ``darshan-parser --perf log.darshan`` for human-readability.

Additionally, a similar command called ``darshan-dxt-parser`` can be used if Darshan eXtended Tracing (DXT) was enabled. This will display
information gathered by the DXT enabled modules (e.g, ``DXT_POSIX`` and ``DXT_MPIIO``). In general, DXT provides finer I/O information
such as the Lustre OST the files reside, the thread ID and/or the MPI rank that performed the I/O operation, etc.

.. note::

    By default, Orion uses a progressive file layout (PFL) when creating new directories or files. Depending on the Darshan-runtime module used, support for PFL may
    or may not exist, and the OST information may not be present in the Darshan logs. If it is essential for you to have this information, consider creating a static
    layout by using ``lfs setstripe`` and creating a new output directory with the required layout.

Finally, ``darshan-diff`` can be used to compare the metadata and access pattern differences between 2 darshan log files.

PyDarshan
^^^^^^^^^

`PyDarshan <https://darshan.readthedocs.io/en/latest/darshan-util/pydarshan/docs/usage.html>`_ is a Python library that simplifies analysis of Darshan log files. 
It offers modules that print summary statistics to the terminal; functionalities to produce json, yaml, or html graphical outputs of I/O statistics; and offers an interface
to easily integrate Darshan information into existing Python workflows. To get started you can install PyDarshan in a Python environment.

.. code:: bash

    module load miniforge3
    conda create -n darshan python=3.13 -y
    conda activate darshan
    pip install darshan

To generate an html document for easily understanding I/O profiles, activate your Darshan environment and use the ``darshan summary``
command.

.. code:: bash
    
    # Generate an html file of your Darshan I/O profile
    python -m darshan summary log.darshan

    # Optionally if DXT was enabled
    python -m darshan summary --enable_dxt_heatmap log.darshan

View an example summary report at the following link:

* https://www.mcs.anl.gov/research/projects/darshan/docs/example_report.html

DXT-Explorer
^^^^^^^^^^^^

If DXT modules were used, the DXT-Explorer Python library may be useful. Using this library, interactive html plots can be generated
to discover unbalanced I/O workloads, straggling ranks, spatiality of I/O operations, and much more. For complete details,
please see the documentation page `here <https://dxt-explorer.readthedocs.io/en/latest/exploring.html>`_.

Installation and usage are simple:

.. code:: bash

    # Installation using the conda environment previously created
    pip install dxt-explorer

    # Generate an interactive plot
    dxt-explorer log.darshan

Interactive examples of generated output can be found here:

* https://jeanbez.gitlab.io/pdsw-2021/

Common Issues
-------------

#. **A Darshan log file was generated, but it does not contain I/O profiling information.**
    This most commonly occurs with Python applications or with nested executions. Often the solution is to preface the specific launch line with ``DARSHAN_ENABLE_NONMPI=1``.
#. **Darshan warns the log contains incomplete information.**
    This can happen for a number of reasons. Most often you'll encounter this because the program did not cleanly close or you exhaust Darshan's default number of trackable records. 
    If your program is not exiting cleanly, please refer to :ref:`software_debugging`. 
    Otherwise, Darshan should provide hints as to what records are being exhausted. Consider increasing the number of trackable
    records for a given module (e.g, ``MAX_RECORDS DXT_POSIX 2048``) or remove file tracing for I/O in uninteresting directories
    (e.g., ``NAME_EXCLUDE /tmp/* DXT_POSIX,DXT_MPIIO``).
#. **I have the Darshan runtime module loaded, but a darshan log is not generated.**
    Double check the darshan library is linked to your compiled executable using ``ldd`` and looking for ``libdarshan.so``. If it's not 
    there, the simplest solution is to ``LD_PRELOAD`` the Darshan library files and rerun your application.






