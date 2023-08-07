---
layout: docu
title: Why DuckDB
selected: Why DuckDB
description: Here, we try to explain what goals DuckDB has and why and how we try to achieve those goals through technical means.

---

There are many database management systems (DBMS) out there. But there is [no one-size-fits all database system](http://cs.brown.edu/research/db/publications/fits_all.pdf). All take different trade-offs to better adjust to specific use cases. DuckDB is no different. Here, we try to explain what goals DuckDB has and why and how we try to achieve those goals through technical means. To start with, DuckDB is a [relational (table-oriented) DBMS](https://en.wikipedia.org/wiki/Relational_database) that supports the [Structured Query Language (SQL)](https://en.wikipedia.org/wiki/SQL).

<div class="headline" id="duckdbisfast">
	<div class="icon"><span class="duckdbsymbol">&#xE300;</span></div>
	<h1>Fast Analytical Queries</h1>
</div>
DuckDB is designed to support **analytical query workloads**, also known as [Online analytical processing (OLAP)](https://en.wikipedia.org/wiki/Online_analytical_processing). These workloads are characterized by complex, relatively long-running queries that process significant portions of the stored dataset, for example aggregations over entire tables or joins between several large tables. Changes to the data are expected to be rather large-scale as well, with several rows being appended, or large portions of tables being changed or added at the same time.

To efficiently support this workload, it is critical to reduce the amount of CPU cycles that are expended per individual value. The state of the art in data management to achieve this are either [vectorized or just-in-time query execution engines](https://www.vldb.org/pvldb/vol11/p2209-kersten.pdf). DuckDB contains a **columnar-vectorized query execution engine**, where queries are still interpreted, but a large batch of values (a "vector") are processed in one operation. This greatly reduces overhead present in traditional systems such as PostgreSQL, MySQL or SQLite which process each row sequentially. Vectorized query execution leads to far better performance in OLAP queries.

<div class="headline" id="duckdbissimple">
	<div class="icon"><span class="duckdbsymbol">&#xE100;</span></div>
	<h1>Simple and Portable Deployment</h1>
</div>
SQLite is the [world's most widely deployed DBMS](https://www.sqlite.org/mostdeployed.html). Simplicity in installation, and embedded in-process operation are central to its success. DuckDB adopts these ideas of simplicity and embedded operation.

DuckDB has **no external dependencies**, neither for compilation nor during run-time. For releases, the entire source tree of DuckDB is compiled into two files, a header and an implementation file, a so-called "amalgamation". This greatly simplifies deployment and integration in other build processes. For building, all that is required to build DuckDB is a working C++11 compiler.

For DuckDB, there is no DBMS server software to install, update and maintain. DuckDB does not run as a separate process, but completely **embedded within a host process**. For the analytical use cases that DuckDB targets, this has the additional advantage of **high-speed data transfer** to and from the database. In some cases, DuckDB can process foreign data without copying. For example, the DuckDB Python package can run queries directly on Pandas data without ever importing or copying any data.

<div class="headline" id="duckdbisfeaturerich">
	<div class="icon"><span class="duckdbsymbol">&#xE200;</span></div>
	<h1>Feature-Rich</h1>
</div>
DuckDB provides serious data management features. There is extensive support for **complex queries** in SQL with a large function library, window functions etc. DuckDB provides **transactional guarantees** (ACID properties) through our custom, bulk-optimized [Multi-Version Concurrency Control (MVCC)](https://en.wikipedia.org/wiki/Multiversion_concurrency_control). Data can be stored in persistent, **single-file databases**. DuckDB supports secondary indexes to speed up queries trying to find a single table entry.

DuckDB is deeply integrated into Python and R for efficient interactive data analysis. DuckDB provides APIs for Java, C, C++, Julia, Swift, and others.

<div class="headline" id="duckdbtesting">
	<div class="icon"><span class="duckdbsymbol">&#xE250;</span></div>
	<h1>Thorough Testing</h1>
</div>
While DuckDB is created by a research group, it is not intended to be a research prototype. DuckDB is intended to be a stable and mature database system.

To facilitate this stability, DuckDB is intensively tested using [Continuous Integration](https://github.com/duckdb/duckdb/actions). DuckDB's test suite currently contains millions of queries, and includes queries adapted from the test suites of SQLite, PostgreSQL and MonetDB. Tests are repeated on a wide variety of platforms and compilers. Every pull request is checked against the full test setup and only merged if it passes.

In addition to this test suite, we run various tests that stress DuckDB under heavy loads. We run the TPC-H and TPC-DS benchmarks, and run various tests where DuckDB is used by many clients in parallel.


<div class="headline" id="duckdbisfree">
	<div class="icon"><span class="duckdbsymbol">&#xE400;</span></div>
	<h1>Free &amp; Open Source License</h1>
</div>
DuckDB's development started while the main developers were public servants in The Netherlands. We see it as our responsibility and duty to society to make the results of our work freely available to anyone in The Netherlands or elsewhere. This is why DuckDB is released under the very permissive [MIT License](https://en.wikipedia.org/wiki/MIT_License). DuckDB is Open Source, the entire source code is freely available on GitHub. We invite contributions from anyone provided they adhere to our [Code of Conduct](../code_of_conduct).


## Peer-Reviewed Papers
* [These Rows Are Made for Sorting and That's Just What We'll Do](/pdf/ICDE2023-kuiper-muehleisen-sorting.pdf) (ICDE 2023)
* [DuckDB-Wasm: Fast Analytical Processing for the Web](/pdf/VLDB2022-kohn-duckdb-wasm.pdf) (VLDB 2022 Demo)
* [Data Management for Data Science - Towards Embedded Analytics](/pdf/CIDR2020-raasveldt-muehleisen-duckdb.pdf) (CIDR 2020)
* [DuckDB: an Embeddable Analytical Database](/pdf/SIGMOD2019-demo-duckdb.pdf) (SIGMOD 2019 Demo)

## Media
* [DuckDB: Bringing analytical SQL directly to your Python shell (EuroPython 2023)](https://www.youtube.com/watch?v=egN4TwVyJss) (Technical talk, ca. 40min)
* [DuckCon #3](https://www.youtube.com/watch?v=9p_sQfy8uuk&list=PLzIMXBizEZjhy6QG4Eqoe9k9NgBa-w67Y) (Latest updates and technical talks about projects using DuckDB)
* [DuckDB keynote (Data + AI Summit 2023)](https://www.youtube.com/watch?v=AKix55rQEUU) (Keynote presentation, ca. 10 min)
* [DuckDB – The SQLite for Analytics (CMU Database Group - Quarantine Tech Talks)](https://www.youtube.com/watch?v=PFUZlNQIndo) (Video Presentation, ca. 1h)
* [DuckDB - An Embeddable Analytical Database (FOSDEM)](https://mirrors.dotsrc.org/fosdem/2020/H.2215/duckdb.mp4) (Video Presentation, ca. 15min)
* [Move Your Database To The Data And Speed Up Your Analytics With DuckDB (Data Engineering Podcast)](https://www.dataengineeringpodcast.com/duckdb-in-process-olap-database-episode-270/) (Podcast, ca. 1:20h)
* [DuckDB, An In-Process Analytical DBMS (NYC Data Hackers)](https://www.youtube.com/watch?v=Z-6SnP6yzgo) (Video Presentation, ca. 1:30h)
* [DuckDB Testing - Present and Future (DBTest 2022 Keynote)](https://www.youtube.com/watch?v=BgC79Zt2fPs) (Video Presentation, ca. 1h)
* [Push-Based Execution in DuckDB (CWI Database Architectures Seminar)](https://www.youtube.com/watch?v=MA0OsvYFGrc) (Video Presentation, ca. 1h)
* [Fastest Table Sort in the West - Redesigning DuckDB’s Sort (DSDSD)](https://www.youtube.com/watch?v=m6Yg2sXGui0) (Video Presentation, ca. 20min)
* [The Case for In-Process Analytics](/pdf/sigmod2021-muehleisen-inprocess-slides.pdf) (Slides)
* [1000 days of DuckDB - The Pareto Principle still holds](http://dsdsd.da.cwi.nl/slides/dsdsd-duckdb.pdf) (Slides)
* [DuckDB - an Embeddable Analytical RDBMS](https://db.in.tum.de/teaching/ss19/moderndbs/duckdb-tum.pdf) (Slides)
* [DuckDB: Introducing a New Class of Data Management Systems (I/O Magazine, ICT Research Platform Nederland)](https://ict-research.nl/wordpress/wp-content/uploads/2023/04/IO-magazine-NR1-2023.pdf#page=10) (article)

## Other Projects
Here are some projects that we know of that use DuckDB. If you would like your project to be added here, open a GitHub issue.

* [taxadb: A High-Performance Local Taxonomic Database Interface](https://CRAN.R-project.org/package=taxadb)
* [duckdb.js - DuckDB compiled to JavaScript (PoC)](https://github.com/ankoh/duckdb.js)
* [SQL for R dataframes with DuckDB](https://github.com/phillc73/duckdf)
* [DuckDB conda support](https://github.com/conda-forge/python-duckdb-feedstock)
* [DBT adapter for DuckDB](https://github.com/jwills/dbt-duckdb)
* [newLISP bindings for DuckDB](https://github.com/luxint/duckdb)
* [duckdb_engine - SQLAlchemy driver for DuckDB](https://github.com/Mause/duckdb_engine)
* [Toy DuckDB based timeseries database](https://github.com/berthubert/ducktime)
* [PHP example to integrate DuckDB using PHP-FFI](https://github.com/thomasbley/php-duckdb-integration)
* [DuckDB Foreign Data Wrapper for PostgreSQL](https://github.com/alitrack/duckdb_fdw)
* [Demo: CRUD operations with Qt5 and DuckDB](https://github.com/chilarai/qt-duckdb)
* [Elixir driver](https://github.com/mpope9/exduckdb) and [Ecto adapter](https://github.com/mpope9/ecto_duckdb/) for DuckDB
* [DuckDB backend](https://fugue-tutorials.readthedocs.io/tutorials/integrations/backends/duckdb.html) for [Fugue](https://github.com/fugue-project/fugue)
* [StabilitySort](https://gitlab.com/baaron/StabilitySort) bioinformatics tool for finding unstable variants from predicted AlphaFold2 structures  
* [Extract and load data from APIs to DuckDB using data load tool](https://dlthub.com/docs/dlt-ecosystem/destinations/duckdb)

## Testimonials
See our [DuckDB Testimonial Twitter Wall](/docs/twitter_wall)

## Standing on the Shoulders of Giants
DuckDB uses some components from various Open-Source projects and draws inspiration from scientific publications. We are very greatful for this. Here is an overview:

* **Execution engine:** The vectorized execution engine is inspired by the paper [MonetDB/X100: Hyper-Pipelining Query Execution](http://cidrdb.org/cidr2005/papers/P19.pdf) by Peter Boncz, Marcin Zukowski and Niels Nes.
* **Optimizer:** DuckDB's optimizer draws inspiration from the papers [Dynamic programming strikes back](https://15721.courses.cs.cmu.edu/spring2020/papers/20-optimizer2/p539-moerkotte.pdf) by Guido Moerkotte and Thomas Neumann as well as [Unnesting Arbitrary Queries](http://www.btw-2015.de/res/proceedings/Hauptband/Wiss/Neumann-Unnesting_Arbitrary_Querie.pdf) by Thomas Neumann and Alfons Kemper.
* **Concurrency control:** Our MVCC implementation is inspired by the paper [Fast Serializable Multi-Version Concurrency Control for Main-Memory Database Systems](https://db.in.tum.de/~muehlbau/papers/mvcc.pdf) by Thomas Neumann, Tobias Mühlbauer and Alfons Kemper.
* **Secondary Indexes:** DuckDB has support for secondary indexes based on the paper [The Adaptive Radix Tree: ARTful Indexing for Main-Memory Databases](https://db.in.tum.de/~leis/papers/ART.pdf) by Viktor Leis, Alfons Kemper and Thomas Neumann.
* **SQL Window Functions:** DuckDB's window functions implementation uses Segment Tree Aggregation as described in the paper "Efficient Processing of Window Functions in Analytical SQL Queries" by Viktor Leis, Kan Kundhikanjana, Alfons Kemper and Thomas Neumann.
* **SQL Inequality Joins:** DuckDB's inequality join implementation uses the IEJoin algorithm as described in the paper [Lightning Fast and Space Efficient Inequality Joins](https://vldb.org/pvldb/vol8/p2074-khayyat.pdf) by 
Zuhair Khayyat, William Lucia, Meghna Singh, Mourad Ouzzani, Paolo Papotti, Jorge-Arnulfo Quiané-Ruiz, Nan Tang and Panos Kalnis.
* **SQL Parser:** We use the PostgreSQL parser that was [repackaged as a stand-alone library](https://github.com/lfittl/libpg_query). The translation to our own parse tree is inspired by [Peloton](https://pelotondb.io).
* **Shell:** We use the [SQLite shell](https://sqlite.org/cli.html) to work with DuckDB.
* **Regular Expressions:** DuckDB uses Google's [RE2](https://github.com/google/re2) regular expression engine.
* **String Formatting:** DuckDB uses the [fmt](https://github.com/fmtlib/fmt) string formatting library.
* **UTF Wrangling:** DuckDB uses the [utf8proc](https://juliastrings.github.io/utf8proc/) library to check and normalize UTF8.
* **Collation and Time:** DuckDB uses the [ICU](https://unicode-org.github.io/icu/) library for collation, time zone, and calendar support.
* **Test Framework:** DuckDB uses the [Catch2](https://github.com/catchorg/Catch2) unit test framework.
* **Test Cases:** We use the [SQL Logic Tests from SQLite](https://www.sqlite.org/sqllogictest/doc/trunk/about.wiki) to test DuckDB.
* **Result Validation:** [Manuel Rigger](https://www.manuelrigger.at) used his excellent [SQLancer](https://github.com/sqlancer/sqlancer) tool to verify DuckDB result correctness.
* **Query fuzzing:** We use [SQLsmith](https://github.com/anse1/sqlsmith) to generate random queries for additional testing.
* **JSON Parser:** We use [yyjson](https://github.com/ibireme/yyjson), a high performance JSON library written in ANSI C, to parse JSON in DuckDB's [JSON Extension](docs/extensions/json).
