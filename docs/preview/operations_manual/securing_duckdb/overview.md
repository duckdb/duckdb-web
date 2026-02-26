---
layout: docu
title: Securing DuckDB
---

DuckDB is a powerful analytical database engine. It can read and write files, access the network, load extensions, 
and use system resources. Like any powerful tool, these capabilities require appropriate configuration when 
working with sensitive data or in shared environments.

This page documents DuckDB's security model and security-related settings. The right configuration depends on your use case, environment, and threat model.
If you plan to embed DuckDB in your application, also consult the ["Embedding DuckDB"]({% link docs/preview/operations_manual/securing_duckdb/embedding_duckdb.md %}) page.

## Untrusted Input

### Untrusted SQL Input

> Warning Treat SQL in DuckDB like code in Bash or Python. Do not execute SQL from untrusted sources without proper sandboxing.

DuckDB executes SQL with the full privileges of the user running it, much like a shell or scripting interpreter (such as bash or Python).
Just as you wouldn't run an untrusted shell script or Python program without sandboxing, apply the same caution to SQL in DuckDB.

If your application must execute SQL from untrusted sources, use additional safeguards when running untrusted code such as:

* Use [duckdb-wasm](https://github.com/duckdb/duckdb-wasm) for sandboxing
* Run DuckDB in an isolated container (e.g., Docker with restricted capabilities)
* Use a virtual machine or separate process with minimal privileges
* Apply operating system-level sandboxing
* Use network isolation to prevent data exfiltration
* Implement strict query timeouts at the application level

The settings described on this page provide **defense-in-depth** and can limit certain capabilities, but they are not a substitute for proper sandboxing. Also keep in mind that
sandboxing should not just be considered for security purposes, but also for preventing denial of service (DoS) attacks: malicious inputs can easily cause DuckDB to consume excessive resources such 
as memory, disk, CPU, or network.

### Untrusted Non-SQL Input

> Warning Even non-SQL input into DuckDB can easily have unintended consequences. When building security-sensitive applications with DuckDB, always make sure you properly understand the impact of feeding untrusted input into DuckDB.

Besides SQL, DuckDB also has several non-SQL APIs that can be used to interact with the database. For example, there is a [relational API]({% link docs/preview/clients/python/relational_api.md %}) in Python that allows building queries programmatically.

These APIs accept user input such as file paths, table names, column names, and filter expressions. While they don't execute raw SQL strings, they still trigger DuckDB operations that can read files, access the network, and use system resources.

**Example considerations for non-SQL APIs:**

* **File paths:** Functions like `duckdb.read_csv(path)` or `duckdb.read_parquet(path)` accept file paths. An attacker-controlled path could read sensitive files (e.g., `/etc/passwd`) or access remote URLs.
* **Table and column names:** While these are typically identifiers rather than executable code, unsanitized input could lead to unexpected behavior or information disclosure.
* **Filter expressions:** Some APIs accept filter expressions that are compiled into DuckDB expressions, which often support subqueries containing arbitrary SQL. Treat these with the same caution as SQL.

**Recommendations:**

* Validate and sanitize all user-provided inputs before passing them to DuckDB APIs.
* Apply the same sandboxing principles as for untrusted SQL when accepting input from untrusted sources.
* Properly read the documentation of all used functions to ensure you understand whether a function is safe to use with untrusted input under your specific use case.

## Extensions

DuckDB has a flexible [extension mechanism]({% link docs/preview/extensions/overview.md %}) that adds functionality such as new file formats, functions, and remote file system access. Extensions run with the same privileges as the DuckDB process itself, so they warrant careful consideration in security-sensitive environments.

### Autoloading

DuckDB can automatically load [core extensions]({% link docs/preview/core_extensions/overview.md %}) when certain SQL statements require them. To maintain full control over which extensions are loaded, you can disable autoloading:

```sql
SET autoload_known_extensions = false;
SET autoinstall_known_extensions = false;
```

### Core vs. Community Extensions

DuckDB extensions fall into two categories:

* **Core extensions:** Maintained by the DuckDB team with full support. These include extensions like `parquet`, `json`, and `httpfs`.
* **[Community extensions]({% link community_extensions/index.md %}):** Contributed by third parties and installed via `INSTALL extension_name FROM community`. These are not maintained by the DuckDB team, so only install community extensions from sources you trust.

To disable community extensions entirely:

```sql
SET allow_community_extensions = false;
```

## Reporting Vulnerabilities

If you discover a potential vulnerability, please [report it confidentially via GitHub](https://github.com/duckdb/duckdb/security/advisories/new).

## Settings to Limit DuckDB's Capabilities

The settings documented in this section provide additional hardening for DuckDB deployments. However, they should not be
relied upon as comprehensive security mechanisms in all configurations. These settings are designed as defense-in-depth
measures to limit the impact of potential security issues, but they cannot provide complete protection against all
attack vectors, especially when executing untrusted SQL. For robust security when dealing with untrusted input, combine
these settings with proper sandboxing at the operating system or container level, as described in
the ["Untrusted SQL Input"](#untrusted-sql-input) section.

### Safe Mode (CLI)

DuckDB's CLI client supports [“safe mode”]({% link docs/preview/clients/cli/safe_mode.md %}), which prevents DuckDB from accessing external files other than the database file.
This can be activated via a command line argument or a [dot command]({% link docs/preview/clients/cli/dot_commands.md %}):

```batch
duckdb -safe ...
```

```plsql
.safe_mode
```


### Restricting File Access

DuckDB can list directories and read arbitrary files via its CSV parser’s [`read_csv` function]({% link docs/preview/data/csv/overview.md %}) or read text via the [`read_text` function]({% link docs/preview/sql/functions/text.md %}#read_textsource).
This makes it possible to read from the local file system, for example:

```sql
SELECT *
FROM read_csv('/etc/passwd', sep = ':');
```

#### Disabling File Access

File access can be disabled in two ways. First, you can disable individual file systems. For example:

```sql
SET disabled_filesystems = 'LocalFileSystem';
```

Second, you can also completely disable external access by setting the [`enable_external_access` option]({% link docs/preview/configuration/overview.md %}#configuration-reference) option to `false`.

```sql
SET enable_external_access = false;
```

This setting implies that:

* `ATTACH` cannot attach to a database in a file.
* `COPY` cannot read from or write to files.
* Functions such as `read_csv`, `read_parquet`, `read_json`, etc. cannot read from an external source.

#### The `allowed_directories` and `allowed_paths` Options

You can restrict DuckDB's access to certain directories or files using the `allowed_directories` and `allowed_paths` options (respectively).
These options allow fine-grained access control for the file system.
For example, you can set DuckDB to only use the `/tmp` directory.

```sql
SET allowed_directories = ['/tmp'];
SET enable_external_access = false;
FROM read_csv('test.csv');
```

With the setting applied, DuckDB will refuse to read files in the current working directory:

```console
Permission Error:
Cannot access file "test.csv" - file system operations are disabled by configuration
```

### Locking Configurations

Security-related configuration settings generally lock themselves for safety reasons. For example, while we can disable [community extensions]({% link community_extensions/index.md %}) using the `SET allow_community_extensions = false`, we cannot re-enable them again after the fact without restarting the database. Trying to do so will result in an error:

```console
Invalid Input Error: Cannot upgrade allow_community_extensions setting while database is running
```

This prevents re-enabling settings that were explicitly disabled.

Nevertheless, many configuration settings do not disable themselves, such as the resource constraints. If you allow users to run SQL statements unrestricted on your own hardware, you might want to consider locking the configuration after your own configuration has finished using the following command:

```sql
SET lock_configuration = true;
```

This prevents any configuration settings from being modified from that point onwards.

## Secrets

[Secrets]({% link docs/preview/configuration/secrets_manager.md %}) are used to manage credentials to log into third party services like AWS or Azure. DuckDB can show a list of secrets using the `duckdb_secrets()` table function. This will redact any sensitive information such as security keys by default. The `allow_unredacted_secrets` option can be set to show all information contained within a security key. It is recommended not to turn on this option if you are running untrusted SQL input.

Queries can access the secrets defined in the Secrets Manager. For example, if there is a secret defined to authenticate with a user, who has write privileges to a given AWS S3 bucket, queries may write to that bucket. This is applicable for both persistent and temporary secrets.

[Persistent secrets]({% link docs/preview/configuration/secrets_manager.md %}#persistent-secrets) are stored in unencrypted binary format on the disk. These have the same permissions as SSH keys, `600`, i.e., only the user who is running the DuckDB (parent) process can read and write them.

## Prepared Statements to Prevent SQL Injection

Similarly to other SQL databases, it's recommended to use [prepared statements]({% link docs/preview/sql/query_syntax/prepared_statements.md %}) in DuckDB to prevent [SQL injection](https://en.wikipedia.org/wiki/SQL_injection).

> Important Prepared statements protect against SQL injection when **you control the query structure** but accept **untrusted data values** (e.g., user-provided search terms or IDs). If users can supply the SQL query itself, this is equivalent to allowing them to run arbitrary code – see ["Untrusted SQL Input"](#untrusted-sql-input).

**Therefore, avoid concatenating strings for queries:**

```python
import duckdb
duckdb.execute("SELECT * FROM (VALUES (32, 'a'), (42, 'b')) t(x) WHERE x = " + str(42)).fetchall()
```

**Instead, use prepared statements:**

```python
import duckdb
duckdb.execute("SELECT * FROM (VALUES (32, 'a'), (42, 'b')) t(x) WHERE x = ?", [42]).fetchall()
```

## Constrain Resource Usage

DuckDB can use quite a lot of CPU, RAM, and disk space. These resources can be limited to control the usage of the DuckDB instance.

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

## Privileges

Avoid running DuckDB as a root user (e.g., using `sudo`).
There is no good reason to run DuckDB as root.
