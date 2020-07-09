****************************
AFW Policy Guides
****************************

Data Use
--------

Prohibited Data
^^^^^^^^^^^^^^^

The National Center for Computational Science (NCCS) computer systems 
are operated in support of United States Air Force (USAF) 557th Weather Wing 
and only contain data related to scientific research and do not contain
personally identifiable information (data that falls under the Privacy
Act of 1974 5U.S.C. 552a). Use of NCCS resources to store, manipulate,
or remotely access classified information, unclassified controlled nuclear
information (UCNI), naval nuclear propulsion information (NNPI), the design
or development of nuclear, biological, or chemical weapons or any weapons
of mass destruction is prohibited. Authors/generators/owners of information
are responsible for its correct categorization as sensitive or non-sensitive.
Owners of sensitive information are responsible for its secure handling,
transmission, processing, storage, and disposal on NCCS systems.
Principal investigators, users, or project delegates that use NCCS
resources, or are responsible for overseeing projects that use NCCS
resources, are strictly responsible for knowing whether their project
generates any of these prohibited data types or information that falls
under Export Control. For questions, contact help@nccs.gov.

Confidentiality, Integrity, and Availability
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The NCCS systems provide protections to maintain the confidentiality,
integrity, and availability of user data. Measures include the
availability of file permissions, archival systems with access control
lists, and parity and CRC checks on data paths and files. It is the
user’s responsibility to set access controls appropriately for the data.
In the event of system failure or malicious actions, the NCCS makes no
guarantee against loss of data or that a user’s data can be accessed,
changed, or deleted by another individual. It is the user’s
responsibility to insure the appropriate level of backup and integrity
checks on critical data and programs.

Administrator Access to Data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

NCCS resources are federal computer systems, and as such, users should
have no explicit or implicit expectation of privacy. NCCS employees and
authorized vendor personnel with “root” privileges have access to all
data on NCCS systems. Such employees can also login to NCCS systems as
other users. As a general rule, NCCS employees will not discuss your
data with any unauthorized entities nor grant access to data files to
any person other than the UNIX “owner” of the data file, except in the
following situations:

-  When the owner of the data requests a change of ownership.
-  In situations of suspected abuse/misuse computational resources,
   criminal activity, or cyber-security violations.

Note that the above applies even to project PIs. In general, the NCCS
will not overwrite existing UNIX permissions on data files owned by
project members for the purpose of granting access to the project PI.
Project PIs should work closely with project members throughout the
duration of the project to ensure UNIX permissions are set
appropriately.

Data Modification/Destruction
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Users are prohibited from taking unauthorized actions to intentionally
modify or delete information or programs.

Data Retention
^^^^^^^^^^^^^^

The NCCS reserves the right to remove any data at any time and/or
transfer data to other users working on the same or similar project once
a user account is deleted or a person no longer has a business
association with the NCCS. After a sensitive project has ended or has
been terminated, all data related to the project must be purged from all
NCCS computing resources within 30 days.

Software Use
------------

All software used on NCCS computers must be appropriately acquired and
used according to the appropriate software license agreement.
Possession, use, or transmission of illegally obtained software is
prohibited. Likewise, users shall not copy, store, or transfer
copyrighted software, except as permitted by the owner of the copyright.
Only export-controlled codes approved by the Export Control Office may
be run by parties with sensitive data agreements.

Malicious Software
^^^^^^^^^^^^^^^^^^

Users must not intentionally introduce or use malicious software such as
computer viruses, Trojan horses, or worms.

Reconstruction of Information or Software
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Users are not allowed to reconstruct information or software for which
they are not authorized. This includes but is not limited to any reverse
engineering of copyrighted software or firmware present on NCCS
computing resources.

User Accountability
-------------------

Users are accountable for their actions and may be held accountable to
applicable administrative or legal sanctions.

Monitoring and Privacy
^^^^^^^^^^^^^^^^^^^^^^

Users are advised that there is no expectation of privacy of your
activities on any system that is owned by, leased or operated by
UT-Battelle on behalf of the U.S. Department of Energy (DOE). 
UT-Battelle retains the right to monitor all activities on these systems, to
access any computer files or electronic mail messages, and to disclose
all or part of information gained to authorized individuals or
investigative agencies, all without prior notice to, or consent from,
any user, sender, or addressee. This access to information or a system
by an authorized individual or investigative agency is in effect during
the period of your access to information on a DOE computer and for a
period of three years thereafter. NCCS personnel and users are required
to address, safeguard against, and report misuse, abuse and criminal
activities. Misuse of NCCS resources can lead to temporary or permanent
disabling of accounts, loss of DOE allocations, and administrative or
legal actions. Users who have not accessed a NCCS computing resource in
at least 6 months will be disabled. They will need to reapply to regain
access to their account. All users must reapply annually.

Authentication and Authorization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All users are required to use a one-time password for authentication.
Tokens will be distributed to users. Users will be required to
create a Personal Identification Number (PIN). This is used in
conjunction with a generated token code as part of a two-factor
authentication implementation. Accounts on the NCCS machines are for the
exclusive use of the individual user named in the account application.
Users should not share accounts or tokens with anyone. If evidence is
found that more than one person is using an account, that account will
be disabled immediately. Users are not to attempt to receive unintended
messages or access information by some unauthorized means, such as
imitating another system, impersonating another user or other person,
misuse of legal user credentials (usernames, tokens, etc.), or by
causing some system component to function incorrectly. Users are
prohibited from changing or circumventing access controls to allow
themselves or others to perform actions outside their authorized
privileges. Users must notify the NCCS immediately when they become
aware that any of the accounts used to access NCCS have been
compromised. Users should inform the NCCS promptly of any changes in
their contact information (E-mail, phone, affiliation, etc.) Updates
should be sent to accounts@ccs.ornl.gov.

Foreign National Access
^^^^^^^^^^^^^^^^^^^^^^^

Applicants who appear on a restricted foreign country listing in section
15 CFR 740.7 License Exceptions for Computers are denied access based on
US Foreign Policy. The countries cited are Cuba, Iran, North Korea,
Sudan, and Syria. Additionally, no work may be performed on NCCS
computers on behalf of foreign nationals from these countries.

Denial of Service
^^^^^^^^^^^^^^^^^

Users may not deliberately interfere with other users accessing system
resources.  

AFW Data Management Policy
======================

.. note::
    This details an official policy of the NCCS, and must be
    agreed to by the following persons as a condition of access to or use of
    NCCS computational resources:

    -  Principal Investigators
    -  All Users

    **Title:** AFW Data Management Policy **Version:** 1.0

Introduction
------------

The NCCS provides a comprehensive suite of hardware and software
resources for the creation, manipulation, and retention of scientific
data. This document comprises guidelines for acceptable use of those
resources. It is an official policy of the NCCS, and as such, must be
agreed to by relevant parties as a condition of access to and use of
NCCS computational resources.

Data Storage Resources
^^^^^^^^^^^^^^^^^^^^^^

The NCCS provides an array of data storage platforms, each designed with
a particular purpose in mind. Storage areas are broadly divided into two
categories: those intended for user data and those intended for project
data. Within each of the two categories, we provide different sub-areas,
each with an intended purpose.


User Home
^^^^^^^^^

Home directories for each user are NFS-mounted on all NCCS systems and
are intended to store long-term, frequently-accessed user data. User
Home areas are backed up on a daily basis. This file system does not
generally provide the input/output (I/O) performance required by most
compute jobs, and is not available to compute jobs on most systems. See
the section :ref:`retention-policy` for more details on
applicable quotas, backups, purge, and retention timeframes.

Project Home
^^^^^^^^^^^^

Project Home directories are NFS-mounted on selected NCCS systems and
are intended to store long-term, frequently-accessed data that is needed
by all collaborating members of a project. Project Home areas are backed
up on a daily basis. This file system does not generally provide the
input/output (I/O) performance required by most compute jobs, and is not
available to compute jobs on most systems. See the section
:ref:`retention-policy` for more details on applicable
quotas, backups, purge, and retention timeframes.

Member Work
^^^^^^^^^^^

Project members get an individual Member Work directory for each associated
project; these reside in the high performance parallel file system
on large, fast disk areas intended for global (parallel) access to
temporary/scratch storage. Member Work areas are not shared with other
users of the system and are intended for project data that the user does
not want to make available to other users. Member Work directories are
provided commonly across all systems. Because of the scratch nature of the
file system, it is not backed up. If a file system associated
with your Member Work directory is nearing capacity, the NCCS may contact
you to request that you reduce the size of your Member Work directory. See
the section :ref:`retention-policy` for more details on applicable quotas,
backups, purge, and retention timeframes.

Project Work
^^^^^^^^^^^^

Each project is granted a Project Work directory; these reside in the
high-performance parallel file system on large, fast disk
areas intended for global (parallel) access to temporary/scratch storage.
Project Work directories can be accessed by all members of a project and
are intended for sharing data within a project. Project Work directories
are provided commonly across most systems. Because of the scratch nature of
the file system, it is not backed up. If a file system associated
with Project Work storage is nearing capacity, the NCCS may contact the PI
of the project to request that he or she reduce the size of the Project
Work directory. See the section :ref:`retention-policy` for more details on
applicable quotas, backups, purge, and retention timeframes.

World Work
^^^^^^^^^^

Each project has a World Work directory that resides in the 
high-capacity parallel file system on large, fast disk areas intended
for global (parallel) access to temporary/scratch storage. World Work areas
can be accessed by all users of the system and are intended for sharing of
data between projects. World Work directories are provided commonly across
most systems. Because of the scratch nature of the file system, it is not
backed up. If a file system associated with World Work
storage is nearing capacity, the NCCS may contact the PI of the project to
request that he or she reduce the size of the World Work directory. See the
section :ref:`retention-policy` for more details on applicable quotas,
backups, purge, and retention timeframes.



.. _retention-policy:

Data Retention, Purge, & Quotas
-------------------------------


Data Retention Overview
^^^^^^^^^^^^^^^^^^^^^^^

By default, there is no lifetime retention for any data on NCCS
resources. The NCCS specifies a limited post-deactivation timeframe
during which user and project data will be retained. When the retention
timeframe expires, the NCCS retains the right to delete data. If you
have data retention needs outside of the default policy, please notify
the NCCS.

User Data Retention
^^^^^^^^^^^^^^^^^^^

The user data retention policy exists to reclaim storage space after a
user account is deactivated, e.g., after the user’s involvement on all
NCCS projects concludes. By default, the NCCS will retain data in
user-centric storage areas only for a designated amount of time after
the user’s account is deactivated. During this time, a user can request
a temporary user account extension for data access. See the section
:ref:`retention-policy` for details on retention
timeframes for each user-centric storage area.

Project Data Retention
^^^^^^^^^^^^^^^^^^^^^^

The project data retention policy exists to reclaim storage space after
a project ends. By default, the NCCS will retain data in project-centric
storage areas only for a designated amount of time after the project end
date. During this time, a project member can request a temporary user
account extension for data access. See the section :ref:`retention-policy`
for details on purge and retention timeframes
for each project-centric storage area.


Data Purges
^^^^^^^^^^^

Data purge mechanisms are enabled on some NCCS file system directories
in order to maintain sufficient disk space availability for job execution.
By default, these purge mechanisms are disabled on Air Force partnership
file systems. Should the file system exceed critical capacity thresholds,
the NCCS reserves the right to purge files to regain file system stability. NCCS
will discuss this with Air Force administration before purging data.

Storage Space Quotas
^^^^^^^^^^^^^^^^^^^^

Each user-centric and project-centric storage area has an associated
quota, which could be a hard (systematically-enforceable) quota or a
soft (policy-enforceable) quota. Storage usage will be monitored
continually. When a user or project exceeds a soft quota for a storage
area, the user or project PI will be contacted and will be asked if at
all possible to purge data from the offending area. See the section
:ref:`retention-policy` for details on quotas for each storage area.
