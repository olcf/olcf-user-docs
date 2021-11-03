.. _workflows:

#########
Workflows
#########

************
Introduction
************

Scientific workflows are a cornerstone of modern scientific computing, and 
are used almost universally across scientific domains. Workflow systems provide 
abstraction and automation for describing complex computational applications 
that require efficient and robust management of large volumes of data, which 
are typically stored/processed on heterogeneous, distributed resources.

A workflow can analyze terabyte-scale data sets, be composed of million 
individual tasks, require coordination between heterogeneous tasks, manage 
tasks that execute for miliseconds to hours, and can process data streams,
files, and data placed in object stores. The computations can be single core
workloads, loosely coupled computations (like MapReduce), or tightly coupled
(like MPI-based parallel programs) all within a single workflow, and can run
in dispersed computing environments.

.. note:: 
    If you want to learn the basics about workflows and distributed 
    computing, you can access this set of 
    `pedagogic modules <https://eduwrench.org/pedagogic_modules/workflows/>`_
    that will introduce you to the workflow model of computation that is 
    used in many scientific applications.

***********************************
Running Workflows on OLCF Resources
***********************************

Sometimes, assembling workflows requires dedicated software like workflow
management systems, especially when the time comes to scale. OLCF supports a
number of different packages, especially through our :ref:`Slate<slate>`
container orchestration service.

.. toctree::
   :maxdepth: 1

   entk
   parsl
   swift_t
