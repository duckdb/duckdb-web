---
github_repository: https://github.com/duckdb/duckdb-legacy-parser
layout: docu
title: Legacy Parser Extension
---

DuckDB v2.0.0 replaced the PostgreSQL-derived parser with a new [PEG-based parser]({% link docs/preview/sql/peg_parser.md %}).
The `legacy_parser` extension allows reverting to the old parser.

> The PEG parser is designed to be compatible with the previous parser, so queries that parsed before should continue to parse.
> If a query that parsed on an earlier version fails on v2.0.0, please [file an issue](https://github.com/duckdb/duckdb/issues).

## Installing and Loading

To install and load the `legacy_parser` extension, run:

```sql
INSTALL AND LOAD legacy_parser;
```

## Usage

To activate the legacy parser, run:

```sql
SET enable_legacy_parser = true;
```

To switch back to the PEG parser, run:

```sql
SET enable_legacy_parser = false;
```
