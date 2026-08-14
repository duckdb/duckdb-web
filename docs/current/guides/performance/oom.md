---
layout: docu
redirect_from:
- /oom
title: Out-of-Memory Issues
---

### Configuration Options

If you are experiencing out-of-memory issues with DuckDB, try tweaking the following configuration options:

* Reduce the number of threads using the `SET threads = ...` command.
* Setting the memory limit lower than the [default 80%]({% link docs/current/operations_manual/limits.md %}) can help prevent out of memory errors. While this configuration sounds counter-intuitive, it helps because some of DuckDB's operations circumvent the database's buffer manager and thus they can reserve more memory than allowed by the memory limit. If this happens (e.g., DuckDB is killed by the operating system or an OOM reaper process), set the memory limit to just 50-60% of the total system memory by using the `SET memory_limit = '...'` statement.
* If your query reads a large amount of data from a file or writes a large amount of data, try setting the `preserve_insertion_order` option to `false`: `SET preserve_insertion_order = false`.

In short, try the settings:

```sql
SET threads = ⟨lower_than_the_number_of_available_threads⟩;
SET memory_limit = ⟨lower_than_80%_of_system_memory⟩;
SET preserve_insertion_order = false;
```

### Schema and Indexes

If you run in a memory-constrained environment, using smaller data types (e.g., `TINYINT`) can reduce the amount of memory and disk space required to complete a query. DuckDB’s [bitpacking compression]({% post_url 2022-10-28-lightweight-compression %}#bit-packing) means small values stored in larger data types will not take up larger sizes on disk, but they will take up more memory during processing – hence, using the most restrictive types possible when creating columns is necessary to reduce memory consumption.

Indexes can significantly increase memory consumption. Additionally, they are [currently not buffer-managed]({% link docs/current/guides/performance/indexing.md %}#indexes-and-memory). Avoid using indexes if possible. If your workload requires indexing large tables, consider reducing the memory limit to accommodate this.
