---
layout: docu
redirect_from:
- /docs/data/json/loading_json
title: Loading JSON
---

The DuckDB JSON reader can automatically infer which configuration flags to use by analyzing the JSON file. This will work correctly in most situations, and should be the first option attempted. In rare situations where the JSON reader cannot figure out the correct configuration, it is possible to manually configure the JSON reader to correctly parse the JSON file.

## The `read_json` Function

The `read_json` is the simplest method of loading JSON files: it automatically attempts to figure out the correct configuration of the JSON reader. It also automatically deduces types of columns.
In the following example, we use the [`todos.json`]({% link data/json/todos.json %}) file,

```sql
SELECT *
FROM read_json('todos.json')
LIMIT 5;
```

| userId | id |                              title                              | completed |
|-------:|---:|-----------------------------------------------------------------|-----------|
| 1      | 1  | delectus aut autem                                              | false     |
| 1      | 2  | quis ut nam facilis et officia qui                              | false     |
| 1      | 3  | fugiat veniam minus                                             | false     |
| 1      | 4  | et porro tempora                                                | true      |
| 1      | 5  | laboriosam mollitia et enim quasi adipisci quia provident illum | false     |

We can use `read_json` to create a persistent table as well:

```sql
CREATE TABLE todos AS
    SELECT *
    FROM read_json('todos.json');
DESCRIBE todos;
```

<div class="monospace_table"></div>

| column_name | column_type | null | key  | default | extra |
|-------------|-------------|------|------|---------|-------|
| userId      | UBIGINT     | YES  | NULL | NULL    | NULL  |
| id          | UBIGINT     | YES  | NULL | NULL    | NULL  |
| title       | VARCHAR     | YES  | NULL | NULL    | NULL  |
| completed   | BOOLEAN     | YES  | NULL | NULL    | NULL  |

If we specify types for a subset of columns, `read_json` excludes columns that we don't specify:

```sql
SELECT *
FROM read_json(
        'todos.json',
        columns = {userId: 'UBIGINT', completed: 'BOOLEAN'}
    )
LIMIT 5;
```

Note that only the `userId` and `completed` columns are shown:

| userId | completed |
|-------:|----------:|
| 1      | false     |
| 1      | false     |
| 1      | false     |
| 1      | true      |
| 1      | false     |

Multiple files can be read at once by providing a glob or a list of files. Refer to the [multiple files section]({% link docs/stable/data/multiple_files/overview.md %}) for more information.

## Functions for Reading JSON Objects

The following table functions are used to read JSON:

| Function | Description |
|:---|:---|
| `read_json_objects(filename)`      | Read a JSON object from `filename`, where `filename` can also be a list of files or a glob pattern. |
| `read_ndjson_objects(filename)`    | Alias for `read_json_objects` with the parameter `format` set to `newline_delimited`. |
| `read_json_objects_auto(filename)` | Alias for `read_json_objects` with the parameter `format` set to `auto` . |

### Parameters

These functions have the following parameters:

| Name | Description | Type | Default |
|:--|:-----|:-|:-|
| `compression` | The compression type for the file. By default this will be detected automatically from the file extension (e.g., `t.json.gz` will use gzip, `t.json` will use none). Options are `none`, `gzip`, `zstd` and `auto_detect`. | `VARCHAR` | `auto_detect` |
| `filename` | Whether or not an extra `filename` column should be included in the result. Since DuckDB v1.3.0, the `filename` column is added automatically as a virtual column and this option is only kept for compatibility reasons. | `BOOL` | `false` |
| `format` | Can be one of `auto`, `unstructured`, `newline_delimited` and `array`. | `VARCHAR` | `array` |
| `hive_partitioning` | Whether or not to interpret the path as a [Hive partitioned path]({% link docs/stable/data/partitioning/hive_partitioning.md %}). | `BOOL` | (auto-detected) |
| `ignore_errors` | Whether to ignore parse errors (only possible when `format` is `newline_delimited`). | `BOOL` | `false` |
| `maximum_sample_files` | The maximum number of JSON files sampled for auto-detection. | `BIGINT` | `32` |
| `maximum_object_size` | The maximum size of a JSON object (in bytes). | `UINTEGER` | `16777216` |

The `format` parameter specifies how to read the JSON from a file.
With `unstructured`, the top-level JSON is read, e.g., for `birds.json`:

```json
{
  "duck": 42
}
{
  "goose": [1, 2, 3]
}
```

```sql
FROM read_json_objects('birds.json', format = 'unstructured');
```

will result in two objects being read:

```text
┌──────────────────────────────┐
│             json             │
│             json             │
├──────────────────────────────┤
│ {\n    "duck": 42\n}         │
│ {\n    "goose": [1, 2, 3]\n} │
└──────────────────────────────┘
```

With `newline_delimited`, [NDJSON](https://github.com/ndjson/ndjson-spec) is read, where each JSON is separated by a newline (`\n`), e.g., for `birds-nd.json`:

```json
{"duck": 42}
{"goose": [1, 2, 3]}
```

```sql
FROM read_json_objects('birds-nd.json', format = 'newline_delimited');
```

will also result in two objects being read:

```text
┌──────────────────────┐
│         json         │
│         json         │
├──────────────────────┤
│ {"duck": 42}         │
│ {"goose": [1, 2, 3]} │
└──────────────────────┘
```

With `array`, each array element is read, e.g., for `birds-array.json`:

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

```sql
FROM read_json_objects('birds-array.json', format = 'array');
```

will again result in two objects being read:

```text
┌──────────────────────────────────────┐
│                 json                 │
│                 json                 │
├──────────────────────────────────────┤
│ {\n        "duck": 42\n    }         │
│ {\n        "goose": [1, 2, 3]\n    } │
└──────────────────────────────────────┘
```

## Functions for Reading JSON as a Table

DuckDB also supports reading JSON as a table, using the following functions:

| Function | Description     |
|:---------|:----------------|
| `read_json(filename)`        | Read JSON from `filename`, where `filename` can also be a list of files, or a glob pattern. |
| `read_json_auto(filename)`   | Alias for `read_json`.                                                                      |
| `read_ndjson(filename)`      | Alias for `read_json` with parameter `format` set to `newline_delimited`.                 |
| `read_ndjson_auto(filename)` | Alias for `read_json` with parameter `format` set to `newline_delimited`.                 |

### Parameters

Besides the `maximum_object_size`, `format`, `ignore_errors` and `compression`, these functions have additional parameters:

| Name | Description | Type | Default |
|:--|:------|:-|:-|
| `auto_detect` | Whether to auto-detect the names of the keys and data types of the values automatically | `BOOL` | `true` |
| `columns` | A struct that specifies the key names and value types contained within the JSON file (e.g., `{key1: 'INTEGER', key2: 'VARCHAR'}`). If `auto_detect` is enabled these will be inferred | `STRUCT` | `(empty)` |
| `dateformat` | Specifies the date format to use when parsing dates. See [Date Format]({% link docs/stable/sql/functions/dateformat.md %}) | `VARCHAR` | `iso` |
| `maximum_depth` | Maximum nesting depth to which the automatic schema detection detects types. Set to -1 to fully detect nested JSON types | `BIGINT` | `-1` |
| `records` | Can be one of `auto`, `true`, `false` | `VARCHAR` | `auto` |
| `sample_size` | Option to define number of sample objects for automatic JSON type detection. Set to -1 to scan the entire input file | `UBIGINT` | `20480` |
| `timestampformat` | Specifies the date format to use when parsing timestamps. See [Date Format]({% link docs/stable/sql/functions/dateformat.md %}) | `VARCHAR` | `iso`|
| `union_by_name` | Whether the schema's of multiple JSON files should be [unified]({% link docs/stable/data/multiple_files/combining_schemas.md %}) | `BOOL` | `false` |
| `map_inference_threshold` | Controls the threshold for number of columns whose schema will be auto-detected; if JSON schema auto-detection would infer a `STRUCT` type for a field that has _more_ than this threshold number of subfields, it infers a `MAP` type instead. Set to `-1` to disable `MAP` inference. | `BIGINT` | `200` |
| `field_appearance_threshold` | The JSON reader divides the number of appearances of each JSON field by the auto-detection sample size. If the average over the fields of an object is less than this threshold, it will default to using a `MAP` type with value type of merged field types. | `DOUBLE` | `0.1` |

Note that DuckDB can convert JSON arrays directly to its internal `LIST` type, and missing keys become `NULL`:

```sql
SELECT *
FROM read_json(
    ['birds1.json', 'birds2.json'],
    columns = {duck: 'INTEGER', goose: 'INTEGER[]', swan: 'DOUBLE'}
);
```

<div class="monospace_table"></div>

| duck |   goose   | swan |
|-----:|-----------|-----:|
| 42   | [1, 2, 3] | NULL |
| 43   | [4, 5, 6] | 3.3  |

DuckDB can automatically detect the types like so:

```sql
SELECT goose, duck FROM read_json('*.json.gz');
SELECT goose, duck FROM '*.json.gz'; -- equivalent
```

DuckDB can read (and auto-detect) a variety of formats, specified with the `format` parameter.
Querying a JSON file that contains an `array`, e.g.:

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

Can be queried exactly the same as a JSON file that contains `unstructured` JSON, e.g.:

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

```sql
SELECT
FROM read_json('birds.json');
```

<div class="monospace_table"></div>

| duck | goose |
|-----:|------:|
|   42 |   4.2 |
|   43 |   4.3 |

If your JSON file does not contain “records”, i.e., any other type of JSON than objects, DuckDB can still read it.
This is specified with the `records` parameter.
The `records` parameter specifies whether the JSON contains records that should be unpacked into individual columns.
DuckDB also attempts to auto-detect this.
For example, take the following file, `birds-records.json`:

```json
{"duck": 42, "goose": [1, 2, 3]}
{"duck": 43, "goose": [4, 5, 6]}
```

```sql
SELECT *
FROM read_json('birds-records.json');
```

The query results in two columns:

<div class="monospace_table"></div>

| duck | goose   |
|-----:|:--------|
|   42 | [1,2,3] |
|   43 | [4,5,6] |

You can read the same file with `records` set to `false`, to get a single column, which is a `STRUCT` containing the data:

<div class="monospace_table"></div>

| json |
|:-----|
| {'duck': 42, 'goose': [1,2,3]} |
| {'duck': 43, 'goose': [4,5,6]} |

For additional examples reading more complex data, please see the [“Shredding Deeply Nested JSON, One Vector at a Time” blog post]({% post_url 2023-03-03-json %}).

## Loading with the `COPY` Statement Using `FORMAT json`

When the `json` extension is installed, `FORMAT json` is supported for `COPY FROM`, `IMPORT DATABASE`, as well as `COPY TO` and `EXPORT DATABASE`. See the [`COPY` statement]({% link docs/stable/sql/statements/copy.md %}) and the [`IMPORT` / `EXPORT` clauses]({% link docs/stable/sql/statements/export.md %}).

By default, `COPY` expects newline-delimited JSON. If you prefer copying data to/from a JSON array, you can specify `ARRAY true`, e.g.,

```sql
COPY (SELECT * FROM range(5) r(i))
TO 'numbers.json' (ARRAY true);
```

will create the following file:

```json
[
	{"i":0},
	{"i":1},
	{"i":2},
	{"i":3},
	{"i":4}
]
```

This can be read back to DuckDB as follows:

```sql
CREATE TABLE numbers (i BIGINT);
COPY numbers FROM 'numbers.json' (ARRAY true);
```

The format can be detected automatically like so:

```sql
CREATE TABLE numbers (i BIGINT);
COPY numbers FROM 'numbers.json' (AUTO_DETECT true);
```

We can also create a table from the auto-detected schema:

```sql
CREATE TABLE numbers AS
    FROM 'numbers.json';
```

### Parameters

| Name | Description | Type | Default |
|:--|:-----|:-|:-|
| `auto_detect` | Whether to auto-detect the names of the keys and data types of the values automatically | `BOOL` | `false` |
| `columns` | A struct that specifies the key names and value types contained within the JSON file (e.g., `{key1: 'INTEGER', key2: 'VARCHAR'}`). If `auto_detect` is enabled these will be inferred | `STRUCT` | `(empty)` |
| `compression` | The compression type for the file. By default this will be detected automatically from the file extension (e.g., `t.json.gz` will use gzip, `t.json` will use none). Options are `uncompressed`, `gzip`, `zstd` and `auto_detect`. | `VARCHAR` | `auto_detect` |
| `convert_strings_to_integers` | Whether strings representing integer values should be converted to a numerical type. | `BOOL` | `false` |
| `dateformat` | Specifies the date format to use when parsing dates. See [Date Format]({% link docs/stable/sql/functions/dateformat.md %}) | `VARCHAR` | `iso` |
| `filename` | Whether or not an extra `filename` column should be included in the result. | `BOOL` | `false` |
| `format` | Can be one of `auto, unstructured, newline_delimited, array` | `VARCHAR` | `array` |
| `hive_partitioning` | Whether or not to interpret the path as a [Hive partitioned path]({% link docs/stable/data/partitioning/hive_partitioning.md %}). | `BOOL` | `false` |
| `ignore_errors` | Whether to ignore parse errors (only possible when `format` is `newline_delimited`) | `BOOL` | `false` |
| `maximum_depth` | Maximum nesting depth to which the automatic schema detection detects types. Set to -1 to fully detect nested JSON types | `BIGINT` | `-1` |
| `maximum_object_size` | The maximum size of a JSON object (in bytes) | `UINTEGER` | `16777216` |
| `records` | Can be one of `auto`, `true`, `false` | `VARCHAR` | `records` |
| `sample_size` | Option to define number of sample objects for automatic JSON type detection. Set to -1 to scan the entire input file | `UBIGINT` | `20480` |
| `timestampformat` | Specifies the date format to use when parsing timestamps. See [Date Format]({% link docs/stable/sql/functions/dateformat.md %}) | `VARCHAR` | `iso`|
| `union_by_name` | Whether the schema's of multiple JSON files should be [unified]({% link docs/stable/data/multiple_files/combining_schemas.md %}). | `BOOL` | `false` |
