
*******
Swift/T
*******


Overview
========

Swift/T is a completely new implementation of the Swift language for
high-performance computing which translates Swift scripts into MPI programs
that use the Turbine (hence, /T) and ADLB runtime libraries. This tutorial
shows how to get up and running with Swift/T on Summit specifically. For more
information about Swift/T, please refer to their
`documentation <http://swift-lang.org/Swift-T/>`_.


Prerequisites
=============

Swift/T is available as a module on Summit, and it can be loaded as follows:

.. code-block:: console

    $ module load gcc/6.4.0  e4s/20.10  spectrum-mpi/10.3.1.2-20200121
    $ module load stc

You will also need to set the ``PROJECT`` environment variable:

.. code-block:: console

    $ export PROJECT="ABC123"


Hello world!
============

To run an example "Hello world" program with Swift/T on Summit, create a
file called ``hello.swift`` with the following contents:

.. code-block:: swift

    trace("Hello world!");


Now, run the program from a shell or script:

.. code-block:: console

    $ swift-t -m lsf hello.swift


The output should look something like the following:

.. code-block::

    TURBINE-LSF SCRIPT
    NODES=2
    PROCS=2
    PPN=1
    TURBINE_OUTPUT=/ccs/home/seanwilk/turbine-output/2021/06/18/17/11/29
    wrote: /ccs/home/seanwilk/turbine-output/2021/06/18/17/11/29/turbine-lsf.sh
    PWD: /autofs/nccs-svm1_home2/seanwilk/turbine-output/2021/06/18/17/11/29
    Job <1095064> is submitted to default queue <batch>.
    JOB_ID=1095064

Congratulations! You have now submitted a Swift/T job to Summit. Inspect the
``TURBINE_OUTPUT`` directory to find the workflow outputs and other artifacts. 


