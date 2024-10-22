---
layout: docu
title: JSON Overview
redirect_from:
  - /docs/data/json
  - /docs/extensions/json
---

DuckDB supports SQL functions that are useful for reading values from existing JSON and creating new JSON data.

## About JSON

JSON is an open standard file format and data interchange format that uses human-readable text to store and transmit data objects consisting of attribute–value pairs and arrays (or other serializable values).
While it is not a very efficient format for tabular data, it is very commonly used, especially as a data interchange format.

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

See more examples of loading JSON data on the [JSON data page]({% link docs/data/json/overview.md %}#examples):

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

## Examples

Read a JSON file from disk, auto-infer options:

```sql
SELECT * FROM 'todos.json';
```

Use the `read_json` function with custom options:

```sql
SELECT *
FROM read_json('todos.json',
               format = 'array',
               columns = {userId: 'UBIGINT',
                          id: 'UBIGINT',
                          title: 'VARCHAR',
                          completed: 'BOOLEAN'});
```

Read a JSON file from stdin, auto-infer options:

```bash
cat data/json/todos.json | duckdb -c "SELECT * FROM read_json('/dev/stdin')"
```

Read a JSON file into a table:

```sql
CREATE TABLE todos (userId UBIGINT, id UBIGINT, title VARCHAR, completed BOOLEAN);
COPY todos FROM 'todos.json';
```

Alternatively, create a table without specifying the schema manually with a [`CREATE TABLE ... AS SELECT` clause]({% link docs/sql/statements/create_table.md %}#create-table--as-select-ctas):

```sql
CREATE TABLE todos AS
    SELECT * FROM 'todos.json';
```

Write the result of a query to a JSON file:

```sql
COPY (SELECT * FROM todos) TO 'todos.json';
```

## Examples of Format Settings

The JSON extension can attempt to determine the format of a JSON file when setting `format` to `auto`.
Here are some example JSON files and the corresponding `format` settings that should be used.

In each of the below cases, the `format` setting was not needed, as DuckDB was able to infer it correctly, but it is included for illustrative purposes.
A query of this shape would work in each case:

```sql
SELECT *
FROM filename.json;
```

### Format: `newline_delimited`

With `format = 'newline_delimited'` newline-delimited JSON can be parsed.
Each line is a JSON.

We use the example file [`records.json`](/data/records.json) with the following content:

```json
{"key1":"value1", "key2": "value1"}
{"key1":"value2", "key2": "value2"}
{"key1":"value3", "key2": "value3"}
```

```sql
SELECT *
FROM read_json('records.json', format = 'newline_delimited');
```

<div class="narrow_table monospace_table"></div>

|  key1  |  key2  |
|--------|--------|
| value1 | value1 |
| value2 | value2 |
| value3 | value3 |

### Format: `array`

If the JSON file contains a JSON array of objects (pretty-printed or not), `array_of_objects` may be used.
To demonstrate its use, we use the example file [`records-in-array.json`](/data/records-in-array.json):

```json
[
    {"key1":"value1", "key2": "value1"},
    {"key1":"value2", "key2": "value2"},
    {"key1":"value3", "key2": "value3"}
]
```

```sql
SELECT *
FROM read_json('records-in-array.json', format = 'array');
```

<div class="narrow_table monospace_table"></div>

|  key1  |  key2  |
|--------|--------|
| value1 | value1 |
| value2 | value2 |
| value3 | value3 |

### Format: `unstructured`

If the JSON file contains JSON that is not newline-delimited or an array, `unstructured` may be used.
To demonstrate its use, we use the example file [`unstructured.json`](/data/unstructured.json):

```json
{
    "key1":"value1",
    "key2":"value1"
}
{
    "key1":"value2",
    "key2":"value2"
}
{
    "key1":"value3",
    "key2":"value3"
}
```

```sql
SELECT *
FROM read_json('unstructured.json', format = 'unstructured');
```

<div class="narrow_table monospace_table"></div>

|  key1  |  key2  |
|--------|--------|
| value1 | value1 |
| value2 | value2 |
| value3 | value3 |

## Examples of Records Settings

The JSON extension can attempt to determine whether a JSON file contains records when setting `records = auto`.
When `records = true`, the JSON extension expects JSON objects, and will unpack the fields of JSON objects into individual columns.

Continuing with the same example file, [`records.json`](/data/records.json):

```json
{"key1":"value1", "key2": "value1"}
{"key1":"value2", "key2": "value2"}
{"key1":"value3", "key2": "value3"}
```

```sql
SELECT *
FROM read_json('records.json', records = true);
```

<div class="narrow_table monospace_table"></div>

|  key1  |  key2  |
|--------|--------|
| value1 | value1 |
| value2 | value2 |
| value3 | value3 |

When `records = false`, the JSON extension will not unpack the top-level objects, and create `STRUCT`s instead:

```sql
SELECT *
FROM read_json('records.json', records = false);
```

<div class="narrow_table monospace_table"></div>

|               json               |
|----------------------------------|
| {'key1': value1, 'key2': value1} |
| {'key1': value2, 'key2': value2} |
| {'key1': value3, 'key2': value3} |

This is especially useful if we have non-object JSON, for example, [`arrays.json`](/data/arrays.json):

```json
[1, 2, 3]
[4, 5, 6]
[7, 8, 9]
```

```sql
SELECT *
FROM read_json('arrays.json', records = false);
```

<div class="narrow_table monospace_table"></div>

|   json    |
|-----------|
| [1, 2, 3] |
| [4, 5, 6] |
| [7, 8, 9] |

