---
layout: docu
railroad: query_syntax/orderby.js
title: ORDER BY Clause
---

`ORDER BY` is an output modifier. Logically it is applied near the very end of the query (just prior to [`LIMIT`]({% link docs/preview/sql/query_syntax/limit.md %}) or [`OFFSET`]({% link docs/preview/sql/query_syntax/limit.md %}), if present).
The `ORDER BY` clause sorts the rows on the sorting criteria in either ascending or descending order.
In addition, every order clause can specify whether `NULL` values should be moved to the beginning or to the end.

The `ORDER BY` clause may contain one or more expressions, separated by commas.
An error will be thrown if no expressions are included, since the `ORDER BY` clause should be removed in that situation.
The expressions may begin with either an arbitrary scalar expression (which could be a column name), a column position number (where the indexing starts from 1), or the keyword `ALL`.
Each expression can optionally be followed by an order modifier (`ASC` or `DESC`, default is `ASC`), and/or a `NULL` order modifier (`NULLS FIRST` or `NULLS LAST`, default is `NULLS LAST`).

## `ORDER BY ALL`

The `ALL` keyword indicates that the output should be sorted by every column in order from left to right.
The direction of this sort may be modified using either `ORDER BY ALL ASC` or `ORDER BY ALL DESC` and/or `NULLS FIRST` or `NULLS LAST`.
Note that `ALL` may not be used in combination with other expressions in the `ORDER BY` clause – it must be by itself.
See examples below.

## `NULL` Order Modifier

By default, DuckDB sorts `ASC` and `NULLS LAST`, i.e., the values are sorted in ascending order and `NULL` values are placed last.
This is identical to the default sort order of PostgreSQL.
The default sort order can be changed with the following configuration options.

Use the `default_null_order` option to change the default `NULL` sorting order to either `NULLS_FIRST`, `NULLS_LAST`, `NULLS_FIRST_ON_ASC_LAST_ON_DESC` or `NULLS_LAST_ON_ASC_FIRST_ON_DESC`:

```sql
SET default_null_order = 'NULLS_FIRST';
```

Use the `default_order` option to change the direction of the default sorting order to either `DESC` or `ASC`:

```sql
SET default_order = 'DESC';
```

## Collations

Text is sorted using the binary comparison collation by default, which means values are sorted on their binary UTF-8 values.
While this works well for ASCII text (e.g., for English language data), the sorting order can be incorrect for other languages.
For this purpose, DuckDB provides collations.
For more information on collations, see the [Collation page]({% link docs/preview/sql/expressions/collations.md %}).

## Examples

All examples use this example table:

```sql
CREATE OR REPLACE TABLE addresses AS
    SELECT '123 Quack Blvd' AS address, 'DuckTown' AS city, '11111' AS zip
    UNION ALL
    SELECT '111 Duck Duck Goose Ln', 'DuckTown', '11111'
    UNION ALL
    SELECT '111 Duck Duck Goose Ln', 'Duck Town', '11111'
    UNION ALL
    SELECT '111 Duck Duck Goose Ln', 'Duck Town', '11111-0001';
```

Select the addresses, ordered by city name using the default `NULL` order and default order:

```sql
SELECT *
FROM addresses
ORDER BY city;
```

Select the addresses, ordered by city name in descending order with nulls at the end:

```sql
SELECT *
FROM addresses
ORDER BY city DESC NULLS LAST;
```

Order by city and then by zip code, both using the default orderings:

```sql
SELECT *
FROM addresses
ORDER BY city, zip;
```

Order by city using German collation rules:

```sql
SELECT *
FROM addresses
ORDER BY city COLLATE DE;
```

### `ORDER BY ALL` Examples

Order from left to right (by address, then by city, then by zip) in ascending order:

```sql
SELECT *
FROM addresses
ORDER BY ALL;
```

|        address         |   city    |    zip     |
|------------------------|-----------|------------|
| 111 Duck Duck Goose Ln | Duck Town | 11111      |
| 111 Duck Duck Goose Ln | Duck Town | 11111-0001 |
| 111 Duck Duck Goose Ln | DuckTown  | 11111      |
| 123 Quack Blvd         | DuckTown  | 11111      |

Order from left to right (by address, then by city, then by zip) in descending order:

```sql
SELECT *
FROM addresses
ORDER BY ALL DESC;
```

|        address         |   city    |    zip     |
|------------------------|-----------|------------|
| 123 Quack Blvd         | DuckTown  | 11111      |
| 111 Duck Duck Goose Ln | DuckTown  | 11111      |
| 111 Duck Duck Goose Ln | Duck Town | 11111-0001 |
| 111 Duck Duck Goose Ln | Duck Town | 11111      |

## Syntax

<div id="rrdiagram"></div>
