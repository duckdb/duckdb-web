---
layout: docu
title: SELECT Clause
railroad: query_syntax/select.js
blurb: The SELECT clause specifies the list of columns that will be returned by the query.
---

The `SELECT` clause specifies the list of columns that will be returned by the query. While it appears first in the clause, *logically* the expressions here are executed only at the end. The `SELECT` clause can contain arbitrary expressions that transform the output, as well as aggregates and window functions.

## Examples

Select all columns from the table called `table_name`:

```sql
SELECT * FROM table_name;
```

Perform arithmetic on the columns in a table, and provide an alias:

```sql
SELECT col1 + col2 AS res, sqrt(col1) AS root FROM table_name;
```

Select all unique cities from the `addresses` table:

```sql
SELECT DISTINCT city FROM addresses;
```

Return the total number of rows in the `addresses` table:

```sql
SELECT count(*) FROM addresses;
```

Select all columns except the city column from the `addresses` table:

```sql
SELECT * EXCLUDE (city) FROM addresses;
```

Select all columns from the `addresses` table, but replace `city` with `lower(city)`:

```sql
SELECT * REPLACE (lower(city) AS city) FROM addresses;
```

Select all columns matching the given regular expression from the table:

```sql
SELECT COLUMNS('number\d+') FROM addresses;
```

Compute a function on all given columns of a table:

```sql
SELECT min(COLUMNS(*)) FROM addresses;
```

To select columns with spaces or special characters, use double quotes (`"`):

```sql
SELECT "Some Column Name" FROM tbl;
```

## Syntax

<div id="rrdiagram"></div>

## `SELECT` List

The `SELECT` clause contains a list of expressions that specify the result of a query. The select list can refer to any columns in the `FROM` clause, and combine them using expressions. As the output of a SQL query is a table – every expression in the `SELECT` clause also has a name. The expressions can be explicitly named using the `AS` clause (e.g., `expr AS name`). If a name is not provided by the user the expressions are named automatically by the system.

> Column names are case-insensitive. See the [Rules for Case Sensitivity]({% link docs/sql/keywords_and_identifiers.md %}#rules-for-case-sensitivity) for more details.

### Star Expressions

Select all columns from the table called `table_name`:

```sql
SELECT *
FROM table_name;
```

Select all columns matching the given regular expression from the table:

```sql
SELECT COLUMNS('number\d+')
FROM addresses;
```

The [star expression]({% link docs/sql/expressions/star.md %}) is a special expression that expands to *multiple expressions* based on the contents of the `FROM` clause. In the simplest case, `*` expands to **all** expressions in the `FROM` clause. Columns can also be selected using regular expressions or lambda functions. See the [star expression page]({% link docs/sql/expressions/star.md %}) for more details.

### `DISTINCT` Clause

Select all unique cities from the addresses table:

```sql
SELECT DISTINCT city
FROM addresses;
```

The `DISTINCT` clause can be used to return **only** the unique rows in the result – so that any duplicate rows are filtered out.

> Queries starting with `SELECT DISTINCT` run deduplication, which is an expensive operation. Therefore, only use `DISTINCT` if necessary.

### `DISTINCT ON` Clause

Select only the highest population city for each country:

```sql
SELECT DISTINCT ON(country) city, population
FROM cities
ORDER BY population DESC;
```

The `DISTINCT ON` clause returns only one row per unique value in the set of expressions as defined in the `ON` clause. If an `ORDER BY` clause is present, the row that is returned is the first row that is encountered *as per the `ORDER BY`* criteria. If an `ORDER BY` clause is not present, the first row that is encountered is not defined and can be any row in the table.

> When querying large data sets, using `DISTINCT` on all columns can be expensive. Therefore, consider using `DISTINCT ON` on a column (or a set of columns) which guaranetees a sufficient degree of uniqueness for your results. For example, using `DISTINCT ON` on the key column(s) of a table guarantees full uniqueness.

### Aggregates

Return the total number of rows in the addresses table:

```sql
SELECT count(*)
FROM addresses;
```

Return the total number of rows in the addresses table grouped by city:

```sql
SELECT city, count(*)
FROM addresses
GROUP BY city;
```

[Aggregate functions]({% link docs/sql/aggregates.md %}) are special functions that *combine* multiple rows into a single value. When aggregate functions are present in the `SELECT` clause, the query is turned into an aggregate query. In an aggregate query, **all** expressions must either be part of an aggregate function, or part of a group (as specified by the [`GROUP BY clause`]({% link docs/sql/query_syntax/groupby.md %})).

### Window Functions

Generate a "row_number" column containing incremental identifiers for each row:

```sql
SELECT row_number() OVER ()
FROM sales;
```

Compute the difference between the current amount, and the previous amount, by order of time:

```sql
SELECT amount - lag(amount) OVER (ORDER BY time)
FROM sales;
```

[Window functions]({% link docs/sql/window_functions.md %}) are special functions that allow the computation of values relative to *other rows* in a result. Window functions are marked by the `OVER` clause which contains the *window specification*. The window specification defines the frame or context in which the window function is computed. See the [window functions page]({% link docs/sql/window_functions.md %}) for more information.

### `unnest` Function

Unnest an array by one level:

```sql
SELECT unnest([1, 2, 3]);
```

Unnest a struct by one level:

```sql
SELECT unnest({'a': 42, 'b': 84});
```

The [`unnest`]({% link docs/sql/query_syntax/unnest.md %}) function is a special function that can be used together with [arrays]({% link docs/sql/data_types/array.md %}), [lists]({% link docs/sql/data_types/list.md %}), or [structs]({% link docs/sql/data_types/struct.md %}). The unnest function strips one level of nesting from the type. For example, `INTEGER[]` is transformed into `INTEGER`. `STRUCT(a INTEGER, b INTEGER)` is transformed into `a INTEGER, b INTEGER`. The unnest function can be used to transform nested types into regular scalar types, which makes them easier to operate on.
