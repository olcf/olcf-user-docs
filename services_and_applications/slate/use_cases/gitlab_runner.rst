.. _slate_gitlab_runners:

**************
GitLab Runners
**************

GitLab CI/CD jobs may be accomplished using the GitLab Runner application. An open-source application written in Go, a GitLab Runner
may be installed with a variety of executors. This documentation focuses on the installation and configuration for use of the
GitLab Runner Kubernetes Executor on Slate.

References
^^^^^^^^^^

* `<https://docs.gitlab.com/runner/>`_
* `<https://docs.gitlab.com/runner/executors/kubernetes.html>`_
* `<https://docs.gitlab.com/runner/install/kubernetes.html>`_

Registration Token
^^^^^^^^^^^^^^^^^^

Prior to installation of the GitLab Runner, a registration token for the runner is needed from the GitLab server. This token will
allow a GitLab runner to register to the server in the needed location for running CI/CD jobs. Runners themselves may be registered
to either a group as a shared runner or a project as a repository specific runner.

If the runner is to be a group shared runner:

#. Navigate to the group in GitLab and then go to Settings -> CI/CD. 
#. Expand the Runners section of the CI/CD Settings panel, and ensure that the "Enable shared runners for this group" toggle is enabled. 
#. The registration token should also be available for retrieval from "Group Runners" area.

If the runner is to be registered to a specific project:

#. Ensure that the project is enabled for pipelines by navigating to the project in GitLab. 
#. In the Settings for the project, select General. 
#. Expand the "Visibility, project features, and permissions" section and locate the "Pipelines" option. If it is currently disabled, enable the "Pipelines" option and then "Save Changes".
#. Once saved, refresh the project General Settings page, and locate the newly available "CI/CD Settings" option. 
#. Select "CI/CD", and expand the "Runners" section of the CI/CD settings. 
#. In the "Specific Runners" area, the registration token should be available for retrieval.

Installation and Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Upon login to the web UI for Marble or Onyx, you will be on a projects page. In the navigation bar in the upper left corner, you should see
either the "Developer" or "Administrator" perspective indicated. These two perspectives present two different ways of viewing resources
deployed to the cluster. The Developer Perspective focuses on a Topology overview for the resources and will be used for the deployment
of a GitLab Runner.

To deploy a GitLab Runner from the Developer Perspective, navigate to "Topology" -> "Helm Chart" and select
"GitLab Runner vX.X.X Provided by Slate Helm Charts". From the new window, select "Install Helm Chart".

On the resulting screen, one can customize the installation of the GitLab Runner helm chart. The chart has been forked from upstream to
allow for customized deployment to Slate. From the Form View, expand the "GitLab Runner" fields. Using the registration token retrieved
in the prior section, enter the token for adding the runner to the GitLab server in the empty field.

.. note::

   If the Registration Token is left blank, the runner installation will not succeed.

If the GitLab Runner needs to be able to use batch scheduler command, toggle the "Enable Batch Scheduler" option to "true". Then, select the
necessary filesystem annotation to use for the cluster the chart is being deployed. For Marble, the "olcf" annotation would be used whereas
whereas for Onyx the "ccsopen" annotation would be used.

The Resources requests and limits are setup to match the namespace default limits. If more resources are anticipated for the deployment,
modify the requests and limits as needed.

This helm chart was forked from the the upstream GitLab Runner helm chart. As such, nearly all of the parameters documented in the
upstream chart could be provided here as well.

To verify that the GitLab runner was properly deployed, one could explore the deployed resources from the Topology view from the
Slate web console, or from the command line by using the following:

.. code-block:: bash

   $ helm ls
   NAME         	NAMESPACE    	REVISION	UPDATED                               	STATUS  	CHART              	APP VERSION
   gitlab-runner	myproject   	1       	2021-09-15 14:10:15.12187869 +0000 UTC	deployed	gitlab-runner-1.0.0	14.2.0
   $ oc get pods
   NAME                                          READY   STATUS    RESTARTS   AGE
   gitlab-runner-gitlab-runner-687486d94-lpmhs   1/1     Running   0          107s

Once the pod has a Status of "Running", navigate to the GitLab web interface and ensure that the runner has registered to either the group or repository per the token given, and that it is listed as available.

Finally, if batch scheduler integration was enabled, one can verify functionality in the pod with:

.. code-block:: bash

   $ oc exec -it pods/gitlab-runner-gitlab-runner-687486d94-lpmhs -- bash
   bash-5.0$ squeue
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
              9951 ...

Removing a GitLab Runner
^^^^^^^^^^^^^^^^^^^^^^^^

To remove a namespace installed GitLab runner, login to the web UI for the cluster and switch to the "Developer" perspective as before. In the 
navigation panel on the left select "Helm". The deployment should be displayed as one of the "Helm Releases". Click on the vertical 
ellipses located at the right side of the deployment, and select "Uninstall Helm Release". A confirmation dialog box will be displayed.
Type the information as requested and click "Uninstall".

.. note::

   When clicking the uninstall, it may appear that the UI hangs and nothing is happening. It may take some time to remove all of the resources.

Once the installation is complete, the UI will refresh and the deployment will no longer be listed.

Verify that the runner has been unregistered from the GitLab project (GitLab->Settings->CI/CD->Runners). One could also check
to ensure that all the pods were deleted by changing over to the "Administrator" perspective and selecting Workloads -> Pods from the navigation.
