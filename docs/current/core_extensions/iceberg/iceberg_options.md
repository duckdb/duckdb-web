---
layout: docu
title: Iceberg Options
---

This page lists the options of the `iceberg` extension: the parameters accepted by the [Iceberg functions]({% link docs/current/core_extensions/iceberg/iceberg_functions.md %}), the options of the `ATTACH` and `CREATE SECRET` statements used to [connect to a catalog]({% link docs/current/core_extensions/iceberg/catalogs.md %}), and the global settings.

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

## `ATTACH` Options

A REST Catalog with OAuth2 authorization can be attached with just an `ATTACH` statement. See the complete list of `ATTACH` options for a REST Catalog below.

| Parameter                   | Type       | Default              | Description                                                                                                                                                          |
| --------------------------- | ---------- | -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ENDPOINT_TYPE`             | `VARCHAR`  | `NULL`               | Used for attaching S3 Tables or Glue catalogs. Allowed values are `GLUE` and `S3_TABLES`.                                                                            |
| `ENDPOINT`                  | `VARCHAR`  | `NULL`               | URL endpoint to communicate with the REST Catalog. Cannot be used in conjunction with `ENDPOINT_TYPE`.                                                               |
| `SECRET`                    | `VARCHAR`  | `NULL`               | Name of secret used to communicate with the REST Catalog.                                                                                                            |
| `CLIENT_ID`                 | `VARCHAR`  | `NULL`               | `CLIENT_ID` used for Secret.                                                                                                                                         |
| `CLIENT_SECRET`             | `VARCHAR`  | `NULL`               | `CLIENT_SECRET` needed for Secret.                                                                                                                                   |
| `DEFAULT_REGION`            | `VARCHAR`  | `NULL`               | A Default region to use when communicating with the storage layer.                                                                                                   |
| `OAUTH2_SERVER_URI`         | `VARCHAR`  | `NULL`               | OAuth2 server url for getting a Bearer Token.                                                                                                                        |
| `AUTHORIZATION_TYPE`        | `VARCHAR`  | `OAUTH2`             | Pass `SigV4` for Catalogs the require SigV4 authorization, `none` for catalogs that don't need authentication.                                                       |
| `ACCESS_DELEGATION_MODE`    | `VARCHAR`  | `vended_credentials` | Access delegation mode. Allowed values are `vended_credentials` and `none`.                                                                                          |
| `EXTRA_HTTP_HEADERS`        | `MAP`      | `NULL`               | Additional HTTP headers to send with REST Catalog requests.                                                                                                          |
| `SUPPORT_NESTED_NAMESPACES` | `BOOLEAN`  | `true`               | Option for catalogs that support nested namespaces.                                                                                                                  |
| `SUPPORT_STAGE_CREATE`      | `BOOLEAN`  | `false`              | Option for catalogs that do not support stage create.                                                                                                                |
| `MAX_TABLE_STALENESS`       | `INTERVAL` | `NULL`               | Option for preventing unnecessary requests to the Iceberg REST Catalog. You can pass human readable interval strings. `10 minutes`, `30 seconds`, `1 year` all work. |
| `PURGE_REQUESTED`           | `BOOLEAN`  | `true`               | Option to send the [PurgeRequested](https://github.com/apache/iceberg/blob/4b4eb38cf6dda7b43faeb40eb00aa5db424d2ecb/open-api/rest-catalog-open-api.yaml#L1144) parameter when dropping a table. |

## Secret Options

The following options can only be passed to a `CREATE SECRET` statement and they require `AUTHORIZATION_TYPE` to be `OAUTH2`:

| Parameter           | Type      | Default | Description                                          |
| ------------------- | --------- | ------- | ---------------------------------------------------- |
| `OAUTH2_GRANT_TYPE` | `VARCHAR` | `NULL`  | Grant Type when requesting an OAuth Token.           |
| `OAUTH2_SCOPE`      | `VARCHAR` | `NULL`  | Requested scope for the returned OAuth Access Token. |

## Settings

| Setting                          | Type      | Default | Description                                                                                     |
| -------------------------------- | --------- | ------- | ----------------------------------------------------------------------------------------------- |
| `unsafe_enable_version_guessing` | `BOOLEAN` | `false` | Allows the extension to guess the latest metadata version when no version or hint file is given. |

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
