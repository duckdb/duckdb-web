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

## Automatic Fallback

Fallback is automatic: if the primary server is unreachable or returns a 5xx error, `INSTALL` retries the download from the backup server. No configuration is needed.

* A 4xx error (e.g., a non-existent extension) is reported directly, without contacting the backup server.
* The fallback only applies to the built-in `core` and `community` repositories. Repositories set via `custom_extension_repository` or `INSTALL ... FROM '⟨url⟩'` are used as-is.
* The installed extension's origin is still recorded as `core` or `community`.

## Using the Backup Server Manually

To always install core extensions from the backup server, run:

```sql
SET custom_extension_repository = 'http://extensions.duckdb-backup.org';
```
