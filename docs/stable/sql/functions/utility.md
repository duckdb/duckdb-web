---
layout: docu
redirect_from:
- /docs/test/functions/utility
- /docs/test/functions/utility/
- /docs/sql/functions/utility
title: Utility Functions
---

<!-- markdownlint-disable MD001 -->

## Scalar Utility Functions

The functions below are difficult to categorize into specific function types and are broadly useful.

| Name | Description |
|:--|:-------|
| [`alias(column)`](#aliascolumn) | Return the name of the column. |
| [`can_cast_implicitly(source_value, target_value)`](#can_cast_implicitlysource_value-target_value) | Whether or not we can implicitly cast from the types of the source value to the target value. |
| [`checkpoint(database)`](#checkpointdatabase) | Synchronize WAL with file for (optional) database without interrupting transactions. |
| [`coalesce(expr, ...)`](#coalesceexpr-) | Return the first expression that evaluates to a non-`NULL` value. Accepts 1 or more parameters. Each expression can be a column, literal value, function result, or many others. |
| [`constant_or_null(arg1, arg2)`](#constant_or_nullarg1-arg2) | If `arg2` is `NULL`, return `NULL`. Otherwise, return `arg1`. |
| [`count_if(x)`](#count_ifx) | Aggregate function; rows contribute 1 if `x` is `true` or a non-zero number, else 0. |
| [`create_sort_key(parameters...)`](#create_sort_keyparameters) | Constructs a binary-comparable sort key based on a set of input parameters and sort qualifiers. |
| [`current_catalog()`](#current_catalog) | Return the name of the currently active catalog. Default is memory. |
| [`current_database()`](#current_database) | Return the name of the currently active database. |
| [`current_query()`](#current_query) | Return the current query as a string. |
| [`current_schema()`](#current_schema) | Return the name of the currently active schema. Default is main. |
| [`current_schemas(boolean)`](#current_schemasboolean) | Return list of schemas. Pass a parameter of `true` to include implicit schemas. |
| [`current_setting('setting_name')`](#current_settingsetting_name) | Return the current value of the configuration setting. |
| [`currval('sequence_name')`](#currvalsequence_name) | Return the current value of the sequence. Note that `nextval` must be called at least once prior to calling `currval`. |
| [`error(message)`](#errormessage) | Throws the given error `message`. |
| [`equi_width_bins(min, max, bincount, nice := false)`](#equi_width_binsmin-max-bincount-nice--false) | Returns the upper boundaries of a partition of the interval `[min, max]` into `bin_count` equal-sized subintervals (for use with, e.g., [`histogram`]({% link docs/stable/sql/functions/aggregates.md %}#histogramargboundaries)). If `nice = true`, then `min`, `max`, and `bincount` may be adjusted to produce more aesthetically pleasing results. |
| [`force_checkpoint(database)`](#force_checkpointdatabase) | Synchronize WAL with file for (optional) database interrupting transactions. |
| [`gen_random_uuid()`](#gen_random_uuid) | Return a random UUID similar to this: `eeccb8c5-9943-b2bb-bb5e-222f4e14b687`. |
| [`getenv(var)`](#getenvvar) | Returns the value of the environment variable `var`. Only available in the [command line client]({% link docs/stable/clients/cli/overview.md %}). |
| [`hash(value)`](#hashvalue) | Returns a `UBIGINT` with a hash of `value`. The used hash function may change across DuckDB versions.|
| [`icu_sort_key(string, collator)`](#icu_sort_keystring-collator) | Surrogate [sort key](https://unicode-org.github.io/icu/userguide/collation/architecture.html#sort-keys) used to sort special characters according to the specific locale. Collator parameter is optional. Only available when the ICU extension is installed. |
| [`if(a, b, c)`](#ifa-b-c) | Ternary conditional operator. |
| [`ifnull(expr, other)`](#ifnullexpr-other) | A two-argument version of coalesce. |
| [`is_histogram_other_bin(arg)`](#is_histogram_other_binarg) | Returns `true` when `arg` is the "catch-all element" of its datatype for the purpose of the [`histogram_exact`]({% link docs/stable/sql/functions/aggregates.md %}#histogram_exactargelements) function, which is equal to the "right-most boundary" of its datatype for the purpose of the [`histogram`]({% link docs/stable/sql/functions/aggregates.md %}#histogramargboundaries) function. |
| [`md5(string)`](#md5string) | Returns the MD5 hash of the `string` as a `VARCHAR`. |
| [`md5_number(string)`](#md5_numberstring) | Returns the MD5 hash of the `string` as a `UHUGEINT`. |
| [`md5_number_lower(string)`](#md5_number_lowerstring) | Returns the lower 64-bit segment of the MD5 hash of the `string` as a `UBIGINT`. |
| [`md5_number_upper(string)`](#md5_number_upperstring) | Returns the upper 64-bit segment of the MD5 hash of the `string` as a `UBIGINT`. |
| [`nextval('sequence_name')`](#nextvalsequence_name) | Return the following value of the sequence. |
| [`nullif(a, b)`](#nullifa-b) | Return `NULL` if `a = b`, else return `a`. Equivalent to `CASE WHEN a = b THEN NULL ELSE a END`. |
| [`pg_typeof(expression)`](#pg_typeofexpression) | Returns the lower case name of the data type of the result of the expression. For PostgreSQL compatibility. |
| [`query(`*`query_string`*`)`](#queryquery_string) | Table function that parses and executes the query defined in *`query_string`*. Only constant strings are allowed. Warning: this function allows invoking arbitrary queries, potentially altering the database state. |
| [`query_table(`*`tbl_name`*`)`](#query_tabletbl_name) | Table function that returns the table given in *`tbl_name`*. |
| [`query_table(`*`tbl_names`*`, [`*`by_name`*`])`](#query_tabletbl_names-by_name) | Table function that returns the union of tables given in *`tbl_names`*. If the optional *`by_name`* parameter is set to `true`, it uses [`UNION ALL BY NAME`]({% link docs/stable/sql/query_syntax/setops.md %}#union-all-by-name) semantics. |
| [`read_blob(source)`](#read_blobsource) | Returns the content from `source` (a filename, a list of filenames, or a glob pattern) as a `BLOB`. See the [`read_blob` guide]({% link docs/stable/guides/file_formats/read_file.md %}#read_blob) for more details. |
| [`read_text(source)`](#read_textsource) | Returns the content from `source` (a filename, a list of filenames, or a glob pattern) as a `VARCHAR`. The file content is first validated to be valid UTF-8. If `read_text` attempts to read a file with invalid UTF-8 an error is thrown suggesting to use `read_blob` instead. See the [`read_text` guide]({% link docs/stable/guides/file_formats/read_file.md %}#read_text) for more details. |
| [`sha1(string)`](#sha1string) | Returns a `VARCHAR` with the SHA-1 hash of the `string`. |
| [`sha256(string)`](#sha256string) | Returns a `VARCHAR` with the SHA-256 hash of the `string`. |
| [`stats(expression)`](#statsexpression) | Returns a string with statistics about the expression. Expression can be a column, constant, or SQL expression. |
| [`txid_current()`](#txid_current) | Returns the current transaction's identifier, a `BIGINT` value. It will assign a new one if the current transaction does not have one already. |
| [`typeof(expression)`](#typeofexpression) | Returns the name of the data type of the result of the expression. |
| [`uuid()`](#uuid) | Return a random UUID (UUIDv4) similar to this: `eeccb8c5-9943-b2bb-bb5e-222f4e14b687`. |
| [`uuidv4()`](#uuidv4) | Return a random UUID (UUIDv4) similar to this: `eeccb8c5-9943-b2bb-bb5e-222f4e14b687`. |
| [`uuidv7()`](#uuidv7) | Return a random UUIDv7 similar to this: `81964ebe-00b1-7e1d-b0f9-43c29b6fb8f5`. |
| [`uuid_extract_timestamp(uuidv7)`](#uuid_extract_timestampuuidv7) | Extracts `TIMESTAMP WITH TIME ZONE` from a UUIDv7 value. |
| [`uuid_extract_version(uuid)`](#uuid_extract_versionuuid) | Extracts UUID version (`4` or `7`). |
| [`version()`](#version) | Return the currently active version of DuckDB in this format. |

#### `alias(column)`

<div class="nostroke_table"></div>

| **Description** | Return the name of the column. |
| **Example** | `alias(column1)` |
| **Result** | `column1` |

#### `can_cast_implicitly(source_value, target_value)`

<div class="nostroke_table"></div>

| **Description** | Whether or not we can implicitly cast from the types of the source value to the target value. |
| **Example** | `can_cast_implicitly(1::BIGINT, 1::SMALLINT)` |
| **Result** | `false` |

#### `checkpoint(database)`

<div class="nostroke_table"></div>

| **Description** | Synchronize WAL with file for (optional) database without interrupting transactions. |
| **Example** | `checkpoint(my_db)` |
| **Result** | success Boolean |

#### `coalesce(expr, ...)`

<div class="nostroke_table"></div>

| **Description** | Return the first expression that evaluates to a non-`NULL` value. Accepts 1 or more parameters. Each expression can be a column, literal value, function result, or many others. |
| **Example** | `coalesce(NULL, NULL, 'default_string')` |
| **Result** | `default_string` |

#### `constant_or_null(arg1, arg2)`

<div class="nostroke_table"></div>

| **Description** | If `arg2` is `NULL`, return `NULL`. Otherwise, return `arg1`. |
| **Example** | `constant_or_null(42, NULL)` |
| **Result** | `NULL` |

#### `count_if(x)`

<div class="nostroke_table"></div>

| **Description** | Aggregate function; rows contribute 1 if `x` is `true` or a non-zero number, else 0. |
| **Example** | `count_if(42)` |
| **Result** | 1 |

#### `create_sort_key(parameters...)`

<div class="nostroke_table"></div>

| **Description** | Constructs a binary-comparable sort key based on a set of input parameters and sort qualifiers. |
| **Example** | `create_sort_key('abc', 'ASC NULLS FIRST');` |
| **Result** | `\x02bcd\x00` |

#### `current_catalog()`

<div class="nostroke_table"></div>

| **Description** | Return the name of the currently active catalog. Default is memory. |
| **Example** | `current_catalog()` |
| **Result** | `memory` |

#### `current_database()`

<div class="nostroke_table"></div>

| **Description** | Return the name of the currently active database. |
| **Example** | `current_database()` |
| **Result** | `memory` |

#### `current_query()`

<div class="nostroke_table"></div>

| **Description** | Return the current query as a string. |
| **Example** | `current_query()` |
| **Result** | `SELECT current_query();` |

#### `current_schema()`

<div class="nostroke_table"></div>

| **Description** | Return the name of the currently active schema. Default is main. |
| **Example** | `current_schema()` |
| **Result** | `main` |

#### `current_schemas(boolean)`

<div class="nostroke_table"></div>

| **Description** | Return list of schemas. Pass a parameter of `true` to include implicit schemas. |
| **Example** | `current_schemas(true)` |
| **Result** | `['temp', 'main', 'pg_catalog']` |

#### `current_setting('setting_name')`

<div class="nostroke_table"></div>

| **Description** | Return the current value of the configuration setting. |
| **Example** | `current_setting('access_mode')` |
| **Result** | `automatic` |

#### `currval('sequence_name')`

<div class="nostroke_table"></div>

| **Description** | Return the current value of the sequence. Note that `nextval` must be called at least once prior to calling `currval`. |
| **Example** | `currval('my_sequence_name')` |
| **Result** | `1` |

#### `error(message)`

<div class="nostroke_table"></div>

| **Description** | Throws the given error `message`. |
| **Example** | `error('access_mode')` |

#### `equi_width_bins(min, max, bincount, nice := false)`

<div class="nostroke_table"></div>

| **Description** | Returns the upper boundaries of a partition of the interval `[min, max]` into `bin_count` equal-sized subintervals (for use with, e.g., [`histogram`]({% link docs/stable/sql/functions/aggregates.md %}#histogramargboundaries)). If `nice = true`, then `min`, `max`, and `bincount` may be adjusted to produce more aesthetically pleasing results.  |
| **Example** | `equi_width_bins(0.1, 2.7, 4, true)` |
| **Result** | `[0.5, 1.0, 1.5, 2.0, 2.5, 3.0]` |

#### `force_checkpoint(database)`

<div class="nostroke_table"></div>

| **Description** | Synchronize WAL with file for (optional) database interrupting transactions. |
| **Example** | `force_checkpoint(my_db)` |
| **Result** | success Boolean |

#### `gen_random_uuid()`

<div class="nostroke_table"></div>

| **Description** | Return a random UUID (UUIDv4) similar to this: `eeccb8c5-9943-b2bb-bb5e-222f4e14b687`. |
| **Example** | `gen_random_uuid()` |
| **Result** | various |

#### `getenv(var)`

| **Description** | Returns the value of the environment variable `var`. Only available in the [command line client]({% link docs/stable/clients/cli/overview.md %}). |
| **Example** | `getenv('HOME')` |
| **Result** | `/path/to/user/home` |

#### `hash(value)`

<div class="nostroke_table"></div>

| **Description** | Returns a `UBIGINT` with the hash of the `value`. The used hash function may change across DuckDB versions. |
| **Example** | `hash('🦆')` |
| **Result** | `2595805878642663834` |

#### `icu_sort_key(string, collator)`

<div class="nostroke_table"></div>

| **Description** | Surrogate [sort key](https://unicode-org.github.io/icu/userguide/collation/architecture.html#sort-keys) used to sort special characters according to the specific locale. Collator parameter is optional. Only available when the ICU extension is installed. |
| **Example** | `icu_sort_key('ö', 'DE')` |
| **Result** | `460145960106` |

#### `if(a, b, c)`

<div class="nostroke_table"></div>

| **Description** | Ternary conditional operator; returns b if a, else returns c. Equivalent to `CASE WHEN a THEN b ELSE c END`. |
| **Example** | `if(2 > 1, 3, 4)` |
| **Result** | `3` |

#### `ifnull(expr, other)`

<div class="nostroke_table"></div>

| **Description** | A two-argument version of coalesce. |
| **Example** | `ifnull(NULL, 'default_string')` |
| **Result** | `default_string` |

#### `is_histogram_other_bin(arg)`

<div class="nostroke_table"></div>

| **Description** | Returns `true` when `arg` is the "catch-all element" of its datatype for the purpose of the [`histogram_exact`]({% link docs/stable/sql/functions/aggregates.md %}#histogram_exactargelements) function, which is equal to the "right-most boundary" of its datatype for the purpose of the [`histogram`]({% link docs/stable/sql/functions/aggregates.md %}#histogramargboundaries) function. |
| **Example** | `is_histogram_other_bin('')` |
| **Result** | `true` |

#### `md5(string)`

<div class="nostroke_table"></div>

| **Description** | Returns the MD5 hash of the `string` as a `VARCHAR`. |
| **Example** | `md5('abc')` |
| **Result** | `900150983cd24fb0d6963f7d28e17f72` |

#### `md5_number(string)`

<div class="nostroke_table"></div>

| **Description** | Returns the MD5 hash of the `string` as a `UHUGEINT`. |
| **Example** | `md5_number('abc')` |
| **Result** | `152195979970564155685860391459828531600` |

#### `md5_number_lower(string)`

<div class="nostroke_table"></div>

| **Description** | Returns the lower 8 bytes of the MD5 hash of `string` as a `UBIGINT`. |
| **Example** | `md5_number_lower('abc')` |
| **Result** | `8250560606382298838` |

#### `md5_number_upper(string)`

<div class="nostroke_table"></div>

| **Description** | Returns the upper 8 bytes of the MD5 hash of `string` as a `UBIGINT`. |
| **Example** | `md5_number_upper('abc')` |
| **Result** | `12704604231530709392` |

#### `nextval('sequence_name')`

<div class="nostroke_table"></div>

| **Description** | Return the following value of the sequence. |
| **Example** | `nextval('my_sequence_name')` |
| **Result** | `2` |

#### `nullif(a, b)`

<div class="nostroke_table"></div>

| **Description** | Return `NULL` if a = b, else return a. Equivalent to `CASE WHEN a = b THEN NULL ELSE a END`. |
| **Example** | `nullif(1+1, 2)` |
| **Result** | `NULL` |

#### `pg_typeof(expression)`

<div class="nostroke_table"></div>

| **Description** | Returns the lower case name of the data type of the result of the expression. For PostgreSQL compatibility. |
| **Example** | `pg_typeof('abc')` |
| **Result** | `varchar` |

#### `query(query_string)`

<div class="nostroke_table"></div>

| **Description** | Table function that parses and executes the query defined in `query_string`. Only constant strings are allowed. Warning: this function allows invoking arbitrary queries, potentially altering the database state. |
| **Example** | `query('SELECT 42 AS x')` |
| **Result** | `42` |

#### `query_table(tbl_name)`

<div class="nostroke_table"></div>

| **Description** | Table function that returns the table given in `tbl_name`. |
| **Example** | `query_table('t1')` |
| **Result** | (the rows of `t1`) |

#### `query_table(tbl_names, [by_name])`

<div class="nostroke_table"></div>

| **Description** | Table function that returns the union of tables given in `tbl_names`. If the optional `by_name` parameter is set to `true`, it uses [`UNION ALL BY NAME`]({% link docs/stable/sql/query_syntax/setops.md %}#union-all-by-name) semantics. |
| **Example** | `query_table(['t1', 't2'])` |
| **Result** | (the union of the two tables) |

#### `read_blob(source)`

<div class="nostroke_table"></div>

| **Description** | Returns the content from `source` (a filename, a list of filenames, or a glob pattern) as a `BLOB`. See the [`read_blob` guide]({% link docs/stable/guides/file_formats/read_file.md %}#read_blob) for more details. |
| **Example** | `read_blob('hello.bin')` |
| **Result** | `hello\x0A` |

#### `read_text(source)`

<div class="nostroke_table"></div>

| **Description** | Returns the content from `source` (a filename, a list of filenames, or a glob pattern) as a `VARCHAR`. The file content is first validated to be valid UTF-8. If `read_text` attempts to read a file with invalid UTF-8 an error is thrown suggesting to use `read_blob` instead. See the [`read_text` guide]({% link docs/stable/guides/file_formats/read_file.md %}#read_text) for more details. |
| **Example** | `read_text('hello.txt')` |
| **Result** | `hello\n` |

#### `sha1(string)`

<div class="nostroke_table"></div>

| **Description** | Returns a `VARCHAR` with the SHA-1 hash of the `string`. |
| **Example** | `sha1('🦆')` |
| **Result** | `949bf843dc338be348fb9525d1eb535d31241d76` |

#### `sha256(string)`

<div class="nostroke_table"></div>

| **Description** | Returns a `VARCHAR` with the SHA-256 hash of the `string`. |
| **Example** | `sha256('🦆')` |
| **Result** | `d7a5c5e0d1d94c32218539e7e47d4ba9c3c7b77d61332fb60d633dde89e473fb` |

#### `stats(expression)`

<div class="nostroke_table"></div>

| **Description** | Returns a string with statistics about the expression. Expression can be a column, constant, or SQL expression. |
| **Example** | `stats(5)` |
| **Result** | `'[Min: 5, Max: 5][Has Null: false]'` |

#### `txid_current()`

<div class="nostroke_table"></div>

| **Description** | Returns the current transaction's identifier, a `BIGINT` value. It will assign a new one if the current transaction does not have one already. |
| **Example** | `txid_current()` |
| **Result** | various |

#### `typeof(expression)`

<div class="nostroke_table"></div>

| **Description** | Returns the name of the data type of the result of the expression. |
| **Example** | `typeof('abc')` |
| **Result** | `VARCHAR` |

#### `uuid()`

<div class="nostroke_table"></div>

| **Description** | Return a random UUID (UUIDv4) similar to this: `eeccb8c5-9943-b2bb-bb5e-222f4e14b687`. |
| **Example** | `uuid()` |
| **Result** | various |

#### `uuidv4()`

| **Description** | Return a random UUID (UUIDv4) similar to this: `eeccb8c5-9943-b2bb-bb5e-222f4e14b687`. |
| **Example** | `uuidv4()` |
| **Result** | various |

#### `uuidv7()`

| **Description** | Return a random UUIDv7 similar to this: `81964ebe-00b1-7e1d-b0f9-43c29b6fb8f5`. |
| **Example** | `uuidv7()` |
| **Result** | various |

#### `uuid_extract_timestamp(uuidv7)`

| **Description** | Extracts `TIMESTAMP WITH TIME ZONE` from a UUIDv7 value. |
| **Example** | `uuid_extract_timestamp(uuidv7())` |
| **Result** | `2025-04-19 15:51:20.07+00` |

#### `uuid_extract_version(uuid)`

| **Description** | Extracts UUID version (`4` or `7`). |
| **Example** | `uuid_extract_version(uuidv7())` |
| **Result** | `7` |

#### `version()`

<div class="nostroke_table"></div>

| **Description** | Return the currently active version of DuckDB in this format. |
| **Example** | `version()` |
| **Result** | various |

## Utility Table Functions

A [table function]({% link docs/stable/sql/query_syntax/from.md %}#table-functions) is used in place of a table in a `FROM` clause.

| Name | Description |
|:--|:-------|
| [`glob(search_path)`](#globsearch_path) | Return filenames found at the location indicated by the *search_path* in a single column named `file`. The *search_path* may contain [glob pattern matching syntax]({% link docs/stable/sql/functions/pattern_matching.md %}). |
| [`repeat_row(varargs, num_rows)`](#repeat_rowvarargs-num_rows) | Returns a table with `num_rows` rows, each containing the fields defined in `varargs`. |

#### `glob(search_path)`

<div class="nostroke_table"></div>

| **Description** | Return filenames found at the location indicated by the *search_path* in a single column named `file`. The *search_path* may contain [glob pattern matching syntax]({% link docs/stable/sql/functions/pattern_matching.md %}). |
| **Example** | `glob('*')` |
| **Result** | (table of filenames) |

#### `repeat_row(varargs, num_rows)`

<div class="nostroke_table"></div>

| **Description** | Returns a table with `num_rows` rows, each containing the fields defined in `varargs`. |
| **Example** | `repeat_row(1, 2, 'foo', num_rows = 3)` |
| **Result** | 3 rows of `1, 2, 'foo'` |
