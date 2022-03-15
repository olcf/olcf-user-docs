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

  The UMS program is currently supported on Summit, Andes, and Spock.

To apply to the UMS program, fill out the application at: 
`https://my.olcf.ornl.gov/project-application-new <https://my.olcf.ornl.gov/project-application-new>`_.
Select "User Managed Software Program" from the drop down menu to begin. 

Currently Available User-Managed Software
-----------------------------------------

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

Usage
-----

To access and use the UMS available on a system:

.. code::

  > module avail ums
  --------------- /sw/summit/modulefiles/core ---------------
    ums/default

  > module load ums
  > module avail ums
  --------------- /sw/summit/modulefiles/core ---------------
    ums/default (L)

  ------------- /sw/summit/modulefiles/ums/core -------------
    ums-abc123/default
    ums-xyz987/default

If there are issues with a UMS provided product, you can find information in the module via:

.. code::

  > module show ums-abc123
  -----------------------------------------------------------
    /sw/summit/modulefiles/ums/Core/ums-abc123/default.lua:
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
    prepend_path("MODULEPATH","/sw/summit/modulefiles/ums/abc123/Core")

Policies
--------

The OLCF UMS Policy is located in the "Accounts and Projects" section of this documentation
`here </accounts/olcf_policy_guide.html#user-managed-software-policy>`_.

Writing UMS Modulefiles
-----------------------

The following directories will be created and made available for you to install software and modulefiles:

.. code::

  /sw/{{HOST}}/ums/{{PROJECT}}                     ## root prefix for installing builds
  /sw/{{HOST}}/modulefiles/ums/{{PROJECT}}/Core    ## root prefix for installing modulefiles

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

The gateway module ``ums-{{PROJECT}}`` will add ``/sw/{{HOST}}/modulefiles/ums/{{PROJECT}}/Core`` to the
``$MODULEPATH``. Any modulefiles you install under this directory will be available to users when they have 
loaded the gateway module. Modulefiles must be organized according to the following structure:

.. code::

  /sw/{{HOST}}/modulefiles/ums/{{PROJECT}}/Core/<package1_name>/<package1_version1>.lua
  /sw/{{HOST}}/modulefiles/ums/{{PROJECT}}/Core/<package1_name>/<package1_version2>.lua
  /sw/{{HOST}}/modulefiles/ums/{{PROJECT}}/Core/<package2_name>/<package2_version1>.lua

You may have as many modulefiles as you see fit, both in terms of ``<package_name>`` and ``<package_version>``. 
However, it is imperative that ``/sw/{{HOST}}/modulefiles/ums/{{PROJECT}}/Core`` only have one level of 
subdirectories (``<packageN_name>``). Having subdirectories will alter the way LMOD searches for modulefiles 
globally and generally make LMOD's behavior indeterminate. It is also recommended that you be careful with 
symlinks in the modulefile prefix. In particular, symlinks under ``/sw/{{HOST}}/modulefiles/ums/{{PROJECT}}/Core`` 
that refer back to ``/sw/{{HOST}}/modulefiles/ums/{{PROJECT}}/Core`` will cause LMOD to enter a recursive 
loop and be unable to display or load your modules correctly.

.. 
  If you want to expand the pilot to other machines, let us know and we can create corresponding directories 
  under ``/sw/{andes,...}``. UA organizes software per-hostname rather than per-architecture 
  and we discourage sharing builds between different machines.
  Even though the architecture may be the same for multiple hosts, these hosts generally go through 
  upgrades and changes to key dependency libraries at different times; or they may have different resource 
  managers; or applications may require different static configuration files between hosts. It saves us the 
  trouble of having to deal with incompatibilities in shared software when the environment between two 
  machines diverges.

For further assistance please contact the OLCF at help@olcf.ornl.gov.
