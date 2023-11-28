---
layout: docu
title: HTTP Parquet Import
---

To load a Parquet file over HTTP(S), the [`httpfs` extension](../../extensions/httpfs) is required. This can be installed use the `INSTALL` SQL command. This only needs to be run once.

```sql
INSTALL httpfs;
```

To load the `httpfs` extension for usage, use the `LOAD` SQL command:

```sql
LOAD httpfs;
```

After the `httpfs` extension is set up, Parquet files can be read over `http(s)`:

```sql
SELECT * FROM read_parquet('https://<domain>/path/to/file.parquet');
```

For example:

```sql
SELECT * FROM read_parquet('https://duckdb.org/data/prices.parquet');
```

The function `read_parquet` can be omitted if the URL ends with `.parquet`:

```sql
SELECT * FROM read_parquet('https://duckdb.org/data/holdings.parquet');
```

Moreover, the `read_parquet` function itself can also be omitted thanks to DuckDB's [replacement scan mechanism](../../api/c/replacement_scans):

```sql
SELECT * FROM 'https://duckdb.org/data/holdings.parquet';
```
