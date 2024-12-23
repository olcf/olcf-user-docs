########################################
Scalable Protected Infrastructure (SPI)
########################################

What is SPI
=============

The OLCF's **Scalable Protected Infrastructure (SPI)** provides resources and protocols that enable researchers to process protected data at scale.  The SPI is built around a framework of security protocols that allows researchers to process large datasets containing private information.  Using this framework researchers can use the center's large HPC resources to compute data containing protected health information (PHI), personally identifiable information (PII), data protected under International Traffic in Arms Regulations, and other types of data that require privacy.  

The SPI utilizes a mixture of existing resources combined with specialized resources targeted at SPI workloads.  Because of this, many processes used within the SPI are very similar to those used for standard non-SPI.  This page lists the differences you may see when using OLCF resources to execute SPI workflows.  The page will also point to sections within the site where more information on standard non-SPI use can be found.

What is Citadel
----------------

The National Center for Computational Science (NCCS) and the Oak Ridge Leadership Computing Facility (OLCF) have implemented the CITADEL security framework as **part of their Scalable Protected Infrastructure (SPI)**. This infrastructure provides resources and protocols that enable researchers to process protected data at scale. With the CITADEL framework, **researchers can use the OLCF’s large HPC resources to compute** data containing protected health information (PHI), personally identifiable information (PII), data protected under International Traffic in Arms Regulations, and other types of data that require privacy.

.. note::
  With the CITADEL framework, researchers can use the OLCF’s large HPC resources including Frontier to compute data containing protected health information (PHI), personally identifiable information (PII), data protected under International Traffic in Arms Regulations, and other types of data that require privacy.

The NCCS CITADEL security framework was originally conceived to facilitate the large-scale analysis of protected health information (PHI) data from the US Department of Veterans Affairs' (VA) Million Veteran Program. The NCCS SPI team, with assistance from ORNL Risk Management and ORNL’s Information Technology Services Division (ITSD), refined the initial prototype and expanded CITADEL's capabilities to accommodate a diverse array of programs, projects, and sponsors.

Although the facility already adheres to the National Institute of Standards and Technology’s security and privacy controls for moderate Official Use Only data, CITADEL was crafted to enforce security measures for handling vast datasets that encompass types of data necessitating heightened privacy safeguards on systems overseen by the Oak Ridge Leadership Computing Facility (OLCF). Extra precautions have been taken to manage private data such that it cannot be accessed by other researchers or used by other projects. For example, HIPAA-protected data for a project sponsored by the VA will be kept absolutely separate from HIPAA-protected data for a projected sponsored by the Centers for Medicare and Medicaid Services (CMS).

CITADEL, having undergone comprehensive technical-, legal-, and policy-oriented reviews and received third-party accreditation, has presented new possibilities for research projects that previously could not access utilize OLCF systems due to the nature of their data.  



New User QuickStart
====================

If you are new to the OLCF or the OLCF's SPI, this page can help get you started.  Below are some of the high-level steps needed to begin use of the OLCF's SPI:

#.  :ref:`Request an allocation (project)<spi-allocations-projects>`.  All access and resource use occurs within an approved allocation.
#.  :ref:`Request a user account<spi-user-accounts>`.  Once an allocation (project) has been approved, each member of the project must request an account to use the project's allocated resources.
#.  :ref:`Whitelist your IPs<spi-whitelisting-ip>`.  Access to the SPI resources is limited to IPs that have been whitelisted by the OLCF.  The only exception is for projects using KDI resources.  If your project also uses KDI resources, you will use the KDI access procedures and do not need to provide your IP to the OLCF.
#.  :ref:`Transfer needed data<spi-data-transfer>` to the SPI filesystems.  The SPI resources mount filesystems unique to the SPI.  Needed data, code, and libraries must be transferred into the SPI using the SPI's Data Transfer Nodes.
#.  :ref:`Build and run on Citadel<spi-compute-citadel>`.  Citadel is front end for the OLCF's HPC resources.  Its resources and programming environment mirror Frontier.  You can ssh into Frontier's Citadel login nodes to build for and execute jobs on the system's compute resources.


Notable Differences 
--------------------

If you have a standard non-SPI account(s) on other OLCF resources, the differences between SPI and non-SPI can be found on this page.  Below are some of the notable differences:

-  :ref:`UserIDs are unique to each SPI project<spi-user-accounts>`.  Unlike non-SPI accounts, SPI accounts can not span multiple projects. SPI userIDs use the format: ``<userid>_<proj>_mde`` 
-  :ref:`Direct access to SPI resources requires your IP to be whitelisted<spi-whitelisting-ip>` by the OLCF.  Before accessing SPI resources, you must contact help@olcf.ornl.gov and provide you system's IP.  If your project also uses KDI resources, you will use the KDI procedure and do not need to provide your IP to the OLCF.
-  :ref:`SPI resources mount SPI filesystems<spi-file-systems>`.  The SPI resources do not mount the non-SPI's scratch filesystems, home areas, or mass storage.  
-  :ref:`SPI compute resources cannot access external resources<spi-data-transfer>`.  Needed data must be transferred to the SPI resources through the SPI's DTN.
-  :ref:`The Citadel login nodes<spi-compute-citadel>` and batch queues must be used to access Frontier for SPI workflows.


Allocations and User Accounts
==============================

.. _spi-allocations-projects:

Allocations (Projects)
-----------------------

Similar to standard OLCF workflows, to run SPI workflows on OLCF resources, you will first need an approved project.  The project will be awarded an allocation(s) that will allow resource access and use.  The first step to requesting an allocation is to complete the project request form.  The form will initiate the process that includes peer review, export control review, agreements, and others.  Once submitted, members of the OLCF accounts team will help walk you through the process.


Requesting a New Allocation (Project)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Please see the `OLCF Accounts and Projects <https://docs.olcf.ornl.gov/accounts/index.html#accounts-and-projects>`_ section of this site to request a new project. 

.. note:: SPI project IDs may look similar to those used in the non-SPI moderate enclave but will always append ``_mde`` to the name. For example: ``abc123_mde``. 

.. note:: Projects cannot overlap non-SPI and SPI enclaves. SPI projects will only exist on SPI resources.


**More information** on the OLCF account process can be found in the `OLCF Accounts and Projects <https://docs.olcf.ornl.gov/accounts/index.html#accounts-and-projects>`_ section of this site.


.. _spi-user-accounts:

User Accounts 
--------------

Once a project has been approved and created, the next step will be to request user accounts.  A user account will allow an individual to access the project's allocated resources.    This process to request an account is very similar to the process used for non-SPI projects.  One notable difference between SPI and non-SPI accounts: SPI usernames are unique to a project.  SPI usernames use the format: ``<userid>_<proj>_mde``.  If you have access to three SPI projects, you will have three userIDs with three separate home areas.

Requesting a New User Account
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Please see the :ref:`OLCF Applying for a User Account<applying-for-a-user-account>` section of this site to request a new account and join an existing project.  Once submitted, the OLCF Accounts team will help walk you through the process.


.. note::
    In order to help ensure data separation, each SPI user is given a unique userID for each project. SPI userIDs use the format: ``<userid>_<proj>_mde`` . For example: ``userx_abc123_mde``. SPI usernames will not overlap with usernames used in the non-SPI enclaves. Unlike non-SPI usernames, SPI usernames only exist in a single project. Users on multiple SPI projects will have a unique username for each SPI project.

**More information** on the account process and a link to the request form can be found in the :ref:`OLCF Applying for a User Account<applying-for-a-user-account>` section. 

Available Resources
====================

The OLCF SPI provides compute, filesystem, and data transfer resources.

:ref:`Compute<spi-compute-citadel>`
-------------------------------------
**Frontier** is available for SPI workloads.  The :ref:`Citadel<spi-compute-citadel>` framework provides the ability to use the OLCF's existing HPC resources for SPI frameworks.  

Please see the :ref:`Citadel<spi-compute-citadel>` section for more details on connecting and using Frontier for your SPI workloads.


:ref:`File Systems<spi-file-systems>`
-------------------------------------
To safely separate SPI and non-SPI workflows, the SPI resources only mount a GPFS resource named :ref:`Arx<spi-file-systems>`.  The Arx filesystem provides both the home and scratch filesystems for Citadel resources.

Please see the :ref:`Arx<spi-file-systems>` section for more details.

:ref:`Data Transfer<spi-data-transfer>`
---------------------------------------
The SPI provides separate :ref:`Data Transfer Nodes<spi-data-transfer>` configured specifically for SPI workflows.  The nodes are not directly accessible for login but are accessible through the Globus tool.  The SPI DTNs mount the same Arx filesystem available on the SPI compute resources.  Globus is the preferred method to transfer data into and out of the SPI resources.

Please see the :ref:`Data Transfer Nodes<spi-data-transfer>` section for more details. 

IP Whitelisting
================

Access to the SPI resources is allowed to approved IP addresses only. 

.. warning:: Direct access to SPI resources require the connecting IP address to be whitelisted.  The OLCF must know your IP before you can directly connect to SPI resources.

.. note:: Project using ORNL's KDI must following KDI access procedures and cannot access SPI resources directly.  If your project uses both KDI and SPI, you do not need to provide an IP.


.. _spi-whitelisting-ip:

Whitelisting an IP or range
----------------------------
To add an IP or range of IPs to your project’s whitelist, please contact help@olcf.ornl.gov


Finding your IP
----------------

An easy way to locate your IP or range of IP addresses is to contact your local network administration team.  Your network administrator will be able to provide your individual IP or the ranges of IP addresses that you will use on the network.

Another way to find your IP is to use tools such as ‘whats my ip’. But please note, the tools may only return your internal IP. The IP you provide for the whitelist must be your external IP. The following are internal rages that cannot be used to whitelist your IP:

-  10.0. 0.0 - 10.255. 255.255 (10.0. 0.0/8 prefix)
-  172.16. 0.0 - 172.31. 255.255 (172.16. 0.0/12 prefix)
-  192.168. 0.0 - 192.168. 255.255 (192.168. 0.0/16 prefix)

The tool may also return you current IP which may change if not static. For these reasons, reaching out to your IT department may be the best option. Your IT department can provide a range of externally facing IP addresses that can be whitelisted.


.. _spi-compute-citadel:

Citadel
========

The **Citadel** framework allows use of the OLCF's existing HPC resource **Frontier** for SPI workflows.  Citadel adds measures to ensure separation of SPI and non-SPI workflows and data. This section provides differences when using OLCF resources for SPI and non-SPI workflows.  Because the Citadel framework just adds another security layer to existing HPC resources, many system use methods are the same between SPI and non-SPI workflows.  For example, compiling, batch scheduling, and job layout are the same between the two security enclaves.  Because of this, the existing resource user guides still cover the majority of system use methods.  

.. note:: This section covers differences between SPI and non-SPI workflows, but the existing resource user guides cover the majority of system use methods.  Please use the :ref:`Frontier User Guide<frontier-user-guide>` for resource use details.


.. _citadel-login-nodes:

Login Nodes
------------
To help separate data and processes, the Citadel framework provides separate login nodes to reach Frontier's compute resources: 

+----------------+-------------+------------------------------------+-------------------------------------------------------------------------------------+
| Resource       | Access Type |  Citadel Login Node Address        |  Example                                                                            |
+================+=============+====================================+=====================================================================================+
| Frontier       | SPI         |  frontierspi.olcf.ornl.gov         |   ``ssh username_projID_mde@frontierspi.olcf.ornl.gov``                             |
|                +-------------+------------------------------------+-------------------------------------------------------------------------------------+
|                | KDI         |  spilogin1.frontier.olcf.ornl.gov  |   ``ssh username_projID_mde@spilogin1.frontier.olcf.ornl.gov``                      |
+----------------+-------------+------------------------------------+-------------------------------------------------------------------------------------+

.. note:: The Citadel login nodes must be used to submit SPI jobs to Frontier's compute resources and access the SPI specific filesystem.

The login nodes listed above mirrors the Frontier login nodes in hardware and software.  The login node also provides access to the same compute resources as are accessible from Frontier's non-SPI workflows.  

The Citadel login nodes cannot access the external network and are only accessible from whitelisted IP addresses. KDI users will need to login to the Frontier SPI login nodes directly from KDI instead of going through the frontierspi load balancer. See the table above for the correct address for your use-case. 


Connecting 
-----------

Similar to the non-SPI resources, SPI resources require two-factor authentication.  If you are new to the center, you will receive a SecurID fob during the account approval/creation process.  If you are an existing user of non-SPI resources, you can use the same SecurID fob and PIN used on your non-SPI account.  

Also similar to non-SPI resources, you will connect directly to the SPI resources through ssh.  

ORNL's KDI users are an exception and cannot, by policy, log directly into SPI resources.  KDI users, please follow the KDI documented procedures:

#.  Login to https://kdivdi.ornl.gov with your KDI issued credentials
#.  Launch the Putty Application
#.  Enter the host address from the table above and click Open. 
#.  You will then be in an ssh terminal to authenticate with your OLCF credentials as detailed above. 

.. note::  Projects using ORNL's KDI must following KDI access procedures and cannot access SPI resources directly.  If your project uses both KDI and SPI, you will not access the SPI resources directly.

In order to help ensure data separation, each SPI user is given a unique userid for each project. SPI user names use the format: ``<userid>_<proj>_mde`` . For example: ``usera_prj123_mde``. 

.. warning:: SPI usernames will not overlap with usernames used in the non-SPI enclaves. Unlike non-SPI usernames, SPI usernames only exist in a single project. Users on multiple SPI projects will have a unique username for each SPI project.  You must specify your unique SPI username matching the target project when connecting.

For users with accounts on non-SPI resources, you will use the same SecurID fob and PIN, but you must specify your unique SPI userID when you connect.  The ID will be used to place you in the proper UNIX groups allowing access to the project specific data, directories, and allocation.





Building Software
------------------

The user environment on the Frontier :ref:`Citadel login nodes<citadel-login-nodes>` login nodes mirror the non-SPI Frontier login nodes.  Because of this, codes built for/on the non-SPI Frontier will also run on the resource within the Citadel framework.  Similarly, third party software, compilers, and libraries provided on the non-SPI Frontier will also be available from the resource within the Citadel framework. The :ref:`Frontier User Guide<frontier-user-guide>` can be used when building workflows for the non-SPI as well as the Citadel framework.  


External Repositories
^^^^^^^^^^^^^^^^^^^^^^
The Citadel framework prevents login and compute resources from accessing the internet.  Because of this, :ref:`Citadel login nodes<citadel-login-nodes>` cannot reach repositories external to the system.  If your build workflow attempts to access external repositories, you may need to alter your build workflows to use data stored locally.  For cases where you are unable to modify your workflow to use only local data, please reach out to help@olcf.ornl.gov.  We may be able to help by providing a partner project on Frontier.  The partner project would provide login access to the non-SPI Frontier login nodes and a build location that is writable from the non-SPI Frontier and read-only from within the Citadel framework.  For example the partner project would provide the ability to build on Frontier in ``/sw/frontier/mde/abc123_mde`` where ``abc123_mde`` is replaced by your Citadel project. This location is writable from Frontier but only readable from within the Citadel framework.

.. warning:: Login and compute resources in the Citadel framework can not access the internet.  This may impact workflows that attempt to access external repositories.


More information on building codes for Citadel including programming environments, compilers, and available software can be found on :ref:`Frontier User Guide<frontier-user-guide>`. 


Running Batch Jobs
-------------------

The Citadel framework allows use of the Frontier compute resources but adds additional layers of security to ensure data protection.  To ensure proper configuration and protection access to the compute resources, the following batch queue(s) must be used from the :ref:`Citadel login nodes<citadel-login-nodes>`:

-  batch-spi

The batch queues mirror the purpose of the similarly named Frontier queues. Details on each queue can be found in the :ref:`Frontier User Guide<frontier-user-guide>`. The SPI queues must be used to launch batch jobs from the :ref:`Citadel login nodes<citadel-login-nodes>` and can not be used directly from the non-SPI Frontier login nodes.

.. note:: To access Frontier's compute resources for SPI workflows, you must first log into a :ref:`Citadel login node<citadel-login-nodes>` and then submit a batch job to one of the SPI specific batch queues.

Use of the SPI queue will trigger configuration changes to the compute nodes to allow enhanced data protection. Compute nodes will be booted before and after each SPI batch job. Compute nodes will be booted into an image that mounts only the Arx filesystem. The image will also restrict connections. **Please note:** the reboot process may cause a slight delay in job startup.

More details on batch job submission through LSF and launching a parallel job through jsrun can be found on :ref:`Frontier User Guide<frontier-user-guide>`.

.. _spi-file-systems:

File Systems
=============

The SPI resources use filesystems visible only from SPI resources. The SPI resources do not mount filesystems mounted on non-SPI resources. The GPFS filesystem named Arx provides home, scratch, and shared project areas for SPI resources.

Available filesystems:

+----------------+---------------------------------------+-------------------------------------------------------------------------------------+
| Name           |  Location                             |  Purpose                                                                            |
+================+=======================================+=====================================================================================+
| Home           | ``/gpfs/arx/<proj>/home/<userid>``    |  Your login/home directory.  Used to store small scripts and source.                |
+----------------+---------------------------------------+-------------------------------------------------------------------------------------+
| Project Shared | ``/gpfs/arx/<proj>/proj-shared``      |  Location to share data with others in your project.                                |
+----------------+---------------------------------------+-------------------------------------------------------------------------------------+
| Scratch        | ``/gpfs/arx/<proj>/scratch/<userid>`` | Location to store compute job I/O.                                                  |
+----------------+---------------------------------------+-------------------------------------------------------------------------------------+

.. note:: SPI resources do not mount filesystems accessible from non-SPI resources.  SPI resources only mount the GPFS Arx filesytem.  


.. _spi-data-transfer:

Data Transfer
==============

Globus is the best option to transfer data into and out of the SPI resources.  

.. note:: The SPI Data Transfer Nodes are not directly accessible, but can be used through Globus to transfer data.

A simple example using the CLI:

::

    myproxy-logon -T -b -l usera_prj123_mde
    globus-url-copy -cred /gpfs/arx/prj123_mde/home/usera_prj123_mde/dataA -dcpriv -list 
