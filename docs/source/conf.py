import os
import pathlib
import sys 

from sphinx.ext.autodoc import between

sys.path.append(
    os.path.join(pathlib.Path(__file__).parents[2].as_posix(),"src")
    )

print(os.path.join(pathlib.Path(__file__).parents[2].as_posix(),"src")
   )





def insert_variable_values(app, what, name, obj, options, lines):
    """
    Custom Sphinx hook to insert the actual value of variables into the documentation.
    """
    #print(what,app,name)
    if what == "data":  # 'data' refers to module-level variables
        value = repr(obj)  # Get the string representation of the variable value
        lines.append(f"**Value:** ``{value}``")

def setup(app):
    app.connect('autodoc-process-docstring', insert_variable_values)


# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Instrumentum sanae Doctrinae docs'
copyright = '2024, AGBALENYO Komi Barthélémy Elvis'
author = 'AGBALENYO Komi Barthélémy Elvis'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
   'sphinx.ext.autosummary',
   'sphinx.ext.intersphinx',
   'myst_parser'
]

templates_path = ['_templates']
exclude_patterns = []


source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

autodoc_default_options = {
    'members': True,
    'special-members': '__init__',
    'undoc-members': True,
}
