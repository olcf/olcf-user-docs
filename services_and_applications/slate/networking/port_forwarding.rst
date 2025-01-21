
-------------------------------
Quick Access from Outside Slate
-------------------------------

Access to the Web UI and CLI
----------------------------

Both the web UI and the API endpoint for the ``oc`` client are exposed outside of ORNL. However, you must log in with ``NCCS USERNAME AND PASSWORD`` rather than NCCS Single Sign On on the Web UI.

Access to Internal Resources
----------------------------

For production workloads, it is recommended to learn about :ref:`services <slate_services>` and :ref:`routes <slate_routes>` in order to gain access to your internal resources.

However, for testing and development, ``oc port-forward`` can be a powerful tool for quick access to internal cluster resources.

This tool will forward a local port on your system to a pod inside the cluster.

For example, if you have an nginx deployment running on port 8080 inside the container, you can view this nginx instance locally by running:

.. code-block::
   
   oc port-forward ${pod_name} 7777:8080

The first port is the local port you want forwarded, and the second port is the port exposed by the pod. After running this command, you can go into your browser (or use ``curl`` in a second terminal) and connect to ``http://localhost:7777``.

Additionally, ``oc port-forward`` doesn't have to be given a pod name. This tool is aware of services and deployments as well. If you had a service called ``nginx-svc`` and a deployment called ``nginx``\ , for example, the following commands would achieve the same result:

.. code-block::

   oc port-forward deployment/nginx 7777:8080
   oc port-forward svc/nginx-svc 7777:8080

You will be forwarded to any of the pods matched by the service or deployment.

Furthermore, this doesn't only work for HTTP traffic. You could also access other exposed services such as databases.

For instance, if you have a mongoDB instance running on port 27017 with a deployment named ``mongodb``\ , you could run ``oc port-forward deployment/mongodb 7777:27017``. Now you can simply run ``mongo --port 7777`` (assuming you have the ``mongo`` client installed on your local machine) and have access to your mongodb instance in the cluster, as if it were running on your local machine.
