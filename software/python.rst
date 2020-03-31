.. _python:

***********************
Python on OLCF Systems
***********************

.. WIP/TODO: Warnings and Best Practices
  - Be cautions about initializing conda from shell init scripts (``~/.bashrc``,
    ``~/.profile``, ``~/.zshrc``, etc.)
  - Conda initialization scripts generally compatible only with ``bash/sh`` login
    shells.

    - Base distribution works with all shells, but conda generally only works with ``[ba]sh``

  - Avoid mixing incompatible/wrong-arch modules via ``PYTHONPATH`` pollution.
  - ``$HOME/.condarc`` in shared ``$HOME`` environments


Python_ is a highly-extensible, multi-paradigm, dynamically-type, interpreted
programming language. Python is designed to be easy to learn, easy to write. It
has a robust standard library, an extremely flexible extension framework, and a
comprehensive repository of extension packages. These features contribute to
Python's popularity among developers and the scientific community, but can also
lead to confusion and problems in a multi-user HPC environment where different
users require a variety of software versions, packages with differing
link-dependencies, and intend to run on multiple machine architectures.

.. _Python: https://www.python.org/doc/

This guide describes the different ways Python can be managed on OLCF resources
and solutions to common problems when using Python in HPC environments.


Overview
========

Python runtime environments are generally available through several means on
each OLCF resource.

Environment Modules
  Site-managed Python runtime environments via environment modules.
  Two flavors of Python distribution are typically available:

  - `Anaconda distributions`_ pre-loaded with commonly used extension packages.
  - `Source-built CPython interperetors`_ with a minimal set of extensions pre-loaded.

    .. _`Source-built CPython interperetors`:  `Native Python`_

OS Packages
  The OS-provided Python distribution installed as part of a node's OS image.

  - Only a limited number of extensions needed by OS components are generally
    pre-installed and available.
  - Python versions are limited.
  - Not easily extensible.

`Self-Installed`_
  Personal, self-installed python environments, either flavors of Anaconda or
  source builds of a python implementation such as CPython.

  .. _`Self-Installed`: `Self-Installed Python`_


Choosing which Python runtime best suits your needs depends largely on how your
project intends to use Python and Python-based applications.

For most casual uses involving common python extensions, choosing one of the stock
Anaconda distributions provided by environment modules is the simplest and
easiest way to get a complete python environment with the latest Python
versions. Environments may be customized and extended using *conda environments*
for situations where additional or specific-versions of extension packages are
needed.

Native builds of CPython are useful when your project must use extension
packages based on compiled C code with specific link-dependencies to external
compiled software that is not compatible with or supplied by libraries included
in an Anaconda distribution. In most cases where a native, non-Anaconda python
distribution is needed, it best to manage the runtime environment using either a
self-installed CPython distribution or a python ``virtualenv`` or ``python3 -m venv``.

Projects that use only scripts written in pure Python (ie, no compiled C-code
extensions) or only require modules from the Python standard library may find
that the OS-provided python distributions are sufficient for their needs.


Anaconda Distributions
======================

Anaconda Distributions are self-contained Python environments produced by
Anaconda Inc. (formerly Continuum Analytics) complete with a specialized package
manager, ``conda``, and backed by a comprehensive repository of pre-compiled
extensions and their dependencies.

Environment Modules
-------------------

The default ``python`` environment module on OLCF machines refers to a Python3
Anaconda distribution. Environment modules for Anaconda-based python are named
``python/{X}.{Y}.{Z}-anaconda{X}-{rel}`` where ``{X}.{Y}.{Z}`` refers to,
respectively, the major-, minor-, micro- version of the python interperetor in
the base Anaconda installation. The ``{rel}`` suffix indicates the Anaconda
release version at the time the module was deployed. Due to occasional in-place
upgrades, may not reflect the release version currently in use but serves to
differentiate multiple Anaconda installations of the same Python version. 

To list all the available python modules on a system, use:

.. code-block:: sh

    $ module avail python
    ---------- /sw/rhea/modulefiles/20180914/site/linux-rhel7-x86_64/Core ----------
       python/2.7.15    python/3.7.0

    -------------------------- /sw/rhea/modulefiles/core ---------------------------
       python/2.7.15-anaconda2-2018.12    python/3.7.0-anaconda3-2018.12 (D)

      Where:
       D:  Default Module

Only ``python`` modules that have the keyword ``anaconda`` in their name will
represent site-managed Anaconda distributions:

.. code-block:: sh

    $ module key anaconda
    ----------------------------------------------------------------------------

    The following modules match your search criteria: "anaconda"
    ----------------------------------------------------------------------------

      python: python/2.7.15-anaconda2-2018.12, python/3.7.0-anaconda3-2018.12

    ----------------------------------------------------------------------------

Load the environment module to put both the python interperetor and the
``conda`` package manager into your PATH:

.. code-block:: sh

    $ module load python  # or python/3.7.0-anaconda3-2018.12


Conda
-----

The ``conda`` utility is a specialized package manager for Anaconda
distributions. It combines the capabilities of the native Python package manager
``pip`` and the native Python virtual environment manager; ``python3 -m venv``
for Python3+ and ``virtualenv`` for Python2 and earlier.

Conda Environments
------------------

Self-Installed Conda Distributions
----------------------------------

See also `Self-Installed Python`_. 

Native Python
=============

Environment Modules
-------------------

Virtualenvs
-----------

Self-Installed Native Python
----------------------------

See also `Self-Installed Python`_. 


Self-Installed Python
=====================
