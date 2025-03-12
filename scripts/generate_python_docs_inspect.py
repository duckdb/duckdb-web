import inspect

import duckdb


def get_doc_for_member(member_name, member, header):
    if member_name.startswith("_"):
        return ""

    bases = ""
    if hasattr(member, "__bases__"):
        bases = f"**Bases**: {','.join([base.__name__ for base in member.__bases__])}"
    return f"""
{header} {member_name}

{inspect.getdoc(member) if inspect.getdoc(member) else ''}

**Type**: {type(member).__name__}

{bases}
"""


def check_if_related_to_expression(member):
    if not callable(member):
        return False
    member_docs = inspect.getdoc(member)
    if not member_docs:
        return False
    return '-> duckdb.duckdb.Expression' in member_docs or member == duckdb.Expression


def get_doc_for_duckdb():
    doc = ""

    duckdb_class_members = inspect.getmembers(duckdb)

    # remove the modules
    duckdb_class_members = [
        member for member in duckdb_class_members if not inspect.ismodule(member[1])
    ]

    # get the expressions related
    expression_classes = [
        member[1]
        for member in duckdb_class_members
        if check_if_related_to_expression(member[1])
    ]
    # remove the expressions for the main list
    duckdb_class_members = [
        member for member in duckdb_class_members if member[1] not in expression_classes
    ]

    # get the exception classes
    exception_classes = [
        member[1]
        for member in duckdb_class_members
        if inspect.isclass(member[1]) and issubclass(member[1], Exception)
    ]
    # remove the exceptions from the main list
    duckdb_class_members = [
        member for member in duckdb_class_members if member[1] not in exception_classes
    ]

    # get the value based classes
    value_classes = [
        member[1]
        for member in duckdb_class_members
        if inspect.isclass(member[1]) and issubclass(member[1], duckdb.Value)
    ]
    # remove the value based classes from the main list
    duckdb_class_members = [
        member for member in duckdb_class_members if member[1] not in value_classes
    ]

    # get the built-in functions and methods for duckdb class
    builtin_members = [
        member[1] for member in duckdb_class_members if inspect.isbuiltin(member[1])
    ]
    # remove the built-in functions and methods for duckdb class from the main list
    duckdb_class_members = [
        member for member in duckdb_class_members if member[1] not in builtin_members
    ]

    doc = f"{doc}\n\n## Class duckdb"
    for value_class in builtin_members:
        doc = f"{doc}\n\n{get_doc_for_member(value_class.__name__, value_class, header="###")}"

    for member_name, member in duckdb_class_members:
        doc = f"{doc}\n\n{get_doc_for_member(member_name, member, header="##")}"
        if inspect.isclass(member):
            for nm, vm in inspect.getmembers(member):
                doc = f"{doc}\n\n{get_doc_for_member(nm, vm, header="###")}"

    doc = f"{doc}\n\n## Expressions"
    for expression_class in expression_classes:
        doc = f"{doc}\n\n{get_doc_for_member(expression_class.__name__, expression_class, header="###")}"
        if inspect.isclass(expression_class):
            for nm, vm in inspect.getmembers(expression_class):
                doc = f"{doc}\n\n{get_doc_for_member(nm, vm, header="####")}"

    doc = f"{doc}\n\n## Values"
    for value_class in value_classes:
        doc = f"{doc}\n\n{get_doc_for_member(value_class.__name__, value_class, header="###")}"

    doc = f"{doc}\n\n## Exceptions"
    for exception_class in exception_classes:
        doc = f"{doc}\n\n{get_doc_for_member(exception_class.__name__, exception_class, header="###")}"

    return doc


def main():
    with open("docs/stable/clients/python/reference/index.md", "w") as f:
        f.write(
            """---
layout: docu
redirect_from:
- /docs/api/python/reference/index
- /docs/api/python/reference/index/
- /docs/clients/python/reference/index
title: Python Client API
---

The API reference documentations is structured as follows:

1. [DuckDB Class Methods](#class-duckdb)
2. [DuckDBPyConnection](#duckdbpyconnection)
3. [DuckDBPyRelation](#duckdbpyrelation)
4. [Expressions](#expressions)
5. [Values](#values)
6. [Exceptions](#exceptions)

"""
        )
        doc = get_doc_for_duckdb()

        f.write(doc)


if __name__ == "__main__":
    main()
