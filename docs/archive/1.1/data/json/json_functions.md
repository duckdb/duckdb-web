---
layout: docu
title: JSON Processing Functions
---

## JSON Extraction Functions

There are two extraction functions, which have their respective operators. The operators can only be used if the string is stored as the `JSON` logical type.
These functions supports the same two location notations as [JSON Scalar functions](#json-scalar-functions).

| Function | Alias | Operator | Description |
|:---|:---|:-|
| `json_exists(json, path)` | | | Returns `true` if the supplied path exists in the `json`, and `false` otherwise. |
| `json_extract(json, path)` | `json_extract_path` | `->` | Extracts `JSON` from `json` at the given `path`. If `path` is a `LIST`, the result will be a `LIST` of `JSON`. |
| `json_extract_string(json, path)` | `json_extract_path_text` | `->>` | Extracts `VARCHAR` from `json` at the given `path`. If `path` is a `LIST`, the result will be a `LIST` of `VARCHAR`. |
| `json_value(json, path)` | | | Extracts `JSON` from `json` at the given `path`. If the `json` at the supplied path is not a scalar value, it will return `NULL`. |

Note that the arrow operator `->`, which is used for JSON extracts, has a low precedence as it is also used in [lambda functions]({% link docs/archive/1.1/sql/functions/lambda.md %}).

Therefore, you need to surround the `->` operator with parentheses when expressing operations such as equality comparisons (`=`).
For example:

```sql
SELECT ((JSON '{"field": 42}')->'field') = 42;
```

> Warning DuckDB's JSON data type uses [0-based indexing]({% link docs/archive/1.1/data/json/overview.md %}#indexing).

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

Note that DuckDB's JSON data type uses [0-based indexing]({% link docs/archive/1.1/data/json/overview.md %}#indexing).

If multiple values need to be extracted from the same JSON, it is more efficient to extract a list of paths:

The following will cause the JSON to be parsed twice,:

Resulting in a slower query that uses more memory:

```sql
SELECT
    json_extract(j, 'family') AS family,
    json_extract(j, 'species') AS species
FROM example;
```

<div class="monospace_table"></div>

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

Note that DuckDB's JSON data type uses [0-based indexing]({% link docs/archive/1.1/data/json/overview.md %}#indexing).

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

## Transforming JSON to Nested Types

In many cases, it is inefficient to extract values from JSON one-by-one.
Instead, we can “extract” all values at once, transforming JSON to the nested types `LIST` and `STRUCT`.

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