.. _workflows-swiftt:

*******
Swift/T
*******


Overview
========

Swift/T is a new implementation of the Swift language for
high-performance computing which translates Swift scripts into MPI programs
that use the Turbine (hence, /T) and ADLB runtime libraries. This tutorial
shows how to get up and running with Swift/T on Frontier specifically. For more
information about Swift/T, please refer to its
`documentation <http://swift-lang.org/Swift-T/>`_.


Prerequisites
=============

Swift/T is available as a module on Frontier, and it can be loaded as follows:

.. code-block:: console

    $ module load swift-t/1.6.5

You will also need to set the ``PROJECT`` environment variable:

.. code-block:: console

    $ export PROJECT="ABC123"


Hello world!
============

To run an example "Hello world" program with Swift/T on Frontier, create a
file called ``hello.swift`` with the following contents:

.. code-block:: swift

    trace("Hello world!");


Now, run the program from a shell or script:

.. code-block:: console

    $ export PROJECT=ABC123
    $ swift-t -m slurm hello.swift


The output should look something like the following:

.. code-block::

    TURBINE-SLURM SCRIPT
    NODES=2
    PROCS=2
    PPN=1
    TURBINE_OUTPUT=/ccs/home/ketan2/turbine-output/2025/02/12/13/10/37
    TURBINE_HOME=/sw/frontier/conda_envs/swift_t/swift-t/turbine
    wrote: /ccs/home/ketan2/turbine-output/2025/02/12/13/10/37/turbine-slurm.sh
    JOB_ID=3037491

Congratulations! You have now submitted a Swift/T job to Frontier. Inspect the
``TURBINE_OUTPUT`` directory to find the workflow outputs and other artifacts. 

Cross Facility Workflow
=======================

This example demonstrates a continuously running cross-facility workflow. The
idea is that there is a science facility (eg. SNS at ORNL) that produces
scientific data to be processed by the remote compute facility (eg. OLCF at
ORNL). The data is continuously arriving in a designated directory at the compute facility from science facility. The
workflow picks data from that directory and does the processing to the
data to produce some output. The Swift source file ``workflow.swift`` looks as follows:

.. code-block:: swift
    
    import files;
    import io;
    
    app (void v) processdata(file f)
    {
     // change path per your location
     "/lustre/orion/proj-shared/stf053/swift-work/cross-facility/processdata.sh" f ;
    }

    for (boolean b = true; b; b=c)
    {
      boolean c;
      // You can change the number of data files while the workflow is running
      file data[] = glob("*.jpg");
      void V[];
      foreach f, i in data
      {
        V[i] = processdata(f);
      }
      printf("processed %i files.", size(V)) => c = true;
    }

In order to demonstrate the data generation, we have a script that downloads image data from the NOAA website periodically. The image is a geographical image showing current cloud cover over south-east US. The code ``gendata.sh`` looks like so:

.. code-block:: bash
   
   #!/bin/bash
   set -eu

   function cleanup() {
     \rm -f ./data/earth*.jpg
   }

   while true
   do
     uid=$(uuidgen | awk -F- '{print $1}')
     wget -q https://cdn.star.nesdis.noaa.gov/GOES16/ABI/SECTOR/se/GEOCOLOR/1200x1200.jpg -O ./data/earth${uid}.jpg
     sleep 5
     trap cleanup EXIT
   done

Next, we have the data processing script called ``processdata.sh`` that looks as follows:

.. code-block:: bash
   
   #!/bin/bash
   set -eu

   TASK=convert
   DATA=$1
   echo "\nProcessing ${DATA}\n"
   ${TASK} ${DATA} -fuzz 10% -fill white -opaque white -fill black +opaque white -format "%[fx:100*mean]" info:
   sleep 5

The above script computes the cloud cover percentage by looking at the amount of white pixels in the image. Note that it uses ImageMagick's ``convert`` utility.

The suggested directory structure is to have a outer directory say ``swift-work`` that has the swift source and shell scripts. Inside of ``swift-work`` create a new directory called ``data``.

Additionally, we will need two terminals open. In the first terminal window, navigate to the ``swift-work`` directory and invoke the data generation script like so:

.. code-block:: console

    $ ./gendata.sh

In the second terminal, we will run the swift workflow as follows (make sure to change the project name per your allocation):

.. code-block:: console

    $ module load imagemagick # for convert utility
    $ export WALLTIME=00:10:00
    $ export PROJECT=STF019
    $ export TURBINE_OUTPUT=/lustre/orion/proj-shared/stf053/swift-data
    $ swift-t -O0 -m slurm workflow.swift

If all goes well, and when the job starts running, the output will be produced in the ``data`` directory ``output.txt`` file.
