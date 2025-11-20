---
layout: post
title: "Data-at-Rest Encryption in DuckDB"
author: "Lotte Felius, Hannes Mühleisen"
thumb: "/images/blog/thumbs/encryption-in-duckdb.svg"
image: "/images/blog/thumbs/encryption-in-duckdb.png"
excerpt: "DuckDB v1.4 ships database encryption capabilities. In this blog post, we dive into the implementation details of the encryption, show how to use it and demonstrate its performance implications."
tags: ["deep dive"]
---

> If you would like to use encryption in DuckDB, we recommend using the latest stable version, v1.4.2. For more details, see the [latest release blog post]({% post_url 2025-11-12-announcing-duckdb-142 %}#vulnerabilities).

Many years ago, we read the excellent “[Code Book](https://en.wikipedia.org/wiki/The_Code_Book)” by [Simon Singh](https://en.wikipedia.org/wiki/Simon_Singh). Did you know that [Mary, Queen of Scots](https://en.wikipedia.org/wiki/Mary,_Queen_of_Scots), used an [encryption method harking back to Julius Caesar](https://en.wikipedia.org/wiki/Caesar_cipher) to encrypt her more saucy letters? But alas: the cipher was broken and the contents of the letters got her [executed](https://en.wikipedia.org/wiki/Execution_of_Mary,_Queen_of_Scots).

These [days](https://en.wikipedia.org/wiki/Crypto_Wars), strong encryption software and hardware is a commodity. Modern CPUs [come with specialized cryptography instructions](https://developer.arm.com/documentation/ddi0602/2025-09/SIMD-FP-Instructions/AESE--AES-single-round-encryption-), and operating systems small and big contain [mostly](https://www.heartbleed.com/)-robust cryptography software like OpenSSL.

Databases store arbitrary information, it is clear that many if not most datasets of any value should perhaps not be plainly available to everyone. Even if stored on tightly controlled hardware like a cloud virtual machine, there have been [many cases](https://haveibeenpwned.com/) of files being lost through various privilege escalations. Unsurprisingly, compliance frameworks like the common [SOC 2](https://secureframe.com/hub/soc-2/what-is-soc-2) “highly recommend” encrypting data when stored on storage mediums like hard drives.

However, database systems and encryption have a somewhat problematic track record. Even PostgreSQL, the self-proclaimed “The World's Most Advanced Open Source Relational Database” has very [limited options](https://www.postgresql.org/docs/current/encryption-options.html) for data encryption. SQLite, the world’s “[Most Widely Deployed and Used Database Engine](https://www.sqlite.org/mostdeployed.html)” does not support data encryption out-of-the-box, its encryption extension is [a $2000 add-on](https://sqlite.org/com/see.html). 

**DuckDB** has supported [Parquet Modular Encryption](https://parquet.apache.org/docs/file-format/data-pages/encryption/) [for a while](https://duckdb.org/docs/stable/data/parquet/encryption). This feature allows reading and writing Parquet files with encrypted columns. However, while Parquet files are great and [reports of their impending death](https://materializedview.io/p/nimble-and-lance-parquet-killers) are greatly exaggerated, they cannot – for example – be updated in place, a pretty basic feature of a database management system.

Starting with DuckDB 1.4.0, DuckDB supports **transparent data encryption** of data-at-rest using industry-standard AES encryption.

> DuckDB's encryption does not yet meet the official [NIST requirements](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines).

## Some Basics of Encryption

There are many different ways to encrypt data, some more secure than others. In database systems and elsewhere, the standard is the [Advanced Encryption Standard](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) (AES), which is a block cipher algorithm standardized by [US NIST](https://en.wikipedia.org/wiki/National_Institute_of_Standards_and_Technology). AES is a symmetric encryption algorithm, meaning that the *same* key is used for both encryption and decryption of data.

For this reason, most systems choose to only support *randomized* encryption, meaning that identical plaintexts will always yield different ciphertexts (if used correctly!). The most commonly used industry standard and recommended encryption algorithm is AES – [Galois Counter Mode](https://en.wikipedia.org/wiki/Galois/Counter_Mode) (AES-GCM). This is because on top of its ability to randomize encryption, it also *authenticates* data by calculating a tag to ensure data has not been tampered with.

DuckDB v1.4 supports encryption at rest using AES-GCM-256 and AES-CTR-256 (counter mode) ciphers. AES-CTR is a simpler and faster version of AES-GCM, but less secure, since it does not provide authentication by calculating a tag. The 256 refers to the size of the key in bits, meaning that DuckDB now only supports GCM with 32-byte keys.

GCM and CTR both require as input a (1) plaintext, (2) an initialization vector (IV) and (3) an encryption key. Plaintext is the text that a user wants to encrypt. An IV is a unique bytestream of usually 16 bytes, that ensures that identical plaintexts get encrypted into different ciphertexts. A *number used once* (nonce) is a bytestream of usually 12 bytes, that together with a 4-byte counter construct the IV. Note that the IV needs to be unique for every encrypted block, but it does not necessarily have to be random. Reuse of the same IV is problematic, since an attacker could XOR the two ciphertexts and extract both messages. The tag in AES-GCM is calculated after all blocks are encrypted, pretty much like a checksum, but it adds an integrity check that securely authenticates the entire ciphertext.

## Implementation in DuckDB

Before diving deeper into how we actually implemented encryption in DuckDB, we’ll explain some things about the DuckDB file format.

DuckDB has one **main database header** which stores data that enables it to correctly load and verify a DuckDB database. At the start of each DuckDB main database header, the magic bytes (“DUCKDB”) are stored and read upon initialization to verify whether the file is a valid DuckDB database file. The magic bytes are followed by four 8-byte of flags that can be set for different purposes. 

When a database is encrypted in DuckDB, the main database header remains plaintext at all times, since the main header contains *no sensitive data* about the contents of the database file.
Upon initializing an encrypted database, DuckDB sets the first bit in the first flag to indicate that the database is encrypted. After setting this bit, additional metadata is stored that is necessary for encryption. This metadata entails the (1) *database identifier*, (2) 8 bytes of additional metadata for e.g. the encryption cipher used, and (3) the encrypted canary.

The *database identifier* is used as a “salt”, and consists of 16 randomly generated bytes created upon initialization of each database. The salt is often used to ensure uniqueness, i.e., it makes sure that identical input keys or passwords are transformed into *different* derived keys. The 8-bytes of metadata comprise the key derivation function (first byte), usage of additional authenticated data (second byte), the encryption cipher (third byte), and the key length (fifth byte). After the metadata, the main header uses the encrypted canary to check if the input key is correct.

### Encryption Key Management

To encrypt data in DuckDB, you can use practically *any* plaintext or base64 encoded string, but we recommend using a secure 32-byte base64 key. The user itself is responsible for the key management and thus for using a secure key. Instead of directly using the plain key provided by the user, DuckDB always derives a more secure key by means of a key derivation function (kdf). The kdf is a function that reduces or extends the input key to a 32-byte secure key. If the correctness of the input key is checked by deriving the secure key and decrypting the canary, the derived key is managed in a *secure* encryption key cache. This cache manages encryption keys for the current DuckDB context and ensures that the derived encryption keys are never swapped to disk by locking its memory. To strengthen security even more, the original input keys are immediately wiped from memory when the input keys are transformed into secure derived keys.

### DuckDB Block Structure

After the main database header, DuckDB stores two 4KB database headers that contain more information about e.g. the block (header) size and the storage version used. After keeping the main database header plaintext, *all* remaining headers and blocks are encrypted when encryption is used.

Blocks in DuckDB are by default 256KB, but their size is configurable. At the start of each *plaintext* block there is an 8-byte block header, which stores an 8-byte checksum. The checksum is a simple calculation that is often used in database systems to check for any corrupted data. 

<img src="{% link images/blog/encryption/plaintext-block-light.svg %}"
     alt="Plaintext block"
     class="lightmode-img"
     />
<img src="{% link images/blog/encryption/plaintext-block-dark.svg %}"
     alt="Plaintext block"
     class="darkmode-img"
     />

For encrypted blocks however, its block header consists of 40 bytes instead of 8 bytes for the checksum. The block header for encrypted blocks contains a 16-byte *nonce/IV* and, optionally, a 16-byte *tag*, depending on which encryption cipher is used. The nonce and tag are stored in plaintext, but the checksum is encrypted for better security. Note that the block header always needs to be 8-bytes aligned to calculate the checksum.

<img src="{% link images/blog/encryption/encrypted-block-light.svg %}"
     alt="Encrypted block"
     class="lightmode-img"
     />
<img src="{% link images/blog/encryption/encrypted-block-dark.svg %}"
     alt="Encrypted block"
     class="darkmode-img"
     />

### Write-Ahead-Log Encryption

The write ahead log (WAL) in database systems is a crash recovery mechanism to ensure *durability*. It is an append-only file that is used in scenarios where the database crashed or is abruptly closed, and when not all changes are written yet to the main database file. The WAL makes sure these changes can be replayed up to the last checkpoint; which is a consistent snapshot of the database at a certain point in time. This means, when a checkpoint is enforced, which happens in DuckDB by either (1) closing the database or (2) reaching a certain threshold for storage, the WAL gets written into the main database file.

In DuckDB, you can force the creation of a WAL by setting

```sql
PRAGMA disable_checkpoint_on_shutdown;
PRAGMA wal_autocheckpoint = '1TB';
```

This way you’ll disable a checkpointing on closing the database, meaning that the WAL does not get merged into the main database file. In addition, by setting wal_autocheckpoint to a high threshold, this will avoid intermediate checkpoints to happen and the WAL will persist. For example, we can create a persistent WAL file by first setting the above PRAGMAS, then attach an encrypted database, and then create a table where we insert 3 values.

```sql
ATTACH 'encrypted.db' as enc (
    ENCRYPTION_KEY 'asdf',
    ENCRYPTION_CIPHER 'GCM'
);
CREATE TABLE enc.test (a INTEGER, b INTEGER);
INSERT INTO enc.test VALUES (11, 22), (13, 22), (12, 21)
```

If we now close the DuckDB process, we can see that there is a `.wal` file shown: `encrypted.db.wal`. But how is the WAL created internally?

Before writing new entries (inserts, updates, deletes) to the database, these entries are essentially logged and appended to the WAL. Only *after* logged entries are flushed to disk, a transaction is considered as committed. A plaintext WAL entry has the following structure:

<img src="{% link images/blog/encryption/plaintext-wal-entry-light.svg %}"
     alt="Plaintext block"
     class="lightmode-img"
     />
<img src="{% link images/blog/encryption/plaintext-wal-entry-dark.svg %}"
     alt="Plaintext block"
     class="darkmode-img"
     />


Since the WAL is append-only, we encrypt a WAL entry *per value*. For AES-GCM this means that we append a nonce and a tag to each entry. The structure in which we do this is depicted in below. When we serialize an encrypted entry to the encrypted WAL, we first store the length in plaintext, because we need to know how many bytes we should decrypt. The length is followed by a nonce, which on its turn is followed by the encrypted checksum and the encrypted entry itself. After the entry, a 16-byte tag is stored for verification.

<img src="{% link images/blog/encryption/encrypted-wal-entry-light.svg %}"
     alt="Plaintext block"
     class="lightmode-img"
     />
<img src="{% link images/blog/encryption/encrypted-wal-entry-dark.svg %}"
     alt="Plaintext block"
     class="darkmode-img"
     />

Encrypting the WAL is triggered by default when an encryption key is given for any (un)encrypted database.

### Temporary File Encryption

Temporary files are used to store intermediate data that is often necessary for large, out-of-core operations such as large joins and [window functions](https://duckdb.org/2021/10/13/windowing). This data could contain sensitive information and can, in case of a crash, remain on disk. To protect this leftover data, DuckDB automatically encrypts temporary files too.

#### The Structure of Temporary Files

There are three different types of temporary files in DuckDB: (1) temporary files that have the same layout as a regular 256KB block, (2) compressed temporary files and (3) temporary files that exceed the standard 256KB block size. The former two are suffixed with .tmp, while the latter is distinguished by a suffix with .block. To keep track of the size of .block temporary files, they are always prefixed with its length. As opposed to regular database blocks, temporary files do not contain a checksum to check for data corruption, since the calculation of a checksum is somewhat expensive. 

#### Encrypting Temporary Files

Temporary files are encrypted (1) **automatically** when you attach an encrypted database or (2) when you use the setting `SET temp_file_encryption = true`. In the latter case, the main database file is plaintext, but the temporary files will be encrypted. For the encryption of temporary files DuckDB internally generates *temporary keys.* This means that when the database crashes, the temporary keys are also lost. Temporary files cannot be decrypted in this case and are then essentially garbage.

To force DuckDB to produce temporary files, you can use a simple trick by just setting the memory limit low. This will create temporary files once the memory limit is exceeded. For example, we can create a new encrypted database, load this database with TPC-H data (SF 1), and then set the memory limit to 1 GB. If we then perform a large join, we force DuckDB to spill intermediate data to disk. For example:

```sql
SET memory_limit = '1GB';
ATTACH 'tpch_encrypted.db' AS enc (
    ENCRYPTION_KEY 'asdf',
    ENCRYPTION_CIPHER '⟨cipher⟩'
);
USE enc;
CALL dbgen(sf = 1);

ALTER TABLE lineitem
    RENAME TO lineitem1;
CREATE TABLE lineitem2 AS
    FROM lineitem1;
CREATE OR REPLACE TABLE ans AS
    SELECT l1.* , l2.*
    FROM lineitem1 l1
    JOIN lineitem2 l2 USING (l_orderkey , l_linenumber);
```

This sequence of commands will result in encrypted temporary files being written to disk. Once the query completes or when the DuckDB shell is exited, the temporary files are automatically cleaned up. In case of a crash however, it may happen that temporary files will be left on disk and need to be cleaned up manually.

## How to Use Encryption in DuckDB

In DuckDB, you can (1) encrypt an existing database, (2) initialize a new, empty encrypted database or (3) reencrypt a database. For example, let's create a new database, load this database with TPC-H data of scale factor 1 and then encrypt this database.

install tpch;
load tpch;
ATTACH 'encrypted.duckdb' AS encrypted (ENCRYPTION_KEY 'asdf');
ATTACH 'unencrypted.duckdb' AS unencrypted;
USE unencrypted;
CALL dbgen(sf=1);
COPY FROM DATABASE unencrypted to encrypted;

There is not a trivial way to prove that a database is encrypted, but correctly encrypted data should look like random noise and has a high entropy. So, to check whether a database is actually encrypted, we can use tools to calculate the entropy or visualize the binary, such as [ent](https://github.com/lsauer/entropy) and [binocle](https://github.com/sharkdp/binocle).

When we use ent after executing the above chunk of SQL, i.e., `ent encrypted.duckdb`, this will result in an entropy of 7.99999 bits per byte. If we do the same for the plaintext (unencrypted) database, this results in 7.65876 bits per byte. Note that the plaintext database also has a high entropy, but this is due to compression.

Let’s now visualize both the plaintext and encrypted data with binocle. For the visualization we created both a plaintext DuckDB database with scale factor of 0.001 of TPC-H data and an encrypted one:

<div align="center">
    <img src="https://blobs.duckdb.org/images/duckdb-plaintext-database.png" width="800" />
    Entropy of a plaintext database
</div>

<div align="center" style="margin-top: 20px">
    <img src="https://blobs.duckdb.org/images/duckdb-encrypted-database.png" width="800" />
    Entropy of an encrypted database
</div>

In these figures, we can clearly observe that the encrypted database file seems completely random, while the plaintext database file shows some clear structure in its binary data.

To decrypt an encrypted database, we can use the following SQL:

```sql
ATTACH 'encrypted.duckdb' AS encrypted (ENCRYPTION_KEY 'asdf');
ATTACH 'new_unencrypted.duckdb' AS unencrypted;
COPY FROM DATABASE encrypted TO unencrypted;
```

And to reencrypt an existing database, we can just simply copy the old encrypted database to a new one, like:

```sql
ATTACH 'encrypted.duckdb' AS encrypted (ENCRYPTION_KEY 'asdf');
ATTACH 'new_encrypted.duckdb' AS new_encrypted (ENCRYPTION_KEY 'xxxx');
COPY FROM DATABASE encrypted TO new_encrypted;
```

The default encryption algorithm is AES GCM. This is recommended since it also authenticates data by calculating a tag. Depending on the use case, you can also use AES CTR. This is faster than AES GCM since it skips calculating a tag after encrypting all data. You can specify the CTR cipher as follows:

```sql
ATTACH 'encrypted.duckdb' AS encrypted (
    ENCRYPTION_KEY 'asdf',
    ENCRYPTION_CIPHER 'CTR'
);
```

To keep track of which databases are encrypted, you can query this by running:

```sql
FROM duckdb_databases();
```

This will show which databases are encrypted, and which cipher is used:

<div class="monospace_table"></div>

| database_name | database_oid | path                   | … | encrypted | cipher |
|---------------|--------------|------------------------|---|-----------|--------|
| encrypted     | 2103         | encrypted.duckdb       | … | true      | GCM    |
| unencrypted   | 2050         | unencrypted.duckdb     | … | false     | NULL   |
| memory        | 592          | NULL                   | … | false     | NULL   |
| system        | 0            | NULL                   | … | false     | NULL   |
| temp          | 1995         | NULL                   | … | false     | NULL   |

**5 rows —  10 columns (5 shown)**

## Implementation and Performance

Here at DuckDB, we strive to achieve a good out-of-the-box experience with zero external dependencies and a small footprint. Encryption and decryption, however, are usually performed by pretty heavy external libraries such as OpenSSL. We would much prefer not to rely on external libraries or statically linking huge codebases just so that people can use encryption in DuckDB without additional steps. This is why we actually implemented encryption *twice* in DuckDB, once with the (excellent) [Mbed TLS](https://github.com/Mbed-TLS/mbedtls) library and once with the ubiquitous OpenSSL library. 

DuckDB already shipped parts of Mbed TLS because we use it to verify RSA extension signatures. However, for maximum compatibility we actually disabled the hardware acceleration of MbedTLS, which has a performance impact. Furthermore, Mbed TLS is not particularly hardened against things like nasty timing attacks. OpenSSL on the other hand contains heavily vetted and hardware-accelerated code to perform AES operations, which is why we can also use it for encryption. 

In DuckDB Land, OpenSSL is part of the `httpfs` extension. Once you load that extension, encryption will *automatically* switch to using OpenSSL. After we shipped encryption in DuckDB 1.4.0, security experts actually found [issues with the random number generator](https://github.com/duckdb/duckdb/security/advisories/GHSA-vmp8-hg63-v2hp) we used in Mbed TLS mode. Even though it would be difficult to actually exploit this, we *disabled writing* to databases in MbedTLS mode from DuckDB 1.4.1. Instead, DuckDB now (version 1.4.2+) tries to auto-install and auto-load the `httpfs` extension whenever a write is attempted. We might be able to revisit this in the future, but for now this seems the safest path forward that still allows high compatibility for reading. In OpenSSL mode, we always used a cryptographically-safe random number generation so that mode is unaffected.

Encrypting and decrypting database files is an additional step in writing tables to disk, so we would naturally assume that there is some performance impact. Let’s investigate the performance impact of DuckDB’s new encryption feature with a very basic experiment. 

We first create two DuckDB database files, one encrypted and one unencrypted. We use the TPC-H benchmark generator again to create the table data, particularly the (somewhat tired) `lineitem` table. 

```sql
INSTALL httpfs;
INSTALL tpch;
LOAD tpch;

ATTACH 'unencrypted.duckdb' AS unencrypted;
CALL dbgen(sf = 10, catalog = 'unencrypted');

ATTACH 'encrypted.duckdb' AS encrypted (ENCRYPTION_KEY 'asdf');
CREATE TABLE encrypted.lineitem AS FROM unencrypted.lineitem;
```

Now we use DuckDB’s neat `SUMMARIZE` command three times: once on the unencrypted database, and once on the encrypted database using MbedTLS and once on the encrypted database using OpenSSL. We set a very low memory limit to force more reading and writing from disk.

```sql
SET memory_limit = '200MB';
.timer on

SUMMARIZE unencrypted.lineitem;
SUMMARIZE encrypted.lineitem;

LOAD httpfs; -- use OpenSSL
SUMMARIZE encrypted.lineitem;
```

Here are the results on a fairly recent MacBook: `SUMMARIZE` on the unencrypted table took ca. 5.4 seconds. Using Mbed TLS, this went up to around 6.2 s. However, when enabling OpenSSL the end-to-end time went straight back to 5.4 s. How is this possible? Is decryption not expensive? Well, there is a lot more happening in query processing than reading blocks from storage. So the impact of decryption is not all that huge, even when using a slow implementation. Secondly, when using hardware acceleration in OpenSSL, the overall overhead of encryption and decryption becomes almost negligible.

But just running summarization is overly simplistic. Real™ database workloads include modifications to data, insertion of new rows, updates of rows, deletion of rows etc. Also, multiple clients will be updating and querying at the same time. So we re-surrected the full TPC-H “Power” test from our previous blog post “[Changing Data with Confidence and ACID](https://duckdb.org/2024/09/25/changing-data-with-confidence-and-acid)”. We slightly tweaked the [benchmark script](https://github.com/duckdb/duckdb-tpch-power-test/blob/main/benchmark.py) to enable the new database encryption. For this experiment, we used the OpenSSL encryption implementation due to the issues outlined above. We observe Power@Size” and “Throughput@Size”. The former is raw sequential query performance, while the latter measures multiple parallel query streams in the presence of updates.

When running on the same MacBook with DuckDB 1.4.1 and a “scale factor” of 100, we get a Power@Size metric of 624,296 and a Throughput@Size metric of 450,409 *without* encryption. 

When we enable encryption, the results are almost unchanged, confirming the observation of the small microbenchmark above. However, the relationship between available memory and the benchmark size means that we’re not stressing temporary file encryption. So we re-ran everything with an 8GB memory limit. We confirmed constant reading and writing to and from disk in this configuration by observing operating system statistics. For the unencrypted case, the Power@Size metric predictably went down to 591,841 and Throughput@Size went down to 153,690. And finally, we could observe a slight performance decrease with Power@Size of 571,985 and Throughput@Size of 145,353. However, that difference is not very great either and likely not relevant in real operational scenarios.

## Conclusion

With the new encrypted database feature, we can now safely pass around DuckDB database files with all information inside them completely opaque to prying eyes. This allows for some interesting new deployment models for DuckDB, for example, we could now put an encrypted DuckDB database file on a Content Delivery Network (CDN). A fleet of DuckDB instances could attach to this file read-only using the decryption key. This elegantly allows efficient distribution of private background data in a similar way like encrypted Parquet files, but of course with many more features like multi-table storage. When using DuckDB with encrypted storage, we can also simplify threat modeling when – for example – using DuckDB on cloud providers. While in the past access to DuckDB storage would have been enough to leak data, we can now relax paranoia regarding storage a little,  especially since temporary files and WAL are also encrypted. And the best part of all of this, there is almost no performance overhead to using encryption in DuckDB, especially with the OpenSSL implementation.

We are very much looking forward to what you are going to do with this feature, and please [let us know](https://github.com/duckdb/duckdb/issues/new) if you run into any issues. 
