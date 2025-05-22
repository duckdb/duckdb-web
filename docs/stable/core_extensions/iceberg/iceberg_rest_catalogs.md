---
layout: docu
redirect_from: null # maybe redirect from old amazon_s3_tables and amazon_sagemaker_lakehouse docs?
title: Iceberg REST Catalogs
---

The `iceberg` extension supports attaching Iceberg REST Catalogs. Before attaching an Iceberg REST Catalog, you must install the `iceberg` extension by following the instructions located in the [overview]({% link docs/stable/core_extensions/iceberg/overview.md %}).

If you are attaching to an Iceberg REST Catalog managed by Amazon, please see the instructions for attaching to [Amazon S3 tables]({% link docs/stable/core_extensions/iceberg/amazon_s3_tables.md %}) or [Amazon Sagemaker Lakehouse]({% link docs/stable/core_extensions/iceberg/amazon_sagemaker_lakehouse.md %}).

For all other Iceberg REST Catalogs, you can follow the instructions below. Please see the [Examples](#examples) section for questions about specific catalogs.

Most Iceberg REST Catalogs authenticate via OAuth2. You can use the existing DuckDB secret workflow to store login credentials for the OAuth2 service.

```sql
CREATE SECRET iceberg_secret (
    TYPE ICEBERG,
    CLIENT_ID '⟨admin⟩',
    CLIENT_SECRET '⟨password⟩',
    OAUTH2_SERVER_URI '⟨http://irc_host_url.com/v1/oauth/tokens⟩'
);
```

If you already have a Bearer token, you can pass it directly to your `CREATE SECRET` statement

```sql
CREATE SECRET iceberg_secret (
    TYPE ICEBERG,
    TOKEN '⟨bearer_token⟩'
);
```

You can attach the Iceberg catalog with the following [`ATTACH`]({% link docs/stable/sql/statements/attach.md %}) statement.

```sql
ATTACH '⟨warehouse⟩' AS iceberg_catalog (
   TYPE iceberg,
   SECRET iceberg_secret, -- pass a specific secret name to prevent ambiguity
   ENDPOINT ⟨https://rest_endpoint.com⟩
);
```

To see the available tables run
```sql
SHOW ALL TABLES;
```

### ATTACH OPTIONS

A REST Catalog with OAuth2 authorization can also be attached with just an `ATTACH` statement. See the complete list of `ATTACH` options for a REST catalog below. 

 
| Parameter                    | Type       | Default  | Description                                                |
| ---------------------------- | ---------- | -------- | ---------------------------------------------------------- |
| `ENDPOINT_TYPE`              | `VARCHAR`  | `NULL`   | Used for attaching S3Tables or Glue catalogs. Allowed values are 'GLUE' and 'S3_TABLES' |
| `ENDPOINT`                   | `VARCHAR`  | `NULL`   | URL endpoint to communicate with the REST Catalog. Cannot be used in conjunction with `ENDPOINT_TYPE`            |
| `SECRET`                     | `VARCHAR`  | `NULL`   | Name of secret used to communicate with the REST Catalog |
| `CLIENT_ID`                  | `VARCHAR`  | `NULL`   | CLIENT_ID used for Secret                                     |
| `CLIENT_SECRET`              | `VARCHAR`  | `NULL`   | CLIENT_SECRET needed for Secret                               |
| `DEFAULT_REGION`             | `VARCHAR`  | `NULL`   | A Default region to use when communicating with the storage layer |
| `OAUTH2_SERVER_URI`          | `VARCHAR`  | `NULL`   | OAuth2 server url for getting a Bearer Token                  |
| `AUTHORIZATION_TYPE`         | `VARCHAR`  | `OAUTH2` | Pass `SigV4` for Catalogs the require SigV4 authorization |


The following options can only be passed to a `CREATE SECRET` statement, and they require `AUTHORIZATION_TYPE` to be `OAUTH2`

| Parameter                    | Type       | Default  | Description                                                |
| ---------------------------- | ---------- | -------- | ---------------------------------------------------------- |
| `OAUTH2_GRANT_TYPE`          | `VARCHAR`  | `NULL` | Grant Type when requesting an OAuth Token |
| `OAUTH2_SCOPE`               | `VARCHAR`  | `NULL` | Requested scope for the returned OAuth Access Token |

## Specific Catalog Examples 

### R2 Catalog

To attach to an [R2 cloudflare](https://developers.cloudflare.com/r2/data-catalog/) managed catalog follow the attach steps below. 


```sql
CREATE SECRET r2_secret (
    TYPE ICEBERG,
    TOKEN '⟨r2_token⟩'
);

```

You can create a token by following the [create an API token](https://developers.cloudflare.com/r2/data-catalog/get-started/#3-create-an-api-token) steps in getting started.

Then, attach the catalog with the following commands.

```sql
ATTACH '⟨warehouse⟩' AS my_r2_catalog (
    TYPE ICEBERG,
    ENDPOINT '⟨catalog-uri⟩'
);
```

The variables for `warehouse` and `catalog-uri` will be available under the settings of the desired R2 Object Storage Catalog (R2 Object Store > Catalog name > Settings).

### Polaris

To attach to a [Polaris](https://polaris.apache.org) catalog the following commands will work.

```sql
CREATE SECRET polaris_secret (
    TYPE ICEBERG,
    CLIENT_ID '⟨admin⟩',
    CLIENT_SECRET '⟨password⟩',
);
```

```sql
ATTACH 'quickstart_catalog' as polaris_catalog (
    TYPE ICEBERG,
    ENDPOINT '⟨polaris_rest_catalog_endpoint⟩'
);
```


### Lakekeeper

To attach to a [Lakekeeper](https://docs.lakekeeper.io) catalog the following commands will work.

```sql
CREATE SECRET lakekeeper_secret (
    TYPE ICEBERG,
    CLIENT_ID '⟨admin⟩',
    CLIENT_SECRET '⟨password⟩',
    OAUTH2_SCOPE '⟨scope⟩',
    OAUTH2_SERVER_URI '⟨lakekeeper_oauth_url⟩'
);
```

```sql
ATTACH '⟨warehouse⟩' as lakekeeper_catalog (
    TYPE ICEBERG,
    ENDPOINT '⟨lakekeeper_irc_url⟩',
    SECRET lakekeeper_secret
);
```

## Limitations

Reading from Iceberg REST Catalogs backed by remote storage that is not S3 or S3Tables is not yet supported.
