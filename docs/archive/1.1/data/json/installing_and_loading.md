---
layout: docu
title: Installing and Loading the JSON extension
---

The `json` extension is shipped by default in DuckDB builds, otherwise, it will be transparently [autoloaded]({% link docs/archive/1.1/extensions/overview.md %}#autoloading-extensions) on first use. If you would like to install and load it manually, run:

```sql
INSTALL json;
LOAD json;
```