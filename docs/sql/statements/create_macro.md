---
layout: docu
title: Create Macro
selected: Documentation/SQL/Create Macro
expanded: SQL
railroad: statements/createmacro.js
---
The `CREATE MACRO` statement can create a scalar or table macro (function) in the catalog. 
A macro may only be a single `SELECT` statement (similar to a `VIEW`), but it has the benefit of accepting parameters.
For a scalar macro, `CREATE MACRO` is followed by the name of the macro, and optionally parameters within a set of parentheses. The keyword `AS` is next, followed by the text of the macro. By design, a scalar macro may only return a single value.
For a table macro, the syntax is similar to a scalar macro except `AS` is replaced with `AS TABLE`. A table macro may return a table of arbitrary size and shape. 

If a `MACRO` is temporary, it is only usable within the same database connection and is deleted when the connection is closed.

### Examples
```sql
-- create a macro that adds two expressions (a and b)
CREATE MACRO add(a, b) AS a + b;
-- create a macro for a case expression
CREATE MACRO ifelse(a, b, c) AS CASE WHEN a THEN b ELSE c END;
-- create a macro that does a subquery
CREATE MACRO one() AS (SELECT 1);
-- create a macro with a common table expression
-- (parameter names get priority over column names: disambiguate using the table name)
CREATE MACRO plus_one(a) AS (WITH cte AS (SELECT 1 AS a) SELECT cte.a + a FROM cte);
-- macro's are schema-dependent, and have an alias: FUNCTION
CREATE FUNCTION main.myavg(x) AS SUM(x) / COUNT(x);
-- create a macro with default constant parameters
CREATE MACRO add_default(a, b := 5) AS a + b;
-- create a macro arr_append (with a functionality equivalent to array_append)
CREATE MACRO arr_append(l, e) AS list_concat(l, list_value(e));

-- TABLE MACROS
-- create a table macro without parameters
CREATE MACRO static_table() AS TABLE SELECT 'Hello' as column1, 'World' as column2;
-- create a table macro with parameters (that can be of any type)
CREATE MACRO dynamic_table(col1_value,col2_value) AS TABLE SELECT col1_value as column1, col2_value as column2;
-- create a table macro that returns multiple rows. 
-- It will be replaced if it already exists, and it is temporary (will be automatically deleted when the connection ends)
CREATE OR REPLACE TEMP MACRO dynamic_table(col1_value,col2_value) AS TABLE 
    SELECT col1_value as column1, col2_value as column2 
    UNION ALL 
    SELECT 'Hello' as col1_value, 456 as col2_value;
```

### Syntax
<div id="rrdiagram"></div>


Macros allow you to create shortcuts for combinations of expressions.
```sql
-- failure! cannot find column "b"
CREATE MACRO add(a) AS a + b;
-- this works
CREATE MACRO add(a,b) AS a + b;
-- error! cannot bind +(VARCHAR, INTEGER)
SELECT add('hello', 3);
-- success!
SELECT add(1, 2);
-- 3
```

Macro's can have default parameters.
```sql
-- b is a default parameter
CREATE MACRO add_default(a, b := 5) AS a + b;
-- the following will result in 42
SELECT add_default(37);
-- error! add_default only has one positional parameter
SELECT add_default(40, 2);
-- success! default parameters are used by assigning them like so
SELECT add_default(40, b=2);
-- error! default parameters must come after positional parameters
SELECT add_default(b=2, 40);
-- the order of default parameters does not matter
CREATE MACRO triple_add(a, b := 5, c := 10) AS a + b + c;
-- success!
SELECT triple_add(40, c := 1, b := 1);
-- 42
```

When macro's are used, they are expanded (i.e. replaced with the original expression), and the parameters within the expanded expression are replaced with the supplied arguments. Step by step:
```sql
-- the 'add' macro we defined above is used in a query
SELECT add(40, 2);
-- internally, add is replaced with its definition of a + b
SELECT a + b;
-- then, the parameters are replaced by the supplied arguments
SELECT 40 + 2;
-- 42
```
