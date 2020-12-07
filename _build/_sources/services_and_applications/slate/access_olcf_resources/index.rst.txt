#####################################
Access OLCF Resources From Containers
#####################################


All containers run as the project-level automation user which has access to
all project files. The automation username is always the project ID and
appended with ``_auser``.

.. note::
  Most container images on registries like Docker Hub are built to run as root. This means 
  that some images will need to be modified by changing ownership of writable directories
  in the image.


.. toctree::
   :maxdepth: 2

   job_submit
   mount_fs
