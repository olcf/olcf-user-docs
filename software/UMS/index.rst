.. _UMS:

######################
User-Managed Software
######################

Introduction
------------

The User-Managed Software (UMS) program defines a set of polices by which users of OLCF
systems are granted the ability and responsibility to install, maintain, document, and support 
software packages intended for use by other general users on OLCF resources.

.. note::

  The UMS program is not currently available on all OLCF systems.

  Depending on the system, the directories used by UMS projects may differ, but the workflow remains the same.

To apply to the UMS program, fill out the application at: 
`https://my.olcf.ornl.gov/project-application-new <https://my.olcf.ornl.gov/project-application-new>`_.
Select "User Managed Software Program" from the drop down menu to begin. 

Currently Available User-Managed Software
-----------------------------------------

.. tab-set::

  .. tab-item:: Frontier

    **Currently Available User-Managed Software on Frontier**
    
    +------------+----------------+--------------------------------------------+--------------------------------------------------------------------------------+
    | Project    | Packages       | Point of Contact                           | Information                                                                    |
    +------------+----------------+--------------------------------------------+--------------------------------------------------------------------------------+
    | ums012     | AMD AFAR       | Felipe Jaramillo (cabarcas@udel.edu)       | AMD ROCM AFAR compiler based on AMD development                                |
    |            |                |                                            |                                                                                |
    |            | LLVM           | Sunita Chandrasekaran (schandra@udel.edu)  | LLVM Development builds                                                        |
    +------------+----------------+--------------------------------------------+--------------------------------------------------------------------------------+
    | ums014     | UPC++          | Paul H. Hargrove (phhargrove@lbl.gov)      | UPC++ library                                                                  |
    |            |                |                                            |                                                                                |
    |            |                |                                            | Issue Tracker:     https://upcxx.lbl.gov/issues                                |
    |            |                |                                            |                                                                                |
    |            |                |                                            | Support Forum:     https://groups.google.com/g/upcxx                           |
    +------------+----------------+--------------------------------------------+--------------------------------------------------------------------------------+
    | ums015     | Intel oneAPI   | Codeplay Software (sycl@codeplay.com)      | Intel oneAPI compiler and runtime libraries                                    |
    |            |                |                                            |                                                                                |
    |            |                |                                            | Website:           https://oneapi.io/ and https://developer.codeplay.com/      |
    |            |                |                                            |                                                                                |
    |            |                |                                            | Issue Tracker:     https://github.com/intel/llvm/issues                        |
    |            |                |                                            |                                                                                |
    |            |                |                                            | Support Forum:     https://support.codeplay.com/                               |
    +------------+----------------+--------------------------------------------+--------------------------------------------------------------------------------+
    | ums022     | VisIt          | Eric Brugger (brugger1@llnl.gov)           | VisIt Visualization and Analysis Tool                                          |
    +------------+----------------+--------------------------------------------+--------------------------------------------------------------------------------+
    | ums023     | HPCToolkit     | Wileam Phan (wil.phan@rice.edu)            | HPCToolkit Performance measurement and analysis tools                          |
    |            |                |                                            |                                                                                |
    |            |                | John Mellor-Crummey (johnmc@rice.edu)      | Website:           http://hpctoolkit.org/                                      |
    |            |                |                                            |                                                                                |
    |            |                |                                            | Issue Tracker:     https://gitlab.com/hpctoolkit/hpctoolkit/-/issues           |
    |            |                |                                            |                                                                                |
    |            |                |                                            | Mailing List:      hpctoolkit-forum@rice.edu                                   |
    +------------+----------------+--------------------------------------------+--------------------------------------------------------------------------------+
    | ums024     | Open MPI       | Thomas Naughton (naughtont@ornl.gov)       | Open MPI for Exascale -- MPI library                                           |
    |            |                |                                            |                                                                                |
    |            |                | Amir Shehata (shehataa@ornl.gov)           | Issue Tracker:     https://github.com/OMPI-X/platforms/issues                  |
    +------------+----------------+--------------------------------------------+--------------------------------------------------------------------------------+
    | ums025     | Clacc          | Joel E. Denny (dennyje@ornl.gov)           | Clacc: Clang/LLVM fork to support OpenACC in C/C++                             |
    |            |                |                                            |                                                                                |
    |            |                |                                            | General Info:      https://csmd.ornl.gov/project/clacc                         |
    |            |                |                                            |                                                                                |
    |            |                |                                            | Source:            https://github.com/llvm-doe-org/llvm-project/tree/clacc/main|
    +------------+----------------+--------------------------------------------+--------------------------------------------------------------------------------+

  .. tab-item:: Crusher

    **Currently Available User-Managed Software on Crusher**
    
    +------------+----------------+--------------------------------------------+--------------------------------------------------------------------------------+
    | Project    | Packages       | Point of Contact                           | Information                                                                    |
    +------------+----------------+--------------------------------------------+--------------------------------------------------------------------------------+
    | ums012     | SOLLVE         | Felipe Jaramillo (cabarcas@udel.edu)       | AMD ROCM AFAR compiler based on AMD development                                |
    |            |                |                                            |                                                                                |
    |            | LLVM           | Sunita Chandrasekaran (schandra@udel.edu)  | LLVM Development builds                                                        |
    +------------+----------------+--------------------------------------------+--------------------------------------------------------------------------------+
    | ums015     | DPC++ for HIP  | Gordon Brown (gordon@codeplay.com)         |                                                                                |
    +------------+----------------+--------------------------------------------+--------------------------------------------------------------------------------+
    | ums023     | HPCToolkit     | Wileam Phan (wil.phan@rice.edu)            | HPCToolkit Performance measurement and analysis tools                          |
    |            |                |                                            |                                                                                |
    |            |                | John Mellor-Crummey (johnmc@rice.edu)      | Website:           http://hpctoolkit.org/                                      |
    |            |                |                                            |                                                                                |
    |            |                |                                            | Issue Tracker:     https://gitlab.com/hpctoolkit/hpctoolkit/-/issues           |
    |            |                |                                            |                                                                                |
    |            |                |                                            | Mailing List:      hpctoolkit-forum@rice.edu                                   |
    +------------+----------------+--------------------------------------------+--------------------------------------------------------------------------------+
    | ompix      | Open MPI       | Thomas Naughton (naughtont@ornl.gov)       | Open MPI for Exascale -- MPI library                                           |
    |            |                |                                            |                                                                                |
    |            |                | Amir Shehata (shehataa@ornl.gov)           | Issue Tracker:     https://github.com/OMPI-X/platforms/issues                  |
    +------------+----------------+--------------------------------------------+--------------------------------------------------------------------------------+

  .. tab-item:: Summit

    **Currently Available User-Managed Software on Summit**
    
    +------------+----------------+--------------------------------------------+--------------------------------------------------------------------------------+
    | Project    | Packages       | Point of Contact                           | Information                                                                    |
    +------------+----------------+--------------------------------------------+--------------------------------------------------------------------------------+
    | gen007flux | Flux           | Stephen Herbein (herbein1@llnl.gov)        | https://github.com/flux-framework                                              |
    +------------+----------------+--------------------------------------------+--------------------------------------------------------------------------------+
    | stf010     | flang          | Fady Ghanim (ghanimfa@ornl.gov)            |                                                                                |
    +------------+----------------+--------------------------------------------+--------------------------------------------------------------------------------+
    | aph114     | openPMD-api    | Axel Huebl (axelhuebl@lbl.gov)             | https://github.com/openPMD/openPMD-api; Complex compiled python extension.     |
    |            | WarpX          |                                            | Might be best to treat as a discrete python environment similar to IBM-WML-CE. |
    |            | libEnsemble    |                                            |                                                                                |
    |            | Ascent/Conduit |                                            |                                                                                |
    |            | Adios2 dev     |                                            |                                                                                |
    +------------+----------------+--------------------------------------------+--------------------------------------------------------------------------------+
    | gen119     | NVIDIA RAPIDS  | Benjamin Hernandez (hernandezarb@ornl.gov) | https://developer.nvidia.com/rapids                                            |
    |            | BlazingSQL     |                                            | https://blazingsql.com/                                                        |
    +------------+----------------+--------------------------------------------+--------------------------------------------------------------------------------+
    | ums012     | SOLLVE         | Felipe Jaramillo (cabarcas@udel.edu)       |                                                                                |
    |            |                |                                            |                                                                                |
    |            | LLVM           | Sunita Chandrasekaran (schandra@udel.edu)  |                                                                                |
    +------------+----------------+--------------------------------------------+--------------------------------------------------------------------------------+
    | ums013     | Julia          | Valentin Churavy  (vchuravy@mit.edu)       | https://julialang.org                                                          |
    +------------+----------------+--------------------------------------------+--------------------------------------------------------------------------------+
    | ums014     | UPC++          | Paul H. Hargrove (phhargrove@lbl.gov)      | UPC++ library                                                                  |
    |            |                |                                            |                                                                                |
    |            |                |                                            | Issue Tracker:     https://upcxx.lbl.gov/issues                                |
    |            |                |                                            |                                                                                |
    |            |                |                                            | Support Forum:     https://groups.google.com/g/upcxx                           |
    +------------+----------------+--------------------------------------------+--------------------------------------------------------------------------------+
    | ums015     | DPC++ for HIP  | Gordon Brown (gordon@codeplay.com)         |                                                                                |
    +------------+----------------+--------------------------------------------+--------------------------------------------------------------------------------+

Usage
-----

To access and use the UMS available on a system, you must first load the base ums module to add
the individual projects to the module list. Once this is loaded, then each project has a module
to gain access to that project’s provided software. For example:

.. tab-set::

  .. tab-item:: Summit

    .. code::
    
      ## Find the base UMS module on Summit:
      > module avail ums
      ----------------- /sw/summit/modulefiles/Core  ------------------
        ums/default
    
      ## Load the UMS project access modules:
      > module load ums
    
      ## See the newly available UMS projects:
      > module avail ums
      ----------------- /sw/summit/ums/modulefiles/ -------------------
        ums-abc123/default
        ums001/default
    
      ----------------- /sw/summit/modulefiles/Core  ------------------
        ums/default (L)
    
      ## Gain access to a UMS project's provided modules:
      > module load ums-abc123
    
      ## See the provided UMS project's modules (truncated output):
      > module avail
      ...
      --------------- /sw/summit/modulefiles/ums/abc123/Core ---------------
        abc123/1.0
        abc123/1.1
    
      ----------------- /sw/summit/ums/modulefiles/ -------------------
        ums-abc123/default (L)
        ums001/default
    
      ----------------- /sw/summit/modulefiles/Core  ------------------
        ums/default (L)
      ...

  .. tab-item:: Crusher

    .. code::
    
      ## Find the base UMS module on Crusher:
      > module avail ums
      ----------------- /sw/crusher/modulefiles ------------------
        ums/default
    
      ## Load the UMS project access modules:
      > module load ums
    
      ## See the newly available UMS projects:
      > module avail ums
      ----------------- /sw/crusher/ums/modulefiles/ -------------------
        ums-abc123/default
        ums001/default
    
      ----------------- /sw/crusher/modulefiles ------------------
        ums/default (L)
    
      ## Gain access to a UMS project's provided modules:
      > module load ums-abc123
    
      ## See the provided UMS project's modules (truncated output):
      > module avail
      ...
      --------------- /sw/crusher/ums/ums-abc123/modules ---------------
        abc123/1.0
        abc123/1.1
    
      ----------------- /sw/crusher/ums/modulefiles/ -------------------
        ums-abc123/default (L)
        ums001/default
    
      ----------------- /sw/crusher/modulefiles ------------------
        ums/default (L)
      ...
  
If there are issues with a UMS provided product, you can find information in that package's gateway module using ``module show ums-``:

.. code::

  > module show ums-abc123
  -----------------------------------------------------------
    /sw/{{HOST}}/ums/modules/ums-abc123/default.lua:
      or
    /sw/{{HOST}}/ums/modulefiles/ums-abc123/default.lua:
  -----------------------------------------------------------

  help([[ABC software description (User Managed Software)

    The ABC123 UMS project provides this feature.

    THIS SOFTWARE IS NOT SUPPORTED BY THE OLCF.

    Please direct all support questions and concerns regarding this software
    installation to one of the following:

       - Point of Contact: <UMS Project PI>
         - Email:  <UMS POC email>
         - GitHub: <if applicable>

    Documentation:
      <URL to the project's documentation>
    ]])
    whatis("UMS - ABC Software")
    prepend_path("MODULEPATH","/sw/{{HOST}}/ums/modules/abc123")
      or
    prepend_path("MODULEPATH","/sw/{{HOST}}/modulefiles/ums/abc123/Core")

Policies
--------

The OLCF UMS Policy is located in the "Accounts and Projects" section of this documentation
`here </accounts/olcf_policy_guide.html#user-managed-software-policy>`_.

Writing UMS Modulefiles
-----------------------

A project directory and modulefiles will be created and made available.  The project directory will be the
workspace for your team to build and install the software you wish to provide to the other OLCF users.
The created modulefile will add your project's provided modules to the modulepath. Note that by default,
the project modulefile will add a default path, ``/sw/{{HOST}}/ums/{{PROJECT}}/modules`` or
``/sw/{{HOST}}/modulefiles/ums/{{PROJECT}}/Core``, to the MODULEPATH. If you wish to locate your project's modules
in another directory, you will need to modify the provided modulefile.

The following will be created and put under the ownership of your UMS project and your project's PI:

.. code::

  /sw/{{HOST}}/ums/modules/{{PROJECT}}/default.lua    ## default project gateway module
  /sw/{{HOST}}/ums/{{PROJECT}}                        ## root prefix for installing builds
  /sw/{{HOST}}/ums/{{PROJECT}}/modules                ## root prefix for installing modulefiles

  ## or

  /sw/{{HOST}}/ums/modulefiles/{{PROJECT}}/default.lua    ## default project gateway module
  /sw/{{HOST}}/ums/{{PROJECT}}                            ## root prefix for installing builds
  /sw/{{HOST}}/modulefiles/ums/{{PROJECT}}/Core           ## root prefix for installing modulefiles

The builds in ``/sw/{{HOST}}/ums/{{PROJECT}}`` can be organized as you see fit, but we ask that you try to 
document the layout and build procedures. For example, under the prefix directory, use one or more of the 
following to improve transparency of the build process:

- keep an up-to-date README or changelog
- keep configure and build logs in your project's area
- use spack or non-interactive build scripts kept in the prefix to deploy all packages
- track changes to configurations or build-scripts in git

so that other people such as new developers and maintainers on your project as well as OLCF staff will have 
a clear understanding of how the builds have been configured and what their dependencies are should 
they need to take over maintaining the builds.

The structure of the modulefile tree is somewhat flexible. These directories will not be in the default 
``$MODULEPATH``. For general users to access them, they will first need to opt-in to using UMS software by loading 
the ``ums/default`` module, then the module for your UMS software project ``ums-{{PROJECT}}`` and finally one or 
more modulefiles that you have written for your software:

.. code::

  module load ums
  module load ums-{{PROJECT}}
  module avail

  # To see modules your project provides:
  ls $(module --redirect show ums-{{PROJECT}} | egrep "MODULEPATH.*$" | grep -o "/sw/[^\'\"]*")

The project gateway module ``ums-{{PROJECT}}`` will add either ``/sw/{{HOST}}/ums/{{PROJECT}}/modules`` or
``/sw/{{HOST}}/modulefiles/ums/{{PROJECT}}/Core`` to the ``$MODULEPATH``. Any modulefiles you install
under this directory will be available to users when they have loaded the gateway module. Modulefiles should
be organized according to the following structure:

.. code::

  /sw/{{HOST}}/ums/{{PROJECT}}/modules/<package1_name>/<package1_version1>.lua
  /sw/{{HOST}}/ums/{{PROJECT}}/modules/<package1_name>/<package1_version2>.lua
  /sw/{{HOST}}/ums/{{PROJECT}}/modules/<package2_name>/<package2_version1>.lua

  or

  /sw/{{HOST}}/modulefiles/ums/{{PROJECT}}/Core/<package1_name>/<package1_version1>.lua
  /sw/{{HOST}}/modulefiles/ums/{{PROJECT}}/Core/<package1_name>/<package1_version2>.lua
  /sw/{{HOST}}/modulefiles/ums/{{PROJECT}}/Core/<package2_name>/<package2_version1>.lua

You may have as many modulefiles as you see fit, both in terms of ``<package_nameX>`` and ``<package_versionX>``. 

.. warning::

  It is imperative that ``/sw/{{HOST}}/ums/{{PROJECT}}/modules`` and ``/sw/{{HOST}}/modulefiles/ums/{{PROJECT}}/Core``
  only have one level of subdirectories (``<packageN_name>``). Having further subdirectories will alter the
  way LMOD searches for modulefiles globally and generally make LMOD's behavior indeterminate. It is also 
  recommended that you be careful with symlinks in the modulefile prefix.

  In particular, symlinks under ``/sw/{{HOST}}/ums/{{PROJECT}}/modules`` or ``/sw/{{HOST}}/modulefiles/ums/{{PROJECT}}/Core``
  that refer back to themselves will cause LMOD to enter a recursive loop and be unable to display or load your modules correctly.

.. 
  If you want to expand the pilot to other machines, let us know and we can create corresponding directories 
  under ``/sw/{andes,crusher,summit,...}``. UA organizes software per-hostname rather than per-architecture 
  and we discourage sharing builds between different machines.
  Even though the architecture may be the same for multiple hosts, these hosts generally go through 
  upgrades and changes to key dependency libraries at different times; or they may have different resource 
  managers; or applications may require different static configuration files between hosts. It saves us the 
  trouble of having to deal with incompatibilities in shared software when the environment between two 
  machines diverges.

For further assistance please contact the OLCF at help@olcf.ornl.gov.
