---
layout: community_extension_doc
title: Community extensions download metrics
---

## What do we measure

Community extensions (as for regular extensions) INSTALL events that trigger downloads from the `http[s]://community-extensions.duckdb.org` metrics are tracked by Cloudflare.

We re-publish data about the total number of downloads, aggregated across DuckDB versions and platforms at the `https://community-extensions.duckdb.org/downloads-last-week.json` endpoint.

An example query to return the list of community extensions sorted by descending number of downloads would be:
```sql
UNPIVOT (
  SELECT 'community' AS repository, *
    FROM 'https://community-extensions.duckdb.org/downloads-last-week.json'
  ) ON COLUMNS(* exclude (_last_update, repository))
INTO NAME extension VALUE downloads_last_week
ORDER BY downloads_last_week DESC;
```
