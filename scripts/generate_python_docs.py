import enum
import inspect
import os
import re
import tempfile
from importlib.metadata import version
from os.path import join, dirname, splitext
from pathlib import Path

import duckdb
from lxml.html import fromstring, tostring
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.locale import __

from generate_python_relational_docs import (
    collect_members,
    generate_python_relational_api_md,
)
from generate_python_relational_docs_methods import DUCKDB_DOC_VERSION

redirect_from_text = """\
redirect_from:
- /docs/api/python/reference/index
- /docs/clients/python/reference/index
- /docs/stable/clients/python/reference/index
- /docs/current/clients/python/reference/index
- /docs/lts/clients/python/reference/index
- /docs/preview/clients/python/reference/index
"""

FRONTMATTER = f"""\
---
# this file is GENERATED, regenerate it with scripts/generate_python_docs.py
layout: docu
{redirect_from_text if DUCKDB_DOC_VERSION == '2.0' else ''}title: Python Client API
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
    # The page title comes from the front matter, so the reference sections are second level headings.
    contents = re.sub(r"<(/?)h1\b", r"<\1h2", contents)

    contents = contents.replace(
        f"%%20link%20docs/{DUCKDB_DOC_VERSION}/clients/python/relational_api.md%20%",
        f"% link docs/{DUCKDB_DOC_VERSION}/clients/python/relational_api.md %",
    )

    with open(filename, "w") as fh:
        fh.write(FRONTMATTER + contents)


REFERENCE_SECTIONS = [
    "Connection",
    "Relation",
    "Expressions",
    "Module Functions",
    "Types and Values",
    "Enumerations",
    "Exceptions",
]

# The classes behind the .str(), .dt(), .list() and .json() method families of Expression, which duckdb does not export.
EXPRESSION_NAMESPACES = ["StrExpr", "DtExpr", "ListExpr", "JsonExpr"]


def reference_section(name, obj):
    """The section of the reference that a name of duckdb.__all__ belongs to, decided by what the object is."""
    if inspect.isclass(obj):
        if issubclass(obj, BaseException):
            return "Exceptions"
        if issubclass(obj, enum.Enum):
            return "Enumerations"
        if issubclass(obj, duckdb.Value):
            return "Types and Values"
    if getattr(obj, "__module__", "").startswith("duckdb._expression"):
        return "Expressions"
    if obj is duckdb.DuckDBPyRelation:
        return "Relation"
    if inspect.isclass(obj):
        return "Connection"
    if (inspect.getdoc(obj) or "").split("\n", 1)[0].endswith("DuckDBPyType"):
        return "Types and Values"
    return "Module Functions"


def autodoc(name, obj):
    if inspect.isclass(obj):
        lines = [f".. autoclass:: {name}", "   :members:", "   :show-inheritance:"]
        # Aggregate methods and the str, dt, list and json namespaces come from mixins.
        if obj is duckdb.Expression:
            lines.append("   :inherited-members:")
        return "\n".join(lines) + "\n"
    return f".. autofunction:: {name}\n"


def create_index_rst():
    sections = {section: [] for section in REFERENCE_SECTIONS}
    for name in sorted(duckdb.__all__, key=str.lower):
        obj = getattr(duckdb, name)
        if name.startswith("_") or inspect.ismodule(obj) or not callable(obj):
            continue
        sections[reference_section(name, obj)].append((name, obj))

    with open(
        join(
            dirname(__file__),
            f"../docs/{DUCKDB_DOC_VERSION}/clients/python/reference/templates/index.rst",
        ),
        "w",
    ) as f:
        for section, entries in sections.items():
            f.write(f".. currentmodule:: duckdb\n\n{section}\n{'=' * len(section)}\n\n")
            for name, obj in entries:
                if obj is duckdb.DuckDBPyRelation:
                    f.write(".. include:: relation.rst\n")
                else:
                    f.write(autodoc(name, obj))
            if section == "Expressions":
                f.write("\n.. currentmodule:: duckdb._expression_namespaces\n\n")
                for name in EXPRESSION_NAMESPACES:
                    f.write(f".. autoclass:: {name}\n   :members:\n")
            f.write("\n")


def create_relation_rst():
    rst_definition = f"""\
.. autoclass:: duckdb.DuckDBPyRelation
    :show-inheritance:

    .. raw:: html

        <div>Detailed examples can be found at <a href="{{% link docs/{DUCKDB_DOC_VERSION}/clients/python/relational_api.md %}}">Relational API page</a>.</div>
        <br>
"""

    relation_members = [
        m for m in collect_members() if m["section"] != "Relation Creation"
    ]
    for member in sorted(relation_members, key=lambda m: m["name"]):
        member_name = member["name"]
        is_property = isinstance(
            inspect.getattr_static(duckdb.DuckDBPyRelation, member_name), property
        )
        rst_definition = f"""\
{rst_definition}
    .. {'autoattribute' if is_property else 'automethod'}:: {member_name}
    
        .. raw:: html
    
            <div>Detailed examples can be found at <a href="{{% link docs/{DUCKDB_DOC_VERSION}/clients/python/relational_api.md %}}#{member['anchor']}">Relational API page</a>.</div>
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
    with tempfile.TemporaryDirectory(prefix="duckdb-python-doctrees-") as doctrees:
        build_reference(destdir, doctrees)

    post_process(Path(destdir) / 'index.html')
    for filename in Path(destdir).glob("*.html"):
        filename.unlink()

    # test objects.inv
    # python -m sphinx.ext.intersphinx http://localhost:4000/docs/2.0/clients/python/reference/objects.inv


def build_reference(destdir, doctrees):
    app = Sphinx(
        srcdir=destdir + "templates",
        confdir=None,
        outdir=destdir,
        doctreedir=doctrees,
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
            # The builtin type in the Expression.cast annotations matches the members called type.
            "suppress_warnings": ["ref.python"],
            "intersphinx_mapping": {
                "pandas": (
                    "https://pandas.pydata.org/pandas-docs/version/3.0/",
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


if __name__ == "__main__":
    main()
