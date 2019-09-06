###########################
Contributing to these docs
###########################


Authoring content
==================

Setup authoring environment
----------------------------

#. Install Sphinx and the ReadTheDocs theme locally::

        $ pip3 install sphinx sphinx_rtd_theme

   This can be in your home area, a virtual environment, container, etc.


#. Fork the documentation repository on GitHub

    Go to https://github.com/olcf/olcf-user-documentation, and click the "Fork"
    button in the upper right corner

    FIXME: add a screenshot with arrow

#. Clone your fork of the documentation repository::

    $ git clone https://github.com/<your-github-id>/olcf-user-documentation.git

#. Point your master branch to track upstream::

    $ git remote add olcf https://github.com/olcf/olcf-user-documentation.git
    $ git fetch olcf
    $ git branch --set-upstream-to=olcf/master

#. Build the docs::

    $ cd olcf-user-documentation && sphinx-build -E . _build

#. Locally preview the generated web pages
   start a webserver on something like ``localhost:8080`` that points at
   your ``olcf-user-documentation/_build`` directory. For example, using busybox::

        $ busybox httpd -p 127.0.0.1:8080 -h /home/ubuntu/olcf-user-docs/_build

   or a python webserver (from inside the document root)::

        $ python3 -m http.server 8080

Edit the docs
-------------------------

#. Setup your environment as above
#. Make your edits in a new git branch::

      $ git checkout -b my-edits-branch
      (edit some files, commit them to your branch)

#. Preview your edits
#. Push your edits to your GitHub fork::

      $ git push -u origin my-edits-branch

#. Open a pull request on github

   FIXME: add screenshots showing how

Resources
---------------

| `Sphinx Quickstart <http://www.sphinx-doc.org/en/master/usage/quickstart.html>`_
| `restructuredText Primer <http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_
| `restructuredText Reference <http://docutils.sourceforge.net/rst.html>`_

Submit suggestions
====================================

Under construction - Use GitHub Issues
