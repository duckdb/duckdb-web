---
layout: docu
railroad: statements/alter.js
title: ALTER TABLE Statement
---

The `ALTER TABLE` statement changes the schema of an existing table in the catalog.

## Examples

```sql
CREATE TABLE integers (i INTEGER, j INTEGER);
```

Add a new column with name `k` to the table `integers`, it will be filled with the default value `NULL`:

```sql
ALTER TABLE integers ADD COLUMN k INTEGER;
```

Add a new column with name `l` to the table integers, it will be filled with the default value 10:

```sql
ALTER TABLE integers ADD COLUMN l INTEGER DEFAULT 10;
```

Drop the column `k` from the table integers:

```sql
ALTER TABLE integers DROP k;
```

Change the type of the column `i` to the type `VARCHAR` using a standard cast:

```sql
ALTER TABLE integers ALTER i TYPE VARCHAR;
```

Change the type of the column `i` to the type `VARCHAR`, using the specified expression to convert the data for each row:

```sql
ALTER TABLE integers ALTER i SET DATA TYPE VARCHAR USING concat(i, '_', j);
```

Set the default value of a column:

```sql
ALTER TABLE integers ALTER COLUMN i SET DEFAULT 10;
```

Drop the default value of a column:

```sql
ALTER TABLE integers ALTER COLUMN i DROP DEFAULT;
```

Make a column not nullable:

```sql
ALTER TABLE integers ALTER COLUMN i SET NOT NULL;
```

Drop the not-`NULL` constraint:

```sql
ALTER TABLE integers ALTER COLUMN i DROP NOT NULL;
```

Rename a table:

```sql
ALTER TABLE integers RENAME TO integers_old;
```

Rename a column of a table:

```sql
ALTER TABLE integers RENAME i TO ii;
```

Add a primary key to a column of a table:

```sql
ALTER TABLE integers ADD PRIMARY KEY (i);
```

## Syntax

<div id="rrdiagram"></div>

`ALTER TABLE` changes the schema of an existing table.
All the changes made by `ALTER TABLE` fully respect the transactional semantics, i.e., they will not be visible to other transactions until committed, and can be fully reverted through a rollback.

## `RENAME TABLE`

Rename a table:

```sql
ALTER TABLE integers RENAME TO integers_old;
```

The `RENAME TO` clause renames an entire table, changing its name in the schema. Note that any views that rely on the table are **not** automatically updated.

## `RENAME COLUMN`

Rename a column of a table:

```sql
ALTER TABLE integers RENAME i TO j;
ALTER TABLE integers RENAME COLUMN j TO k;
```

The `RENAME COLUMN` clause renames a single column within a table. Any constraints that rely on this name (e.g., `CHECK` constraints) are automatically updated. However, note that any views that rely on this column name are **not** automatically updated.

## `ADD COLUMN`

Add a new column with name `k` to the table `integers`, it will be filled with the default value NULL:

```sql
ALTER TABLE integers ADD COLUMN k INTEGER;
```

Add a new column with name `l` to the table integers, it will be filled with the default value 10:

```sql
ALTER TABLE integers ADD COLUMN l INTEGER DEFAULT 10;
```

The `ADD COLUMN` clause can be used to add a new column of a specified type to a table. The new column will be filled with the specified default value, or `NULL` if none is specified.

## `DROP COLUMN`

Drop the column `k` from the table `integers`:

```sql
ALTER TABLE integers DROP k;
```

The `DROP COLUMN` clause can be used to remove a column from a table. Note that columns can only be removed if they do not have any indexes that rely on them. This includes any indexes created as part of a `PRIMARY KEY` or `UNIQUE` constraint. Columns that are part of multi-column check constraints cannot be dropped either.
If you attempt to drop a column with an index on it, DuckDB will return the following error message:

```console
Dependency Error: Cannot alter entry "..." because there are entries that depend on it.
```

## `ALTER TYPE`

Change the type of the column `i` to the type `VARCHAR` using a standard cast:

```sql
ALTER TABLE integers ALTER i TYPE VARCHAR;
```

Change the type of the column `i` to the type `VARCHAR`, using the specified expression to convert the data for each row:

```sql
ALTER TABLE integers ALTER i SET DATA TYPE VARCHAR USING concat(i, '_', j);
```

The `SET DATA TYPE` clause changes the type of a column in a table. Any data present in the column is converted according to the provided expression in the `USING` clause, or, if the `USING` clause is absent, cast to the new data type. Note that columns can only have their type changed if they do not have any indexes that rely on them and are not part of any `CHECK` constraints.

## `SET` / `DROP DEFAULT`

Set the default value of a column:

```sql
ALTER TABLE integers ALTER COLUMN i SET DEFAULT 10;
```

Drop the default value of a column:

```sql
ALTER TABLE integers ALTER COLUMN i DROP DEFAULT;
```

The `SET/DROP DEFAULT` clause modifies the `DEFAULT` value of an existing column. Note that this does not modify any existing data in the column. Dropping the default is equivalent to setting the default value to NULL.

> Warning At the moment DuckDB will not allow you to alter a table if there are any dependencies. That means that if you have an index on a column you will first need to drop the index, alter the table, and then recreate the index. Otherwise, you will get a `Dependency Error`.

## `ADD PRIMARY KEY`

Add a primary key to a column of a table:

```sql
ALTER TABLE integers ADD PRIMARY KEY (i);
```

Add a primary key to multiple columns of a table:

```sql
ALTER TABLE integers ADD PRIMARY KEY (i, j);
```

## `ADD` / `DROP CONSTRAINT`

> `ADD CONSTRAINT` and `DROP CONSTRAINT` clauses are not yet supported in DuckDB.