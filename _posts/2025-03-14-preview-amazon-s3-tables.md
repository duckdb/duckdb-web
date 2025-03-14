---
layout: post
title: "Preview: Amazon S3 Tables in DuckDB"
author: "Sam Ansmink, Tom Ebergen, Gabor Szarnyas"
thumb: "/images/blog/thumbs/amazon-s3-tables.png"
image: "/images/blog/thumbs/amazon-s3-tables.png"
excerpt: "We are happy to announce a new preview feature that adds support for Apache Iceberg REST Catalogs, enabling DuckDB users to connect to Amazon S3 Tables and Amazon SageMaker Lakehouse with ease."
tags: ["extensions"]
---

## Iceberg Ahead!

In recent years, the [Iceberg open table format](https://iceberg.apache.org/) has become increasingly popular. Major data warehouse platforms such as
[Databricks](https://www.databricks.com/company/newsroom/press-releases/databricks-agrees-acquire-tabular-company-founded-original-creators),
[Snowflake](https://docs.snowflake.com/en/release-notes/2024/other/2024-10-18-snowflake-open-catalog-ga),
[Google BigQuery](https://cloud.google.com/blog/products/data-analytics/biglake-support-for-building-apache-iceberg-lakehouses-is-now-ga)
and
[AWS](https://aws.amazon.com/blogs/big-data/read-and-write-s3-iceberg-table-using-aws-glue-iceberg-rest-catalog-from-open-source-apache-spark/)
have all announced or already implemented support for Iceberg tables. These platforms also support Iceberg [catalogs](https://iceberg.apache.org/terms/#catalog), which are responsible for tracking current metadata for a collection of Iceberg tables grouped by namespaces.

DuckDB has supported reading Iceberg tables [since September 2023]({% post_url 2023-09-26-announcing-duckdb-090 %}) via the [`iceberg` extension]({% link docs/stable/extensions/iceberg/overview.md %}). Today, we are happy to introduce a new preview feature in this extension, which allows attaching to [Iceberg REST catalogs](https://www.tabular.io/apache-iceberg-cookbook/getting-started-catalog-background/). This preview release coincides with two AWS announcements yesterday: [support for Iceberg tables in Amazon S3 Tables](https://aws.amazon.com/about-aws/whats-new/2025/03/amazon-s3-tables-apache-iceberg-rest-catalog-apis/) and the [GA release of the integration between S3 Tables and SageMaker Lakehouse (AWS Glue Data Catalog)](https://aws.amazon.com/about-aws/whats-new/2025/03/amazon-sagemaker-lakehouse-integration-s3-tables-generally-available/). In practice, these developments mean that DuckDB now provides an end-to-end solution for reading Iceberg tables in [S3 Tables]({% link docs/stable/extensions/iceberg/amazon_s3_tables.md %}) and [SageMaker Lakehouse]({% link docs/stable/extensions/iceberg/amazon_sagemaker_lakehouse.md %}).

> DuckDB's support for Iceberg REST Catalog endpoints in Amazon S3 Tables is the result of a collaboration between AWS and DuckDB Labs.

## Using Apache Iceberg REST Catalogs in DuckDB

### Steps for Installing

To connect to Apache Iceberg REST Catalogs in DuckDB,
make sure you are running the **latest stable** DuckDB release (version 1.2.1).
For our example steps, we'll use the DuckDB [CLI client]({% link docs/stable/clients/overview.md %}).
You can obtain this client from the [installation page]({% link docs/installation/index.html %}) and start it with:

```bash
duckdb
```

Next, we need to install the “bleeding edge” versions of the required extensions from the [`core_nightly` repository]({% link docs/stable/extensions/installing_extensions.md %}#extension-repositories).

```sql
FORCE INSTALL aws FROM core_nightly;
FORCE INSTALL httpfs FROM core_nightly;
FORCE INSTALL iceberg FROM core_nightly;
```

> For more information on using the `core_nightly` repository, please see the [notes](#footnotes) at the end of the post.

With these extensions installed, your DuckDB is now capable of using Apache Iceberg REST Catalogs.
Let's find some data.

### Setting up an Amazon S3 Table Bucket

(If you already have Iceberg tables in Amazon S3 Tables, you can skip to the [“Reading Iceberg Catalogs with DuckDB” section](#reading-amazon-s3-tables-with-duckdb).)

In this post, we demonstrate how to read data from Amazon S3 Tables.
To follow along, make sure that your account has [`s3tables` permissions](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-setting-up.html)
and create a new [S3 table bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-buckets.html).
Note that Amazon S3 Tables is currently only supported in [selected AWS regions](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-regions-quotas.html).

### Populating an Amazon S3 Table Bucket

If you don't have an S3 table bucket with tables already, we found the easiest way to get going is to create a table using Amazon Athena.
See their [instructions](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-getting-started.html#s2-tables-tutorial-EMR-cluster).
For our example, we created a simple table with three columns using the Athena query editor:

```sql
CREATE TABLE duck_species (
    id INT,
    english_name STRING,
    latin_name STRING
) TBLPROPERTIES ('table_type' = 'ICEBERG');
```

Let's insert some data to the table:

```sql
INSERT INTO duck_species VALUES
    (0, 'Anas nivis', 'Snow duck');
```

### Reading Amazon S3 Tables with DuckDB

Querying S3 Tables with DuckDB is really easy.
The first step is to get your AWS credentials into DuckDB.
You can achieve this in two ways.
First, you can let DuckDB detect your AWS credentials and configuration based on the default profile in your `~/.aws` directory by creating the following secret using the [Secrets Manager]({% link docs/stable/configuration/secrets_manager.md %}):

```sql
CREATE SECRET (
    TYPE s3,
    PROVIDER credential_chain
);
```

Alternatively, you can set the AWS key, secret, and region values manually:

```sql
CREATE SECRET (
    TYPE s3,
    KEY_ID '⟨YOUR_ACCESS_KEY_ID⟩',
    SECRET '⟨YOUR_SECRET_ACCESS_KEY⟩',
    REGION '⟨YOUR_DEFAULT_REGION⟩'
);
```

> Tip To see the secrets in your session, run `FROM duckdb_secrets();`

Next, point DuckDB to your S3 table bucket.
You can do so by copy-pasting the S3 Tables ARN value directly from the AWS Management Console and using it in the `ATTACH` command:

```sql
ATTACH 'arn:aws:s3tables:us-east-2:111122223333:bucket/my_bucket_name'
    AS s3_tables_db (
        TYPE iceberg,
        ENDPOINT_TYPE s3_tables
    );
```

And that's all! Now, DuckDB is connected to Amazon S3 Tables. 
To show the available tables, run:

```sql
SHOW ALL TABLES;
```

```text
┌──────────────┬─────────┬───────────────┬──────────────┬──────────────┬───────────┐
│   database   │ schema  │     name      │ column_names │ column_types │ temporary │
│   varchar    │ varchar │    varchar    │  varchar[]   │  varchar[]   │  boolean  │
├──────────────┼─────────┼───────────────┼──────────────┼──────────────┼───────────┤
│ s3_tables_db │ ducks   │ duck_species  │ [__]         │ [INTEGER]    │ false     │
└──────────────┴─────────┴───────────────┴──────────────┴──────────────┴───────────┘
```

You can query tables as if they were ordinary DuckDB tables:

```sql
FROM s3_tables_db.ducks.duck_species;
```

```text
┌───────┬──────────────┬────────────┐
│  id   │ english_name │ latin_name │
│ int32 │   varchar    │  varchar   │
├───────┼──────────────┼────────────┤
│   0   │ Anas nivis   │ Snow duck  │
└───────┴──────────────┴────────────┘
```

You also have an alternative option to connect to S3 Tables using the Amazon SageMaker Lakehouse (AWS Glue Data Catalog) Iceberg REST Catalog endpoint.
To do so, run:

```sql
ATTACH '⟨account_id⟩:s3tablescatalog/⟨namespace_name⟩'
AS (
    TYPE iceberg,
    ENDPOINT_TYPE glue
);
```
 
> Tip If you need basic read access to tabular data in a single S3 table bucket, use the `s3_tables` endpoint type.
> If you want a unified view across all of your tabular data in AWS use the `glue` endpoint type.

### Schema Evolution

A key feature of the Iceberg format is [schema evolution](https://iceberg.apache.org/docs/1.7.1/evolution/),
i.e., the ability to follow changes in the table's schema.
To demonstrate this, we go back to the Athena query editor and add a new column to the `duck_species` table:

```sql
ALTER TABLE duck_species
    ADD COLUMNS (conservation_status STRING);
```

Then, we insert a few more duck species:

```sql
INSERT INTO duck_species VALUES
    (1, 'Anas eatoni', 'Eaton''s pintail', 'Vulnerable'),
    (2, 'Histrionicus histrionicus', 'Harlequin duck', 'Least concern');
```

Let's run the query again from DuckDB:

```sql
FROM s3_tables_db.ducks.duck_species;
```

The query now returns a table with the additional fourth column, which has a `NULL` value in the row inserted before the change in the schema
– as expected.

```text
┌───────┬───────────────────────────┬─────────────────┬─────────────────────┐
│  id   │       english_name        │   latin_name    │ conservation_status │
│ int32 │          varchar          │     varchar     │       varchar       │
├───────┼───────────────────────────┼─────────────────┼─────────────────────┤
│     1 │ Anas eatoni               │ Eaton's pintail │ Vulnerable          │
│     2 │ Histrionicus histrionicus │ Harlequin duck  │ Least concern       │
│     0 │ Anas nivis                │ Snow duck       │ NULL                │
└───────┴───────────────────────────┴─────────────────┴─────────────────────┘
```

## Conclusion

The latest preview release of the DuckDB `iceberg` extension enables directly reading tables using Iceberg REST endpoints.
This allows you to query Amazon S3 Tables and Amazon SageMaker Lakehouse (AWS Glue Data Catalog) with ease.
As of today, the extension is in an experimental state and is under active development.
We will publish a stable release later this year.

## Footnotes

### Cleaning Up

If you created a new S3 table bucket to follow the examples,
don't forget to clean up by [deleting your S3 table bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-buckets-delete.html).

### Using the `core_nightly` Repository

The extensions used in this blog post are currently experimental, and hence they are distributed through the [`core_nightly` repository]({% link docs/stable/extensions/installing_extensions.md %}#extension-repositories). If you want to switch back to using extensions from the `core` repository, follow the [extension documentation]({% link docs/stable/extensions/installing_extensions.md %}#force-installing-to-upgrade-extensions).

Note that DuckDB does not support reloading extensions. Therefore, if you experience any issues, try restarting DuckDB after updating the extensions.
