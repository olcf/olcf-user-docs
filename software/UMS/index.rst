.. _UMS:

######################
User-Managed Software
######################

User-managed software is built, maintained, and supported by facility users rather than as official
offerings of the facility, but exposed to all users through the common tool of the module system.

Available Software
------------------

  Partial list.

.. toctree::
   :maxdepth: 2

   Flux
   Adios2

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
    ums-adios2/default
    ums-aph114/default
    ums-gen007flux/default
    ums-gen119/default
    ums-stf010/default

If there are issues with a UMS provided product, you can find information in the module via:

.. code::

  > module show ums-adios2
  -----------------------------------------------------------
    /sw/summit/modulefiles/ums/Core/ums-adios2/default.lua:
  -----------------------------------------------------------

  help([[Adios Developers Project (User Managed Software)

  THIS SOFTWARE IS NOT OFFICIALLY SUPPORTED BY THE OLCF.

  Please direct all support questions and concerns regarding this software
  installation to:

    William Godoy (godoywf@ornl.gov)

  ]])
  whatis("UMS - Adios Developers Project Software")
  prepend_path("MODULEPATH","/sw/summit/modulefiles/ums/adios2/Core")

Policies
--------

OLCF UMS Policy Guide is located in the Accounts and Projects section of this documentation
`here </accounts/olcf_policy_guide.html#user-managed-software-policy>`_.
