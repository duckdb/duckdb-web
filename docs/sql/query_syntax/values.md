---
layout: docu
title: VALUES Clause
railroad: query_syntax/values.js
---

The `VALUES` clause is used to specify a fixed number of rows. The `VALUES` clause can be used as a stand-alone statement, as part of the `FROM` clause, or as input to an `INSERT INTO` statement.

## Examples

Generate two rows and directly return them:

```sql
VALUES ('Amsterdam', 1), ('London', 2);
```

Generate two rows as part of a `FROM` clause, and rename the columns:

```sql
SELECT *
FROM (VALUES ('Amsterdam', 1), ('London', 2)) cities(name, id);
```

Generate two rows and insert them into a table:

```sql
INSERT INTO cities
VALUES ('Amsterdam', 1), ('London', 2);
```

Create a table directly from a `VALUES` clause:

```sql
CREATE TABLE cities AS
    SELECT *
    FROM (VALUES ('Amsterdam', 1), ('London', 2)) cities(name, id);
```

## Syntax

<div id="rrdiagram"></div>
