---
github_repository: https://github.com/phillc73/duckdf
layout: docu
redirect_from:
- /docs/clients/r/duckdf
- /docs/stable/clients/r/duckdf
- /docs/current/clients/r/duckdf
- /docs/lts/clients/r/duckdf
- /docs/preview/clients/r/duckdf
title: duckdf
---

[`duckdf`](https://github.com/phillc73/duckdf) is an SQL interface for R data frames, built on the [DuckDB R client]({% link docs/2.0/clients/r/overview.md %}). Data frames are registered directly with an in-process DuckDB instance as zero-copy views, queried with standard SQL, and returned as data frame results, without copying data to an external database server. `duckdf` has no tidyverse dependencies.

## Installation

`duckdf` is available on [CRAN](https://cran.r-project.org/web/packages/duckdf/index.html) and requires `duckdb` 1.5.6 or later:

```r
install.packages("duckdf")
```

## Querying Data Frames

The `duckdf()` function runs a `SELECT` query on the data frames in scope and returns the result as a data frame:

```r
library("duckdf")

df <- data.frame(id = 1:3, value = c(10, 20, 30))
duckdf("SELECT id, value FROM df WHERE value >= 20")
```

```text
  id value
1  2    20
2  3    30
```

`duckdf` finds the data frames referenced in the query using DuckDB's parser, so subqueries, joins, CTEs, and quoted identifiers work. Files that DuckDB reads natively, such as [CSV]({% link docs/2.0/data/csv/overview.md %}) and [Parquet]({% link docs/2.0/data/parquet/overview.md %}) files, can be queried without registration.

To skip the table discovery, name the data frame explicitly with the `df_name` argument. To bind query parameters safely, pass them with the `params` argument:

```r
duckdf("SELECT mpg, cyl FROM mtcars WHERE disp >= 200", df_name = "mtcars")
duckdf(
  "SELECT mpg FROM mtcars WHERE cyl = $1",
  df = list(mtcars = mtcars),
  params = list(4)
)
```

## Other Functions

| Function | Description |
|----------|-------------|
| `persist()` | Run a query on an on-disk DuckDB database, writing the referenced data frames into it as tables |
| `gander()` | Preview the first five rows of each table in a database |
| `ingest()` | Read a CSV file into DuckDB, either into a database on disk or returned to R |
| `cleanup()` | Remove a named on-disk database and close the shared connection |
| `duckdf_views()` | List the views registered on the shared connection |

## History

The approach dates from 2020, when [issue #459](https://github.com/duckdb/duckdb/issues/459) proposed registering an R data frame as a virtual table with [`duckdb_register()`]({% link docs/2.0/clients/r/overview.md %}#efficient-transfer) in duckdb-r. Version 0.2.1 is a rebuild of the package for `duckdb` 1.5.6 and later.
