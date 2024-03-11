---
layout: docu
title: Utility Functions
---

## Utility Functions

The functions below are difficult to categorize into specific function types and are broadly useful.

| Function | Description | Example | Result |
|:--|:--|:---|:--|
| `alias(`*`column`*`)` | Return the name of the column| `alias(column1)` | `column1` |
| `checkpoint(`*`database`*`)`| Synchronize WAL with file for (optional) database without interrupting transactions. | `checkpoint(my_db)`| success boolean |
| `coalesce(`*`expr`*`, `*`...`*`)` | Return the first expression that evaluates to a non-`NULL` value. Accepts 1 or more parameters. Each expression can be a column, literal value, function result, or many others. | `coalesce(NULL, NULL, 'default_string')` | `default_string`|
| `constant_or_null(`*`arg1`*`, `*`arg2`*`)` | If *`arg2`* is `NULL`, return `NULL`. Otherwise, return *`arg1`*. | `constant_or_null(42, NULL)` | `NULL` |
| `count_if(`*`x`*`)` | Returns 1 if *x* is `true` or a non-zero number | `count_if(42)` | 1 |
| `current_catalog()` | Return the name of the currently active catalog. Default is memory. | `current_catalog()` | `memory` |
| `current_schema()`| Return the name of the currently active schema. Default is main. | `current_schema()` | `main`|
| `current_schemas(`*`boolean`*`)`| Return list of schemas. Pass a parameter of `true` to include implicit schemas.| `current_schemas(true)`| `['temp', 'main', 'pg_catalog']`|
| `current_setting(`*`'setting_name'`*`)` | Return the current value of the configuration setting| `current_setting('access_mode')` | `automatic` |
| `currval(`*`'sequence_name'`*`)`| Return the current value of the sequence. Note that `nextval` must be called at least once prior to calling `currval`. | `currval('my_sequence_name')`| `1` |
| `error(`*`message`*`)` | Throws the given error *`message`* | `error('access_mode')` | |
| `force_checkpoint(`*`database`*`)`| Synchronize WAL with file for (optional) database interrupting transactions. | `force_checkpoint(my_db)`| success boolean |
| `gen_random_uuid()` | Alias of `uuid`. Return a random UUID similar to this: `eeccb8c5-9943-b2bb-bb5e-222f4e14b687`. | `gen_random_uuid()`| various |
| `hash(`*`value`*`)` | Returns a `UBIGINT` with the hash of the *`value`*| `hash('🦆')` | `2595805878642663834` |
| `icu_sort_key(`*`string`*`, `*`collator`*`)` | Surrogate key used to sort special characters according to the specific locale. Collator parameter is optional. Valid only when ICU extension is installed.| `icu_sort_key('ö', 'DE')` | `460145960106` |
| `ifnull(`*`expr`*`, `*`other`*`)` | A two-argument version of coalesce | `ifnull(NULL, 'default_string')` | `default_string`|
| `md5(`*`string`*`)` | Return an md5 one-way hash of the *`string`*.| `md5('123')` | `202c...`|
| `nextval(`*`'sequence_name'`*`)`| Return the following value of the sequence.| `nextval('my_sequence_name')`| `2` |
| `nullif(`*`a`*`, `*`b`*`)` | Return null if a = b, else return a. Equivalent to `CASE WHEN a = b THEN NULL ELSE a END`. | `nullif(1+1, 2)` | `NULL`|
| `pg_typeof(`*`expression`*`)` | Returns the lower case name of the data type of the result of the expression. For PostgreSQL compatibility.| `pg_typeof('abc')` | `varchar` |
| `query(`*`query_string`*`)` | Parses and executes the query defined in *`query_string`*. Warning: this function allows invoking arbitrary queries, potentially altering the database state. | `query('SELECT 42')` | `42` |
| `query_table(`*`tbl_name`*`)` | Returns the table given in *`tbl_name`*. Warning: this function allows invoking arbitrary queries, potentially altering the database state. | `query(t1)` | (the rows of `t1`) |
| `query_table(`*`tbl_names`*`, [`*`by_name`*`])` | Returns the union of tables given in *`tbl_names`*. If the optional *`by_name`* parameter is set to `true`, it uses [`UNION ALL BY NAME`](../../sql/query_syntax/setops#union-all-by-name) semantics. Warning: this function allows invoking arbitrary queries, potentially altering the database state. | `query(['t1', 't2'])` | (union of two tables) |
| `read_blob(`*`source`*`)` | Returns the content from *`source`* (a filename, a list of filenames, or a glob pattern) as a `BLOB`. See the [`read_blob` guide](../../guides/import/read_file#read_blob) for more details. | `read_blob('hello.bin')` | `hello\x0A` |
| `read_text(`*`source`*`)` | Returns the content from *`source`* (a filename, a list of filenames, or a glob pattern) as a `VARCHAR`. The file content is first validated to be valid UTF-8. If `read_text` attempts to read a file with invalid UTF-8 an error is thrown suggesting to use `read_blob` instead. See the [`read_text` guide](../../guides/import/read_file#read_text) for more details. | `read_text('hello.txt')` | `hello\n` |
| `repeat_row(`*`varargs`*`, `*`num_rows`*`)` | Returns a table with *`num_rows`* rows, each containing the fields defined in *`varargs`* | `repeat_row(1, 2, 'foo', num_rows = 3)` | 3 rows of `1, 2, 'foo'` |
| `sha256(`*`value`*`)` | Returns a `VARCHAR` with the SHA-256 hash of the *`value`*| `sha-256('🦆')` | `d7a5...` |
| `stats(`*`expression`*`)` | Returns a string with statistics about the expression. Expression can be a column, constant, or SQL expression.| `stats(5)` | `'[Min: 5, Max: 5][Has Null: false]'` |
| `txid_current()`| Returns the current transaction's ID (a `BIGINT`). It will assign a new one if the current transaction does not have one already.| `txid_current()` | various |
| `typeof(`*`expression`*`)`| Returns the name of the data type of the result of the expression. | `typeof('abc')`| `VARCHAR` |
| `uuid()`| Return a random UUID similar to this: `eeccb8c5-9943-b2bb-bb5e-222f4e14b687`.| `uuid()` | various |
| `version()` | Return the currently active version of DuckDB in this format | `version()`| various |

## Utility Table Functions

A table function is used in place of a table in a `FROM` clause.

<div class="narrow_table"></div>

| Function | Description | Example |
|:--|:---|:-|
| `glob(`*`search_path`*`)` | Return filenames found at the location indicated by the *search_path* in a single column named `file`. The *search_path* may contain [glob pattern matching syntax](patternmatching). | `glob('*')` |
