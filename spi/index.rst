########################################
Scalable Protected Infrastructure (SPI)
########################################

What is SPI
=============

The OLCF's **Scalable Protected Infrastructure (SPI)** provides resources and protocols that enable researchers to process protected data at scale.  The SPI is built around a framework of security protocols that allows researchers to process large datasets containing private information.  Using this framework researchers can use the center's large HPC resources to compute data containing protected health information (PHI), personally identifiable information (PII), data protected under International Traffic in Arms Regulations, and other types of data that require privacy.  

The SPI utilizes a mixture of existing resources combined with specialized resources targeted at SPI workloads.  Because of this, many processes used within the SPI are very similar to those used for standard non-SPI.  This page lists the differences you may see when using OLCF resources to execute SPI workflows.  The page will also point to sections within the site where more information on standard non-SPI use can be found.

New User QuickStart
--------------------

If you are new to the OLCF or the OLCF's SPI, this page can help get you started.  Below are some of the high-level steps needed to begin use of the OLCF's SPI:

#.  :ref:`Request an allocation (project)<spi-allocations-projects>`.  All access and resource use occurs within an approved allocation.
#.  :ref:`Request a user account<spi-user-accounts>`.  Once an allocation (project) has been approved, each member of the project must request an account to use the project's allocated resources.
#.  :ref:`Whitelist your IPs<spi-whitelisting-ip>`.  Access to the SPI resources is limited to IPs that have been whitelisted by the OLCF.  The only exception is for projects using KDI resources.  If your project also uses KDI resources, you will use the KDI access procedures and do not need to provide your IP to the OLCF.
#.  :ref:`Transfer needed data<spi-data-transfer>` to the SPI filesystems.  The SPI resources mount filesystems unique to the SPI.  Needed data, code, and libraries must be transferred into the SPI using the SPI's Data Transfer Nodes.
#.  :ref:`Build and run on Citadel<spi-compute-citadel>`.  Citadel is front end for the OLCF's Summit resource.  Its resources and programming environment mirror Summit.  You can ssh into Citadel to build for and execute jobs on Summit's compute resources.


Notable Differences 
--------------------

If you have a standard non-SPI account(s) on other OLCF resources, the differences between SPI and non-SPI can be found on this page.  Below are some of the notable differences:

-  :ref:`UserIDs are unique to each SPI project<spi-user-accounts>`.  Unlike non-SPI accounts, SPI accounts can not span multiple projects. SPI userIDs use the format: ``<userid>_<proj>_mde`` 
-  :ref:`Direct access to SPI resources requires your IP to be whitelisted<spi-whitelisting-ip>` by the OLCF.  Before accessing SPI resources, you must contact help@olcf.ornl.gov and provide you system's IP.  If your project also uses KDI resources, you will use the KDI procedure and do not need to provide your IP to the OLCF.
-  :ref:`SPI resources mount SPI filesystems<spi-file-systems>`.  The SPI resources do not mount the non-SPI's scratch filesystems, home areas, or mass storage.  
-  :ref:`SPI compute resources cannot access external resources<spi-data-transfer>`.  Needed data must be transferred to the SPI resources through the SPI's DTN.
-  :ref:`The Citadel login nodes<spi-compute-citadel>` and batch queues must be used to access Summit for SPI workflows.


Allocations and User Accounts
==============================

.. _spi-allocations-projects:

Allocations (Projects)
-----------------------

Similar to standard OLCF workflows, to run SPI workflows on OLCF resources, you will first need an approved project.  The project will be given an allocation(s) that will allow resource access and use.  The first step to requesting an allocation is to complete the project request form.  The form will initiate the process that includes peer review, export control review, agreements, and others.  Once submitted, members of the OLCF accounts team will help walk you through the process.


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
The SPI provides access to the OLCF's Summit resource for compute.  To safely separate SPI and non-SPI workflows, SPI workflows must use a separate login node named :ref:`Citadel<spi-compute-citadel>`.  Citadel provides a login node specifically for SPI workflows.  

The login node used by Citadel mirrors the Summit login nodes in hardare and software.  The login node also provides access to the same compute resources as are accessible from Summit.  

Similar to Summit, accessing the compute nodes is accomplished through the batch system.  Separate batch queues must be used to access the compute resources and ensure the compute resourcs are configured for SPI workflows.

:ref:`File Systems<spi-file-systems>`
-------------------------------------
To safely separate SPI and non-SPI workflows, the SPI resources only mount a GPFS resource named :ref:`Arx<spi-file-systems>`.  The Arx filesystem provides both the home and scratch filesystems for SPI resources.

:ref:`Data Transfer<spi-data-transfer>`
---------------------------------------
The SPI provides separate :ref:`Data Transfer Nodes<spi-data-transfer>` configured specifically for SPI workflows.  The nodes are not directly accessible for login but are accessible through the Globus tool.  The SPI DTNs mount the same Arx filesystem available on the SPI compute resources.  Globus is the prefered method to transfer data into and out of the SPI resources.


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

The SPI resource, **Citadel**, utilizes Summit's compute resources but adds measures to ensure separation of SPI and non-SPI workflows and data. The :ref:`Summit User Guide<summit-documentation-resources>` provides documentation on system details and use.  Because Citadel is largely a front end for Summit, you can use the Summit documentation when using Citadel.  This section describes some of the notable differences in using Summit directly and through the SPI's Citadel.  It should be used in combination with the :ref:`Summit User Guide<summit-user-guide>` .


Connecting 
----------

Similar to the non-SPI resources, SPI resources reqiure two-factor authentication.  If you are new to the center, you will receive a SecurID fob during the account approval/creation process.  If you are an existing user of non-SPI resources, you can use the same SecurID fob and PIN used on your non-SPI account.  

Also similar to non-SPI resources, you will connect directly to the SPI resources through ssh.  

ORNL's KDI users are an exception and can not by policy log directly into SPI resources.  KDI users, please follow the KDI documented procedures:

#.  Login to https://kdivdi.ornl.gov with your KDI issued credentials
#.  Launch the Putty Application
#.  Enter the hostname "citadel.ccs.ornl.gov" and click Open
#.  You will then be in an ssh terminal to authenticate with your OLCF credentials as detailed above. 

.. note::  Projects using ORNL's KDI must following KDI access procedures and cannot access SPI resources directly.  If your project uses both KDI and SPI, you will not access the SPI resources directly.

In order to help ensure data separation, each SPI user is given a unique userid for each project. SPI user names use the format: ``<userid>_<proj>_mde`` . For example: ``usera_prj123_mde``. 

.. warning:: SPI usernames will not overlap with usernames used in the non-SPI enclaves. Unlike non-SPI usernames, SPI usernames only exist in a single project. Users on multiple SPI projects will have a unique username for each SPI project.  You must specify your unique SPI username matching the target project when connecting.

For users with accounts on non-SPI resources, you will use the same SecurID fob and PIN, but you must specify your unique SPI userID when you connect.  The ID will be used to place you in the proper UNIX groups allowing access to the project specific data, directories, and allocation.


Login Nodes
------------
To help separate data and processes, SPI use separate login nodes, ``citadel.ccs.ornl.gov``, to reach Summit’s compute resources. 

.. note:: The Citadel login node must be used to submit SPI jobs to Summit’s compute resources and access the SPI specific filesystem.

The login node used by Citadel mirrors the Summit login nodes in hardware and software.  The login node also provides access to the same compute resources as are accessible from Summit.  

The Citadel login nodes cannot access the external network and are only accessible from whitelisted IP addresses.


Building Software
------------------

The user environment on the Citadel login nodes mirrors the Summit login nodes.  Code build for/on Summit, should also run on Citadel. Third party software, compilers, and libraries provided on Summit will also be available from Citadel. The :ref:`Summit User Guide<summit-user-guide>` can be used when building workflows for Citadel.  

.. warning:: The Citadel login nodes can not access the internet.  This may impact build workflows that attempt to access external repositories.

Because the Citadel login nodes cannot reach repositories external to the system, you may need to alter your build workflows.  For these cases, you may be able to retrieve needed data. For cases where this is not possible, you can reach out to help@olcf.ornl.gov and request login access to Summit.  We can provide Summit login access by creating a sister project on Summit. You can then login to Summit to build your code and copy it to ``/sw/summit/mde/abc123_mde`` where ``abc123_mde`` is replaced by your Citadel project. This location is writable from Summit but only readable from Citadel. If the source code and data is small enough, you can also use the ``scp`` command from your whitelisted IP system to copy the data onto the Citadel login nodes directly.

More information on building codes for Citadel including programming environments, compilers, and available software can be found on :ref:`Summit User Guide<summit-user-guide>`. 


Running Batch Jobs
-------------------

Citadel and Summit share compute resources.  However, compute resources are reconfigured for SPI workloads to protect data.  To access the compute resources, you must first log into Citadel.  From Citadel you can access the compute nodes through the batch system as you would from Summit.  The notable difference between Summit and Citadel batch submission is the requirement to use SPI specific batch queues. SPI batch jobs must specify one of the following SPI specific batch queues:

-  batch-spi
-  debug-spi
-  batch-hm-spi

The batch queues mirror the purpose of the similarly named Summit queues. Details on each queue can be found in the :ref:`Summit User Guide<summit-user-guide>`. The SPI queues must be used to launch batch jobs from the Citadel nodes and can not be used directly from the moderate enclave Summit login nodes.

.. note:: To access Summit's compute resources for SPI workflows, you must first log into Citadel and then submit a batch job to one of the SPI specific batch queues.

Use of the queues will trigger configuration changes to the Summit compute nodes to allow enhanced data protection. Compute nodes will be booted before and after each SPI batch job. Compute nodes will be booted into an image that mounts only the Arx filesystem. The image will also restrict connections. Please note: the reboot process may cause a slight delay in job startup.

More details on batch job submission through LSF and launching a parallel job through jsrun can be found on :ref:`Summit User Guide<summit-user-guide>`.

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
