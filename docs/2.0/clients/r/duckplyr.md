---
github_repository: https://github.com/tidyverse/duckplyr
layout: docu
redirect_from:
- /docs/clients/r/duckplyr
- /docs/stable/clients/r/duckplyr
- /docs/current/clients/r/duckplyr
- /docs/lts/clients/r/duckplyr
- /docs/preview/clients/r/duckplyr
title: duckplyr
---

[`duckplyr`](https://duckplyr.tidyverse.org/) is a drop-in replacement for [dplyr](https://dplyr.tidyverse.org/), powered by DuckDB. It runs existing dplyr code with the same results, using DuckDB's execution engine where possible and falling back to dplyr where it is not. It can also analyze larger-than-memory datasets directly from files on disk or on the web. `duckplyr` is developed by [Posit](https://posit.co/), [cynkra](https://www.cynkra.com/), and DuckDB Labs.

Unlike [`dbplyr`]({% link docs/2.0/clients/r/dbplyr.md %}), `duckplyr` does not generate SQL strings: it translates dplyr verbs directly into DuckDB's relational API. For the full documentation, visit [`duckplyr.tidyverse.org`](https://duckplyr.tidyverse.org/).

## Installation

`duckplyr` is available on [CRAN](https://cran.r-project.org/package=duckplyr) and installs the [DuckDB R client]({% link docs/2.0/clients/r/overview.md %}) as a dependency:

```r
install.packages("duckplyr")
```

## Usage as a Drop-In Replacement

Loading `duckplyr` overrides the dplyr methods for data frames for the rest of the session. Existing dplyr code then runs on DuckDB without changes:

```r
library("duckplyr")

flights_df() |>
  filter(!is.na(arr_delay), !is.na(dep_delay)) |>
  mutate(inflight_delay = arr_delay - dep_delay) |>
  summarize(
    .by = c(year, month),
    mean_inflight_delay = mean(inflight_delay),
    median_inflight_delay = median(inflight_delay),
  ) |>
  filter(month <= 6) |>
  arrange(month)
```

```text
# A tibble: 6 × 4
   year month mean_inflight_delay median_inflight_delay
  <int> <int>               <dbl>                 <dbl>
1  2013     1               -3.86                    -5
2  2013     2               -5.15                    -6
3  2013     3               -7.36                    -9
4  2013     4               -2.67                    -5
5  2013     5               -9.37                   -10
6  2013     6               -4.24                    -7
```

To restore the original dplyr methods, call `methods_restore()` or restart the R session.

## Usage for Individual Data Frames

To use DuckDB only for selected data frames, convert them with `as_duckdb_tibble()` and use dplyr as usual. In this case, there is no need to attach `duckplyr`:

```r
library("dplyr")

df <- duckplyr::as_duckdb_tibble(data.frame(n = 1:10))

df |>
  mutate(m = n + 1) |>
  filter(m > 5) |>
  count()
```

The `duckdb_tibble()` function creates a `duckplyr` data frame from columns, similar to `tibble()`. To inspect the DuckDB query plan of a pipeline, use `explain()`.

## Reading and Writing Files

`duckplyr` uses DuckDB's readers to process files without loading them into R's memory first:

* `read_csv_duckdb()` for [CSV files]({% link docs/2.0/data/csv/overview.md %})
* `read_parquet_duckdb()` for [Parquet files]({% link docs/2.0/data/parquet/overview.md %})
* `read_json_duckdb()` for [JSON files]({% link docs/2.0/data/json/overview.md %})
* `read_file_duckdb()` for any other format supported by a DuckDB table function

These functions accept local paths, glob patterns, and URLs. To query remote files, install and load the [`httpfs` extension]({% link docs/2.0/core_extensions/httpfs/overview.md %}) first:

```r
library("duckplyr")

db_exec("INSTALL httpfs")
db_exec("LOAD httpfs")

flights <- read_parquet_duckdb(
  "https://blobs.duckdb.org/flight-data-partitioned/Year=2024/data_0.parquet"
)

flights |>
  count(Reporting_Airline, sort = TRUE) |>
  head(3) |>
  collect()
```

To write the result of a pipeline to a file without materializing it in R, use `compute_parquet()` or `compute_csv()`:

```r
flights |>
  filter(Month == 1) |>
  compute_parquet("flights_january.parquet")
```

The `db_exec()` function runs any SQL statement on the default DuckDB connection used by `duckplyr`, e.g., to [load extensions]({% link docs/2.0/extensions/overview.md %}) or to [change settings]({% link docs/2.0/configuration/overview.md %}).

## Lazy Evaluation and Prudence

Computations in `duckplyr` are lazy: DuckDB only runs the query when the result is accessed, e.g., when it is printed or when a column is accessed. To protect memory, the `prudence` setting controls when a `duckplyr` data frame is materialized automatically:

| Prudence  | Automatic materialization | Default for |
|-----------|---------------------------|-------------|
| `lavish`  | Always | `duckdb_tibble()`, `as_duckdb_tibble()` |
| `thrifty` | Only for small results (up to 1 million cells for local data) | `read_*_duckdb()` functions |
| `stingy`  | Never | – |

When automatic materialization is not allowed, accessing the data, e.g., with `nrow()`, throws an error. In this case, use `collect()` to materialize the result explicitly:

```r
flights |> collect() |> nrow()
```

The prudence level can be set with the `prudence` argument of `as_duckdb_tibble()` and the `read_*_duckdb()` functions. For details, see the [“Memory protection” article](https://duckplyr.tidyverse.org/articles/prudence.html).

## Fallback to dplyr

`duckplyr` supports the most common dplyr verbs and functions. If an operation cannot be translated to DuckDB, `duckplyr` falls back to dplyr transparently, and the result is computed in R. With the `stingy` prudence level, fallbacks are blocked, which ensures that a pipeline runs entirely in DuckDB. To review the fallback status, use `fallback_sitrep()`. For the supported verbs and functions, see the [“Translations” article](https://duckplyr.tidyverse.org/articles/limits.html).

## Further Reading

* [`duckplyr` documentation](https://duckplyr.tidyverse.org/)
* [“duckplyr: dplyr Powered by DuckDB” blog post]({% post_url 2024-04-02-duckplyr %})
* [“Analyzing Open Government Data with duckplyr” blog post]({% post_url 2024-10-09-analyzing-open-government-data-with-duckplyr %})
