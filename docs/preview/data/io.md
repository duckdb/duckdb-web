---
layout: docu
title: I/O
---




Keeping more fetch tasks in flight consumes more memory. To determine a budget and avoid out-of-memory issues, we introduced the `read_ahead_depth` configuration option. It can have three types of values:

* `-1` (default): unlimited depth, bounded by memory.
* `N > 0`: at most `N` jobs ahead, with no memory budget.
* `0`: read-ahead is off, each scan task schedules I/O only for its own job.

To configure it, use the `SET` clause, e.g.:

```sql
SET read_ahead_depth = 5;
```
