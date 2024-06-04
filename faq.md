---
layout: docu
title: Frequently Asked Questions
---

<div class="qa-wrap" markdown="1">

### Who makes DuckDB?

<div class="answer" markdown="1">

DuckDB is maintained by [Dr. Mark Raasveldt](https://mytherin.github.io) & [Prof. Dr. Hannes Mühleisen](https://hannes.muehleisen.org) along with [many other contributors](https://github.com/duckdb/duckdb/graphs/contributors) from all over the world. Mark and Hannes have set up the [DuckDB Foundation](https://duckdb.org/foundation/) that collects donations and funds development and maintenance of DuckDB. Mark and Hannes are also co-founders of [DuckDB Labs](https://www.duckdblabs.com), which provides commercial services around DuckDB. Several other DuckDB contributors are also affiliated with DuckDB Labs.  
DuckDB's initial development took place at the [Database Architectures Group](https://www.cwi.nl/research/groups/database-architectures) at the [Centrum Wiskunde & Informatica (CWI)](https://www.cwi.nl) in Amsterdam, The Netherlands. 

</div>

</div>

<!-- Q&A entry -->

<div class="qa-wrap" markdown="1">

### Why call it DuckDB?

<div class="answer" markdown="1">

Ducks are amazing animals. They can fly, walk and swim. They can also live off pretty much everything. They are quite resilient to environmental challenges. A duck's song will bring people back from the dead and [inspires database research](/images/wilbur.jpg). They are thus the perfect mascot for a versatile and resilient data management system. Also the logo designs itself.

</div>

</div>

<!-- Q&A entry -->

<div class="qa-wrap" markdown="1">

### How are DuckDB, the DuckDB Foundation, DuckDB Labs, and MotherDuck related?

<div class="answer" markdown="1">

[**DuckDB**](https://duckdb.org/) is the name of the MIT licensed open-source project.<br/>
The [**DuckDB Foundation**](/foundation/) is a non-profit organization that holds the intellectual property of the DuckDB project.
Its statutes also ensure DuckDB remains open-source under the MIT license in perpetuity.
Donations to the DuckDB Foundation directly fund DuckDB development.<br/>
[**DuckDB Labs**](https://duckdblabs.com/) is a company based in Amsterdam that provides commercial support services for DuckDB.
DuckDB Labs employs the core contributors of the DuckDB project.<br/>
[**MotherDuck**](https://motherduck.com/) is a venture-backed company creating a hybrid cloud/local platform using DuckDB.
MotherDuck contracts with DuckDB Labs for development services, and DuckDB Labs owns a portion of MotherDuck.
[See the partnership announcement for details](https://duckdblabs.com/news/2022/11/15/motherduck-partnership.html).
To learn more about MotherDuck, see the [CIDR 2024 paper on MotherDuck](https://www.cidrdb.org/cidr2024/papers/p46-atwal.pdf) and the [MotherDuck documentation](https://motherduck.com/docs).

</div>

</div>

<!-- Q&A entry -->

<div class="qa-wrap" markdown="1">

### Where do I find the DuckDB logo?

<div class="answer" markdown="1">

You can download the DuckDB Logo here: <br/>

- Stacked logo: [svg](/images/logo-dl/DuckDB_Logo-stacked.svg) / [png](/images/logo-dl/DuckDB_Logo-stacked.png) <br/>
- Horizontal logo: [svg](/images/logo-dl/DuckDB_Logo-horizontal.svg) / [png](/images/logo-dl/DuckDB_Logo-horizontal.png) <br/>

Inverted variants for dark backgrounds:

- Stacked logo: [svg](/images/logo-dl/DuckDB_Logo-stacked-dark-mode.svg) / [png](/images/logo-dl/DuckDB_Logo-stacked-dark-mode.png) <br/>
- Horizontal logo: [svg](/images/logo-dl/DuckDB_Logo-horizontal-dark-mode.svg) / [png](/images/logo-dl/DuckDB_Logo-horizontal-dark-mode.png) <br/>

The DuckDB logo & website were designed by [Jonathan Auch](http://jonathan-auch.de) & [Max Wohlleber](https://maxwohlleber.de).

</div>

</div>

<!-- Q&A entry -->

<div class="qa-wrap" markdown="1">

### Where do I find DuckDB trademark use guidelines?

<div class="answer" markdown="1">

Please consult the [trademark guidelines for DuckDB™](/trademark_guidelines).

</div>

</div>

<!-- Q&A entry -->

<div class="qa-wrap" markdown="1">

### How can I expand the DuckDB website?

<div class="answer" markdown="1">

The DuckDB Website is hosted by GitHub Pages, its repository is at [`duckdb/duckdb-web`](https://github.com/duckdb/duckdb-web).
When the documentation is browsed from a desktop computer, every page has a "Page Source" button on the top that navigates you to its Markdown source file.
Pull requests to fix issues or to expand the documentation section on DuckDB's features are very welcome.
Before opening a pull request, please consult our [Contributor Guide](https://github.com/duckdb/duckdb/blob/main/CONTRIBUTING.md).

</div>

</div>

<!-- Q&A entry -->

<div class="qa-wrap" markdown="1">

### I benchmarked DuckDB and its slower than \[some other system\]

<div class="answer" markdown="1">

We welcome experiments comparing DuckDB's performance to other systems.
To ensure fair comparison, we have two recommendations.
First, try to use the [latest DuckDB version available as a nightly build](https://duckdb.org/docs/installation/), which often has significant performance improvements compared to the last stable release.
Second, consider consulting our DBTest 2018 paper [_Fair Benchmarking Considered Difficult: Common Pitfalls In Database Performance Testing_](https://hannes.muehleisen.org/publications/DBTEST2018-performance-testing.pdf) for guidelines on how to avoid common issues in benchmarks.

</div>

</div>

<!-- Q&A entry -->

<div class="qa-wrap" markdown="1">

### Does DuckDB use SIMD?

<div class="answer" markdown="1">

DuckDB does not use *explicit SIMD* instructions because they greatly complicate portability and compilation. Instead, DuckDB uses *implicit SIMD*, where we go to great lengths to write our C++ code in such a way that the compiler can *auto-generate SIMD instructions* for the specific hardware. As an example why this is a good idea, it took 10 minutes to port DuckDB to the Apple Silicon architecture.

</div>

</div>

<!-- Q&A entry -->

<div class="qa-wrap" markdown="1">

### Can DuckDB save data to disk?

<div class="answer" markdown="1">

DuckDB supports [persistent storage](/docs/connect/overview#persistent-database) and stores the database as a single file, which includes all tables, views, indexes, macros, etc. present in the database.
DuckDB's [storage format](/internals/storage) uses a compressed columnar representation, which is compact but allows for efficient bulk updates.
DuckDB can also run in [in-memory mode](docs/connect/overview#in-memory-database), where no data is persisted to disk.

</div>

</div>

<!-- Q&A entry -->

<div class="qa-wrap" markdown="1">

### How does DuckDB handle concurrency?

<div class="answer" markdown="1">
See the documentation on [concurrency](/docs/connect/concurrency#handling-concurrency).
</div>

</div>

<!-- Q&A entry -->

<div class="qa-wrap" markdown="1">

### How can multiple processes write to DuckDB?

<div class="answer" markdown="1">
See the [documentation on concurrency](/docs/connect/concurrency#writing-to-duckdb-from-multiple-processes).
</div>

</div>

<!-- Q&A entry -->

<div class="qa-wrap" markdown="1">

### Is there an official DuckDB Docker image available?

<div class="answer" markdown="1">
There is no official DuckDB Docker image available.
DuckDB uses an [in-process deployment model](/why_duckdb#simple), where the client application and DuckDB are running in the same process.
Additionally to the DuckDB clients for Python, R, and other programming languages, DuckDB is also available as a standalone command-line client. This client is available on a [wide range of platforms](/docs/installation/?version=stable&environment=cli) and is portable without containerization, making it unnecessary to containerize the process for most deployments.
</div>

</div>

<!-- Q&A entry -->

<div class="qa-wrap" markdown="1">

### Glossary of terms

<div class="answer" markdown="1">

Here is a glossay of a few common terms used in DuckDB.<br/>
– **In-process database management system:** The DBMS runs in the client application's process instead of running as a separate process, which is common in the traditional client–server setup. An alterative term is **embeddable** database management system. In general, the term _"embedded database management system"_ should be avoided, as it can be confused with DBMSs targeting _embedded systems_ (which run on e.g. microcontrollers).<br/>
– **Replacement scan:** In DuckDB, replacement scans are used when a table name used by a query does not exist in the catalog. These scans can substitute another data source intead of the table. Using replacement scans allows DuckDB to, e.g., seamlessly read [Pandas DataFrames](docs/guides/python/sql_on_pandas) or read input data from remote sources without explicitly invoking the functions that perform this (e.g., [reading Parquet files from https](/docs/guides/import/http_import)). For details, see the [C API - Replacement Scans page](/docs/api/c/replacement_scans).<br/>
– **Extension:** DuckDB has a flexible extension mechanism that allows for dynamically loading extensions. These may extend DuckDB's functionality by providing support for additional file formats, introducing new types, and domain-specific functionality. For details, see the [Extensions page](/docs/extensions/overview).<br/>
– **Platform:** The platform is a combination of the operating system (e.g., Linux, macOS, Windows), system architecture (e.g., AMD64, ARM64), and, optionally, the compiler used (e.g., GCC4). Platforms are used to distributed DuckDB binaries and [extension packages](/docs/extensions/working_with_extensions#platforms).

</div>

</div>
