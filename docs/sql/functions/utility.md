---
layout: docu
title: Utility Functions
redirect_from:
  - docs/test/functions/utility
---

## Scalar Utility Functions

The functions below are difficult to categorize into specific function types and are broadly useful.

| Name | Description |
|:--|:-------|
| [`alias(column)`](#aliascolumn) | Return the name of the column. |
| [`checkpoint(database)`](#checkpointdatabase) | Synchronize WAL with file for (optional) database without interrupting transactions. |
| [`coalesce(expr, ...)`](#coalesceexpr-) | Return the first expression that evaluates to a non-`NULL` value. Accepts 1 or more parameters. Each expression can be a column, literal value, function result, or many others. |
| [`constant_or_null(arg1, arg2)`](#constant_or_nullarg1-arg2) | If `arg2` is `NULL`, return `NULL`. Otherwise, return `arg1`. |
| [`count_if(x)`](#count_ifx) | Returns 1 if `x` is `true` or a non-zero number. |
| [`current_catalog()`](#current_catalog) | Return the name of the currently active catalog. Default is memory. |
| [`current_schema()`](#current_schema) | Return the name of the currently active schema. Default is main. |
| [`current_schemas(boolean)`](#current_schemasboolean) | Return list of schemas. Pass a parameter of `true` to include implicit schemas. |
| [`current_setting('setting_name')`](#current_settingsetting_name) | Return the current value of the configuration setting. |
| [`currval('sequence_name')`](#currvalsequence_name) | Return the current value of the sequence. Note that `nextval` must be called at least once prior to calling `currval`. |
| [`error(message)`](#errormessage) | Throws the given error `message`. |
| [`force_checkpoint(database)`](#force_checkpointdatabase) | Synchronize WAL with file for (optional) database interrupting transactions. |
| [`gen_random_uuid()`](#gen_random_uuid) | Alias of `uuid`. Return a random UUID similar to this: `eeccb8c5-9943-b2bb-bb5e-222f4e14b687`. |
| [`hash(value)`](#hashvalue) | Returns a `UBIGINT` with the hash of the `value`. |
| [`icu_sort_key(string, collator)`](#icu_sort_keystring-collator) | Surrogate key used to sort special characters according to the specific locale. Collator parameter is optional. Valid only when ICU extension is installed. |
| [`ifnull(expr, other)`](#ifnullexpr-other) | A two-argument version of coalesce. |
| [`md5(string)`](#md5string) | Return an MD5 hash of the `string`. |
| [`nextval('sequence_name')`](#nextvalsequence_name) | Return the following value of the sequence. |
| [`nullif(a, b)`](#nullifa-b) | Return null if a = b, else return a. Equivalent to `CASE WHEN a = b THEN NULL ELSE a END`. |
| [`pg_typeof(expression)`](#pg_typeofexpression) | Returns the lower case name of the data type of the result of the expression. For PostgreSQL compatibility. |
| [`read_blob(source)`](#read_blobsource) | Returns the content from `source` (a filename, a list of filenames, or a glob pattern) as a `BLOB`. See the [`read_blob` guide](../../guides/file_formats/read_file#read_blob) for more details. |
| [`read_text(source)`](#read_textsource) | Returns the content from `source` (a filename, a list of filenames, or a glob pattern) as a `VARCHAR`. The file content is first validated to be valid UTF-8. If `read_text` attempts to read a file with invalid UTF-8 an error is thrown suggesting to use `read_blob` instead. See the [`read_text` guide](../../guides/file_formats/read_file#read_text) for more details. |
| [`sha256(value)`](#sha256value) | Returns a `VARCHAR` with the SHA-256 hash of the `value`. |
| [`stats(expression)`](#statsexpression) | Returns a string with statistics about the expression. Expression can be a column, constant, or SQL expression. |
| [`txid_current()`](#txid_current) | Returns the current transaction's identifier, a `BIGINT` value. It will assign a new one if the current transaction does not have one already. |
| [`typeof(expression)`](#typeofexpression) | Returns the name of the data type of the result of the expression. |
| [`uuid()`](#uuid) | Return a random UUID similar to this: `eeccb8c5-9943-b2bb-bb5e-222f4e14b687`. |
| [`version()`](#version) | Return the currently active version of DuckDB in this format. |

### `alias(column)`

<div class="nostroke_table"></div>

| **Description** | Return the name of the column. |
| **Example** | `alias(column1)` |
| **Result** | `column1` |

### `checkpoint(database)`

<div class="nostroke_table"></div>

| **Description** | Synchronize WAL with file for (optional) database without interrupting transactions. |
| **Example** | `checkpoint(my_db)` |
| **Result** | success boolean |

### `coalesce(expr, ...)`

<div class="nostroke_table"></div>

| **Description** | Return the first expression that evaluates to a non-`NULL` value. Accepts 1 or more parameters. Each expression can be a column, literal value, function result, or many others. |
| **Example** | `coalesce(NULL, NULL, 'default_string')` |
| **Result** | `default_string` |

### `constant_or_null(arg1, arg2)`

<div class="nostroke_table"></div>

| **Description** | If `arg2` is `NULL`, return `NULL`. Otherwise, return `arg1`. |
| **Example** | `constant_or_null(42, NULL)` |
| **Result** | `NULL` |

### `count_if(x)`

<div class="nostroke_table"></div>

| **Description** | Returns 1 if `x` is `true` or a non-zero number. |
| **Example** | `count_if(42)` |
| **Result** | 1 |

### `current_catalog()`

<div class="nostroke_table"></div>

| **Description** | Return the name of the currently active catalog. Default is memory. |
| **Example** | `current_catalog()` |
| **Result** | `memory` |

### `current_schema()`

<div class="nostroke_table"></div>

| **Description** | Return the name of the currently active schema. Default is main. |
| **Example** | `current_schema()` |
| **Result** | `main` |

### `current_schemas(boolean)`

<div class="nostroke_table"></div>

| **Description** | Return list of schemas. Pass a parameter of `true` to include implicit schemas. |
| **Example** | `current_schemas(true)` |
| **Result** | `['temp', 'main', 'pg_catalog']` |

### `current_setting('setting_name')`

<div class="nostroke_table"></div>

| **Description** | Return the current value of the configuration setting. |
| **Example** | `current_setting('access_mode')` |
| **Result** | `automatic` |

### `currval('sequence_name')`

<div class="nostroke_table"></div>

| **Description** | Return the current value of the sequence. Note that `nextval` must be called at least once prior to calling `currval`. |
| **Example** | `currval('my_sequence_name')` |
| **Result** | `1` |

### `error(message)`

<div class="nostroke_table"></div>

| **Description** | Throws the given error `message`. |
| **Example** | `error('access_mode')` |

### `force_checkpoint(database)`

<div class="nostroke_table"></div>

| **Description** | Synchronize WAL with file for (optional) database interrupting transactions. |
| **Example** | `force_checkpoint(my_db)` |
| **Result** | success boolean |

### `gen_random_uuid()`

<div class="nostroke_table"></div>

| **Description** | Alias of `uuid`. Return a random UUID similar to this: `eeccb8c5-9943-b2bb-bb5e-222f4e14b687`. |
| **Example** | `gen_random_uuid()` |
| **Result** | various |

### `hash(value)`

<div class="nostroke_table"></div>

| **Description** | Returns a `UBIGINT` with the hash of the `value`. |
| **Example** | `hash('🦆')` |
| **Result** | `2595805878642663834` |

### `icu_sort_key(string, collator)`

<div class="nostroke_table"></div>

| **Description** | Surrogate key used to sort special characters according to the specific locale. Collator parameter is optional. Valid only when ICU extension is installed. |
| **Example** | `icu_sort_key('ö', 'DE')` |
| **Result** | `460145960106` |

### `ifnull(expr, other)`

<div class="nostroke_table"></div>

| **Description** | A two-argument version of coalesce. |
| **Example** | `ifnull(NULL, 'default_string')` |
| **Result** | `default_string` |

### `md5(string)`

<div class="nostroke_table"></div>

| **Description** | Return an MD5 hash of the `string`. |
| **Example** | `md5('123')` |
| **Result** | `202cb962ac59075b964b07152d234b70` |

### `nextval('sequence_name')`

<div class="nostroke_table"></div>

| **Description** | Return the following value of the sequence. |
| **Example** | `nextval('my_sequence_name')` |
| **Result** | `2` |

### `nullif(a, b)`

<div class="nostroke_table"></div>

| **Description** | Return null if a = b, else return a. Equivalent to `CASE WHEN a = b THEN NULL ELSE a END`. |
| **Example** | `nullif(1+1, 2)` |
| **Result** | `NULL` |

### `pg_typeof(expression)`

<div class="nostroke_table"></div>

| **Description** | Returns the lower case name of the data type of the result of the expression. For PostgreSQL compatibility. |
| **Example** | `pg_typeof('abc')` |
| **Result** | `varchar` |

### `read_blob(source)`

<div class="nostroke_table"></div>

| **Description** | Returns the content from `source` (a filename, a list of filenames, or a glob pattern) as a `BLOB`. See the [`read_blob` guide](../../guides/file_formats/read_file#read_blob) for more details. |
| **Example** | `read_blob('hello.bin')` |
| **Result** | `hello\x0A` |

### `read_text(source)`

<div class="nostroke_table"></div>

| **Description** | Returns the content from `source` (a filename, a list of filenames, or a glob pattern) as a `VARCHAR`. The file content is first validated to be valid UTF-8. If `read_text` attempts to read a file with invalid UTF-8 an error is thrown suggesting to use `read_blob` instead. See the [`read_text` guide](../../guides/file_formats/read_file#read_text) for more details. |
| **Example** | `read_text('hello.txt')` |
| **Result** | `hello\n` |

### `sha256(value)`

<div class="nostroke_table"></div>

| **Description** | Returns a `VARCHAR` with the SHA-256 hash of the `value`. |
| **Example** | `sha256('🦆')` |
| **Result** | `d7a5c5e0d1d94c32218539e7e47d4ba9c3c7b77d61332fb60d633dde89e473fb` |

### `stats(expression)`

<div class="nostroke_table"></div>

| **Description** | Returns a string with statistics about the expression. Expression can be a column, constant, or SQL expression. |
| **Example** | `stats(5)` |
| **Result** | `'[Min: 5, Max: 5][Has Null: false]'` |

### `txid_current()`

<div class="nostroke_table"></div>

| **Description** | Returns the current transaction's identifier, a `BIGINT` value. It will assign a new one if the current transaction does not have one already. |
| **Example** | `txid_current()` |
| **Result** | various |

### `typeof(expression)`

<div class="nostroke_table"></div>

| **Description** | Returns the name of the data type of the result of the expression. |
| **Example** | `typeof('abc')` |
| **Result** | `VARCHAR` |

### `uuid()`

<div class="nostroke_table"></div>

| **Description** | Return a random UUID similar to this: `eeccb8c5-9943-b2bb-bb5e-222f4e14b687`. |
| **Example** | `uuid()` |
| **Result** | various |

### `version()`

<div class="nostroke_table"></div>

| **Description** | Return the currently active version of DuckDB in this format. |
| **Example** | `version()` |
| **Result** | various |

## Utility Table Functions

A table function is used in place of a table in a `FROM` clause.

<div class="narrow_table"></div>

| Name | Description |
|:--|:-------|
| [`glob(search_path)`](#globsearch_path) | Return filenames found at the location indicated by the *search_path* in a single column named `file`. The *search_path* may contain [glob pattern matching syntax](pattern_matching). |
| [`repeat_row(varargs, num_rows)`](#repeat_rowvarargs-num_rows) | Returns a table with `num_rows` rows, each containing the fields defined in `varargs`. |

### `glob(search_path)`

<div class="nostroke_table"></div>

| **Description** | Return filenames found at the location indicated by the *search_path* in a single column named `file`. The *search_path* may contain [glob pattern matching syntax](pattern_matching). |
| **Example** | `glob('*')` |
| **Result** | (table of filenames) |

### `repeat_row(varargs, num_rows)`

<div class="nostroke_table"></div>

| **Description** | Returns a table with `num_rows` rows, each containing the fields defined in `varargs`. |
| **Example** | `repeat_row(1, 2, 'foo', num_rows = 3)` |
| **Result** | 3 rows of `1, 2, 'foo'` |
