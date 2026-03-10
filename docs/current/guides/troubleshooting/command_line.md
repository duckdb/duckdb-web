---
layout: docu
title: Command Line
---

On Linux, DuckDB v1.5.0 has a known issue that the command line does not interpret piped scripts ([#21243](https://github.com/duckdb/duckdb/issues/21243)):

```batch
echo "SELECT 42 AS x;" > test.sql
```

This does not run the script:

```batch
duckdb < test.sql
```

To work around this, add `| cat` to the end of the call:

```batch
duckdb < test.sql | cat
```
