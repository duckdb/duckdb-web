---
layout: docu
railroad: statements/use.js
redirect_from:
- /docs/sql/statements/use
title: USE Statement
---

The `USE` statement selects a database and optional schema, or just a schema to use as the default.

## Examples

```sql
--- Sets the 'memory' database as the default. Will use 'main' schema implicitly or error
--- if it does not exist.
USE memory;
--- Sets the 'duck.main' database and schema as the default
USE duck.main;
-- Sets the `main` schema of the currently selected database as the default, in this case 'duck.main'
USE main;
```

## Syntax

<div id="rrdiagram1"></div>

The `USE` statement sets a default database, schema or database/schema combination to use for
future operations. For instance, tables created without providing a fully qualified
table name will be created in the default database.
