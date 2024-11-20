---
github_directory: https://github.com/duckdb/duckdb/tree/main/extension/json
layout: docu
title: JSON Extension
---

The `json` extension is a loadable extension that implements SQL functions that are useful for reading values from existing JSON, and creating new JSON data.

## Installing and Loading

The `json` extension is shipped by default in DuckDB builds, otherwise, it will be transparently [autoloaded]({% link docs/archive/1.0/extensions/overview.md %}#autoloading-extensions) on first use.
If you would like to install and load it manually, run:

```sql
INSTALL json;
LOAD json;
```

## Example Uses

Read a JSON file from disk, auto-infer options:

```sql
SELECT * FROM 'todos.json';
```

`read_json` with custom options:

```sql
SELECT *
FROM read_json('todos.json',
               format = 'array',
               columns = {userId: 'UBIGINT',
                          id: 'UBIGINT',
                          title: 'VARCHAR',
                          completed: 'BOOLEAN'});
```

Write the result of a query to a JSON file:

```sql
COPY (SELECT * FROM todos) TO 'todos.json';
```

See more examples of loading JSON data on the [JSON data page]({% link docs/archive/1.0/data/json/overview.md %}#examples):

Create a table with a column for storing JSON data:

```sql
CREATE TABLE example (j JSON);
```

Insert JSON data into the table:

```sql
INSERT INTO example VALUES
    ('{ "family": "anatidae", "species": [ "duck", "goose", "swan", null ] }');
```

Retrieve the family key's value:

```sql
SELECT j.family FROM example;
```

```text
"anatidae"
```

Extract the family key's value with a JSONPath expression:

```sql
SELECT j->'$.family' FROM example;
```

```text
"anatidae"
```

Extract the family key's value with a JSONPath expression as a VARCHAR:

```sql
SELECT j->>'$.family' FROM example;
```

```text
anatidae
```

## JSON Type

The `json` extension makes use of the `JSON` logical type.
The `JSON` logical type is interpreted as JSON, i.e., parsed, in JSON functions rather than interpreted as `VARCHAR`, i.e., a regular string (modulo the equality-comparison caveat at the bottom of this page).
All JSON creation functions return values of this type.

We also allow any of DuckDB's types to be casted to JSON, and JSON to be casted back to any of DuckDB's types, for example, to cast `JSON` to DuckDB's `STRUCT` type, run:

```sql
SELECT '{"duck": 42}'::JSON::STRUCT(duck INTEGER);
```

```text
{'duck': 42}
```

And back:

```sql
SELECT {duck: 42}::JSON;
```

```text
{"duck":42}
```

This works for our nested types as shown in the example, but also for non-nested types:

```sql
SELECT '2023-05-12'::DATE::JSON;
```

```text
"2023-05-12"
```

The only exception to this behavior is the cast from `VARCHAR` to `JSON`, which does not alter the data, but instead parses and validates the contents of the `VARCHAR` as JSON.

## JSON Table Functions

The following table functions are used to read JSON:

| Function | Description |
|:---|:---|
| `read_json_objects(filename)`   | Read a JSON object from `filename`, where `filename` can also be a list of files or a glob pattern. |
| `read_ndjson_objects(filename)` | Alias for `read_json_objects` with parameter `format` set to `'newline_delimited'`. |
| `read_json_objects_auto(filename)` | Alias for `read_json_objects` with parameter `format` set to `'auto'`. |

These functions have the following parameters:

| Name | Description | Type | Default |
|:--|:-----|:-|:-|
| `compression` | The compression type for the file. By default this will be detected automatically from the file extension (e.g., `t.json.gz` will use gzip, `t.json` will use none). Options are `'none'`, `'gzip'`, `'zstd'`, and `'auto'`. | `VARCHAR` | `'auto'` |
| `filename` | Whether or not an extra `filename` column should be included in the result. | `BOOL` | `false` |
| `format` | Can be one of `['auto', 'unstructured', 'newline_delimited', 'array']`. | `VARCHAR` | `'array'` |
| `hive_partitioning` | Whether or not to interpret the path as a [Hive partitioned path]({% link docs/archive/1.0/data/partitioning/hive_partitioning.md %}). | `BOOL` | `false` |
| `ignore_errors` | Whether to ignore parse errors (only possible when `format` is `'newline_delimited'`). | `BOOL` | `false` |
| `maximum_sample_files` | The maximum number of JSON files sampled for auto-detection. | `BIGINT` | `32` |
| `maximum_object_size` | The maximum size of a JSON object (in bytes). | `UINTEGER` | `16777216` |

The `format` parameter specifies how to read the JSON from a file.
With `'unstructured'`, the top-level JSON is read, e.g.:

```json
{
  "duck": 42
}
{
  "goose": [1, 2, 3]
}
```

will result in two objects being read.

With `'newline_delimited'`, [NDJSON](https://github.com/ndjson/ndjson-spec) is read, where each JSON is separated by a newline (`\n`), e.g.:

```json
{"duck": 42}
{"goose": [1, 2, 3]}
```

will also result in two objects being read.

With `'array'`, each array element is read, e.g.:

```json
[
    {
        "duck": 42
    },
    {
        "goose": [1, 2, 3]
    }
]
```

Again, will result in two objects being read.

Example usage:

```sql
SELECT * FROM read_json_objects('my_file1.json');
```

```text
{"duck":42,"goose":[1,2,3]}
```

```sql
SELECT * FROM read_json_objects(['my_file1.json', 'my_file2.json']);
```

```text
{"duck":42,"goose":[1,2,3]}
{"duck":43,"goose":[4,5,6],"swan":3.3}
```

```sql
SELECT * FROM read_ndjson_objects('*.json.gz');
```

```text
{"duck":42,"goose":[1,2,3]}
{"duck":43,"goose":[4,5,6],"swan":3.3}
```

DuckDB also supports reading JSON as a table, using the following functions:

| Function | Description |
|:----|:-------|
| `read_json(filename)` | Read JSON from `filename`, where `filename` can also be a list of files, or a glob pattern. |
| `read_json_auto(filename)` | Alias for `read_json` with all auto-detection enabled. |
| `read_ndjson(filename)` | Alias for `read_json` with parameter `format` set to `'newline_delimited'`. |
| `read_ndjson_auto(filename)` | Alias for `read_json_auto` with parameter `format` set to `'newline_delimited'`. |

Besides the `maximum_object_size`, `format`, `ignore_errors` and `compression`, these functions have additional parameters:

| Name | Description | Type | Default |
|:--|:------|:-|:-|
| `auto_detect` | Whether to auto-detect the names of the keys and data types of the values automatically | `BOOL` | `false` |
| `columns` | A struct that specifies the key names and value types contained within the JSON file (e.g., `{key1: 'INTEGER', key2: 'VARCHAR'}`). If `auto_detect` is enabled these will be inferred | `STRUCT` | `(empty)` |
| `dateformat` | Specifies the date format to use when parsing dates. See [Date Format]({% link docs/archive/1.0/sql/functions/dateformat.md %}) | `VARCHAR` | `'iso'` |
| `maximum_depth` | Maximum nesting depth to which the automatic schema detection detects types. Set to -1 to fully detect nested JSON types | `BIGINT` | `-1` |
| `records` | Can be one of `['auto', 'true', 'false']` | `VARCHAR` | `'records'` |
| `sample_size` | Option to define number of sample objects for automatic JSON type detection. Set to -1 to scan the entire input file | `UBIGINT` | `20480` |
| `timestampformat` | Specifies the date format to use when parsing timestamps. See [Date Format]({% link docs/archive/1.0/sql/functions/dateformat.md %}) | `VARCHAR` | `'iso'`|
| `union_by_name` | Whether the schema's of multiple JSON files should be [unified]({% link docs/archive/1.0/data/multiple_files/combining_schemas.md %}) | `BOOL` | `false` |

Example usage:

```sql
SELECT * FROM read_json('my_file1.json', columns = {duck: 'INTEGER'});
```

<div class="narrow_table monospace_table"></div>

| duck |
|:---|
| 42 |

DuckDB can convert JSON arrays directly to its internal `LIST` type, and missing keys become `NULL`:

```sql
SELECT *
FROM read_json(
        ['my_file1.json', 'my_file2.json'],
        columns = {duck: 'INTEGER', goose: 'INTEGER[]', swan: 'DOUBLE'}
    );
```

<div class="narrow_table monospace_table"></div>

| duck | goose | swan |
|:---|:---|:---|
| 42 | [1, 2, 3] | NULL |
| 43 | [4, 5, 6] | 3.3 |

DuckDB can automatically detect the types like so:

```sql
SELECT goose, duck FROM read_json('*.json.gz');
SELECT goose, duck FROM '*.json.gz'; -- equivalent
```

<div class="narrow_table monospace_table"></div>

| goose | duck |
|:---|:---|
| [1, 2, 3] | 42 |
| [4, 5, 6] | 43 |

DuckDB can read (and auto-detect) a variety of formats, specified with the `format` parameter.
Querying a JSON file that contains an `'array'`, e.g.:

```json
[
  {
    "duck": 42,
    "goose": 4.2
  },
  {
    "duck": 43,
    "goose": 4.3
  }
]
```

Can be queried exactly the same as a JSON file that contains `'unstructured'` JSON, e.g.:

```json
{
    "duck": 42,
    "goose": 4.2
}
{
    "duck": 43,
    "goose": 4.3
}
```

Both can be read as the table:

<div class="narrow_table monospace_table"></div>

| duck | goose |
|:---|:---|
| 42 | 4.2 |
| 43 | 4.3 |

If your JSON file does not contain 'records', i.e., any other type of JSON than objects, DuckDB can still read it.
This is specified with the `records` parameter.
The `records` parameter specifies whether the JSON contains records that should be unpacked into individual columns, i.e., reading the following file with `records`:

```json
{"duck": 42, "goose": [1, 2, 3]}
{"duck": 43, "goose": [4, 5, 6]}
```

Results in two columns:

<div class="narrow_table monospace_table"></div>

| duck | goose |
|:---|:---|
| 42 | [1,2,3] |
| 42 | [4,5,6] |

You can read the same file with `records` set to `'false'`, to get a single column, which is a `STRUCT` containing the data:

<div class="narrow_table monospace_table"></div>

| json |
|:---|
| {'duck': 42, 'goose': [1,2,3]} |
| {'duck': 43, 'goose': [4,5,6]} |

For additional examples reading more complex data, please see the [“Shredding Deeply Nested JSON, One Vector at a Time” blog post]({% post_url 2023-03-03-json %}).

## JSON Import/Export

When the `json` extension is installed, `FORMAT JSON` is supported for `COPY FROM`, `COPY TO`, `EXPORT DATABASE` and `IMPORT DATABASE`. See [Copy]({% link docs/archive/1.0/sql/statements/copy.md %}) and [Import/Export]({% link docs/archive/1.0/sql/statements/export.md %}).

By default, `COPY` expects newline-delimited JSON. If you prefer copying data to/from a JSON array, you can specify `ARRAY true`, e.g.,

```sql
COPY (SELECT * FROM range(5)) TO 'my.json' (ARRAY true);
```

will create the following file:

```json
[
    {"range":0},
    {"range":1},
    {"range":2},
    {"range":3},
    {"range":4}
]
```

This can be read like so:

```sql
CREATE TABLE test (range BIGINT);
COPY test FROM 'my.json' (ARRAY true);
```

The format can be detected automatically the format like so:

```sql
COPY test FROM 'my.json' (AUTO_DETECT true);
```

## JSON Creation Functions

The following functions are used to create JSON.

<div class="narrow_table"></div>

| Function | Description |
|:--|:----|
| `to_json(any)` | Create `JSON` from a value of `any` type. Our `LIST` is converted to a JSON array, and our `STRUCT` and `MAP` are converted to a JSON object. |
| `json_quote(any)` | Alias for `to_json`. |
| `array_to_json(list)` | Alias for `to_json` that only accepts `LIST`. |
| `row_to_json(list)` | Alias for `to_json` that only accepts `STRUCT`. |
| `json_array([any, ...])` | Create a JSON array from `any` number of values. |
| `json_object([key, value, ...])` | Create a JSON object from any number of `key`, `value` pairs. |
| `json_merge_patch(json, json)` | Merge two JSON documents together. |

Examples:

```sql
SELECT to_json('duck');
```

```text
"duck"
```

```sql
SELECT to_json([1, 2, 3]);
```

```text
[1,2,3]
```

```sql
SELECT to_json({duck : 42});
```

```text
{"duck":42}
```

```sql
SELECT to_json(map(['duck'],[42]));
```

```text
{"duck":42}
```

```sql
SELECT json_array(42, 'duck', NULL);
```

```text
[42,"duck",null]
```

```sql
SELECT json_object('duck', 42);
```

```text
{"duck":42}
```

```sql
SELECT json_merge_patch('{"duck": 42}', '{"goose": 123}');
```

```text
{"goose":123,"duck":42}
```



## JSON Extraction Functions

There are two extraction functions, which have their respective operators. The operators can only be used if the string is stored as the `JSON` logical type.
These functions supports the same two location notations as the previous functions.

| Function | Alias | Operator | Description |
|:---|:---|:-|
| `json_extract(json, path)` | `json_extract_path` | `->` | Extract `JSON` from `json` at the given `path`. If `path` is a `LIST`, the result will be a `LIST` of `JSON` |
| `json_extract_string(json, path)` | `json_extract_path_text` | `->>` | Extract `VARCHAR` from `json` at the given `path`. If `path` is a `LIST`, the result will be a `LIST` of `VARCHAR` |

Note that the equality comparison operator (`=`) has a higher precedence than the `->` JSON extract operator. Therefore, surround the uses of the `->` operator with parentheses when making equality comparisons. For example:

```sql
SELECT ((JSON '{"field": 42}')->'field') = 42;
```

> Warning DuckDB's JSON data type uses [0-based indexing](#indexing).

Examples:

```sql
CREATE TABLE example (j JSON);
INSERT INTO example VALUES
    ('{ "family": "anatidae", "species": [ "duck", "goose", "swan", null ] }');
```

```sql
SELECT json_extract(j, '$.family') FROM example;
```

```text
"anatidae"
```

```sql
SELECT j->'$.family' FROM example;
```

```text
"anatidae"
```

```sql
SELECT j->'$.species[0]' FROM example;
```

```text
"duck"
```

```sql
SELECT j->'$.species[*]' FROM example;
```

```text
["duck", "goose", "swan", null]
```

```sql
SELECT j->>'$.species[*]' FROM example;
```

```text
[duck, goose, swan, null]
```

```sql
SELECT j->'$.species'->0 FROM example;
```

```text
"duck"
```

```sql
SELECT j->'species'->['0','1'] FROM example;
```

```text
["duck", "goose"]
```

```sql
SELECT json_extract_string(j, '$.family') FROM example;
```

```text
anatidae
```

```sql
SELECT j->>'$.family' FROM example;
```

```text
anatidae
```

```sql
SELECT j->>'$.species[0]' FROM example;
```

```text
duck
```

```sql
SELECT j->'species'->>0 FROM example;
```

```text
duck
```

```sql
SELECT j->'species'->>['0','1'] FROM example;
```

```text
[duck, goose]
```

Note that DuckDB's JSON data type uses [0-based indexing](#indexing).

If multiple values need to be extracted from the same JSON, it is more efficient to extract a list of paths:

The following will cause the JSON to be parsed twice,:

Resulting in a slower query that uses more memory:

```sql
SELECT
    json_extract(j, 'family') AS family,
    json_extract(j, 'species') AS species
FROM example;
```

<div class="narrow_table monospace_table"></div>

|   family   |           species            |
|------------|------------------------------|
| "anatidae" | ["duck","goose","swan",null] |

The following produces the same result but is faster and more memory-efficient:

```sql
WITH extracted AS (
    SELECT json_extract(j, ['family', 'species']) AS extracted_list
    FROM example
)
SELECT
    extracted_list[1] AS family,
    extracted_list[2] AS species
FROM extracted;
```

## JSON Scalar Functions

The following scalar JSON functions can be used to gain information about the stored JSON values.
With the exception of `json_valid(json)`, all JSON functions produce an error when invalid JSON is supplied.

We support two kinds of notations to describe locations within JSON: [JSON Pointer](https://datatracker.ietf.org/doc/html/rfc6901) and JSONPath.

| Function | Description |
|:---|:----|
| `json_array_length(json[, path])` | Return the number of elements in the JSON array `json`, or `0` if it is not a JSON array. If `path` is specified, return the number of elements in the JSON array at the given `path`. If `path` is a `LIST`, the result will be `LIST` of array lengths. |
| `json_contains(json_haystack, json_needle)` | Returns `true` if `json_needle` is contained in `json_haystack`. Both parameters are of JSON type, but `json_needle` can also be a numeric value or a string, however the string must be wrapped in double quotes. |
| `json_keys(json[, path])` | Returns the keys of `json` as a `LIST` of `VARCHAR`, if `json` is a JSON object. If `path` is specified, return the keys of the JSON object at the given `path`. If `path` is a `LIST`, the result will be `LIST` of `LIST` of `VARCHAR`. |
| `json_structure(json)` | Return the structure of `json`. Defaults to `JSON` if the structure is inconsistent (e.g., incompatible types in an array). |
| `json_type(json[, path])` | Return the type of the supplied `json`, which is one of `ARRAY`, `BIGINT`, `BOOLEAN`, `DOUBLE`, `OBJECT`, `UBIGINT`, `VARCHAR`, and `NULL`. If `path` is specified, return the type of the element at the given `path`. If `path` is a `LIST`, the result will be `LIST` of types. |
| `json_valid(json)` | Return whether `json` is valid JSON. |
| `json(json)` | Parse and minify `json`. |

The JSONPointer syntax separates each field with a `/`.
For example, to extract the first element of the array with key `duck`, you can do:

```sql
SELECT json_extract('{"duck": [1, 2, 3]}', '/duck/0');
```

```text
1
```

The JSONPath syntax separates fields with a `.`, and accesses array elements with `[i]`, and always starts with `$`. Using the same example, we can do the following:

```sql
SELECT json_extract('{"duck": [1, 2, 3]}', '$.duck[0]');
```

```text
1
```

Note that DuckDB's JSON data type uses [0-based indexing](#indexing).

JSONPath is more expressive, and can also access from the back of lists:

```sql
SELECT json_extract('{"duck": [1, 2, 3]}', '$.duck[#-1]');
```

```text
3
```

JSONPath also allows escaping syntax tokens, using double quotes:

```sql
SELECT json_extract('{"duck.goose": [1, 2, 3]}', '$."duck.goose"[1]');
```

```text
2
```

Examples using the [anatidae biological family](https://en.wikipedia.org/wiki/Anatidae):

```sql
CREATE TABLE example (j JSON);
INSERT INTO example VALUES
    ('{ "family": "anatidae", "species": [ "duck", "goose", "swan", null ] }');
```

```sql
SELECT json(j) FROM example;
```

```text
{"family":"anatidae","species":["duck","goose","swan",null]}
```

```sql
SELECT j.family FROM example;
```

```text
"anatidae"
```

```sql
SELECT j.species[0] FROM example;
```

```text
"duck"
```

```sql
SELECT json_valid(j) FROM example;
```

```text
true
```

```sql
SELECT json_valid('{');
```

```text
false
```

```sql
SELECT json_array_length('["duck", "goose", "swan", null]');
```

```text
4
```

```sql
SELECT json_array_length(j, 'species') FROM example;
```

```text
4
```

```sql
SELECT json_array_length(j, '/species') FROM example;
```

```text
4
```

```sql
SELECT json_array_length(j, '$.species') FROM example;
```

```text
4
```

```sql
SELECT json_array_length(j, ['$.species']) FROM example;
```

```text
[4]
```

```sql
SELECT json_type(j) FROM example;
```

```text
OBJECT
```

```sql
SELECT json_keys(j) FROM example;
```

```text
[family, species]
```

```sql
SELECT json_structure(j) FROM example;
```

```text
{"family":"VARCHAR","species":["VARCHAR"]}
```

```sql
SELECT json_structure('["duck", {"family": "anatidae"}]');
```

```text
["JSON"]
```

```sql
SELECT json_contains('{"key": "value"}', '"value"');
```

```text
true
```

```sql
SELECT json_contains('{"key": 1}', '1');
```

```text
true
```

```sql
SELECT json_contains('{"top_key": {"key": "value"}}', '{"key": "value"}');
```

```text
true
```

## JSON Aggregate Functions

There are three JSON aggregate functions.

<div class="narrow_table"></div>

| Function | Description |
|:---|:----|
| `json_group_array(any)` | Return a JSON array with all values of `any` in the aggregation. |
| `json_group_object(key, value)` | Return a JSON object with all `key`, `value` pairs in the aggregation. |
| `json_group_structure(json)` | Return the combined `json_structure` of all `json` in the aggregation. |

Examples:

```sql
CREATE TABLE example1 (k VARCHAR, v INTEGER);
INSERT INTO example1 VALUES ('duck', 42), ('goose', 7);
```

```sql
SELECT json_group_array(v) FROM example1;
```

```text
[42, 7]
```

```sql
SELECT json_group_object(k, v) FROM example1;
```

```text
{"duck":42,"goose":7}
```

```sql
CREATE TABLE example2 (j JSON);
INSERT INTO example2 VALUES
    ('{"family": "anatidae", "species": ["duck", "goose"], "coolness": 42.42}'),
    ('{"family": "canidae", "species": ["labrador", "bulldog"], "hair": true}');
```

```sql
SELECT json_group_structure(j) FROM example2;
```

```text
{"family":"VARCHAR","species":["VARCHAR"],"coolness":"DOUBLE","hair":"BOOLEAN"}
```

## Transforming JSON

In many cases, it is inefficient to extract values from JSON one-by-one.
Instead, we can “extract” all values at once, transforming JSON to the nested types `LIST` and `STRUCT`.

<div class="narrow_table"></div>

| Function | Description |
|:---|:---|
| `json_transform(json, structure)` | Transform `json` according to the specified `structure`. |
| `from_json(json, structure)` | Alias for `json_transform`. |
| `json_transform_strict(json, structure)` | Same as `json_transform`, but throws an error when type casting fails. |
| `from_json_strict(json, structure)` | Alias for `json_transform_strict`. |

The `structure` argument is JSON of the same form as returned by `json_structure`.
The `structure` argument can be modified to transform the JSON into the desired structure and types.
It is possible to extract fewer key/value pairs than are present in the JSON, and it is also possible to extract more: missing keys become `NULL`.

Examples:

```sql
CREATE TABLE example (j JSON);
INSERT INTO example VALUES
    ('{"family": "anatidae", "species": ["duck", "goose"], "coolness": 42.42}'),
    ('{"family": "canidae", "species": ["labrador", "bulldog"], "hair": true}');
```

```sql
SELECT json_transform(j, '{"family": "VARCHAR", "coolness": "DOUBLE"}') FROM example;
```

```text
{'family': anatidae, 'coolness': 42.420000}
{'family': canidae, 'coolness': NULL}
```

```sql
SELECT json_transform(j, '{"family": "TINYINT", "coolness": "DECIMAL(4, 2)"}') FROM example;
```

```text
{'family': NULL, 'coolness': 42.42}
{'family': NULL, 'coolness': NULL}
```

```sql
SELECT json_transform_strict(j, '{"family": "TINYINT", "coolness": "DOUBLE"}') FROM example;
```

```console
Invalid Input Error: Failed to cast value: "anatidae"
```

## Serializing and Deserializing SQL to JSON and Vice Versa

The `json` extension also provides functions to serialize and deserialize `SELECT` statements between SQL and JSON, as well as executing JSON serialized statements.

| Function | Type | Description |
|:------|:-|:---------|
| `json_deserialize_sql(json)` | Scalar  | Deserialize one or many `json` serialized statements back to an equivalent SQL string. |
| `json_execute_serialized_sql(varchar)` | Table | Execute `json` serialized statements and return the resulting rows. Only one statement at a time is supported for now. |
| `json_serialize_sql(varchar, skip_empty := boolean, skip_null := boolean, format := boolean)` | Scalar | Serialize a set of semicolon-separated (`;`) select statements to an equivalent list of `json` serialized statements. |
| `PRAGMA json_execute_serialized_sql(varchar)` | Pragma | Pragma version of the `json_execute_serialized_sql` function. |

The `json_serialize_sql(varchar)` function takes three optional parameters, `skip_empty`, `skip_null`, and `format` that can be used to control the output of the serialized statements.

If you run the `json_execute_serialize_sql(varchar)` table function inside of a transaction the serialized statements will not be able to see any transaction local changes. This is because the statements are executed in a separate query context. You can use the `PRAGMA json_execute_serialize_sql(varchar)` pragma version to execute the statements in the same query context as the pragma, although with the limitation that the serialized JSON must be provided as a constant string, i.e., you cannot do `PRAGMA json_execute_serialize_sql(json_serialize_sql(...))`.

Note that these functions do not preserve syntactic sugar such as `FROM * SELECT ...`, so a statement round-tripped through `json_deserialize_sql(json_serialize_sql(...))` may not be identical to the original statement, but should always be semantically equivalent and produce the same output.

Examples:

Simple example:

```sql
SELECT json_serialize_sql('SELECT 2');
```

```text
'{"error":false,"statements":[{"node":{"type":"SELECT_NODE","modifiers":[],"cte_map":{"map":[]},"select_list":[{"class":"CONSTANT","type":"VALUE_CONSTANT","alias":"","value":{"type":{"id":"INTEGER","type_info":null},"is_null":false,"value":2}}],"from_table":{"type":"EMPTY","alias":"","sample":null},"where_clause":null,"group_expressions":[],"group_sets":[],"aggregate_handling":"STANDARD_HANDLING","having":null,"sample":null,"qualify":null}}]}'
```

Example with multiple statements and skip options:

```sql
SELECT json_serialize_sql('SELECT 1 + 2; SELECT a + b FROM tbl1', skip_empty := true, skip_null := true);
```

```text
'{"error":false,"statements":[{"node":{"type":"SELECT_NODE","select_list":[{"class":"FUNCTION","type":"FUNCTION","function_name":"+","children":[{"class":"CONSTANT","type":"VALUE_CONSTANT","value":{"type":{"id":"INTEGER"},"is_null":false,"value":1}},{"class":"CONSTANT","type":"VALUE_CONSTANT","value":{"type":{"id":"INTEGER"},"is_null":false,"value":2}}],"order_bys":{"type":"ORDER_MODIFIER"},"distinct":false,"is_operator":true,"export_state":false}],"from_table":{"type":"EMPTY"},"aggregate_handling":"STANDARD_HANDLING"}},{"node":{"type":"SELECT_NODE","select_list":[{"class":"FUNCTION","type":"FUNCTION","function_name":"+","children":[{"class":"COLUMN_REF","type":"COLUMN_REF","column_names":["a"]},{"class":"COLUMN_REF","type":"COLUMN_REF","column_names":["b"]}],"order_bys":{"type":"ORDER_MODIFIER"},"distinct":false,"is_operator":true,"export_state":false}],"from_table":{"type":"BASE_TABLE","table_name":"tbl1"},"aggregate_handling":"STANDARD_HANDLING"}}]}'
```

Example with a syntax error:

```sql
SELECT json_serialize_sql('TOTALLY NOT VALID SQL');
```

```text
'{"error":true,"error_type":"parser","error_message":"syntax error at or near \"TOTALLY\"\nLINE 1: TOTALLY NOT VALID SQL\n        ^"}'
```

Example with deserialize:

```sql
SELECT json_deserialize_sql(json_serialize_sql('SELECT 1 + 2'));
```

```text
'SELECT (1 + 2)'
```

Example with deserialize and syntax sugar:

```sql
SELECT json_deserialize_sql(json_serialize_sql('FROM x SELECT 1 + 2'));
```

```text
'SELECT (1 + 2) FROM x'
```

Example with execute:

```sql
SELECT * FROM json_execute_serialized_sql(json_serialize_sql('SELECT 1 + 2'));
```

```text
3
```

Example with error:

```sql
SELECT * FROM json_execute_serialized_sql(json_serialize_sql('TOTALLY NOT VALID SQL'));
```

```console
Error: Parser Error: Error parsing json: parser: syntax error at or near "TOTALLY"
```

## Indexing

> Warning Following PostgreSQL's conventions, DuckDB uses 1-based indexing for [arrays]({% link docs/archive/1.0/sql/data_types/array.md %}) and [lists]({% link docs/archive/1.0/sql/data_types/list.md %}) but [0-based indexing for the JSON data type](https://www.postgresql.org/docs/16/functions-json.html#FUNCTIONS-JSON-PROCESSING).

## Equality Comparison

> Warning Currently, equality comparison of JSON files can differ based on the context. In some cases, it is based on raw text comparison, while in other cases, it uses logical content comparison.

The following query returns true for all fields:

```sql
SELECT
    a != b, -- Space is part of physical JSON content. Despite equal logical content, values are treated as not equal.
    c != d, -- Same.
    c[0] = d[0], -- Equality because space was removed from physical content of fields:
    a = c[0], -- Indeed, field is equal to empty list without space...
    b != c[0], -- ... but different from empty list with space.
FROM (
    SELECT
        '[]'::JSON AS a,
        '[ ]'::JSON AS b,
        '[[]]'::JSON AS c,
        '[[ ]]'::JSON AS d
    );
```

<div class="narrow_table monospace_table"></div>

| (a != b) | (c != d) | (c[0] = d[0]) | (a = c[0]) | (b != c[0]) |
|----------|----------|---------------|------------|-------------|
| true     | true     | true          | true       | true        |