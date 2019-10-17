.. _dtn-user-guide:

**************************
Data Transfer Nodes (DTNs)
**************************

.. _dtn-system-overview:

System Overview
===============
The Data Transfer Nodes ("DTNs"; ``dtn.ccs.ornl.gov``) are hosts specifically
designed to provide optimized data transfer between OLCF systems and systems
outside of the OLCF network. These nodes perform well on local-area transfers
as well as the wide-area data transfers for which they are tuned. The OLCF
recommends that users use these nodes to improve transfer speed and reduce load
on computational systems’ login and service nodes.

.. _dtn-access-connecting:

Access & Connecting
===================
DTN access is automatically granted to all enabled OLCF users.

To connect to the DTNs, SSH to ``dtn.ccs.ornl.gov``. For example:

::

    ssh username@dtn.ccs.ornl.gov

For more information on connecting to OLCF resources, see
:ref:`connecting-to-olcf`.
