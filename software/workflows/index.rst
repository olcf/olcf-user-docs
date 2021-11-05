.. _workflows:

#########
Workflows
#########

Scientific workflows are a cornerstone of modern scientific computing, and 
are used almost universally across scientific domains. Workflow systems provide 
**abstraction** and **automation** for describing complex computational 
applications that require efficient and robust management of large volumes of 
data, which are typically stored/processed on heterogeneous, distributed 
resources.

At OLCF, we are thriving to offer users with a selection of cutting-edge 
workflow systems that are *easy-to-use* while providing a comprehensive set 
of features for supporting a large range of use cases from different science
domains.

**What is a Workflow?**
 Many computationally intensive scientific applications have been framed as 
 scientific workflows that execute on various compute platforms and platform 
 scales. Scientific workflows are typically described as Directed Acyclic 
 Graphs (DAGs) in which vertices represent tasks and edges represent 
 dependencies between tasks, as defined by application-specific semantics. 
 Workflows can also be composed of loops (e.g., iterative processes) and 
 dynamic behaviors (e.g., if-else).
 
**What a workflow can do?**
 A workflow can analyze terabyte-scale data sets, be composed of million 
 individual tasks, require coordination between heterogeneous tasks, manage 
 tasks that execute for miliseconds to hours, and can process data streams,
 files, and data placed in object stores. The computations can be single core
 workloads, loosely coupled computations (like MapReduce), or tightly coupled
 (like MPI-based parallel programs) all within a single workflow, and can run
 in dispersed computing environments.

**Which workflow system should I use?**
 Identifying the best workflow system to use is key for obtaining experiment
 results with good performance (i.e., turnaround time from experiment 
 definition, to execution, to fetching results). This documentation provides
 some hints on how each supported system could benefit your science use 
 case, and how to design your workflow experiment. 
 
**How can we help?**
 In addition to providing documentation, one of the goals of the OLCF's workflow
 team is to engage with users to 

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
