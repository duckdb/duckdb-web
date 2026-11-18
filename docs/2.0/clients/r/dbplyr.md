---
layout: docu
redirect_from:
- /docs/clients/r/dbplyr
- /docs/stable/clients/r/dbplyr
- /docs/current/clients/r/dbplyr
- /docs/lts/clients/r/dbplyr
- /docs/preview/clients/r/dbplyr
title: dbplyr
---

DuckDB plays well with the [dbplyr](https://CRAN.R-project.org/package=dbplyr) / [dplyr](https://dplyr.tidyverse.org) packages for programmatic query construction from R. `dbplyr` translates dplyr pipelines to SQL and runs them on a [DuckDB connection]({% link docs/2.0/clients/r/overview.md %}#startup--shutdown). For a drop-in replacement for dplyr that works on data frames directly, see [`duckplyr`]({% link docs/2.0/clients/r/duckplyr.md %}).

## Installation

```r
install.packages(c("duckdb", "dbplyr"))
```

## Querying Tables

Here is an example:

```r
library("duckdb")
library("dplyr")
con <- dbConnect(duckdb())
duckdb_register(con, "flights", nycflights13::flights)

tbl(con, "flights") |>
  group_by(dest) |>
  summarise(delay = mean(dep_time, na.rm = TRUE)) |>
  collect()
```

## Querying Files

When using `dbplyr`, CSV and Parquet files can be read using the `dplyr::tbl` function.

```r
# Establish a CSV for the sake of this example
write.csv(mtcars, "mtcars.csv")

# Summarize the dataset in DuckDB to avoid reading the entire CSV into R's memory
tbl(con, "mtcars.csv") |>
  group_by(cyl) |>
  summarise(across(disp:wt, .fns = mean)) |>
  collect()
```

```r
# Establish a set of Parquet files
dbExecute(con, "COPY flights TO 'dataset' (FORMAT parquet, PARTITION_BY (year, month))")

# Summarize the dataset in DuckDB to avoid reading 12 Parquet files into R's memory
tbl(con, "read_parquet('dataset/**/*.parquet', hive_partitioning = true)") |>
  filter(month == "3") |>
  summarise(delay = mean(dep_time, na.rm = TRUE)) |>
  collect()
```
