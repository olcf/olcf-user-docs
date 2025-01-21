

*****************************
Deploy NGINX with Hello World
*****************************

One of the simplest use cases for Kubernetes is running a web server. We will walk through the
steps needed to set up an NGINX web server on OpenShift that serves a static html file. This
example assumes that you have an allocation on the cluster.

First, make sure that you are in the correct project:

.. code-block:: text

   oc project <YOUR_PROJECT>

In the next part of this we will be creating a few objects needed to run NGINX. The objects will be
saved into a file and then added to the cluster with the command:

.. code-block:: text

   oc create -f <FILENAME>

The first object we wish to create is our BuildConfig. This is the object that defines how we build
our NGINX image.

Before we create the BuildConfig, we should give it a way to access two files before they are
pulled into the build pod. The files are my ``index.html`` and my ``nginx.conf`` file. You can get them
into your build pod however you wish, for simplicity I chose to add them to a public git repository
and wget them. The ``index.html`` and ``nginx.conf`` file are defined respectively as:

.. code-block:: html

   <h1>Hello, World!</h1>

.. code-block:: nginx

   user nginx;
   worker_processes auto;
   error_log /tmp/error.log;
   pid /tmp/nginx.pid;

   # Load dynamic modules. See /usr/share/nginx/README.dynamic.
   include /usr/share/nginx/modules/*.conf;

   events {
       worker_connections 1024;
   }

   http {
       log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                         '$status $body_bytes_sent "$http_referer" '
                         '"$http_user_agent" "$http_x_forwarded_for"';

       access_log  /tmp/access.log  main;

       client_body_temp_path /tmp/nginx 1 2;
       proxy_temp_path /tmp/nginx-proxy;
       fastcgi_temp_path /tmp/nginx-fastcgi;
       uwsgi_temp_path /tmp/nginx-uwsgi;
       scgi_temp_path /tmp/nginx-scgi;

       sendfile            on;
       tcp_nopush          on;
       tcp_nodelay         on;
       keepalive_timeout   65;
       types_hash_max_size 2048;

       include             /etc/nginx/mime.types;
       default_type        application/octet-stream;

       # Load modular configuration files from the /etc/nginx/conf.d directory.
       # See http://nginx.org/en/docs/ngx_core_module.html#include
       # for more information.
       include /etc/nginx/conf.d/*.conf;

       server {
           listen       8080 default_server;
           listen       [::]:8080 default_server;
           server_name  _;
           root         /usr/share/nginx/html;

           # Load configuration files for the default server block.
           include /etc/nginx/default.d/*.conf;

           location / {
           }

           error_page 404 /404.html;
               location = /40x.html {
           }

           error_page 500 502 503 504 /50x.html;
               location = /50x.html {
           }
       }
   }

.. note::
  The NGINX configuration file is completely standard except I changed the listen port to be
  from 80 to 8080 since the server will be running as a non-root user. The Route, that we will add
  later on, will redirect traffic coming in on port 80 to our server running on port 8080.

The BuildConfig, the following should be placed inside a ``buildconfig.yaml`` file:

.. code-block:: yaml

   apiVersion: build.openshift.io/v1
   kind: BuildConfig
   metadata:
       name: nginx-hello-world
   spec:
     runPolicy: Serial
     source:
       dockerfile: |
         FROM rockylinux:latest
         RUN yum install -y epel-release && \
             yum install -y nginx

         COPY index.html /usr/share/nginx/html
         COPY nginx.conf /etc/nginx/nginx.conf

         CMD /usr/sbin/nginx -g 'daemon off;'

     strategy:
       type: Docker
       dockerStrategy:
         noCache: false
     output:
       to:
         kind: ImageStreamTag
         name: "nginx-hello-world:latest"

We create the BuildConfig object with:

.. code-block:: text

   oc create -f buildconfig.yaml

We now need to create an ImageStream with the same name as our build. This will create a place for
our BuildConfig to push the image to, and our Deployment to pull the image from during a deployment.

.. code-block:: text

   oc create imagestream nginx-hello-world

We can now start a build to get our NGINX image:

.. code-block:: text

   oc start-build nginx-hello-world --from-dir=./ --follow

This should spin up a build pod that produces a nginx-hello-world image while also tailing the
logs. Once the build completes, then we should have an image pushed to our ImageStream:

.. code-block:: text

   oc get imagestream nginx-hello-world
   NAME                DOCKER REPO                                                         TAGS      UPDATED
   nginx-hello-world   image-registry.openshift-image-registry.svc:5000/YOUR_NAMESPACE/nginx-hello-world   latest    3 minutes ago

If all goes well it is time to create the Deployment. The following should be placed inside a ``deployment.yaml`` file:

.. code-block:: yaml

   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: nginx-hello-world
     labels:
       app: nginx-hello-world
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: nginx-hello-world
     template:
       metadata:
         labels:
           app: nginx-hello-world
       spec:
         containers:
           - name: nginx
             image: "image-registry.openshift-image-registry:5000/YOUR_NAMESPACE/nginx-hello-world"
             terminationMessagePath: /dev/termination-log
             terminationMessagePolicy: File
             tty: true
             stdin: true
             serviceAccount: default
         terminationGracePeriodSeconds: 5

.. note::
  In the Deployment make sure to change the YOUR_NAMESPACE string.

Create the Deployment object:

.. code-block:: text

   oc create -f deployment.yaml

View the deployment:

.. code-block:: text

   oc get deployment nginx-hello-world
   NAME                DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
   nginx-hello-world   3         3         3            3           9s

.. note::
  You should see Desired: 3 and Current: 3

After the deployment has been created, it will spin up a pod running NGINX, but we need to get
traffic from outside the cluster to the pod so that we can display the hello world.

The Service object will create a Cluster IP address that will direct traffic to any pod in our
deployment that is considered by the cluster to be ready. The following should be placed inside a ``service.yaml`` file:

.. code-block:: yaml

   apiVersion: v1
   kind: Service
   metadata:
     labels:
       app: nginx-hello-world
     name: nginx-hello-world
   spec:
     ports:
     - name: nginx
       port: 80
       protocol: TCP
       targetPort: 8080
     selector:
       app: nginx-hello-world
     sessionAffinity: None
     type: ClusterIP

Create the Service object:

.. code-block:: text

   oc create -f service.yaml

The Route object will set up the cluster load balancers to accept traffic for a specified hostname
and direct the traffic to the service, which will, in turn, direct the traffic to any pod into our
deployment that is considered by the cluster to be ready.

If you do not set a hostname on the route, one will be automatically chosen. We will use this
mechanism for this demo but you can choose any hostname as long as it ends with
``apps.CLUSTER.ccs.ornl.gov``, where CLUSTER is one marble or onyx.

The following should be placed inside a ``route.yaml`` file:

.. code-block:: yaml

   apiVersion: route.openshift.io/v1
   kind: Route
   metadata:
     name: nginx-hello-world
   spec:
     # hostname: foo.apps.CLUSTER.ccs.ornl.gov
     port:
       targetPort: nginx
     tls:
       insecureEdgeTerminationPolicy: Redirect
       termination: edge
     to:
       kind: Service
       name: nginx-hello-world
       weight: 100
     wildcardPolicy: None

Create the Route object:

.. code-block:: text

   oc create -f route.yaml

We need to get the route so that we can see the generated hostname.

.. code-block:: text

   oc get route nginx-hello-world
   NAME                HOST/PORT                                             PATH      SERVICES            PORT      TERMINATION     WILDCARD
   nginx-hello-world   nginx-hello-world-test.apps.granite.ccs.ornl.gov                nginx-hello-world   nginx     edge/Redirect   None

Now if you access the hostname that you set up with the route from a browser, you should see the
text "Hello World".

Once you are finished, you can remove the resources that were created for this demo:

.. code-block:: text

   oc delete buildconfig nginx-hello-world
   oc delete imagestream nginx-hello-world
   oc delete deployment nginx-hello-world
   oc delete service nginx-hello-world
   oc delete route nginx-hello-world
