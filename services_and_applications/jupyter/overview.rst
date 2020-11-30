.. _jupyter_overview:

**************************
Overview
**************************


Jupyter at OLCF
---------------

Jupyter is a powerful tool enabling reproducible research and teaching. Use it to create notebooks that contain both computer code and rich text elements (paragraphs, equations, figures, widgets, links). This allows you to create human-readable documents containing executable data analytics components, results, and descriptions.

JupyterLab
^^^^^^^^^^

JupyterLab is a web-based interactive development environment for Jupyter. It provide a way to use notebooks, text editors, terminals, and custom components together. You can configure and arrange the user interface to support a wide range of workflows in data science, scientific computing, and machine learning. 

The OLCF JupyterHub implementation will spawn you into a single-user JupyterLab environment.


Jupyter Hub
^^^^^^^^^^^

JupyterHub is the best way to serve Jupyter Labs for multiple users within a project. It is a multi-user Hub that spawns, manages, and proxies multiple selectable instances of the single-user JupyterLab server.

JupyterHub within OLCF works by first authenticating each user using NCCS LDAP authentication. The Hub will offer each user a selection of Lab images to launch, which will then be spun up automatically. Upon successfull authentication, your UID/GID/Groups are queried and built into the deployment of your personal JupyterLab. In addition, you will have access to your standard OLCF storage space(s) on NFS and GPFS.

Access
------

OLCF JupyterHub link: `https://jupyter.olcf.ornl.gov/ <https://jupyter.olcf.ornl.gov/>`__

The above link will present you with the page below. Please login with your OLCF account and PASSCODE.

.. image:: /images/jupyter/login.png



After succesfull authentication you will be presented with a choice of JupyterLab images (see below for description of lab images):

.. image:: /images/jupyter/jupyterlab_images.png


CPU vs. GPU JupyterLab (Available Resources)
--------------------------------------------


Conda Environments
------------------