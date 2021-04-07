
*************
Software News
*************

This page lists significant changes to software provided on OLCF systems. The
most recent changes are listed first.

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


