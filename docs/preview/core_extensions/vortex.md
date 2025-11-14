---
github_directory: https://github.com/vortex-data/duckdb-vortex
layout: docu
title: Vortex Extension
---

> The `vortex` extension requires DuckDB 1.4.2+.

The `vortex` extension allows you to read and write files using the [Vortex file format](https://vortex.dev/).

## Installing and Loading

To install and load the extension, run:

```sql
INSTALL vortex;
LOAD vortex;
```

## Reading Vortex Files

Using the `read_vortex` function to read Vortex files:

```sql
SELECT * FROM read_vortex('my.vortex');
```

```text
┌───────┐
│   i   │
│ int64 │
├───────┤
│     0 │
│     1 │
│     2 │
└───────┘
```

## Writing Vortex Files

You can write Vortex files as follows:

```sql
COPY (SELECT * FROM generate_series(0, 3) t(i))
TO 'my.vortex' (FORMAT vortex);
```
