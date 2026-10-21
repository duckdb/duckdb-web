---
github_directory: https://github.com/duckdb/duckdb/tree/main/extension/icu
layout: docu
redirect_from:
- /docs/extensions/ice
- /docs/stable/extensions/icu
- /docs/stable/core_extensions/icu
- /docs/current/core_extensions/icu
- /docs/lts/core_extensions/icu
- /docs/preview/core_extensions/icu
title: ICU Extension
---

The `icu` extension provides collation, time zone, and calendar support.

> New In DuckDB 2.0, the dependency on the external [ICU library](https://github.com/unicode-org/icu) was removed. The `icu` extension now implements collations, time zones, and calendars natively, with time zone data built directly from the [IANA Time Zone Database](https://www.iana.org/time-zones). Behavior is unchanged, and the native implementation is smaller and faster. If you ship a custom build, note that ICU is no longer bundled.

## Installing and Loading

The `icu` extension will be transparently [autoloaded]({% link docs/2.0/extensions/overview.md %}#autoloading-extensions) on first use from the official extension repository.
If you would like to install and load it manually, run:

```sql
INSTALL AND LOAD icu;
```

## Features

The `icu` extension introduces the following features:

* [Region-dependent collations]({% link docs/2.0/sql/expressions/collations.md %})
* [Time zones]({% link docs/2.0/sql/data_types/timezones.md %}), used for [timestamp data types]({% link docs/2.0/sql/data_types/timestamp.md %}) and [timestamp functions]({% link docs/2.0/sql/functions/timestamptz.md %})
