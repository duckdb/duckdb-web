---
layout: docu
title: Backup Extension Repositories
---

The core and community extension repositories have backup servers (see [duckdb-backup.org](https://www.duckdb-backup.org/)):

| Repository  | Primary server                           | Backup server                                   |
|:------------|:-----------------------------------------|:------------------------------------------------|
| `core`      | `http://extensions.duckdb.org`           | `http://extensions.duckdb-backup.org`           |
| `community` | `http://community-extensions.duckdb.org` | `http://community-extensions.duckdb-backup.org` |

The backup servers serve byte-identical binaries, so [signature checks]({% link docs/preview/operations_manual/securing_duckdb/securing_extensions.md %}) are unaffected.

## Using the Backup Server Manually

To always install core extensions from the backup server, run:

```sql
SET custom_extension_repository = 'http://extensions.duckdb-backup.org';
```
