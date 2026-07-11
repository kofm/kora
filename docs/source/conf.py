project = "kora"
copyright = "2025, Gabriele Mongiano"
author = "Gabriele Mongiano"
release = "0.5.13"
version = release

extensions = ["sphinxcontrib.openapi"]

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "furo"
html_static_path = ["_static"]

redoc = [
    {
        "name": "Kora API",
        "page": "openapi",
        "spec": "openapi.yaml",
        "embed": True,
    }
]

# Add domain objects such as functions/classes/HTTP endpoints to the page TOC.
toc_object_entries = True

# Optional: make generated entries shorter.
toc_object_entries_show_parents = "hide"
