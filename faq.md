---
layout: default
title: Frequently Asked Questions
body_class: faq
toc: false
---

<!-- ################################################################################# -->
<!-- ################################################################################# -->
<!-- ################################################################################# -->

<div class="wrap pagetitle">
  <h1>Frequently Asked Questions</h1>
</div>

## Overview

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### Who makes DuckDB?

<div class="answer" markdown="1">

DuckDB was created by [Dr. Mark Raasveldt](https://mytherin.github.io) & [Dr. Hannes Mühleisen](https://hannes.muehleisen.org) at the [Centrum Wiskunde & Informatica (CWI)](https://www.cwi.nl) in Amsterdam, the Netherlands. Mark and Hannes have set up the [DuckDB Foundation](https://duckdb.org/foundation/) that collects donations and funds development and maintenance of DuckDB. Mark and Hannes are also co-founders of [DuckDB Labs](https://www.duckdblabs.com), which provides commercial services around DuckDB, and employs several core contributors of DuckDB.

</div>

</div>

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### Why call it DuckDB?

<div class="answer" markdown="1">

Ducks are amazing animals. They can fly, walk and swim. They can also live off pretty much everything. They are quite resilient to environmental challenges. A duck's song will bring people back from the dead and [inspires database research](/images/wilbur.jpg). They are thus the perfect mascot for a versatile and resilient data management system.

</div>

</div>

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### Is DuckDB open-source?

<div class="answer" markdown="1">

DuckDB is fully open-source under the MIT license and its development takes place [on GitHub in the `duckdb/duckdb` repository](https://github.com/duckdb/duckdb).
All components of DuckDB are available in the free version under this license: there is no “enterprise version” of DuckDB.

Most of the intellectual property of DuckDB has been purposefully moved to a non-profit entity to disconnect the licensing of the project from the commercial company, DuckDB Labs.
The DuckDB Foundation's [statutes]({% link pdf/deed-of-incorporation-stichting-duckdb-foundation.pdf %}) also ensure DuckDB remains open-source under the MIT license in perpetuity.
The [CWI (Centrum Wiskunde & Informatica)](https://cwi.nl/) has a seat on the board of the DuckDB Foundation
and donations to the DuckDB Foundation directly fund DuckDB development.

For more information on the organizations around DuckDB, see the next question–answer pair.

</div>

</div>

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### How are DuckDB, the DuckDB Foundation, DuckDB Labs, and MotherDuck related?

<div class="answer" markdown="1">

[**DuckDB**](https://duckdb.org/) is the name of the MIT licensed open-source project.

The [**DuckDB Foundation**]({% link foundation/index.html %}) is a non-profit organization that holds the intellectual property of the DuckDB project.
The DuckDB Foundation's [statutes]({% link pdf/deed-of-incorporation-stichting-duckdb-foundation.pdf %}) ensure DuckDB remains open-source under the MIT license in perpetuity.

[**DuckDB Labs**](https://duckdblabs.com/) is a company based in Amsterdam that provides commercial support services for DuckDB.
DuckDB Labs employs the core contributors of the DuckDB project.

[**MotherDuck**](https://motherduck.com/) is a venture-backed company creating a hybrid cloud/local platform using DuckDB.
MotherDuck contracts with DuckDB Labs for development services, and DuckDB Labs owns a portion of MotherDuck.
[See the partnership announcement for details](https://duckdblabs.com/news/2022/11/15/motherduck-partnership).
To learn more about MotherDuck, see the [CIDR 2024 paper on MotherDuck](https://www.cidrdb.org/cidr2024/papers/p46-atwal.pdf) and the [MotherDuck documentation](https://motherduck.com/docs).

</div>

</div>

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### Where do I find the DuckDB logo and design guidelines?

<div class="answer" markdown="1">

Please head to the [Design & Brand Assets page]({% link design/index.html %}).

</div>

</div>

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### Where do I find DuckDB trademark use guidelines?

<div class="answer" markdown="1">

Please consult the [trademark guidelines for DuckDB™]({% link trademark_guidelines.md %}).

</div>

</div>

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### I found a project with “duck” in its name. Is it officially affiliated with DuckDB?

<div class="answer" markdown="1">

The following projects are officially affiliated with DuckDB:

* the [DuckDB project](https://github.com/duckdb/duckdb)
* all primary [client libraries]({% link docs/stable/clients/overview.md %})
* all [core DuckDB extensions]({% link docs/stable/core_extensions/overview.md %})
* the [DuckDB UI](https://github.com/duckdb/duckdb-ui)
* [MotherDuck](https://motherduck.com)
* [`dbt-duckdb`](https://github.com/duckdb/dbt-duckdb)
* [`pg_duckdb`](https://github.com/duckdb/pg_duckdb)

Other projects are likely _not affiliated_ with the DuckDB project. Please check their websites, READMEs and licenses for more details.

</div>

</div>

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### What is the official name of the project?

<div class="answer" markdown="1">

In official communication, we refer to DuckDB exclusively as “DuckDB” and avoid other names and spellings such as “DDB”, “the Duck” and “DuckDb”.
Of course, the alternatives are also widely understood and you are welcome to use them, but using “DuckDB” is preferred.

</div>

</div>

<!-- ################################################################################# -->
<!-- ################################################################################# -->
<!-- ################################################################################# -->

## Working with DuckDB

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### Can DuckDB save data to disk?

<div class="answer" markdown="1">

DuckDB supports [persistent storage]({% link docs/stable/connect/overview.md %}#persistent-database) and stores the database as a single file, which includes all tables, views, indexes, macros, etc. present in the database.
DuckDB's [storage format]({% link docs/stable/internals/storage.md %}) uses a compressed columnar representation, which is compact but allows for efficient bulk updates.
DuckDB can also run in [in-memory mode]({% link docs/stable/connect/overview.md %}#in-memory-database), where no data is persisted to disk.
DuckDB can also save data in [DuckLake format](http://ducklake.select/) through the [`ducklake` extension]({% link docs/stable/core_extensions/ducklake.md %}).

</div>

</div>

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### What type of storage should I run DuckDB on (e.g., local disks, network-attached storage)?

<div class="answer" markdown="1">

The type of storage used to run DuckDB has a [significant performance impact]({% link docs/stable/guides/performance/environment.md %}#disk).
In general, using SSDs (SATA or NVMe SSDs) leads to superior performance compared to HDDs.

The location of the storage varies greatly depending the workload:

* _For read-only workloads,_ the DuckDB database can be stored on local disks and remote endpoints such as [HTTPS]({% link docs/stable/core_extensions/httpfs/https.md %}) and cloud object storage such as [AWS S3]({% link docs/stable/core_extensions/httpfs/s3api.md %}) and similar providers.
* _For read-write workloads,_ storing the database on instance-attached storage yields the best performance.
Network-attached cloud storage such as [AWS EBS](https://aws.amazon.com/ebs/) also works and its performance can be fine-tuned with the guaranteed IOPS settings.
Based on our experience, we **strongly advise against running DuckDB – or any other database management system – for read-write workloads on [network-attached storage (NAS)](https://en.wikipedia.org/wiki/Network-attached_storage).**
These setups are often slow and result in spurious failures that are difficult to troubleshoot.

</div>

</div>

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### Is DuckDB an in-memory database?

<div class="answer" markdown="1">

It is a common misconception that DuckDB is an in-memory database.
While DuckDB _can_ work in-memory, it is **not an in-memory database**.
DuckDB can make use of available memory for caching, it also fully supports disk-based persistence and [offloading larger-than-memory operations]({% link docs/stable/guides/performance/how_to_tune_workloads.md %}#larger-than-memory-workloads-out-of-core-processing) to disk.

</div>

</div>

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### Is DuckDB built on Arrow?

<div class="answer" markdown="1">

DuckDB does not use the [Apache Arrow format](https://arrow.apache.org/) internally.
However, DuckDB supports reading from and writing to Arrow using the [`arrow` community extension]({% link community_extensions/extensions/arrow.md %}).
It can also run SQL queries directly on Arrow using [`pyarrow`]({% link docs/stable/guides/python/sql_on_arrow.md %}).

</div>

</div>

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### Are DuckDB's database files portable between different DuckDB versions and clients?

<div class="answer" markdown="1">

Since version 0.10.0 (released in February 2024), DuckDB is backwards-compatible when reading database files, i.e., newer versions of DuckDB are always able to read database files created with an older version of DuckDB.
DuckDB also provides partial forwards-compatibility on a best-effort basis. See the [storage page]({% link docs/stable/internals/storage.md %}) for more details.
Compatibility is also guaranteed between different DuckDB clients (e.g., Python and R): a database file created with one client can be read with other clients.

</div>

</div>

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### How does DuckDB handle concurrency? Can multiple processes write to DuckDB?

<div class="answer" markdown="1">
See the documentation on [handling concurrency]({% link docs/stable/connect/concurrency.md %}#handling-concurrency)
and the section on [“Writing to DuckDB from Multiple Processes”]({% link docs/stable/connect/concurrency.md %}#writing-to-duckdb-from-multiple-processes).

To work on the same data set with multiple DuckDB clients, consider using the [DuckLake format](http://ducklake.select/) through the [`ducklake` extension]({% link docs/stable/core_extensions/ducklake.md %}).
</div>

</div>

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### Is there an official DuckDB Docker image available?

<div class="answer" markdown="1">
You can run the DuckDB command line client using the official [DuckDB Docker image]({% link docs/stable/operations_manual/duckdb_docker.md %}).

Please note that in most cases you do not need a container to run DuckDB: you can simply deploy it [in-process]({% link why_duckdb.md %}#simple) within your client application or as a standalone command-line binary.
</div>

</div>

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### How to work with multiple DuckDB clients on the same computer?

<div class="answer" markdown="1">

You can install multiple DuckDB clients on the same computer.
These clients are installed individually and can have different DuckDB versions.
For example, you can use the DuckDB 1.3.2 package in R, DuckDB 1.4.0 as the CLI client, and the preview release in Python.

If you are unsure about the DuckDB version used in a process, run the `PRAGMA version` query, which prints the version of DuckDB.

</div>

</div>

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### Where can I learn more about DuckDB?

<div class="answer" markdown="1">

DuckDB has an the official [documentation]({% link docs/stable/index.md %}), [blog]({% link news/index.html %}) and [library]({% link library/index.html %}).
At the same time, there are a few third-party resources which can help you learn more about DuckDB:

* To discover projects using DuckDB, we recommend visiting the [`awesome-duckdb` repository](https://github.com/davidgasquez/awesome-duckdb).
* There is a number of [DuckDB books](https://www.goodreads.com/search?utf8=%E2%9C%93&q=duckdb&search_type=books) available.
* The [tldr pages](https://tldr.sh/) initiative has a [DuckDB entry](https://tldr.inbrowser.app/pages/common/duckdb).

</div>

</div>

<!-- ################################################################################# -->
<!-- ################################################################################# -->
<!-- ################################################################################# -->

## Performance

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### Does DuckDB use SIMD?

<div class="answer" markdown="1">

DuckDB does not use *explicit SIMD* (single instruction, multiple data) instructions because they greatly complicate portability and compilation. Instead, DuckDB uses *implicit SIMD*, where we go to great lengths to write our C++ code in such a way that the compiler can *auto-generate SIMD instructions* for the specific hardware. As an example why this is a good idea, it took 10 minutes to port DuckDB to the Apple Silicon architecture.

</div>

</div>

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### How does scalability work in DuckDB?

<div class="answer" markdown="1">

DuckDB is a single-node database system, hence it makes use of _vertical scalability,_
i.e., making use of more resources (CPU, memory, and disk) to support larger datasets.
DuckDB has been tested on machines with 100+ CPU cores and terabytes of memory.

DuckDB's native database format also scales for multiple terabytes of data but this needs some planning – see the [“Working with Huge Databases” page]({% link docs/stable/guides/performance/working_with_huge_databases.md %}).

For working with large-scale datasets and/or collaborating on the same dataset, consider using the [DuckLake](https://ducklake.select/) lakehouse format.

</div>

</div>

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### I would like to benchmark DuckDB against another system. How do I proceed?

<div class="answer" markdown="1">

We welcome experiments comparing DuckDB's performance to other systems.
To ensure fair comparison, we have a few recommendations.
First, try to use the [preview release]({% link docs/preview/index.md %}), which often has significant performance improvements compared to the last stable release.
Second, consider consulting our DBTest 2018 paper [_Fair Benchmarking Considered Difficult: Common Pitfalls In Database Performance Testing_](https://hannes.muehleisen.org/publications/DBTEST2018-performance-testing.pdf) for guidelines on how to avoid common issues in benchmarks.
Third, study the DuckDB [Performance Guide]({% link docs/stable/guides/performance/overview.md %}), which has best practices for ensuring optimal performance.
Finally, please report the DuckDB version (for stable version, the version number, for nightly builds, the commit hash).

</div>

</div>

<!-- ################################################################################# -->
<!-- ################################################################################# -->
<!-- ################################################################################# -->

## Using DuckDB

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### Is DuckDB intended for data science or data engineering workloads?

<div class="answer" markdown="1">

DuckDB was designed with both data science and data engineering workloads in mind.
Therefore, you can use DuckDB's SQL syntax to be highly flexible, or very precise, depending on your needs.

For data science users, who often run queries in an interactive fashion, DuckDB offers several mechanisms for quickly exploring data sets.
For example, CSV files can be loaded by [auto-inferring their schema]({% link docs/stable/data/csv/auto_detection.md %}) using `CREATE TABLE tbl AS FROM 'input.csv'`.
Moreover, there numerous SQL shorthands known as [“friendly SQL”]({% link docs/stable/sql/dialect/friendly_sql.md %}) for more concise expressions, e.g., the [`GROUP BY ALL` clause]({% link docs/stable/sql/query_syntax/groupby.md %}#group-by-all).

For data engineering use cases, DuckDB allows full control over the loading process, so it is possible to define the precise schema using a `CREATE TABLE tbl ⟨schema⟩`{:.language-sql .highlight} statement and populate it using a [`COPY` statement]({% link docs/stable/sql/statements/copy.md %}) that specifies the CSV's dialect (delimiter, quotes, etc.).
Most friendly SQL extensions are simple to rewrite to SQL queries that are fully compatible with PostgreSQL.
For example, the `GROUP BY ALL` clause can be replaced with a `GROUP BY` clause and an explicit list of columns.

</div>

</div>

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### What are typical use cases for DuckDB?

<div class="answer" markdown="1">

DuckDB's use cases can be split into roughly
<a href="https://blobs.duckdb.org/events/duckcon5/hannes-muhleisen-mark-raasveldt-introduction-and-state-of-project.pdf#page=8">three major categories</a>.
Namely, DuckDB can be used
for interactive data analysis by a user (“data science”) and
as pipeline component for automated data processing (“data enginereering”).
DuckDB can also be deployed in novel architectures, where one traditionally couldn't run an analytical database management system but DuckDB is available thanks to its portability.
These architectures include running DuckDB in browsers (using the <a href="{% link docs/stable/clients/wasm/overview.md %}">WebAssembly client</a>) and on smartphones.
Additionally, DuckDB's extensions unlock use cases such as <a href="{% link docs/stable/core_extensions/spatial/overview.md %}">geospatial analysis</a> and deep integration with
<a href="{% link docs/stable/core_extensions/mysql.md %}">other</a>
<a href="{% link docs/stable/core_extensions/postgres.md %}">database</a>
<a href="{% link docs/stable/core_extensions/sqlite.md %}">systems</a>.
And finally, in some cases, DuckDB <a href="https://www.nikolasgoebel.com/2024/05/28/duckdb-doesnt-need-data">doesn't even need data to be a database</a>.

</div>

</div>

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### I would like feature X to be implemented in DuckDB. How do I proceed?

<div class="answer" markdown="1">

Features in DuckDB can be implemented in different ways: in the main DuckDB project, as a [core extension]({% link docs/stable/core_extensions/overview.md %}) or a [community extension]({% link community_extensions/index.md %}). If you have a feature request for DuckDB, please follow these guidelines:

* If you have a feature idea, please raise an issue in the [“Ideas” section in DuckDB's GitHub Discussions](https://github.com/duckdb/duckdb/discussions/categories/ideas). The DuckDB team monitors these ideas and, over time, implements the frequently requested features. For example, we recently published the [Avro Community Extension]({% link community_extensions/extensions/avro.md %}) to support reading Avro files, which was the most requested feature in the issue tracker.
* If you would like to implement a feature in the main DuckDB project, please discuss it with the DuckDB team on GitHub Discussions or on [our Discord server](https://discord.duckdb.org/). The team can verify whether the idea and the proposed implementation line up with the project's long-term vision.
* If you would like to implement a feature as an extension, consider submitting it to the [Community Extensions repository]({% link community_extensions/index.md %}).

Please note that DuckDB Labs, the company that employs the main DuckDB contributors, provides [consultancy services for DuckDB](https://duckdblabs.com/support/), which can include implementing features in DuckDB or as DuckDB extensions.

</div>

</div>

<!-- ################################################################################# -->
<!-- ################################################################################# -->
<!-- ################################################################################# -->

## Releases and Development

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### Which DuckDB clients and versions are officially supported?

<div class="answer" markdown="1">

Official supports covers the [primary clients]({% link docs/stable/clients/overview.md %}) of the latest LTS version (currently 1.4.x) and the latest stable version (currently also 1.4.x).

</div>

</div>

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### How frequently are new DuckDB versions released?

<div class="answer" markdown="1">

New feature releases (e.g., v1.2.0) are released every 3–5 months.
Bugfix releases (e.g., v1.1.3) are released every 2–4 weeks after a feature release.
You can find the recent releases in the [Release Calendar]({% link release_calendar.md %}).

</div>

</div>

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### When is the next version going to be released and what features can I expect?

<div class="answer" markdown="1">

Please check the [Release Calendar]({% link release_calendar.md %}) for the planned release date of the next stable version of DuckDB
and the [Development Roadmap]({% link roadmap.md %}) for the features planned for the upcoming year.

</div>

</div>

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### How can I contribute to the DuckDB documentation?

<div class="answer" markdown="1">

The DuckDB website is hosted by GitHub Pages and is deployed from the repository at [`duckdb/duckdb-web`](https://github.com/duckdb/duckdb-web).
When the documentation is browsed from a desktop computer, every page has a “Page Source” button on the top that navigates you to its Markdown source file.
Pull requests to fix issues or to expand the documentation section on DuckDB's features are very welcome.
Before opening a pull request, please consult our [Contributor Guide](https://github.com/duckdb/duckdb-web/blob/main/CONTRIBUTING.md).

</div>

</div>

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### What are official sources on DuckDB?

<div class="answer" markdown="1">

In the following, we list official, authoritative sources on the DuckDB and the DuckLake projects.
Exercise caution when using other sources.
You should be particularly cautious when downloading binaries and installation scripts from other sources.

Websites:

* [`duckdb.org`](https://duckdb.org/) and [`duckdb.io`](https://duckdb.io/): DuckDB
* [`duckdblabs.com`](https://duckdblabs.com/): DuckDB Labs
* [`ducklake.select`](https://ducklake.select/) and [`ducklake.dev`](https://ducklake.dev/): DuckLake

Social media:

* [Bluesky](https://bsky.app/profile/duckdb.org)
* [LinkedIn](https://www.linkedin.com/company/duckdb/)
* [Twitter (X)](https://x.com/duckdb)


</div>

</div>
