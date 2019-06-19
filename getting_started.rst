#############################
Getting Started at the OLCF
#############################

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
------------------------

Access to OLCF resources is limited to approved projects and their
users. The type of project (INCITE, ALCC, or Director's Discretion) will
determine the application and review procedures. \*Quarterly reports are
required from industrial Director's Discretion projects only.

+--------------------------+------------------------------------------------------------------------+------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------+
|                          | **INCITE**                                                             | **Director's Discretion**                                                                      | **ALCC**                                                                                         |
+==========================+========================================================================+================================================================================================+==================================================================================================+
| **Allocations**          | Large                                                                  | Small                                                                                          | Large                                                                                            |
+--------------------------+------------------------------------------------------------------------+------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------+
| **Call for Proposals**   | Once per year                                                          | At any time                                                                                    | Once per year                                                                                    |
+--------------------------+------------------------------------------------------------------------+------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------+
| **Duration**             | 1 year                                                                 | Up to 12 months                                                                                | 1 year                                                                                           |
+--------------------------+------------------------------------------------------------------------+------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------+
| **Priority**             | High                                                                   | Medium                                                                                         | High                                                                                             |
+--------------------------+------------------------------------------------------------------------+------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------+
| **Closeout Report**      | yes                                                                    | yes                                                                                            | yes                                                                                              |
+--------------------------+------------------------------------------------------------------------+------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------+
| **Quarterly Reports**    | yes                                                                    | no*                                                                                            | yes                                                                                              |
+--------------------------+------------------------------------------------------------------------+------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------+
| **Where to apply**       | `Apply for INCITE <https://proposals.doeleadershipcomputing.org/>`__   | `Apply for DD </for-users/documents-forms/olcf-directors-discretion-project-application/>`__   | `Apply for ALCC <http://science.energy.gov/ascr/facilities/accessing-ascr-facilities/alcc/>`__   |
+--------------------------+------------------------------------------------------------------------+------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------+

 

What are the differences between project types?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
proposal <https://proposals.doeleadershipcomputing.org/>`__. **ALCC –**
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
all DD requests. Applications are accepted year round via the `OLCF
Director's Discretion Project
Application </for-users/documents-forms/olcf-directors-discretion-project-application/>`__.
**Vendor –** OLCF resources are also available to ORNL vendors.
Applications may be submitted year round by completing the `Vendor
Project
Application </support/getting-started/olcf-vendor-project-application/>`__.

.. raw:: html

   <div class="kb-note">

If you have questions about project types or application procedures,
feel free to contact the OLCF Accounts Team at accounts@ccs.ornl.gov.

.. raw:: html

   </div>

Approved projects will be granted an allocation of core-hours for a
period of time on one or more of the OLCF systems.

What happens after a project request is approved?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
about Summit, please visit the `Summit User
Guide </for-users/system-user-guides/summit>`__.

Applying for a user account
---------------------------

.. raw:: html

   <div class="kb-note">

**Note:** Project PIs do not receive a user account with project
creation, and must also submit a User Account Application.

.. raw:: html

   </div>

.. raw:: html

   <div class="kb-note">

**Note:** If you will be contributing to multiple projects, your user
account will need to be associated with each. If you already have a user
account and need to be added to additional projects, complete the User
Account Application and indicate you are an existing user.

.. raw:: html

   </div>

Collaborators involved with an approved and activated OLCF project can
apply for a user account associated with it. There are several steps in
receiving a user account, and we're here to help you through them.

#. Apply for an account using the `Account Request
   Form </support/getting-started/olcf-account-application>`__.
#. The principal investigator (PI) of the project must approve your
   account and system access. The Accounts Team will contact the PI for
   this approval.
#. If you have or will receive a RSA SecurID from our facility,
   additional paperwork will be sent to you via email to complete for
   identity proofing.
#. Foreign national participants will be sent an Oak Ridge National Lab
   (ORNL) Personnel Access System (PAS) request specific for the
   facility and cyber-only access. After receiving your response, it
   takes between 15-35 days for approval.
#. Fully-executed User Agreements with each institution having
   participants are required. If our records indicate your institution
   needs to sign either a User Agreement and/or Appendix A, the form(s)
   along with instructions will be sent via email.
#. If you are processing sensitive or proprietary data, additional
   paperwork is required and will be sent to you.

When all of the above steps are completed, your user account will be
created and you will be notified by email. Now that you have a user
account and it has been associated with a project, you're ready to get
to work. This website provides extensive documentation for OLCF systems,
and can help you efficiently use your project's allocation. We recommend
reading the `System User Guides </for-users/system-user-guides/>`__ for
the machines you will be using often.

Systems Available to All Projects
---------------------------------

After a user account has been approved and created, the requesting user
will be sent an email listing the system(s) to which the user has
requested and been given access. In addition to the system(s) listed in
the email, all users also have access to the following systems:

Home
~~~~

*Home* is a general purpose system that can be used to log into other
OLCF systems that are not directly accessible from outside the OLCF
network. For example, running the ``screen`` or ``tmux`` utility is one
common use of Home. Compiling, data transfer, or executing long-running
or memory-intensive tasks should never be performed on Home.

Connecting to the ``home`` Host
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Home can be accessed through ssh utilities:

.. code::

      ssh userid@home.ccs.ornl.gov 

Acceptable Tasks
^^^^^^^^^^^^^^^^

The Home system should only be used to access systems within the OLCF
network. The following are examples of appropriate uses of Home:

-  SSH
-  VI and other non-gui editors
-  Screen or other terminal multiplexers

Unacceptable Tasks
^^^^^^^^^^^^^^^^^^

The following are examples of inappropriate uses of Home:

-  Compiling
-  Data transfer
-  Long-running or memory-intensive tasks

Data Transfer Nodes
~~~~~~~~~~~~~~~~~~~

The *Data Transfer Nodes* (DTNs) are hosts specifically designed to
provide optimized data transfer between OLCF systems and systems outside
of the OLCF network. These nodes perform well on local-area transfers as
well as the wide-area data transfers for which they are tuned. The OLCF
recommends that users `employ these
nodes <../file-systems/#employing-data-transfer-nodes>`__ to improve
transfer speed and reduce load on computational systems' login and
service nodes.

High Performance Storage System (HPSS)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The *High Performance Storage System (HPSS)* provides tape storage for
large amounts of data created on OLCF systems. The HPSS can be accessed
from any OLCF system through the ``hsi`` utility. More information about
using HPSS can be found on the `HPSS section of the File Systems: Data
Storage & Transfers
page <../file-systems/#hpss-high-performance-storage-system>`__ in each
System User Guide.

Connecting for the first time
-----------------------------

With an active user account, you'll be able to log into any of the
systems allocated to your project(s). Use of the OLCF-provided RSA
SecurID fob is necessary since two-factor authentication is required. To
activate a new SecurID fob:

#. Initiate a SSH connection to ``username@home.ccs.ornl.gov``.
#. When prompted for a PASSCODE, enter the 6-digit code shown on the
   fob.
#. You will be asked if you are ready to set your PIN. Answer with "Y".
#. You will be prompted to enter a PIN. Enter a (4) to (6) digit number
   you can remember. You will then be prompted to re-enter your PIN.
#. Allow the 6-digit code to change (codes regenerate every 30 seconds).
   Once the (6) digits on your fob change, enter your PIN followed by
   the new (6) digits displayed on the fob.
#. Your PIN is now set, and your fob is activated for login to other
   OLCF systems.

Once activated, the RSA SecurID fob can be used to access OLCF systems.
When initiating a SSH connection to a system, you will be prompted to
enter your PASSCODE. Simply enter your PIN followed by the (6) digit
code shown on your SecurID fob and press enter. For example, if your pin
is ``1234`` and the (6) digits on the fob are ``000987``, you would
enter ``1234000987`` when prompted for a PASSCODE.

.. raw:: html

   <div class="kb-note">

**Note:** The 6-digit code displayed on the SecurID fob can only be used
once. If prompted for multiple PASSCODE entries, always allow the code
to change between attempts. Re-using a code can cause your account to be
automatically locked.

.. raw:: html

   </div>

Additional Resources
--------------------

We're here to provide support at every step. We also provide a
collection of `Tutorials </for-users/training/tutorials/>`__ for applied
technical demonstrations, `System User
Guides </for-users/system-user-guides/>`__, `Training
Events </for-users/training/>`__, and the `User Assistance
Center </for-users/user-assistance/>`__ to answer questions and resolve
technical issues as they arise.

