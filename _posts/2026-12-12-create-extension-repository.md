---
layout: post
title: "Publishing Custom Extension Repositories for DuckDB"
authors:
  - Geertjan Wielenga
thumb: "/images/blog/thumbs/custom-extension-repositories.svg"
image: "/images/blog/thumbs/custom-extension-repositories.png"
excerpt: "DuckDB 2.0 lets developers publish custom extension repositories and users register them with CREATE EXTENSION REPOSITORY. Extensions are signed to verify authenticity, and repositories can be served from HTTPS, HTTP, S3, or local paths."
tag: release
---

DuckDB 2.0 added the ability to publish your own extension repositories. Users can register custom repositories with [`CREATE EXTENSION REPOSITORY`]({% link docs/2.0/extensions/extension_repositories.md %}) and install extensions from them alongside the built-in ones. The framework relies on cryptographic signatures to verify that extensions come from a trusted publisher. Host-based registration (e.g., `CREATE EXTENSION REPOSITORY extensions.example.org;`) requires DuckDB 2.0.1; in 2.0.0, only the prefix form (`WITH PREFIX`) was supported.

## What You Need to Publish a Repository

A custom extension repository consists of three components:

1. **Extension files**: Built binaries organized in a standard directory structure
2. **A key pair**: 2048-bit RSA keys for signing and verifying extensions
3. **A metadata file**: `.well-known/duckdb-extension-repo.json` published from your host

The metadata file is the trust root. It tells users where the repository is and which public keys sign the extensions:

```json
{
    "version": 1,
    "repository_url": "https://extensions.example.org",
    "signature_keys": ["-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----\n"]
}
```

## The Two Registration Patterns

Users can register your repository in two ways:

```sql
-- By host (requires a public HTTPS domain)
CREATE EXTENSION REPOSITORY extensions.example.org;

-- By prefix (works from anywhere: local paths, internal hosts, CDNs)
CREATE EXTENSION REPOSITORY my_repo WITH PREFIX 'https://extensions.example.org';
```

When registering by host, DuckDB reads `.well-known/duckdb-extension-repo.json` from that host and pins the keys it finds. This requires that your host has two or more dot-separated labels (a domain, not an IP address) and a valid HTTPS certificate.

The prefix form is more flexible. Users provide the full path to your repository, and DuckDB reads the metadata file from there. This works for local paths, internal single-label hosts, and repositories served from CDNs, S3, or object storage that you do not fully control. When using HTTP (unencrypted), DuckDB only requests gzipped extension files; uncompressed files fall back only for HTTPS, S3, and file paths.

## How DuckDB's Own Repository Works

DuckDB's official repository follows the host-based pattern:

```sql
CREATE EXTENSION REPOSITORY duckdb.org;
```

DuckDB reads `https://duckdb.org/.well-known/duckdb-extension-repo.json`, which names `https://extensions.duckdb.org` as the actual repository URL. This separation lets DuckDB control the trust root while serving extensions from a dedicated CDN. The metadata file at the CDN carries the actual signing keys.

## Signing Extensions

Every extension file is signed with your private key. DuckDB verifies the signature when it installs and every time it loads the extension.

The signing process splits the extension file into 1 MiB chunks, hashes each with SHA-256, concatenates the digests, and hashes again. That value is signed with your private key, and the resulting 256-byte signature replaces the last 256 bytes of the extension file.

DuckDB provides scripts to do this:

```bash
# Generate the key pair
openssl genrsa -out signing_key.pem 2048
openssl rsa -in signing_key.pem -pubout -out signing_key.pub

# Compute the hash and sign
./scripts/compute-extension-hash.sh my_ext.unsigned > my_ext.hash
openssl pkeyutl -sign -in my_ext.hash -inkey signing_key.pem -pkeyopt digest:sha256 -out my_ext.sig

# Combine the unsigned extension with the signature
cat my_ext.unsigned my_ext.sig | gzip > repository/v2.0.0/linux_amd64/my_ext.duckdb_extension.gz
```

The public key goes into the metadata file. Publish its fingerprint (the SHA-256 hash of the DER-encoded key) through a secondary channel—a website, a README, or a community post—so users can verify they are pinning the right key.

## Directory Structure

Serve your extensions in the same structure as DuckDB's repositories:

```text
repository/
├── .well-known/
│   └── duckdb-extension-repo.json
└── v2.0.0/
    ├── linux_amd64/
    │   ├── my_ext.duckdb_extension.gz
    │   └── other_ext.duckdb_extension.gz
    └── osx_arm64/
        └── my_ext.duckdb_extension.gz
```

To support [installing specific versions]({% link docs/2.0/extensions/versioning_of_extensions.md %}#installing-a-specific-extension-version), also serve extensions at:

```text
repository/⟨extension_name⟩/⟨extension_version⟩/v⟨duckdb_version⟩/⟨platform⟩/⟨extension_name⟩.duckdb_extension.gz
```

## Rotating Keys

Since DuckDB pins the public keys when users register your repository, changing keys requires coordination. To rotate to a new key:

1. Add the new key to `signature_keys` in your metadata file, while keeping the old one
2. Announce the change and give users time to run `CREATE OR REPLACE EXTENSION REPOSITORY` to update their pinned keys
3. Re-sign all published extensions with the new key
4. Once users have upgraded, remove the old key from the metadata file

Signatures have no timestamp, so an older build signed with a pinned key remains valid indefinitely. Protect write access to both your metadata file and your extension files as carefully as you protect your private key.

## Getting Started

The [`extension-template` repository](https://github.com/duckdb/extension-template/) is the starting point for building extensions. For setting up the repository itself, the [`extension-repository-template`](https://github.com/duckdb/extension-repository-template) provides the directory structure, scripts for signing and uploading extensions, and a template for the metadata file. DuckDB also provides utility scripts for computing extension hashes and verifying signatures.

For a working example, see [carlopi's example DuckDB extension repository](https://carlopi.github.io/example-duckdb-extension-repository/), which demonstrates a complete setup with signing, hosting, and documentation.

If you publish an extension repository, we'd like to hear about it. Email [geertjan@ducklabs.com](mailto:geertjan@ducklabs.com).
