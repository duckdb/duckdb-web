---
layout: docu
railroad: query_syntax/values.js
title: VALUES Clause
---

The `VALUES` clause is used to specify a fixed number of rows. The `VALUES` clause can be used as a stand-alone statement, as part of the `FROM` clause, or as input to an `INSERT INTO` statement.

## Examples

Generate two rows and directly return them:

```sql
VALUES ('Amsterdam', 1), ('London', 2);
```

Generate two rows as part of a `FROM` clause, and rename the columns:

```sql
SELECT * FROM (VALUES ('Amsterdam', 1), ('London', 2)) Cities(Name, Id);
```

Generate two rows and insert them into a table:

```sql
INSERT INTO Cities VALUES ('Amsterdam', 1), ('London', 2);
```

Create a table directly from a `VALUES` clause:

```sql
CREATE TABLE Cities AS SELECT * FROM (VALUES ('Amsterdam', 1), ('London', 2)) Cities(Name, Id);
```

## Syntax

<div id="rrdiagram"></div>