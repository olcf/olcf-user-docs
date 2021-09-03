******************
E4S Software Stack
******************

The `Extreme-scale Scientific Software Stack (E4S) <https://e4s-project.github.io/>`_ 
is a community effort to provide open source software packages for developing, deploying,
and running scientific applications on high-performance computing (HPC) platforms. 
E4S provides from-source builds and containers of a broad collection of HPC software
packages.

For information about the software packages included in the E4S project,
visit https://e4s-project.github.io/Resources/ProductInfo.html

.. note::
  The packages installed on Summit include only those that meet OLCF policy
  requirements for facility-provided software; build successfully on Summit's
  hardware architectures for a given toolchain and runtime environment; and are
  otherwise appropriate for use with the resource scheduler and communication
  fabrics supported by the OLCF.

  Therefore, not all the packages in the E4S project collection are necessarily
  provided by the OLCF nor are these packages necessarily configured the same way
  for each toolchain and runtime environment

Summit
######

The E4S software list is installed along side the existing software on Summit and
can be access via ``lmod`` modulefiles.  There is also a metamodule file to load the
entire available subset of the 20.10 and 21.02 (in development) release for GCC 6.4.0.

Access via modulefiles
----------------------

To access the installed software, load the desired compiler via:

::

  module load < compiler/version >
  .. ie ..
  module load gcc/9.1.0
  .. or ..
  module load gcc/7.5.0

Then use ``module avail`` to see the installed list of packages.

..
  Access via metamodules
  ----------------------

  To load the currently installed E4S stack on Summit:

  ::

  module load gcc/9.1.0
  module load e4s/20.10
  .. or ..
  module load e4s/21.02  ## in development


List of installed packages on Summit for GCC 9.1.0 (E4S release 21.05):

.. csv-table::
  :header: "Software Name", "Loaded Version", "Module Name"
  :widths: 20, 20, 20

  adios2, 2.7.1, adios2/2.7.1
  aml, 0.1.0, aml/0.1.0
  amrex, 21.05, amrex/21.05
  arborx, 1.0, arborx/1.0
  archer, 2.0.0, archer/2.0.0
  argobots, 1.1, argobots/1.1
  ascent, 0.7.1, ascent/0.7.1
  axom, 0.5.0, axom/0.5.0
  bolt, 2.0, bolt/2.0
  cabana, 0.3.0, cabana/0.3.0
  caliper, 2.4.0, caliper/2.4.0
  chai, 2.3.0, chai/2.3.0
  conduit, 0.7.2, conduit/0.7.2
  darshan-runtime, 3.3.0, darshan-runtime/3.3.0
  darshan-util, 3.3.0, darshan-util/3.3.0
  dyninst, 11.0.0, dyninst/11.0.0
  faodel, 1.1906.1, faodel/1.1906.1
  flecsi, 1.4, flecsi/1.4
  flit, 2.1.0, flit/2.1.0
  gasnet, 2020.3.0, gasnet/2020.3.0
  ginkgo, 1.13.0, ginkgo/1.13.0
  globalarrays, 5.8, globalarrays/5.8
  gotcha, 1.0.3, gotcha/1.0.3
  gmp, 6.2.1, gmp/6.2.1
  gotcha, 1.0.3, gotcha/1.0.3
  hdf5, 1.10.7, hdf5/1.10.7
  heffte, 2.0.0, heffte/2.0.0
  hpctoolkit, 2021.03.01, hpctoolkit/2021.03.01
  hpx, 1.6.0, "| hpx/1.6.0-cxx17 
  | hpx/1.6.0-cxx14-boost1.72.0 
  | hpx/1.6.0-cxx17-boost1.72.0"
  hypre, 2.20.0, hypre/2.20.0
  kokkos-kernels, 3.2.00, kokkos-kernels/3.2.00
  kokkos, 3.4.00, "| kokkos/3.4.00
  | kokkos/3.4.00-omp
  | kokkos/3.4.00-cudalambda"
  legion, 21.03.0, legion/21.03.0
  libquo, 1.3.1, libquo/1.3.1
  libunwind, 1.5.0, libunwind/1.5.0
  magma, 2.5.4, magma/2.5.4
  mercury, 2.0.1, mercury/2.0.1
  mpark-variant, 1.4.0, mpark-variant/1.4.0
  mpifileutils, 0.11, mpifileutils/0.11
  ninja, 1.10.2, ninja/1.10.2
  omega-h, 9.32.5, omega-h/9.32.5
  openpmd-api, 0.13.4, openpmd-api/0.13.4
  papi, 6.0.0.1, "| papi/6.0.0.1
  | papi/6/0/0/1-nogpu"
  papyrus, 1.0.1, papyrus/1.0.1
  parallel-netcdf, 1.12.1, parallel-netcdf/1.12.1
  pdt, 3.25.1, pdt/3.25.1
  petsc, 3.15.0, "| petsc/3.15.0
  | petsc/3.15.0-no_cuda"
  plasma, 20.9.20, plasma/20.9.20
  precice, 2.2.1, precice/2.2.1
  pumi, 2.2.5, pumi/2.2.5
  qt, 5.15.2, qt/5.15.2
  qthreads, 1.16, qthreads/1.16-distrib
  raja, 0.13.0, raja/0.13.0
  rempi, 1.1.0, rempi/1.1.0
  slate, 2021.5.2, slate/2021.05.2
  slepc, 3.15.0, slepc/3.15.0
  stc, 0.9.0, stc/0.9.0
  strumpack, 5.1.1, strumpack/5.1.1
  sundials, 5.7.0, sundials/5.7.0
  superlu, 5.2.1, superlu/5.2.1
  superlu-dist, 6.4.1, superlu-dist/6.4.1
  swig, 4.0.2, "| swig/4.0.2
  | swig/4.0.2-fortran"
  sz, 2.1.11.1, sz/2.1.11.1
  tasmanian, 7.5, tasmanian/7.5
  tau, 2.30.1, tau/2.30.1
  trilinos, 13.0.1, trilinos/13.0.1
  turbine, 1.3.0, turbine/1.3.0
  umap, 2.1.0, umap/2.1.0
  umpire, 4.1.2, umpire/4.1.2
  unifyfs, 0.9.2, unifyfs/0.9.2
  upcxx, 2021.3.0, upcxx/2021.3.0
  zfp, 0.5.5, zfp/0.5.5

Spock
#####

The E4S software list is installed along side the existing software on Spock and
can be access via ``lmod`` modulefiles.

Access via modulefiles
----------------------

To access the installed software, load the desired compiler via:

::

  module load < compiler/version >
  .. ie ..
  module load gcc/9.3.0
  .. or ..
  module load gcc/10.2.0

Then use ``module avail`` to see the installed list of packages.

As an example for GCC 10.2.0, the following modules are available.

.. csv-table::
  :header: "Software Module Name"
  :widths: 20

  adios2/2.7.1
  aml/0.1.0
  amrex/21.04
  bolt/2.0
  caliper/2.5.0
  dyninst/10.2.1
  faodel/1.1906.1
  flecsi/1.4
  flit/2.1.0
  gasnet/2020.3.0
  ginkgo/1.3.0
  globalarrays/5.8
  gotcha/1.0.3
  hdf5/1.10.7
  hpx/1.6.0
  kokkos-kernels/3.2.00
  legion/20.03.0
  libquo/1.3.1
  mercury/2.0.0
  mfem/4.2.0
  ninja/1.10.2
  openpmd-api/0.13.2
  papi/6.0.0.1
  papyrus/1.0.1
  pdt/3.25.1
  precice/2.2.0
  pumi/2.2.5
  qthreads/1.16
  raja/0.13.0
  slate/2020.10.00
  slepc/3.15.0
  sundials/5.7.0
  superlu/5.2.1
  superlu-dist/6.4.0
  swig/4.0.2-fortran
  sz/2.1.11.1
  tasmanian/7.3
  umap/2.1.0
  umpire/4.1.2
  zfp/0.5.5

