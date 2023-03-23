---
layout: docu
title: R API
selected: Client APIs
---
## Installation
The DuckDB R API can be installed using `install.packages`. Please see the [installation page](../installation?environment=r) for details.

## Basic API Usage
The standard DuckDB R API implements the [DBI interface](https://CRAN.R-project.org/package=DBI) for R. If you are not familiar with DBI yet, see [here for an introduction](https://solutions.rstudio.com/db/r-packages/DBI/).

### Startup & Shutdown

To use DuckDB, you must first create a connection object that represents the database. The connection object takes as parameter the database file to read and write from. If the database file does not exist, it will be created (the file extension may be `.db`, `.duckdb`, or anything else). The special value `:memory:` (the default) can be used to create an **in-memory database**. Note that for an in-memory database no data is persisted to disk (i.e. all data is lost when you exit the R process). If you would like to connect to an existing database in read-only mode, set the `read_only` flag to `TRUE`. Read-only mode is required if multiple R processes want to access the same database file at the same time.

```R
library("DBI")
# to start an in-memory database
con <- dbConnect(duckdb::duckdb(), dbdir = ":memory:")
# to use a database file (not shared between processes)
con <- dbConnect(duckdb::duckdb(), dbdir = "my-db.duckdb", read_only = FALSE)
# to use a database file (shared between processes)
con <- dbConnect(duckdb::duckdb(), dbdir = "my-db.duckdb", read_only = TRUE)
```
Connections are closed implicitly when they go out of scope or if they are explicitly closed using `dbDisconnect()`. To shut down the database instance associated with the connection, use `dbDisconnect(con, shutdown=TRUE)`

### Querying
DuckDB supports the standard DBI methods to send queries and retreive result sets. `dbExecute()` is meant for queries where no results are expected like `CREATE TABLE` or `UPDATE` etc. and `dbGetQuery()` is meant to be used for queries that produce results (e.g. `SELECT`). Below an example.

```R
# create a table
dbExecute(con, "CREATE TABLE items(item VARCHAR, value DECIMAL(10,2), count INTEGER)")
# insert two items into the table
dbExecute(con, "INSERT INTO items VALUES ('jeans', 20.0, 1), ('hammer', 42.2, 2)")

# retrieve the items again
res <- dbGetQuery(con, "SELECT * FROM items")
print(res)
#     item value count
# 1  jeans  20.0     1
# 2 hammer  42.2     2
```


DuckDB also supports prepared statements in the R API with the `dbExecute` and `dbGetQuery` methods. Here is an example:

```R
# prepared statement parameters are given as a list
dbExecute(con, "INSERT INTO items VALUES (?, ?, ?)", list('laptop', 2000, 1))

# if you want to reuse a prepared statement multiple times, use dbSendStatement() and dbBind()
stmt <- dbSendStatement(con, "INSERT INTO items VALUES (?, ?, ?)")
dbBind(stmt, list('iphone', 300, 2))
dbBind(stmt, list('android', 3.5, 1))
dbClearResult(stmt)

# query the database using a prepared statement
res <- dbGetQuery(con, "SELECT item FROM items WHERE value > ?", list(400))
print(res)
#       item
# 1 laptop
```

> Do **not** use prepared statements to insert large amounts of data into DuckDB. See below for better options.

## Efficient Transfer
To write a R data frame into DuckDB, use the standard DBI function `dbWriteTable()`. This creates a table in DuckDB and populates it with the data frame contents. For example:
```R
dbWriteTable(con, "iris_table", iris)
res <- dbGetQuery(con, "SELECT * FROM iris_table LIMIT 1")
print(res)
#   Sepal.Length Sepal.Width Petal.Length Petal.Width Species
# 1          5.1         3.5          1.4         0.2  setosa
```
It is also possible to "register" a R data frame as a virtual table, comparable to a SQL `VIEW`. This *does not actually transfer data* into DuckDB yet. Below is an example:

```R
duckdb::duckdb_register(con, "iris_view", iris)
res <- dbGetQuery(con, "SELECT * FROM iris_view LIMIT 1")
print(res)
#   Sepal.Length Sepal.Width Petal.Length Petal.Width Species
# 1          5.1         3.5          1.4         0.2  setosa
```

> DuckDB keeps a reference to the R data frame after registration. This prevents the data frame from being garbage-collected. The reference is cleared when the connection is closed, but can also be cleared manually using the `duckdb::duckdb_unregister()` method.

Also refer to [the data import documentation](../data/overview) for more options of efficiently importing data.

## dbplyr 
DuckDB also plays well with the [dbplyr](https://CRAN.R-project.org/package=dbplyr) / [dplyr](https://dplyr.tidyverse.org) packages for programmatic query construction from R. Here is an example:

```R
library("DBI")
library("dplyr")
con <- dbConnect(duckdb::duckdb())
duckdb::duckdb_register(con, "flights", nycflights13::flights)

tbl(con, "flights") |>
  group_by(dest) |>
  summarise(delay = mean(dep_time, na.rm = TRUE)) |>
  collect()
```

When using dbplyr, CSV and Parquet files can be read using the `dplyr::tbl` function.

```R
write.csv(mtcars, "mtcars.csv")

tbl(con, "mtcars.csv") |>
  group_by(cyl) |>
  summarise(across(disp:wt, .fns = mean)) |>
  collect()
```
