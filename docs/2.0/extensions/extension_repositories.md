---
layout: docu
redirect_from:
- /docs/current/extensions/extension_repositories
- /docs/lts/extensions/extension_repositories
- /docs/preview/extensions/extension_repositories
- /docs/stable/extensions/extension_repositories
title: Extension Repositories
---

> New Support for custom extension repositories was introduced in DuckDB 2.0. This feature is currently work-in-progress and the syntax may still change.

By default, DuckDB installs extensions from its built-in repositories (`core`, `core_nightly`, `community`, …). In addition, you can register your own trusted repositories, so that an organization can host and sign its own extensions and have them install and load just like the built-in ones.

A repository is a name, a URL prefix, and one or more RSA public keys that are trusted to sign the extensions served from it.

## Enabling Custom Repositories

Adding custom repositories is gated by the `allow_extension_repositories` setting. It has three values:

* `undecided` (the default): adding new repositories and installing extensions from existing repositories are blocked. Existing repositories remain trusted, so extensions already installed from them can still be loaded.
* `allowed`: custom repositories can be added and extensions can be installed from them.
* `forbidden`: adding new repositories is blocked and existing custom repositories are distrusted, so extensions installed from them can no longer be loaded.

While the database is running, the setting can only move from `undecided` to `allowed` or `forbidden`, or from `allowed` to `forbidden`. To opt in:

```sql
SET allow_extension_repositories = 'allowed';
```

The setting is not persisted. Set it again in each session that creates a repository or installs an extension from one.

## Creating a Repository

The prefix can point at anything DuckDB can read: a local path, [`https`]({% link docs/2.0/core_extensions/httpfs/https.md %}), [`s3`]({% link docs/2.0/core_extensions/httpfs/s3api.md %}), and so on.

```sql
CREATE EXTENSION REPOSITORY my_repo
    WITH PREFIX 'https://extensions.example.org';
```

At `CREATE` time, DuckDB fetches the repository's public keys from `⟨prefix⟩/.well-known/duckdb-extension-repo.json`{:.language-sql .highlight} and pins them into the repository definition, printing each key's SHA-256 fingerprint so you can compare it against one published out of band. The keys are not fetched again after this point.

The file contains a JSON object of at most 64 KiB. Its `signature_keys` array lists the keys:

```json
{"signature_keys": ["-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----\n"]}
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

Extensions are signed using 2048-bit RSA keys. The key can be provided either in PEM format or as the base64-encoded body of the PEM format. This also applies to the entries of the `signature_keys` array.

The fingerprint is the SHA-256 hash of the DER-encoded public key. To compute it for a public key file:

```batch
openssl pkey -pubin -in signing_key.pub -outform DER | openssl dgst -sha256
```

`CREATE OR REPLACE EXTENSION REPOSITORY` replaces an existing definition, and `CREATE EXTENSION REPOSITORY IF NOT EXISTS` leaves it unchanged.

Repository definitions are stored locally in `~/.duckdb/extension_repositories`, so each machine or container image has to create the repository once. To use a different directory, set `extension_repository_directory` at startup. The `home_directory` setting does not change this location.

## Signing Extensions

DuckDB verifies an extension's signature when it is installed and every time it is loaded. The signature occupies the last 256 bytes of the extension file and covers all bytes before it, including the [metadata footer]({% link docs/2.0/extensions/extension_distribution.md %}#binary-compatibility). Extension builds leave these 256 bytes zeroed.

The signed value is not a plain hash of the file. The bytes before the signature are split into 1 MiB chunks, each chunk is hashed with SHA-256, and the concatenated digests are hashed with SHA-256 again. The [`compute-extension-hash.sh` script](https://github.com/duckdb/duckdb/blob/main/scripts/compute-extension-hash.sh) computes this value.

To create a key pair:

```batch
openssl genrsa -out signing_key.pem 2048
openssl rsa -in signing_key.pem -pubout -out signing_key.pub
```

To sign an extension and add it to the [repository's directory structure]({% link docs/2.0/extensions/extension_distribution.md %}#creating-a-custom-repository):

```batch
size=$(wc -c < my_ext.duckdb_extension)
head -c $((size - 256)) my_ext.duckdb_extension > my_ext.unsigned
./scripts/compute-extension-hash.sh my_ext.unsigned > my_ext.hash
openssl pkeyutl -sign -in my_ext.hash -inkey signing_key.pem -pkeyopt digest:sha256 -out my_ext.sig
mkdir -p repository/v2.0.0/linux_amd64
cat my_ext.unsigned my_ext.sig | gzip > repository/v2.0.0/linux_amd64/my_ext.duckdb_extension.gz
```

Because only the last 256 bytes change, an existing build can be re-signed without rebuilding it. The [`extension-upload-single.sh` script](https://github.com/duckdb/duckdb/blob/main/scripts/extension-upload-single.sh) performs these steps when `DUCKDB_EXTENSION_SIGNING_PK` is set, and the [`verify-extension-signing.sh` script](https://github.com/duckdb/duckdb/blob/main/scripts/verify-extension-signing.sh) checks uncompressed signed extensions against a public key.

## Using a Repository

Once a repository is registered, install and load its extensions by referring to the repository by name:

```sql
INSTALL AND LOAD my_ext FROM my_repo;
```

In later sessions, only load the extension, which does not require setting `allow_extension_repositories` to `allowed`:

```sql
LOAD my_ext FROM my_repo;
```

Extensions from custom repositories are installed into a separate subdirectory for each repository, `⟨extension_directory⟩/⟨duckdb_version⟩/⟨platform⟩/repositories/⟨repository_name⟩`{:.language-sql .highlight}. This has the following consequences:

* A plain `LOAD my_ext;` does not find the extension. For the same reason, these extensions are never [autoloaded]({% link docs/2.0/extensions/overview.md %}#autoloading-extensions).
* In `INSTALL AND LOAD`, the repository has to be given as an identifier: `INSTALL AND LOAD my_ext FROM 'my_repo';` installs the extension but then fails to load it.
* [`UPDATE EXTENSIONS`]({% link docs/2.0/sql/statements/update_extensions.md %}) skips these extensions. To upgrade one, run `FORCE INSTALL my_ext FROM my_repo;`.
* [`duckdb_extensions()`]({% link docs/2.0/sql/meta/duckdb_table_functions.md %}#duckdb_extensions) only lists these extensions once they are loaded, reporting `installed` as `false` and `signature_key_fingerprint` as `NULL`.

The pinned keys only apply when the repository is referred to by name. The following statements verify the extension against DuckDB's built-in `core` keys instead, so they reject extensions signed with your own key unless `allow_unsigned_extensions` is enabled:

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
SELECT repository_name, prefix, key_fingerprints
FROM duckdb_extension_repositories();
```

## Rotating Keys

Pinned keys only change when the repository is created again. To move to a new signing key:

1. On each client, pin both keys using `CREATE OR REPLACE EXTENSION REPOSITORY` with `USING PUBLIC KEYS`. This step is not needed if the new key was pinned from the start.
1. Re-sign the published extensions with the new key.
1. On each client, run `FORCE INSTALL` for the installed extensions.
1. On each client, remove the old key using `CREATE OR REPLACE EXTENSION REPOSITORY`.

Removing a key makes extensions signed with it fail on the next `LOAD`, so complete the third step first.

## Dropping a Repository

```sql
DROP EXTENSION REPOSITORY my_repo;
```

## Security Considerations

* Without `USING PUBLIC KEY`, whoever controls the repository's key file at `CREATE` time chooses the pinned keys. Compare the printed fingerprints against a value published through another channel.
* There is no key revocation or expiry. A compromised key remains trusted until each client removes it.
* Signatures carry no timestamp, so pinning does not protect against rollback: anyone who can write to the repository can serve an older, validly signed build.

See also the [“Securing Extensions” page]({% link docs/2.0/operations_manual/securing_duckdb/securing_extensions.md %}).
