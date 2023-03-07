---
layout: docu
title: Frequently Asked Questions
selected: FAQ
---


### Who makes DuckDB?
DuckDB is maintained by [Dr. Mark Raasveldt](https://mytherin.github.io) & [Dr. Hannes Mühleisen](https://hannes.muehleisen.org) along with [many other contributors](https://github.com/duckdb/duckdb/graphs/contributors) from all over the world. Mark and Hannes have set up the [DuckDB Foundation](https://duckdb.org/foundation/) that collects donations and funds development and maintenance of DuckDB. Mark and Hannes are also co-founders of [DuckDB Labs](https://www.duckdblabs.com), which provides commercial services around DuckDB. Several other DuckDB contributors are also affiliated with DuckDB Labs.  
DuckDB's initial development took place at the [Database Architectures Group](https://www.cwi.nl/research/groups/database-architectures) at the [Centrum Wiskunde & Informatica (CWI)](https://www.cwi.nl) in Amsterdam, The Netherlands. 

### Why call it DuckDB?
Ducks are amazing animals. They can fly, walk and swim. They can also live off pretty much everything. They are quite resilient to environmental challenges. A duck's song will bring people back from the dead and [inspires database research](https://static1.squarespace.com/static/51f8f4aae4b0cdf15da554e1/57023acae321408302d6b936/5973b537bebafb04b9520c3d/1500755312736/11_Wilbur_buiten_DQ1C0104.jpg?format=1000w). They are thus the perfect mascot for a versatile and resilient data management system. Also the logo designs itself.

### Where do I find the DuckDB Logo?
You can download the DuckDB Logo here: <br/> • Web: [png](/images/logo-dl/DuckDB_Logo.png) / [jpg](/images/logo-dl/DuckDB_Logo.jpg) <br/>  • Print: [svg](/images/logo-dl/DuckDB_Logo.svg) / [pdf](/images/logo-dl/DuckDB_Logo.pdf) <br/><br/>The DuckDB logo & website were designed by [Jonathan Auch](http://jonathan-auch.de) & [Max Wohlleber](https://maxwohlleber.de).

### How can I expand the DuckDB website?
The DuckDB Website is hosted by GitHub pages, its repository is [here](
https://github.com/duckdb/duckdb-web). Pull requests to fix issues or generally expand the documentation section are very welcome.

### I benchmarked DuckDB and its slower than \[some other system\]
In a departure from traditional academic systems research practise, we have at first focused our attention on correctness, not raw performance. So it is entirely possible DuckDB is slower than some other, more mature system at this point. That being said, we are now confident DuckDB produces correct query results, and are actively working to make it fast, too. So publishing benchmark numbers from the current preview releases is certainly interesting, but should not be taken as the definitive results on what the DuckDB architecture can or cannot do.

### Does DuckDB use SIMD?
DuckDB does not use *explicit SIMD* instructions because they greatly complicate portability and compilation. Instead, DuckDB uses *implicit SIMD*, where we go to great lengths to write our C++ code in such a way that the compiler can *auto-generate SIMD instructions* for the specific hardware. As an example why this is a good idea, porting DuckDB to the new Apple M1 architecture took 10 minutes.

### How does DuckDB handle concurrency?
DuckDB has 2 configurable options for concurrency. 1. One process can both read and write to the database. 2. Multiple processes can read from the database, but no processes can write ([`access_mode = 'READ_ONLY'`](/docs/sql/configuration#configuration-reference)). When using option 1, DuckDB does support multiple writer threads using a combination of MVCC (Multi-Version Concurrency Control) and optimistic concurrency control (see below), but all within that single writer process. The reason for this concurrency model is to allow for the caching of data in RAM for faster analytical queries, rather than going back and forth to disk during each query. It also allows the caching of functions pointers, the database catalog, and other items so that subsequent queries on the same connection are faster. DuckDB is also optimized for bulk operations, so executing many small transactions is not a primary design goal. 

### How does DuckDB handle concurrency within a single process?
DuckDB supports multiple writer threads using a combination of MVCC (Multi-Version Concurrency Control) and optimistic concurrency control. As long as there are no write conflicts, multiple concurrent writes will succeed. Appends will never conflict, even on the same table. Multiple threads can also simultaneously update separate tables or separate subsets of the same table. Optimistic concurrency control comes into play when two threads attempt to edit (update or delete) the same row of data at the same time. In that situation, the second thread to attempt the edit will fail with a conflict error. 

### How can multiple processes write to DuckDB?
Note that this is not supported automatically and is not a primary design goal (see "How does DuckDB handle concurrency?" above). If multiple processes must write to the same file, several design patterns are possible, but would need to be implemented in application logic. For example, each process could acquire a cross-process mutex lock, then open the database in read/write mode and close it when the query is complete. Instead of using a mutex lock, each process could instead retry the connection if another process is already connected to the database (being sure to close the connection upon query completion). Another alternative would be to do multiprocess transactions on a Postgres or SQLite database, and use DuckDB's [Postgres scanner](/docs/extensions/postgres_scanner) or [SQLite scanner](/docs/extensions/sqlite_scanner) to execute analytical queries on that data periodically. Additional options include writing data to parquet files and using DuckDB's ability to [read multiple parquet files](/docs/data/parquet), taking a similar approach with [csv files](/docs/data/csv), or creating a web server to receive requests and manage reads and writes to DuckDB. 

### How are DuckDB, the DuckDB Foundation, DuckDB Labs, and MotherDuck related?
**DuckDB** is the name of the MIT licensed open source project. The [**DuckDB Foundation**](/foundation/) is a non-profit organization that holds much of the intellectual property of the DuckDB project. Its statutes also ensure DuckDB remains open source under the MIT license in perpetuity. Donations to the DuckDB Foundation directly fund DuckDB development and allow membership into the DuckDB user association. This association provides input to the DuckDB development roadmap. [**DuckDB Labs**](https://duckdblabs.com/) is a company that provides services around DuckDB including prioritized feature development, integration with external systems, custom extensions, or flexible licensing terms. [**MotherDuck**](https://motherduck.com/) is a venture-backed company creating a hybrid cloud/local platform using DuckDB. MotherDuck contracts with DuckDB Labs for development services, and DuckDB Labs owns a portion of MotherDuck. [See the partnership announcement for details](https://duckdblabs.com/news/2022/11/15/motherduck-partnership.html). 
