
*************
Software News
*************

This page lists significant changes to software provided on OLCF systems. The
most recent changes are listed first.

----

Frontier: Updated Modules for cpe/23.12 (October 16 2024)
---------------------------------------------------------

For the HPE/Cray Programming Environment 23.12 (cpe/23.12) on Frontier,
the table below lists packages that are updated or added.  New CPU packages
are netcdf, paraview, stat, tau, unifyfs, and visit.  New GPU packages
are ascent, blaspp, hwloc, lapackpp and paraview.
Please report any issues to help@olcf.ornl.gov.

.. csv-table::
    :header: "Package", "Version"

    "adios2", "2.10.0"
    "amrex", "24.5"
    "arborx", "1.6"
    "ascent", "0.9.2"
    "blaspp", "2023.11.5"
    "boost", "1.85.0"
    "cabana", "0.6.0"
    "chai", "2024.2.0"
    "darshan-runtime", "3.4.4"
    "dyninst", "13.0.0"
    "flecsi", "2.2.1"
    "flux-core", "0.61.2"
    "fortrilinos", "2.3.0"
    "gasnet", "2023.9.0"
    "ginkgo", "1.7.0"
    "globalarrays", "5.8.2"
    "hdf5", "1.14.3"
    "heffte", "2.4.0"
    "hpx", "1.9.1"
    "hwloc", "2.9.1"
    "hypre", "2.31.0"
    "kokkos", "4.3.00"
    "kokkos-kernels", "4.3.00"
    "lammps", "20230802.3"
    "lapackpp", "2023.11.05"
    "libunwind", "1.6.2"
    "magma", "2.8.0"
    "mfem", "4.6.0"
    "nco", "5.1.9"
    "netcdf-c", "4.9.2"
    "openpmd-api", "0.15.2"
    "papi", "7.1.0"
    "parallel-netcdf", "1.12.3"
    "paraview", "5.12.0"
    "parsec", "3.0.2209"
    "petsc", "3.21.1"
    "phist", "1.12.0"
    "plasma", "23.8.2"
    "plumed", "2.9.0"
    "raja", "2024.2.0"
    "slate", "2023.11.5"
    "slepc", "3.21.0"
    "stat", "4.2.1"
    "strumpack", "7.2.0"
    "suite-sparse", "7.3.1"
    "sundials", "7.0.0"
    "superlu-dist", "8.2.1"
    "swig", "4.1.1"
    "swig", "4.1.1-fortran"
    "sz", "2.1.12.5"
    "tasmanian", "8.0"
    "tau", "2.33.2"
    "trilinos", "15.1.1"
    "umpire", "2024.2.0"
    "unifyfs", "2.0"
    "upcxx", "2023.9.0"
    "visit", "3.3.3"
    "vtk-m", "2.1.0"

----

Frontier: Core Module (October 15, 2024)
------------------------------------------------

On October 15, 2024, the ``Core`` module on Frontier will be updated from ``Core/24.00`` to ``Core/24.07`` .  
Please test the new module and report issues to help@olcf.ornl.gov 

The table below summarizes the main version changes.

.. csv-table::
    :header: "Component", "Old Version", "New Version"

    "autoconf", "2.69", "2.72"
    "bazel", "4.0.0", "7.0.2"
    "ccache", "4.5.1", "4.6.3"
    "cmake", "3.23.2", "3.27.9"
    "darshan-util", "3.4.0", "3.4.4"
    "emacs", "28.1", "29.3"
    "gdb", "10.2", "14.1"
    "git-lfs", "2.11.0", "3.3.0"
    "gnupg", "2.3.4", "2.4.5"
    "gnuplot", "5.4.3", "6.0.0"
    "googletest", "1.10.0", "1.14.0"
    "hpctoolkit", "N/A", "2024.01.1"
    "htop", "3.0.2", "3.2.2"
    "hwloc", "2.5.0", "2.9.1"
    "imagemagick", "7.0.8-7", "7.1.1-29"
    "julia", "1.8.2", "1.10.2"
    "libzmq", "4.3.4", "4.3.5"
    "mercurial", "5.8", "6.6.3"
    "nano", "6.3", "7.2"
    "ninja", "1.10.2", "1.11.1"
    "openblas", "0.3.17", "0.3.26"
    "r", "1.7.0", "4.4.0"
    "screen", "4.8.0", "4.9.1"
    "subversion", "1.14.1", "1.14.2"
    "tmux", "3.2a", "3.4"
    "vim", "8.2.2541", "9.0.0045"

Other packages provided by ``Core/24.07`` are ``exuberant-ctags``, ``go``, ``hpctoolkit``, ``papi``, ``parallel``, and ``wget``. 
If you use a package not listed here, and was provided by ``Core/24.00``, please contact help@olcf.ornl.gov.

----

Frontier: System Software Update (July 16, 2024)
------------------------------------------------

The Frontier system will be upgraded to a new version of the system software stack.  

.. warning:: **Codes should be rebuilt** prior to running following the upgrade due to the OS and software changes.

As a result of the upgrade, the following packages are now default:

.. csv-table::
    :header: "Package", "Previous Default", "New Default"

    "ROCm", "5.3.0", "5.7.1"
    "HPE/Cray Programming Environment (CPE)", "22.12", "23.12"
    "Cray Compiler Environment (CCE)", "15.0.0", "17.0.0"
    "GNU Compiler Collection (GCC)", "12.2.0", "12.3.0"
    "AMD Compiler (AMD)", "5.3.0", "5.7.1"

In addition to the default modules changing, the layout of the modules for the OLCF provided software stack will change.
Going forward our core software (i.e., software independent of compiler type/version) will be in a default module
called ``Core`` with the version being in the format `year/month`. Additionally explicit suffixes have been added to modules to indicate MPI, OpenMP, and GPU support. 
All modules that depend on ROCm are suffixed with ``-gpu``. The same is true for packages with mpi ``-mpi`` and
openmp ``-omp``. Software is built to target CPE releases based on compiler (e.g., cce, amd, or gcc), cray-mpich, and ROCm versions.
If you have an :ref:`unsupported combination <understanding-the-compatibility-of-compilers-rocm-and-cray-mpich>` of those modules you may not see certain parts of the normal software stack.

Please contact help@olcf.ornl.gov if you encounter any issues or have questions.

----

Frontier: User Environment Changes (July 9, 2024)
-------------------------------------------------

The following packages will be retired from the system on Tuesday July 9, 2024:

.. csv-table::
    :header: "Package", "Version"

    "ROCm", "4.5.2, 5.1.0, 5.2.0"
    "CPE", "22.06"
    "CCE", "14.0.1"
    "Cray MPICH", "8.1.17"
    "Cray LibSci", "21.08.1.2"
    "aml", "0.2.0"
    "argobots", "1.1"
    "bolt", "2.0"
    "butterflypack", "2.0.0, 2.1.0, 2.1.1"
    "caliper", "2.7.0"
    "conduit", "0.7.2, 0.8.2, 0.8.3"
    "datatransferkit", "3.1-rc3, 3.1rc3-gpu"
    "faodel", "1.2108.1"
    "flit", "2.1.0"
    "gmp", "6.2.1"
    "gotcha", "1.0.3"
    "legion", "21.03.0"
    "libquo", "1.3.1"
    "loki", "0.1.7"
    "mercury", "2.0.1, 2.1.0"
    "metall", "0.17, 0.20"
    "mpark-variant", "1.4.0"
    "mpifileutils", "0.11, 0.11.1"
    "nccmp", "1.9.0.1"
    "papyrus", "1.0.1, 1.0.2"
    "pdt", "3.25.1"
    "precice", "2.3.0-cpu, 2.4.0-cpu, 2.3.0, 2.4.0-cpu"
    "pumi", "2.2.6, 2.2.7"
    "qthreads", "1.16"
    "turbine", "1.3.0"
    "umap", "2.1.0"
    "veloc", "1.5"
    "zfp", "0.5.5"

If your workloads require a package listed above, please contact the OLCF User Assistance team at help@olcf.ornl.gov as soon as possible. 

----

.. raw:: html

   <p style="font-size:20px"><b>Frontier and Crusher: System Software Upgrade (January 23, 2024)</b></p>

The Crusher TDS and Frontier systems were upgraded to a new version of the system software stack. This stack introduces ROCm 6.0.0 and HPE/Cray Programming Environment 23.12. For more information, please see:

-  `Crusher System Updates <https://docs.olcf.ornl.gov/systems/crusher_quick_start_guide.html#system-updates>`_.
-  `Frontier System Updates <https://docs.olcf.ornl.gov/systems/frontier_user_guide.html#system-updates>`_.

Please contact help@olcf.ornl.gov with any issues or questions.

----

.. raw:: html

   <p style="font-size:20px"><b>Frontier and Crusher: System Software Upgrade (July 18, 2023)</b></p>

The Crusher TDS and Frontier systems were upgraded to a new version of the system software stack. This stack introduces ROCm 5.5.1 and HPE/Cray Programming Environment 23.05. For more information, please see:

-  `Crusher System Updates <https://docs.olcf.ornl.gov/systems/crusher_quick_start_guide.html#system-updates>`_.
-  `Frontier System Updates <https://docs.olcf.ornl.gov/systems/frontier_user_guide.html#system-updates>`_.

Please contact help@olcf.ornl.gov with any issues or questions.
    
----

.. raw:: html

   <p style="font-size:20px"><b>Frontier: Darshan Runtime 3.4.0 (May 10, 2023)</b></p>

The Darshan Runtime modulefile ``darshan-runtime/3.4.0`` on Frontier is now loaded by default. This module will allow users to profile the I/O of their applications with minimal impact. The logs are available to users on the Orion file system in ``/lustre/orion/darshan/<system>/<yyyy>/<mm>/<dd>``. 

Unloading `darshan-runtime` modulefile is recommended for users profiling their applications with other profilers to prevent conflicts.

Please make a note of this change and contact help@olcf.ornl.gov with any issues or questions.

.. csv-table::
    :header: "Package", "Version"


    "darshan-runtime", "3.4.0"
    
----

.. raw:: html

   <p style="font-size:20px"><b>Ascent: Software Installation/Default Software Changes (February 7-11, 2022)</b></p>

Ascent's operating system was upgraded to Red Hat Enterprise Linux 8 (RHEL 8) on February 7-11, 2022.  

.. warning:: **Codes should be rebuilt** prior to running following the upgrade due to the OS and software changes.

As a result of the upgrade, the following new packages became available:

.. csv-table::
    :header: "Package", "Current Default", "New Default"

    "CUDA Toolkit", "10.1.243", "11.0.3"
    "IBM Spectrum MPI", "10.3.1.2-20200121", "10.4.0.3-20210112"
    "IBM XL", "16.1.1-5", "16.1.1-10"
    "IBM ESSL", "6.1.0-2", "6.3.0"

.. note::  The **OS-provided Python will no longer be accessible as python** (including variations like */usr/bin/python* or */usr/bin/env python*); rather, you must specify it as *python2* or *python3*. If you are using python from one of the modulefiles rather than the version in */usr/bin*, this change should not affect how you invoke python in your scripts, although we encourage specifying *python2* or *python3* as a best practice.

----

.. raw:: html

   <p style="font-size:20px"><b>Andes: OS Upgrade (November 30, 2021)</b></p>

On November 30, 2021, the Andes cluster will be upgraded to a newer (minor) version of the operating system. The table below summarizes the main changes. While recompiling is not required, it is recommended.   

.. csv-table::
    :header: "Component", "Old Version", "New Version"

    "Red Hat Enterprise Linux", "8.3", "8.4"
     "Mellanox InfiniBand Driver", "5.3-1.0.0.1", "5.4-1.0.3.0"
     "NVIDIA driver", "450.36.06", "460.106.00-1"
     "Slurm", "20.02.6", "20.02.7-1"

----

.. raw:: html

   <p style="font-size:20px"><b>All Systems: Python2 End of Life (January 01, 2020)</b></p>

On January 1, 2020, Python 2 will reach its end of life and will no longer be
supported by the project’s core developers. On this date, the OLCF will also
end its support for Python 2. Users reliant on Python 2 should port code to
Python 3 for forward compatibility with OLCF systems and many open source
packages. Python 2 modules will not be removed on January 1, but will no longer
receive maintenance or regular updates.

While default Python modules on OLCF systems are already set to Python 3, we
recommend all users follow PEP394 by explicitly invoking either ‘python2’ or
‘python3’ instead of simply ‘python’. Python 2 Conda Environments and user
installations of Python 2 will remain as options for using Python 2 on OLCF
systems.

Official documentation for porting from Python 2 to Python3 can be found at:
`<https://docs.python.org/3/howto/pyporting.html>`_

General information and a list of open source packages dropping support for
Python 2 can be found at: `<https://python3statement.org/>`_



