---
layout: docu
redirect_from:
- /docs/preview/clients/cli/friendly
title: Friendly CLI
---

Along with our [Friendly SQL]({% link docs/current/sql/dialect/friendly_sql.md %}), we provice 
**friendly CLI** features.

## Return the Result of the Last Query Using `_`

You can use the `_` (underscore) table to query the result of the last query:

```sql
SELECT 42 AS x;
```
```text
┌───────┐
│   x   │
│ int32 │
├───────┤
│    42 │
└───────┘
```
```sql
FROM _;
```
```text
┌───────┐
│   x   │
│ int32 │
├───────┤
│    42 │
└───────┘
```

If the last query did not return a result (e.g., because it performed an update operation), the CLI throws an error:

```console
Binder Error:
Failed to query last result "_": no result available
```
