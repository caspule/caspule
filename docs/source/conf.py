# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys
import pathlib

# Add the project root (where your six Python scripts live) to sys.path:
sys.path.insert(0, os.path.abspath('../..'))
ROOT = pathlib.Path(__file__).resolve().parents[2]   # adjust if needed
sys.path.insert(0, str(ROOT))


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'generate_InitCond'
copyright = '2025, Aniruddha Chattaraj, David Kanovich'
author = 'Aniruddha Chattaraj, David Kanovich'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",      # ← add this line
    "sphinx.ext.napoleon",        # (optional, but nice for NumPy/Google style)
    "sphinx.ext.viewcode",        # (optional)
]

autosummary_generate = True

myst_enable_extensions = [
    "colon_fence",  # lets you use ::: fenced code blocks
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_sidebars = {
    '**': [
        'globaltoc.html',   # show the full toctree from index.rst
        'relations.html',   # “Previous / Next” links
        'sourcelink.html',  # “View page source” link
        'searchbox.html',   # Search field
    ]
}

html_logo = f"_static/img/Logo.png" 
html_favicon = f"_static/img/Icon.png"
html_theme_options = {
    "logo_only": True,                 # show only the logo, not project name text
    "display_version": False           # hide the version string
}
# --
