.. _hpss:

**************************
HPSS Data Archival System
**************************

Currently, HSI and HTAR are offered for archiving data into HPSS or retrieving
data from the HPSS archive. For optimal transfer performance, we recommend
sending a file of 768 GB or larger to HPSS. The minimum file size that we
recommend sending is 512 MB. HPSS will handle files between 0K and 512 MB, but
write and read performance will be negatively affected. For files smaller than
512 MB we recommend bundling them with HTAR to achieve an archive file of at
least 512 MB.

Using Globus
=============

The OLCF users have access to a new functionality, using Globus to transfer
files to HPSS through the endpoint "**OLCF HPSS**". Globus has restriction of 8
active transfers across all the users. Each user has a limit of 3 active
transfers, so it is required to transfer a lot of data on each transfer than
less data across many transfers. If a folder is constituted with mixed files
including thousands of small files (less than 1MB each one), it would be better
to tar the small files.  Otherwise, if the files are larger, Globus will handle
them. To transfer the files, follow these steps:

- Visit www.globus.org and login

.. image:: /images/globus_first_page.png
   :align: center


- Then select the organization that you belong, if you don't work for ORNL, do
  not select ORNL. If your organization is not in the list, create a Globus
  account

.. image:: /images/globus_organization.png
   :align: center


- Search for the endpoint **OLCF DTN**

.. image:: /images/search_endpoint1.png
   :align: center

.. image:: /images/search_endpoint2.png
   :align: center


- Declare path

.. image:: /images/globus_first_endpoint.png
   :align: center


- Open a second panel to declare the new endpoint called **OLCF HPSS** and use
  the appropriate path for HPSS

.. image:: /images/globus_second_endpoint_hpss.png
   :align: center

.. image:: /images/globus_second_endpoint_hpss2.png
   :align: center


- Select your file/folder and click start. hen an activity report will appear
  and you can click on it to see the status. When the transfer is finished or
  failed, you will receive an email

.. image:: /images/globus_select_start.png
   :align: center

.. image:: /images/globus_activity.png
   :align: center


.. image:: /images/globus_activity_information.png
   :align: center

.. image:: /images/globus_activity_done.png
   :align: center


Using HSI
==========

When retrieving data from a tar archive larger than 1 TB, we recommend that you
pull only the files that you need rather than the full archive.  Examples of
this will be given in the htar section below. Issuing the command ``hsi`` will
start HSI in interactive mode. Alternatively, you can use:

     ``hsi [options] command(s)``

...to execute a set of HSI commands and then return. To list you files on the
HPSS, you might use:

     ``hsi ls``

``hsi`` commands are similar to ``ftp`` commands. For example, ``hsi get`` and
``hsi put`` are used to retrieve and store individual files, and ``hsi mget``
and ``hsi mput`` can be used to retrieve multiple files. To send a file to HPSS,
you might use:

     ``hsi put a.out : /hpss/prod/[projid]/users/[userid]/a.out``

To retrieve one, you might use:

     ``hsi get /hpss/prod/[projid]/proj-shared/a.out``

Here is a list of commonly used hsi commands.

========== ====================================================================
Command    Function
========== ====================================================================
cd         Change current directory
get, mget  Copy one or more HPSS-resident files to local files
cget       Conditional get - get the file only if it doesn't already exist
cp         Copy a file within HPSS
rm mdelete Remove one or more files from HPSS
ls         List a directory
put, mput  Copy one or more local files to HPSS
cput       Conditional put - copy the file into HPSS unless it is already there
pwd        Print current directory
mv         Rename an HPSS file
mkdir      Create an HPSS directory
rmdir      Delete an HPSS directory
========== ====================================================================

 

Additional HSI Documentation
-----------------------------

There is interactive documentation on the ``hsi`` command available by running:

     ``hsi help``

Additionally, documentation can be found at the Gleicher Enterprises website,
including an `HSI Reference Manual
<http://pal.mgleicher.us/HSI/hsi/hsi_reference_manual_2/>`__ and man pages for
`HSI <http://pal.mgleicher.us/HSI/hsi/hsi_man_page.html>`__.

Using HTAR
===========

The ``htar`` command provides an interface very similar to the traditional
``tar`` command found on UNIX systems. It is used as a command-line interface.
The basic syntax of ``htar`` is:

   ``htar -{c|K|t|x|X} -f tarfile [directories] [files]``

As with the standard Unix ``tar`` utility the ``-c``, ``-x``, and ``-t``
options, respectively, function to create, extract, and list tar archive files.
The ``-K`` option verifies an existing tarfile in HPSS and the ``-X`` option can
be used to re-create the index file for an existing archive. For example, to
store all files in the directory ``dir1`` to a file named
``/hpss/prod/[projid]/users/[userid]/allfiles.tar`` on HPSS, use the command:

     ``htar -cvf /hpss/prod/[projid]/users/[userid]/allfiles.tar dir1/*``

To retrieve these files:

     ``htar -xvf  /hpss/prod/[projid]/users/[userid]/allfiles.tar``

``htar`` will overwrite files of the same name in the target directory.  **When
possible, extract only the files you need from large archives.** To display the
names of the files in the ``project1.tar`` archive file within the HPSS home
directory:

     ``htar -vtf  /hpss/prod/[projid]/users/[userid]/project1.tar``

To extract only one file, ``executable.out``, from the ``project1`` directory in
the Archive file called `` /hpss/prod/[projid]/users/[userid]/project1.tar``:

     ``htar -xm -f project1.tar project1/ executable.out``

To extract all files from the ``project1/src`` directory in the archive file
called ``project1.tar``, and use the time of extraction as the modification
time, use the following command:

     ``htar -xm -f  /hpss/prod/[projid]/users/[userid]/project1.tar project1/src``

HTAR Limitations
-----------------

The ``htar`` utility has several limitations.

Apending data
^^^^^^^^^^^^^

You cannot add or append files to an existing archive.

File Path Length
^^^^^^^^^^^^^^^^

File path names within an ``htar`` archive of the form prefix/name are limited
to 154 characters for the prefix and 99 characters for the file name. Link names
cannot exceed 99 characters.

Size
^^^^

There are limits to the size and number of files that can be placed in an HTAR
archive.

=================================== ========================
Individual File Size Maximum        68GB, due to POSIX limit
Maximum Number of Files per Archive 1 million
=================================== ========================

For example, when attempting to HTAR a directory with one member file larger
that 64GB, the following error message will appear:

.. code::

   $ htar -cvf  /hpss/prod/[projid]/users/[userid]/hpss_test.tar hpss_test/

   INFO: File too large for htar to handle: hpss_test/75GB.dat (75161927680 bytes)
   ERROR: 1 oversize member files found - please correct and retry
   ERROR: [FATAL] error(s) generating filename list
   HTAR: HTAR FAILED

Additional HTAR Documentation
------------------------------

The HTAR user's guide can be found at the Gleicher Enterprises website `Gleicher
Enterprises website <http://pal.mgleicher.us/HSI/htar/htar_user_guide.html>`__,
including `the HTAR man page
<http://pal.mgleicher.us/HSI/htar/htar_man_page.html>`__.

