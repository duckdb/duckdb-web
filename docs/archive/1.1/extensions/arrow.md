---
github_repository: https://github.com/duckdb/arrow
layout: docu
title: Arrow Extension
---

The `arrow` extension implements features for using [Apache Arrow](https://arrow.apache.org/), a cross-language development platform for in-memory analytics.
See the [announcement blog post]({% post_url 2021-12-03-duck-arrow %}) for more details.

## Installing and Loading

The `arrow` extension will be transparently autoloaded on first use from the official extension repository.
If you would like to install and load it manually, run:

```sql
INSTALL arrow;
LOAD arrow;
```

## Functions

| Function | Type | Description |
|--|----|-------|
| `to_arrow_ipc` | Table in-out function | Serializes a table into a stream of blobs containing Arrow IPC buffers |
| `scan_arrow_ipc` | Table function | Scan a list of pointers pointing to Arrow IPC buffers |