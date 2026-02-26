---
layout: docu
title: MotherDuck Extension
---

The `motherduck` (`md`) extension allows connecting to [MotherDuck](https://motherduck.com/), a cloud data warehouse built on DuckDB.

## Installing and Loading

The `motherduck` extension will be transparently [autoinstalled and autoloaded]({% link docs/preview/core_extensions/overview.md %}#autoloading-extensions) on first use from the official extension repository.
If you would like to install and load it manually, run:

```sql
INSTALL motherduck;
LOAD motherduck;
```

## Usage

You can connect to MotherDuck by executing the following command:

```sql
ATTACH 'md:';
```

## MotherDuck Documentation

For more details, see the [MotherDuck documentation](https://motherduck.com/docs/).
