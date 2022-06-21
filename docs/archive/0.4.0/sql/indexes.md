---
layout: docu
title: Indexes
selected: Documentation/Indexes
railroad: statements/indexes.js
---
## Index types

DuckDB currently uses two index types:

* A [min-max index](https://en.wikipedia.org/wiki/Block_Range_Index) is automatically created for columns of all [general-purpose data types](../sql/data_types/overview).
* An [Adaptive Radix Tree (ART)](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.674.248&rep=rep1&type=pdf) is mainly used to ensure primary key constraints and to speed up point and very highly selective (i.e., < 0.1%) queries. Such an index is automatically created for columns with a `UNIQUE` or `PRIMARY KEY` constraint and can be defined using `CREATE INDEX`.

Joins on columns with an ART index can make use of the [index join algorithm](https://en.wikipedia.org/wiki/Nested_loop_join#Index_join_variation). Forcing index joins is possible using [pragmas](../sql/pragmas).

## Persistence

* Min-max indexes are persisted.
* Currently, ART indexes are [not persisted](https://github.com/duckdb/duckdb/issues/693). Unique and primary key indexes are rebuilt upon startup, while user-defined indexes are discarded.

## Create Index

<div id="rrdiagram1"></div>

`CREATE INDEX` constructs an index on the specified column(s) of the specified table. Compound indexes on multiple columns/expressions are supported. Currently unidimensional indexes are supported, [multidimensional indexes are not supported](https://github.com/duckdb/duckdb/issues/63).

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
-- Create index 's_idx' that allows for duplicate values on column revenue of table films.
CREATE INDEX revenue_idx ON films (revenue);
-- Create compound index 'gy_idx' on genre and year columns.
CREATE INDEX gy_idx ON films (genre, year);
-- Create index 'i_index' on the expression of the sum of columns j and k from table integers.
CREATE INDEX i_index ON integers ((j+k))
```

## Drop Index

<div id="rrdiagram2"></div>

`DROP INDEX` drops an existing index from the database system.


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
