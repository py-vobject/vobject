# -*- coding: utf-8 -*-
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import datetime

import vobject

project = "Python vObject"
copyright = f"© {datetime.datetime.now().year}, David Arnold"
author = "David Arnold"
release = vobject.VERSION

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"

html_theme_options = {
    "github_user": "py-vobject",
    "github_repo": "vobject",
    "github_type": "star",
    "github_button": "true",
    "github_count": "true",
}

html_static_path = ["_static"]
