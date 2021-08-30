.. _home-user-guide:

***********
Home 
***********

.. _home-system-overview:

System Overview
===============

``home.ccs.ornl.gov`` (Home) is a general purpose system that can be used to
log into other OLCF systems that are not directly accessible from outside the
OLCF network. For example, running the ``screen`` or ``tmux`` utility is one
common use of Home. Compiling, data transfer, or executing long-running or
memory-intensive tasks should never be performed on Home.


.. _home-access-connecting:

Access & Connecting
===================

Home access is automatically granted to all enabled OLCF users.

To connect to Home, SSH to ``home.ccs.ornl.gov``. For example:

::

    ssh username@home.ccs.ornl.gov

For more information on connecting to OLCF resources, see
:ref:`connecting-to-olcf`.

Usage
===========

Acceptable Tasks
----------------

The Home system should only be used to access systems within the OLCF network.
The following are examples of appropriate uses of Home:

* RSA SecurID Token setup
* SSH 
* Vi and other non-GUI editors
* Screen or other terminal multiplexers

Unacceptable Tasks
------------------

The following are examples of inappropriate uses of Home:

* Compiling
* Data Transfers
* Long-running or memory-intensive processes
