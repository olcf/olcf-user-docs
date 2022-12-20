.. _citadel-user-guide:

*******************
Citadel User Guide
*******************

The OLCF's **Scalable Protected Infrastructure (SPI)** provides resources and protocols that enable researchers to process protected data at scale.  The SPI is built around a framework of security protocals that allows researchers to process large datasets containing private information.  Using this framework researchers can use the center's large HPC resources to compute data containing protected health information (PHI), personally identifiable information (PII), data protected under International Traffic in Arms Regulations, and other types of data that require privacy.  

The SPI utilizes a mixture of existing resources combined with specialized resources targeted at SPI workloads.  Because of this, many processes used within the SPI are very similar to those used for standard non-SPI. 

.. note::
    The SPI provides access to the OLCF's Summit resource for compute.  To safely separate SPI and non-SPI workflows, SPI workflows must use a separate login node named :ref:`Citadel<spi-compute-citadel>`.  Citadel provides a login node specifically for SPI workflows. 


Summit Documentation
=====================
The SPI resource, :ref:`Citadel<spi-compute-citadel>`, utilizes Summit's compute resources but adds measures to ensure separation of SPI and non-SPI workflows and data.  At a high level :ref:`Citadel<spi-compute-citadel>` is a Summit login node for SPI workflows. Because of this, the :ref:`Summit User Guide<summit-documentation-resources>` provides much of the needed documentation on system details and use.  

More information on the Programming Environment, Compiling, and Running Batch Jobs can be found in the :ref:`Summit User Guide<summit-documentation-resources>`.



Citadel (SPI) Documentation
============================
For notable differences between Citadel and Summit, please see the :ref:`SPI<spi-compute-citadel>` documentation.

.. note::
    The login node used by Citadel mirrors the Summit login nodes in hardare and software.  The login node also provides access to the same compute resources as are accessible from Summit. 

