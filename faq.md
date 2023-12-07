---
layout: docu
title: Frequently Asked Questions
---


### Who makes DuckDB?

DuckDB is maintained by [Dr. Mark Raasveldt](https://mytherin.github.io) & [Prof. Dr. Hannes Mühleisen](https://hannes.muehleisen.org) along with [many other contributors](https://github.com/duckdb/duckdb/graphs/contributors) from all over the world. Mark and Hannes have set up the [DuckDB Foundation](https://duckdb.org/foundation/) that collects donations and funds development and maintenance of DuckDB. Mark and Hannes are also co-founders of [DuckDB Labs](https://www.duckdblabs.com), which provides commercial services around DuckDB. Several other DuckDB contributors are also affiliated with DuckDB Labs.  
DuckDB's initial development took place at the [Database Architectures Group](https://www.cwi.nl/research/groups/database-architectures) at the [Centrum Wiskunde & Informatica (CWI)](https://www.cwi.nl) in Amsterdam, The Netherlands. 

### Why call it DuckDB?

Ducks are amazing animals. They can fly, walk and swim. They can also live off pretty much everything. They are quite resilient to environmental challenges. A duck's song will bring people back from the dead and [inspires database research](/images/wilbur.jpg). They are thus the perfect mascot for a versatile and resilient data management system. Also the logo designs itself.

### Where do I find the DuckDB Logo?

You can download the DuckDB Logo here: <br/> • Stacked logo: [png](/images/logo-dl/DuckDB_Logo-stacked.png) / [svg](/images/logo-dl/DuckDB_Logo-stacked.svg) <br/>  • Horizontal logo: [svg](/images/logo-dl/DuckDB-Logo-horizontal.svg) / [png](/images/logo-dl/DuckDB-Logo-horizontal.png) <br/><br/>The DuckDB logo & website were designed by [Jonathan Auch](http://jonathan-auch.de) & [Max Wohlleber](https://maxwohlleber.de).

### Where do I find DuckDB trademark use guidelines?

You can find the guidelines for DuckDB™ [here](/trademark_guidelines).

### How can I expand the DuckDB website?

The DuckDB Website is hosted by GitHub Pages, its repository is at [`duckdb/duckdb-web`](https://github.com/duckdb/duckdb-web).
When the documentation is browsed from a desktop computer, every page has a "Page Source" button on the top that navigates you to its Markdown source file.
Pull requests to fix issues or to expand the documentation section on DuckDB's features are very welcome.
Before opening a pull request, please consult our [Contributor Guide](https://github.com/duckdb/duckdb/blob/main/CONTRIBUTING.md).

### I benchmarked DuckDB and its slower than \[some other system\]
We welcome experiments comparing DuckDB's performance to other systems.
To ensure fair comparison, we have two recommendations.
First, try to use the [latest (bleeding edge) DuckDB version](https://duckdb.org/docs/installation/), which often has significant performance improvements compared to the last stable release.
Second, consider consulting our DBTest 2018 paper [_Fair Benchmarking Considered Difficult: Common Pitfalls In Database Performance Testing_](https://hannes.muehleisen.org/publications/DBTEST2018-performance-testing.pdf) for guidelines on how to avoid common issues in benchmarks.

### Does DuckDB use SIMD?

DuckDB does not use *explicit SIMD* instructions because they greatly complicate portability and compilation. Instead, DuckDB uses *implicit SIMD*, where we go to great lengths to write our C++ code in such a way that the compiler can *auto-generate SIMD instructions* for the specific hardware. As an example why this is a good idea, porting DuckDB to the new Apple M1 architecture took 10 minutes.

### How does DuckDB handle concurrency?

DuckDB has 2 configurable options for concurrency. 1. One process can both read and write to the database. 2. Multiple processes can read from the database, but no processes can write ([`access_mode = 'READ_ONLY'`](/docs/sql/configuration#configuration-reference)). When using option 1, DuckDB does support multiple writer threads using a combination of MVCC (Multi-Version Concurrency Control) and optimistic concurrency control (see below), but all within that single writer process. The reason for this concurrency model is to allow for the caching of data in RAM for faster analytical queries, rather than going back and forth to disk during each query. It also allows the caching of functions pointers, the database catalog, and other items so that subsequent queries on the same connection are faster. DuckDB is also optimized for bulk operations, so executing many small transactions is not a primary design goal. 

### How does DuckDB handle concurrency within a single process?

DuckDB supports multiple writer threads using a combination of MVCC (Multi-Version Concurrency Control) and optimistic concurrency control. As long as there are no write conflicts, multiple concurrent writes will succeed. Appends will never conflict, even on the same table. Multiple threads can also simultaneously update separate tables or separate subsets of the same table. Optimistic concurrency control comes into play when two threads attempt to edit (update or delete) the same row of data at the same time. In that situation, the second thread to attempt the edit will fail with a conflict error. 

### How can multiple processes write to DuckDB?

Note that this is not supported automatically and is not a primary design goal (see "How does DuckDB handle concurrency?" above). If multiple processes must write to the same file, several design patterns are possible, but would need to be implemented in application logic. For example, each process could acquire a cross-process mutex lock, then open the database in read/write mode and close it when the query is complete. Instead of using a mutex lock, each process could instead retry the connection if another process is already connected to the database (being sure to close the connection upon query completion). Another alternative would be to do multiprocess transactions on a Postgres or SQLite database, and use DuckDB's [Postgres](/docs/extensions/postgres) or [SQLite](/docs/extensions/sqlite) extensions to execute analytical queries on that data periodically. Additional options include writing data to parquet files and using DuckDB's ability to [read multiple parquet files](/docs/data/parquet), taking a similar approach with [csv files](/docs/data/csv), or creating a web server to receive requests and manage reads and writes to DuckDB. 

### Glossary of terms

Here is a glossay of a few common terms used in DuckDB.\
**– In-process database management system:** The DBMS runs in the client application's process instead of running as a separate process, which is common in the traditional client–server setup. An alterative term is **embeddable** database management system. In general, the term _"embedded database management system"_ should be avoided, as it can be confused with DBMSs targeting _embedded systems_ (which run on e.g. microcontrollers).\
**– Replacement scan:** In DuckDB, replacement scans are used when a table name used by a query does not exist in the catalog. These scans can substitute another data source intead of the table. Using replacement scans allows DuckDB to, e.g., seamlessly read [Pandas DataFrames](docs/guides/python/sql_on_pandas) or read input data from remote sources without explicitly invoking the functions that perform this (e.g., [reading Parquet files from https](/docs/guides/import/http_import)). For details, see the [C API - Replacement Scans page](/docs/api/c/replacement_scans).\
**– Extension:** DuckDB has a flexible extension mechanism that allows for dynamically loading extensions. These may extend DuckDB's functionality by providing support for additional file formats, introducing new types, and domain-specific functionality. For details, see the [Extensions page](/docs/extensions/overview).\
**– Platform:** The platform is a combination of the operating system (e.g., Linux, macOS, Windows), system architecture (e.g., AMD64, ARM64), and, optionally, the compiler used (e.g., GCC4). Platforms are used to distributed DuckDB binaries and [extension packages](/docs/extensions/working_with_extensions#platforms).

### How are DuckDB, the DuckDB Foundation, DuckDB Labs, and MotherDuck related?

[**DuckDB**](https://duckdb.org/) is the name of the MIT licensed open-source project.\
The [**DuckDB Foundation**](/foundation/) is a non-profit organization that holds the intellectual property of the DuckDB project.
Its statutes also ensure DuckDB remains open-source under the MIT license in perpetuity.
Donations to the DuckDB Foundation directly fund DuckDB development.\
[**DuckDB Labs**](https://duckdblabs.com/) is a company based in Amsterdam that provides commercial support services for DuckDB.
DuckDB Labs employs the core contributors of the DuckDB project.\
[**MotherDuck**](https://motherduck.com/) is a venture-backed company creating a hybrid cloud/local platform using DuckDB.
MotherDuck contracts with DuckDB Labs for development services, and DuckDB Labs owns a portion of MotherDuck.
[See the partnership announcement for details](https://duckdblabs.com/news/2022/11/15/motherduck-partnership.html).
To learn more about MotherDuck, see the [MotherDuck documentation](https://motherduck.com/docs).
