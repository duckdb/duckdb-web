---
layout: community_extension_doc
title: Community Extensions
excerpt: |
  List of Community contributed open-source DuckDB extension 
---

Welcome to the documentation for the DuckDB Community Extensions.

This website contains all documentation specific to community contributed & maintained extensions for DuckDB.

DuckDB is an analytical in-process SQL database management system, documented at [DuckDB documentation Website](https://duckdb.org/docs/).

Community means that the extensions are created by external contributors and not maintained by [DuckDB Labs](https://duckdblabs.com/).

Extensions for DuckDB are the preferred way to package additional functionality for DuckDB. Generic extensions are documented in the [core DuckDB documentation](https://duckdb.org/docs/extensions/).

## How to Use a Community Extension

To install and load a community extension, for example the `quack` demo extension, simply run:

```sql
INSTALL quack FROM community;
LOAD quack;
```

The `quack` extension is now loaded and ready to use

```sql
SELECT quack('world');
```

## What are Community Extensions

Community Extensions are [DuckDB extensions]({% link docs/extensions/overview.md %}) that are not maintained by the DuckDB team.

They are different from the [Core Extensions]({% link docs/extensions/core_extensions.md %}), which *are* maintained by the DuckDB team, or from unsigned extensions, that are extensions that have an empty or invalid key.

Community Extensions are distributed via the Community Extension endpoint at `http(s)://community-extensions.duckdb.org`, and on `INSTALL` or `UPDATE EXTENSIONS` are retrieved from there.

Community Extension submissions and build process happens via the [Community Extension repo](https://github.com/duckdb/community-extensions).

Check the [Development page]({% link community_extensions/development.md %}) on how to contribute an extension.

DuckDB Community extensions are conceptually similar to a package manager such as [Homebrew](https://brew.sh/), where code will reside in your own repository, but build and distribution is centralized.

## Secure usage of DuckDB Community Extensions

DuckDB Community Extensions are signed, so that on LOAD a check is performed to prove a given extensions has been built by the Community Extension CI.

For more information on extensions and how to use them, check the [“Securing Extensions”]({% link docs/operations_manual/securing_duckdb/securing_extensions.md %}) and [“Working with Extensions”]({% link docs/extensions/working_with_extensions.md %}) pages.

In particular if you want to forbid `LOAD` of Community Extensions, run:

```sql
SET allow_community_extensions = false;
```

This will disable any subsequent load of extensions signed with the Community Extension key and lock the `allow_community_extensions` configuration.
