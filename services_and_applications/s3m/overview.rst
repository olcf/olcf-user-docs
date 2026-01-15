.. _s3m_overview:

********
Overview
********

What is S3M (OLCF API)?
=======================

.. note::

    All elements of the OLCF Facility API in an
    **early release** state and are subject to change without notification.
    As such these resources should only be used for the purposes of testing
    and should not be relied upon for any production workflows.

The Secure Scientific Service Mesh (S3M) is an OLCF facility-managed gateway
which aims to provide access to a wide range of API services. Y This is
done via OLCF-Project level access tokens which can then be used with an
OLCF-hosted API.

S3M Use Cases
-------------

* Submit Slurm jobs programmatically
* Set up data streaming services for OLCF compute resources
* View OLCF center/resource statuses programmatically

Token Policy
------------

**Draft** - *Last updated 8/15/2025*

OLCF-issued API tokens, known as Project Access Tokens, are explicitly
scoped to individual projects and may only be used for authorized actions
within the boundaries of the project for which they were generated. While
tokens are tied to project access, the user who generates a token remains
ultimately responsible for its use. Any misuse or abuse of an API token,
whether intentional or accidental, may result in strict disciplinary action,
including revocation of access. To minimize risk, users must handle tokens
with the utmost confidentiality, taking all necessary precautions to avoid
accidental exposure, such as in source code repositories, shared documentation,
or other public contexts. If a token is exposed, the user must immediately
revoke it and generate a new one. Additionally, only project members with
valid OLCF accounts are authorized to interact with the project’s API tokens;
individuals without an OLCF account, even if associated with the project,
are prohibited from using or accessing the token. In the event of token
misuse, malicious activity, or a compromised token, users must promptly
notify OLCF staff at <help@olcf.ornl.gov> to mitigate risks and take
corrective measures, including revoking the compromised token and ensuring
the security of associated accounts and projects.

Contact Us
----------

As we continue to develop the OLCF API services we
are eager to hear about your questions, challenges, or
general feedback. Please reach out: ``olcf-s3m@email.ornl.gov``
