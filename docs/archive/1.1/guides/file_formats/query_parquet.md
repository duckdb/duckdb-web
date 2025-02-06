---
layout: docu
redirect_from:
- /docs/archive/1.1/guides/import/query_parquet
title: Querying Parquet Files
---

To run a query directly on a Parquet file, use the `read_parquet` function in the `FROM` clause of a query.

```sql
SELECT * FROM read_parquet('input.parquet');
```

The Parquet file will be processed in parallel. Filters will be automatically pushed down into the Parquet scan, and only the relevant columns will be read automatically.

For more information see the blog post [“Querying Parquet with Precision using DuckDB”]({% post_url 2021-06-25-querying-parquet %}).