---
layout: post
title: "From Spreadsheets to DuckLake: A Data Engineer's Road to DuckDB"
authors:
  - Matt Martin in conversation with Geertjan Wielenga & Tim Cox
thumb: "/images/blog/thumbs/ducklake.svg"
image: "/images/blog/thumbs/ducklake.png"
excerpt: "TL;DR: After nearly two decades working with increasingly sophisticated data infrastructure, data engineer [Matt Martin](https://www.linkedin.com/in/mattmartin14/) discovered DuckDB could handle many of the analytical tasks he cared about without the operational complexity he had come to associate with big data. The same preference for familiar SQL and simpler infrastructure drew him to DuckLake, and he has since become an active tester and advocate of DuckDB's evolving capabilities."
tag: using-duckdb
---

## From Copy-Paste to Code

Matt's career started in 2008 the way many data careers do: with spreadsheets. As a fresh graduate, he spent his days copying and pasting between Excel, Microsoft Access and SQL Server. Assembling a single report could take three hours, and one mistake meant starting over.

**“There's got to be an easier way,”** he remembers thinking. His dad taught him how to write VBA macros, and that was the first step. Next, he got access to the SQL Server and Oracle databases behind those spreadsheets and started querying the source directly instead of other people's workbooks. Macros turned into scheduled stored procedures, and stored procedures turned into automated pipelines. 

When he started, the team published its 20 to 30 daily reports by 10 AM. By the time he had automated the process, the reports were out by 6 AM, before anyone had touched anything.

## Teradata, BigQuery and the Spark Years

From there, Matt moved into big data. Teradata gave him his first taste of massively parallel processing, along with lessons about data skew and distributing work evenly across nodes. Around 2016, at The Home Depot, he moved to Google BigQuery. BigQuery did not support stored procedures at the time, so Matt picked up Python, then pandas and eventually Apache Spark.

Spark was powerful, but it was also heavy. Even local testing meant aligning JVM and Spark versions, deciphering stack traces that ran for hundreds of lines and waiting three to five minutes for the cluster to warm up before processing a few hundred files. **“A lot of battle scars,”** as Matt puts it.

He is also skeptical that most teams need that machinery. Outside a handful of domains such as aerospace, fraud detection and high-frequency trading, he rarely sees workloads that truly need to churn through petabytes at speed. More often, it is the classic meme: someone insists on real-time data, and it turns out to be for a monthly report.

## Meeting DuckDB

Matt first came across DuckDB around 2022. At first, he was not sure what to make of it: it was not pandas, not Spark and not SQLite, yet it promised SQL for transforming data. Then he installed it and read a CSV file with two lines of code:

```python
import duckdb
duckdb.sql("FROM 'sales.csv'").show()
```

**“There actually is something out there that's easy to use and doesn't require a bunch of infrastructure overhead,”** he says. No JVM, no knobs to turn. From local files, he moved on to files on Amazon S3, over the [`s3://`]({% link docs/current/core_extensions/httpfs/s3api.md %}) protocol:

```sql
CREATE SECRET (TYPE s3, PROVIDER credential_chain);

SELECT count(*) AS num_rows
FROM 's3://⟨bucket⟩/exports/*.parquet';
```

And from there, to mixing CSV, Parquet and Iceberg tables in a single query:

```sql
INSTALL iceberg;
LOAD iceberg;

SELECT
    o.order_id,
    c.customer_name,
    p.product_name
FROM iceberg_scan('s3://⟨bucket⟩/warehouse/orders') AS o
JOIN 's3://⟨bucket⟩/customers.parquet' AS c
    ON o.customer_id = c.customer_id
JOIN 'products.csv' AS p
    ON o.product_id = p.product_id;
```

Two things made DuckDB a natural fit. First, simplicity: after nearly two decades in data engineering, Matt values a frictionless experience above almost anything else, as long as the SLAs are met. Second, SQL: after 15 years of writing advanced SQL, he found that DuckDB supported practically all of the syntax he already knew.

He also uses DuckDB for his personal finances, analyzing CSV exports of his bank transactions locally, the kind of query that takes a minute to write:

```sql
SELECT
    date_trunc('month', transaction_date) AS month,
    category,
    sum(amount) AS total
FROM 'transactions_*.csv'
GROUP BY ALL
ORDER BY month, total;
```

He is experimenting with LLM-based assistants for this, but likes knowing that he does not depend on them: **“If LLMs ever become too expensive, I could easily pick right back up with DuckDB and write it myself. It's like riding a bike at this point.”**

## Why DuckLake

As open table formats took off, Matt worked extensively with Apache Iceberg and Delta Lake. Both are good at managing large datasets and their version history. The trouble starts when the metadata grows. Iceberg writes several metadata files per transaction, including metadata JSON, manifest lists and manifests. Over time, a query that used to plan in seconds can slow down significantly because thousands of metadata files need to be resolved first.

[DuckLake](https://ducklake.select/) takes a different approach: it stores all metadata in a SQL database. **“Organizations have been doing SQL for over four decades and have gotten very, very good at optimizing queries,”** Matt says. In his experience, catalog operations that take seconds with Iceberg resolve in under a millisecond with DuckLake, because they are queries against indexed tables. 

What Matt likes most is how little setup it takes: standing up an Iceberg lakehouse involves a lot of tooling, while a DuckLake on object storage takes two statements, one to create a secret for the bucket and one to attach the lake:

```sql
CREATE SECRET (TYPE s3, PROVIDER credential_chain);

ATTACH 'ducklake:⟨metadata.ducklake⟩' AS my_lake (
    DATA_PATH 's3://⟨bucket⟩/⟨prefix⟩/'
);
```

If the DuckLake does not exist yet, DuckDB creates it and you can start creating tables right away. Matt has also written about [streaming events straight into a DuckLake](https://performancede.substack.com/p/streaming-events-to-ducklake).

The same simplicity applies to existing Iceberg catalogs. Matt has [written on his Substack](https://performancede.substack.com/) about the Spark configuration of 20-plus lines he once needed to query an Iceberg table in AWS Glue, just to get the right JARs and the right AWS settings. With DuckDB's [Iceberg extension]({% link docs/current/core_extensions/iceberg/overview.md %}), it takes three statements:

```sql
INSTALL iceberg;
LOAD iceberg;

ATTACH '⟨aws_account_id⟩' AS glue_catalog (
    TYPE iceberg,
    ENDPOINT_TYPE glue
);
```

## Looking Forward to DuckDB v2.0

Matt has been testing the DuckDB v2.0 alpha and has not run into any regressions so far. Several features stand out for him.

**Dynamic `ATTACH` statements.** While writing the book, Matt needed to attach AWS Glue catalogs in examples. Up to v1.5, the `ATTACH` path had to be a literal, so the account number had to be hard-coded in the script, as calling `getenv` raised an error. 

Matt filed a feature request, and a pull request followed within two days. In v2.0, `ATTACH` accepts expressions, so account IDs, usernames, passwords and connection strings can come from environment variables at runtime instead of living in the script:

```sql
ATTACH getenv('AWS_ACCOUNT_ID') AS glue_catalog (
    TYPE iceberg,
    ENDPOINT_TYPE glue
);
```

**Asynchronous I/O.** This is the feature Matt calls a game changer. In his [benchmarks, published on his Substack](https://performancede.substack.com/p/duckdb-20-and-s3-file-read-performance), reading 1,000 and 10,000 files from Amazon S3 consistently took 67% to 70% less time with the v2.0 alpha. 

Much of the time used to go into sequential requests to list and fetch files. In v2.0, DuckDB issues these in the background. No code changes are needed: a query like the following simply runs faster on v2.0.

```sql
SELECT count(*) AS num_events
FROM read_json('s3://⟨bucket⟩/logs/*.json');
```

For workloads such as log analytics over large numbers of raw files in S3, Google Cloud Storage or Azure, where teams would traditionally spin up a wide Spark cluster, a single DuckDB process can now keep up, with less overhead and lower cost.

**Quack.** The [Quack remote protocol]({% link docs/current/quack/overview.md %}) turns a DuckDB instance into a server that other DuckDB instances can connect to over HTTP. Matt likes the cleaner connect and disconnect syntax in v2.0 and the official DuckLake support. 

He has written about [serving a DuckLake on an Amazon EC2 instance via Quack](https://performancede.substack.com/p/serving-a-ducklake-on-ec2-via-quack). End users only need the Quack address and a token, with no AWS credentials and no knowledge of the DuckLake behind it. He has also built a DuckDB-Wasm dashboard on top of this setup, which he covers in the DuckLake book he is writing. The Wasm build is still on v1.5 and will be updated for the v2.0 release.

## Conclusion

Matt's journey does not suggest that distributed systems are unnecessary. It illustrates a different engineering principle: start with the requirements of the workload, and introduce additional infrastructure only when those requirements justify it. For Matt, DuckDB and DuckLake demonstrate how much analytical capability can be delivered without making the underlying system unnecessarily complicated.

We would like to thank Matt for the conversation. You can follow his writing on DuckDB and DuckLake on [his Substack](https://performancede.substack.com/). And if you are reading this, are using DuckDB, and would like to share your story, drop us a line at [quack@duckdb.org](mailto:quack@duckdb.org).
