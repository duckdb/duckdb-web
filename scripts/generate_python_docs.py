import inspect
import os
from importlib.metadata import version
from os.path import join, dirname, splitext
from pathlib import Path

import duckdb
from lxml.html import fromstring, tostring
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.locale import __

from generate_python_relational_docs import generate_python_relational_api_md

DUCKDB_DOC_VERSION = os.getenv("DUCKDB_DOC_VERSION", "preview")

redirect_from_text = """\
redirect_from:
- /docs/api/python/reference/index
- /docs/api/python/reference/index/
- /docs/clients/python/reference/index
"""

FRONTMATTER = f"""\
---
# this file is GENERATED, regenerate it with scripts/generate_python_docs.py
layout: docu
{redirect_from_text if DUCKDB_DOC_VERSION == 'stable' else ''}
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


def post_process(filename: Path):
    with filename.open() as fh:
        html = fh.read()

    (doc,) = fromstring(html).xpath(".//div[@class='documentwrapper']")

    filename = splitext(filename)[0] + ".md"

    contents = tostring(doc, pretty_print=True).decode()
    contents = '\n'.join(line.lstrip() for line in contents.splitlines())

    contents = contents.replace(
        f"%%20link%20docs/{DUCKDB_DOC_VERSION}/clients/python/relational_api.md%20%",
        f"% link docs/{DUCKDB_DOC_VERSION}/clients/python/relational_api.md %",
    )

    with open(filename, "w") as fh:
        fh.write(FRONTMATTER + contents)


def create_index_rst():
    classes = [
        {
            "name": name,
            "rst_type": 'automethod' if not inspect.isclass(obj) else 'autoclass',
        }
        for name, obj in inspect.getmembers(duckdb)
        if inspect.isclass(obj) or inspect.isroutine(obj)
    ]

    with open(
        join(
            dirname(__file__),
            f"../docs/{DUCKDB_DOC_VERSION}/clients/python/reference/templates/index.rst",
        ),
        "w",
    ) as f:
        f.write(".. currentmodule:: duckdb\n\n")
        for cls in classes:
            if cls['name'] == "DuckDBPyRelation":
                f.write(".. include:: relation.rst\n")
            else:
                f.write(f".. {cls['rst_type']}:: duckdb.{cls['name']}\n")
                if cls['rst_type'] == 'autoclass':
                    f.write("   :members:\n")
                    f.write("   :show-inheritance:\n")


def create_relation_rst():
    rst_definition = f"""\
.. autoclass:: duckdb.DuckDBPyRelation
    :show-inheritance:

    .. raw:: html

        <div>Detailed examples can be found at <a href="{{% link docs/{DUCKDB_DOC_VERSION}/clients/python/relational_api.md %}}">Relational API page</a>.</div>
        <br>
"""

    for member_name, member_type in inspect.getmembers(duckdb.DuckDBPyRelation):
        if member_name.startswith("_"):
            continue
        rst_definition = f"""\
{rst_definition}
    .. {'automethod' if callable(member_type) else 'autoattribute'}:: {member_name}
    
        .. raw:: html
    
            <div>Detailed examples can be found at <a href="{{% link docs/{DUCKDB_DOC_VERSION}/clients/python/relational_api.md %}}#{member_name}">Relational API page</a>.</div>
            <br>
"""

    with open(
        join(
            dirname(__file__),
            f"../docs/{DUCKDB_DOC_VERSION}/clients/python/reference/templates/relation.rst",
        ),
        "w",
    ) as rst_file:
        rst_file.write(rst_definition)


def main():
    print(
        'generating against duckdb version',
        version('duckdb'),
        'and pandas version',
        version('pandas'),
    )

    generate_python_relational_api_md()
    create_index_rst()
    create_relation_rst()
    destdir = join(
        dirname(__file__), f"../docs/{DUCKDB_DOC_VERSION}/clients/python/reference/"
    )
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
                "pandas": (
                    "https://pandas.pydata.org/pandas-docs/version/1.5.1/",
                    None,
                ),
                "pyarrow": ("https://arrow.apache.org/docs/9.0/", None),
                "fsspec": ("https://filesystem-spec.readthedocs.io/en/latest/", None),
            },
            "exclude_patterns": ['relation.rst'],
        },
        buildername="jekyll",
    )

    app.build(True)

    post_process(Path(destdir) / 'index.html')
    for filename in Path(destdir).glob("*.html"):
        filename.unlink()

    # test objects.inv
    # python -m sphinx.ext.intersphinx http://localhost:4000/docs/preview/clients/python/reference/objects.inv


if __name__ == "__main__":
    main()
