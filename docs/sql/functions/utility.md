---
layout: docu
title: Utility Functions
---

## Utility Functions

The functions below are difficult to categorize into specific function types and are broadly useful. 

| Function| Description| Example| Result|
|:--|:--|:---|:--|
| `alias(`*`column`*`)` | Return the name of the column| `alias(column1)` | `'column1'` |
| `checkpoint(`*`database`*`)`| Synchronize WAL with file for (optional) database without interrupting transactions. | `checkpoint(my_db)`| success boolean |
| `coalesce(`*`expr`*`, `*`...`*`)` | Return the first expression that evaluates to a non-`NULL` value. Accepts 1 or more parameters. Each expression can be a column, literal value, function result, or many others. | `coalesce(NULL, NULL, 'default_string')` | `'default_string'`|
| `constant_or_null(`*`arg1`*`, `*`arg2`*`)` | If *`arg2`* is `NULL`, return `NULL`. Otherwise, return *`arg1`*. | `constant_or_null(42, NULL)` | `NULL` |
| `count_if(`*`x`*`)` | Returns 1 if *x* is `true` or a non-zero number | `count_if(42)` | 1 |
| `error(`*`message`*`)` | Throws the given error *`message`* | `error('access_mode')` | |
| `ifnull(`*`expr`*`, `*`other`*`)` | A two-argument version of coalesce | `ifnull(NULL, 'default_string')` | `'default_string'`|
| `nullif(`*`a`*`, `*`b`*`)` | Return null if a = b, else return a. Equivalent to `CASE WHEN a = b THEN NULL ELSE a END`. | `nullif(1+1, 2)` | `NULL`|
| `current_schema()`| Return the name of the currently active schema. Default is main. | `current_schema()` | `'main'`|
| `current_schemas(`*`boolean`*`)`| Return list of schemas. Pass a parameter of `true` to include implicit schemas.| `current_schemas(true)`| `['temp', 'main', 'pg_catalog']`|
| `current_setting(`*`'setting_name'`*`)` | Return the current value of the configuration setting| `current_setting('access_mode')` | `'automatic'` |
| `currval(`*`'sequence_name'`*`)`| Return the current value of the sequence. Note that `nextval` must be called at least once prior to calling `currval`. | `currval('my_sequence_name')`| `1` |
| `force_checkpoint(`*`database`*`)`| Synchronize WAL with file for (optional) database interrupting transactions. | `force_checkpoint(my_db)`| success boolean |
| `gen_random_uuid()` | Alias of `uuid`. Return a random uuid similar to this: eeccb8c5-9943-b2bb-bb5e-222f4e14b687. | `gen_random_uuid()`| various |
| `hash(`*`value`*`)` | Returns a `UBIGINT` with the hash of the *`value`*| `hash('🦆')` | `2595805878642663834` |
| `icu_sort_key(`*`string`*`, `*`collator`*`)` | Surrogate key used to sort special characters according to the specific locale. Collator parameter is optional. Valid only when ICU extension is installed.| `icu_sort_key('ö', 'DE')` | `460145960106` |
| `md5(`*`string`*`)` | Return an md5 one-way hash of the *`string`*.| `md5('123')` | `'202cb962ac59075b964b07152d234b70'`|
| `nextval(`*`'sequence_name'`*`)`| Return the following value of the sequence.| `nextval('my_sequence_name')`| `2` |
| `pg_typeof(`*`expression`*`)` | Returns the lower case name of the data type of the result of the expression. For PostgreSQL compatibility.| `pg_typeof('abc')` | `'varchar'` |
| `repeat_row(`*`varargs`*`, `*`num_rows`*`)` | Returns a table with *`num_rows`* rows, each containing the fields defined in *`varargs`* | `repeat_row(1, 2, 'foo', num_rows = 3)` | 3 rows of `1, 2, 'foo'` |
| `sha256(`*`value`*`)` | Returns a `VARCHAR` with the SHA-256 hash of the *`value`*| `sha-256('🦆')` | `d7a5c5e0d1d94c32218539e7e47d4ba9c3c7b77d61332fb60d633dde89e473fb` |
| `stats(`*`expression`*`)` | Returns a string with statistics about the expression. Expression can be a column, constant, or SQL expression.| `stats(5)` | `'[Min: 5, Max: 5][Has Null: false]'` |
| `txid_current()`| Returns the current transaction's ID (a `BIGINT`). It will assign a new one if the current transaction does not have one already.| `txid_current()` | various |
| `typeof(`*`expression`*`)`| Returns the name of the data type of the result of the expression. | `typeof('abc')`| `'VARCHAR'` |
| `uuid()`| Return a random uuid similar to this: eeccb8c5-9943-b2bb-bb5e-222f4e14b687.| `uuid()` | various |
| `version()` | Return the currently active version of DuckDB in this format | `version()`| various |

## Utility Table Functions

A table function is used in place of a table in a `FROM` clause.

<div class="narrow_table"></div>

| Function | Description | Example |
|:--|:---|:-|
| `glob(`*`search_path`*`)` | Return filenames found at the location indicated by the *search_path* in a single column named `file`. The *search_path* may contain [glob pattern matching syntax](patternmatching). | `glob('*')` |
