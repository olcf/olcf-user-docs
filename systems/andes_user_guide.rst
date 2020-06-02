******
Andes
******

System Overview
===============

Andes is a replacement for the Rhea system. Andes has 8 login nodes, 704
compute nodes and 9 GPU nodes. The primary purpose of Andes is to provide a
conduit for large-scale scientific discovery via pre/post processing and
analysis of simulation data generated on Summit.  Users with accounts on Summit
will automatically be given access to Andes.

.. _andes-compute-nodes:

Compute nodes
-------------

Andes contains 704 compute nodes and 9 GPU nodes. Andes has two partitions:

+-------------+-------------+---------+-------------------+------------------------------------+
| Partition   | Node Count  | Memory  | GPU               | CPU                                |
+=============+=============+=========+===================+====================================+
| andes       | 704         | 256 GB  | N/A               | [2x] AMD EPYC 7302 16Core Processor|
| (default)   |             |         |                   | 3.0 GHz                            |   
|             |             |         |                   | (total 32 cores *per node*)        |
+-------------+-------------+---------+-------------------+------------------------------------+
| gpu         | 9           | 1 TB    | [2x]              | [2x] Intel\ |R| Xeon\ |R| E5-2695  |
|             |             |         | NVIDIA\ |R|       | @2.3 GHz - 14 cores, 28 HT         |
|             |             |         | K80               | (total 28 cores, 56 HT *per node*) |
+-------------+-------------+---------+-------------------+------------------------------------+

**Andes Partition**

The first 704 nodes make up the *andes* partition, where each node contains two
16-core 3.0 GHz AMD EPYC 7302 processors and 256GB of main memory.  Each CPU in
this partition features 16 physical cores, for a total of 32 physical cores per
node.

**GPU Partition**

Andes also has 9 large memory/GPU nodes, which make up the *gpu* partition.
These nodes each have 1TB of main memory and two NVIDIA K80 GPUs in addition to
two 14-core 2.30 GHz Intel Xeon processors with HT Technology. Each CPU in this
partition features 14 physical cores, for a total of 28 physical cores per
node.  With Hyper-Threading enabled, these nodes have 56 logical cores that can
execute 56 hardware threads for increased parallelism.

.. note::
    To access the gpu partition, batch job submissions should request ``-p gpu``.

Both compute partitions are accessible through the same batch queue from Andes' login nodes.


.. _andes-login-nodes:

Login nodes
-----------

Andes features 8 login nodes which are identical to the *andes* partition
compute nodes.  The login nodes provide an environment for editing, compiling,
and launching codes onto the compute nodes. All Andes users will access the
system through these same login nodes, and as such, any CPU- or
memory-intensive tasks on these nodes could interrupt service to other users.
As a courtesy, we ask that you refrain from doing any analysis or visualization
tasks on the login nodes.

For more information on connecting to OLCF resources, see :ref:`connecting-to-olcf`.

--------------

File systems
------------

The OLCF's center-wide :ref:`alpine-ibm-spectrum-scale-filesystem` name Alpine
is available on Andes for computational work.  An NFS-based file system provides
:ref:`user-home-directories-nfs` and :ref:`project-home-directories-nfs`.
Additionally, the OLCF's :ref:`hpss` provides archival spaces.

Shell and programming environments
==================================

OLCF systems provide hundreds of software packages and scientific libraries
pre-installed at the system-level for users to take advantage of. To facilitate
this, environment management tools are employed to handle necessary changes to
the shell dynamically. The sections below provide information about using the
management tools at the OLCF.

--------------

Default shell
-------------

A user's default shell is selected when completing the user account request
form. The chosen shell is set across all OLCF resources.  Currently, supported
shells include:

-  bash
-  tsch
-  csh
-  ksh

If you would like to have your default shell changed, please contact the
`OLCF user assistance center <https://www.olcf.ornl.gov/for-users/user-assistance/>`__ at
help@olcf.ornl.gov.

--------------

Environment management with lmod
--------------------------------

The *modules* software package allows you to dynamically modify your user
environment by using pre-written *modulefiles*. environment modules are provided
through `Lmod <https://lmod.readthedocs.io/en/latest/>`__, a Lua-based module
system for dynamically altering shell environments.  by managing changes to the
shell’s environment variables (such as ``path``, ``ld_library_path``, and
``pkg_config_path``), Lmod allows you to alter the software available in your
shell environment without the risk of creating package and version combinations
that cannot coexist in a single environment.

Lmod is a recursive environment module system, meaning it is aware of module
compatibility and actively alters the environment to protect against conflicts.
Messages to stderr are issued upon Lmod implicitly altering the environment.
Environment modules are structured hierarchically by compiler family such that
packages built with a given compiler will only be accessible if the compiler
family is first present in the environment.

    **note:** Lmod can interpret both Lua modulefiles and legacy Tcl
    modulefiles. However, long and logic-heavy Tcl modulefiles may require
    porting to Lua.


General usage
^^^^^^^^^^^^^

Typical use of Lmod is very similar to that of interacting with modulefiles on
other OLCF systems. The interface to Lmod is provided by the ``module`` command:

+----------------------------------+-----------------------------------------------------------------------+
| Command                          | Description                                                           |
+==================================+=======================================================================+
| module -t list                   | Shows a terse list of the currently loaded modules.                   |
+----------------------------------+-----------------------------------------------------------------------+
| module avail                     | Shows a table of the currently available modules                      |
+----------------------------------+-----------------------------------------------------------------------+
| module help <modulename>         | Shows help information about <modulename>                             |
+----------------------------------+-----------------------------------------------------------------------+
| module show <modulename>         | Shows the environment changes made by the <modulename> modulefile     |
+----------------------------------+-----------------------------------------------------------------------+
| module spider <string>           | Searches all possible modules according to <string>                   |
+----------------------------------+-----------------------------------------------------------------------+
| module load <modulename> [...]   | Loads the given <modulename>(s) into the current environment          |
+----------------------------------+-----------------------------------------------------------------------+
| module use <path>                | Adds <path> to the modulefile search cache and ``MODULESPATH``        |
+----------------------------------+-----------------------------------------------------------------------+
| module unuse <path>              | Removes <path> from the modulefile search cache and ``MODULESPATH``   |
+----------------------------------+-----------------------------------------------------------------------+
| module purge                     | Unloads all modules                                                   |
+----------------------------------+-----------------------------------------------------------------------+
| module reset                     | Resets loaded modules to system defaults                              |
+----------------------------------+-----------------------------------------------------------------------+
| module update                    | Reloads all currently loaded modules                                  |
+----------------------------------+-----------------------------------------------------------------------+

.. note::
    Modules are changed recursively. Some commands, such as
    ``module swap``, are available to maintain compatibility with scripts
    using Tcl Environment Modules, but are not necessary since Lmod
    recursively processes loaded modules and automatically resolves
    conflicts.

Searching for modules
^^^^^^^^^^^^^^^^^^^^^

Modules with dependencies are only available when the underlying dependencies,
such as compiler families, are loaded. Thus, ``module avail`` will only display
modules that are compatible with the current state of the environment. To search
the entire hierarchy across all possible dependencies, the ``spider``
sub-command can be used as summarized in the following table.

+----------------------------------------+------------------------------------------------------------------------------------+
| Command                                | Description                                                                        |
+========================================+====================================================================================+
| module spider                          | Shows the entire possible graph of modules                                         |
+----------------------------------------+------------------------------------------------------------------------------------+
| module spider <modulename>             | Searches for modules named <modulename> in the graph of possible modules           |
+----------------------------------------+------------------------------------------------------------------------------------+
| module spider <modulename>/<version>   | Searches for a specific version of <modulename> in the graph of possible modules   |
+----------------------------------------+------------------------------------------------------------------------------------+
| module spider <string>                 | Searches for modulefiles containing <string>                                       |
+----------------------------------------+------------------------------------------------------------------------------------+

 
Defining custom module collections
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Lmod supports caching commonly used collections of environment modules on a
per-user basis in ``$home/.lmod.d``. to create a collection called "NAME" from
the currently loaded modules, simply call ``module save NAME``. omitting "NAME"
will set the user’s default collection. Saved collections can be recalled and
examined with the commands summarized in the following table.

+-------------------------+----------------------------------------------------------+
| Command                 | Description                                              |
+=========================+==========================================================+
| module restore NAME     | Recalls a specific saved user collection titled "NAME"   |
+-------------------------+----------------------------------------------------------+
| module restore          | Recalls the user-defined defaults                        |
+-------------------------+----------------------------------------------------------+
| module reset            | Resets loaded modules to system defaults                 |
+-------------------------+----------------------------------------------------------+
| module restore system   | Recalls the system defaults                              |
+-------------------------+----------------------------------------------------------+
| module savelist         | Shows the list user-defined saved collections            |
+-------------------------+----------------------------------------------------------+

.. note::
    You should use unique names when creating collections to
    specify the application (and possibly branch) you are working on. For
    example, ``app1-development``, ``app1-production``, and
    ``app2-production``.

.. note::
    In order to avoid conflicts between user-defined collections
    on multiple compute systems that share a home file system (e.g.
    ``/ccs/home/[username]``), lmod appends the hostname of each system to the
    files saved in in your ``~/.lmod.d`` directory (using the environment
    variable ``lmod_system_name``). This ensures that only collections
    appended with the name of the current system are visible.

The following screencast shows an example of setting up user-defined module
collections on Summit. https://vimeo.com/293582400

--------------

Installed Software
------------------

The OLCF provides hundreds of pre-installed software packages and scientific
libraries for your use, in addition to taking `software installation requests
<https://www.olcf.ornl.gov/support/software/software-request/>`__. See the
`software <https://www.olcf.ornl.gov/for-users/software/>`__ page for complete
details on existing installs.

Compiling
=========

Compiling code on andes is typical of commodity or beowulf-style hpc linux
clusters.

Available compilers
-------------------

The following compilers are available on andes:

- `intel <https://www.olcf.ornl.gov/software_package/intel/>`__, intel composer xe (default)
- `pgi <https://www.olcf.ornl.gov/software_package/pgi/>`__, the portland group compilar suite
- `gcc <https://www.olcf.ornl.gov/software_package/gcc/>`__, the gnu compiler collection

Upon login, default versions of the intel compiler and openmpi (message passing
interface) libraries are automatically added to each user's environment. Users
do not need to make any environment changes to use the default version of intel
and openmpi.

--------------

Changing compilers
------------------

If a different compiler is required, it is important to use the correct
environment for each compiler. To aid users in pairing the correct compiler and
environment, the module system on andes automatically pulls in libraries compiled
with a given compiler when changing compilers. The compiler modules will load
the correct pairing of compiler version, message passing libraries, and other
items required to build and run code. To change the default loaded intel
environment to the gcc environment for example, use:

.. code::

    $ module load gcc

This will automatically unload the current compiler and system libraries
associated with it, load the new compiler environment and automatically load
associated system libraries as well.

Changing versions of the same compiler
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To use a specific compiler *version*, you must first ensure the compiler's
module is loaded, and *then* swap to the correct compiler version. For example,
the following will configure the environment to use the gcc compilers, then load
a non-default gcc compiler version:

.. code::

    $ module load gcc
    $ module swap gcc gcc/4.7.1

..

    **note: we recommend the following general guidelines for using the
    programming environment modules:**

    -  Do not purge all modules; rather, use the default module environment
       provided at the time of login, and modify it.
    -  Do not swap moab, torque, or mysql modules after loading a
       programming environment modulefile.

--------------

Compiler wrappers
-----------------

Commodity clusters at the olcf can be accessed via the following wrapper
programs:

-  ``mpicc`` to invoke the c compiler
-  ``mpicc``, ``mpicxx``, or ``mpic++`` to invoke the c++ compiler
-  ``mpif77`` or ``mpif90`` to invoke appropriate versions of the
   fortran compiler

These wrapper programs are cognizant of your currently loaded modules, and will
ensure that your code links against our openmpi installation.  more information
about using openmpi at our center can be found in our `software documentation
<https://www.olcf.ornl.gov/software_package/openmpi/>`__.

Compiling threaded codes
------------------------

When building threaded codes, compiler-specific flags must be included to ensure
a proper build.

Openmp
^^^^^^

For pgi, add "-mp" to the build line.

.. code::

    $ mpicc -mp test.c -o test.x
    $ export omp_num_threads=2

For gnu, add "-fopenmp" to the build line.

.. code::

    $ mpicc -fopenmp test.c -o test.x
    $ export omp_num_threads=2

For intel, add "-qopenmp" to the build line.

.. code::

    $ mpicc -qopenmp test.c -o test.x
    $ export omp_num_threads=2

For information on *running threaded codes*, please see the :ref:`andes-thread-layout`
subsection of the :ref:`andes-running-jobs` section in this user guide.

.. _andes-running-jobs:


