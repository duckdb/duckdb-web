---
layout: docu
title: Safe Mode
---

The DuckDB CLI client supports “safe mode”.
In safe mode, the CLI is prevented from accessing external files other than the database file that it was initially connected to and prevented from interacting with the host file system.

This has the following effects:

* The following [dot commands]({% link docs/stable/clients/cli/dot_commands.md %}) are disabled:
    * `.cd`
    * `.excel`
    * `.import`
    * `.log`
    * `.once`
    * `.open`
    * `.output`
    * `.read`
    * `.sh`
    * `.system`
* Auto-complete no longer scans the file system for files to suggest as auto-complete targets.
* The [`getenv` function]({% link docs/stable/clients/cli/overview.md %}#reading-environment-variables) is disabled.
* The [`enable_external_access` option]({% link docs/stable/configuration/overview.md %}#configuration-reference) is set to `false`. This implies that:
    * `ATTACH` cannot attach a database from an on-disk file.
    * `COPY` cannot read to/write from files.
    * `read_csv`, `read_parquet`, `read_json`, etc. cannot read from disk.

Once safe mode is activated, it cannot be deactivated in the same DuckDB CLI session.
