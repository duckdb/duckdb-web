---
layout: docu
title: Internal Errors
---

Internal errors signal an assertion failure within DuckDB. They usually occur due to unexpected conditions or errors in the program's logic.

For example, running [issue 17002](https://github.com/duckdb/duckdb/issues/17002) on DuckDB v1.2.1 results in an internal error.

```console
INTERNAL Error:
Attempted to access index 3 within vector of size 3
```

> The issue is fixed in DuckDB v1.2.2 and newer versions.

After encountering an internal error, DuckDB enters a restricted mode where any further operations will result in the following error message:

```console
FATAL Error:
Failed: database has been invalidated because of a previous fatal error.
The database must be restarted prior to being used again.
```

To continue working with the same database, start a new DuckDB session on the same database.

If you encounter an internal error, please consider creating a minimal reproducible example and submitting an issue to the [DuckDB issue tracker](https://github.com/duckdb/duckdb/issues/new/choose).
