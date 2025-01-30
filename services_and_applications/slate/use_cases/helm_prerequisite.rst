.. _helm_prerequisite:

******************
Helm Prerequisites
******************
 
The following items need to be established before deploying applications on
Slate systems (Marble or Onyx OpenShift clusters).

Establish a project/namespace on Onyx or Marble
-----------------------------------------------

Follow :ref:`slate_getting_started` if you do not already have a
project/namespace established on Onyx or Marble.

Install Helm
------------

It is recommended to use Helm version 3. 

Helm enables application deployment via `Helm Charts
<https://helm.sh/docs/topics/charts/>`_. The high level `Helm Architecture
<https://helm.sh/docs/topics/architecture/>`_ docs are also a great reference
for understanding Helm.

Like ``oc``, Helm is a single binary executable. 

 - This can be installed on macOS with `Homebrew <https://brew.sh/>`_ : 
 
 .. code-block:: bash 

     $ brew install helm

 - Or can be pulled from the `Helm Release Page
   <https://github.com/helm/helm/releases>`_. If downloading from the GitHub
   release page, you can copy this executable into ``/usr/local/bin`` to add it to
   ``$PATH``.

.. note::
  One nice feature of Helm is that it uses the underlying
  authentication credentials used with ``oc``, so once you login with ``oc login``,
  the helm client will authenticate automatically.

Once ``oc`` and ``helm`` are setup and you are logged in with ``oc login``, test Helm:

.. code-block:: bash

    $ helm ls
