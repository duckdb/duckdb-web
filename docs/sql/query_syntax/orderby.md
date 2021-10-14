---
layout: docu
title: ORDER BY Clause
selected: Documentation/SQL/Query Syntax/Order By
expanded: SQL
railroad: query_syntax/orderby.js
---

`ORDER BY` is an output modifier. Logically it is applied at the very end of the query. The `ORDER BY` clause sorts the rows on the sorting criteria in either ascending or descending order. In addition, every order clause can specify whether `NULL` values should be moved to the beginning or to the end.

By default if no modifiers are provided, DuckDB sorts `ASC NULLS FIRST`, i.e. the values are sorted in ascending order and null values are placed first. This is identical to the default sort order of SQLite. PostgreSQL by default sorts in `ASC NULLS LAST` order. The default sort order can be changed using the following `PRAGMA` statements.

```sql
-- change the default null sorting order to either NULLS FIRST and NULLS LAST
PRAGMA default_null_order='NULLS LAST';
-- change the default sorting order to either DESC or ASC
PRAGMA default_order='DESC';
```

Text is sorted using the binary comparison collation by default, which means values are sorted on their binary UTF8 values. While this works well for ASCII text (e.g. for English language data), the sorting order can be incorrect for other languages. For this purpose, DuckDB provides collations. For more information on collations, see the [Collation page](/docs/sql/expressions/collations).

### Examples

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

### Syntax
<div id="rrdiagram"></div>
