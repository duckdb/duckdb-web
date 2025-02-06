---
layout: docu
railroad: statements/createmacro.js
title: CREATE MACRO Statement
---

The `CREATE MACRO` statement can create a scalar or table macro (function) in the catalog.
A macro may only be a single `SELECT` statement (similar to a `VIEW`), but it has the benefit of accepting parameters.

For a scalar macro, `CREATE MACRO` is followed by the name of the macro, and optionally parameters within a set of parentheses. The keyword `AS` is next, followed by the text of the macro. By design, a scalar macro may only return a single value.
For a table macro, the syntax is similar to a scalar macro except `AS` is replaced with `AS TABLE`. A table macro may return a table of arbitrary size and shape.

> If a `MACRO` is temporary, it is only usable within the same database connection and is deleted when the connection is closed.

## Examples

### Scalar Macros

Create a macro that adds two expressions (`a` and `b`):

```sql
CREATE MACRO add(a, b) AS a + b;
```

Create a macro for a `CASE` expression:

```sql
CREATE MACRO ifelse(a, b, c) AS CASE WHEN a THEN b ELSE c END;
```

Create a macro that does a subquery:

```sql
CREATE MACRO one() AS (SELECT 1);
```

Create a macro with a common table expression.
Note that parameter names get priority over column names. To work around this, disambiguate using the table name.

```sql
CREATE MACRO plus_one(a) AS (WITH cte AS (SELECT 1 AS a) SELECT cte.a + a FROM cte);
```

Macros are schema-dependent, and have an alias, `FUNCTION`:

```sql
CREATE FUNCTION main.my_avg(x) AS sum(x) / count(x);
```

Create a macro with default constant parameters:

```sql
CREATE MACRO add_default(a, b := 5) AS a + b;
```

Create a macro `arr_append` (with a functionality equivalent to `array_append`):

```sql
CREATE MACRO arr_append(l, e) AS list_concat(l, list_value(e));
```

### Table Macros

Create a table macro without parameters:

```sql
CREATE MACRO static_table() AS TABLE
    SELECT 'Hello' AS column1, 'World' AS column2;
```

Create a table macro with parameters (that can be of any type):

```sql
CREATE MACRO dynamic_table(col1_value, col2_value) AS TABLE
    SELECT col1_value AS column1, col2_value AS column2;
```

Create a table macro that returns multiple rows. It will be replaced if it already exists, and it is temporary (will be automatically deleted when the connection ends):

```sql
CREATE OR REPLACE TEMP MACRO dynamic_table(col1_value, col2_value) AS TABLE
    SELECT col1_value AS column1, col2_value AS column2
    UNION ALL
    SELECT 'Hello' AS col1_value, 456 AS col2_value;
```

Pass an argument as a list:

```sql
CREATE MACRO get_users(i) AS TABLE
    SELECT * FROM users WHERE uid IN (SELECT unnest(i));
```

An example for how to use the `get_users` table macro is the following:

```sql
CREATE TABLE users AS
    SELECT *
    FROM (VALUES (1, 'Ada'), (2, 'Bob'), (3, 'Carl'), (4, 'Dan'), (5, 'Eve')) t(uid, name);
SELECT * FROM get_users([1, 5]);
```

To define macros on arbitrary tables, use the [`query_table` function]({% link docs/archive/1.1/guides/sql_features/query_and_query_table_functions.md %}). For example, the following macro computes a column-wise checksum on a table:

```sql
CREATE MACRO checksum(table_name) AS TABLE
    SELECT bit_xor(md5_number(COLUMNS(*)::VARCHAR))
    FROM query_table(table_name);

CREATE TABLE tbl AS SELECT unnest([42, 43]) AS x, 100 AS y;
SELECT * FROM checksum('tbl');
```

## Overloading

It is possible to overload a macro based on the amount of parameters it takes, this works for both scalar and table macros.

By providing overloads we can have both `add_x(a, b)` and `add_x(a, b, c)` with different function bodies.

```sql
CREATE MACRO add_x
    (a, b) AS a + b,
    (a, b, c) AS a + b + c;
```

```sql
SELECT
    add_x(21, 42) AS two_args,
    add_x(21, 42, 21) AS three_args;
```

| two_args | three_args |
|----------|------------|
|    63    |     84     |

## Syntax

<div id="rrdiagram"></div>

Macros allow you to create shortcuts for combinations of expressions.

```sql
CREATE MACRO add(a) AS a + b;
```

```console
Binder Error: Referenced column "b" not found in FROM clause!
```

This works:

```sql
CREATE MACRO add(a, b) AS a + b;
```

Usage example:

```sql
SELECT add(1, 2) AS x;
```

| x |
|--:|
| 3 |

However, this fails:

```sql
SELECT add('hello', 3);
```

```console
Binder Error: Could not choose a best candidate function for the function call "+(STRING_LITERAL, INTEGER_LITERAL)". In order to select one, please add explicit type casts.
    Candidate functions:
    +(DATE, INTEGER) -> DATE
    +(INTEGER, INTEGER) -> INTEGER
```

Macros can have default parameters.
Unlike some languages, default parameters must be named
when the macro is invoked.

`b` is a default parameter:

```sql
CREATE MACRO add_default(a, b := 5) AS a + b;
```

The following will result in 42:

```sql
SELECT add_default(37);
```

The following will throw an error:

```sql
SELECT add_default(40, 2);
```

```console
Binder Error: Macro function 'add_default(a)' requires a single positional argument, but 2 positional arguments were provided.
```

Default parameters must used by assigning them like the following:

```sql
SELECT add_default(40, b := 2) AS x;
```

| x  |
|---:|
| 42 |

However, the following fails:

```sql
SELECT add_default(b := 2, 40);
```

```console
Binder Error: Positional parameters cannot come after parameters with a default value!
```

The order of default parameters does not matter:

```sql
CREATE MACRO triple_add(a, b := 5, c := 10) AS a + b + c;
```

```sql
SELECT triple_add(40, c := 1, b := 1) AS x;
```

| x  |
|---:|
| 42 |

When macros are used, they are expanded (i.e., replaced with the original expression), and the parameters within the expanded expression are replaced with the supplied arguments. Step by step:

The `add` macro we defined above is used in a query:

```sql
SELECT add(40, 2) AS x;
```

Internally, add is replaced with its definition of `a + b`:

```sql
SELECT a + b; AS x
```

Then, the parameters are replaced by the supplied arguments:

```sql
SELECT 40 + 2 AS x;
```

## Limitations

### Using Named Parameters

Currently, positional macro parameters can only be used positionally, and named parameters can only be used by supplying their name. Therefore, the following will not work:

```sql
CREATE MACRO my_macro(a, b := 42) AS (a + b);
SELECT my_macro(32, 52);
```

```console
Binder Error: Macro function 'my_macro(a)' requires a single positional argument, but 2 positional arguments were provided.
```

### Using Subquery Macros

If a `MACRO` is defined as a subquery, it cannot be invoked in a table function. DuckDB will return the following error:

```console
Binder Error: Table function cannot contain subqueries
```

### Overloads

Overloads for macro functions have to be set at creation, it is not possible to define a macro by the same name twice without first removing the first definition.