---
layout: docu
title: Known Issues
---

## Incorrect Memory Values on Old Linux Distributions and WSL 2

On Windows Subsystem for Linux 2 (WSL2), when querying the `max_memory` or `memory_limit` from the `duckdb_settings`, the values may be inaccurate on certain Ubuntu versions (e.g., 20.04 and 24.04). The issue also occurs on older distributions such as Red Hat Enterprise Linux 8 (RHEL 8):

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
