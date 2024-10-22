---
layout: community_extension_doc
title: Community Extensions Download Metrics
---

## What Do We Measure?

The `INSTALL` events of Community Extensions (as well as regular extensions), which trigger downloads from the `http[s]://community-extensions.duckdb.org` site, are tracked by Cloudflare.

We re-publish data about the total number of downloads, aggregated across DuckDB versions and platforms at the <https://community-extensions.duckdb.org/downloads-last-week.json> endpoint.

An example query to return the list of community extensions sorted by descending number of downloads would be:

```sql
UNPIVOT (
    SELECT 'community' AS repository, *
        FROM 'https://community-extensions.duckdb.org/downloads-last-week.json'
    ) ON COLUMNS(* EXCLUDE (_last_update, repository))
INTO NAME extension VALUE downloads_last_week
ORDER BY downloads_last_week DESC;
```
