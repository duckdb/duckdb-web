---
layout: docu
redirect_from:
- /docs/preview/core_extensions/motherduck
title: MotherDuck Extension
---

The `motherduck` extension allows connecting to [MotherDuck](https://motherduck.com/), a cloud data warehouse built on DuckDB.

## Installing and Loading

The `motherduck` extension will be transparently [autoinstalled and autoloaded]({% link docs/current/core_extensions/overview.md %}#autoloading-extensions) on first use from the official extension repository.
If you would like to install and load it manually, you can use the `motherduck` extension name or the `md` shorthand:

```sql
INSTALL md;
LOAD md;
```

## Usage

You can connect to MotherDuck by executing the following command:

```sql
ATTACH 'md:';
```

## Platforms

The `windows_arm64` platform is currently not supported.

## MotherDuck Documentation

For more details, see the [MotherDuck documentation](https://motherduck.com/docs/).
