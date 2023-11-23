---
layout: docu
title: Create Index
railroad: statements/indexes.js
---

## `CREATE INDEX`

The `CREATE INDEX` statement constructs an index on the specified column(s) of the specified table. Compound indexes on multiple columns/expressions are supported.

> Unidimensional indexes are supported, while multidimensional indexes are not yet supported.

### Examples

```sql
-- Create a unique index 'films_id_idx' on the column id of table films.
CREATE UNIQUE INDEX films_id_idx ON films (id);
-- Create index 's_idx' that allows for duplicate values on column revenue of table films.
CREATE INDEX s_idx ON films (revenue);
-- Create compound index 'gy_idx' on genre and year columns.
CREATE INDEX gy_idx ON films (genre, year);
-- Create index 'i_index' on the expression of the sum of columns j and k from table integers.
CREATE INDEX i_index ON integers ((j + k));
```

### Parameters

<div class="narrow_table"></div>

| Name | Description |
|:-|:-----|
|`UNIQUE`|Causes the system to check for duplicate values in the table when the index is created (if data already exist) and each time data is added. Attempts to insert or update data that would result in duplicate entries will generate an error.|
|`name`|The name of the index to be created.|
|`table`|The name of the table to be indexed.|
|`column`|The name of the column to be indexed.|
|`expression`|An expression based on one or more columns of the table. The expression usually must be written with surrounding parentheses, as shown in the syntax. However, the parentheses can be omitted if the expression has the form of a function call.|

### Syntax

<div id="rrdiagram1"></div>

## `DROP INDEX`

`DROP INDEX` drops an existing index from the database system.

### Examples

```sql
-- Remove the index title_idx.
DROP INDEX title_idx;
```

### Parameters

<div class="narrow_table"></div>

| Name | Description |
|:---|:---|
|`IF EXISTS`|Do not throw an error if the index does not exist.|
|`name`|The name of an index to remove.|

### Syntax

<div id="rrdiagram2"></div>
