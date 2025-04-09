---
layout: docu
title: Writing JSON
---

The contents of tables or the result of queries can be written directly to a JSON file using the `COPY` statement.
For example:

```sql
CREATE TABLE cities AS
    FROM (VALUES ('Amsterdam', 1), ('London', 2)) cities(name, id);
COPY cities TO 'cities.json';
```

This will result in `cities.json` with the following content:

```json
{"name":"Amsterdam","id":1}
{"name":"London","id":2}
```

See the [`COPY` statement]({% link docs/preview/sql/statements/copy.md %}#copy-to) for more information.