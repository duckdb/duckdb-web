---
layout: docu
railroad: statements/indexes.js
title: CREATE INDEX Statement
---

## `CREATE INDEX`

The `CREATE INDEX` statement constructs an index on the specified column(s) of the specified table. Compound indexes on multiple columns/expressions are supported.

> Unidimensional indexes are supported, while multidimensional indexes are not yet supported.

### Examples

Create a unique index `films_id_idx` on the column id of table `films`:

```sql
CREATE UNIQUE INDEX films_id_idx ON films (id);
```

Create index `s_idx` that allows for duplicate values on column `revenue` of table `films`:

```sql
CREATE INDEX s_idx ON films (revenue);
```

Create compound index `gy_idx` on `genre` and `year` columns:

```sql
CREATE INDEX gy_idx ON films (genre, year);
```

Create index `i_index` on the expression of the sum of columns `j` and `k` from table `integers`:

```sql
CREATE INDEX i_index ON integers ((j + k));
```

### Parameters

| Name | Description |
|:-|:-----|
| `UNIQUE` | Causes the system to check for duplicate values in the table when the index is created (if data already exist) and each time data is added. Attempts to insert or update data that would result in duplicate entries will generate an error. |
| `name` | The name of the index to be created. |
| `table` | The name of the table to be indexed. |
| `column` | The name of the column to be indexed. |
| `expression` | An expression based on one or more columns of the table. The expression usually must be written with surrounding parentheses, as shown in the syntax. However, the parentheses can be omitted if the expression has the form of a function call. |
| `index type` | Specified index type, see [Indexes]({% link docs/archive/1.1/sql/indexes.md %}). Optional. |
| `option` | Index option in the form of a Boolean true value (e.g., `is_cool`) or a key-value pair (e.g., `my_option = 2`). Optional. |

### Syntax

<div id="rrdiagram1"></div>

## `DROP INDEX`

`DROP INDEX` drops an existing index from the database system.

### Examples

Remove the index `title_idx`:

```sql
DROP INDEX title_idx;
```

### Parameters

| Name | Description |
|:---|:---|
| `IF EXISTS` | Do not throw an error if the index does not exist. |
| `name` | The name of an index to remove. |

### Syntax

<div id="rrdiagram2"></div>