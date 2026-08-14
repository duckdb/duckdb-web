---
layout: docu
redirect_from:
- /docs/preview/sql/dialect/indexing
- /docs/sql/dialect/indexing
- /docs/stable/sql/dialect/indexing
title: Indexing
---

DuckDB uses 1-based indexing except for [JSON objects]({% link docs/current/data/json/overview.md %}), which use 0-based indexing.

## Examples

The index origin is 1 for strings, lists, etc.

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

The index origin is 0 for JSON objects.

```sql
SELECT json[1] AS element
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
