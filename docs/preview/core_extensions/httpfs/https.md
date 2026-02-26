---
layout: docu
title: HTTP(S) Support
---

With the `httpfs` extension, it is possible to directly query files over the HTTP(S) protocol. This works for all files supported by DuckDB or its various extensions, and provides read-only access.

```sql
SELECT *
FROM 'https://domain.tld/file.extension';
```

## Partial Reading

For CSV files, files will be downloaded entirely in most cases, due to the row-based nature of the format.
For Parquet files, DuckDB supports [partial reading]({% link docs/preview/data/parquet/overview.md %}#partial-reading), i.e., it can use a combination of the Parquet metadata and [HTTP range requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests) to only download the parts of the file that are actually required by the query. For example, the following query will only read the Parquet metadata and the data for the `column_a` column:

```sql
SELECT column_a
FROM 'https://domain.tld/file.parquet';
```

In some cases, no actual data needs to be read at all as they only require reading the metadata:

```sql
SELECT count(*)
FROM 'https://domain.tld/file.parquet';
```

## Scanning Multiple Files

Scanning multiple files over HTTP(S) is also supported:

```sql
SELECT *
FROM read_parquet([
    'https://domain.tld/file1.parquet',
    'https://domain.tld/file2.parquet'
]);
```

## Authenticating

To authenticate for an HTTP(S) endpoint, create an `HTTP` secret using the [Secrets Manager]({% link docs/preview/configuration/secrets_manager.md %}):

```sql
CREATE SECRET http_auth (
    TYPE http,
    BEARER_TOKEN '⟨token⟩'
);
```

Or:

```sql
CREATE SECRET http_auth (
    TYPE http,
    EXTRA_HTTP_HEADERS MAP {
        'Authorization': 'Bearer ⟨token⟩'
    }
);
```

## HTTP Proxy

DuckDB supports HTTP proxies.

You can add an HTTP proxy using the [Secrets Manager]({% link docs/preview/configuration/secrets_manager.md %}):

```sql
CREATE SECRET http_proxy (
    TYPE http,
    HTTP_PROXY '⟨http_proxy_url⟩',
    HTTP_PROXY_USERNAME '⟨username⟩',
    HTTP_PROXY_PASSWORD '⟨password⟩'
);
```

You can also set the scope for an HTTP proxy using the `SCOPE` keyword.

```sql
CREATE SECRET http_proxy (
    TYPE HTTP, 
    SCOPE ['⟨https://duckdb.org⟩', '⟨https://some-other-website.org⟩'], 
    HTTP_PROXY '⟨http_proxy_url⟩',
    HTTP_PROXY_USERNAME '⟨username⟩',
    HTTP_PROXY_PASSWORD '⟨password⟩'
);
```

Alternatively, you can add it via [configuration options]({% link docs/preview/configuration/pragmas.md %}):

```sql
SET http_proxy = '⟨http_proxy_url⟩';
SET http_proxy_username = '⟨username⟩';
SET http_proxy_password = '⟨password⟩';
```

Note: You cannot set a proxy scope using the configurations options.

## Using a Custom Certificate File

To use the `httpfs` extension with a custom certificate file, set the following [configuration options]({% link docs/preview/configuration/pragmas.md %}) prior to loading the extension:

```sql
LOAD httpfs;
SET ca_cert_file = '⟨certificate_file⟩';
SET enable_server_cert_verification = true;
```

If you would like to disable SSL verification for all HTTP requests using an HTTP secret you can do so with the following statement:

```sql
CREATE SECRET disable_ssl (
    TYPE HTTP, 
    VERIFY_SSL 0
);
```

To enable it again for one specific endpoint, you can take advantage of the scope parameter:

```sql
CREATE SECRET enable_ssl_for_your_website (
    TYPE HTTP, 
    SCOPE 'https://⟨your-website.com⟩', 
    VERIFY_SSL 1
); 
```
