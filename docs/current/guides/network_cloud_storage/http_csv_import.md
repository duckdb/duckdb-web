---
layout: docu
title: HTTP CSV Import
---

To load a CSV file directly over HTTP(S), the [`httpfs` extension]({% link docs/current/core_extensions/httpfs/overview.md %}) is required. This can be installed using the `INSTALL` SQL command. This only needs to be run once.

```sql
INSTALL httpfs;
```

To load the `httpfs` extension for usage, use the `LOAD` SQL command:

```sql
LOAD httpfs;
```

After the `httpfs` extension is set up, CSV files can be read over `http(s)` the same way as a local file, using [`read_csv`]({% link docs/current/guides/file_formats/csv_import.md %}) (or `read_csv_auto` for older DuckDB versions):

```sql
SELECT * FROM read_csv('https://⟨domain⟩/path/to/file.csv');
```

Moreover, the `read_csv` function itself can also be omitted thanks to DuckDB's [replacement scan mechanism]({% link docs/current/clients/c/replacement_scans.md %}):

```sql
SELECT * FROM 'https://⟨domain⟩/path/to/file.csv';
```

## Example

The following query reads an openly licensed (CC BY 4.0) real-world CSV directly from GitHub's raw file host and aggregates it, with no local download step:

```sql
SELECT
    area,
    round(avg(sunbed_price), 0) AS avg_sunbed_price_eur,
    count(*) AS clubs
FROM read_csv('https://raw.githubusercontent.com/shiftdylson1/marbella-price-data/main/beach-clubs/beach-clubs.csv')
WHERE sunbed_price IS NOT NULL
GROUP BY area
ORDER BY avg_sunbed_price_eur DESC;
```

```text
┌────────────────────────────┬──────────────────────┬───────┐
│            area            │ avg_sunbed_price_eur │ clubs │
│          varchar           │        double        │ int64 │
├────────────────────────────┼──────────────────────┼───────┤
│ Marbella centre (El Cable) │                120.0 │     1 │
│ Puerto Banús               │                103.0 │     4 │
│ Golden Mile                │                 70.0 │     1 │
│ El Rosario (Marbella East) │                 30.0 │     1 │
│ Elviria (Marbella East)    │                 30.0 │     1 │
│ Marbella centre            │                 20.0 │     1 │
│ Casablanca (Golden Mile)   │                 15.0 │     1 │
└────────────────────────────┴──────────────────────┴───────┘
```

Because `read_csv` streams the file rather than materializing it first, this works the same way for CSVs far larger than fit in memory, and pairs naturally with `read_csv`'s usual options (`columns`, `types`, `delim`, etc.) for files that need explicit schema hints.
