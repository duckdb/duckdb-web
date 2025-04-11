#!/usr/bin/env python3

import duckdb
from dataclasses import dataclass, field
from typing import Callable


@dataclass
class DocFunction:
    category: str
    name: str
    parameters: list[str]
    description: str
    examples: list[str]
    is_variadic: bool = False
    aliases: list[str] = field(default_factory=list)
    fixed_example_results: list[str] = field(default_factory=list)


DOC_CATEGORY_MAP = {
    'docs/stable/sql/functions/blob.md': 'blob',
    'docs/stable/sql/functions/char.md': 'string',
}

# 'functions' that are binary operators are listed between the arguments
BINARY_OPERATORS = ['||', '^@', 'LIKE', 'SIMILAR TO']
EXTRACT_OPERATOR = '[]'

# override/add to duckdb_functions() outputs:
OVERRIDES: list[DocFunction] = [
    DocFunction(
        category='blob',
        name='||',
        parameters=['blob', 'blob'],
        description='Concatenates two blobs. Any `NULL` input results in `NULL`.',
        examples=[r"'\xAA'::BLOB || '\xBB'::BLOB"],
    ),
    DocFunction(
        category='blob',
        name='read_blob',
        parameters=['source'],
        description="Returns the content from `source` (a filename, a list of filenames, or a glob pattern) as a `BLOB`. See the `read_blob` guide for more details.",
        examples=["read_blob('hello.bin')"],
        fixed_example_results=[r"hello\x0A"],
    ),
    DocFunction(
        category='string',
        name='||',
        parameters=['string', 'string'],
        description="Concatenates two strings. Any `NULL` input results in `NULL`. See also `concat(string, ...)`.",
        examples=["'Duck' || 'DB'"],
    ),
    DocFunction(
        category='string',
        name='[]',
        parameters=['string', 'index'],
        description="Extracts a single character using a (1-based) index.",
        examples=["'DuckDB'[4]"],
        aliases=['array_extract'],
    ),
    DocFunction(
        category='string',
        name='[]',
        parameters=['string', 'begin', 'end'],
        description='Extracts a string using slice conventions similar to Python. Missing `begin` or `end` arguments are interpreted as the beginning or end of the list respectively. Negative values are accepted.',
        examples=["'DuckDB'[:4]"],
        aliases=['array_slice'],
    ),
    DocFunction(
        category='string',
        name='LIKE',
        parameters=['string', 'target'],
        description='Returns `true` if the `string` matches the like specifier (see Pattern Matching).',
        examples=["'hello' LIKE '%lo'"],
    ),
    DocFunction(
        category='string',
        name='SIMILAR TO',
        parameters=['string', 'regex'],
        description="Returns `true` if the `string` matches the `regex` (see Pattern Matching).",
        examples=["'hello' SIMILAR TO 'l+'"],
        aliases=['regexp_full_match'],
    ),
    DocFunction(
        category='string',
        name='md5_number_lower',
        parameters=['string'],
        description="Returns the lower 64-bit segment of the `MD5` hash of the `string` as a `BIGINT`.",
        examples=["md5_number_lower('123')"],
    ),
    DocFunction(
        category='string',
        name='md5_number_upper',
        parameters=['string'],
        description="Returns the upper 64-bit segment of the `MD5` hash of the `string` as a `BIGINT`.",
        examples=["md5_number_upper('123')"],
    ),
    DocFunction(
        category='regex',
        name='regexp_split_to_table',
        parameters=['string', 'regex'],
        description="Splits the `string` along the `regex` and returns a row for each part.",
        examples=["regexp_split_to_table('hello world; 42', ';? ')"],
    ),
    DocFunction(
        category='string',
        name='split_part',
        parameters=['string', 'separator', 'index'],
        description="Splits the `string` along the `separator` and returns the data at the (1-based) `index` of the list. If the `index` is outside the bounds of the list, return an empty string (to match PostgreSQL's behavior).",
        examples=["split_part('a;b;c', ';', 2)"],
    ),
    DocFunction(
        category='string',
        name='read_text',
        parameters=['source'],
        description="Returns the content from `source` (a filename, a list of filenames, or a glob pattern) as a `VARCHAR`. The file content is first validated to be valid UTF-8. If `read_text` attempts to read a file with invalid UTF-8 an error is thrown suggesting to use `read_blob` instead. See the `read_text` guide for more details.",
        examples=["read_text('hello.txt')"],
        fixed_example_results=["hello\\n"],
    ),
]

EXCLUDES = [('string', 'list_slice')]

URL_CONVERSIONS = {
    '`read_blob` guide': ('docs/stable/guides/file_formats/read_file.md', '#read_blob'),
    '`concat(string, ...)`': ('', "#concatstring-"),
}


def main():
    for doc_file, category in DOC_CATEGORY_MAP.items():
        print(f"creating file {doc_file} ...")
        generate_doc_file(doc_file, category)


def generate_doc_file(doc_file: str, category: str) -> None:
    function_data: list[DocFunction] = get_function_data(category)
    startline = (
        "<!-- Start of section generated by scripts/generate_sql_function_docs.py -->\n"
    )
    endline = (
        "<!-- End of section generated by scripts/generate_sql_function_docs.py -->\n"
    )
    with open(doc_file, "r") as f:
        doc_text = f.read()
    if startline not in doc_text or endline not in doc_text:
        print(
            f"doc generation failed, start or end line is missing in file " + doc_file
        )
        exit(1)
    else:
        split_start = doc_text.rsplit(startline, 1)
        split_end = doc_text.rsplit(endline, 1)
        doc_text_new = (
            split_start[0]
            + startline
            + generate_docs_table(function_data)
            + generate_docs_records(function_data)
            + endline
            + split_end[1]
        )
        with open(doc_file, "w+") as f:
            f.write(doc_text_new)


def get_function_data(category: str) -> list[DocFunction]:
    query = f"""
select distinct
  '{category}' category,
  f1.function_name,
  f1.parameters,
  f1.description,
  f1.examples,
  f1.varargs='ANY' as is_variadic,
  list_sort(list_distinct(list(f2.function_name))) as aliases,
  list_value() fixed_example_results
from
  duckdb_functions() f1
  left join duckdb_functions() f2 on (
    f1.alias_of = f2.function_name
    or f1.function_name = f2.alias_of
    or (f1.alias_of = f2.alias_of and f1.function_name != f2.function_name)
  )
where
  list_contains(f1.categories, '{category}')
group by all
order by all
"""
    function_data: list[DocFunction] = [
        DocFunction(*func) for func in duckdb.sql(query).fetchall()
    ]
    # apply overrides and add additional functions
    function_data = [
        func
        for func in function_data
        if not any(
            func.category == override.category and func.name == override.name
            for override in OVERRIDES
        )
        and (category, func.name) not in EXCLUDES
    ]
    function_data += [
        override for override in OVERRIDES if override.category == category
    ]
    # sort on: function_name, nr of arguments, argument names
    sorter: Callable[[DocFunction], str] = (
        lambda func: f"{func.name}-{len(func.parameters)}-{func.parameters}"
    )
    function_data_1 = sorted(
        [func for func in function_data if func.name == EXTRACT_OPERATOR], key=sorter
    )
    function_data_2 = sorted(
        [func for func in function_data if func.name in BINARY_OPERATORS], key=sorter
    )
    function_data_3 = sorted(
        [
            func
            for func in function_data
            if (func.name not in BINARY_OPERATORS) and (func.name != EXTRACT_OPERATOR)
        ],
        key=sorter,
    )
    function_data = function_data_1 + function_data_2 + function_data_3
    # apply url conversions
    for function in function_data:
        for conversion in URL_CONVERSIONS:
            if conversion in function.description:
                function.description = function.description.replace(
                    conversion,
                    f"[{conversion}]"
                    "({% "
                    f"link {URL_CONVERSIONS[conversion][0]}"
                    " %}"
                    f"{URL_CONVERSIONS[conversion][1]})",
                )
    return function_data


def generate_docs_table(function_data: list[DocFunction]):
    res = "<!-- markdownlint-disable MD056 -->\n\n"
    res += "| Name | Description |\n|:--|:-------|\n"
    for f in function_data:
        if not f.examples:
            print(f"WARNING (skipping): '{f.name}' - no example is available")
            continue
        if f.name in BINARY_OPERATORS and len(f.parameters) == 2:
            res += f"| [`{f.parameters[0]} {f.name} {f.parameters[1]}`](#{f.parameters[0]}--{f.parameters[1]}) | {f.description} |\n"
        elif f.name == EXTRACT_OPERATOR and len(f.parameters) >= 2:
            res += f"| [`{f.parameters[0]}[{":".join(f.parameters[1:])}]`](#{"".join(f.parameters)}) | {f.description} |\n"
        else:
            res += f"| [`{f.name}({", ".join(f.parameters)}{', ...' if (f.is_variadic) else ''})`](#{f.name.lstrip('@*!^')}{"-".join(f.parameters)}{'-' if (f.is_variadic) else ''}) | {f.description} |\n"
    res += "\n<!-- markdownlint-enable MD056 -->\n"
    return res


def generate_docs_records(function_data: list[DocFunction]):
    res = "\n"
    for f in function_data:
        if not f.examples:
            print(f"skipping {f.name}")
            continue
        if len(f.examples) > 1:
            print(f"WARNING: '{f.name}' multiple examples available: {f.examples}")
        example = f.examples[0]
        example_result = f.fixed_example_results[0] if f.fixed_example_results else ''
        if f.name in BINARY_OPERATORS and len(f.parameters) == 2:
            res += f"#### `{f.parameters[0]} {f.name} {f.parameters[1]}`\n\n"
        elif f.name == EXTRACT_OPERATOR and len(f.parameters) >= 2:
            res += f"#### `{f.parameters[0]}[{":".join(f.parameters)}]`\n\n"
        else:
            res += f"#### `{f.name}({", ".join(f.parameters)}{', ...' if (f.is_variadic) else ''})`\n\n"
        res += '<div class="nostroke_table"></div>\n\n'
        res += f"| **Description** | {f.description} |\n"
        res += f"| **Example** | `{example}` |\n"
        if not example_result:
            try:
                example_result = duckdb.sql(rf"select {example}::VARCHAR").fetchone()[0]
            except duckdb.ParserException as e:
                print(
                    f"Error for function '{f.name}', could not calculate example: '{example}'. Consider adding it via OVERRIDES'. {e}"
                )
        res += f"| **Result** | `{example_result}` |\n"
        if f.aliases:
            res += f"| **Alias** | {','.join(f"`{alias}`" for alias in f.aliases)} |\n"
        res += '\n'
    return res


if __name__ == "__main__":
    main()
