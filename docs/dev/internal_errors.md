---
layout: docu
title: Internal Errors
---

Internal errors signal an assertion failure within DuckDB. They usually occur due to unexpected conditions or errors in the program's logic.

After encountering an internal error, DuckDB enters safe mode where any further operations will result in the following error message:

```console
FATAL Error: Failed: database has been invalidated because of a previous fatal error.
The database must be restarted prior to being used again.
```

If you encounter an internal error, please consider creating a minimal reproducible example and submitting an issue to the [DuckDB issue tracker](https://github.com/duckdb/duckdb/issues/new/choose).
