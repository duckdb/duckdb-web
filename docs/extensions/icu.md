---
layout: docu
title: ICU Extension
github_directory: https://github.com/duckdb/duckdb/tree/main/extension/icu
---

The `icu` extension contains an easy-to-use version of the collation/timezone part of the [ICU library](https://github.com/unicode-org/icu).

## Installing and Loading

The `icu` extension will be transparently [autoloaded]({% link docs/extensions/overview.md %}#autoloading-extensions) on first use from the official extension repository.
If you would like to install and load it manually, run:

```sql
INSTALL icu;
LOAD icu;
```

## Features

The `icu` extension introduces the following features:

* [region-dependent collations]({% link docs/sql/expressions/collations.md %})
* [time zones]({% link docs/sql/data_types/timezones.md %}), used for [timestamp data types]({% link docs/sql/data_types/timestamp.md %}) and [timestamp functions]({% link docs/sql/functions/timestamptz.md %})
