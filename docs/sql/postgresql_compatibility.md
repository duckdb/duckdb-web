---
layout: docu
title: PostgreSQL Compatibility
---

DuckDB's SQL dialect closely follows the conventions of the PostgreSQL dialect.
The few exceptions to this are listed on this page.

## Division on Integers

When computing division on integers, PostgreSQL performs integer divison, while DuckDB performs float division:

```sql
SELECT 1 / 2 AS x;
```

PostgreSQL returns:

```text
 x
---
 0
(1 row)
```

DuckDB returns:

|  x  |
|----:|
| 0.5 |

To perform integer division in DuckDB, use the `//` operator:

```sql
SELECT 1 // 2 AS x;
```

| x |
|--:|
| 0 |

## `UNION` of Boolean and Integer Values

The following query fails in PostgreSQL but successfully completes in DuckDB:

```sql
SELECT true AS x
UNION
SELECT 2;
```

PostgreSQL returns an error:

```console
ERROR:  UNION types boolean and integer cannot be matched
```

DuckDB performs an enforced cast, therefore, it completes the query and returns the following:

| x |
|--:|
| 1 |
| 2 |
