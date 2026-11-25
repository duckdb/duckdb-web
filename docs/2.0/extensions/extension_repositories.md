---
layout: docu
redirect_from:
- /docs/current/extensions/extension_repositories
- /docs/lts/extensions/extension_repositories
- /docs/preview/extensions/extension_repositories
- /docs/stable/extensions/extension_repositories
title: Extension Repositories
---

> New Support for custom extension repositories was introduced in DuckDB 2.0.0. This page describes the state as of DuckDB 2.0.1: registering a repository by its host, the `hosts` and `hosts_only` values of `allow_extension_repositories`, and the `host` column of `duckdb_extension_repositories()` require 2.0.1. In 2.0.0, repositories are added `WITH PREFIX` only, and the setting has the values `undecided` (the default), `allowed`, and `forbidden`. This feature is currently work-in-progress and the syntax may still change.

By default, DuckDB installs extensions from its built-in repositories (`core`, `core_nightly`, `community`, …). In addition, you can register repositories run by others, so that extensions an organization publishes and signs itself install and load just like the built-in ones.

A repository is a name, a URL prefix, and one or more RSA public keys. DuckDB checks that every extension installed or loaded from the repository is signed with one of these keys, and that is the only check it performs: see [“What DuckDB Checks”](#what-duckdb-checks). This page covers registering and using a repository. Setting one up is described on the [“Publishing an Extension Repository” page]({% link docs/2.0/extensions/publishing_extension_repositories.md %}).

## Adding a Repository by Its Host

The simplest way to register a repository is to name the publisher's host:

```sql
CREATE EXTENSION REPOSITORY extensions.example.org;
INSTALL AND LOAD my_ext FROM extensions.example.org;
```

This works out of the box: no setting has to be changed first, and no URL or key has to be typed. The name says who is trusted, and the host says where its extensions are and which keys sign them. DuckDB reads `https://extensions.example.org/.well-known/duckdb-extension-repo.json` over verified HTTPS, takes the repository URL from it, then fetches the signing keys from `⟨repository_url⟩/.well-known/duckdb-extension-repo.json`{:.language-sql .highlight} and pins them. The statement returns the repository's name, its prefix, and the SHA-256 fingerprint of each pinned key, so you can compare them against a value published out of band. The keys are not fetched again after this point.

The name must be a host on the public internet: two or more dot-separated labels, with a letters-only last label, so a single word, an IP address, or `localhost` is refused. Names may be written as dotted identifiers or as strings, wherever a repository is named:

```sql
INSTALL my_ext FROM 'extensions.example.org';
```

Reading from the host requires the [`httpfs` extension]({% link docs/2.0/core_extensions/httpfs/overview.md %}), which is autoloaded when available. A secret or setting that disables certificate verification for the host makes the statement fail: a repository is only resolved from a host that is verified.

DuckDB's own repository is published this way: `duckdb.org` names `https://extensions.duckdb.org` as the repository, and the keys are served from there. Registering it adds nothing that the built-in `core` repository does not already provide, but it shows the mechanism end to end:

```sql
CREATE EXTENSION REPOSITORY duckdb.org;
```

<!-- markdownlint-disable MD034 -->

<div class="monospace_table"></div>

| repository_name | prefix                        | key_fingerprints                                                                  |
|-----------------|-------------------------------|-----------------------------------------------------------------------------------|
| duckdb.org      | https://extensions.duckdb.org | [sha256:a319de1f13bc85a0af0c51d5ca47e3aff9680d8333e895a3a35e5ff97a69dc12, …]      |

<!-- markdownlint-enable MD034 -->

The first fingerprint is that of the key currently signing DuckDB's extensions; the list continues with the keys held in reserve. The same keys are built into DuckDB, so they can be compared against the ones in `duckdb_extensions()` for a loaded `core` extension. From here on the repository is used like any other:

```sql
INSTALL inet FROM duckdb.org;
```

## Adding a Repository by Its Prefix

Alternatively, name the repository's location directly. The prefix can point at anything DuckDB can read: a local path, [`https`]({% link docs/2.0/core_extensions/httpfs/https.md %}), [`s3`]({% link docs/2.0/core_extensions/httpfs/s3api.md %}), and so on.

```sql
CREATE EXTENSION REPOSITORY my_repo
    WITH PREFIX 'https://extensions.example.org';
```

With a prefix, the keys are fetched from `⟨prefix⟩/.well-known/duckdb-extension-repo.json`{:.language-sql .highlight}, pinned, and reported as above. Because you rather than the host decide what is trusted, this form requires an [opt-in](#controlling-which-repositories-can-be-added) first:

```sql
SET allow_extension_repositories = 'allowed';
```

If you would rather not trust the network, you can pass the key directly:

```sql
CREATE EXTENSION REPOSITORY my_repo
    WITH PREFIX 'https://extensions.example.org'
    USING PUBLIC KEY '-----BEGIN PUBLIC KEY----- ...';
```

To pin several keys, e.g., to prepare for [key rotation](#rotating-keys), use `USING PUBLIC KEYS` with a comma-separated list:

```sql
CREATE EXTENSION REPOSITORY my_repo
    WITH PREFIX 'https://extensions.example.org'
    USING PUBLIC KEYS '⟨current_key⟩', '⟨next_key⟩';
```

A key can be given in PEM format or as the base64-encoded body of the PEM format. Keys cannot be passed when the repository is resolved from its host: the host's file is the only source of what the host vouches for.

`CREATE OR REPLACE EXTENSION REPOSITORY` replaces an existing definition, and `CREATE EXTENSION REPOSITORY IF NOT EXISTS` leaves it unchanged.

Repository definitions are stored locally in `~/.duckdb/extension_repositories`, so each machine or container image has to create the repository once. To use a different directory, set `extension_repository_directory` at startup. The `home_directory` setting does not change this location.

## Controlling Which Repositories Can Be Added

By default, DuckDB does not restrict host-based repositories: any user of the database can add one by naming its host, and extensions from every registered repository can be installed and loaded. Adding a repository by prefix, on the other hand, requires an opt-in, because there the user rather than the host decides which keys get trusted. Restricting things further is an opt-in as well, in either of two directions: forbidding the creation of new repositories, or forbidding the use of any.

The `allow_extension_repositories` setting decides which repositories can be added and which are trusted. It has four values:

* `hosts` (the default): repositories can be added by naming their host. Adding one by prefix requires `allowed`. Existing repositories, however they were added, stay trusted.
* `allowed`: repositories can be added by host or by prefix.
* `hosts_only`: only repositories resolved from their host can be added, and only those are trusted. Extensions installed from a repository that was added by prefix can no longer be installed or loaded.
* `forbidden`: no repository can be added, and all custom repositories are distrusted.

While the database is running, the setting is a ratchet: it can only be tightened, in the order `hosts` → `allowed` → `hosts_only` → `forbidden`, and never loosened again. Whoever sets the value first wins. Once an application or an operator has set `hosts_only` or `forbidden`, no later statement in that database, from a user, a script, or an extension, can bring custom repositories back, because moving back to `allowed` or `hosts` fails from there. Likewise, `allowed` can only be chosen before anything has tightened the setting.

To forbid the use of any custom repository, set:

```sql
SET allow_extension_repositories = 'forbidden';
```

To keep using the repositories that are already registered but forbid adding or dropping any, lock the configuration instead. This freezes the trust store without changing it:

```sql
SET lock_configuration = true;
```

Neither setting is persisted, so set them again in each session, typically at startup. See also the [“Securing Extensions” page]({% link docs/2.0/operations_manual/securing_duckdb/securing_extensions.md %}#custom-extension-repositories).

## Using a Repository

Once a repository is registered, install and load its extensions by referring to the repository by name:

```sql
INSTALL AND LOAD my_ext FROM extensions.example.org;
```

In later sessions, only load the extension:

```sql
LOAD my_ext FROM extensions.example.org;
```

Extensions from custom repositories are installed into a separate subdirectory for each repository, `⟨extension_directory⟩/⟨duckdb_version⟩/⟨platform⟩/repositories/⟨repository_name⟩`{:.language-sql .highlight}. This has the following consequences:

* A plain `LOAD my_ext;` does not find the extension. For the same reason, these extensions are never [autoloaded]({% link docs/2.0/extensions/overview.md %}#autoloading-extensions).
* [`UPDATE EXTENSIONS`]({% link docs/2.0/sql/statements/update_extensions.md %}) skips these extensions. To upgrade one, run `FORCE INSTALL my_ext FROM extensions.example.org;`.
* [`duckdb_extensions()`]({% link docs/2.0/sql/meta/duckdb_table_functions.md %}#duckdb_extensions) lists these extensions once they are installed, reporting `installed` as `true`, the repository name in `installed_from`, and the signing key fingerprint in `signature_key_fingerprint`. `loaded` is `false` until the extension is loaded.

The pinned keys only apply when the repository is referred to by name. The following statements verify the extension against DuckDB's built-in `core` keys instead, so they reject extensions signed with a publisher's own key unless `allow_unsigned_extensions` is enabled:

```sql
INSTALL my_ext FROM 'https://extensions.example.org';

SET custom_extension_repository = 'https://extensions.example.org';
INSTALL my_ext;

INSTALL 'https://extensions.example.org/v2.0.0/linux_amd64/my_ext.duckdb_extension.gz';

LOAD './my_ext.duckdb_extension';
```

## Inspecting Repositories

Pinned repositories survive restarts, support key rotation by trusting multiple keys, and can be audited at any time through the `duckdb_extension_repositories()` table function:

```sql
SELECT repository_name, host, prefix, key_fingerprints
FROM duckdb_extension_repositories();
```

`host` is set for repositories that were resolved from their host and `NULL` for those added by prefix.

## Rotating Keys

Pinned keys only change when the repository is created again. When a publisher [rotates its signing key]({% link docs/2.0/extensions/publishing_extension_repositories.md %}#rotating-keys), each client has to:

1. Pin both the old and the new key with `CREATE OR REPLACE EXTENSION REPOSITORY`, naming the host or, for a repository added by prefix, using `USING PUBLIC KEYS`. This step is not needed if both keys were pinned from the start.
1. Once the publisher has re-signed the extensions, run `FORCE INSTALL` for the installed extensions.
1. Once the publisher has removed the old key, run `CREATE OR REPLACE EXTENSION REPOSITORY` again to drop it.

Removing a key makes extensions signed with it fail on the next `LOAD`, so complete the second step first.

## Dropping a Repository

```sql
DROP EXTENSION REPOSITORY extensions.example.org;
```

## What DuckDB Checks

DuckDB guarantees one thing about an extension installed or loaded from a custom repository: its signature verifies against one of the keys pinned for that repository, and those keys are the ones served, at `CREATE` time, by the host or prefix you named, or the ones you passed yourself. In other words, the extension comes from whoever holds the publisher's signing key, and it has not been altered since it was signed.

DuckDB makes no other claim about what a custom repository publishes and performs no other check on it. It does not review the extension's code, does not know what the extension does once loaded, does not vouch for the publisher, and does not check that the repository keeps serving the same extensions over time. A loaded extension runs with the full privileges of the DuckDB process. Registering a repository is a decision to trust its publisher to the same degree as installing their software by any other means.

The check holds against the network and the repository: a tampered download, a hostile mirror, or a compromised CDN cannot make DuckDB load an extension the publisher did not sign. It does not hold against whoever controls the machine DuckDB runs on. The pinned keys live in a file under the home directory, the `extension_repository_directory` setting chooses that file, and `allow_unsigned_extensions` switches the check off, so anyone who can write to the user's files or set these options can bypass it. As for the rest of DuckDB, the guarantee assumes that the host, the user running DuckDB, and the SQL being executed are trusted. See the [“Securing DuckDB” page]({% link docs/2.0/operations_manual/securing_duckdb/overview.md %}) for the security model.

## Security Considerations

* A repository resolved from its host relies on the same machinery as the web: DNS and HTTPS map the host name to a server, and that server's `/.well-known/duckdb-extension-repo.json`, a [well-known URI](https://www.rfc-editor.org/rfc/rfc8615) reserved for site-wide metadata, is taken as the host's own statement of where its repository is and which keys sign it. Naming a host therefore means trusting whoever publishes at that host's root at `CREATE` time, just as visiting the site would. A path on a shared host, such as a project page, is not a host and is not reached by this form. `WITH PREFIX` without `USING PUBLIC KEY` works the same way with the prefix in place of the host. Compare the reported fingerprints against a value published through another channel.
* There is no key revocation or expiry. A compromised key remains trusted until each client removes it.
* Signatures carry no timestamp, so pinning does not protect against rollback: anyone who can write to the repository can serve an older, validly signed build.

See also the [“Securing Extensions” page]({% link docs/2.0/operations_manual/securing_duckdb/securing_extensions.md %}).
