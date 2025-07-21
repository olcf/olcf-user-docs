"""
Configuration file for the Sphinx documentation builder.

This file only contains a selection of the most common options. For a full
list see the documentation:
http://www.sphinx-doc.org/en/master/config
"""

# pylint: disable=import-error, invalid-name, redefined-builtin

import datetime as dt
import os
import shutil
from sphinx.writers.html import HTMLTranslator

#

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
copyright = '%s, OLCF' % dt.datetime.now().year
author = 'OLCF'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be

# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx_design', 'sphinx_copybutton']

copybutton_prompt_text = r">>> |\.\.\. |\$ "
copybutton_prompt_is_regexp = True
copybutton_line_continuation_character = "\\"

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# To avoid errors with older versions of Sphinx and Sphinx RTD theme, explicitly
# specify the master document.
master_doc = 'index'


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# The "title" is used in the HTML <title> tag of individual pages.
html_title = 'OLCF User Documentation'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_css_files = [
    'css/theme_overrides.css',
]

html_js_files = [
    'js/custom.js',
]

html_logo = 'images/olcf_logo.png'

html_favicon = 'images/favicon.ico'

html_context = {
    'vcs_pageview_mode': 'edit',
    'display_github': True,
    'github_user': 'olcf', # Username
    'github_repo': 'olcf-user-docs', # Repo name
    'github_version': 'master', # Version
    'conf_py_path': '/', # Path in the checkout to the docs root
}

# see https://sphinx-rtd-theme.readthedocs.io/en/stable/configuring.html
html_theme_options = {
    'canonical_url': 'https://docs.olcf.ornl.gov',
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'style_external_links': True,
    'style_nav_header_background': '#efefef',
    'logo_only': True,
}


# pylint: disable=too-few-public-methods
class PatchedHTMLTranslator(HTMLTranslator):
    '''HTMLTranslator patched to open external links in new tabs.

    Taken from: 'http://jack.rosenth.al/hacking-docutils.html#sphinx-hacks'
    '''
    def visit_reference(self, node):
        '''Sets link target to '_blank' (new page tab) if link node is
        external to the site.
        '''
        if (node.get('newtab')
                or not (node.get('target')
                        or node.get('internal')
                        or 'refuri' not in node)):
            node['target'] = '_blank'
        super().visit_reference(node)

def copy_sw_file(app, exception):
    src = '/tmp/software_list_group.json'
    dest = os.path.join(app.builder.outdir, 'software/software_list/', 'software_list_group.json')

    if os.path.exists(src):
        shutil.copy(src, dest)

def setup(app):
    '''Function to setup sphinx customizations.'''
    app.set_translator('html', PatchedHTMLTranslator)
    # Add DataTables JavaScript
    app.add_js_file('https://cdn.datatables.net/2.2.1/js/dataTables.js')
    app.add_js_file('https://code.jquery.com/jquery-3.7.1.js')
    # Add DataTables CSS
    app.add_css_file('https://cdn.datatables.net/2.2.1/css/dataTables.dataTables.css')
    # copy software list json after sphinx build completed
    app.connect('build-finished', copy_sw_file)


# globally-available substitutions

rst_prolog = r"""
.. |R| replace:: \ :sup:`®`
"""
