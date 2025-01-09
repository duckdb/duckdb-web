---
layout: docu
railroad: statements/use.js
redirect_from:
- docs/archive/0.9.2/sql/statements/use
- docs/archive/0.9.1/sql/statements/use
- docs/archive/0.9.0/sql/statements/use
title: Use
---

The `USE` statement selects a database and optional schema to use as the default.

## Examples

```sql
--- Sets the 'memory' database as the default
USE memory;
--- Sets the 'duck.main' database and schema as the default
USE duck.main;
```

## Syntax

<div id="rrdiagram1"></div>

The `USE` statement sets a default database or database/schema combination to use for
future operations. For instance, tables created without providing a fully qualified
table name will be created in the default database.