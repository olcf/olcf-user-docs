.. _workflows:

#########
Workflows
#########

Workflows are cornerstones of modern scientific computing, and 
are used widely across scientific domains. Workflow systems provide 
**abstraction** and **automation** for describing complex computational 
applications that require efficient and robust management of large volumes of 
data on high-performance compute resources.

At OLCF, we offer users with a selection of cutting-edge 
workflow systems that are *easy-to-use* while providing a comprehensive set 
of features for supporting a large range of use-cases from science
domains.

**What is a Workflow?**
 Many computationally intensive scientific applications have been framed as 
 workflows that execute on compute platforms at platform 
 scales. Scientific workflows are typically described as Directed Acyclic 
 Graphs (DAGs) in which vertices represent tasks and edges represent 
 dependencies between tasks, as defined by application-specific semantics. 
 Workflows can also be composed of dynamic behaviors (e.g., loops, 
 conditionals, etc.).
 
**What a workflow can do?**
 A workflow can automate analysis of terabyte-scale data sets, be composed of millions of 
 individual tasks, require coordination between tasks, manage 
 tasks that execute for miliseconds to hours, and can process data streams,
 files, and data placed in object stores. The computations can be single core
 workloads, loosely coupled computations (like MapReduce), or tightly coupled
 (like MPI-based parallel programs).

**Which workflow system should I use?**
 Identifying the best workflow system to use is key for obtaining experiment
 results with good performance (i.e., turnaround time from experiment 
 definition, to execution, to fetching results). The present documentation provides
 some information on how each supported system could benefit your use-case, and how to design your workflow. 
 
**How can we help?**
 In addition to providing documentation, one of the goals of the OLCF's 
 workflows team is to engage with users to guide them on describing their 
 workflow applications which may include (i) understanding the use-case, (ii) identifying the need for workflows, (iii) determining the most 
 suited workflow system as well as OLCF resource, and (iv) helping designing and executing 
 the workflow on OLCF resources.

.. note:: 
    To learn the basics about workflows and distributed 
    computing, see this set of 
    `pedagogic modules <https://eduwrench.org/pedagogic_modules/workflows/>`_
    that will introduce you to the workflow model of computation that is 
    used in many scientific applications.

***********************************
Running Workflows on OLCF Resources
***********************************

Due to the increasing need to support workflows, dedicated workflow systems 
were developed to provide abstractions for creating, executing, and adapting 
workflows conveniently and efficiently while ensuring portability. While 
these efforts are all worthwhile individually, there are now hundreds of 
independent workflow systems. At OLCF, we are constantly evaluating and 
refining the selection of workflow systems made available to users. Below,
you will find a list of current frameworks natively supported in our 
:ref:`Systems<system-user-guides>`:

+------------------------------------------------+-------------+
| Workflow System                                | OLCF System |
+================================================+=============+
| :ref:`Ensemble Toolkit (EnTK)<workflows-entk>` | Frontier    |
+------------------------------------------------+-------------+
| :ref:`Parsl<workflows-parsl>`                  | Frontier    |
+------------------------------------------------+-------------+
| :ref:`Swift/T<workflows-swiftt>`               | Frontier    |
+------------------------------------------------+-------------+

---------

****************
Workflow Systems
****************

.. toctree::
   :maxdepth: 1
   
   entk
   parsl
   swift_t

.. note:: 
    Only one workflow module may be loaded at a time as they are based on conda
    environments. The modules will unload any other python related modules.
    They are based on the miniforge3 module.


