---
layout: docu
redirect_from:
- /docs/operations_manual/securing_duckdb/encryption
title: Database Encryption
---

DuckDB supports transparent data-at-rest encryption using the [Advanced Encryption Standard (AES)](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard). Starting with version 1.4.0, you can encrypt database files to protect sensitive data stored on disk.

## What Gets Encrypted

When encryption is enabled, DuckDB encrypts:

* The main database file.
* The write-ahead log (WAL) file.
* Temporary files (encrypted automatically when you attach an encrypted database).

The main database header remains unencrypted as it contains no sensitive data.

## Supported Encryption Ciphers

DuckDB supports two AES encryption modes:

| Cipher | Description | Recommendation |
|--------|-------------|----------------|
| **AES-GCM-256** | Galois/Counter Mode with authentication tag | Default and recommended |
| **AES-CTR-256** | Counter mode without authentication | Faster but less secure |

We recommend AES-GCM because it authenticates data by calculating a tag, ensuring data has not been tampered with.

## Creating an Encrypted Database

To create a new encrypted database, use the [`ATTACH` statement]({% link docs/stable/sql/statements/attach.md %}) with the `ENCRYPTION_KEY` option:

```sql
ATTACH 'encrypted.db' AS enc_db (ENCRYPTION_KEY 'your-secure-key');
```

To specify a different cipher:

```sql
ATTACH 'encrypted.db' AS enc_db (
    ENCRYPTION_KEY 'your-secure-key',
    ENCRYPTION_CIPHER 'CTR'
);
```

## Encrypting an Existing Database

To encrypt an existing unencrypted database:

```sql
ATTACH 'unencrypted.db' AS source;
ATTACH 'encrypted.db' AS target (ENCRYPTION_KEY 'your-secure-key');
COPY FROM DATABASE source TO target;
```

## Decrypting a Database

To create an unencrypted copy of an encrypted database:

```sql
ATTACH 'encrypted.db' AS source (ENCRYPTION_KEY 'your-secure-key');
ATTACH 'unencrypted.db' AS target;
COPY FROM DATABASE source TO target;
```

## Re-encrypting with a New Key

To change the encryption key:

```sql
ATTACH 'old_encrypted.db' AS old_db (ENCRYPTION_KEY 'old-key');
ATTACH 'new_encrypted.db' AS new_db (ENCRYPTION_KEY 'new-key');
COPY FROM DATABASE old_db TO new_db;
```

## Checking Encryption Status

To check which databases are encrypted and which cipher is used:

```sql
FROM duckdb_databases();
```

This returns columns including `encrypted` (boolean) and `cipher` (the encryption cipher used).

## Performance Considerations

DuckDB can use two implementations for encryption:

| Implementation | Source | Performance |
|----------------|--------|-------------|
| **MbedTLS** | Built-in | Slower (no hardware acceleration) |
| **OpenSSL** | `httpfs` extension | Faster (hardware accelerated) |

For better performance, load the `httpfs` extension before attaching encrypted databases:

```sql
LOAD httpfs;
ATTACH 'encrypted.db' AS enc_db (ENCRYPTION_KEY 'your-secure-key');
```

The performance overhead of encryption is minimal when using OpenSSL with hardware acceleration.

## Temporary File Encryption

DuckDB automatically encrypts temporary files when you attach an encrypted database. To encrypt temporary files without encrypting the main database:

```sql
SET temp_file_encryption = true;
```

This is useful when working with sensitive data in queries that spill to disk.

## Key Management

You are responsible for managing encryption keys securely. DuckDB:

* Derives a secure 32-byte key from your input using a key derivation function.
* Never stores the encryption key in the database file.
* Wipes input keys from memory after deriving secure keys.
* Stores derived keys in a memory-locked cache to prevent swapping to disk.

We recommend using a secure 32-byte base64-encoded key.

## Limitations

> DuckDB's encryption does not yet meet the official [NIST requirements](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines).
> See issue [#20162](https://github.com/duckdb/duckdb/issues/20162) to track progress towards NIST compliance.

* Key management is the user's responsibility.
* Database encryption requires [storage version]({% link docs/stable/sql/statements/attach.md %}#explicit-storage-versions) 1.4.0 or later.

## Related Documentation

* [ATTACH Statement]({% link docs/stable/sql/statements/attach.md %}#database-encryption) – Encryption options for ATTACH.
* [Parquet Encryption]({% link docs/stable/data/parquet/encryption.md %}) – Encrypting individual Parquet files.
