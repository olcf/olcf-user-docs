.. _software_list:

OLCF Software Inventory
***********************

OLCF provides a wide range of software modules for use on its systems.
See the `Module Usage Example`_ below for more information on how to use module commands.

.. raw:: html
   :file: software_list_group.html

Note: A module which has a ``Description: None`` may have more information using
``module help <package>``. An ``OUTDATED`` module is one that was not found in
the most recent scan, but has been seen previously in the last 60 days.  A
module with the tag ``e4s`` gets its Spack build recipe from the Extreme-Scale
Scientific Software Stack (E4S). 

|
.. _Module Usage Example:

**Module Usage Example**

Missing software? If there is a software package you would like, please let us
know by `submitting a ticket <https://www.olcf.ornl.gov/for-users/getting-started/submit-ticket/>`_.

* Search for a package: ``module spider <package>``
* Get a list of prerequisite modules:  ``module spider <package>/<version>``
* Get package information after loading prerequisites: ``module help <package>/<version>``
* Get general information on a package: ``module help <package>``


**Example:** To find an adaptive mesh refinement packages, search for ``amr``.
The search returns that the ``amrex`` package is available on several systems.
To find out how to use the package, log onto one of the systems, ``module spider
amrex`` and ``module spider amrex/22.11-gpu-mpi`` using the desired
version.  This will list any modules that may need to be preloaded to access the
package. Once the dependencies are loaded, the package can be loaded with
``module load amrex/22.11-gpu-mpi``.

.. code:: bash

   $ module spider amrex
   amrex:
      Versions:
         amrex/22.05-mpi
         amrex/22.11-gpu-mpi
         amrex/24.05-gpu-mpi
         amrex/24.05-mpi
   For detailed information about a specific module use the modules full name.
   For example:
      $ module spider Foo/1.2.3

   $ module spider amrex/22.11-gpu-mpi
   amrex:
      You will need to load all module(s) on one of the lines below before the 'amrex/22.11-gpu-mpi' module is available to load.
         amd/5.7.1  rocm/5.7.1  cray-mpich/8.1.28
         cce/17.0.0  rocm/5.7.1  cray-mpich/8.1.28
         gcc/12.3  rocm/5.7.1  cray-mpich/8.1.28

   # Load the prerequisites
   $ module load cce/17.0.0  rocm/5.7.1  cray-mpich/8.1.28
   # Load amrex
   $ module load amrex/22.11-gpu-mpi

   # General package informatiom
   $ module help amrex/22.11-gpu-mpi
   Name   : amrex
   Version: 22.11
   Target : zen3
   AMReX is a publicly available software framework designed for building
   massively parallel block- structured adaptive mesh refinement (AMR)
   applications.

   # Details about how this package was configured and installed
   $ module show amrex/22.11-gpu-mpi
   ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
      /sw/borg/spack-envs/modules/cce/17.0.0/cray-mpich-8.1.28/rocm-5.7.1/cce-17.0.0/amrex/22.11-gpu-mpi.lua:
   ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
   whatis("Name : amrex")
   whatis("Version : 22.11")
   whatis("Target : zen3")
   whatis("Short description : AMReX is a publicly available software framework designed for building massively parallel block- structured adaptive mesh refinement (AMR) app\
   lications.")
   whatis("Configure options : -DUSE_XSDK_DEFAULTS=ON -DAMReX_SPACEDIM:STRING=3 -DBUILD_SHARED_LIBS:BOOL=OFF -DAMReX_MPI:BOOL=ON -DAMReX_OMP:BOOL=OFF -DXSDK_PRECISION:STRING\
   =DOUBLE -DXSDK_ENABLE_Fortran:BOOL=OFF -DAMReX_FORTRAN_INTERFACES:BOOL=OFF -DAMReX_EB:BOOL=OFF -DAMReX_LINEAR_SOLVERS:BOOL=ON -DAMReX_AMRDATA:BOOL=OFF -DAMReX_PARTICLES:B\
   OOL=ON -DAMReX_PLOTFILE_TOOLS:BOOL=OFF -DAMReX_TINY_PROFILE:BOOL=OFF -DAMReX_HDF5:BOOL=OFF -DAMReX_HYPRE:BOOL=OFF -DAMReX_PETSC:BOOL=OFF -DAMReX_SUNDIALS:BOOL=OFF -DAMReX\
   _PIC:BOOL=OFF -DCMAKE_CXX_COMPILER=/opt/rocm-5.7.1/hip/bin/hipcc -DAMReX_GPU_BACKEND=HIP -DAMReX_AMD_ARCH=gfx90a")
   help([[Name   : amrex]])
   help([[Version: 22.11]])
   help([[Target : zen3]])
   ]])
   help([[AMReX is a publicly available software framework designed for building
   massively parallel block- structured adaptive mesh refinement (AMR)
   applications.]])
   prepend_path("LD_LIBRARY_PATH","/sw/borg/spack-envs/cpe23.12-gpu/opt/cce-17.0.0/amrex-22.11-xqkqdmrxybw5baodxr3dpqmg3z2rzjkl/lib")
   prepend_path("CMAKE_PREFIX_PATH","/sw/borg/spack-envs/cpe23.12-gpu/opt/cce-17.0.0/amrex-22.11-xqkqdmrxybw5baodxr3dpqmg3z2rzjkl/.")
   prepend_path("CMAKE_PREFIX_PATH","/sw/borg/spack-envs/cpe23.12-gpu/opt/cce-17.0.0/amrex-22.11-xqkqdmrxybw5baodxr3dpqmg3z2rzjkl/.")
   prepend_path("LD_LIBRARY_PATH","/opt/rocm-5.7.1/llvm/lib")
   setenv("OLCF_AMREX_ROOT","/sw/borg/spack-envs/cpe23.12-gpu/opt/cce-17.0.0/amrex-22.11-xqkqdmrxybw5baodxr3dpqmg3z2rzjkl")
