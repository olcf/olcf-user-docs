R and pbdR on Summit
====================

Loading R
---------

Several versions of R are available on Summit. You can see which by entering
the command ``module spider r``. Throughout this example, we will be using R
version 3.6.1.

If you have logged in with the default modules, then you need to swap
``xl`` for ``gcc`` and the load R:

.. code:: bash

   module swap xl gcc/6.4.0
   module load r/3.6.1

If we do that and launch R, then we see:

.. code:: r

   version
   ## platform       powerpc64le-unknown-linux-gnu
   ## arch           powerpc64le                  
   ## os             linux-gnu                    
   ## system         powerpc64le, linux-gnu       
   ## status                                      
   ## major          3                            
   ## minor          6.1                          
   ## year           2019                         
   ## month          07                           
   ## day            05                           
   ## svn rev        76782                        
   ## language       R                            
   ## version.string R version 3.6.1 (2019-07-05) 
   ## nickname       Action of the Toes           

   sessionInfo()
   ## R version 3.6.1 (2019-07-05)
   ## Platform: powerpc64le-unknown-linux-gnu (64-bit)
   ## Running under: Red Hat Enterprise Linux Server 7.6 (Maipo)
   ## 
   ## Matrix products: default
   ## BLAS/LAPACK: /autofs/nccs-svm1_sw/summit/r/3.6.1/rhel7.6_gnu6.4.0/lib64/R/lib/libRblas.so
   ## 
   ## locale:
   ## [1] C
   ## 
   ## attached base packages:
   ## [1] stats     graphics  grDevices utils     datasets  methods   base     
   ## 
   ## loaded via a namespace (and not attached):
   ## [1] compiler_3.6.1

How to Run an R Script
----------------------

Summit has a node hierarchy that can be very confusing for the
uninitiated. The `Summit User
Guide <https://docs.olcf.ornl.gov/systems/summit_user_guide.html>`__
explains this in depth. This has some consequences that may be unusual
for R programmers. A few important ones to note are:

-  You must have a script that you can run in batch, e.g. with
   ``Rscript`` or ``R CMD BATCH``
-  All data that needs to be visible to the R process (including the
   script and your packages) *must be on gpfs (not your home directory!)*.
-  You must launch your script from the launch nodes with ``jsrun``.

R Hello World Example
---------------------

We'll start with something very simple. The script is:

.. code:: r

   "hello world"

Save this in a file ``hw.r``, *somewhere on gpfs*. So say your project
is ``abc123``. You might have ``hw.r`` in
``/gpfs/alpine/abc123/proj-shared/my_hw_path/``.

There are two ways we can run this. One is with an interactive job, and
one is with a batch job. The interactive job doesn’t provide us with the
ability to run interactive R jobs on the compute nodes (using R interactively
on the compute node is complicated, so we do not discuss that here.). However,
it does allow us to interactively submit tasks to the compute nodes (launched
via ``jsrun``). This can be useful if you are trying to debug a script
that unexpectedly dies, without having to continuously submit jobs to
the batch queue (more on that in a moment).

We can start an interactive job with 1 node that will run for no more
than 10 minutes via:

.. code:: bash

   bsub -P $PROJECT -nnodes 1 -W 10 -Is $SHELL

Note that you need to either set the shell variable ``PROJECT`` to your
project identifier, or replace ``$PROJECT`` above with the identifier.

Once your job begins, you will again be at a shell prompt, but the host
should have changed from something like ``login1`` to ``batch1``
(numbering may differ). From here, you can launch the hello world
script.

With our interactive job running, we can run our script on the compute node
via:

.. code:: bash

   $ jsrun -n 1 Rscript hw.r
   ## [1] "hello world"

Our task run, we can enter ``exit`` into the terminal.

Of course, this involves no parallelism, since it is a single R session.
We will show how to run a basic MPI example with pbdR next.

pbdR Hello World Example
------------------------

The R code is:

.. code:: r

   suppressMessages(library(pbdMPI))

   msg = paste0("Hello from rank ", comm.rank(), " (local rank ", comm.localrank(), ") of ", comm.size())
   comm.print(msg, all.rank=TRUE, quiet=TRUE)

   finalize()

As before, save this file as, say, ``pbdr_hw.r`` somewhere on gpfs. This
time, we will get an interactive node with 2 nodes:

.. code:: bash

   bsub -P $PROJECT -nnodes 2 -W 10 -Is $SHELL

We will use 2 MPI ranks per node, giving 4 total ranks across the 2 nodes:

.. code:: bash

   $ jsrun -n4 -r2 Rscript hw.r 
   ## [1] "Hello from rank 0 (local rank 0) of 4"
   ## [1] "Hello from rank 1 (local rank 1) of 4"
   ## [1] "Hello from rank 2 (local rank 0) of 4"
   ## [1] "Hello from rank 3 (local rank 1) of 4"

At this point, we are still running the job and can submit more tasks to
the compute nodes if we like. If not, we can end the job by entering
``exit`` to the terminal.

So far we have seen how to launch jobs interactively. The other way to run our
script is to submit a batch job. To do that, we need to create a batch script:

.. code:: bash

   #!/bin/bash
   #BSUB -P ABC123
   #BSUB -W 10
   #BSUB -nnodes 2
   #BSUB -J rhw

   module load gcc/6.4.0
   module load r/3.6.1

   cd /gpfs/alpine/abc123/proj-shared/my_hw_path/

   jsrun -n4 -r2 Rscript hw.r 

Before continuing, a few comments. First you need to replace the example
project identifiers (``ABC123`` above) with your project. Second, load
the appropriate modules (here we just need R). Third, make sure that you
change directory to the appropriate place on gpfs. Fourth, add your
``jsrun`` call. Finally, you should also change the name of your job from
``rhw`` to something else by modifying the ``#BSUB -J`` line.

We need to save this to a file, say ``job.bs``. We submit the job to the
queue via ``bsub job.bs``. Once we do, we have to wait for the job to
start, then to run. After however long that takes, I get the output file
``rhw.679095``. If I cat that file, I see:

::

   [1] "Hello from rank 0 (local rank 0) of 4"
   [1] "Hello from rank 1 (local rank 1) of 4"
   [1] "Hello from rank 2 (local rank 0) of 4"
   [1] "Hello from rank 3 (local rank 1) of 4"

   ------------------------------------------------------------
   (additional output excluded for brevity's sake)

The information below the dashes which we omitted can be occasionally
helpful for debugging, say if there is some kind of hardware problem..

Common R Packages for Parallelism
---------------------------------

There are many R packages for parallel computing. Some popular ones include
the core parallel package, as well as high-level interface packages like
future and foreach. Many of these will use the OS fork mechanism to launch
additional R processes. This mechanism generally does not behave well with
MPI, which you must use (in the form of ``jsrun``) to push your task out
to the compute node(s). We highly recommend you avoid these packages if at
all possible, unless they are a frontend to Rmpi.

For parallelism, you should use pbdR packages, Rmpi directly, or an interface
which can use Rmpi as a backend. We address GPUs specifically next.

GPU Computing with R
--------------------

There are some R packages which can use GPUs, such as
`xgboost <https://xgboost.readthedocs.io/en/latest/>`__.
There is also the `gpuR <https://github.com/gpuRcore>`__ series of packages.
Several pbdR packages support GPU
computing. It is also possible to offload some linear algebra
computations (specifically matrix-matrix products, and methods which are
computationally dominated by them) to the GPU using `NVIDIA’s
NVBLAS <https://docs.nvidia.com/cuda/nvblas/index.html>`__.

If you want to do GPU computing on Summit with R, we would love to collaborate
with you (see contact details at the bottom of this document).

More Information
----------------

For more information about using R and pbdR effectively in an HPC environment
such as Summit, please see the `R and pbdR
articles <https://github.com/RBigData/pbdRticles/blob/master/README.md>`__.
These are long-form articles that introduce HPC concepts like MPI programming
in much more detail than we do here.

Also, if you want to use R and/or pbdR on Summit, please feel free to
contact us directly:

-  Mike Matheson - mathesonma AT ornl DOT gov
-  George Ostrouchov - ostrouchovg AT ornl DOT gov
-  Drew Schmidt - schmidtda AT ornl DOT gov

We are happy to provide support and collaboration for R and pbdR users on
Summit.
