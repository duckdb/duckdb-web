---
layout: docu
title: JSON
selected: Documentation/JSON
---
The __json__ extension is a loadable extension that implements SQL functions that are useful for reading values from existing JSON, and creating new JSON data.

## JSON Type
The JSON extension makes use of the **JSON** logical type.
The **JSON** logical type is interpreted as JSON, i.e., parsed, in JSON functions rather than interpreted as **VARCHAR**, i.e., a regular string.
All JSON creation functions return values of this type.

We also allow any of our types to be casted to JSON, and JSON to be casted back to any of our types, for example:
```sql
-- Cast JSON to our STRUCT type
SELECT '{"duck":42}'::JSON::STRUCT(duck INTEGER);
-- {'duck': 42}

-- And back:
SELECT {duck: 42}::JSON;
-- {"duck":42}
```

This works for our nested types as shown in the example, but also for non-nested types:
```sql
select '2023-05-12'::DATE::JSON;
-- "2023-05-12"
```

The only exception to this behavior is the cast from `VARCHAR` to `JSON`, which does not alter the data, but instead parses and validates the contents of the `VARCHAR` as JSON.

## JSON Table Functions
The following two table functions are used to read JSON:

| Function | Description |
|:---|:---|
| `read_json_objects(`*`filename`*`)`   | Read 1 JSON objects from **filename**, where **filename** can also be a list of files, or a glob pattern |
| `read_ndjson_objects(`*`filename`*`)` | Alias for `read_json_objects` with parameter **format** set to `'newline_delimited'` |
| `read_json_objects_auto(`*`filename`*`)` | Alias for `read_json_objects` with parameter **format** set to `'auto'` |

These functions have the following parameters:

| Name | Description | Type | Default
|:---|:---|:---|:---|
| `maximum_object_size` | The maximum size of a JSON object (in bytes) | uinteger | `16777216` |
| `format` | Can be one of `['auto', 'unstructured', 'newline_delimited', 'array']` | varchar | `'array'` |
| `ignore_errors` | Whether to ignore parse errors (only possible when `format` is `'newline_delimited'`) | bool | false |
| `compression` | The compression type for the file. By default this will be detected automatically from the file extension (e.g. **t.json.gz** will use gzip, **t.json** will use none). Options are `'none'`, `'gzip'`, `'zstd'`, and `'auto'`. | varchar | `'auto'` |
| `filename` | Whether or not an extra `filename` column should be included in the result. | bool | false |
| `hive_partitioning` | Whether or not to interpret the path as a [hive partitioned path](../data/partitioning/hive_partitioning). | bool | false |

The `format` parameter specifies how to read the JSON from a file.
With `'unstructured'`, the top-level JSON is read, e.g.:
```json
{
  "duck": 42
}
{
  "goose": [1,2,3]
}
```
Will result in two objects being read.

With `'newline_delimited'`, [NDJSON](http://ndjson.org) is read, where each JSON is separated by a newline (`\n`), e.g.:
```json
{"duck": 42}
{"goose": [1,2,3]}
```
Will also result in two objects being read.

With `'array'`, each array element is read, e.g.:
```json
[
  {
    "duck": 42
  },
  {
    "goose": [1,2,3]
  }
```
Again, will result in two objects being read.

Example usage:
```sql
SELECT * FROM read_json_objects('my_file1.json');
-- {"duck":42,"goose":[1,2,3]}
SELECT * FROM read_json_objects(['my_file1.json','my_file2.json']);
-- {"duck":42,"goose":[1,2,3]}
-- {"duck":43,"goose":[4,5,6],"swan":3.3}
SELECT * FROM read_ndjson_objects('*.json.gz');
-- {"duck":42,"goose":[1,2,3]}
-- {"duck":43,"goose":[4,5,6],"swan":3.3}
```

DuckDB also supports reading JSON as a table, using the following functions:

| Function | Description |
|:---|:---|
| `read_json(`*`filename`*`)`   | Read JSON from **filename**, where **filename** can also be a list of files, or a glob pattern |
| `read_ndjson(`*`filename`*`)` | Alias for `read_json` with parameter **format** set to `'newline_delimited'` |
| `read_json_auto(`*`filename`*`)`   | Alias for `read_json` with all auto-detection enabled |
| `read_ndjson_auto(`*`filename`*`)` | Alias for `read_json_auto` with parameter **format** set to `'newline_delimited'` |

Besides the `maximum_object_size`, `format`, `ignore_errors` and `compression`, these functions have additional parameters:

| Name | Description | Type | Default |
|:---|:---|:---|:---|
| `columns` | A struct that specifies the key names and value types contained within the JSON file (e.g. `{key1: 'INTEGER', key2: 'VARCHAR'}`). If `auto_detect` is enabled these will be inferred | struct | `(empty)` |
| `records` | Can be one of `['auto', 'true', 'false']` | varchar | `'records'` |
| `auto_detect` | Whether to auto-detect detect the names of the keys and data types of the values automatically | bool | `false` |
| `sample_size` | Option to define number of sample objects for automatic JSON type detection. Set to -1 to scan the entire input file | ubigint | `20480` |
| `maximum_depth` | Maximum nesting depth to which the automatic schema detection detects types. Set to -1 to fully detect nested JSON types | bigint | `-1` |
| `dateformat` | Specifies the date format to use when parsing dates. See [Date Format](../sql/functions/dateformat) | varchar | `'iso'` |
| `timestampformat` | Specifies the date format to use when parsing timestamps. See [Date Format](../sql/functions/dateformat) | varchar | `'iso'`|
| `union_by_name` | Whether the schema's of multiple JSON files should be [unified](../data/multiple_files/combining_schemas). | bool | false |

Example usage:
```sql
SELECT * FROM read_json('my_file1.json', columns={duck: 'INTEGER'});
```

| duck |
|:---|
| 42 |

DuckDB can convert JSON arrays directly to its internal `LIST` type, and missing keys become `NULL`.

```sql
SELECT *
FROM read_json(['my_file1.json','my_file2.json'],
               columns={duck: 'INTEGER', goose: 'INTEGER[]', swan: 'DOUBLE'});
```

| duck | goose | swan |
|:---|:---|:---|
| 42 | [1, 2, 3] | NULL |
| 43 | [4, 5, 6] | 3.3 |

DuckDB can automatically detect the types like so:
```sql
SELECT goose, duck FROM read_json_auto('*.json.gz');
SELECT goose, duck FROM '*.json.gz'; -- equivalent
```

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

| duck | goose |
|:---|:---|
| 42 | 4.2 |
| 43 | 4.3 |

If your JSON file does not contain 'records', i.e., any other type of JSON than objects, DuckDB can still read it.
This is specified with the `records` parameter.
The `records` parameter specifies whether the JSON contains records that should be unpacked into individual columns, i.e., reading the following file with `records`:
```json
{"duck": 42, "goose": [1,2,3]}
{"duck": 43, "goose": [4,5,6]}
```
Results in two columns:

| duck | goose |
|:---|:---|
| 42 | [1,2,3] |
| 42 | [4,5,6] |

You can read the same file with `records` set to `'false'`, to get a single column, which is a `STRUCT` containing the data:

| json |
|:---|
| {'duck': 42, 'goose': [1, 2, 3]} |
 |{'duck': 43, 'goose': [4, 5, 6]} |

For additional examples reading more complex data, please see the [Shredding Deeply Nested JSON, One Vector at a Time blog post](https://duckdb.org/2023/03/03/json.html).

## JSON Import/Export
When the JSON extension is installed, `FORMAT JSON` is supported for `COPY FROM`, `COPY TO`, `EXPORT DATABASE` and `IMPORT DATABASE`. See [Copy](../sql/statements/copy) and [Import/Export](../sql/statements/export).

By default, `COPY` expects newline-delimited JSON. If you prefer copying data to/from a JSON array, you can specify `ARRAY TRUE`, i.e.,
```sql
COPY (SELECT * FROM range(5)) TO 'my.json' (ARRAY TRUE);
```
Will create the following file:
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
COPY test FROM 'my.json' (ARRAY TRUE);
```

The format can be detected automatically the format like so:
```sql
COPY test FROM 'my.json' (AUTO_DETECT TRUE);
```

## JSON Scalar Functions
The following scalar JSON functions can be used to gain information about the stored JSON values.
With the exception of `json_valid(`*`json`*`)`, all JSON functions produce an error when invalid JSON is supplied.

We support two kinds of notations to describe locations within JSON: [JSON Pointer](https://datatracker.ietf.org/doc/html/rfc6901) and JSONPath.

| Function | Description |
|:---|:---|
| `json(`*`json`*`)` | Parse and minify *`json`* |
| `json_valid(`*`json`*`)` | Return whether *`json`* is valid JSON |
| `json_array_length(`*`json `*`[, `*`path`*`])` | Return the number of elements in the JSON array *`json`*, or `0` if it is not a JSON array. If *`path`* is specified, return the number of elements in the JSON array at the given *`path`*. If *`path`* is a **LIST**, the result will be **LIST** of array lengths |
| `json_type(`*`json `*`[, `*`path`*`])` | Return the type of the supplied *`json`*, which is one of **OBJECT**, **ARRAY**, **BIGINT**, **UBIGINT**, **VARCHAR**, **BOOLEAN**, **NULL**. If *`path`* is specified, return the type of the element at the given *`path`*. If *`path`* is a **LIST**, the result will be **LIST** of types |
| `json_keys(`*`json `*`[, `*`path`*`])` | Returns the keys of `json` as a **LIST** of **VARCHAR**, if `json` is a JSON object. If *`path`* is specified, return the keys of the JSON object at the given *`path`*. If *`path`* is a **LIST**, the result will be **LIST** of **LIST** of **VARCHAR** |
| `json_structure(`*`json`*`)` | Return the structure of *`json`*. Defaults to `JSON` the structure is inconsistent (e.g., incompatible types in an array) |
| `json_contains(`*`json_haystack`*`, `*`json_needle`*`)` | Returns `true` if *`json_needle`* is contained in *`json_haystack`*. Both parameters are of JSON type, but *`json_needle`* can also be a numeric value or a string, however the string must be wrapped in double quotes |

The JSONPointer syntax separates each field with a `/`.
For example, to extract the first element of the array with key `"duck"`, you can do:
```sql
SELECT json_extract('{"duck":[1,2,3]}', '/duck/0');
-- 1
```

The JSONPath syntax separates fields with a `.`, and accesses array elements with `[i]`, and always starts with `$`. Using the same example, we can do:
```sql
SELECT json_extract('{"duck":[1,2,3]}', '$.duck[0]');
-- 1
```

JSONPath is more expressive, and can also access from the back of lists:
```sql
SELECT json_extract('{"duck":[1,2,3]}', '$.duck[#-1]');
-- 3
```

JSONPath also allows escaping syntax tokens, using double quotes:
```sql
SELECT json_extract('{"duck.goose":[1,2,3]}', '$."duck.goose"[1]');
-- 2
```

Other examples:
```sql
CREATE TABLE example (j JSON);
INSERT INTO example VALUES
  (' { "family": "anatidae", "species": [ "duck", "goose", "swan", null ] }');
SELECT json(j) FROM example;
-- {"family":"anatidae","species":["duck","goose","swan",null]}
SELECT json_valid(j) FROM example;
-- true
SELECT json_valid('{');
-- false
SELECT json_array_length('["duck","goose","swan",null]');
-- 4
SELECT json_array_length(j, 'species') FROM example;
-- 4
SELECT json_array_length(j, '/species') FROM example;
-- 4
SELECT json_array_length(j, '$.species') FROM example;
-- 4
SELECT json_array_length(j, ['$.species']) FROM example;
-- [4]
SELECT json_type(j) FROM example;
-- OBJECT
SELECT json_keys FROM example;
-- [family, species]
SELECT json_structure(j) FROM example;
-- {"family":"VARCHAR","species":["VARCHAR"]}
SELECT json_structure('["duck",{"family":"anatidae"}]');
-- ["JSON"]
SELECT json_contains('{"key":"value"}', '"value"');
-- true
SELECT json_contains('{"key":1}', 1);
-- true
SELECT json_contains('{"top_key":{"key":"value"}}', '{"key":"value"}');
-- true
```

## JSON Extraction Functions
There are two extraction functions, which have their respective operators. The operators can only be used if the string is stored as the **JSON** logical type.
These functions supports the same two location notations as the previous functions.

| Function | Alias | Operator | Description |
|:---|:---|:---|
| `json_extract(`*`json`*`,`*`path`*`)` | `json_extract_path` | `->` | Extract **JSON** from *`json`* at the given *`path`*. If *`path`* is a **LIST**, the result will be a **LIST** of **JSON** |
| `json_extract_string(`*`json`*`,`*`path`*`)` | `json_extract_path_text` | `->>` | Extract **VARCHAR** from *`json`* at the given *`path`*. If *`path`* is a **LIST**, the result will be a **LIST** of **VARCHAR** |

Examples:
```sql
CREATE TABLE example (j JSON);
INSERT INTO example VALUES
  (' { "family": "anatidae", "species": [ "duck", "goose", "swan", null ] }');
SELECT json_extract(j, '$.family') FROM example;
-- "anatidae"
SELECT j->'$.family' FROM example;
-- "anatidae"
SELECT j->'$.species[0]' FROM example;
-- "duck"
SELECT j->'$.species'->0 FROM example;
-- "duck"
SELECT j->'species'->>[0,1] FROM example;
-- ["duck", "goose"]
SELECT json_extract_string(j, '$.family') FROM example;
-- anatidae
SELECT j->>'$.family' FROM example;
-- anatidae
SELECT j->>'$.species[0]' FROM example;
-- duck
SELECT j->'species'->>0 FROM example;
-- duck
SELECT j->'species'->>[0,1] FROM example;
-- [duck, goose]
```

## JSON Creation Functions
The following functions are used to create JSON.

| Function | Description |
|:---|:---|
| `to_json(`*`any`*`)` | Create **JSON** from a value of *`any`* type. Our **LIST** is converted to a JSON array, and our **STRUCT** and **MAP** are converted to a JSON object |
| `json_quote(`*`any`*`)` | Alias for `to_json` |
| `array_to_json(`*`list`*`)` | Alias for `to_json` that only accepts **LIST** |
| `row_to_json(`*`list`*`)` | Alias for `to_json` that only accepts **STRUCT** |
| `json_array([`*`any`*`, ...])` | Create a JSON array from *`any`* number of values |
| `json_object([`*`key`*`,`*`value`*`, ...])` | Create a JSON object from any number of *`key`*, *`value`* pairs |
| `json_merge_patch(`*`json`*`,`*`json`*`)` | Merge two json documents together |

Examples:
```sql
SELECT to_json('duck');
-- "duck"
SELECT to_json([1, 2, 3]);
-- [1,2,3]
SELECT to_json({duck : 42});
-- {"duck":42}
SELECT to_json(map(['duck'],[42]));
-- {"duck":42}
SELECT json_array(42, 'duck', NULL);
-- [42,"duck",null]
SELECT json_object('duck', 42);
-- {"duck":42}
SELECT json_merge_patch('{"duck": 42}', '{"goose": 123}');
-- {"goose":123,"duck":42}
```

## JSON Aggregate Functions
There are three JSON aggregate functions.

| Function | Description |
|:---|:---|
| `json_group_array(`*`any`*`)` | Return a JSON array with all values of *`any`* in the aggregation |
| `json_group_object(`*`key`*`, `*`value`*`)` | Return a JSON object with all *`key`*, *`value`* pairs in the aggregation |
| `json_group_structure(`*`json`*`)` | Return the combined `json_structure` of all *`json`* in the aggregation |

Examples:
```sql
CREATE TABLE example (k VARCHAR, v INTEGER);
INSERT INTO example VALUES ('duck', 42), ('goose', 7);
SELECT json_group_array(v) FROM example;
-- [42, 7]
SELECT json_group_object(k, v) FROM example;
-- {"duck":42,"goose":7}
DROP TABLE example;
CREATE TABLE example (j JSON);
INSERT INTO example VALUES
  ('{"family": "anatidae", "species": ["duck", "goose"], "coolness": 42.42}'),
  ('{"family": "canidae", "species": ["labrador", "bulldog"], "hair": true}');
SELECT json_group_structure(j) FROM example;
-- {"family":"VARCHAR","species":["VARCHAR"],"coolness":"DOUBLE","hair":"BOOLEAN"}
```

## Transforming JSON
In many cases, it is inefficient to extract values from JSON one-by-one.
Instead, we can "extract" all values at once, transforming JSON to the nested types **LIST** and **STRUCT**.

| Function | Description |
|:---|:---|
| `json_transform(`*`json`*`, `*`structure`*`)` | Transform *`json`* according to the specified *`structure`* |
| `from_json(`*`json`*`, `*`structure`*`)` | Alias for `json_transform` |
| `json_transform_strict(`*`json`*`, `*`structure`*`)` | Same as `json_transform`, but throws an error when type casting fails |
| `from_json_strict(`*`json`*`, `*`structure`*`)` | Alias for `json_transform_strict` |

The *`structure`* argument is JSON of the same form as returned by `json_structure`.
The *`structure`* argument can be modified to transform the JSON into the desired structure and types.
It is possible to extract fewer key/value pairs than are present in the JSON, and it is also possible to extract more: missing keys become **NULL**.

Examples:
```sql
CREATE TABLE example (j JSON);
INSERT INTO example VALUES
  ('{"family": "anatidae", "species": ["duck", "goose"], "coolness": 42.42}'),
  ('{"family": "canidae", "species": ["labrador", "bulldog"], "hair": true}');
SELECT json_transform(j, '{"family":"VARCHAR","coolness":"DOUBLE"}') FROM example;
-- {'family': anatidae, 'coolness': 42.420000}
-- {'family': canidae, 'coolness': NULL}
SELECT json_transform(j, '{"family":"TINYINT","coolness":"DECIMAL(4,2)"}') FROM example;
-- {'family': NULL, 'coolness': 42.42}
-- {'family': NULL, 'coolness': NULL}
SELECT json_transform_strict(j, '{"family":"TINYINT","coolness":"DOUBLE"}') FROM example;
-- Invalid Input Error: Failed to cast value: "anatidae"
```

## De/Serializing SQL to JSON and vice versa
The JSON extension also provides functions to serialize and deserialize `SELECT` statements between SQL and JSON, as well as executing JSON serialized statements.

| Function | Type | Description |
|:---|:---|:---|
| `json_serialize_sql(`*`varchar`*`, skip_empty := `*`boolean`*`, skip_null := `*`boolean`*`, format := `*`boolean`*`)` | Scalar | Serialize a set of `;` separated select statments to an equivalent list of *`json`* serialized statements |
| `json_deserialize_sql(`*`json`*`)` | Scalar  | Deserialize one or many *`json`* serialized statements back to an equivalent sql string |
| `json_execute_serialized_sql(`*`varchar`*`)` | Table | Execute *`json`* serialized statements and return the resulting rows. Only one statement at a time is supported for now. |
| `PRAGMA json_execute_serialized_sql(`*`varchar`*`)` | Pragma | Pragma version of the `json_execute_serialized_sql` function. |

The `json_serialize_sql(varchar)` function takes three optional parameters, `skip_empty`, `skip_null`, and `format` that can be used to control the output of the serialized statements.

If you run the `json_execute_serialize_sql(varchar)` table function inside of a transaction the serialized statements will not be able to see any transaction local changes. This is because the statements are executed in a separate query context. You can use the `PRAGMA json_execute_serialize_sql(varchar)` pragma version to execute the statements in the same query context as the pragma, although with the limitation that the serialized json must be provided as a constant string. I.E. you cannot do `PRAGMA json_execute_serialize_sql(json_serialize_sql(...))`.

Note that these functions do not preserve syntactic sugar such as `FROM * SELECT ...`, so a statement round-tripped through `json_deserialize_sql(json_serialize_sql(...))` may not be identical to the original statement, but should always be semantically equivalent and produce the same output.

Examples:
```sql
-- Simple example
SELECT json_serialize_sql('SELECT 2');
-- '{"error":false,"statements":[{"node":{"type":"SELECT_NODE","modifiers":[],"cte_map":{"map":[]},"select_list":[{"class":"CONSTANT","type":"VALUE_CONSTANT","alias":"","value":{"type":{"id":"INTEGER","type_info":null},"is_null":false,"value":2}}],"from_table":{"type":"EMPTY","alias":"","sample":null},"where_clause":null,"group_expressions":[],"group_sets":[],"aggregate_handling":"STANDARD_HANDLING","having":null,"sample":null,"qualify":null}}]}'

-- Example with multiple statements and skip options
SELECT json_serialize_sql('SELECT 1 + 2; SELECT a + b FROM tbl1', skip_empty := true, skip_null := true);
-- '{"error":false,"statements":[{"node":{"type":"SELECT_NODE","select_list":[{"class":"FUNCTION","type":"FUNCTION","function_name":"+","children":[{"class":"CONSTANT","type":"VALUE_CONSTANT","value":{"type":{"id":"INTEGER"},"is_null":false,"value":1}},{"class":"CONSTANT","type":"VALUE_CONSTANT","value":{"type":{"id":"INTEGER"},"is_null":false,"value":2}}],"order_bys":{"type":"ORDER_MODIFIER"},"distinct":false,"is_operator":true,"export_state":false}],"from_table":{"type":"EMPTY"},"aggregate_handling":"STANDARD_HANDLING"}},{"node":{"type":"SELECT_NODE","select_list":[{"class":"FUNCTION","type":"FUNCTION","function_name":"+","children":[{"class":"COLUMN_REF","type":"COLUMN_REF","column_names":["a"]},{"class":"COLUMN_REF","type":"COLUMN_REF","column_names":["b"]}],"order_bys":{"type":"ORDER_MODIFIER"},"distinct":false,"is_operator":true,"export_state":false}],"from_table":{"type":"BASE_TABLE","table_name":"tbl1"},"aggregate_handling":"STANDARD_HANDLING"}}]}'

-- Example with a syntax error
SELECT json_serialize_sql('TOTALLY NOT VALID SQL');
-- '{"error":true,"error_type":"parser","error_message":"syntax error at or near \"TOTALLY\"\nLINE 1: TOTALLY NOT VALID SQL\n        ^"}'

-- Example with deserialize
SELECT json_deserialize_sql(json_serialize_sql('SELECT 1 + 2'));
-- 'SELECT (1 + 2)'

-- Example with deserialize and syntax sugar
SELECT json_deserialize_sql(json_serialize_sql('FROM x SELECT 1 + 2'));
-- 'SELECT (1 + 2) FROM x'

-- Example with execute
SELECT * FROM json_execute_serialized_sql(json_serialize_sql('SELECT 1 + 2'));
-- 3

-- Example with error
SELECT * FROM json_execute_serialized_sql(json_serialize_sql('TOTALLY NOT VALID SQL'));
-- Error: Parser Error: Error parsing json: parser: syntax error at or near "TOTALLY"
```
