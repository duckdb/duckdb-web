---
layout: docu
title: JSON Loading
redirect_from:
  - /docs/data/json
---

### Examples

```sql
-- read a JSON file from disk, auto-infer options
SELECT * FROM 'todos.json';
-- read_json with custom options
SELECT *
FROM read_json('todos.json',
               json_format='array_of_records',
               columns={userId: 'UBIGINT',
                        id: 'UBIGINT',
                        title: 'VARCHAR',
                        completed: 'BOOLEAN'});
-- read a JSON file from stdin, auto-infer options
cat data/json/todos.json | duckdb -c "select * from read_json_auto('/dev/stdin')"

-- read a JSON file into a table
CREATE TABLE todos(userId UBIGINT, id UBIGINT, title VARCHAR, completed BOOLEAN);
COPY todos FROM 'todos.json';
-- alternatively, create a table without specifying the schema manually
CREATE TABLE todos AS SELECT * FROM 'todos.json';

-- write the result of a query to a JSON file
COPY (SELECT * FROM todos) TO 'todos.json';
```

### JSON Loading
JSON is an open standard file format and data interchange format that uses human-readable text to store and transmit data objects consisting of attribute–value pairs and arrays (or other serializable values).
While it is not a very efficient format for tabular data, it is very commonly used, as a data interchange format.

The DuckDB JSON reader can automatically infer which configuration flags to use by analyzing the JSON file. This will work correctly in most situations, and should be the first option attempted. In rare situations where the JSON reader cannot figure out the correct configuration, it is possible to manually configure the JSON reader to correctly parse the JSON file.

Below are parameters that can be passed in to the JSON reader.

# Parameters

| Name | Description | Type | Default |
|:---|:---|:---|:---|
| `maximum_object_size` | The maximum size of a JSON object (in bytes) | uinteger | `1048576` |
| `lines` | When set to `'true` only newline-delimited JSON can be read, which can be read in parallel, When set to `'false'`, pretty-printed JSON can be read. Set to `'auto'` to automatically detect | varchar | `'false'` |
| `ignore_errors` | Whether to ignore parse errors (only possible when `lines` is `'true'`) | bool | false |
| `compression` | The compression type for the file. By default this will be detected automatically from the file extension (e.g. **t.json.gz** will use gzip, **t.json** will use none). Options are `'none'`, `'gzip'`, `'zstd'`, and `'auto'`. | varchar | `'auto'` |
| `columns` | A struct that specifies the key names and value types contained within the JSON file (e.g. `{key1: 'INTEGER', key2: 'VARCHAR'}`). If `auto_detect` is enabled these will be inferred | struct | `(empty)` |
| `json_format` | Can be one of `['auto', 'records', 'array_of_records', 'values', 'array_of_values']` | varchar | `'records'` |
| `auto_detect` | Whether to auto-detect detect the names of the keys and data types of the values automatically | bool | `false` |
| `sample_size` | Option to define number of sample objects for automatic JSON type detection. Set to -1 to scan the entire input file | ubigint | `2048` |
| `maximum_depth` | Maximum nesting depth to which the automatic schema detection detects types. Set to -1 to fully detect nested JSON types | bigint | `-1` |
| `dateformat` | Specifies the date format to use when parsing dates. See [Date Format](../sql/functions/dateformat) | varchar | `'iso'` |
| `timestampformat` | Specifies the date format to use when parsing timestamps. See [Date Format](../sql/functions/dateformat) | varchar | `'iso'`|

When using `read_json_auto`, everything parameter that supports auto-detection is enabled.

### Writing

The contents of tables or the result of queries can be written directly to a JSON file using the `COPY` statement. See the [COPY documentation](../../sql/statements/copy#copy-to) for more information.

# read_json_auto function
The `read_json_auto` is the simplest method of loading JSON files: it automatically attempts to figure out the correct configuration of the JSON reader. It also automatically deduces types of columns.

```sql
SELECT * FROM read_json_auto('todos.json') LIMIT 5;
```

| userId | id |                              title                              | completed |
|--------|----|-----------------------------------------------------------------|-----------|
| 1      | 1  | delectus aut autem                                              | false     |
| 1      | 2  | quis ut nam facilis et officia qui                              | false     |
| 1      | 3  | fugiat veniam minus                                             | false     |
| 1      | 4  | et porro tempora                                                | true      |
| 1      | 5  | laboriosam mollitia et enim quasi adipisci quia provident illum | false     |

The path can either be a relative path (relative to the current working directory) or an absolute path.

We can use `read_json_auto` to create a persistent table as well:

```sql
CREATE TABLE todos AS SELECT * FROM read_json_auto('todos.json');
DESCRIBE todos;
```

| column_name | column_type | null | key | default | extra |
|-------------|-------------|------|-----|---------|-------|
| userId      | UBIGINT     | YES  |     |         |       |
| id          | UBIGINT     | YES  |     |         |       |
| title       | VARCHAR     | YES  |     |         |       |
| completed   | BOOLEAN     | YES  |     |         |       |

If we specify the columns, we can bypass the automatic detection. Note that not all columns need to be specified:

```sql
SELECT *
FROM read_json_auto('todos.json',
                    columns={userId: 'UBIGINT',
                             completed: 'BOOLEAN'});
```

Multiple files can be read at once by providing a glob or a list of files. Refer to the [multiple files section](../multiple_files/overview) for more information.


## COPY Statement
The `COPY` statement can be used to load data from a JSON file into a table. For the `COPY` statement, we must first create a table with the correct schema to load the data into. We then specify the JSON file to load from plus any configuration options separately.

```sql
CREATE TABLE todos(userId UBIGINT, id UBIGINT, title VARCHAR, completed BOOLEAN);
COPY todos FROM 'todos.json';
SELECT * FROM todos LIMIT 5;
```

| userId | id |                              title                              | completed |
|--------|----|-----------------------------------------------------------------|-----------|
| 1      | 1  | delectus aut autem                                              | false     |
| 1      | 2  | quis ut nam facilis et officia qui                              | false     |
| 1      | 3  | fugiat veniam minus                                             | false     |
| 1      | 4  | et porro tempora                                                | true      |
| 1      | 5  | laboriosam mollitia et enim quasi adipisci quia provident illum | false     |

More on the copy statement can be found [here](/docs/sql/statements/copy.html).
