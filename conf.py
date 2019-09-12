# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'OLCF User Documentation'
copyright = '2019, OLCF'
author = 'OLCF'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
#html_logo = 'images/OLCF_official_white_10_26_15.png'
html_favicon = 'images/favicon.png'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_context = {
  'css_files': [
      '_static/theme_overrides.css',  # override wide tables in RTD theme
  ],
}

# see https://sphinx-rtd-theme.readthedocs.io/en/stable/configuring.html
html_theme_options = {
  'canonical_url': 'https://docs.olcf.ornl.gov',
  'collapse_navigation': False,
  'sticky_navigation': True,
  'navigation_depth': 4,
  'style_external_links': True,
}

# for opening external links in new tabs (from
# http://jack.rosenth.al/hacking-docutils.html#sphinx-hacks

from sphinx.writers.html import HTMLTranslator
class PatchedHTMLTranslator(HTMLTranslator):
    def visit_reference(self, node):
        if node.get('newtab') or not (node.get('target') or node.get('internal') or 'refuri' not in node):
            node['target'] = '_blank'
        super().visit_reference(node)

def setup(app):
    app.set_translator('html', PatchedHTMLTranslator)

# globally-available substitutions

rst_prolog = """
.. |R| replace:: \ :sup:`®`
"""

