---
layout: docu
title: Known Issues
---

## Incorrect Memory Values on Certain Ubuntu Versions

On certain Ubuntu versions (e.g., 20.04 and 24.04), when querying the `max_memory` or `memory_limit` from the `duckdb_settings`, the values may be inaccurate:

Example:

```sql
FROM duckdb_settings() WHERE name LIKE '%mem%';
```

The output contains values larger than 1000 PiB:

```text
┌──────────────┬────────────┬─────────────────────────────────────────────┬────────────┬─────────┐
│     name     │   value    │                 description                 │ input_type │  scope  │
│   varchar    │  varchar   │                   varchar                   │  varchar   │ varchar │
├──────────────┼────────────┼─────────────────────────────────────────────┼────────────┼─────────┤
│ max_memory   │ 1638.3 PiB │ The maximum memory of the system (e.g. 1GB) │ VARCHAR    │ GLOBAL  │
│ memory_limit │ 1638.3 PiB │ The maximum memory of the system (e.g. 1GB) │ VARCHAR    │ GLOBAL  │
└──────────────┴────────────┴─────────────────────────────────────────────┴────────────┴─────────┘
```
