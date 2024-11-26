# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "DESimpy"
copyright = "2024, Galen Seilis"
author = "Galen Seilis"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_material"
html_title = project
html_theme_options = {
    "color_primary": "green",
    "color_accent": "light-green",
    "repo_url": "https://github.com/galenseilis/DESimpy/",
    "repo_name": project,
}
html_static_path = ["_static"]
