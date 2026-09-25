---
layout: community_extension_doc
title: Community Extensions
excerpt: |
  List of Community contributed open-source DuckDB extension 
redirect_from:
- /ce
---

Welcome to the documentation for the DuckDB Community Extensions.

This website contains all documentation specific to community-contributed extensions for DuckDB.

DuckDB is an analytical in-process SQL database management system, documented at [DuckDB documentation website]({% link docs/current/index.md %}).

Community means that the extensions are created by external contributors and not maintained by [DuckLabs](https://ducklabs.com/).

Extensions for DuckDB are the preferred way to package additional functionality for DuckDB. Generic extensions are documented in the [core DuckDB documentation]({% link docs/current/core_extensions/overview.md %}).

## How to Use a Community Extension

To install and load a community extension, for example the `waddle` demo extension, simply run:

```sql
INSTALL waddle FROM community;
LOAD waddle;
```

The `waddle` extension is now loaded and ready to use

```sql
SELECT waddle('world');
```

## What Are Community Extensions?

Community Extensions are [DuckDB extensions]({% link docs/current/core_extensions/overview.md %}) that are not maintained by the DuckDB team.

They are different from the [Core Extensions]({% link docs/current/core_extensions/overview.md %}), which *are* maintained by the DuckDB team, or from unsigned extensions, that are extensions that have an empty or invalid key.

Community Extensions are distributed via the Community Extension endpoint at `http(s)://community-extensions.duckdb.org`, and on `INSTALL` or `UPDATE EXTENSIONS` are retrieved from there.

Community Extension submissions and build process happens via the [Community Extension repo](https://github.com/duckdb/community-extensions).

Check the [Development page]({% link community_extensions/development.md %}) on how to contribute an extension.

DuckDB Community extensions are conceptually similar to a package manager such as [Homebrew](https://brew.sh/), where code will reside in your own repository, but build and distribution is centralized.

## Security Considerations for Using Community Extensions

> Warning Community extensions are contributed by third parties. They are not written, audited, or maintained by Duck Labs, and they run with the same privileges as DuckDB itself, including access to your data, filesystem, and network. Signing proves only that an extension was built by the Community Extension CI from the published source. It does not certify that the code is safe or free of bugs. Install and load community extensions only if you trust their author and source.

DuckDB Community Extensions are signed, so that on LOAD a check is performed to prove a given extensions has been built by the Community Extension CI.

For more information on extensions and how to use them, check the [“Securing Extensions”]({% link docs/current/operations_manual/securing_duckdb/securing_extensions.md %}) and [“Installing Extensions”]({% link docs/current/extensions/installing_extensions.md %}) pages.

In particular if you want to forbid `LOAD` of Community Extensions, run:

```sql
SET allow_community_extensions = false;
```

This will disable any subsequent load of extensions signed with the Community Extension key and lock the `allow_community_extensions` configuration.
