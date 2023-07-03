---
layout: docu
title: ORDER BY Clause
selected: Documentation/SQL/Query Syntax/Order By
expanded: SQL
railroad: query_syntax/orderby.js
---

`ORDER BY` is an output modifier. Logically it is applied near the very end of the query (just prior to [`LIMIT`](./limit) or [`OFFSET`](./limit), if present). 
The `ORDER BY` clause sorts the rows on the sorting criteria in either ascending or descending order. 
In addition, every order clause can specify whether `NULL` values should be moved to the beginning or to the end.

The `ORDER BY` clause may contain one or more expressions, separated by commas.
An error will be thrown if no expressions are included, since the `ORDER BY` clause should be removed in that situation. 
The expressions may begin with either an arbitrary scalar expression (which could be a column name), a column position number (Ex: `1`. Note that it is 1-indexed), or the keyword `ALL`.
Each expression can optionally be followed by an order modifier (`ASC` or `DESC`, default is `ASC`), and/or a `NULL` order modifier (`NULLS FIRST` or `NULLS LAST`, default is `NULLS LAST`).

### ORDER BY ALL
The `ALL` keyword indicates that the output should be sorted by every column in order from left to right. 
The direction of this sort may be modified using either `ORDER BY ALL ASC` or `ORDER BY ALL DESC` and/or `NULLS FIRST` or `NULLS LAST`.
Note that `ALL` may not be used in combination with other expressions in the `ORDER BY` clause - it must be by itself.
See examples below.

### NULL Order Modifier

By default if no modifiers are provided, DuckDB sorts `ASC NULLS LAST`, i.e. the values are sorted in ascending order and null values are placed last. 
This is identical to the default sort order of PostgreSQL. 
Note that this was a breaking change in version 0.8.0. Prior to 0.8.0, DuckDB sorted using `ASC NULLS FIRST`.
The default sort order can be changed using the following `PRAGMA` statements.

```sql
-- change the default null sorting order to either NULLS FIRST and NULLS LAST
PRAGMA default_null_order='NULLS FIRST';
-- change the default sorting order to either DESC or ASC
PRAGMA default_order='DESC';
```

### Collations

Text is sorted using the binary comparison collation by default, which means values are sorted on their binary UTF8 values.
While this works well for ASCII text (e.g. for English language data), the sorting order can be incorrect for other languages.
For this purpose, DuckDB provides collations.
For more information on collations, see the [Collation page](../../sql/expressions/collations).

### Examples

All examples use this example table:
```sql
CREATE OR REPLACE TABLE addresses AS 
    SELECT '123 Quack Blvd' AS address, 'DuckTown' AS city, '11111' AS zip 
    UNION ALL 
    SELECT '111 Duck Duck Goose Ln', 'DuckTown', '11111' 
    UNION ALL 
    SELECT '111 Duck Duck Goose Ln', 'Duck Town', '11111'
    UNION ALL 
    SELECT '111 Duck Duck Goose Ln', 'Duck Town', '11111-0001'
;
```

```sql
-- select the addresses, ordered by city name using the default null order and default order
SELECT *
FROM addresses
ORDER BY city;
-- select the addresses, ordered by city name in descending order with nulls at the end
SELECT *
FROM addresses
ORDER BY city DESC NULLS LAST;
-- order by city and then by zip code, both using the default orderings
SELECT *
FROM addresses
ORDER BY city, zip;
-- order by city using german collation rules
SELECT *
FROM addresses
ORDER BY city COLLATE DE;
```

#### ORDER BY ALL Examples
```sql
-- Order from left to right (by address, then by city, then by zip) in ascending order
SELECT *
FROM addresses
ORDER BY ALL
```

|        address         |   city    |    zip     |
|------------------------|-----------|------------|
| 111 Duck Duck Goose Ln | Duck Town | 11111      |
| 111 Duck Duck Goose Ln | Duck Town | 11111-0001 |
| 111 Duck Duck Goose Ln | DuckTown  | 11111      |
| 123 Quack Blvd         | DuckTown  | 11111      |


```sql
-- Order from left to right (by address, then by city, then by zip) in descending order
SELECT *
FROM addresses
ORDER BY ALL DESC
```

|        address         |   city    |    zip     |
|------------------------|-----------|------------|
| 123 Quack Blvd         | DuckTown  | 11111      |
| 111 Duck Duck Goose Ln | DuckTown  | 11111      |
| 111 Duck Duck Goose Ln | Duck Town | 11111-0001 |
| 111 Duck Duck Goose Ln | Duck Town | 11111      |



### Syntax
<div id="rrdiagram"></div>
