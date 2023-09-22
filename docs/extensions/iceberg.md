---
layout: docu
title: Iceberg
---

The `iceberg` extension is a loadable extension that implements support for the [Apache Iceberg format](https://iceberg.apache.org/).

> This extension currently only works on the `main` branch of DuckDB (bleeding edge releases).

## Usage

```sql
SELECT count(*) FROM iceberg_scan('data/iceberg/lineitem_iceberg', ALLOW_MOVED_PATHS=true);
```
```text
51793
```

```sql
SELECT * FROM iceberg_snapshots('data/iceberg/lineitem_iceberg', ALLOW_MOVED_PATHS=true);
```
```text
1	3776207205136740581	2023-02-15 15:07:54.504	0	lineitem_iceberg/metadata/snap-3776207205136740581-1-cf3d0be5-cf70-453d-ad8f-48fdc412e608.avro
2	7635660646343998149	2023-02-15 15:08:14.73	0	lineitem_iceberg/metadata/snap-7635660646343998149-1-10eaca8a-1e1c-421e-ad6d-b232e5ee23d3.avro
```

> The `ALLOW_MOVED_PATHS` option ensures that some path resolution is performed, which allows scanning Iceberg tables that are moved.

## GitHub Repository

[<span class="github">GitHub</span>](https://github.com/duckdblabs/duckdb_iceberg)
