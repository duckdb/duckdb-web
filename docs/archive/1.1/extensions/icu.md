---
github_directory: https://github.com/duckdb/duckdb/tree/main/extension/icu
layout: docu
title: ICU Extension
---

The `icu` extension contains an easy-to-use version of the collation/timezone part of the [ICU library](https://github.com/unicode-org/icu).

## Installing and Loading

The `icu` extension will be transparently [autoloaded]({% link docs/archive/1.1/extensions/overview.md %}#autoloading-extensions) on first use from the official extension repository.
If you would like to install and load it manually, run:

```sql
INSTALL icu;
LOAD icu;
```

## Features

The `icu` extension introduces the following features:

* [Region-dependent collations]({% link docs/archive/1.1/sql/expressions/collations.md %})
* [Time zones]({% link docs/archive/1.1/sql/data_types/timezones.md %}), used for [timestamp data types]({% link docs/archive/1.1/sql/data_types/timestamp.md %}) and [timestamp functions]({% link docs/archive/1.1/sql/functions/timestamptz.md %})