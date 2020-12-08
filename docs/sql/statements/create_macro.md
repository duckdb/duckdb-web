---
layout: docu
title: Create Macro
selected: Documentation/SQL/Create Macro
expanded: SQL
railroad: statements/createmacro.js
---
CREATE MACRO - this statement creates a scalar macro in the catalog.

### Examples
```sql
-- create a macro for a case expression
CREATE MACRO ifelse(a, b, c) AS CASE WHEN a THEN b ELSE c END;
-- create a macro that adds two expressions (a and b)
CREATE MACRO add(a, b) AS a + b;
-- create a macro that does a subquery
CREATE MACRO one() AS (SELECT 1);
-- create a macro with a common table expression
-- (parameter names get priority over column names: disambiguate using the table name)
CREATE MACRO plus_one(a) AS (WITH cte AS (SELECT 1 AS a) SELECT cte.a + a);
-- macro's are schema-dependent, and have an alias: FUNCTION
CREATE FUNCTION main.myavg(x) AS SUM(x) / COUNT(x);
```

### Syntax
<div id="rrdiagram"></div>
