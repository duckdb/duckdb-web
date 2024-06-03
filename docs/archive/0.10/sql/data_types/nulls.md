---
blurb: The NULL value represents a missing value.
layout: docu
title: NULL Values
---

`NULL` values are special values that are used to represent missing data in SQL. Columns of any type can contain `NULL` values. Logically, a `NULL` value can be seen as "the value of this field is unknown".

A `NULL` value can be inserted to any field that does not have the `NOT NULL` qualifier:

```sql
CREATE TABLE integers (i INTEGER);
INSERT INTO integers VALUES (NULL);
```

`NULL` values have special semantics in many parts of the query as well as in many functions:

> Any comparison with a `NULL` value returns `NULL`, including `NULL = NULL`.

You can use `IS NOT DISTINCT FROM` to perform an equality comparison where `NULL` values compare equal to each other. Use `IS (NOT) NULL` to check if a value is `NULL`.

```sql
SELECT NULL = NULL;
```

```text
NULL
```

```sql
SELECT NULL IS NOT DISTINCT FROM NULL;
```

```text
true
```

```sql
SELECT NULL IS NULL;
```

```text
true
```

## NULL and Functions

A function that has input argument as `NULL` **usually** returns `NULL`.

```sql
SELECT cos(NULL);
```

```text
NULL
```

The `coalesce` function is an exception to this: it takes any number of arguments, and returns for each row the first argument that is not `NULL`. If all arguments are `NULL`, `coalesce` also returns `NULL`.

```sql
SELECT coalesce(NULL, NULL, 1);
```

```text
1
```

```sql
SELECT coalesce(10, 20);
```

```text
10
```

```sql
SELECT coalesce(NULL, NULL);
```

```text
NULL
```

The `ifnull` function is a two-argument version of `coalesce`.

```sql
SELECT ifnull(NULL, 'default_string');
```

```text
default_string
```

```sql
SELECT ifnull(1, 'default_string');
```

```text
1
```

## `NULL` and Conjunctions

`NULL` values have special semantics in `AND`/`OR` conjunctions. For the ternary logic truth tables, see the [Boolean Type documentation](../../sql/data_types/boolean).

## `NULL` and Aggregate Functions

`NULL` values are ignored in most aggregate functions.

Aggregate functions that do not ignore `NULL` values include: `first`, `last`, `list`, and `array_agg`. To exclude `NULL` values from those aggregate functions, the [`FILTER` clause](../../sql/query_syntax/filter) can be used.

```sql
CREATE TABLE integers (i INTEGER);
INSERT INTO integers VALUES (1), (10), (NULL);
```

```sql
SELECT min(i) FROM integers;
```

```text
1
```

```sql
SELECT max(i) FROM integers;
```

```text
10
```