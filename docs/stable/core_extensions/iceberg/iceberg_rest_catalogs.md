---
layout: docu
redirect_from: null # maybe redirect from old amazon_s3_tables and amazon_sagemaker_lakehouse docs?
title: Iceberg Rest Catalogs
---

The `iceberg` extension supports attaching Iceberg Rest Catalogs. Before attaching an Iceberg Rest Catalog, you must install the `iceberg` extension by following the instructions located in the [overview]({% link docs/stable/core_extensions/iceberg/overview.md %}).

If you are attaching to an Iceberg Rest Catalog managed by Amazon, please see the instructions for attaching to [Amazon S3 tables]({% link docs/stable/core_extensions/iceberg/amazon_s3_tables.md %}) or [Amazon Sagemaker Lakehouse]({% link docs/stable/core_extensions/iceberg/amazon_sagemaker_lakehouse.md %}).

For all other Iceberg Rest Catalogs, you can follow the instructions below. Please see the [Examples](#examples) section for questionsabout specific catalogs.

Most Iceberg Rest Catalogs authenticate via Oauth2. You can use the existing DuckDB secret workflow to create the oauth secret.

```sql
CREATE SECRET iceberg_secret (
    TYPE ICEBERG,
    CLIENT_ID '⟨admin⟩',
    CLIENT_SECRET '⟨password⟩',
    OAUTH2_SERVER_URI '⟨http://irc_host_url.com/v1/oauth/tokens⟩'
);
```

If you already have a token, you can pass it directly to your `CREATE SECRET` statement

```sql
CREATE SECRET iceberg_secret (
    TYPE ICEBERG,
    TOKEN '⟨one_time_token⟩'
);
```

You can attach the iceberg catalog with the following `Attach` statement.

```sql
ATTACH '⟨warehouse-name⟩' AS iceberg_catalog (
   TYPE iceberg,
   SECRET iceberg_secret, -- pass a specific secret name to prevent ambiguity
   ENDPOINT rest-catalog-endpoint⟩
);
```

To see the available tables run
```sql
SHOW ALL TABLES;
```

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
ATTACH '⟨warehouse-name⟩' AS my_r2_catalog (
    TYPE ICEBERG,
    ENDPOINT '⟨catalog-uri⟩'
);
```

The variables for `warehouse-name` and `catalog-uri` will be available under the settings of the desired R2 Object Storage Catalog (R2 Object Store > Catalog name > Settings).

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

Reading from Iceberg Rest Catalogs backed by remote storage that is not S3 or S3Tables is not yet supported.