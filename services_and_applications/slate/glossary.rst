.. _slate_glossary:

########
Glossary
########

This is a glossary of terms that will become second nature to you after you have been using Openshift for a time. Before then, however, keeping them all straight can be confusing. This is not an extensive list of all things related to Openshift but instead a list that can be referenced when reading other documentation or googleing a question.

**Cluster and Slate:** A cluster is one of the Kubernetes cluster (Marble or Onyx) that the Platform team in the HPC Data and Operations group supports. Slate is the overarching term for all Openshift resources managed by the Platform team.

**Container:** A container is a set of linux namespaces and cgroups which isolate a running process from other containers and the rest of the OS.

**Deployment:** An object that represents multiple, identical Pods. A Deployment is an ``Owner`` of a Pod and likewise if the Deployment is deleted so too are the Pods that it owns.

**Host/Node:** The machine or VM that is a member of the Kubernetes cluster. A Node is where Kubernetes objects execute.

**Images:** A ready to run package of software. This will contain the necessary components needed to run some specific task or application.

**Namespace:** A way to divide cluster resources among multiple projects. Contain a subsection of authorization and policy from the cluster i.e. someone in another project cannot delete your Pods. A namespace gets its resource allocation from an overarching RATS project. This means that a RATS project can have a 1:1 mapping with a namespace or a 1:many mapping with multiple namespaces. All of the namespaces under a RATS project will take away from the quota of the overarching RATS project and all quota is managed in RATS. This is all simplified by the Quota Dashboard.

**NodePort:** A type of Service that reserves a port across all nodes in a cluster and forwards pod traffic to that port.

**Object:** Object is *something* in a Kubernetes Cluster. This something can be a Pod, Route, Deployment, Stateful Set or any one of the other things you define in YAML and create in the cluster. Objects are added to the cluster through the Kubernetes API. You will almost certainly only ever interact with the Kubernetes API through the ``oc`` client or through the web GUI at: ``https://console-openshift-console.apps.<CLUSTER_NAME>.ccs.ornl.go``

**Persistent Volume Claim (PVC):** A request for a volume. A pod could be thought of as a request for compute resources and a Persistent Volume Claim can be thought of as a request for storage.

**Pod:** A Pod is a group of containers with shared networking and storage. These containers will be co-located and co-scheduled and run in a shared context. You can think of a Pod as a “logical host” - it contains one or more application containers which are relatively tightly coupled — in a pre-container world, being executed on the same physical or virtual machine would mean being executed on the same logical host.

**Quota Dashboard:** A web application that allows you to create Kubernetes namespaces from a OLCF project allocation. This can be useful for creating separate development and production namespaces. The Quota Dashboard can be found at ``https://quota.<CLUSTER_NAME>.ccs.ornl.gov`` where `<CLUSTER_NAME>` is either ``marble`` or ``onyx``.

**Role:**  A namespaced grouping of Policy Rules that can be referenced by a Rolebinding

**RoleBinding:** An object that associates a user with a role

**Route:** An object that allows exposing services over HTTPS.

**Service:** An object that allows exposing Pod(s) as a network service.

**Stateful Set:** An object that manages the deployment and scaling of Pods while also providing guarentees about the ordering and uniqueness of the Pods.

**Volume:** External storage to a Pod that is mounted into a Pod and accessible by all containers in the Pod. Data stored here will persist Pod restarts where as data on the Pod will be lost in a Pod restart. Assuming there are enough resources, a Volume is created when a PVC is created.
