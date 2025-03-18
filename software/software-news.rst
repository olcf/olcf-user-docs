
*************
Software News
*************

This page lists significant changes to software provided on OLCF systems. The
most recent changes are listed first.

----

Frontier: Core Module (March 18, 2025)
------------------------------------------------

On March 18, 2025, a new version of the ``Core`` module, ``Core/25.03``, was provided on Frontier. Note that the default ``Core`` remains ``Core/24.07`` at this time.
Please test this module and report any issues to help@olcf.ornl.gov.

The table below summarizes the main version changes.

.. csv-table::
    :header: "Component", "Old Version", "New Version"

    "ccache", "4.6.3", "4.10.2"
    "cmake", "3.27.9", "3.30.5"
    "darshan-util", "3.4.4", "3.4.6"
    "emacs", "29.3", "29.4"
    "gdb", "14.1", "15.2"
    "git-lfs", "3.3.0", "3.5.1"
    "git", "2.45.1", "2.47.0"
    "go", "1.22.2", "1.23.2"
    "gsl", "2.7.1", "2.8"
    "htop", "3.2.2", "3.3.0"
    "hwloc", "2.9.1", "2.11.1"
    "imagemagick", "7.1.1-29", "7.1.1-39"
    "julia", "1.10.2", "1.11.0"
    "libjpeg-turbo", "3.0.0", "3.0.3"
    "linaro-forge", "24.0.2", "24.0.6"
    "mercurial", "6.6.3", "6.7.3"
    "nano", "7.2", "8.2"
    "ninja", "1.11.1", "1.12.1"
    "openblas", "0.3.26", "0.3.28"
    "parallel", "20220522", "20240822"
    "python", "3.11.7", "3.13.0"
    "r", "4.4.0", "4.4.1"
    "tau", "N/A", "2.34"
    "vim", "9.0.0045", "9.1.0437"
    "wget", "1.21.3", "1.24.5"

Other packages provided by ``Core/25.03`` are ``autoconf``, ``bazel``, ``bear``, ``exuberant-ctags``, ``gmake``, ``gnupg``,
``gnuplot``, ``googletest``, ``hpctoolkit``, ``libpng``, ``libzmq``, ``papi``, ``pkgconf``, ``screen``, ``subversion``, ``tmux``, and ``zlib``.
These packages' versions have not changed from ``Core/24.07`` to ``Core/25.03``.
If you use a package not listed here, and it was provided by ``Core/24.07``, please contact help@olcf.ornl.gov.

Frontier: System Software Update (February 18, 2025)
----------------------------------------------------

The Frontier system was upgraded to a new version of the system software stack.

.. warning:: **Codes should be rebuilt** prior to running following the upgrade due to the OS and software changes.

As a result of the upgrade, the following packages are now default:

.. csv-table::
    :header: "Package", "Previous Default", "New Default"

    "ROCm", "5.7.1", "6.2.4"
    "HPE/Cray Programming Environment (CPE)", "23.12", "24.11"
    "Cray Compiler Environment (CCE)", "17.0.0", "18.0.1"
    "GNU Compiler Collection (GCC)", "12.3.0", "13.2.0"
    "AMD Compiler (AMD)", "5.7.1", "6.2.4"
    "libfabric", "1.20.1", "1.22.0"

As part of this upgrade, the libfabric/1.15.2.0 module has also be removed, as a new libfabric version, 1.22.0, is available.
Version 1.20.1 is retained, as libfabric/1.22.0 is not compatible with cray-mpich modules prior to 8.1.28.

Please see the `Frontier System Updates post <https://docs.olcf.ornl.gov/systems/frontier_user_guide.html#id17>`_ for further information about this upgrade.

Please contact help@olcf.ornl.gov if you encounter any issues or have questions.

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

   <p style="font-size:20px"><b>Summit: System Software Upgrade (January 24, 2024)</b></p>

The Summit system was upgraded to a new version of the system software stack.  

.. warning:: **Codes should be rebuilt** prior to running following the upgrade due to the OS and software changes.

As a result of the upgrade, the following new packages are now default:

.. csv-table::
    :header: "Package", "Previous Default", "New Default"

    "CUDA Toolkit", "11.0.3", "11.7.1"
    "IBM Spectrum MPI", "10.4.0.3-20210112", "10.4.0.6-20230210"
    "IBM XL", "16.1.1-10", "16.1.1-13"
    "GCC", "9.1.0", "12.1.0"

Please note the previous software stack remains available and can be accessed by loading the ``DefApps-2023`` modulefile. For convenience, a ``DefApps-2024`` is also provide to restore the most recent version of packages. From the ``DefApps-2023`` environment, users can load the ``DefApps-2024`` modulefile or start a fresh login to reset the environment to the latest versions.

In addition, OpenCE 1.10 is now available for Python 3.9 and 3.11. OpenCE 1.10 is available by loading the ``open-ce/1.10.0-py39-ibm`` or ``open-ce/1.10.0-py311-ibm`` modulefiles. Please note that each environment includes a differesent set of Python packages as outlined below.

.. csv-table::
    :header: "Python 3.9 Package", "Version"

    "pytorch", "2.0.1"
    "pytorch-lightning", "2.0.1"
    "pytorch-lightning-bolts", "0.6.0"
    "torchdata", "0.4.1"
    "torchmetrics", "0.11.4"
    "torchvision", "0.15.2"
    "torchvision-base", "0.15.2"
    "sentencepiece", "0.1.97"
    "horovod", "0.28.0"

.. csv-table::
    :header: "Python 3.11 Package", "Version"

    "tensorboard", "2.13.0"
    "tensorflow", "2.13.0"
    "tensorflow-datasets", "4.9.2"
    "tensorflow-estimator", "2.13.0"
    "tensorflow-hub", "0.14.0"
    "tensorflow-metadata", "1.13.1"
    "tensorflow-model-optimization", "0.7.5"
    "tensorflow-probability", "0.20.0"
    "tensorflow-text", "2.13.0"
    "pytorch", "2.0.1"
    "pytorch-base", "2.0.1"
    "pytorch-lightning", "2.0.9"
    "pytorch-lightning-bolts", "0.7.0"
    "torchtext", "0.15.2"
    "torchvision", "0.15.2"
    "onnx", "1.14.0"
    "keras", "2.13.1"
    "xgboost", "1.7.6"
    "tokenizers", "0.15.0"
    "transformers", "4.37.0"
    "sentencepiece", "0.1.97"
    "horovod", "0.28.0"
    "dali", "1.28.0"
    "opencv", "4.8.0"

Please contact help@olcf.ornl.gov if you encounter any issues or have questions.

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

   <p style="font-size:20px"><b>Summit: Darshan Runtime 3.4.0-lite (December 28, 2022)</b></p>

The default version of Darshan Runtime has been updated on Summit to version 3.4.0-lite and is available via the `darshan-runtime/3.4.0-lite` modulefile. In addition, the default version for the companion set of tools provided in Darshan Util has been updated to `darshan-util/3.4.0`. Please note that `darshan-util/3.4.0` is required to properly parse logs generated with `darshan-runtime/3.4.0-lite`.

.. csv-table::
    :header: "Package", "Version"


    "darshan-runtime", "3.4.0-lite"
    
----

.. raw:: html

   <p style="font-size:20px"><b>Summit: OpenCE 1.5.2 (March 17, 2022)</b></p>

OpenCE 1.5.2 is now available on Summit. OpenCE 1.5.2 is available for python versions 3.9, 3.8, and 3.7. These builds can be accessed by
loading the open-ce/1.5.2-py39-0, open-ce/1.5.2-py38-0, and open-ce/1.5.2-py37-0 modules, respectively.

The following packages are available in this release of OpenCE:

.. csv-table::
    :header: "Package", "Version"


    "Tensorflow", "2.7.1"
    "TensorFlow Estimators", "2.7.0"
    "TensorFlow Probability", "0.15.0"
    "TensorBoard", "2.7.0"
    "TensorFlow Text", "2.7.3"
    "TensorFlow Model Optimizations", "0.7.0"
    "TensorFlow Addons", "0.15.0"
    "TensorFlow Datasets", "4.4.0"
    "TensorFlow Hub", "0.12.0"
    "TensorFlow MetaData", "1.5.0"
    "PyTorch", "1.10.2"
    "TorchText", "0.11.2"
    "TorchVision", "0.11.3"
    "PyTorch Lightning", "1.5.10"
    "PyTorch Lightning Bolts", "0.5.0"
    "ONNX", "1.10.2"
    "Keras", "2.7.0"
    "Magma", "2.5.4"
    "XGBoost", "1.5.2"
    "Transformers", "4.11.3"
    "Tokenizers", "0.10.3"
    "SentencePiece", "0.1.96"
    "Spacy", "3.2.1"
    "OpenCV", "4.5.5"
    "DALI", "1.9.0"
    "Horovod", "0.23.0"
    
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

   <p style="font-size:20px"><b>Summit: OpenCE 1.5.0 (December 29, 2021)</b></p>

OpenCE 1.5.0 is now available on Summit. OpenCE 1.5.0 is available for python versions 3.7, 3.8, and 3.9. These builds can be accessed by
loading the ``open-ce/1.5.0-py37-0``, ``open-ce/1.5.0-py38-0``, and ``open-ce/1.5.0-py39-0`` modules, respectively.

The following packages are available in this release of OpenCE:

.. csv-table::
    :header: "Package", "Version"

    "Tensorflow", "2.7.0"
    "TensorFlow Estimators", "2.7.0"
    "TensorFlow Probability", "0.15.0"
    "TensorBoard", "2.7.0"
    "TensorFlow Text", "2.7.0"
    "TensorFlow Model Optimizations", "0.7.0"
    "TensorFlow Addons", "0.15.0"
    "TensorFlow Datasets", "4.4.0"
    "TensorFlow Hub", "0.12.0"
    "TensorFlow MetaData", "1.0.0"
    "PyTorch", "1.10.0"
    "TorchText", "0.11.0"
    "TorchVision", "0.11.1"
    "PyTorch Lightning", "1.5.4"
    "PyTorch Lightning Bolts", "0.4.0"
    "ONNX", "1.10.2"
    "Keras", "2.7.0"
    "Magma", "2.5.4"
    "XGBoost", "1.5.1"
    "Transformers", "4.11.3"
    "Tokenizers", "0.10.3"
    "SentencePiece", "0.1.96"
    "Spacy", "3.2.0"
    "Thinc", "8.0.13"
    "OpenCV", "4.5.3"
    "DALI", "1.9.0"
    "Horovod", "0.23.0"

.. raw:: html

    Please note that Tensorflow Serving is currently unavailable. We are working with IBM to
    resolve the issue and will publish and update once available.

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

   <p style="font-size:20px"><b>Summit: OpenCE 1.4.0 (October 13, 2021)</b></p>

OpenCE 1.4.0 is now available on Summit. OpenCE 1.4.0 is available for python versions 3.7, 3.8, and 3.9. These builds can be accessed by
loading the ``open-ce/1.4.0-py37-0``, ``open-ce/1.4.0-py38-0``, and ``open-ce/1.4.0-py39-0`` modules, respectively.  

The following packages are available in this release of OpenCE:

.. csv-table::
    :header: "Package", "Version"

    "Tensorflow", "2.6.0"
    "TensorFlow Estimators", "2.6.0"
    "TensorFlow Probability", "0.14.0"
    "TensorBoard", "2.6.0"
    "TensorFlow Text", "2.6.0"
    "TensorFlow Model Optimizations", "0.6.0"
    "TensorFlow Addons", "0.14.0"
    "TensorFlow Datasets", "4.4.0"
    "TensorFlow Hub", "0.12.0"
    "TensorFlow MetaData", "1.0.0"
    "PyTorch", "1.9.0"
    "TorchText", "0.10.0"
    "TorchVision", "0.10.0"
    "PyTorch Lightning", "1.4.4"
    "PyTorch Lightning Bolts", "0.3.4"
    "ONNX", "1.7.0"
    "Keras", "2.6.0"
    "Magma", "2.5.4"
    "XGBoost", "1.4.2"
    "Transformers", "4.9.2"
    "Tokenizers", "0.10.3"
    "SentencePiece", "0.1.91"
    "Spacy", "3.1.2"
    "Thinc", "8.0.8"
    "OpenCV", "3.4.14"
    "Horovod", "0.22.1"
    
.. raw:: html
    
    Please note that DALI and Tensorflow Serving are currently unavailable on ppc64le. We are working with IBM to
    resolve the issue and will publish and update once available.

----

.. raw:: html

   <p style="font-size:20px"><b>Summit: Software Installation/Default Software Changes (August 17-19, 2021)</b></p>

Summit's operating system will be upgraded to Red Hat Enterprise Linux 8 (RHEL 8) on August 17-19, 2021.  

.. warning:: **Codes should be rebuilt** prior to running following the upgrade due to the OS and software changes.

As a result of the upgrade, the following new packages will become available:

.. csv-table::
    :header: "Package", "Current Default", "New Default"

    "CUDA Toolkit", "10.1.243", "11.0.3"
    "IBM Spectrum MPI", "10.3.1.2-20200121", "10.4.0.3-20210112"
    "IBM XL", "16.1.1-5", "16.1.1-10"
    "IBM ESSL", "6.1.0-2", "6.3.0"

.. note::  The **OS-provided Python will no longer be accessible as python** (including variations like */usr/bin/python* or */usr/bin/env python*); rather, you must specify it as *python2* or *python3*. If you are using python from one of the modulefiles rather than the version in */usr/bin*, this change should not affect how you invoke python in your scripts, although we encourage specifying *python2* or *python3* as a best practice.

In addition, the following packages will be upgraded to newer versions and the specific versions listed below will be removed from the system. If you need any of the specific versions scheduled to be removed, please contact help@olcf.ornl.gov.

.. csv-table::
    :header: "Package", "Versions Removed", "Versions Available"    
    
    "adios", "1.11.1, 1.13.1", "None"
    "adios2", "2.2.0, 2.4.0, 2.5.0", "2.6.0"
    "amgx", "2.0.0.130.0, 2.0.0.130.1, 2.0.0.130.2", "2.1.0-1"
    "apr", "1.6.2", "1.7.0"
    "apr-util", "1.6.0", "1.6.1"
    "automake", "1.16.1", "1.16.2"
    "binutils", "2.31.1", "2.33.1"
    "bison", "3.0.5", "3.6.4"
    "boost", "1.59.0, 1.61.0, 1.66.0, 1.70.0", "1.62.0, 1.72.0, 1.74.0"
    "bzip2", "1.0.6", "1.0.8"
    "c-blosc", "1.12.1", "1.17.0"
    "cairo", "1.14.12", "1.16.0"
    "ccache", "3.7.9", "3.7.11"
    "cmake", "3.11.3, 3.12.2, 3.13.4, 3.14.2, 3.15.2, 3.17.3, 3.18.1, 3.18.2, 3.6.1", "3.18.4"
    "cuda", "9.1.85, 9.2.148, 10.1.105, 10.1.168, 10.1.243, 11.0.1, 11.0.2, 11.1.0", "10.2.89, 11.0.3, 11.1.1"
    "curl", "7.60.0, 7.63.0", "7.72.0"
    "darshan-runtime", "3.1.5-pre1, 3.1.6, 3.1.7", "3.2.1"
    "darshan-util", "3.1.4, 3.1.5-pre1, 3.1.6, 3.1.7", "3.2.1"
    "emacs", "25.1", "27.1"
    "essl", "6.2.0-20190419", "6.1.0-2, 6.2.1, 6.3.0"
    "expat", "2.2.5", "2.2.10"
    "flex", "2.6.3", "2.6.4"
    "font-util", "1.3.1", "1.3.2"
    "fontconfig", "2.12.3", "2.13.92"
    "freetype", "2.7.1, 2.9.1", "2.10.1"
    "gcc", "4.8.5, 5.4.0, 6.4.0, 7.4.0, 8.1.0, 8.1.1, 9.1.0, 9.2.0, 10.1.0", "8.3.1 (OS), 9.3.0, 10.2.0, 11.1.0"
    "gdb", "8.0, 8.2", "9.2"
    "gdbm", "1.14.1", "1.18.1"
    "gdrcopy", "2.0", "2.1"
    "gettext", "0.19.8.1", "0.21"
    "git", "2.13.0, 2.20.1, 2.9.3", "2.29.0"
    "git-lfs", "2.8.0", "None"
    "glib", "2.56.2, 2.56.3", "2.66.2"
    "gnupg", "2.2.3", "2.2.19"
    "go", "1.11.5", "1.15.2"
    "go-bootstrap", "1.7.1-bootstrap", "None"
    "gobject-introspection", "1.49.2", "1.56.1"
    "gperf", "3.0.4", "3.1"
    "gromacs", "2020, 2020.2", "2020.4"
    "harfbuzz", "1.4.6, 2.1.3", "2.6.8"
    "hdf5", "1.10.3, 1.10.4, 1.8.18", "1.10.7"
    "help2man", "1.47.4", "1.47.11"
    "hpx", "1.3.0, 1.4.1", "1.5.1"
    "htop", "2.0.2", "3.0.2"
    "hwloc", "2.0.2", "1.11.11, 2.2.0"
    "hypre", "2.11.1, 2.13.0, 2.15.1, develop", "2.20.0"
    "icu4c", "58.2, 60.1", "67.1"
    "julia", "1.4.2", "1.5.2"
    "kokkos", "3.0.00", "3.2.00"
    "kokkos-nvcc-wrapper", "20200221", "3.2.00"
    "libassuan", "2.4.5", "2.5.3"
    "libbsd", "0.8.6, 0.9.1", "0.10.0"
    "libevent", "2.0.21", "2.1.8"
    "libfabric", "1.7.0", "1.11.0"
    "libffi", "3.2.1", "3.3"
    "libgcrypt", "1.8.1", "1.8.5"
    "libgpg-error", "1.27", "1.37"
    "libiconv", "1.15", "1.16"
    "libjpeg-turbo", "1.5.90", "2.0.4"
    "libksba", "1.3.5", "1.4.0"
    "libpciaccess", "0.13.5", "0.16"
    "libpng", "1.6.34", "1.6.37"
    "libsigsegv", "2.11", "2.12"
    "libsodium", "1.0.15", "1.0.18"
    "libtiff", "4.0.9", "4.1.0"
    "libunwind", "1.2.1", "1.4.0"
    "libx11", "1.6.5", "1.6.7"
    "libxext", "1.3.3", "None"
    "libxml2", "2.9.8", "2.9.10"
    "libxrender", "0.9.10", "None"
    "libzmq (renamed from zeromq)", "4.2.5", "4.3.2"
    "log4c", "1.2.4", "None"
    "lz4", "1.8.1.2", "1.9.2"
    "magma", "2.1.0, 2.2.0, 2.3.0, 2.4.0, 2.5.1, 2.5.4", "2.5.3"
    "mercurial", "3.9.1, 4.4.1", "5.3"
    "mpip", "3.4.1, 3.4.1-1", "3.5"
    "mumps", "5.0.1", "5.3.3"
    "nano", "2.6.3", "4.9"
    "nasm", "2.13.03", "2.15.05"
    "nco", "4.6.9, 4.8.1, 4.9.1", "4.9.3"
    "ncurses", "6.1", "6.2"
    "netcdf-c (renamed from netcdf)", "4.6.1, 4.6.2", "4.7.4"
    "netcdf-cxx (renamed to netcdf-cxx4)", "4.2", "4.3.1"
    "netcdf-fortran", "4.4.4", "4.4.5"
    "netlib-scalapack", "2.0.2", "2.1.0"
    "npth", "1.5", "1.6"
    "numactl", "2.0.11", "2.0.14"
    "openblas", "0.3.5, 0.3.6, 0.3.9", "0.3.12"
    "open-ce", "1.1.3", "1.2.0"
    "openmpi", "4.0.3", "4.0.5"
    "papi", "5.5.1, 5.6.0, 5.7.0", "6.0.0.1"
    "parallel-netcdf", "1.8.0, 1.8.1", "1.12.1"
    "patchelf", "0.9", "0.10"
    "pcre", "8.42", "8.44"
    "perl", "5.26.2", "5.30.1"
    "petsc", "3.10.1, 3.10.3, 3.6.3, 3.6.4, 3.7.2", "3.14.1"
    "pgi", "17.10, 17.9, 18.1, 18.10, 18.3, 18.4, 18.5, 18.7, 19.1, 19.10, 19.4, 19.5, 19.7, 19.9, 19.10", "20.1, 20.4"
    "pixman", "0.34.0, 0.38.0", "0.40.0"
    "pkgconf (renamed from pkg-config)", "1.4.2, 1.5.4", "1.7.3"
    "py-certifi", "2017.1.23", "2020.6.20"
    "py-cython", "0.28.3, 0.29", "0.29.21"
    "py-docutils", "0.13.1", "0.15.2"
    "py-h5py", "2.8.0", "None"
    "py-mpi4py", "3.0.0", "3.0.3"
    "py-nose", "1.3.7", "None"
    "py-numpy", "1.15.1", "1.19.4"
    "py-pip", "10.0.1", "None"
    "py-pkgconfig", "1.2.2", "None"
    "py-pygments", "2.2.0", "2.6.1"
    "py-setuptools", "40.2.0, 40.4.3", "50.3.2"
    "py-six", "1.11.0", "None"
    "py-virtualenv", "16.0.0", "None"
    "python", "2.7.15-anaconda2-5.3.0, 3.6.6-anaconda3-5.3.0, 3.7.0-anaconda3-5.3.0, 2.7.12, 3.5.2, 3.7.0", "2.7.15, 3.7.7, 3.8.6"
    "r", "3.5.2", "4.0.5"
    "raja", "0.1.0", "0.12.1"
    "rdma-core", "20", "32.0"
    "readline", "6.3, 7.0", "8.0"
    "renderproto", "0.11.1", "None"
    "scons", "3.0.1", "3.1.2"
    "screen", "4.3.1", "4.8.0"
    "snappy", "1.1.7", "1.1.8"
    "spectral", "20181227, 20190401, 20200714, 20200903", "20210514"
    "spectrum-mpi", "10.2.0.10-20181214, 10.2.0.11-20190201, 10.2.0.7-20180830, 10.3.0.0-20190419, 10.3.0.1-20190611, 10.3.1.2-20200121", "10.4.0.3-20210112"
    "sqlite", "3.23.1, 3.26.0", "3.33.0"
    "subversion", "1.9.3", "1.14.0"
    "superlu-dist", "4.3, 5.1.3, 5.4.0", "6.4.0"
    "sz", "1.4.10.0, 1.4.12.3", "2.0.2.0, 2.1.11"
    "tar", "1.30, 1.31", "1.32"
    "tcl", "8.6.8", "None"
    "tk", "8.6.8", "None"
    "tmux", "2.2", "3.1b"
    "ucx", "1.7.0", "None"
    "udunits (renamed from udunits2)", "2.2.24", "None"
    "valgrind", "3.11.0, 3.14.0", "3.15.0"
    "vim", "7.4.2367, 8.1.0338", "8.2.1201"
    "xl", "16.1.1-4, 16.1.1-5, 16.1.1-6, 16.1.1-7, 16.1.1-9", "16.1.1-8, 16.1.1-10"
    "xz", "5.2.4", "5.2.5"
    "zfp", "0.5.0, 0.5.2", "0.5.5"
    "zstd", "1.3.0", "1.4.5"

----

.. raw:: html

   <p style="font-size:20px"><b>Summit: Software Installation/Default Software Changes (April 7, 2021)</b></p>

The following modules were installed as default on April 7, 2021.

.. csv-table::
    :header: "Package", "Current Default", "New Default"

    "open-ce", "0.1-0", "1.1.3-py38-0"

In addition, open-ce 1.1.3 is also available for python versions 3.6 and 3.7. These builds can be accessed by
loading the ``open-ce/1.1.3-py36-0`` and ``open-ce/1.1.3-py37-0`` modules, respectively.

The following packages are available in this release of open-ce.

.. csv-table::
    :header: "Package", "Version"

    "Tensorflow", "2.4.1"
    "TensorFlow Serving", "2.4.1"
    "TensorFlow Estimators", "2.4.0"
    "TensorFlow Probability", "0.12.1"
    "TensorBoard", "2.4.1"
    "TensorFlow Text", "2.4.1"
    "TensorFlow Model Optimizations", "0.5.0"
    "TensorFlow Addons", "0.11.2"
    "TensorFlow Datasets", "4.1.0"
    "TensorFlow Hub", "0.10.0"
    "TensorFlow MetaData", "0.26.0"
    "PyTorch", "1.7.1"
    "TorchText", "0.8.1"
    "TorchVision", "0.8.2"
    "PyTorch Lightning", "1.1.0"
    "PyTorch Lightning Bolts", "0.2.5"
    "XGBoost", "1.3.3"
    "Transformers", "3.5.1"
    "Tokenizers", "0.9.3"
    "SentencePiece", "0.1.91"
    "Spacy", "2.3.4"
    "Thinc", "7.4.1"
    "DALI", "0.28.0"
    "OpenCV", "3.4.10"
    "Horovod", "0.21.0"

----

.. raw:: html

   <p style="font-size:20px"><b>Summit: Software Installation/Default Software Changes (April 8, 2020)</b></p>

The following modules were installed as default on April 8, 2020.

.. csv-table::
    :header: "Package", "Current Default", "New Default"

    "ibm-wml-ce", "1.7.0-1", "1.7.0-2"

The new IBM Watson Machine Learning (WML) Community Edition (CE) install adds
improvements to DDL including support for ``jsrun``.

----

.. raw:: html

   <p style="font-size:20px"><b>Summit: Software Installation/Default Software Changes (March 10, 2020)</b></p>

The following modules will be installed as default on March 10, 2020. The new
stack requires the latest version of Spectrum MPI and as a result, previous
versions have been deprecated.

.. csv-table::
    :header: "Package", "Current Default", "New Default"

    "cuda", "10.1.168", "10.1.243"
    "spectrum-mpi", "10.3.0.1-20190611", "10.3.1.2-20200121"
    "hdf5", "1.10.3", "1.10.4"
    "pgi", "19.4", "19.9"
    "xl", "16.1.1-3", "16.1.1-5"
    "ibm-wml-ce", "1.6.2-3", "1.7.0-1"

In addition, the following new packages have been installed and are available for use:

.. csv-table::
    :header: "Package", "New Version"

    "pgi", "20.1"
    "xl", "16.1.1-6"
    "kokkos", "3.0.0"

Finally, the FFTW installations on Summit for the XL compiler have been rebuilt
using ``-O2`` to address an issue observed when running the FFTW suite using
the default optimization options. All builds of the ``fftw`` package that use
the XL compiler have been rebuilt.

If you encounter any issues, please contact help@olcf.ornl.gov.

----

.. raw:: html

   <p style="font-size:20px"><b>Rhea: OpenMPI Upgrade (February 18, 2020)</b></p>

On February 18, 2020, Rhea’s default OpenMPI will be updated to version 3.1.4.
Due to underlying library changes that will be made on the same day, following
the change, all codes should be rebuilt against the updated version.

.. csv-table::
    :header: "Package", "Current Default", "New Default"

    "OpenMPI", "3.1.3", "3.1.4"


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

----

.. raw:: html

   <p style="font-size:20px"><b>Summit: Software Upgrade (July 16, 2019)</b></p>

The following modules will be installed and will become the default on July 16,
2019. The new stack requires Spectrum MPI 10.3 PTF 1 and as a result previous
versions of Spectrum MPI have been deprecated.

.. csv-table::
    :header: "Package", "Default"

    "cuda", "10.1.168"
    "spectrum-mpi", "10.3.0.1-20190716"

Details about the software stack upgrade can be found in the `IBM Service Pack 3.1 site <https://www.ibm.com/developerworks/community/wikis/home?lang=en#!/wiki/Welcome%20to%20High%20Performance%20Computing%20(HPC)%20Central/page/IBM%20HPC%20Clusters%20of%20Power%20Advanced%20Compute%20AC922%20Servers%20with%20NVIDIA%20Tesla%20V100%20SXM2%20%20GPUs%20with%20NVLink%20Service%20Pack%203.1?section=What's_Changed>`_ and the `Spectrum MPI 10.3.0.1 release notes <https://www.ibm.com/support/knowledgecenter/SSZTET_10.3/releasenotes/smpi_releasenotes.html>`_.

----

.. raw:: html

   <p style="font-size:20px"><b>Summit: Software Installation/Default Software Changes (May 21, 2019)</b></p>

The following modules will be installed as default on May 21, 2019. The new
stack requires Spectrum MPI 10.3 and as a result previous versions of Spectrum
MPI have been deprecated.

.. csv-table::
    :header: "Package", "Default"

	"xl", "16.1.1.3"
    "cuda", "10.1.105"
    "essl", "6.2.0-20190419"
    "spectrum-mpi", "10.3.0.0-20190419"

----

.. raw:: html

   <p style="font-size:20px"><b>Rhea: Default Software Changes (March 12, 2019)</b></p>

The following modules will become the default on March 12, 2019.

.. csv-table::
    :header: "Package", "Default"

    "intel", "19.0.0"
    "pgi", "18.10"
    "gcc", "6.2.0"
    "cuda", "10.0.3"
    "openmpi", "3.1.3"
    "anaconda", "5.3.0"
    "adios", "1.11.1"
    "atlas", "3.10.2"
    "boost", "1.67.0"
    "fftw", "3.3.8"
    "hdf5", "1.10.3"
    "nco", "4.6.9"
    "netcdf", "4.6.1"
    "netcdf-fortran", "4.4.4"
    "netcdf-cxx", "4.3.0"
    "parallel-netcdf", "1.8.0"

----

.. raw:: html

   <p style="font-size:20px"><b>Summit: Default Software Changes (March 12, 2019)</b></p>

The following modules will become the default on March 12, 2019.

.. csv-table::
    :header: "Package", "Current Default", "New Default"

    "spectrum-mpi", "unset", "10.2.0.11-20190201"
    "xl", "16.1.1-1", "16.1.1-2"
    "pgi", "unset", "18.10"

In addition, the following default Spectrum MPI settings will be changed to
address issues resolved with the February 19, 2019 software upgrade:

.. csv-table::
    :header: "Environment Variable", "Current Default", "New Default"

    "OMP_MCA_io", "romio314", "romio321"
    "OMPI_MCA_coll_ibm_xml_disable_cache", "1", "unset"
    "PAMI_PMIX_USE_OLD_MAPCACHE", "1", "unset"


