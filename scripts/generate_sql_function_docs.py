#!/usr/bin/env python3

from dataclasses import dataclass, field
import copy
import duckdb
import re
import operator
from typing import Optional, Self


@dataclass(order=True)
class DocFunction:
    name: str
    parameters: list[str]
    description: str
    examples: list[str]
    category: str
    alias_of: str = ''
    is_variadic: bool = False
    aliases: list[str] = field(default_factory=list)
    fixed_example_results: list[str] = field(default_factory=list)
    nr_optional_arguments: int = 0
    alias_of_obj: Optional[Self] = None


DOC_VERSION = 'preview'
DOC_FILES = [
    f'docs/{DOC_VERSION}/sql/functions/array.md',
    f'docs/{DOC_VERSION}/sql/functions/blob.md',
    f'docs/{DOC_VERSION}/sql/functions/lambda.md',
    f'docs/{DOC_VERSION}/sql/functions/list.md',
    f'docs/{DOC_VERSION}/sql/functions/text.md',
]

# 'functions' that are binary operators are listed between the arguments
BINARY_OPERATORS = ['||', '^@', '&&', '<->', '<=>', '<@', '@>', 'LIKE', 'SIMILAR TO']
EXTRACT_OPERATOR = '[]'
# 'position' requires keyword 'IN' as argument
NON_STANDARD_FUNCTIONS = ['position']

# list macros defined in duckdb/src/catalog/default/default_functions.cpp
LIST_AGGREGATE_FUNCTIONS = [
    # algebraic list aggregates
    "list_avg",
    "list_var_samp",
    "list_var_pop",
    "list_stddev_pop",
    "list_stddev_samp",
    "list_sem",
    # distributive list aggregates
    "list_approx_count_distinct",
    "list_bit_xor",
    "list_bit_or",
    "list_bit_and",
    "list_bool_and",
    "list_bool_or",
    "list_count",
    "list_entropy",
    "list_last",
    "list_first",
    "list_any_value",
    "list_kurtosis",
    "list_kurtosis_pop",
    "list_min",
    "list_max",
    "list_product",
    "list_skewness",
    "list_sum",
    "list_string_agg",
    # holistic list aggregates
    "list_mode",
    "list_median",
    "list_mad",
    # nested list aggregates
    "list_histogram",
]

# override/add to duckdb_functions() outputs:
"""
NOTE: duckdb_functions() only contains sufficient information for scalar and aggregate functions.
For now, function info for table functions, macros, and a number of spcials is added via the
OVERRIDES list
"""
OVERRIDES: list[DocFunction] = [
    # table functions
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
        name='read_text',
        parameters=['source'],
        description="Returns the content from `source` (a filename, a list of filenames, or a glob pattern) as a `VARCHAR`. The file content is first validated to be valid UTF-8. If `read_text` attempts to read a file with invalid UTF-8 an error is thrown suggesting to use `read_blob` instead. See the `read_text` guide for more details.",
        examples=["read_text('hello.txt')"],
        fixed_example_results=["hello\\n"],
    ),
    DocFunction(
        category='list',
        name='unnest',
        parameters=['list'],
        description="Unnests a list by one level. Note that this is a special function that alters the cardinality of the result. See the unnest page for more details.",
        examples=["unnest([1, 2, 3])"],
    ),
    # macros
    DocFunction(
        category='string',
        name='md5_number_lower',
        parameters=['string'],
        description="Returns the lower 64-bit segment of the MD5 hash of the `string` as a `UBIGINT`.",
        examples=["md5_number_lower('abc')"],
    ),
    DocFunction(
        category='string',
        name='md5_number_upper',
        parameters=['string'],
        description="Returns the upper 64-bit segment of the MD5 hash of the `string` as a `UBIGINT`.",
        examples=["md5_number_upper('abc')"],
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
        category='list',
        name='list_prepend',
        parameters=['element', 'list'],
        description="Prepends `element` to `list`.",
        examples=["list_prepend(3, [4, 5, 6])"],
        aliases=["array_prepend"],
    ),
    DocFunction(
        category='list',
        name='array_push_front',
        parameters=['list', 'element'],
        description="Prepends `element` to `list`.",
        examples=["array_push_front([4, 5, 6], 3)"],
    ),
    DocFunction(
        category='list',
        name='list_append',
        parameters=["list", "element"],
        description="Appends `element` to `list`.",
        examples=["list_append([2, 3], 4)"],
        aliases=["array_append", "array_push_back"],
    ),
    DocFunction(
        category='list',
        name='array_pop_back',
        parameters=["list"],
        description="Returns the `list` without the last element.",
        examples=["array_pop_back([4, 5, 6])"],
    ),
    DocFunction(
        category='list',
        name='array_pop_front',
        parameters=["list"],
        description="Returns the `list` without the first element.",
        examples=["array_pop_front([4, 5, 6])"],
    ),
    DocFunction(
        category='list',
        name='array_to_string',
        parameters=['list', 'delimiter'],
        description="Concatenates list/array elements using an optional `delimiter`.",
        examples=[
            "array_to_string([1, 2, 3], '-')",
            "array_to_string(['aa', 'bb', 'cc'], '')",
        ],
    ),
    DocFunction(
        category='list',
        name='array_to_string_comma_default',
        parameters=['array'],
        description="Concatenates list/array elements with a comma delimiter.",
        examples=["array_to_string_comma_default(['Banana', 'Apple', 'Melon'])"],
    ),
    DocFunction(
        category='list',
        name='list_intersect',
        parameters=['list1', 'list2'],
        description="Returns a list of all the elements that exist in both `list1` and `list2`, without duplicates.",
        examples=["list_intersect([1, 2, 3], [2, 3, 4])"],
        aliases=["array_intersect"],
    ),
    DocFunction(
        category='list',
        name='list_reverse',
        parameters=['list'],
        description="Reverses the `list`.",
        examples=["list_reverse([3, 6, 1, 2])"],
        aliases=["array_reverse"],
    ),
    # others
    DocFunction(
        category='string',
        name='[]',
        parameters=['string', 'index'],
        description="Extracts a single character using a (1-based) `index`.",
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
        category='list',
        name='[]',
        parameters=['list', 'index'],
        description="Extracts a single list element using a (1-based) `index`.",
        examples=["[4, 5, 6][3]"],
        aliases=['list_extract'],
    ),
    DocFunction(
        category='list',
        name='[]',
        parameters=['list', 'begin', 'end', 'step'],
        description="Extracts a sublist using slice conventions. Negative values are accepted.",
        examples=["[4, 5, 6][3]"],
        aliases=['list_slice'],
        nr_optional_arguments=2,
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
        name='position',  # non-standard parsing with 'IN' as pseudo argument
        parameters=['search_string IN string'],
        description="Return location of first occurrence of `search_string` in `string`, counting from 1. Returns 0 if no match found.",
        examples=["position('b' IN 'abc')"],
        aliases=['instr', 'strpos'],
    ),
    DocFunction(
        category='string',
        name='^@',  # edge case: alias between operator and regular function
        parameters=['string', 'search_string'],
        description="Returns `true` if `string` begins with `search_string`.",
        examples=["'abc' ^@ 'a'"],
        aliases=['starts_with'],
    ),
    DocFunction(
        category='list',
        name='list_concat',  # edge case: variadic taking ANY[]
        parameters=['list_1', '...', 'list_n'],
        description="Concatenates lists. `NULL` inputs are skipped. See also operator `||`.",
        examples=["list_concat([2, 3], [4, 5, 6], [7])"],
        aliases=['list_cat', 'array_concat', 'array_cat'],
        is_variadic=True,
    ),
    DocFunction(
        category='list',
        name='list_zip',  # edge case: variadic taking ANY (multiple lists, plus optional boolean)
        parameters=['list_1', '...', 'list_n', 'truncate'],
        description="Zips n `LIST`s to a new `LIST` whose length will be that of the longest list. Its elements are structs of n elements from each list `list_1`, …, `list_n`, missing elements are replaced with `NULL`. If `truncate` is set, all lists are truncated to the smallest list length.",
        examples=[
            "list_zip([1, 2], [3, 4], [5, 6])",
            "list_zip([1, 2], [3, 4], [5, 6, 7])",
            "list_zip([1, 2], [3, 4], [5, 6, 7], true)",
        ],
        aliases=['array_zip'],
        nr_optional_arguments=1,
        is_variadic=True,
    ),
]

# NOTE: All function aliases are added, unless explicitly excluded. Format: (<category>, <function_name>)
EXCLUDES = [('string', 'list_slice')]

# define appends to function descriptions, e.g. for 'more details' links.
DESCRIPTION_EXTENSIONS = {
    "list_aggregate": "See the List Aggregates section for more details.",
    "list_filter": "See `list_filter` examples.",
    "list_reduce": "See `list_reduce` examples.",
    "list_transform": "See `list_transform` examples.",
    "list_sort": "See the Sorting Lists section for more details about sorting order and `NULL` values.",
    "list_reverse_sort": "See the Sorting Lists section for more details about sorting order and `NULL` values.",
}

PAGE_LINKS = {
    # intra-page links:
    'operator `||`': "#arg1--arg2",
    'fmt syntax': "#fmt-syntax",
    'printf syntax': '#printf-syntax',
    'Flattens': '#flattening',
    'List Aggregates': '#list-aggregates',
    'Sorting Lists': '#sorting-lists',
    'list_sort': '#list_sortlist',
    # links to other doc pages:
    '`concat(arg1, arg2, ...)`': f"docs/{DOC_VERSION}/sql/functions/text.md#concatvalue-",
    '`list_concat(list1, list2, ...)`': f'docs/{DOC_VERSION}/sql/functions/list.md#list_concatlist_1--list_n',
    '`list_filter` examples': f'docs/{DOC_VERSION}/sql/functions/lambda.md#list_filter-examples',
    '`list_reduce` examples': f'docs/{DOC_VERSION}/sql/functions/lambda.md#list_reduce-examples',
    '`list_transform` examples': f'docs/{DOC_VERSION}/sql/functions/lambda.md#list_transform-examples',
    '`read_blob` guide': f'docs/{DOC_VERSION}/guides/file_formats/read_file.md#read_blob',
    '`read_text` guide': f'docs/{DOC_VERSION}/guides/file_formats/read_file.md#read_text',
    'slicing': f'docs/{DOC_VERSION}/sql/functions/list.md#slicing',
    'slice conventions': f'docs/{DOC_VERSION}/sql/functions/list.md#slicing',
    'Pattern Matching': f'docs/{DOC_VERSION}/sql/functions/pattern_matching.md',
    'collations': f'docs/{DOC_VERSION}/sql/expressions/collations.md',
    'regex `options`': f'docs/{DOC_VERSION}/sql/functions/regular_expressions.md#options-for-regular-expression-functions',
    'unnest page': f'docs/{DOC_VERSION}/sql/query_syntax/unnest.md',
    # external page links:
    '`os.path.dirname`': 'https://docs.python.org/3.7/library/os.path.html#os.path.dirname',
    '`os.path.basename`': 'https://docs.python.org/3.7/library/os.path.html#os.path.basename',
    '`pathlib.parts`': 'https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.parts',
    '`re.escape` function': 'https://docs.python.org/3/library/re.html#re.escape',
    'Percent-Encoding': 'https://datatracker.ietf.org/doc/html/rfc3986#section-2.1',
}


def main():
    print(
        f"generating docfiles with DuckDB version: {duckdb.sql('pragma version').fetchone()}"
    )
    for doc_file in DOC_FILES:
        print(f"creating file {doc_file} ...")
        with open(doc_file, "r") as f:
            doc_text = f.read()
        block_endline = "<!-- End of section generated by scripts/generate_sql_function_docs.py -->\n"
        for current_block, startline, categories in get_function_blocks(
            doc_text, block_endline
        ):
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


# returns (full_block_content, startline, categories) per function block in the file
def get_function_blocks(
    doc_text: str, block_endline: str
) -> list[tuple[list[str], str, str]]:
    startline_regex = r"(<!-- Start of section generated by scripts/generate_sql_function_docs.py; categories: \[)(.*?)(\] -->\n)"
    block_regex = startline_regex + "(.*?)" + f"({block_endline})"
    function_blocks: list[tuple[str, str, str, str, str]] = re.findall(
        block_regex, doc_text, re.DOTALL
    )
    # regex groups: 0,1,2 = startline; group 3 = block content, group 4 = endline
    if not function_blocks or any(
        len(block_groups) != 5 for block_groups in function_blocks
    ):
        print(f"ERROR: doc generation failed, start or end line missing in file")
        exit(1)
    function_blocks_info = []
    for block_groups in function_blocks:
        full_block_content = ''.join(block_groups)
        startline = ''.join(block_groups[:3])
        categories = [category.strip() for category in block_groups[1].split(',')]
        function_blocks_info.append((full_block_content, startline, categories))
    return function_blocks_info


def get_function_data(categories: list[str]) -> list[DocFunction]:
    query = function_data_query(categories)
    function_data: list[DocFunction] = [
        DocFunction(*func) for func in duckdb.sql(query).fetchall()
    ]
    function_data = apply_overrides(function_data, categories)
    function_data = sort_function_data(function_data)
    function_data = prune_duplicates(function_data)
    for function in function_data:
        apply_description_appends(function)
        apply_url_conversions(function)
        set_canonical_function(function, function_data)
    return function_data


def function_data_query(categories: str) -> str:
    return f"""
with categories as (select unnest({categories}) category)
select distinct
  f1.function_name,
  f1.parameters,
  f1.description,
  f1.examples,
  categories.category,
  f1.alias_of,
  f1.varargs='ANY' as is_variadic,
  list_sort(list_distinct(list(f2.function_name))) as aliases,
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


def apply_overrides(function_data: list[DocFunction], categories: list[str]):
    function_data = [
        func
        for func in function_data
        if not any(
            func.category == override.category and func.name == override.name
            for override in OVERRIDES
        )
        and (func.category, func.name) not in EXCLUDES
    ]
    if 'list' in categories:
        for list_aggregate_function in LIST_AGGREGATE_FUNCTIONS:
            example_list = (
                "[3,3,9]" if 'bool' not in list_aggregate_function else "[true, false]"
            )
            function_data.append(
                DocFunction(
                    category='list',
                    name=list_aggregate_function,
                    parameters=['list'],
                    description=f"Applies aggregate function [`{list_aggregate_function[5:]}`]({{% link docs/{DOC_VERSION}/sql/functions/aggregates.md %}}#general-aggregate-functions) to the `list`.",
                    examples=[f"{list_aggregate_function}({example_list})"],
                )
            )
    for override in OVERRIDES:
        if override.category in categories:
            function_data.append(override)
            for alias_str in override.aliases:
                if (
                    alias_str not in function_data
                    and override.name not in BINARY_OPERATORS
                    and override.name not in NON_STANDARD_FUNCTIONS
                    and override.name != EXTRACT_OPERATOR
                ):
                    alias: DocFunction = copy.deepcopy(override)
                    alias.name = alias_str
                    alias.aliases.remove(alias_str)
                    alias.aliases.append(override.name)
                    alias.examples = [
                        example.replace(override.name, alias.name)
                        for example in alias.examples
                    ]
                    function_data.append(alias)
    return function_data


def sort_function_data(function_data: list[DocFunction]):
    function_data_1 = sorted(
        [func for func in function_data if func.name == EXTRACT_OPERATOR],
        key=lambda func: len(func.parameters),
    )
    function_data_2 = sorted(
        [func for func in function_data if func.name in BINARY_OPERATORS],
        key=operator.attrgetter("name", "description", "parameters"),
    )
    function_data_3 = sorted(
        [
            func
            for func in function_data
            if (func.name not in BINARY_OPERATORS) and (func.name != EXTRACT_OPERATOR)
        ],
        key=operator.attrgetter("name", "description", "parameters"),
    )
    return function_data_1 + function_data_2 + function_data_3


# remove duplicates with optional parameters
def prune_duplicates(function_data: list[DocFunction]):
    for idx_func, func in enumerate(function_data):
        if idx_func == 0:
            continue
        if (
            func.name == function_data[idx_func - 1].name
            and function_data[idx_func - 1].description == func.description
        ):
            if function_data[idx_func - 1].parameters == func.parameters[:-1]:
                func.nr_optional_arguments = (
                    function_data[idx_func - 1].nr_optional_arguments + 1
                )
                function_data[idx_func - 1].name = "DELETE_ME"
            elif all(
                param in function_data[idx_func - 1].parameters
                for param in func.parameters
            ):
                func.name = "DELETE_ME"
    return [func for func in function_data if func.name != "DELETE_ME"]


def apply_description_appends(function: DocFunction):
    for extension_function in DESCRIPTION_EXTENSIONS:
        if (
            extension_function == function.name
            or extension_function in function.aliases
        ):
            function.description = (
                f"{function.description} {DESCRIPTION_EXTENSIONS[extension_function]}"
            )
    return function


def apply_url_conversions(function: DocFunction):
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
    return function


def set_canonical_function(function: DocFunction, function_data: list[DocFunction]):
    if function.alias_of:
        for other_func in function_data:
            if (
                other_func.name == function.alias_of
                and other_func.parameters == function.parameters
            ):
                function.alias_of_obj = other_func
                break
    return function


def generate_docs_table(function_data: list[DocFunction]):
    table_str = "<!-- markdownlint-disable MD056 -->\n\n"
    table_str += "| Function | Description |\n|:--|:-------|\n"
    for func in function_data:
        if not func.examples:
            print(f"WARNING (skipping): '{func.name}' - no example is available")
            continue
        func_title = get_function_title(func)
        if func.alias_of_obj:
            anchor = get_anchor_from_title(get_function_title(func.alias_of_obj))
            func_description = f"Alias for `{func.alias_of_obj.name}`."
        else:
            anchor = get_anchor_from_title(func_title)
            func_description = func.description
        table_str += f"| [`{func_title}`](#{anchor}) | {func_description} |\n"
    table_str += "\n<!-- markdownlint-enable MD056 -->\n"
    return table_str


def generate_docs_records(function_data: list[DocFunction]):
    record_str = "\n"
    for func in function_data:
        if func.alias_of_obj:
            continue
        record_str += f"#### `{get_function_title(func)}`\n\n"
        record_str += '<div class="nostroke_table"></div>\n\n'
        record_str += f"| **Description** | {func.description} |\n"
        record_str += generate_example_rows(func)
        if func.aliases:
            aliases = ', '.join(f"`{alias}`" for alias in func.aliases)
            record_str += f"| **{'Alias' if len(func.aliases) == 1 else 'Aliases'}** | {aliases} |\n"
        record_str += '\n'
    return record_str


def get_function_title(func: DocFunction):
    if func.name in BINARY_OPERATORS:
        assert len(func.parameters) == 2
        function_title = f"{func.parameters[0]} {func.name} {func.parameters[1]}"
    elif func.name == EXTRACT_OPERATOR:
        assert len(func.parameters) >= 2
        if func.nr_optional_arguments == 0:
            parameter_str = ":".join(func.parameters[1:])
        else:
            mandatory_args = func.parameters[1 : -1 * func.nr_optional_arguments]
            optional_args = func.parameters[-1 * func.nr_optional_arguments :]
            parameter_str = f"{":".join(mandatory_args)}{"".join(f"[:{arg}]" for arg in optional_args)}"
        function_title = f"{func.parameters[0]}[{parameter_str}]"
    else:
        if func.is_variadic and len(func.parameters) == 0:
            func.parameters = ['arg']
        if func.nr_optional_arguments == 0:
            parameter_str = f"{", ".join(func.parameters)}{', ...' if (func.is_variadic and '...' not in func.parameters) else ''}"
        else:
            mandatory_args = func.parameters[: -1 * func.nr_optional_arguments]
            optional_args = func.parameters[-1 * func.nr_optional_arguments :]
            parameter_str = f"{", ".join(mandatory_args)}{"".join(f"[, {arg}]" for arg in optional_args)}"
        function_title = f"{func.name}({parameter_str})"
    return function_title


def get_anchor_from_title(title: str):
    return re.sub(r'[\(\)\[\]\.,$@|:<>=&^]+', '', title.lower().replace(' ', '-'))


def generate_example_rows(func: DocFunction):
    lines = ''
    for idx, example in enumerate(func.examples):
        example_result = (
            func.fixed_example_results[idx] if func.fixed_example_results else ''
        )
        example_num = ' ' + str(idx + 1) if len(func.examples) > 1 else ''
        lines += f"| **Example{example_num}** | `{example}` |\n"
        if not example_result:
            try:
                if func.name in BINARY_OPERATORS:
                    example = f"({example})"
                query_result = duckdb.sql(rf"select {example}::VARCHAR").fetchall()
                if len(query_result) != 1:
                    example_result = 'Multiple rows: ' + ', '.join(
                        (
                            f"`'{query_result[idx_result][0]}'`"
                            if query_result[idx_result][0]
                            else "`NULL`"
                        )
                        for idx_result in range(len(query_result))
                    )
                else:
                    example_result = (
                        f"{query_result[0][0]}" if query_result[0][0] else "NULL"
                    )
            except duckdb.ParserException as e:
                print(
                    f"Error for function '{func.name}', could not calculate example: '{example}'. Consider adding it via OVERRIDES'. {e}"
                )
        if '`' not in example_result:
            example_result = f"`{example_result}`"
        lines += f"| **Result** | {example_result} |\n"
    return lines


if __name__ == "__main__":
    main()
