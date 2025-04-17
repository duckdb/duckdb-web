---
layout: docu
title: JSON Format Settings
---

The JSON extension can attempt to determine the format of a JSON file when setting `format` to `auto`.
Here are some example JSON files and the corresponding `format` settings that should be used.

In each of the below cases, the `format` setting was not needed, as DuckDB was able to infer it correctly, but it is included for illustrative purposes.
A query of this shape would work in each case:

```sql
SELECT *
FROM filename.json;
```

#### Format: `newline_delimited`

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

<div class="monospace_table"></div>

|  key1  |  key2  |
|--------|--------|
| value1 | value1 |
| value2 | value2 |
| value3 | value3 |

#### Format: `array`

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

<div class="monospace_table"></div>

|  key1  |  key2  |
|--------|--------|
| value1 | value1 |
| value2 | value2 |
| value3 | value3 |

#### Format: `unstructured`

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

<div class="monospace_table"></div>

|  key1  |  key2  |
|--------|--------|
| value1 | value1 |
| value2 | value2 |
| value3 | value3 |

### Records Settings

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

<div class="monospace_table"></div>

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

<div class="monospace_table"></div>

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

<div class="monospace_table"></div>

|   json    |
|-----------|
| [1, 2, 3] |
| [4, 5, 6] |
| [7, 8, 9] |
