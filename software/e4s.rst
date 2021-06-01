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

Access via modules
---------------------

To load the currently installed E4S stack on Summit:

::

  module load gcc/6.4.0
  module load e4s/20.10

List of installed packages:

.. csv-table::
  :header: "Software Name", "Loaded Version", "Module Name"
  :widths: 20, 20, 20

  adios2, 2.6.0, adios2/2.6.0
  bolt, 1.0, bolt/1.0
  caliper, 2.4.0, caliper/2.4.0
  dyninst, 10.2.1, dyninst/10.2.1
  faodel, 1.1906.1, faodel/1.1906.1
  flit, 2.1.0-py3, flit/2.1.0-py3
  gasnet, 2020.3.0, gasnet/2020.3.0
  ginkgo, 1.13.0, ginkgo/1.13.0
  globalarrays, 5.7, globalarrays/5.7
  gotcha, 1.0.3, gotcha/1.0.3
  hdf5, 1.10.6, hdf5/1.10.6
  hpctoolkit, 2020.08.03, hpctoolkit/2020.08.03
  hypre, 2.20.0, hypre/2.20.0
  kokkos-kernels, 3.2.00, kokkos-kernels/3.2.00
  kokkos, 3.2.00, kokkos/3.2.00-omp
  legion, 20.03.0, legion/20.03.0
  libquo, 1.3.1, libquo/1.3.1
  magma, 2.5.4, magma/2.5.4
  mercury, 1.0.1, mercury/1.0.1
  mpifileutils, 0.10.1, mpifileutils/0.10.1
  ninja, 1.10.1, ninja/1.10.1
  openpmd-api, 0.12.0, openpmd-api/0.12.0
  papi, 6.0.0.1, papi/6.0.0.1
  papyrus, 1.0.0, papyrus/1.0.0
  parallel-netcdf, 1.12.1, parallel-netcdf/1.12.1
  pdt, 3.25.1, pdt/3.25.1
  petsc, 3.14.0, petsc/3.14.0
  plasma, 20.9.20, plasma/20.9.20
  pumi, 2.2.2, pumi/2.2.2
  qthreads, 1.14, qthreads/1.14
  raja, 0.12.1, raja/0.12.1
  rempi, 1.1.0, rempi/1.1.0
  slepc, 3.14.0, slepc/3.14.0
  strumpack, 5.0.0, strumpack/5.0.0
  sundials, 5.4.0, sundials/5.4.0
  superlu-dist, 6.3.1, superlu-dist/6.3.1
  superlu, 5.2.1, superlu/5.2.1
  swig, 4.0.2, swig/4.0.2
  sz, 2.1.10, sz/2.1.10
  tasmanian, 7.3, tasmanian/7.3
  tau, 2.29.1, tau/2.29.1
  trilinos, 13.0.0, trilinos/13.0.0
  umap, 2.1.0, umap/2.1.0
  umpire, 4.0.1, umpire/4.0.1
  unifyfs, 0.9.0, unifyfs/0.9.0
  upcxx, 2020.3.0, upcxx/2020.3.0-py3
  veloc, 1.4, veloc/1.4
  zfp, 0.5.5, zfp/0.5.5
