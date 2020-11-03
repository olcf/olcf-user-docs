
**New to the Oak Ridge Leadership Computing Facility?**

Welcome! The information below introduces how we structure user
accounts, projects, and system allocations. It's all you need to know
about getting to work. In general, OLCF resources are granted to
projects in allocations, and are made available to the users associated
with each project.

.. image:: /images/projects_allocation_overview.png
   :width: 400px
   :height: 446px
   :align: center

Request a New Allocation
=============================

Access to OLCF resources is limited to approved projects and their
users. The type of project (INCITE, ALCC, or Director's Discretion) will
determine the application and review procedures. \*Quarterly reports are
required from industrial Director's Discretion projects only.

+--------------------------+----------------------------------------------------+-----------------------------+--------------------------------------------------------------------------------+
|                          | **INCITE**                                         | **Director's Discretion**   | **ALCC**                                                                       |
+==========================+====================================================+=============================+================================================================================+
| **Allocations**          | Large                                              | Small                       | Large                                                                          |
+--------------------------+----------------------------------------------------+-----------------------------+--------------------------------------------------------------------------------+
| **Call for Proposals**   | Once per year                                      | At any time                 | Once per year                                                                  |
+--------------------------+----------------------------------------------------+-----------------------------+--------------------------------------------------------------------------------+
| **Duration**             | 1 year                                             | Up to 12 months             | 1 year                                                                         |
+--------------------------+----------------------------------------------------+-----------------------------+--------------------------------------------------------------------------------+
| **Priority**             | High                                               | Medium                      | High                                                                           |
+--------------------------+----------------------------------------------------+-----------------------------+--------------------------------------------------------------------------------+
| **Closeout Report**      | yes                                                | yes                         | yes                                                                            |
+--------------------------+----------------------------------------------------+-----------------------------+--------------------------------------------------------------------------------+
| **Quarterly Reports**    | yes                                                | no*                         | yes                                                                            |
+--------------------------+----------------------------------------------------+-----------------------------+--------------------------------------------------------------------------------+
| **Where to apply**       | `Apply for INCITE                                  | `Apply for DD`_             | `Apply for ALCC                                                                |
|                          | <https://proposals.doeleadershipcomputing.org/>`__ |                             | <http://science.energy.gov/ascr/facilities/accessing-ascr-facilities/alcc/>`__ |
+--------------------------+----------------------------------------------------+-----------------------------+--------------------------------------------------------------------------------+

.. _Apply for DD: https://www.olcf.ornl.gov/for-users/documents-forms/olcf-directors-discretion-project-application/
 

What are the differences between project types?
------------------------------------------------

**INCITE –** The Novel Computational Impact on Theory and Experiment
(INCITE) program invites proposals for large-scale, computationally
intensive research projects to run at the OLCF. The INCITE program
awards sizeable allocations (typically, millions of processor-hours per
project) on some of the world’s most powerful supercomputers to address
grand challenges in science and engineering. There is an annual call for
INCITE proposals and awards are made on an annual basis. Please visit
the `Department of Energy Leadership Computing
website <http://www.doeleadershipcomputing.org>`__ for more information
and to `submit a
proposal <https://proposals.doeleadershipcomputing.org/>`__.

**ALCC –**
The ASCR Leadership Computing Challenge (ALCC) is open to scientists
from the research community in national laboratories, academia and
industry. The ALCC program allocates computational resources at the OLCF
for special situations of interest to the Department with an emphasis on
high-risk, high-payoff simulations in areas directly related to the
Department’s energy mission in areas such as advancing the clean energy
agenda and understanding the Earth’s climate, for national emergencies,
or for broadening the community of researchers capable of using
leadership computing resources. For more information or to submit a
proposal, please visit the `ASCR Leadership Computing Challenge
webpage <http://science.energy.gov/ascr/facilities/accessing-ascr-facilities/alcc/>`__.

**DD –** Director’s Discretion (DD) projects are dedicated to leadership
computing preparation, INCITE and ALCC scaling, and application
performance to maximize scientific application efficiency and
productivity on leadership computing platforms. The OLCF Resource
Utilization Council, as well as independent referees, review and approve
all DD requests. Applications are accepted year-round via the `OLCF
Director's Discretion Project
Application <https://www.olcf.ornl.gov/for-users/documents-forms/olcf-directors-discretion-project-application/>`__.

**Vendor –** OLCF resources are also available to ORNL vendors.
Applications may be submitted year-round by completing the `Vendor
Project
Application <https://www.olcf.ornl.gov/support/getting-started/olcf-vendor-project-application/>`__.

    If you have questions about project types or application procedures,
    feel free to contact the OLCF Accounts Team at accounts@ccs.ornl.gov.

Approved projects will be granted an allocation of core-hours for a
period of time on one or more of the OLCF systems.

What happens after a project request is approved?
---------------------------------------------------

Once a project request is approved, an OLCF Accounts Manager will
communicate the following steps for activation to the project's PI.

#. A signed Principal Investigator’s PI Agreement must be submitted with
   the project application.
#. Export Control: The project request will be reviewed by ORNL Export
   Control to determine whether sensitive or proprietary data will be
   generated or used. The results of this review will be forwarded to
   the PI. If the project request is deemed sensitive and/or
   proprietary, the OLCF Security Team will schedule a conference call
   with the PI to discuss the data protection needs.
#. ORNL Personnel Access System (PAS): All PI’s are required to be
   entered into the ORNL PAS system. An OLCF Accounts Manager will send
   the PI a PAS invitation to submit all the pertinent information.
   Please note that processing a PAS request may take 15 or more days.
#. User Agreement/Appendix A or Subcontract: A User Agreement/Appendix A
   or Subcontract must be executed between UT-Battelle and the PI’s
   institution. If our records indicate this requirement has not been
   met, all necessary documents will be provided to the applicant by an
   OLCF Accounts Manager.

Upon completion of the above steps, the PI will be notified that the
project has been created, and provided with the project ID and system
allocation details. At this time, project participants may apply for
user accounts.

Guidance on Summit Allocation Requests
-------------------------------------------

Summit delivers 8 times the computational performance of Titan’s 18,688
nodes, using only 4,608 nodes. Like Titan, Summit has a hybrid
architecture, and each node contains multiple IBM POWER9 CPUs and NVIDIA
Volta GPUs all connected together with NVIDIA’s high-speed NVLink. The
peak node performance is 42 teraflops per node with 512 gigabytes of
DDR4 memory, 96 gigabytes of HPM2 memory, and 1,600 gigabytes of
non-volatile memory. To provide a high rate of I/O throughput, the nodes
are connected in a non-blocking fat-tree using a dual-rail Mellanox EDR
InfiniBand interconnect. The OLCF Director's Discretionary (DD) program
allocates approximately 10% of the available Summit hours in a calendar
year. **Summit is allocated in *node* hours, and a typical DD project is
awarded between 15,000 - 20,000 *node* hours.** For more information
about Summit, please visit the :ref:`summit-user-guide`.

.. _applying-for-a-user-account:

Applying for a user account
================================

Collaborators involved with an approved and activated OLCF project can
apply for a user account associated with it. There are several steps in
receiving a user account, and we're here to help you through them.

.. note::
    Project PIs do not receive a user account with project
    creation, and must also apply.

.. note::
    If you will be contributing to multiple projects, your user
    account will need to be associated with each. For instructions on joining
    additional projects with an existing account, see the
    :ref:`Get access to additional projects<get-additional-projects>` section below.

#. First-time users should apply for an account using the `Account Request
   Form <https://www.olcf.ornl.gov/support/getting-started/olcf-account-application>`__.
#. When our accounts team begins processing your application, you will receive an automated
   email containing an unique 36-character confirmation code. Make note of it; you can use
   it to check the status of your application at any time.
#. The principal investigator (PI) of the project must approve your
   account and system access. We will make the project PI aware of your request.
#. Foreign national participants will be sent an Oak Ridge National Lab
   (ORNL) Personnel Access System (PAS) request specific for the
   facility and cyber-only access. After receiving your response, it
   takes between 15-35 days for approval.
#. Fully-executed Institutional User Agreements with each institution having
   participants are required. If our records indicate your institution
   needs to sign either an Institutional User Agreement and/or Appendix A, the proper
   form(s), along with instructions, will be sent via email.
#. If you are processing sensitive or proprietary data, additional
   paperwork is required and will be sent to you.
#. If you need an RSA SecurID token from our facility, the token and
   additional paperwork will be sent to you via email to complete identity proofing.

.. _checking-application-status:

Checking the status of your application
=======================================

You can check the general status of your application at any time using the myOLCF self-service
portal's `account status page <https://my.olcf.ornl.gov/pending/status>`__.
For more information, see the :ref:`myOLCF self-service portal documentation<myolcf-overview>`.
If you need to make further inquiries about your application, you may email our
Accounts Team at accounts@ccs.ornl.gov.

When all of the above steps are completed, your user account will be
created and you will be notified by email. Now that you have a user
account and it has been associated with a project, you're ready to get
to work. This website provides extensive documentation for OLCF systems,
and can help you efficiently use your project's allocation. We recommend
reading the :ref:`System User Guides<system-user-guides>` for the machines you will be using often.

.. _get-additional-projects:

Get access to additional projects
======================================

If you already have a user account at the OLCF, your existing credentials can be
leveraged across multiple projects.

If your user account has an associated RSA SecurID (i.e. you have an "OLCF Moderate" account), you
gain access to another project by logging in to the `myOLCF self-service portal <https://my.olcf.ornl.gov>`__
and filling out the application under `My Account` > `Join Another Project`. For more information,
see the :ref:`myOLCF self-service portal documentation<myolcf-overview>`.

If your user account has only an associated password (i.e. you have an "OLCF Open" account) you
gain access to another project by filling out the `Account Request Form
<https://www.olcf.ornl.gov/support/getting-started/olcf-account-application>`__; myOLCF is only
available to users with RSA SecurID tokens at this time.

In either case, once the PI of that project has been contacted and granted permission, your user account
will be added to the relevant charge accounts and unix groups, and you will see these additions
when you log in.
