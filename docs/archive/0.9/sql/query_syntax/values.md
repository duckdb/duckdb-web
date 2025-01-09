---
layout: docu
railroad: query_syntax/values.js
redirect_from:
- docs/archive/0.9.2/sql/query_syntax/values
- docs/archive/0.9.1/sql/query_syntax/values
- docs/archive/0.9.0/sql/query_syntax/values
title: VALUES Clause
---

The `VALUES` clause is used to specify a fixed number of rows. The `VALUES` clause can be used as a stand-alone statement, as part of the `FROM` clause, or as input to an `INSERT INTO` statement.

## Examples

```sql
-- generate two rows and directly return them
VALUES ('Amsterdam', 1), ('London', 2);
-- generate two rows as part of a FROM clause, and rename the columns
SELECT * FROM (VALUES ('Amsterdam', 1), ('London', 2)) Cities(Name, Id);
-- generate two rows and insert them into a table
INSERT INTO Cities VALUES ('Amsterdam', 1), ('London', 2);
-- create a table directly from a VALUES clause
CREATE TABLE Cities AS SELECT * FROM (VALUES ('Amsterdam', 1), ('London', 2)) Cities(Name, Id);
```

## Syntax

<div id="rrdiagram"></div>