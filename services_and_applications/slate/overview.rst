.. _slate_overview:

**************
Slate Overview
**************

Overview of what Slate is and how Docker, Kubernetes, and OpenShift come
together.

What is Slate?
--------------

*Slate* provides container orchestration services that support a user project's
existing Summit and Alpine allocations. The Slate service today consists two
user facing OpenShift clusters which each provide capabilities unique to the
security enclave that they are in.

| **There is one OpenShift cluster in each OLCF 
  enclave, Open and Moderate, listed below:**.
| - **Marble** (Moderate Enclave)
| - **Onyx** (Open Enclave)

Moderate is the enclave in which Summit (:ref:`summit-user-guide`) is
accessible.  Open is the enclave in which :ref:`ascent-user-guide` is
accessible.

What is Docker?
---------------
Docker is a container runtime and is used by Kubernetes to actually run the
containers on a node.

What is Kubernetes?
-------------------
Kubernetes is an open-source system for automating deployment, scaling, and
management of containerized applications. It provides a rich API and workload
primitives that allows users to manage the application deployments of long
running services such as web servers and databases.

What is OpenShift?
------------------
OpenShift is a Kubernetes Certified Platform. This means that all of the
functionality that is in Kubernetes is also implemented in OpenShift. OpenShift
has extra functionality built on top though, such as the container builder and
integrated registry services.

Simply, OpenShift is a platform as a service (PaaS) offering from Red Hat that
brings together Docker and Kubernetes, providing an API to manage container
services.
