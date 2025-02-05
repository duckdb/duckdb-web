---
layout: docu
title: Securing Extensions
---

DuckDB has a powerful extension mechanism, which have the same privileges as the user running DuckDB's (parent) process.
This introduces security considerations. Therefore, we recommend reviewing the configuration options listed on this page and setting them according to your attack models.

## DuckDB Signature Checks

DuckDB extensions are checked on every load using the signature of the binaries.
There are currently three categories of extensions:

* Signed with a `core` key. Only extensions vetted by the core DuckDB team are signed with these keys.
* Signed with a `community` key. These are open-source extensions distributed via the [DuckDB Community Extensions repository]({% link community_extensions/index.md %}).
* Unsigned.

## Overview of Security Levels for Extensions

DuckDB offers the following security levels for extensions.

| Usable extensions | Description | Configuration |
|-----|---|---|
| `core` | Extensions can only be loaded if signed from a `core` key. | `SET allow_community_extensions = false` |
| `core` and `community` | Extensions can only be loaded if signed from a `core` or `community` key. | This is the default security level. |
| Any extension including unsigned | Any extensions can be loaded. | `SET allow_unsigned_extensions = true` |

Security-related configuration settings [lock themselves]({% link docs/operations_manual/securing_duckdb/overview.md %}#locking-configurations), i.e., it is only possible to restrict capabilities in the current process.

For example, attempting the following configuration changes will result in an error:

```sql
SET allow_community_extensions = false;
SET allow_community_extensions = true;
```

```console
Invalid Input Error: Cannot upgrade allow_community_extensions setting while database is running
```

## Community Extensions

DuckDB has a [Community Extensions repository]({% link community_extensions/index.md %}), which allows convenient installation of third-party extensions.
Community extension repositories like pip or npm are essentially enabling remote code execution by design. This is less dramatic than it sounds. For better or worse, we are quite used to piping random scripts from the web into our shells, and routinely install a staggering amount of transitive dependencies without thinking twice. Some repositories like CRAN enforce a human inspection at some point, but that’s no guarantee for anything either.

We’ve studied several different approaches to community extension repositories and have picked what we think is a sensible approach: we do not attempt to review the submissions, but require that the *source code of extensions is available*. We do take over the complete build, sign and distribution process. Note that this is a step up from pip and npm that allow uploading arbitrary binaries but a step down from reviewing everything manually. We allow users to [report malicious extensions](https://github.com/duckdb/community-extensions/security/advisories/new) and show adoption statistics like GitHub stars and download count. Because we manage the repository, we can remove problematic extensions from distribution quickly.

Despite this, installing and loading DuckDB extensions from the community extension repository will execute code written by third party developers, and therefore *can* be dangerous. A malicious developer could create and register a harmless-looking DuckDB extension that steals your crypto coins. If you’re running a web service that executes untrusted SQL from users with DuckDB, it is probably a good idea to disable community extension installation and loading entirely. This can be done like so:

```sql
SET allow_community_extensions = false;
```

## Disabling Autoinstalling and Autoloading Known Extensions

By default, DuckDB automatically installs and loads known extensions.

To disable autoinstalling known extensions, run:

```sql
SET autoinstall_known_extensions = false;
```

To disable autoloading known extensions, run:

```sql
SET autoload_known_extensions = false;
```

To lock this configuration, use the [`lock_configuration` option]({% link docs/operations_manual/securing_duckdb/overview.md %}#locking-configurations):

```sql
SET lock_configuration = true;
```

## Always Require Signed Extensions

By default, DuckDB requires extensions to be either signed as core extensions (created by the DuckDB developers) or community extensions (created by third-party developers but distributed by the DuckDB developers). The `allow_unsigned_extensions` setting can be enabled on start-up to allow running extensions that are not signed at all. While useful for extension development, enabling this setting will allow DuckDB to load any extensions, which means more care must be taken to ensure malicious extensions are not loaded.
