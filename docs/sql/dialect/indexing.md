---
layout: docu
title: Indexing
---

DuckDB uses 1-based indexing except for [JSON objects]({% link docs/data/json/overview.md %}), which use 0-based indexing.

## Examples

```sql
SELECT list[1] AS element
FROM (SELECT ['first', 'second', 'third'] AS list);
```

```text
┌─────────┐
│ element │
│ varchar │
├─────────┤
│ first   │
└─────────┘
```

```sql
SELECT json[1][1] AS element
FROM (SELECT '["first", "second", "third"]'::JSON AS json);
```

```text
┌──────────┐
│ element  │
│   json   │
├──────────┤
│ "second" │
└──────────┘
```
