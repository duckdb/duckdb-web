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

## JSON Table Functions
The following two table functions are used to read JSON:

| Function | Description |
|:---|:---|
| `read_json_objects(`*`filename`*`)`   | Read 1 JSON objects from **filename**, where **filename** can be list of files, or a glob pattern |
| `read_ndjson_objects(`*`filename`*`)` | Alias for `read_json_objects` with parameter **lines** set to `'true'` |

These functions have the following parameters:

| Name | Description | Type | Default
|:---|:---|:---|:---|
| `maximum_object_size` | The maximum size of a JSON object (in bytes) | uinteger | `1048576` |
| `lines` | When set to `'true` only newline-delimited JSON can be read, which can be read in parallel, When set to `'false'`, pretty-printed JSON can be read. Set to `'auto'` to automatically detect | varchar | `'false'` |
| `ignore_errors` | Whether to ignore parse errors (only possible when `lines` is `'true'`) | bool | false |
| `compression` | The compression type for the file. By default this will be detected automatically from the file extension (e.g. **t.json.gz** will use gzip, **t.json** will use none). Options are `'none'`, `'gzip'`, `'zstd'`, and `'auto'`. | varchar | `'auto'` |

Examples:
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
| `read_json(`*`filename`*`)`   | Read JSON from **filename**, where **filename** can be list of files, or a glob pattern |
| `read_ndjson(`*`filename`*`)` | Alias for `read_json` with parameter **lines** set to `'true'` |
| `read_json_auto(`*`filename`*`)`   | Read 1 json objects from **filename**, where **filename** can be list of files, or a glob pattern |
| `read_ndjson_auto(`*`filename`*`)` | Alias for `read_json_auto` with parameter **lines** set to `'true'` |

Besides the `maximum_object_size`, `lines`, `ignore_errors` and `compression`, these functions have additional parameters:

| Name | Description | Type | Default |
|:---|:---|:---|:---|
| `columns` | A struct that specifies the key names and value types contained within the JSON file (e.g. `{key1: 'INTEGER', key2: 'VARCHAR'}`). If `auto_detect` is enabled these will be inferred | struct | `(empty)` |
| `json_format` | Can be one of `['auto', 'records', 'array_of_records', 'values', 'array_of_values']` | varchar | `'records'` |
| `auto_detect` | Whether to auto-detect detect the names of the keys and data types of the values automatically | bool | `false` |
| `sample_size` | Option to define number of sample objects for automatic JSON type detection. Set to -1 to scan the entire input file | ubigint | `2048` |
| `maximum_depth` | Maximum nesting depth to which the automatic schema detection detects types. Set to -1 to fully detect nested JSON types | bigint | `-1` |
| `dateformat` | Specifies the date format to use when parsing dates. See [Date Format](../sql/functions/dateformat) | varchar | `'iso'` |
| `timestampformat` | Specifies the date format to use when parsing timestamps. See [Date Format](../sql/functions/dateformat) | varchar | `'iso'`|

Examples:
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

DuckDB can read (and auto-detect) a variety of formats, specified with the `json_format` parameter.
Querying a JSON file that contains an `'array_of_records'`, e.g.:
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
Can be queried exactly the same as a JSON file that contains `'records'`, e.g.:
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

Note that the `lines` parameter is independent of `json_format`, i.e., any JSON format can be either pretty-printed or newline-delimited.

If your JSON file does not contain 'records', i.e., any other type of JSON than objects, DuckDB can still read it.
Considered the following two JSON files:
```json
[1, 2, 3]
[4, 5, 6]
```
And similarly:
```json
[
  [1, 2, 3],
  [4, 5, 6]
]
```
By reading the first example with `json_format='values'` and the second example with `json_format='array_of_values'`, you will get the same result:

| json |
|:---|
| [1, 2, 3] |
| [4, 5, 6] |

## JSON Import/Export
When the JSON extension is installed, `FORMAT JSON` is supported for `COPY FROM`, `COPY TO`, `EXPORT DATABASE` and `IMPORT DATABASE`. See [Copy](../sql/statements/copy) and [Import/Export](../sql/statements/export).

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
| `json_structure(`*`json`*`)` | Return the structure of *`json`*. Throws an error if the structure is inconsistent (incompatible types in an array) |
| `json_contains(`*`json_haystack`*`, `*`json_needle`*`)` | Returns `true` if *`json_needle`* is contained in *`json_haystack`*. Both parameters are of JSON type, but *`json_needle`* can also be a numeric value or a string, however the string must be wrapped in double quotes |

Examples:
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
-- Invalid Input Error: Inconsistent JSON structure
SELECT json_contains('{"key":"value"}','"value"');
-- true
SELECT json_contains('{"key":1}',1);
-- true
SELECT json_contains('{"top_key":{"key":"value"}}','{"key":"value"}');
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
