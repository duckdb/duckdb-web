---
layout: docu
title: Information Schema
selected: Documentation/Information Schema
---
The views in the `information_schema` are SQL-standard views that describe the catalog entries of the database. These views can be filtered to obtain information about a specific column or table.

## Database, Catalog and Schema
The top level catalog view is `information_schema.schemata`. It lists the catalogs and the schemas present in the database and has the following layout:

| Column | Description | Type | Example |
|:---|:---|:---|:---|
| `catalog_name` |Name of the database that the schema is contained in. Not yet implemented. | `VARCHAR` | `NULL` |
| `schema_name` |Name of the schema. | `VARCHAR` | `'main'` |
| `schema_owner` |Name of the owner of the schema. Not yet implemented. | `VARCHAR` | `NULL` |
| `default_character_set_catalog` |Applies to a feature not available in DuckDB. | `VARCHAR` | `NULL` |
| `default_character_set_schema` |Applies to a feature not available in DuckDB. | `VARCHAR` | `NULL` |
| `default_character_set_name` |Applies to a feature not available in DuckDB. | `VARCHAR` | `NULL` |
| `sql_path` |The file system location of the database. Currently unimplemented. | `VARCHAR` | `NULL` |

## Tables and Views
The view that describes the catalog information for tables and views is `information_schema.tables`. It lists the tables present in the database and has the following layout:

| Column | Description | Type | Example |
|:---|:---|:---|:---|
| `table_catalog` |The catalog the table or view belongs to. Not yet implemented.| `VARCHAR` | `NULL` |
| `table_schema` |The schema the table or view belongs to.| `VARCHAR` | `'main'` |
| `table_name` |The name of the table or view.| `VARCHAR` | `'widgets'` |
| `table_type` |The type of table. One of: `BASE TABLE`, `LOCAL TEMPORARY`, `VIEW`.| `VARCHAR` | `'BASE TABLE'` |
| `self_referencing_column_name` |Applies to a feature not available in DuckDB.| `VARCHAR` | `NULL` |
| `reference_generation` |Applies to a feature not available in DuckDB.| `VARCHAR` | `NULL` |
| `user_defined_type_catalog` |If the table is a typed table, the name of the database that contains the underlying data type (always the current database), else null. Currently unimplemented.| `VARCHAR` | `NULL` |
| `user_defined_type_schema` |If the table is a typed table, the name of the schema that contains the underlying data type, else null. Currently unimplemented.| `VARCHAR` | `NULL` |
| `user_defined_type_name` |If the table is a typed table, the name of the underlying data type, else null. Currently unimplemented.| `VARCHAR` | `NULL` |
| `is_insertable_into` |`YES` if the table is insertable into, `NO` if not (Base tables are always insertable into, views not necessarily.)| `VARCHAR` | `'YES'` |
| `is_typed` |`YES` if the table is a typed table, `NO` if not.| `VARCHAR` | `'NO'` |
| `commit_action` |Not yet implemented.| `VARCHAR` | `'NO'` |

## Columns
The view that describes the catalog information for columns is `information_schema.columns`. It lists the column present in the database and has the following layout:

| Column | Description | Type | Example |
|:---|:---|:---|:---|
| `table_catalog` |Name of the database containing the table. Not yet implemented.| `VARCHAR` | `NULL` |
| `table_schema` |Name of the schema containing the table.| `VARCHAR` | `'main'` |
| `table_name` |Name of the table.| `VARCHAR` | `'widgets'` |
| `column_name` |Name of the column. | `VARCHAR` | `'price'` |
| `ordinal_position` |Ordinal position of the column within the table (count starts at 1). | `INTEGER` | `5` |
| `column_default` |Default expression of the column.|`VARCHAR`| `1.99` |
| `is_nullable` |`YES` if the column is possibly nullable, `NO` if it is known not nullable.|`VARCHAR`| `'YES'` |
| `data_type` |Data type of the column.|`VARCHAR`| `'DECIMAL(18,2)'` |
| `character_maximum_length` |If `data_type` identifies a character or bit string type, the declared maximum length; null for all other data types or if no maximum length was declared.|`INTEGER`| `255` |
| `character_octet_length` |If data_type identifies a character type, the maximum possible length in octets (bytes) of a datum; null for all other data types. The maximum octet length depends on the declared character maximum length (see above) and the character encoding.|`INTEGER`| `1073741824` |
| `numeric_precision` |If data_type identifies a numeric type, this column contains the (declared or implicit) precision of the type for this column. The precision indicates the number of significant digits. For all other data types, this column is null.|`INTEGER`| `18` |
| `numeric_scale` |If data_type identifies a numeric type, this column contains the (declared or implicit) scale of the type for this column. The precision indicates the number of significant digits. For all other data types, this column is null.|`INTEGER`| `2` |
| `datetime_precision` |If data_type identifies a date, time, timestamp, or interval type, this column contains the (declared or implicit) fractional seconds precision of the type for this column, that is, the number of decimal digits maintained following the decimal point in the seconds value. No fractional seconds are currently supported in DuckDB. For all other data types, this column is null.|`INTEGER`| `0` |

## Catalog Functions
Several functions are also provided to see details about the schemas that are configured in the database.

| Function | Description | Example | Result |
|:---|:---|:---|:---|
| `current_schema()` | Return the name of the currently active schema. Default is main. | `current_schema()` | `'main'` |
| `current_schemas(boolean)` | Return list of schemas. Pass a parameter of `True` to include implicit schemas. | `current_schemas(true)` | `['temp', 'main', 'pg_catalog']` |
