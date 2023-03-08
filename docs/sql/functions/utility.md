---
layout: docu
title: Utility Functions
selected: Documentation/Functions/Utility Functions
expanded: Functions
---

## Utility Functions
The functions below are difficult to categorize into specific function types and are broadly useful. 

| Function | Description | Example | Result |
|:---|:---|:---|:---|
| `alias(column)` | Return the name of the column | `alias(column1)` | `'column1'` |
| `coalesce(expr, ...)` | Return the first expression that evaluates to a non-`NULL` value. Accepts 1 or more parameters. Each expression can be a column, literal value, function result, or many others.  | `coalesce(NULL,NULL,'default_string')` | `'default_string'` |
| `current_schema()` | Return the name of the currently active schema. Default is main. | `current_schema()` | `'main'` |
| `current_schemas(boolean)` | Return list of schemas. Pass a parameter of `True` to include implicit schemas. | `current_schemas(true)` | `['temp', 'main', 'pg_catalog']` |
| `current_setting('setting_name')` | Return the current value of the configuration setting | `current_setting('access_mode')` | `'automatic'` |
| `currval('sequence_name')` | Return the current value of the sequence. Note that `nextval` must be called at least once prior to calling `currval`. | `currval('my_sequence_name')` | `1` |
| `gen_random_uuid()` | Alias of `uuid`. Return a random uuid similar to this: eeccb8c5-9943-b2bb-bb5e-222f4e14b687. | `gen_random_uuid()` | various |
| `hash(`*`value`*`)` | Returns an integer with the hash of the _value_ | `hash('🦆')` | `2595805878642663834` |
| `icu_sort_key(string , collator)` | Surrogate key used to sort special characters according to the specific locale. Collator parameter is optional. Valid only when ICU extension is installed. | `icu_sort_key('ö','DE')` | 460145960106 |
| `md5(string)` | Return an md5 one-way hash of the *string*. | `md5('123')` | `'202cb962ac59075b964b07152d234b70'` |
| `nextval('sequence_name')` | Return the following value of the sequence. | `nextval('my_sequence_name')` | `2` |
| `pg_typeof(expression)` | Returns the lower case name of the data type of the result of the expression. For Postgres compatibility. | `pg_typeof('abc')` | `'varchar'` |
| `stats(expression)` | Returns a string with statistics about the expression. Expression can be a column, constant, or SQL expression. | `stats(5)` | `'[Min: 5, Max: 5][Has Null: false]'` |
| `txid_current()` | Returns the current transaction's ID (a `BIGINT`). It will assign a new one if the current transaction does not have one already. | `txid_current()` | various |
| `typeof(expression)` | Returns the name of the data type of the result of the expression. | `typeof('abc')` | `'VARCHAR'` |
| `uuid()` | Return a random uuid similar to this: eeccb8c5-9943-b2bb-bb5e-222f4e14b687. | `uuid()` | various |
| `version()` | Return the currently active version of DuckDB in this format: `v0.3.2` | `version()` | various |
