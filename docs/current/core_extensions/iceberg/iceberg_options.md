---
layout: docu
title: Iceberg Options
---

This page lists the options of the `iceberg` extension: the parameters accepted by the [Iceberg functions]({% link docs/current/core_extensions/iceberg/iceberg_functions.md %}), the options of the `ATTACH` and `CREATE SECRET` statements used to [connect to a catalog]({% link docs/current/core_extensions/iceberg/catalogs.md %}), and the global settings.


## `ATTACH` Options

To make an Iceberg Catalog (not just a single table) known to the system, you'll need to use the `ATTACH` statement.
The options provided to the `ATTACH` are divided into categories:

| Parameter                            | Type       | Default              | Description                                                                                                                                                                            |
| ------------------------------------ | ---------- | -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ENDPOINT`                           | `VARCHAR`  | `NULL`               | URL endpoint to communicate with the REST Catalog.                                                                                                                                     |
| `DEFAULT_SCHEMA`                     | `VARCHAR`  | `NULL`               | The default schema (namespace) to use for the attached catalog.                                                                                                                        |
| `ACCESS_DELEGATION_MODE`             | `VARCHAR`  | `vended_credentials` | Access delegation mode. Allowed values are `vended_credentials` and `none`.                                                                                                            |
| `SUPPORT_NESTED_NAMESPACES`          | `BOOLEAN`  | `false`              | Set to `true` for catalogs that support nested namespaces.                                                                                                                             |
| `STAGE_CREATE_TABLES`                | `BOOLEAN`  | `true`               | Controls whether DuckDB uses staged `CREATE TABLE`. Disable for catalogs that do not support staged table creation.                                                                    |
| `DISABLE_MULTI_TABLE_COMMIT`         | `BOOLEAN`  | `false`              | Disables the multi-table transactions/commit endpoint. Enable for catalogs that reject this endpoint.                                                                                  |
| `SKIP_CREATE_TABLE_METADATA_UPDATES` | `BOOLEAN`  | `false`              | Skips follow-up metadata updates after non-staged `CREATE TABLE`. Enable for catalogs that fully initialize metadata during table creation and reject subsequent updates.              |
| `REMOVE_FILES_ON_DELETE`             | `BOOLEAN`  | `true`               | Controls whether DuckDB removes storage files when a table is dropped.                                                                                                                 |
| `PURGE_REQUESTED`                    | `BOOLEAN`  | `false`              | Sends the [PurgeRequested](https://github.com/apache/iceberg/blob/4b4eb38cf6dda7b43faeb40eb00aa5db424d2ecb/open-api/rest-catalog-open-api.yaml#L1144) parameter when dropping a table. |
| `ENCODE_ENTIRE_PREFIX`               | `BOOLEAN`  | `false`              | URL-encode the entire path prefix when communicating with the catalog.                                                                                                                 |
| `MAX_TABLE_STALENESS`                | `INTERVAL` | `NULL`               | Prevents unnecessary requests to the Iceberg REST Catalog. Accepts human-readable interval strings such as `10 minutes`, `30 seconds`, or `1 year`.                                    |

Some parameters enable others, see the list of associated additional parameters below this table.

| Parameter            | Type      | Default  | Accepted options    | Description                                                                      |
| -------------------- | --------- | -------- | ------------------- | -------------------------------------------------------------------------------- |
| `ENDPOINT_TYPE`      | `VARCHAR` | `NULL`   | `S3_TABLES`, `GLUE` | A common identifier of an Iceberg Catalog type, sets certain default parameters. |
| `AUTHORIZATION_TYPE` | `VARCHAR` | `OAUTH2` | `OAUTH2`, `SIGV4`   | The Authorization layer of the Iceberg Catalog to attach to.                     |

### `Endpoint Type`

For commonly used Iceberg Catalog providers, the `ENDPOINT_TYPE` parameter can be used to set certain parameters to default values. Acting as a shorthand for connecting to these catalogs.

#### `S3 Tables`

The parameters set by using the `S3_TABLES` `ENDPOINT_TYPE` are:

| Parameter                | Value                                                                                                                                  |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------- |
| `AUTHORIZATION_TYPE`     | `SIGV4`                                                                                                                                |
| `SIGV4_REGION`           | The `REGION` section of the [ARN](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html) provided as the `ATTACH` path. |
| `ENDPOINT`               | `⟨REGION⟩.s3tables.amazonaws.com/iceberg`{:.language-sql .highlight}                                                                   |
| `REMOVE_FILES_ON_DELETE` | `false` (unless explicitly set)                                                                                                        |
| `STAGE_CREATE_TABLES`    | `false` (unless explicitly set)                                                                                                        |
| `PURGE_REQUESTED`        | `true` (unless explicitly set)                                                                                                         |

#### `Glue`

When using the `GLUE` `ENDPOINT_TYPE`, the `SECRET` parameter of type `VARCHAR` has to be set to the path of an existing S3/AWS `SECRET`.
The parameters set by using the `GLUE` `ENDPOINT_TYPE` are:

| Parameter                | Value                                                                                                     |
| ------------------------ | --------------------------------------------------------------------------------------------------------- |
| `AUTHORIZATION_TYPE`     | `SIGV4`                                                                                                   |
| `ENDPOINT`               | `⟨REGION⟩.glue.amazonaws.com/iceberg`{:.language-sql .highlight} using the region from the found `SECRET` |
| `REMOVE_FILES_ON_DELETE` | `false` (unless explicitly set)                                                                           |
| `STAGE_CREATE_TABLES`    | `false` (unless explicitly set)                                                                           |
| `PURGE_REQUESTED`        | `true` (unless explicitly set)                                                                            |

### `Authorization`

To configure the Authorization layer for connecting to an Iceberg REST Catalog, you'll need to pass the `AUTHORIZATION_TYPE` parameter.
These are the supported options:

#### `OAUTH2` Authorization Options

The additional parameters that can be provided when the `AUTHORIZATION_TYPE` is set to `OAUTH2` are the following.

| Parameter           | Type      | Default | Description                                                                                                                               |
| ------------------- | --------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `SECRET`            | `VARCHAR` | `NULL`  | The path to a `SECRET` of type `ICEBERG` to get the `CLIENT_ID` and `CLIENT_SECRET` from.                                                 |
| `CLIENT_ID`         | `VARCHAR` | `NULL`  | [`CLIENT_ID`](https://datatracker.ietf.org/doc/html/rfc6749#section-2.2) used in the OAuth2 authorization request.                        |
| `CLIENT_SECRET`     | `VARCHAR` | `NULL`  | [`CLIENT_SECRET`](https://datatracker.ietf.org/doc/html/rfc6749#section-2.3.1) used in the OAuth2 authorization request.                  |
| `OAUTH2_SERVER_URI` | `VARCHAR` | `NULL`  | The endpoint of the OAuth2 server to contact.                                                                                             |
| `OAUTH2_GRANT_TYPE` | `VARCHAR` | `NULL`  | The [grant_type](https://datatracker.ietf.org/doc/html/rfc6749#appendix-A.10) to use.                                                     |
| `OAUTH2_SCOPE`      | `VARCHAR` | `NULL`  | The [scope](https://datatracker.ietf.org/doc/html/rfc6749#section-3.3) to use.                                                            |
| `DEFAULT_REGION`    | `VARCHAR` | `NULL`  | The region to add to vended credentials if none is provided by the Catalog.                                                               |
| `TOKEN`             | `VARCHAR` | `NULL`  | The [Bearer Token](https://datatracker.ietf.org/doc/html/rfc6750) to use instead of making a request to the server. (disables refreshing) |

#### `SIGV4` Authorization Options

The additional parameters that can be provided when the `AUTHORIZATION_TYPE` is set to `SIGV4` are the following.

| Parameter            | Type                    | Default | Description                                                                                    |
| -------------------- | ----------------------- | ------- | ---------------------------------------------------------------------------------------------- |
| `SECRET`             | `VARCHAR`               | `NULL`  | The `S3` or `AWS` `SECRET` to use for signing.                                                 |
| `SIGV4_SERVICE`      | `VARCHAR`               | `NULL`  | Override the `SERVICE` for signing requests, otherwise inferred from the `ENDPOINT` parameter. |
| `SIGV4_REGION`       | `VARCHAR`               | `NULL`  | Override the `REGION` for signing requests, otherwise inferred from the `ENDPOINT` parameter.  |
| `EXTRA_HTTP_HEADERS` | `MAP(VARCHAR, VARCHAR)` | `NULL`  | Extra headers (key-value) sent along with the signing request.                                 |

## Working with an Attached Catalog

Once a catalog is attached, you can run the full set of read and write operations against its tables:

* **Reading and metadata**: `SELECT`, time travel with the `AT` clause, and the `iceberg_metadata`, `iceberg_snapshots`, and statistics functions. See the [Functions and Settings Reference]({% link docs/current/core_extensions/iceberg/reference.md %}).
* **Writing**: `CREATE`/`DROP SCHEMA` and `TABLE`, partitioning, `INSERT`, `UPDATE`, `DELETE`, `MERGE INTO`, `ALTER TABLE`, table properties, and `COPY FROM DATABASE`. See [Writing to Iceberg]({% link docs/current/core_extensions/iceberg/writing.md %}).

Metadata functions accept a fully qualified table name, e.g.:

```sql
SELECT * FROM iceberg_snapshots(my_catalog.default.t);
```

## Secret Options

The following options can only be passed to a `CREATE SECRET` statement and they require `AUTHORIZATION_TYPE` to be `OAUTH2`:

| Parameter           | Type      | Default | Description                                          |
| ------------------- | --------- | ------- | ---------------------------------------------------- |
| `OAUTH2_GRANT_TYPE` | `VARCHAR` | `NULL`  | Grant Type when requesting an OAuth Token.           |
| `OAUTH2_SCOPE`      | `VARCHAR` | `NULL`  | Requested scope for the returned OAuth Access Token. |

## Settings

| Setting                          | Type      | Default | Description                                                                                      |
| -------------------------------- | --------- | ------- | ------------------------------------------------------------------------------------------------ |
| `unsafe_enable_version_guessing` | `BOOLEAN` | `false` | Allows the extension to guess the latest metadata version when no version or hint file is given. |


## Scan Options

The following parameters can be passed to `iceberg_scan` and `iceberg_metadata`:

| Parameter                    | Type        | Default                                    | Description                                                |
| ---------------------------- | ----------- | ------------------------------------------ | ---------------------------------------------------------- |
| `allow_moved_paths`          | `BOOLEAN`   | `false`                                    | Allows scanning Iceberg tables that are moved              |
| `metadata_compression_codec` | `VARCHAR`   | `''`                                       | Treats metadata files as when set to `'gzip'`              |
| `snapshot_from_id`           | `UBIGINT`   | `NULL`                                     | Access snapshot with a specific `id`                       |
| `snapshot_from_timestamp`    | `TIMESTAMP` | `NULL`                                     | Access snapshot with a specific `timestamp`                |
| `version`                    | `VARCHAR`   | `'?'`                                      | Provides an explicit version string, hint file or guessing |
| `version_name_format`        | `VARCHAR`   | `'v%s%s.metadata.json,%s%s.metadata.json'` | Controls how versions are converted to metadata file names |

> `iceberg_snapshots` does not take `allow_moved_paths`, `snapshot_from_id` or `snapshot_from_timestamp` as parameters.


## Selecting Metadata Versions

By default, the `iceberg` extension will look for a `version-hint.text` file to identify the proper metadata version to use. This can be overridden by explicitly supplying a version number via the `version` parameter to the functions of the `iceberg` extension:

```sql
SELECT *
FROM iceberg_snapshots(
    'data/iceberg/lineitem_iceberg',
    version = '1'
);
```

By default, `iceberg` functions will look for both `v{version}.metadata.json` and `{version}.metadata.json` files, or `v{version}.gz.metadata.json` and `{version}.gz.metadata.json` when `metadata_compression_codec = 'gzip'` is specified.
Other compression codecs are not supported.

If any text file is provided through the `version` parameter, it is opened and treated as a version hint file:

```sql
SELECT *
FROM iceberg_snapshots(
    'data/iceberg/lineitem_iceberg',
    version = 'version-hint.txt'
);
```

The `iceberg` extension will open this file and use the **entire content** of the file as a provided version number.
Note that the entire content of the `version-hint.txt` file will be treated as a literal version name, with no encoding, escaping or trimming. This includes any whitespace, or unsafe characters  which will be explicitly passed formatted into filenames in the logic described below.

## Working with Alternative Metadata Naming Conventions

The `iceberg` extension can handle different metadata naming conventions by specifying them as a comma-delimited list of format strings via the `version_name_format` parameter. Each format string must contain two `%s` parameters. The first is the location of the version number in the metadata filename and the second is the location of the filename extension specified by the `metadata_compression_codec`. The behavior described above is provided by the default value of `"v%s%s.metadata.gz,%s%smetadata.gz`.
If you had an alternatively named metadata file, e.g., `rev-2.metadata.json.gz`, the table can be read via the follow statement:

```sql
SELECT *
FROM iceberg_snapshots(
    'data/iceberg/alternative_metadata_gz_naming',
    version = '2',
    version_name_format = 'rev-%s.metadata.json%s',
    metadata_compression_codec = 'gzip'
);
```

## “Guessing” Metadata Versions

By default, either a table version number or a `version-hint.text` **must** be provided for the `iceberg` extension to read a table. This is typically provided by an external data catalog. In the event neither is present, the `iceberg` extension can attempt to guess the latest version by passing `?` as the `version` parameter:

```sql
SELECT count(*)
FROM iceberg_scan(
    'data/iceberg/lineitem_iceberg_no_hint',
    version = '?',
    allow_moved_paths = true
);
```

The “latest” version is assumed to be the filename that is lexicographically largest when sorting the filenames. Collations are not considered. This behavior is not enabled by default as it may potentially violate ACID constraints. It can be enabled by setting `unsafe_enable_version_guessing` to `true`. When this is set, `iceberg` functions will attempt to guess the latest version by default before failing.

```sql
SET unsafe_enable_version_guessing = true;
SELECT count(*)
FROM iceberg_scan(
    'data/iceberg/lineitem_iceberg_no_hint',
    allow_moved_paths = true
);
```
