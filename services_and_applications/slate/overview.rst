.. _slate_overview:

********
Overview
********

Overview of what Slate is and how Kubernetes and OpenShift come
together.

What is Slate?
--------------

Built on Kubernetes and OpenShift, *Slate* provides a container orchestration service for running user-managed
persistent application services that do not fit into a batch job. It supports all containerized services with
Kubernetes. The *Slate* service today consists two user facing OpenShift clusters in different security enclaves.

Marble Cluster
==============

Marble is in the Moderate Security Enclave and has access to Frontier and Orion (Lustre). 

Marble is a heterogeneus cluster of 30 nodes with 10 Gigabit ethernet connectivity. Marble
has a node pool of GPU nodes with 3x NVIDIA V100 each, a node pool with Infiniband connectivity
to Frontier and Lustre access, and a node pool of standard compute nodes.

Onyx Cluster
============

Onyx is in the Open Security Enclave and has access to Wolf2 (GPFS).

Onyx is a heterogeneus cluster of 15 nodes with 10 Gigabit ethernet connectivity. Onyx has a
node pool of ppc64le nodes and a node pool of standard compute nodes.


What is Kubernetes?
-------------------
Kubernetes is an open-source system for automating deployment, scaling, and
management of containerized applications. It provides a rich API and workload
primitives that allows users to manage the application deployments of long
running services such as web servers and databases.

`<https://kubernetes.io/>`_


What is OpenShift?
------------------
OpenShift is a Kubernetes Certified Platform. This means that all of the
functionality that is in Kubernetes is also implemented in OpenShift. OpenShift
has extra functionality built on top though, such as the container builder and
integrated registry services.

Simply, OpenShift is a platform as a service (PaaS) offering from Red Hat, provided as a 
supported and trusted distribution of Kubernetes. The API that OpenShift provides
can be accessed via either the Web UI or on the command line via the ``oc`` tool. See the
:ref:`slate_getting_started` guide for more information.

`<https://www.openshift.com/>`_
