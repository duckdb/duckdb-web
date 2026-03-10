---
layout: docu
title: Command Line
---

On Linux and macOS, DuckDB v1.5.0 has a known issue that the [command line client]({% link docs/current/clients/cli/overview.md %}) does not interpret piped scripts ([#21243](https://github.com/duckdb/duckdb/issues/21243)).

To demonstrate the problem, create a `test.sql` file:

```batch
echo "SELECT 42 AS x;" > test.sql
```

Piping the file to the DuckDB CLI client does not run the script:

```bash
$ duckdb < test.sql
# does not run the script
```

To work around this, add `| cat` to the end of the call:

```batch
duckdb < test.sql | cat
┌───────┐
│   x   │
│ int32 │
├───────┤
│    42 │
└───────┘
```
