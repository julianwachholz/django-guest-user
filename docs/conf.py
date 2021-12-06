# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

import importlib
import inspect

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

import django
import pkg_resources

sys.path.insert(0, os.path.abspath(".."))


# -- Project information -----------------------------------------------------

project = "django-guest-user"
copyright = "2021, Julian Wachholz"
author = "Julian Wachholz"

# The full version, including alpha/beta/rc tags
release = pkg_resources.get_distribution("django-guest-user").version

if os.getenv("READTHEDOCS_VERSION") == "latest":
    release = "main"

# -- General configuration ---------------------------------------------------

# Setup django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_proj.settings")
django.setup()

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.linkcode",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
]

autodoc_member_order = "bysource"
add_module_names = False

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "django": (
        "https://docs.djangoproject.com/en/3.2/",
        "http://docs.djangoproject.com/en/3.2/_objects/",
    ),
}
intersphinx_disabled_domains = ["std"]

# Repository URL, used with `linkcode_resolve`
repository = "https://github.com/julianwachholz/django-guest-user"


def linkcode_resolve(domain, info):
    if domain != "py":
        return None
    module = info["module"]
    if not module:
        return None

    mod = importlib.import_module(module)
    attrs = info["fullname"].split(".")
    obj = inspect.getattr_static(mod, attrs[0])

    if len(attrs) > 1:
        attr = inspect.getattr_static(obj, attrs[1])
        obj = attr

    try:
        definition_line = inspect.getsourcelines(obj)[1]
        filename = module.replace(".", "/")
        return f"{repository}/blob/{release}/{filename}.py#L{definition_line}"
    except TypeError:
        return None


# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
