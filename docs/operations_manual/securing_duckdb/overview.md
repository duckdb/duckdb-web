---
layout: docu
title: Securing DuckDB
---

DuckDB is quite powerful, which can be problematic, especially if untrusted SQL queries are run, e.g., from public-facing user inputs.
This page lists some options to restrict the potential fallout from malicious SQL queries.

The approach to securing DuckDB varies depending on your use case, environment, and potential attack models.
Therefore, consider the security-related configuration options carefully, especially when working with confidential data sets.

## Reporting Vulnerabilities

If you discover a potential vulnerability, please [report it confidentially via GitHub](https://github.com/duckdb/duckdb/security/advisories/new).

## Disabling File Access

DuckDB can list directories and read arbitrary files via its CSV parser’s [`read_csv` function]({% link docs/data/csv/overview.md %}) or read text via the [`read_text` function]({% link docs/sql/functions/char.md %}#read_textsource). For example:

```sql
SELECT *
FROM read_csv('/etc/passwd', sep = ':');
```

This can be disabled either by disabling external access altogether (`enable_external_access`) or disabling individual file systems. For example:

```sql
SET disabled_filesystems = 'LocalFileSystem';
```

## Secrets

[Secrets]({% link docs/configuration/secrets_manager.md %}) are used to manage credentials to log into third party services like AWS or Azure. DuckDB can show a list of secrets using the `duckdb_secrets()` table function. This will redact any sensitive information such as security keys by default. The `allow_unredacted_secrets` option can be set to show all information contained within a security key. It is recommended not to turn on this option if you are running untrusted SQL input.

Queries can access the secrets defined in the Secrets Manager. For example, if there is a secret defined to authenticate with a user, who has write privileges to a given AWS S3 bucket, queries may write to that bucket. This is applicable for both persistent and temporary secrets.

[Persistent secrets]({% link docs/configuration/secrets_manager.md %}#persistent-secrets) are stored in unencrypted binary format on the disk. These have the same permissions as SSH keys, `600`, i.e., only user who is running the DuckDB (parent) process can read and write them.

## Locking Configurations

Security-related configuration settings generally lock themselves for safety reasons. For example, while we can disable community extensions using the `SET allow_community_extensions = false`, we cannot re-enable them again after the fact without restarting the database. Trying to do so will result in an error:

```console
Invalid Input Error: Cannot upgrade allow_community_extensions setting while database is running
```

This prevents untrusted SQL input from re-enabling settings that were explicitly disabled for security reasons.

Nevertheless, many configuration settings do not disable themselves, such as the resource constraints. If you allow users to run SQL statements unrestricted on your own hardware, it is recommended that you lock the configuration after your own configuration has finished using the following command:

```sql
SET lock_configuration = true;
```

This prevents any configuration settings from being modified from that point onwards.

## Constrain Resource Usage

DuckDB can use quite a lot of CPU, RAM, and disk space. To avoid denial of service attacks, these resources can be limited.

The number of CPU threads that DuckDB can use can be set using, for example:

```sql
SET threads = 4;
```

Where 4 is the number of allowed threads.

The maximum amount of memory (RAM) can also be limited, for example:

```sql
SET memory_limit = '4GB';
```

The size of the temporary file directory can be limited with:

```sql
SET max_temp_directory_size = '4GB';
```

## Extensions

DuckDB has a powerful extension mechanism, which have the same privileges as the user running DuckDB's (parent) process.
This introduces security considerations. Therefore, we recommend reviewing the configuration options for [securing extensions]({% link docs/operations_manual/securing_duckdb/securing_extensions.md %}).

## Generic Solutions

Securing DuckDB can also be supported via proven means, for example:

* Scoping user privileges via [`chroot`](https://en.wikipedia.org/wiki/Chroot), relying on the operating system
* Containerization, e.g., Docker and Podman
* Running DuckDB in WebAssembly
