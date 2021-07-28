Summit
############################################

This example is intended for use on Summit with RHEL 7 as the OS.

Purpose
--------------------------------------------

This guide meant as an example for a user to setup a Spack environment for application development using the OLCF 
provided files as a template.

.. warning::

  The provided ``spack.yaml`` files are templates for a user to use as an example.

  This not intended as a guide for a new Spack user.  Please see `the Spack 101 tutorial <https://spack-tutorial.readthedocs.io/en/latest>`_
  if you need assistance starting out with Spack.

The provided Spack environment files are intended to assist OLCF users in setup their development environment at the 
OLCF.  The base environment file includes the compilers and packages that are installed at the system level.

Traditionally, the user environment is modified by module files.  For example, a user would add use  ``module load cmake/3.18.2`` to 
load CMake version 3.18.2 into their environment.  Using a Spack environment, a user can add an OLCF provided package
and build against it using Spack without having to load the module file separately.

The information presented here is a subset of what can be found at `the Spack documentation site <https://spack.readthedocs.io/>`_.

.. note:: 
  Definitions

  - Spack environment - A set of Spack specs for the purpose of building, rebuilding and deploying in a coherent fashion.

  - External Packages - An externally-installed package used by Spack, rather than building its own package.

Getting Started
--------------------------------------------

Clone the OLCF User Environment repo and the Spack repo, start a new Spack instance, and create and activate a new Spack environment:

.. code-block:: none

  ## From a Summit login

  > git clone https://code.ornl.gov/2ff/olcf-user-environments.git
  > cd olcf-user-environments

  > git clone https://github.com/spack/spack.git
  > source spack/share/spack/setup-env.sh

  > spack env create my_env linux-rhel7-ppc64le/summit/spack.yaml
  > spack env activate my_env

Now a user can add and install their dependencies with Spack and proceed with developing their application.

Add Dependencies to the environment
--------------------------------------------

Adding OLCF Installed Dependencies as External Packages
-------------------------------------------------------

If an OLCF installed package is available, these can be added via the ``spack.yaml`` file by adding to the ``packages``
section.  For this example, CMake was found on Summit by finding a modulefile for the installed CMake package.

By marking the CMake package as ``buildable: false`` it will force Spack to use the externally installed CMake with the 
listed modulefile.  If this is not indicated, Spack may build its own version of the package.

.. code-block:: none

  packages:
    # EXAMPLE
    cmake:
      version: [3.18.2]
      buildable: false
      externals:
      - spec: cmake@3.18.2
        modules:
        - cmake/3.18.2

Adding User-Defined Dependencies to the environment
-------------------------------------------------------

These can be added to the ``spack.yaml`` by adding to the ``specs`` section.  A dependency that is not already installed
will be built via Spack once the environment is concretized and installed.

.. code-block:: none

  specs:
  - cmake@3.18.2                            ## example from above
  - my_apps_dependency1@version%compiler    ## other explicitly defined specs
  - my_apps_dependency2@version%compiler

Installing the Environment
-------------------------------------------------------

When in the Spack environment, any packages that are added to the environment file can be installed via:

.. code-block:: none

  > spack concretize -f
  > spack install

Alternatively, a user may install a package manually by:

.. code-block:: none

  > spack install <my_app_dependencies@version%compiler>

More Details
********************************************

For more information regarding Spack and its usage, please see `the Spack documentation <https://spack.readthedocs.io>`_.

For an extensive tutorial concerning Spack, go to `the Spack 101 tutorial <https://spack-tutorial.readthedocs.io/en/latest>`_.

For more information concerning external packages, please see `here <https://spack.readthedocs.io/en/latest/build_settings.html#external-packages>`_.

References
********************************************
* `Spack <https://spack.readthedocs.io/>`_ - package management tool
* `Spack 101 tutorial <https://spack-tutorial.readthedocs.io/en/latest/>`_ - Spack tutorial

Authors
********************************************
* **Matt Belhorn** - *Initial work* `OLCF Spack Environments <https://github.com/mpbelhorn/olcf-spack-environments>`_
* **Jamie Finney**

