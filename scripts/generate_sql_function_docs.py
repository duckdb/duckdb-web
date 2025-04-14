#!/usr/bin/env python3

from dataclasses import dataclass, field
import duckdb
import re
from typing import Callable


@dataclass
class DocFunction:
    name: str
    parameters: list[str]
    description: str
    examples: list[str]
    category: str
    is_variadic: bool = False
    aliases: list[str] = field(default_factory=list)
    fixed_example_results: list[str] = field(default_factory=list)


DOC_VERSION = 'stable'
DOC_FILES = [
    f'docs/{DOC_VERSION}/sql/functions/blob.md',
    f'docs/{DOC_VERSION}/sql/functions/char.md',
]

# 'functions' that are binary operators are listed between the arguments
BINARY_OPERATORS = ['||', '^@', 'LIKE', 'SIMILAR TO']
EXTRACT_OPERATOR = '[]'

# override/add to duckdb_functions() outputs:
OVERRIDES: list[DocFunction] = [
    DocFunction(
        category='string',
        name='||',
        parameters=['string', 'string'],
        description="Concatenates two strings. Any `NULL` input results in `NULL`. See also `concat(string, ...)`.",
        examples=["'Duck' || 'DB'"],
    ),
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
        description="Returns the lower 64-bit segment of the MD5 hash of the `string` as a `BIGINT`.",
        examples=["md5_number_lower('123')"],
    ),
    DocFunction(
        category='string',
        name='md5_number_upper',
        parameters=['string'],
        description="Returns the upper 64-bit segment of the MD5 hash of the `string` as a `BIGINT`.",
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
    DocFunction(
        category='string',
        name='position',  # non standard parsing with 'IN' as pseudo argument
        parameters=['search_string IN string'],
        description="Return location of first occurrence of `search_string` in `string`, counting from 1. Returns 0 if no match found.",
        examples=["position('b' IN 'abc')"],
    ),
]

EXCLUDES = [('string', 'list_slice')]

PAGE_LINKS = {
    # intra page links
    '`concat(string, ...)`': "#concatstring-",
    '`string || string`': "#string--string",
    'fmt syntax': "#fmt-syntax",
    'printf syntax': '#printf-syntax',
    # other page links
    '`read_blob` guide': f'docs/{DOC_VERSION}/guides/file_formats/read_file.md#read_blob',
    'slicing': f'docs/{DOC_VERSION}/sql/functions/list.md#slicing',
    'Pattern Matching': f'docs/{DOC_VERSION}/sql/functions/pattern_matching.md',
    'collations': f'docs/{DOC_VERSION}/sql/expressions/collations.md',
    '`read_text` guide': f'docs/{DOC_VERSION}/guides/file_formats/read_file.md#read_text',
    'Regular Expressions': f'docs/{DOC_VERSION}/sql/functions/regular_expressions',
    # external page links
    '`os.path.dirname`': 'https://docs.python.org/3.7/library/os.path.html#os.path.dirname',
    '`os.path.basename`': 'https://docs.python.org/3.7/library/os.path.html#os.path.basename',
    '`pathlib.parts`': 'https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.parts',
    '`re.escape` function': 'https://docs.python.org/3/library/re.html#re.escape',
    'Percent-Encoding': 'https://datatracker.ietf.org/doc/html/rfc3986#section-2.1',
}


def main():
    for doc_file in DOC_FILES:
        print(f"creating file {doc_file} ...")
        generate_doc_file(doc_file)


def generate_doc_file(doc_file: str) -> None:
    with open(doc_file, "r") as f:
        doc_text = f.read()
    block_start_regex = r"(<!-- Start of section generated by scripts/generate_sql_function_docs.py; categories: \[)(.*?)(\] -->\n)"
    block_endline = (
        "<!-- End of section generated by scripts/generate_sql_function_docs.py -->\n"
    )
    block_regex = block_start_regex + "(.*?)" + f"({block_endline})"

    # group 0,1,2 = startline; group 3 = block content, group 4 = endline
    function_blocks: list[tuple[str, str, str, str, str]] = re.findall(
        block_regex, doc_text, re.DOTALL
    )
    if not function_blocks or any(
        len(block_groups) != 5 for block_groups in function_blocks
    ):
        print(
            f"doc generation failed, start or end line is missing in file " + doc_file
        )
        return
    for block_groups in function_blocks:
        current_block = ''.join(block_groups)
        startline = ''.join(block_groups[:3])
        categories = [category.strip() for category in block_groups[1].split(',')]
        function_data = get_function_data(categories)
        updated_block = (
            startline
            + generate_docs_table(function_data)
            + generate_docs_records(function_data)
            + block_endline
        )
        doc_text = doc_text.replace(current_block, updated_block)
    with open(doc_file, "w+") as f:
        f.write(doc_text)


def get_query(categories: str) -> str:
    return f"""
with categories as (select unnest({categories}) category)
select distinct
  f1.function_name,
  f1.parameters,
  f1.description,
  f1.examples,
  categories.category,
  f1.varargs='ANY' as is_variadic,
  list_sort(list_distinct(list(f2.function_name))) as aliases,
  list_value() fixed_example_results
from
  categories
  join duckdb_functions() f1 on list_contains(f1.categories, categories.category)
  left join duckdb_functions() f2 on (
    f1.alias_of = f2.function_name
    or f1.function_name = f2.alias_of
    or (f1.alias_of = f2.alias_of and f1.function_name != f2.function_name)
  )
group by all
order by all
"""


def get_function_data(categories: list[str]) -> list[DocFunction]:
    query = get_query(categories)
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
        and (func.category, func.name) not in EXCLUDES
    ]
    function_data += [
        override for override in OVERRIDES if override.category in categories
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
        for link_text in PAGE_LINKS:
            if link_text in function.description:
                if PAGE_LINKS[link_text].startswith('http'):
                    # external link
                    url = f"{PAGE_LINKS[link_text]}"
                else:
                    # internal link
                    page, _, section = PAGE_LINKS[link_text].partition('#')
                    url = ''
                    if page:
                        url = "{% " + f"link {page}" + " %}"
                    if section:
                        url += f"#{section}"
                function.description = function.description.replace(
                    link_text, f"[{link_text}]({url})"
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
            res += f"| [`{f.name}({", ".join(f.parameters)}{', ...' if (f.is_variadic) else ''})`](#{f.name.lstrip('@*!^')}{"-".join(f.parameters).lower().replace(' ', '-')}{'-' if (f.is_variadic) else ''}) | {f.description} |\n"
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
                query_result = duckdb.sql(rf"select {example}::VARCHAR").fetchall()
                if len(query_result) != 1:
                    print(f"WARNING: example for '{f.name}' yields multiple rows!")
                    example_result = 'Multiple rows: ' + ', '.join(
                        f"`'{query_result[idx_res][0]}'`"
                        for idx_res in range(len(query_result))
                    )
                else:
                    example_result = f"`{query_result[0][0]}`"
            except duckdb.ParserException as e:
                print(
                    f"Error for function '{f.name}', could not calculate example: '{example}'. Consider adding it via OVERRIDES'. {e}"
                )
        if '`' not in example_result:
            example_result = f"`{example_result}`"
        res += f"| **Result** | {example_result} |\n"
        if f.aliases:
            res += f"| **Alias** | {','.join(f"`{alias}`" for alias in f.aliases)} |\n"
        res += '\n'
    return res


if __name__ == "__main__":
    main()
