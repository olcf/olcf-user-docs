
******************
Workflows Overview
******************

The question "what is a workflow system" usually starts a spirited debate. Here, we will be referring to software
or sets of tools used to automate processes and tasks on Slate. In addition to the Slate platform, these processes
and tasks may utilize other NCCS compute and storage systems.

CI/CD Workflows
^^^^^^^^^^^^^^^

Taking the `GitLab CI/CD concepts documentation <https://docs.gitlab.com/ee/ci/index.html>`_ as a start point,
Continuous Integration (CI) completes tasks necessary to test and build software resulting in a container image.
Example tasks performed could be code linting, test coverage, unit testing, functional testing, code compiling
or integration testing. Tasks would be triggered whenever code is pushed into a repository.

CD could be either Continuous Delivery or Continuous Deployment. Both take an application following CI
and make it available for use. In Continuous Delivery, an application deployment is triggered
manually whereas in Continuous Deployment the process occurs automatically without the involvement of a person.

A more in depth discussion may be found with Martin Fowler's
`Continuous Integration <https://martinfowler.com/articles/continuousIntegration.html>`_ article.

On Slate, there are three primary CI/CD style tools in use:

* GitLab Runners
* Jenkins
* OpenShift Pipelines

**GitLab Runners**

Deploying a GitLab Runner into a Slate project may be found in the :ref:`slate_gitlab_runners` document
which leverages a localized `Slate Helm Chart <https://github.com/olcf/slate-helm-charts>`_. The
`GitLab Pipelines <https://docs.gitlab.com/ee/ci/pipelines/>`_ documentation as well as
`GitLab CI/CD Examples <https://docs.gitlab.com/ee/ci/examples/>`_ provide more details on GitLab Runner capabilities
and usage.

**Jenkins**

For Jenkins deployment, a Slate Helm Chart is planned to be released. Documentation concerning
`Jenkins Pipelines <https://www.jenkins.io/doc/book/pipeline/>`_
as well as `Jenkins Pipeline Tutorials <https://www.jenkins.io/doc/tutorials/#pipeline/>`_ are available.

**OpenShift Pipelines**

A more recent offering on Slate, Red Hat OpenShift Pipelines is based on the open source `Tekton <https://tekton.dev/>`_
project and provides a cloud native test, build and deployment framework fully integrated into the OpenShift Console.
For details, see :ref:`slate_openshift_pipelines`. 

GitOps Workflows
^^^^^^^^^^^^^^^^

Unlike the CI/CD tools mentioned above, ArgoCD is not used for testing and creating container images. Rather, ArgoCD
manages Kubernetes application deployments in an automated and consistent manner using custom resource files versioned
in a git repository. Additionally, individual development, test and production deployments across multiple projects
may be accomplished using a singular git repository. Whenever a change occurs in the git repository, ArgoCD will
make the necessary changes to a project by adding, reconfiguring, or removing resources. In other words, the CD in
ArgoCD is for continuous delivery of the application(s).

With GitOps potentially meaning different ideas to different groups, the mission of the Cloud Native Computing
Foundation (CNCF) GitOps Working Group (WG) is to define vendor neutral, principle-led meaning for GitOps practices.
With the KubeCon NA conference in October, 2021, the GitOps WG released a set of four core
`GitOps Principles <https://opengitops.dev/#principles>`_ where the desired state of a GitOps managed system must be:

1. Declarative: A system managed by GitOps must have its desired state expressed declaratively.
2. Versioned and Immutable: Desired state is stored in a way that enforces immutability, versioning and retains a complete version history.
3. Pulled Automatically: Software agents automatically pull the desired declarations from the source.
4. Continuously Reconciled: Software agents continuously observe actual system state and attempt to apply the desired state.

On Slate, Red Hat OpenShift GitOps is based on the open source `ArgoCD <https://argoproj.github.io/cd/>`_ project.
For more information as well as how to install and use ArgoCD on Slate, see: :ref:`slate_openshift_gitops`. 

Scientific Workflows
^^^^^^^^^^^^^^^^^^^^

Scientific workflows at OLCF can be found in the :ref:`workflows` page under the Software section.
