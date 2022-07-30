from sphinx.locale import __
from os.path import join, dirname, splitext
from lxml.html import fromstring, tostring
from pathlib import Path
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.writers.html5 import HTML5Translator
from docutils.nodes import SkipChildren


FRONTMATTER = """\
---
# this file is GENERATED, regenerate it with scripts/generate_python_docs.py
layout: docu
selected: Documentation/Python/Client API
title: Python Client API
---
"""


class JekyllTranslator(HTML5Translator):
    def visit_desc_parameter(self, node):
        txt = node.astext()
        if " = <duckdb." in txt:
            # FIXME: duckdb uses class instances as default params
            self.body.append(txt.split(" = ")[0] + " = None")
            raise SkipChildren()


class JekyllBuilder(StandaloneHTMLBuilder):
    name = "jekyll"
    format = "markdown"
    epilog = __("The jekyll files are in %(outdir)s.")

    allow_parallel = True
    default_translator_class = JekyllTranslator

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
                "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None)
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
