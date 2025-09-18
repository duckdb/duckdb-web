---
layout: docu
redirect_from:
- /docs/stable/extensions/iceberg/troubleshooting
- /docs/stable/extensions/iceberg/troubleshooting/
title: Troubleshooting
---

## Limitations

* Writing Iceberg tables is currently not supported.
* Reading tables with deletes is not yet supported.

## Curl Request Fails

### Problem

When trying to attach to an Iceberg REST Catalog endpoint, DuckDB returns the following error:

```console
IO Error:
Curl Request to '/v1/oauth/tokens' failed with error: 'URL using bad/illegal format or missing URL'
```

### Solution

Make sure that you have the latest Iceberg extension installed:

```batch
duckdb
```

```plsql
FORCE INSTALL iceberg FROM core_nightly;
```

Exit DuckDB and start a new session:

```batch
duckdb
```

```plsql
LOAD iceberg;
```

## HTTP Error 403

### Problem

When trying to list the tables in a remote-attached catalog, DuckDB returns the following error:

```sql
SHOW ALL TABLES;
```

```console
Failed to query https://s3tables.us-east-2.amazonaws.com/iceberg/v1/arn:aws:s3tables:... http error 403 thrown.
Message: {"message":"The security token included in the request is invalid."}
```

### Solution

Use the `duckdb_secrets()` function to check whether DuckDB loaded the required credentials:

```sql
.mode line
FROM duckdb_secrets();
```

If you do not see your credentials, set them manually using the following secret:

```sql
CREATE SECRET (
    TYPE s3,
    KEY_ID '⟨AKIAIOSFODNN7EXAMPLE⟩',
    SECRET '⟨wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY⟩',
    REGION '⟨us-east-1⟩'
);
```
