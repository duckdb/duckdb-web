---
layout: post
title: "DuckDB User Survey Analysis"
author: "Gabor Szarnyas"
thumb: "/images/blog/thumbs/survey.svg"
excerpt: "We share the findings from a survey of 500+ DuckDB users."
---

Earlier this year, we conducted a survey in the DuckDB community.
We were mostly curious about the following topics:

1. How do people use DuckDB?
2. Where do people use DuckDB?
3. What do they like about DuckDB?
4. What improvements would they like to see in future releases?

The survey was open for about three weeks. More than 500 people submitted their answers and we raffled 20 t-shirts and hoodies among the participants.

## Summary

We summarize the key findings of the survey below:

* The favorite device to run DuckDB on is laptops but servers are also very popular.
* The most popular clients are the Python API and the standalone CLI client.
* Most users don't have huge data sets but they very much appreciate high performance.
* Users would like to see performance optimizations related to time series and partitioned data.
* DuckDB is popular among data engineers, analysts and scientists but also software engineers.

Let's dive into the details! For the full list of questions in the survey, please scroll down to the [appendix](#appendix).

## Using DuckDB

### Environments

We asked users about the environment where DuckDB is deployed and found that most of them, 87%, run DuckDB on their laptops.
This is in line with the vision that originally drove the creation of DuckDB: creating a system that harnesses the power of hardware available in modern end-user devices.
29% run DuckDB on desktop workstations and 58% run it on servers (see the breakdown later in the [“Server Types” section](#server-types)).

![DuckDB environments](/images/blog/survey/environments.svg)

### Clients

[Unsurprisingly](https://www.tiobe.com/tiobe-index/python/), DuckDB is most often used from Python (73%), followed by the [standalone command-line application]({% link docs/api/cli/overview.md %}) (47%).
The third spot is hotly contested with R, Webassembly (!) and Java all achieving around 14%, followed by Node.js (Javascript) at 9.3%

![DuckDB clients](/images/blog/survey/clients.svg)

The next few places, with 6-7% each, are occupied by ODBC, Rust, and Go.
Finally, Arrow (ADBC) rounds off the top-10 with 5%.

### Operating Systems

We found that most users, 61%, run DuckDB on Linux servers.
These deployments include cloud instances, on-premises installations, and continuous integration (CI) runners.
Windows desktop and macOS have a similar share of users, 41–45%.
A further 8.8% run DuckDB on Windows servers.

![DuckDB platforms](/images/blog/survey/platforms.svg)

We found the number of Linux desktop users quite striking.
While the overall [market share of Linux desktop is around 4.5%](https://gs.statcounter.com/os-market-share/desktop/worldwide/2024),
_29% of respondents indicated that they run DuckDB on Linux desktop!_
We suspect that this is thanks to DuckDB's [popularity among data engineers](#user-roles),
who often use Linux desktop thanks to its customizability and similarity to the Linux server-based deployment environments.

### Server Types

As we discussed in the [“Environments” section](#environments), DuckDB is often run on servers.
But how big are these servers and where are they operated?
Both small servers (less than 16 GB memory) and medium-sized servers (16-512 GB memory) are popular with 56% and 61% of users reporting that they run DuckDB on these.
About 14% of respondents run DuckDB on servers with more than 0.5TB memory.

![Server size](/images/blog/survey/server-sizes.svg)

Regarding _where_ the servers run, on-premises deployments and AWS are neck-and-neck with 27.2%.
They are followed by two other clouds, Microsoft Azure and the Google Cloud Platform.
Finally, about 4% of users run DuckDB on Hetzner servers.

![Server premises](/images/blog/survey/server-premises.svg)

## Data

### Data Formats

We inquired about the data formats used when working with DuckDB.
Parquet is the most popular format by 79% of users reporting to use it. CSV is a close second with 73%.
JSON is also popular (vanilla JSON: 42%, NDJSON: 11%).
About ⅓ reported to use Arrow.

![Data formats](/images/blog/survey/data-formats.svg)

### Dataset Sizes

We asked users about the size of the largest dataset they processed with DuckDB. We defined _dataset size_ as the size of the data when stored in uncompressed CSV format.
For Parquet files and DuckDB database files, we asked users to approximate the CSV size by multiplying their file sizes by 5.

The responses showed that [few users of DuckDB process Big Data](https://motherduck.com/blog/big-data-is-dead/). For ¾ of users, their largest dataset size was less than 100 GB data,
20% of users processed a dataset between 100 GB and 1 TB and approximately 5% of the users ventured into the 1 TB+ territory. About 1% processed 10 TB+ datasets.
These findings are in line with [statistics derived from a recent RedShift usage dataset](https://motherduck.com/blog/redshift-files-hunt-for-big-data/#whos-got-big-data) by [Jordan Tigani of MotherDuck](https://motherduck.com/authors/jordan-tigani/), and the recent analysis of the [Snowflake and RedShift datasets](https://www.fivetran.com/blog/how-do-people-use-snowflake-and-redshift) by [George Fraser of Fivetran](https://www.fivetran.com/people/george-fraser).

![Dataset sizes](/images/blog/survey/dataset_sizes.svg)

While these results obviously are somewhat biased – users who need to crunch through huge datasets may not work with DuckDB (yet!) –, the skew towards smaller datasets is quite significant and shows that many real-world use cases can be tackled using small to medium-sized datasets. The results also show that DuckDB *can* solve many problems on datasets larger than 1 TB.

## Features

### Most Liked Features

We were curious: what do users like most about DuckDB? The plot shows the most frequent responses:
![Most liked DuckDB features](/images/blog/survey/most_liked_features.svg)

The most liked feature, by far, is **high performance**.
Users also enjoy **file format support** (CSV, Parquet, JSON, etc.),
**ease of use**,
**extensive SQL support** (including [friendly SQL]({% link docs/sql/dialect/friendly_sql.md %}))
and **in-memory integrations** such as support for Pandas, Arrow and NumPy.
Finally, users mentioned low memory usage, protocol support (e.g., HTTPS, S3), database integrations, and portability.

### Feature Requests

We asked users about the features that they'd most like to see in future DuckDB versions. The most popular requests are listed in the table below:

| Feature                                                                 | Percentage |
|:------------------------------------------------------------------------|-----------:|
| Improved partitioning and optimizations related to partitioning         | 39%        |
| Improved support for time series and optimizations for pre-sorted data  | 35%        |
| Support for materialized views                                          | 28%        |
| Support for vector search                                               | 24%        |
| Support for attaching to database systems via ODBC                      | 24%        |
| Support for time travel queries (query the database as of a given time) | 23%        |
| Support for the Delta Lake format                                       | 22%        |
| Improved support for Iceberg (including writes)                         | 17%        |

We are happy to report that, since survey was conducted pre-v1.0.0 and DuckDB is now at version 1.1.1, some of these requests are already a reality:

* Reading Delta Lake is now possible via the [`delta` extension]({% post_url 2024-06-10-delta %}).
* Vector search is now supported via the [`vss` extension]({% post_url 2024-05-03-vector-similarity-search-vss %}).

For the rest of the requested features, several ones are in the making at DuckDB Labs. Stay tuned!

## User Roles

We asked respondents to indicate their main roles in their organization. The top-5 answers were as follows:

![User roles](/images/blog/survey/roles.svg)

It's no surprise that DuckDB is popular in the “data” roles: 26.5% of the respondents are data engineers, 14.0% are data scientists and 9.3% are data analysts.
The form had a surprisingly high share of software engineers, 23.4%.
Finally, about 2% of respondents indicated that their primary role is DBA.

## Conclusion

We would like to thank all participants for taking the time to complete the survey.
We will use the answers to guide the future development of DuckDB and we hope that readers of this analysis find it informative as well.

## Appendix

For reference, the questions in the user survey were phrased as follows:

* Which DuckDB client(s) do you use?
    * ADBC (Arrow)
    * C
    * C++
    * C#
    * CLI (command line interface)
    * Go
    * Java (JDBC)
    * Javascript / Node.js
    * Julia
    * ODBC
    * Python
    * R
    * Rust
    * Webassembly (Wasm)
    * Other
* What environment(s) do you run DuckDB on?
    * Laptop
    * Desktop workstation
    * Small server or cloud instance (Less than 16 GB of RAM)
    * Medium-sized server or cloud instance (RAM between 16 GB and 512 GB)
    * Large server or cloud instance (More than 512 GB of RAM)
    * Handheld or wearable device (smartphones, tablets, watches)
    * Single-board computers (e.g., Raspberry Pi)
* Which data format(s) do you use when working with DuckDB?
    * Arrow
    * CSV
    * Iceberg
    * JSON
    * NDJSON
    * Parquet
* What is the largest dataset you processed with DuckDB? The dataset size is defined as the approximate size of the data when serialized in uncompressed CSV format. _If you work with Parquet or DuckDB database files, you can approximate this by multiplying the total file sizes by 5._
    * < 1 GB
    * 1 GB – 10 GB
    * 10 GB – 100 GB
    * 100 GB – 1 TB
    * 1 TB – 10 TB
    * \> 10TB
* If you run DuckDB on servers, where are these servers hosted?
    * On-premises cluster
    * Hetzner
    * Alibaba Cloud
    * Amazon Web Services (AWS)
    * Google Cloud Platform (GCP)
    * Microsoft Azure
* Which platforms do you run DuckDB on?
    * Linux server
    * Linux destop
    * macOS
    * Windows server
    * Windows desktop
* Which DuckDB features are the most important for you? Please select up to 3 items, including the "Other" option.
    * Extensive SQL support
    * High performance
    * Ease of use
    * Low memory usage
    * Portability
    * File format support (CSV, Parquet, JSON, etc.)
    * Protocol support (S3, Azure, etc.)
    * Database integrations (Postgres, SQLite, MySQL, ...)
    * In-memory integrations (Pandas, Arrow, NumPy, Polars, ...)
* What features would you like to see in future DuckDB versions? Please select up to 3 items, including the "Other" option.
    * Improved partitioning and optimizations related to partitioning
    * Improved PySpark API
    * Improved support for time series and optimizations for pre-sorted data
    * Improved support for Iceberg (including writes)
    * Support for the Delta Lake format
    * Support for materialized views
    * Support for vector search
    * Support for attaching to database systems via ODBC
    * Support for time travel queries (query the database as of a given time in the past)
    * Support for triggers
* What other improvements would you like to see in DuckDB?
* Are there any issues you are experiencing with DuckDB?
* What improvements would you like to see in the DuckDB documentation? (optional)
* What other data management tools do you use on a regular basis? (Including database systems, data processing tools, etc.)
    * ClickHouse
    * Dask
    * Databricks
    * dbt
    * dplyr
    * Google BigQuery
    * Microsoft SQL Server
    * MongoDB
    * MySQL / MariaDB
    * Oracle
    * Pandas
    * Polars
    * PostgreSQL
    * Snowflake
    * Spark
    * SQLite
* What is your main role in your organization? (optional)
