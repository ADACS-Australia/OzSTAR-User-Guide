# Configuration file for the Sphinx documentation builder.

# -- Project information -----------------------------------------------------

project = "OzSTAR User Guide"
copyright = "ADACS"
author = "ADACS"

# -- General configuration ---------------------------------------------------

extensions = [
    "myst_parser",
    "sphinx_copybutton",
    "sphinx_design",
]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

root_doc = "index"
language = "en"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
smartquotes = False

# -- Extension configuration -------------------------------------------------

myst_enable_extensions = [
    "colon_fence",
]
myst_heading_anchors = 3

copybutton_prompt_text = r"\$ |% |\[[^\]]+\]\$ "
copybutton_prompt_is_regexp = True

# -- Options for HTML output -------------------------------------------------

html_theme = "furo"
html_title = "OzSTAR User Guide"
html_static_path = ["_static"]
html_favicon = "_static/favicon.ico"
html_show_sourcelink = False
html_show_sphinx = False
html_show_copyright = False

html_theme_options = {
    "light_logo": "OzStar-FA-Colour.png",
    "dark_logo": "OzStar-FA-Mono-KEYLINE.png",
    "sidebar_hide_name": True,
}
