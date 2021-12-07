---
layout: docu
title: Create Macro
selected: Documentation/SQL/Create Macro
expanded: SQL
railroad: statements/createmacro.js
---
The `CREATE MACRO` statement creates a scalar macro in the catalog.

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
CREATE MACRO add_default(a, b=5) AS a + b;
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
CREATE MACRO add_default(a, b=5) AS a + b;
-- the following will result in 42
SELECT add_default(37);
-- error! add_default only has one positional parameter
SELECT add_default(40, 2);
-- success! default parameters are used by assigning them like so
SELECT add_default(40, b=2);
-- error! default parameters must come after positional parameters
SELECT add_default(b=2, 40);
-- the order of default parameters does not matter
CREATE MACRO triple_add(a, b=5, c=10) AS a + b + c;
-- success!
SELECT triple_add(40, c=1, b=1);
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
