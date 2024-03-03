---
layout: docu
title: SELECT Clause
selected: Documentation/SQL/Query Syntax/Select
expanded: SQL
railroad: query_syntax/select.js
blurb: The SELECT clause specifies the list of columns that will be returned by the query.
---

The `SELECT` clause specifies the list of columns that will be returned by the query. While it appears first in the clause, *logically* the expressions here are executed only at the end. The `SELECT` clause can contain arbitrary expressions that transform the output, as well as aggregates and window functions.

### Examples

```sql
-- select all columns from the table called "table_name"
SELECT * FROM table_name;
-- perform arithmetic on columns in a table, and provide an alias
SELECT col1 + col2 AS res, sqrt(col1) AS root FROM table_name;
-- select all unique cities from the addresses table
SELECT DISTINCT city FROM addresses;
-- return the total number of rows in the addresses table
SELECT COUNT(*) FROM addresses;
-- select all columns except the city column from the addresses table
SELECT * EXCLUDE (city) FROM addresses;
-- select all columns from the addresses table, but replace city with LOWER(city)
SELECT * REPLACE (LOWER(city) AS city) FROM addresses;
-- select all columns matching the given regex from the table
SELECT COLUMNS('number\d+') FROM addresses;
-- compute a function on all given columns of a table
SELECT MIN(COLUMNS(*)) FROM addresses;
```

### Syntax
<div id="rrdiagram"></div>

### Select List

The `SELECT` clause contains a list of expressions that specify the result of a query. The select list can refer to any columns in the `FROM` clause, and combine them using expressions. As the output of a SQL query is a table - every expression in the `SELECT` clause also has a name. The expressions can be explicitly named using the `AS` clause (e.g. `expr AS name`). If a name is not provided by the user the expressions are named automatically by the system. 

#### Star Expressions

```sql
-- select all columns from the table called "table_name"
SELECT * FROM table_name;
-- select all columns matching the given regex from the table
SELECT COLUMNS('number\d+') FROM addresses;
```

The [star expression](../expressions/star) is a special expression that expands to *multiple expressions* based on the contents of the `FROM` clause. In the simplest case, `*` expands to **all** expressions in the `FROM` clause. Columns can also be selected using regular expressions or lambda functions. See the [star expression page](../expressions/star) for more details.

#### Distinct Clause

```sql
-- select all unique cities from the addresses table
SELECT DISTINCT city FROM addresses;
```

The `DISTINCT` clause can be used to return **only** the unique rows in the result - so that any duplicate rows are filtered out.

#### Distinct On Clause

```sql
-- select only the highest population city for each country
SELECT DISTINCT ON(country) city, population FROM cities ORDER BY population DESC;
```

The `DISTINCT ON` clause returns only one row per unique value in the set of expressions as defined in the `ON` clause. If an `ORDER BY` clause is present, the row that is returned is the first row that is encountered *as per the `ORDER BY`* criteria. If an `ORDER BY` clause is not present, the first row that is encountered is not defined and can be any row in the table.

#### Aggregates
```sql
-- return the total number of rows in the addresses table
SELECT COUNT(*) FROM addresses;
-- return the total number of rows in the addresses table grouped by city
SELECT city, COUNT(*) FROM addresses GROUP BY city;
```

[Aggregate functions](../aggregates) are special functions that *combine* multiple rows into a single value. When aggregate functions are present in the `SELECT` clause, the query is turned into an aggregate query. In an aggregate query, **all** expressions must either be part of an aggregate function, or part of a group (as specified by the [`GROUP BY clause`](groupby)).

#### Window Functions
```sql
-- generate a "row_number" column containing incremental identifiers for each row
SELECT row_number() OVER () FROM sales;
-- compute the difference between the current amount, and the previous amount, by order of time
SELECT amount - lag(amount) OVER (ORDER BY time) FROM sales;
```

[Window functions](../window_functions) are special functions that allow the computation of values relative to *other rows* in a result. Window functions are marked by the `OVER` clause which contains the *window specification*. The window specification defines the frame or context in which the window function is computed. See the [window functions page](../window_functions) for more information.

#### Unnest
```sql
-- unnest an array by one level
SELECT UNNEST([1, 2, 3]);
-- unnest a struct by one level
SELECT UNNEST({'a': 42, 'b': 84});
```

[Unnest](unnest) is a special function that can be used together with arrays or structs. The unnest function strips one level of nesting from the type. For example, `INT[]` is transformed into `INT`. `STRUCT(a INT, b INT)` is transformed into `a INT, b INT`. The unnest function can be used to transform nested types into regular scalar types, which makes them easier to operate on.
