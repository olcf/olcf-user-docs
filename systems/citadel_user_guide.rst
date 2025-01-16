.. _citadel-user-guide:

*******************
Citadel User Guide
*******************

The OLCF's **Scalable Protected Infrastructure (SPI)** provides resources and protocols that enable researchers to process protected data at scale.  The SPI is built around a framework of security protocols that allows researchers to process large datasets containing private information.  Using this framework researchers can use the center's large HPC resources to compute data containing protected health information (PHI), personally identifiable information (PII), data protected under International Traffic in Arms Regulations, and other types of data that require privacy.  

The SPI utilizes a mixture of existing resources combined with specialized resources targeted at SPI workloads.  Because of this, many processes used within the SPI are very similar to those used for standard non-SPI.  This page lists the differences you may see when using OLCF resources to execute SPI workflows.  The page will also point to sections within the site where more information on standard non-SPI use can be found.


What is Citadel
----------------

The National Center for Computational Science (NCCS) and the Oak Ridge Leadership Computing Facility (OLCF) have implemented the CITADEL security framework as **part of their Scalable Protected Infrastructure (SPI)**. This infrastructure provides resources and protocols that enable researchers to process protected data at scale. With the CITADEL framework, **researchers can use the OLCF’s large HPC resources to compute** data containing protected health information (PHI), personally identifiable information (PII), data protected under International Traffic in Arms Regulations, and other types of data that require privacy.

.. note::
  With the CITADEL framework, researchers can use the OLCF’s large HPC resources including **Frontier** to compute data containing protected health information (PHI), personally identifiable information (PII), data protected under International Traffic in Arms Regulations, and other types of data that require privacy.

The NCCS CITADEL security framework was originally conceived to facilitate the large-scale analysis of protected health information (PHI) data from the US Department of Veterans Affairs' (VA) Million Veteran Program. The NCCS SPI team, with assistance from ORNL Risk Management and ORNL’s Information Technology Services Division (ITSD), refined the initial prototype and expanded CITADEL's capabilities to accommodate a diverse array of programs, projects, and sponsors.

Although the facility already adheres to the National Institute of Standards and Technology’s security and privacy controls for moderate Official Use Only data, CITADEL was crafted to enforce security measures for handling vast datasets that encompass types of data necessitating heightened privacy safeguards on systems overseen by the OLCF. Extra precautions have been taken to manage private data such that it cannot be accessed by other researchers or used by other projects. For example, HIPAA-protected data for a project sponsored by the VA will be kept absolutely separate from HIPAA-protected data for a projected sponsored by the Centers for Medicare and Medicaid Services (CMS).

CITADEL, having undergone comprehensive technical-, legal-, and policy-oriented reviews and received third-party accreditation, has presented new possibilities for research projects that previously could not utilize OLCF systems due to the nature of their data.  


.. note::
    The :ref:`Citadel framework<spi-compute-citadel>` provides the ability to compute SPI workflows on the OLCF's Frontier resources. 


Citadel (SPI) Documentation
============================
For details on the Citadel framework and how it dffers from the non-SPI Frontier workflows, please see the :ref:`SPI documentation<spi-compute-citadel>`.


