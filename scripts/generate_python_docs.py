from sphinx.locale import __
from os.path import join, dirname, splitext
from lxml.html import fromstring, tostring
from pathlib import Path
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.writers.html5 import HTML5Translator
from docutils.nodes import SkipChildren

import pandas
print(pandas)
print(pandas.DataFrame)

import duckdb


FRONTMATTER = """\
---
# this file is GENERATED, regenerate it with scripts/generate_python_docs.py
layout: docu
selected: Documentation/Python/Client API
title: Python Client API
---
"""


class JekyllBuilder(StandaloneHTMLBuilder):
    name = "jekyll"
    format = "markdown"
    epilog = __("The jekyll files are in %(outdir)s.")

    allow_parallel = True

    def copy_static_files(self) -> None:
        pass


def setup(app):
    app.add_builder(JekyllBuilder)


def post_process(filename:Path):
    with filename.open() as fh:
        html = fh.read()

    doc, = fromstring(html).xpath(".//div[@class='documentwrapper']")

    filename = splitext(filename)[0] + ".md"

    contents = tostring(doc, pretty_print=True).decode()
    contents = '\n'.join(line.lstrip() for line in contents.splitlines())

    with open(filename, "w") as fh:
        fh.write(FRONTMATTER + contents)


def main():
    print('generating against duckdb version', duckdb.__version__)

    destdir = join(dirname(__file__), "../docs/api/python/reference/")
    app = Sphinx(
        srcdir=destdir + "templates",
        confdir=None,
        outdir=destdir,
        doctreedir="/tmp/",
        confoverrides={
            "project": "duckdb",
            "extensions": [
                "sphinx.ext.intersphinx",
                "sphinx.ext.autodoc",
                "generate_python_docs",
            ],
            "html_theme": "basic",
            "html_show_sourcelink": False,
            "html_copy_source": False,
            "html_show_sphinx": False,
            "html_use_index": False,
            "intersphinx_mapping": {
                "pandas": ("https://pandas.pydata.org/pandas-docs/version/1.5.1/", None),
                "pyarrow": ("https://arrow.apache.org/docs/9.0/", None),
                "fsspec": ("https://filesystem-spec.readthedocs.io/en/latest/", None)
            }
        },
        buildername="jekyll",
    )

    app.build(True)

    post_process(Path(destdir) / 'index.html')
    for filename in Path(destdir).glob("*.html"):
        filename.unlink()


if __name__ == "__main__":
    main()
