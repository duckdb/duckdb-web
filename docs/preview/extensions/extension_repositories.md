---
layout: docu
title: Extension Repositories
---

> New Support for custom extension repositories is introduced in DuckDB 2.0. This feature is currently work-in-progress and the syntax may still change.

By default, DuckDB installs extensions from its built-in repositories (`core`, `core_nightly`, `community`, …). In addition, you can register your own trusted repositories, so that an organization can host and sign its own extensions and have them install and load just like the built-in ones.

A repository is a name, a URL prefix, and one or more RSA public keys that are trusted to sign the extensions served from it.

## Enabling Custom Repositories

Adding custom repositories is gated by the `allow_extension_repositories` setting. It has three values:

* `undecided` (the default): adding new repositories is blocked, but existing repositories remain trusted.
* `allowed`: custom repositories can be added.
* `forbidden`: adding new repositories is blocked and existing custom repositories are distrusted.

While the database is running, the setting can only move from `undecided` to `allowed` or `forbidden`, or from `allowed` to `forbidden`. To opt in:

```sql
SET allow_extension_repositories = 'allowed';
```

## Creating a Repository

The prefix can point at anything DuckDB can read: a local path, [`https`]({% link docs/preview/core_extensions/httpfs/https.md %}), [`s3`]({% link docs/preview/core_extensions/httpfs/s3api.md %}), and so on.

```sql
CREATE EXTENSION REPOSITORY my_repo
    WITH PREFIX 'https://extensions.example.org';
```

At `CREATE` time, DuckDB fetches the repository's public keys and pins them into the repository definition, printing each key's SHA-256 fingerprint so you can compare it against one published out of band.

If you would rather not trust the network, you can pass the key directly:

```sql
CREATE EXTENSION REPOSITORY my_repo
    WITH PREFIX 'https://extensions.example.org'
    USING PUBLIC KEY '-----BEGIN PUBLIC KEY----- ...';
```

Extensions are signed using 2048-bit RSA keys. The key can be provided either in PEM format or as the base64-encoded body of the PEM format.

## Using a Repository

Once a repository is registered, install and load its extensions by referring to the repository by name:

```sql
INSTALL my_ext FROM my_repo;
LOAD my_ext;
```

## Inspecting Repositories

Pinned repositories survive restarts, support key rotation by trusting multiple keys, and can be audited at any time through the `duckdb_extension_repositories()` table function:

```sql
SELECT repository_name, prefix, key_fingerprints
FROM duckdb_extension_repositories();
```

## Dropping a Repository

```sql
DROP EXTENSION REPOSITORY my_repo;
```
