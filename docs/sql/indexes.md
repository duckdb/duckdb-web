---
layout: docu
title: Indexes
selected: Documentation/Indexes
---
An Adaptive Radix Tree is used as the index data structure of choice for DuckDB. Its mainly used to ensure primary key constraints and to speed up point and very highly selective (i.e., < 0.1%) queries. Note that an index is automatically created for columns with a UNIQUE or PRIMARY KEY constrain.

# Create Index
```sql
CREATE [ UNIQUE ] INDEX [ name ] ON table ({ column | ( expression )})
```
CREATE INDEX constructs an index on the specified column(s) of the specified table. We currently only support unidimensional indexes of the following types:

| Name | Aliases | Description |
|:---|:---|:---|
| bigint | int8 | signed eight-byte integer |
| integer | int, int4, signed | signed four-byte integer |
| smallint | int2 | signed two-byte integer|
| tinyint |   | signed one-byte integer|

### Parameters

| Name | Description |
|:---|:---|
|`UNIQUE`|Causes the system to check for duplicate values in the table when the index is created (if data already exist) and each time data is added. Attempts to insert or update data that would result in duplicate entries will generate an error.|
|`name`|The name of the index to be created.|
|`table`|The name of the table to be indexed.|
|`column`|The name of the column to be indexed.|
|`expression`|An expression based on one or more columns of the table. The expression usually must be written with surrounding parentheses, as shown in the syntax. However, the parentheses can be omitted if the expression has the form of a function call.|


### Examples

```sql
-- Create an unique index 'films_id_idx' on the column id of table films.
CREATE UNIQUE INDEX films_id_idx ON films (id);
-- Creates index 's_idx' that allows for duplicate values on column revenue of table films.
CREATE INDEX revenue_idx ON films (revenue);
-- Create index 'i_index' on the expression of the sum of columns j and k from table integers.
CREATE INDEX i_index ON integers ((j+k))
```

# Drop Index
```sql
DROP INDEX [ IF EXISTS ] name
```

DROP INDEX drops an existing index from the database system.


### Parameters

| Name | Description |
|:---|:---|
|`IF EXISTS`|Do not throw an error if the index does not exist.|
|`name`|The name of an index to remove.|

### Examples

```sql
-- Remove the index title_idx.
DROP INDEX title_idx;
```
