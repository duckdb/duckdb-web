---
layout: community_extension_doc
title: Community Extensions Download Metrics
---

## What Do We Measure?

We use an estimate provided by Cloudflare for the `INSTALL` events of Community Extensions (as well as regular extensions) that triggered downloads from the `http[s]://community-extensions.duckdb.org` site.

We publish data about the total number of downloads, aggregated across DuckDB versions and platforms at the [`https://community-extensions.duckdb.org/downloads-last-week.json`](https://community-extensions.duckdb.org/downloads-last-week.json) endpoint.

## Analyzing Downloads

An example query to return the list of community extensions sorted by descending number of downloads would be:

```sql
UNPIVOT (
    SELECT 'community' AS repository, *
        FROM 'https://community-extensions.duckdb.org/downloads-last-week.json'
    )
ON COLUMNS(* EXCLUDE (_last_update, repository))
INTO NAME extension VALUE downloads_last_week
ORDER BY downloads_last_week DESC;
```

For example, to return the download counts for the weeks since October 1, 2024:

```sql
PIVOT (
    UNPIVOT (
        FROM read_json([
            printf('https://community-extensions.duckdb.org/download-stats-weekly/%s.json',
                strftime(x, '%Y/%W'))
            FOR x IN range(TIMESTAMP '2024-10-01', now()::TIMESTAMP, INTERVAL 1 WEEK)
        ])
    )
    ON COLUMNS(* EXCLUDE _last_update)
    INTO NAME extension VALUE tot
)
ON date_trunc('day',_last_update)
USING any_value(tot)
ORDER BY extension;
```
