---
layout: docu
title: DuckDB_% Metadata Functions
selected: Documentation/Metadata Functions
---
DuckDB offers a collection of table functions that provide metadata about the current database. These functions reside in the `main` schema and their names are prefixed with `duckdb_`. 

The resultset returned by a `duckdb_` table function may be used just like an ordinary table or view. For example, you can use a `duckdb_` function call in the `FROM` clause of a `SELECT` statement, and you may refer to the columns of its returned resultset elsewhere in the statement, for example in the `WHERE` clause.

Table functions are still functions, and you should write parenthesis after the function name to call it to obtain its returned resultset: 

`SELECT * FROM duckdb_settings()`

Alternatively, you may execute table functions also using the `CALL`-syntax:

`CALL duckdb_settings()`

In this case too, the parentheses are mandatory. 

Note: For some of the `duckdb_%` functions, there is also a identically named view available, which also resides in the `main` schema. Typically, these views do a `SELECT` on the `duckdb_` table function with the same name, while filtering out those objects that are marked as internal. We mention it here, because if you accidentally omit the parentheses in your `duckdb_` table function call, you might still get a result, but from the identically named view. 

Example:

```sql
-- duckdb_views table function: returns all views, including those marked internal
SELECT *
FROM   duckdb_views()
;
-- duckdb_views view: returns views that are not marked as internal
SELECT *
FROM   duckdb_views
;
```

## duckdb_columns
The `duckdb_columns()` function provides metadata about the columns available in the DuckDB instance.

| Column | Description | Type |
|:---|:---|:---|
| `database_name` | The name of the database that contains the column object. | VARCHAR |
| `database_oid` | Internal identifier of the database that contains the column object. | BIGINT |
| `schema_name` |The SQL name of the schema that contains the table object that defines this column.| `VARCHAR` |
| `schema_oid` |Internal identifier of the schema object that contains the table of the column.| `BIGINT` |
| `table_name` |The SQL name of the table that defines the column.| `VARCHAR` |
| `table_oid` |Internal identifier (name) of the table object that defines the column.| `BIGINT` |
| `column_name` |The SQL name of the column.| `VARCHAR` |
| `column_index` |The unique position of the column within its table.| `INTEGER` |
| `internal` |`true` if this column built-in, `false` if it is user-defined.| `BOOLEAN` |
| `column_default` |The default value of the column (expressed in SQL)| `VARCHAR` |
| `is_nullable` |`true` if the column can hold `NULL` values; `false` if the column cannot hold `NULL`-values.| `BOOLEAN` |
| `data_type` |The name of the column datatype.| `VARCHAR` |
| `data_type_id` |The internal identifier of the column data type| `BIGINT` |
| `character_maximum_length` |Always `NULL`. DuckDB [text types](./data_types/text) do not enforce a value length restriction based on a length type parameter.| `INTEGER` |
| `numeric_precision` |The number of units (in the base indicated by `numeric_precision_radix`) used for storing column values. For integral and approximate numeric types, this is the number of bits. For decimal types, this is the number of digits positions.| `INTEGER` |
| `numeric_precision_radix` |The number-base of the units in the `numeric_precision` column. For integral and approximate numeric types, this is `2`, indicating the precision is expressed as a number of bits. For the `decimal` type this is `10`, indicating the precision is expressed as a number of decimal positions.| `INTEGER` |
| `numeric_scale` |Applicable to `decimal` type. Indicates the maximum number of fractional digits (i.e. the number of digits that may appear after the decimal separator). | `INTEGER` |

The [`information_schema.columns`](./information_schema#columns) system view provides a more standardized way to obtain metadata about database columns, but the `duckdb_columns` function also returns metadata about DuckDB internal objects. (In fact, `information_schema.columns` is implemented as a query on top of `duckdb_columns()`)

## duckdb_constraints
The `duckdb_constraints()` function provides metadata about the constraints available in the DuckDB instance.

| Column | Description | Type |
|:---|:---|:---|
| `database_name` | The name of the database that contains the constraint. | VARCHAR |
| `database_oid` | Internal identifier of the database that contains the constraint. | BIGINT |
| `schema_name` |The SQL name of the schema that contains the table on which the constraint is defined.| `VARCHAR` |
| `schema_oid` |Internal identifier of the schema object that contains the table on which the constraint is defined.| `BIGINT` |
| `table_name` |The SQL name of the table on which the constraint is defined.| `VARCHAR` |
| `table_oid` |Internal identifier (name) of the table object on which the constraint is defined.| `BIGINT` |
| `constraint_index` |Indicates the position of the constraint as it appears in its table definition.| `BIGINT` |
| `constraint_type` |Indicates the type of constraint. Applicable values are `CHECK`, `FOREIGN KEY`, `PRIMARY KEY`, `NOT NULL`, `UNIQUE`. | `VARCHAR` |
| `constraint_text` |The definition of the constraint expressed as a SQL-phrase. (Not necessarily a complete or syntactically valid DDL-statement.)| `VARCHAR` |
| `expression` |If constraint is a check constraint, the definition of the condition being checked, otherwise `NULL`.| `VARCHAR` |
| `constraint_column_indexes` |An array of table column indexes referring to the columns that appear in the constraint definition| `BIGINT[]` |
| `constraint_column_names` |An array of table column names appearing in the constraint definition| `VARCHAR[]` |

## duckdb_databases
The `duckdb_databases()` function lists the databases that are accessible from within the current DuckDB process.
Apart from the database associated at startup, the list also includes databases that were [attached](./statements/attach.html) later on to the duckdb process

| Column | Description | Type |
|:---|:---|:---|
| `database_name` | The name of the database, or the alias if the database was attached using an ALIAS-clause. | VARCHAR |
| `database_oid` | The internal identifier of the database. | VARCHAR |
| `path` | The file path associated with the database. | VARCHAR |
| `internal` | True indicates a system or built-in database. False indicates a user-defined database. | BOOLEAN
| `type` | The type indicates the type of RDBMS implemented by the attached database. For DuckDB databases, that value is `duckdb`. 

## duckdb_dependencies
The `duckdb_dependencies()` function provides metadata about the dependencies available in the DuckDB instance.

| Column | Description | Type |
|:---|:---|:---|
| `classid` |Always 0| `BIGINT` |
| `objid` |The internal id of the object.| `BIGINT` |
| `objsubid` |Always 0| `INTEGER` |
| `refclassid` |Always 0| `BIGINT` |s
| `refobjid` |The internal id of the dependent object.| `BIGINT` |
| `refobjsubid` |Always 0| `INTEGER` |
| `deptype` |The type of dependency. Either regular (n) or automatic (a).| `VARCHAR` |

## duckdb_extensions
The `duckdb_extensions()` function provides metadata about the extensions available in the DuckDB instance.

| Column | Description | Type |
|:---|:---|:---|
| `extension_name` |The name of the extension.| `VARCHAR` |
| `loaded` |`true` if the extension is loaded, `false` if it's not loaded.| `BOOLEAN` |
| `installed` |`true` if the extension is installed, `false` if it's not installed.| `BOOLEAN` |
| `install_path` |`(BUILT-IN)` if the extension is built-in, otherwise, the filesystem path where binary that implements the extension resides.| `VARCHAR` |
| `description` |Human readable text that describes the extension's functionality.| `VARCHAR` |
| `aliases` |List of alternative names for this extension.| `VARCHAR[]` |

## duckdb_functions
The `duckdb_functions()` function provides metadata about the functions available in the DuckDB instance.

| Column | Description | Type |
|:---|:---|:---|
| `database_name` |The name of the database that contains this function.| `VARCHAR` |
| `schema_name` |The SQL name of the schema where the function resides.| `VARCHAR` |
| `function_name` |The SQL name of the function.| `VARCHAR` |
| `function_type` |The function kind. Value is one of: `table`,`scalar`,`aggregate`,`pragma`,`macro`| `VARCHAR` |
| `description` |Description of this function (always `NULL`)| `VARCHAR` |
| `return_type` |The logical data type name of the returned value. Applicable for scalar and aggregate functions.| `VARCHAR` |
| `parameters` |If the function has parameters, the list of parameter names.| `VARCHAR[]` |
| `parameter_types` |If the function has parameters, a list of logical data type names corresponding to the parameter list.| `VARCHAR[]` |
| `varargs` |The name of the data type in case the function has a variable number of arguments, or `NULL` if the function does not have a variable number of arguments.| `VARCHAR` |
| `macro_definition` |If this is a [macro](./statements/create_macro), the SQL expression that defines it.| `VARCHAR` |
| `has_side_effects` |`false` if this is a pure function. `true` if this function changes the database state (like sequence funtions `nextval()` and `curval()`).| `BOOLEAN` |
| `function_oid` | The internal identifier for this function | BIGINT |

## duckdb_indexes
The `duckdb_indexes()` function provides metadata about secondary indexes available in the DuckDB instance.

| Column | Description | Type |
|:---|:---|:---|
| `database_name` |The name of the database that contains this index.| `VARCHAR` |
| `database_oid` | Internal identifier of the database containing the index. | BIGINT |
| `schema_name` |The SQL name of the schema that contains the table with the secondary index.| `VARCHAR` |
| `schema_oid` |Internal identifier of the schema object.| `BIGINT` |
| `index_name` |The SQL name of this secondary index| `VARCHAR` |
| `index_oid` |The object identifier of this index.| `BIGINT` |
| `table_name` |The name of the table with the index| `VARCHAR` |
| `table_oid` | Internal identifier (name) of the table object.| `BIGINT` |
| `is_unique` |`true` if the index was created with the `UNIQUE` modifier, `false` if it was not.| `BOOLEAN` |
| `is_primary` |Always `false`| `BOOLEAN` |
| `expressions` |Always `NULL`| `VARCHAR` |
| `sql` |The definition of the index, expressed as a `CREATE INDEX` SQL statement.| `VARCHAR` |
  
Note that `duckdb_indexes` only provides metadata about secondary indexes - i.e. those indexes created by explicit [`CREATE INDEX`](./indexes#create-index) statements. Primary keys are maintained using indexes, but their details are included in the `duckdb_constraints()` function. 

## duckdb_keywords
The `duckdb_keywords()` function provides metadata about DuckDB's keywords and reserved words.

| Column | Description | Type |
|:---|:---|:---|
| `keyword_name` |The keyword.| `VARCHAR` |
| `keyword_category` |Indicates the category of the keyword. Values are `column_name`, `reserved`, `type_function` and `unreserved`. | `VARCHAR` |

## duckdb_schemas
The `duckdb_schemas()` function provides metadata about the schemas available in the DuckDB instance.

| Column | Description | Type |
|:---|:---|:---|
| `oid` |Internal identifier of the schema object.| `BIGINT` |
| `database_name` |The name of the database that contains this schema.| `VARCHAR` |
| `database_oid` | Internal identifier of the database containing the schema. | BIGINT |
| `schema_name` |The SQL name of the schema.| `VARCHAR` |
| `internal` |`true` if this is an internal (built-in) schema, `false` if this is a user-defined schema.| `BOOLEAN` |
| `sql` |Always `NULL`| `VARCHAR` |

The [`information_schema.schemata`](./information_schema) system view provides a more standardized way to obtain metadata about database schemas.

## duckdb_sequences
The `duckdb_sequences()` function provides metadata about the sequences available in the DuckDB instance.

| Column | Description | Type |
|:---|:---|:---|
| `database_name` |The name of the database that contains this sequence | `VARCHAR` |
| `database_oid` | Internal identifier of the database containing the sequence. | `BIGINT` |
| `schema_name` |The SQL name of the schema that contains the sequence object.| `VARCHAR` |
| `schema_oid` |Internal identifier of the schema object that contains the sequence object.| `BIGINT` |
| `sequence_name` |The SQL name that identifies the sequence within the schema.| `VARCHAR` |
| `sequence_oid` |The internal identifier of this sequence object.| `BIGINT` |
| `temporary` |Wheter this sequence is temporary. Temporary sequences are transient and only visible within the current connection.| `BOOLEAN` |
| `start_value` |The initial value of the sequence. This value will be returned when `nextval()` is called for the very first time on this sequence.| `BIGINT` |
| `min_value` |The minimum value of the sequence.| `BIGINT` |
| `max_value` |The maximum value of the sequence.| `BIGINT` |
| `increment_by` |The value that is added to the current value of the sequence to draw the next value from the sequence.| `BIGINT` |
| `cycle` |Whether the sequence should start over when drawing the next value would result in a value outside the range.| `BOOLEAN` |
| `last_value` |`null` if no value was ever drawn from the sequence using `nextval(...)`. `1` if a value was drawn.| `BIGINT` |
| `sql` |The definition of this object, expressed as SQL DDL-statement.| `VARCHAR` |

Attributes like `temporary`, `start_value` etc. correspond to the various options available in the [`create sequence`](./statements/create_sequence.html) statement and are documented there in full. Note that the attributes will always be filled out in the `duckdb_sequences` resultset, even if they were not explicitly specified in the `create sequence` statement.
Note1: The column name `last_value` suggests that it contains the last value that was drawn from the sequence, but that is not the case. It's either `null` if a value was never drawn from the sequence, or `1` (when there was a value drawn, ever, from the sequence).
Note2: If the sequence cycles, then the sequence will start over from the boundary of its range, not necessarily from the value specified as start value.

## duckdb_settings
The `duckdb_settings()` function provides metadata about the settings available in the DuckDB instance. 

| Column | Description | Type |
|:---|:---|:---|
| `name` |Name of the setting.| `VARCHAR` |
| `value` |Current value of the setting.| `VARCHAR` |
| `description` |A description of the setting.| `VARCHAR` |
| `input_type` |The logical datatype of the setting's value.| `VARCHAR` |

The various settings are described in the [configuration page](./configuration).

## duckdb_tables
The `duckdb_tables()` function provides metadata about the base tables available in the DuckDB instance.

| Column | Description | Type |
|:---|:---|:---|
| `database_name` |The name of the database that contains this table | `VARCHAR` |
| `database_oid` | Internal identifier of the database containing the table. | `BIGINT` |
| `schema_name` |The SQL name of the schema that contains the base table.| `VARCHAR` |
| `schema_oid` |Internal identifier of the schema object that contains the base table.| `BIGINT` |
| `table_name` |The SQL name of the base table.| `VARCHAR` |
| `table_oid` |Internal identifier of the base table object.| `BIGINT` |
| `internal` |`false` if this is a user-defined table. | `BOOLEAN` |
| `temporary` |Wheter this is a temporary table. Temporary tables are not persisted and only visible within the current connection.| `BOOLEAN` |
| `has_primary_key` |`true` if this table object defines a `PRIMARY KEY`.| `BOOLEAN` |
| `estimated_size` |The estimated number of rows in the table.| `BIGINT` |
| `column_count` |The number of columns defined by this object| `BIGINT` |
| `index_count` |The number of indexes associated with this table. This number includes all secondary indexes, as well as internal indexes generated to maintain `PRIMARY KEY` and/or `UNIQUE` constraints.| `BIGINT` |
| `check_constraint_count` |The number of check constraints active on columns within the table.| `BIGINT` |
| `sql` |The definition of this object, expressed as SQL [`CREATE TABLE`-statement](./statements/create_table).| `VARCHAR` |

The [`information_schema.tables`](./information_schema#tables) system view provides a more standardized way to obtain metadata about database tables that also includes views. But the resultset returned by `duckdb_tables` contains a few columns that are not included in `information_schema.tables`.

## duckdb_types
The `duckdb_types()` function provides metadata about the data types available in the DuckDB instance.

| Column | Description | Type |
|:---|:---|:---|
| `database_name` |The name of the database that contains this schema. | `VARCHAR` |
| `database_oid` | Internal identifier of the database that contains- the data type. | BIGINT |
| `schema_name` |The SQL name of the schema containing the type definition. Always `main`.| `VARCHAR` |
| `schema_oid` |Internal identifier of the schema object.| `BIGINT` |
| `type_name` |The name or alias of this data type.| `VARCHAR` |
| `type_oid` |The internal identifier of the data type object. If `NULL`, then this is an alias of the type (as identified by the value in the `logical_type` column).| `BIGINT` |
| `type_size` |The number of bytes required to represent a value of this type in memory.| `BIGINT` |
| `logical_type` |The 'canonical' name of this data type. The same `logical_type` may be referenced by several types having different `type_name`s. | `VARCHAR` |
| `type_category` |The category to which this type belongs. Data types within the same category generally expose similar behavior when values of this type are used in expression. For example, the `NUMERIC` type_category includes integers, decimals, and floating point numbers. | `VARCHAR` |
| `internal` |Whether this is an internal (built-in) or a user object.| `BOOLEAN` |

## duckdb_views
The `duckdb_views()` function provides metadata about the views available in the DuckDB instance.

| Column | Description | Type |
|:---|:---|:---|
| `database_name` |The name of the database that contains this view| `VARCHAR` |
| `database_oid` | Internal identifier of the database that contains this view. | BIGINT |
| `schema_name` |The SQL name of the schema where the view resides.| `VARCHAR` |
| `schema_oid` |Internal identifier of the schema object that contains the view.| `BIGINT` |
| `view_name` |The SQL name of the view object.| `VARCHAR` |
| `view_oid` |The internal identifier of this view object.| `BIGINT` |
| `internal` |`true` if this is an internal (built-in) view, `false` if this is a user-defined view.| `BOOLEAN` |
| `temporary` |`true` if this is a temporary view. Temporary views are not persistent and are only visible within the current connection.| `BOOLEAN` |
| `column_count` |The number of columns defined by this view object.| `BIGINT` |
| `sql` |The definition of this object, expressed as SQL DDL-statement.| `VARCHAR` |

The [`information_schema.tables`](./information_schema#tables) system view provides a more standardized way to obtain metadata about database views that also includes base tables. But the resultset returned by `duckdb_views` contains also definitions of internal view objects as well as a few columns that are not included in `information_schema.tables`.
