---
layout: docu
title: Set Operations
railroad: query_syntax/setops.js
---

Set operations allow queries to be combined according to [set operation semantics](https://en.wikipedia.org/wiki/Set_(mathematics)#Basic_operations). Set operations refer to the [`UNION [ALL]`](#union), [`INTERSECT [ALL]`](#intersect) and [`EXCEPT [ALL]`](#except) clauses. The vanilla variants use set semantics, i.e., they eliminate duplicates, while the variants with `ALL` use bag semantics.

Traditional set operations unify queries **by column position**, and require the to-be-combined queries to have the same number of input columns. If the columns are not of the same type, casts may be added.  The result will use the column names from the first query.

DuckDB also supports [`UNION [ALL] BY NAME`](#union-all-by-name), which joins columns by name instead of by position. `UNION BY NAME` does not require the inputs to have the same number of columns. `NULL` values will be added in case of missing columns.

## `UNION`

The `UNION` clause can be used to combine rows from multiple queries. The queries are required to have the same number of columns and the same column types.

### Vanilla `UNION` (Set Semantics)

The vanilla `UNION` clause follows set semantics, therefore it performs duplicate elimination, i.e., only unique rows will be included in the result.

```sql
SELECT * FROM range(2) t1(x)
UNION
SELECT * FROM range(3) t2(x);
```

| x |
|--:|
| 2 |
| 1 |
| 0 |

### `UNION ALL` (Bag Semantics)

`UNION ALL` returns all rows of both queries following bag semantics, i.e., *without* duplicate elimination.

```sql
SELECT * FROM range(2) t1(x)
UNION ALL
SELECT * FROM range(3) t2(x);
```

| x |
|--:|
| 0 |
| 1 |
| 0 |
| 1 |
| 2 |

### `UNION [ALL] BY NAME`

The `UNION [ALL] BY NAME` clause can be used to combine rows from different tables by name, instead of by position. `UNION BY NAME` does not require both queries to have the same number of columns. Any columns that are only found in one of the queries are filled with `NULL` values for the other query.

Take the following tables for example:

```sql
CREATE TABLE capitals (city VARCHAR, country VARCHAR);
INSERT INTO capitals VALUES
    ('Amsterdam', 'NL'),
    ('Berlin', 'Germany');
CREATE TABLE weather (city VARCHAR, degrees INTEGER, date DATE);
INSERT INTO weather VALUES
    ('Amsterdam', 10, '2022-10-14'),
    ('Seattle', 8, '2022-10-12');
```

```sql
SELECT * FROM capitals
UNION BY NAME
SELECT * FROM weather;
```

|   city    | country | degrees |    date    |
|-----------|---------|--------:|------------|
| Seattle   | NULL    | 8       | 2022-10-12 |
| Amsterdam | NL      | NULL    | NULL       |
| Berlin    | Germany | NULL    | NULL       |
| Amsterdam | NULL    | 10      | 2022-10-14 |

`UNION BY NAME` follows set semantics (therefore it performs duplicate elimination), whereas `UNION ALL BY NAME` follows bag semantics.

## `INTERSECT`

The `INTERSECT` clause can be used to select all rows that occur in the result of **both** queries.

### Vanilla `INTERSECT` (Set Semantics)

Vanilla `INTERSECT` performs duplicate elimination, so only unique rows are returned.

```sql
SELECT * FROM range(2) t1(x)
INTERSECT
SELECT * FROM range(6) t2(x);
```

| x |
|--:|
| 0 |
| 1 |

### `INTERSECT ALL` (Bag Semantics)

`INTERSECT ALL` follows bag semantics, so duplicates are returned.

```sql
SELECT unnest([5, 5, 6, 6, 6, 6, 7, 8]) AS x
INTERSECT ALL
SELECT unnest([5, 6, 6, 7, 7, 9]);
```

| x |
|--:|
| 5 |
| 6 |
| 6 |
| 7 |

## `EXCEPT`

The `EXCEPT` clause can be used to select all rows that **only** occur in the left query.

### Vanilla `EXCEPT` (Set Semantics)

Vanilla `EXCEPT` follows set semantics, therefore, it performs duplicate elimination, so only unique rows are returned.

```sql
SELECT * FROM range(5) t1(x)
EXCEPT
SELECT * FROM range(2) t2(x);
```

| x |
|--:|
| 2 |
| 3 |
| 4 |

### `EXCEPT ALL` (Bag Semantics)

`EXCEPT ALL` uses bag semantics:

```sql
SELECT unnest([5, 5, 6, 6, 6, 6, 7, 8]) AS x
EXCEPT ALL
SELECT unnest([5, 6, 6, 7, 7, 9]);
```

| x |
|--:|
| 5 |
| 8 |
| 6 |
| 6 |

## Syntax

<div id="rrdiagram"></div>
