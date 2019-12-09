###########################
Contributing to these docs
###########################

Submitting suggestions
====================================

Have a suggestion for improvement? Share it with us by `opening an issue
<https://github.com/olcf/olcf-user-docs/issues/new>`_.


Authoring content
==================

Setup authoring environment
----------------------------

#. Install Sphinx and the ReadTheDocs theme locally::

        $ pip3 install sphinx sphinx_rtd_theme

   This can be in your home area, a virtual environment, container, etc.


#. Fork the documentation repository on GitHub

    Go to https://github.com/olcf/olcf-user-docs, and click the "Fork"
    button in the upper right corner.

    .. image:: /images/github_fork.png
       :width: 80.0%
       :align: center


#. Clone your fork of the documentation repository::

    $ git clone https://github.com/<your-github-id>/olcf-user-docs.git

#. Point your master branch to track upstream::

    $ git remote add olcf https://github.com/olcf/olcf-user-docs.git
    $ git fetch olcf
    $ git branch --set-upstream-to=olcf/master

#. Build the docs::

    $ cd olcf-user-docs && sphinx-build -E . _build

#. Locally preview the generated web pages
   start a webserver on something like ``localhost:8080`` that points at
   your ``olcf-user-docs/_build`` directory. For example, using busybox::

        $ busybox httpd -p 127.0.0.1:8080 -h /home/ubuntu/olcf-user-docs/_build

   or a python webserver (from inside the document root)::

        $ python3 -m http.server 8080

Edit the docs
-------------------------

After having set up your environment as described above, you can reuse your
local environment to make multiple changes.

#. Update your local clone from the upstream repository::

      $ git checkout master
      $ git pull

#. Make your edits in a new git branch::

      $ git checkout -b my-edits-branch
      (edit some files, commit them to your branch)

#. Preview your edits
#. Push your edits to your GitHub fork::

      $ git push -u origin my-edits-branch

#. Open a pull request on github

    After you push your branch, you should see a button to open a pull request.

    .. image:: /images/github_pr.png
       :width: 80.0%
       :align: center

Resources
---------------

| `Sphinx Quickstart <http://www.sphinx-doc.org/en/master/usage/quickstart.html>`_
| `restructuredText Primer <http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_
| `restructuredText Reference <http://docutils.sourceforge.net/rst.html>`_

GitHub Guidelines
===================

Here are some guidelines and common practices that we use in this project.

- When you want to work on an issue, assign it to yourself if no one is assigned
  yet. If there is somebody assigned, check in with that person about
  collaborating.
- Reference the issue(s) that your PR addresses with GitHub's '#' notation.
- Use "WIP" in your PR title to indicate that it should not be merged yet.
  Remove just the WIP when you are ready for it to be merged.
- If you think certain individuals should be aware of your proposed changes,
  suggest them as reviewers on the PR.
- You do not need to assign labels to your PR, but you may do so if you have
  suggestions. However, be aware that the labels might get changed.
- If an issue or PR requires discussion with the OLCF's User Support Group,
  use the GitHub Team tag ``@olcf/ua-support``.
