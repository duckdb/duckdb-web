---
layout: docu
title: Publishing an Extension Repository
---

> New Support for custom extension repositories was introduced in DuckDB 2.0.0. This page describes the state as of DuckDB 2.0.1: registering a repository by its host, and with it the `version` and `repository_url` fields of the metadata file, require 2.0.1. DuckDB 2.0.0 reads only `signature_keys`, from a repository added `WITH PREFIX`. This feature is currently work-in-progress and the file format may still change.

This page describes how to publish a repository of DuckDB extensions that users can register with [`CREATE EXTENSION REPOSITORY`]({% link docs/2.0/extensions/extension_repositories.md %}) and then install and load from as they do from the built-in repositories. A repository consists of three things:

* A directory structure, served over HTTPS, S3, or a local path, that holds the extension files.
* A signing key pair. Every extension in the repository is signed with the private key.
* A metadata file, `.well-known/duckdb-extension-repo.json`, that publishes the public keys and, for a repository registered by its host, says where the repository is.

DuckDB checks that every extension it installs or loads from the repository is signed with one of the published keys. That is the whole of what DuckDB verifies: it does not inspect what the extensions do, and it makes no claim about the repository beyond the signature. What the repository serves, and keeping the private key private, is the publisher's responsibility.

## The Metadata File

The metadata file is a JSON object of at most 64 KiB, served at `.well-known/duckdb-extension-repo.json` relative to the repository's root. The `.well-known/` path is the [well-known URI](https://www.rfc-editor.org/rfc/rfc8615) prefix defined by RFC 8615 for metadata that applies to a whole host, which is what makes it the right place for a file that speaks for the host. It publishes the repository's signing keys:

```json
{
    "version": 1,
    "repository_url": "https://extensions.example.org",
    "signature_keys": ["-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----\n"]
}
```

* `version`: the format version, currently `1`.
* `repository_url`: the URL at which the repository is served, without a trailing slash. It must use `https`.
* `signature_keys`: the public keys trusted to sign the repository's extensions, each in PEM format or as the base64-encoded body of the PEM format. List every key that is currently in use, see [“Rotating Keys”](#rotating-keys).

When a user registers the repository with `CREATE EXTENSION REPOSITORY extensions.example.org;`, DuckDB reads `https://extensions.example.org/.well-known/duckdb-extension-repo.json` over verified HTTPS, follows `repository_url`, reads the metadata file there, and pins the `signature_keys` it finds. When the repository is served on the host itself, as above, both reads hit the same file. When the extensions are served elsewhere, e.g., from a CDN or an object store, the host's file only needs `version` and `repository_url`, and the file at the repository URL carries the `signature_keys`:

```json
{
    "version": 1,
    "repository_url": "https://cdn.example.org/duckdb-extensions"
}
```

This is how DuckDB's own repository is published: `https://duckdb.org/.well-known/duckdb-extension-repo.json` names `https://extensions.duckdb.org`, whose metadata file carries the keys.

For a user who registers the repository by prefix with `CREATE EXTENSION REPOSITORY my_repo WITH PREFIX 'https://extensions.example.org';`, only `signature_keys` is read, from the metadata file under the given prefix.

The host that users name must be a host on the public internet, with two or more dot-separated labels and a letters-only last label, and it must serve the file over HTTPS with a valid certificate. A repository on a local path, an IP address, or an internal single-label host can only be registered by prefix.

DuckDB uses DNS and HTTPS to map a host name to its repository, the same way a browser maps it to a site: the name resolves to a server, the certificate proves the server is the host, and the file at `https://⟨host⟩/.well-known/duckdb-extension-repo.json`{:.language-sql .highlight} is taken as the host's own statement. Users who name your host trust whoever publishes at its root, so publish the file only on a host whose root you control. If your extensions live under a path on a host you do not control, e.g., a project page or a shared bucket, the host form is not for you: publish the keys in the metadata file under your prefix instead, and have users register the repository `WITH PREFIX`.

## Directory Structure

The repository serves the extension files in the same structure as DuckDB's own repositories, described in the [“Downloading Extensions Directly from S3” section]({% link docs/2.0/extensions/advanced_installation_methods.md %}#downloading-extensions-directly-from-s3):

```text
base_repository_path_or_url
├── .well-known
│   └── duckdb-extension-repo.json
└── v2.0.0
    └── osx_arm64
        ├── my_ext.duckdb_extension.gz
        └── other_ext.duckdb_extension.gz
```

To support [installing a specific version]({% link docs/2.0/extensions/versioning_of_extensions.md %}#installing-a-specific-extension-version) of an extension, also serve it at the following path:

```text
base_repository_path_or_url/⟨extension_name⟩/⟨extension_version⟩/v⟨duckdb_version⟩/⟨platform_name⟩/⟨extension_name⟩.duckdb_extension.gz
```

When installing an extension, DuckDB first looks for `⟨extension_name⟩.duckdb_extension.gz`{:.language-sql .highlight} and then for the uncompressed `⟨extension_name⟩.duckdb_extension`{:.language-sql .highlight}. This fallback only applies to repositories that are read through a file system, i.e., local paths and HTTPS or S3 URLs. For `http://` repositories, DuckDB only requests the gzipped file.

See the [`extension-template` repository](https://github.com/duckdb/extension-template/) for the code and scripts to build extensions and set up a repository.

## Creating a Key Pair

Extensions are signed using 2048-bit RSA keys. To create a key pair:

```bash
openssl genrsa -out signing_key.pem 2048
openssl rsa -in signing_key.pem -pubout -out signing_key.pub
```

The public key goes into the metadata file's `signature_keys`. The private key signs the extensions and should be kept out of the repository and out of version control.

DuckDB identifies a key by its fingerprint, the SHA-256 hash of the DER-encoded public key, and reports it when a user registers the repository. Publish the fingerprint through a second channel, e.g., on a web page or in a README, so that users can compare it. To compute it for a public key file:

```bash
openssl pkey -pubin -in signing_key.pub -outform DER | openssl dgst -sha256
```

## Signing Extensions

DuckDB verifies an extension's signature when it is installed and every time it is loaded. The signature occupies the last 256 bytes of the extension file and covers all bytes before it, including the [metadata footer]({% link docs/2.0/extensions/extension_distribution.md %}#binary-compatibility). Extension builds leave these 256 bytes zeroed.

The signed value is not a plain hash of the file. The bytes before the signature are split into 1 MiB chunks, each chunk is hashed with SHA-256, and the concatenated digests are hashed with SHA-256 again. The [`compute-extension-hash.sh` script](https://github.com/duckdb/duckdb/blob/main/scripts/compute-extension-hash.sh) computes this value.

To sign an extension and add it to the directory structure above:

```bash
size=$(wc -c < my_ext.duckdb_extension)
head -c $((size - 256)) my_ext.duckdb_extension > my_ext.unsigned
./scripts/compute-extension-hash.sh my_ext.unsigned > my_ext.hash
openssl pkeyutl -sign -in my_ext.hash -inkey signing_key.pem -pkeyopt digest:sha256 -out my_ext.sig
mkdir -p repository/v2.0.0/linux_amd64
cat my_ext.unsigned my_ext.sig | gzip > repository/v2.0.0/linux_amd64/my_ext.duckdb_extension.gz
```

Because only the last 256 bytes change, an existing build can be re-signed without rebuilding it. The [`extension-upload-single.sh` script](https://github.com/duckdb/duckdb/blob/main/scripts/extension-upload-single.sh) performs these steps when `DUCKDB_EXTENSION_SIGNING_PK` is set, and the [`verify-extension-signing.sh` script](https://github.com/duckdb/duckdb/blob/main/scripts/verify-extension-signing.sh) checks uncompressed signed extensions against a public key.

## Rotating Keys

Users pin the keys when they register the repository and only update them by registering it again, so a new key has to be announced before it is used. To move to a new signing key:

1. Add the new public key to `signature_keys`, keeping the old one, and announce the change. Users [pin both keys]({% link docs/2.0/extensions/extension_repositories.md %}#rotating-keys) by running `CREATE OR REPLACE EXTENSION REPOSITORY`. Publishing a spare key from the start, before it is ever used, avoids this step.
1. Re-sign the published extensions with the new key.
1. Once users have had time to reinstall, remove the old key from `signature_keys`.

Extensions signed with a key that a user has not pinned fail to install and load for that user, so leave enough time between the steps. There is no key revocation or expiry: a compromised key stays trusted by every user until each of them removes it, so rotate and announce promptly.

## Security Considerations

* The metadata file is the trust root. Whoever can write to `.well-known/duckdb-extension-repo.json` on the host or at the repository URL chooses which keys users pin, and to DuckDB that party is the host. Protect write access to it as you would protect the private key, and know who else can publish at the host's root, e.g., through a hosting platform's shared namespace.
* Signatures carry no timestamp. Anyone who can write to the repository can serve an older, validly signed build, so protect write access to the extension files as well.
* DuckDB follows redirects when reading the host's metadata file. A redirect away from the host is the host's own decision and is trusted as such.

See also the [“Securing Extensions” page]({% link docs/2.0/operations_manual/securing_duckdb/securing_extensions.md %}).
