---
layout: docu
title: Julia Package
---

The DuckDB Julia package provides a high-performance front-end for DuckDB. Much like SQLite, DuckDB runs in-process within the Julia client, and provides a DBInterface front-end.

The package also supports multi-threaded execution. It uses Julia threads/tasks for this purpose. If you wish to run queries in parallel, you must launch Julia with multi-threading support (by e.g., setting the `JULIA_NUM_THREADS` environment variable).

## Installation

Install DuckDB as follows:

```julia
using Pkg
Pkg.add("DuckDB")
```

Alternatively, enter the package manager using the `]` key, and issue the following command:

```julia
pkg> add DuckDB
```

## Basics

```julia
using DuckDB

# create a new in-memory database
con = DBInterface.connect(DuckDB.DB, ":memory:")

# create a table
DBInterface.execute(con, "CREATE TABLE integers (i INTEGER)")

# insert data using a prepared statement
stmt = DBInterface.prepare(con, "INSERT INTO integers VALUES(?)")
DBInterface.execute(stmt, [42])

# query the database
results = DBInterface.execute(con, "SELECT 42 a")
print(results)
```

## Scanning DataFrames

The DuckDB Julia package also provides support for querying Julia DataFrames. Note that the DataFrames are directly read by DuckDB - they are not inserted or copied into the database itself.

If you wish to load data from a DataFrame into a DuckDB table you can run a `CREATE TABLE ... AS` or `INSERT INTO` query.

```julia
using DuckDB
using DataFrames

# create a new in-memory dabase
con = DBInterface.connect(DuckDB.DB)

# create a DataFrame
df = DataFrame(a = [1, 2, 3], b = [42, 84, 42])

# register it as a view in the database
DuckDB.register_data_frame(con, df, "my_df")

# run a SQL query over the DataFrame
results = DBInterface.execute(con, "SELECT * FROM my_df")
print(results)
```

## Appender API

The DuckDB Julia package also supports the Appender api, which is much faster than using prepared statements or individual INSERT INTO statements.  Appends are made in row-wise format. For every column, an append() call should be made, after which the row should be finished by calling flush(). After all rows have been appended, close() should be used to finalize the appender and clean up the resulting memory.

```julia
using DuckDB, DataFrames, Dates
db = DuckDB.DB()
# create a table
DBInterface.execute(db, "CREATE OR REPLACE
                         TABLE data(id INT PRIMARY KEY, value FLOAT,
                         timestamp TIMESTAMP, date DATE)")
# create data to insert
len = 100
df = DataFrames.DataFrame(id=collect(1:len),
    value=rand(len),
    timestamp=Dates.now() + Dates.Second.(1:len),
    date=Dates.today() + Dates.Day.(1:len))
# append data by row
appender = DuckDB.Appender(db, "data")
for i in eachrow(df)
    for j in i
        DuckDB.append(appender, j)
    end
    DuckDB.end_row(appender)
end
# flush the appender after all rows
DuckDB.flush(appender)
DuckDB.close(appender)
```

## Concurrency

Within a julia process, tasks are able to concurrently read and write to the database, as long as each task maintains its own connection to the database.  In the example below, a single task is spawned to periodically read the database and many tasks are spawned to write to the database using both INSERT statements as well as the appender api.

```julia
using Dates, DataFrames, DuckDB
db = DuckDB.DB()
DBInterface.connect(db)
DBInterface.execute(db, "CREATE OR REPLACE TABLE data (date TIMESTAMP, id INT)")

function run_reader(db)
    # create a DuckDB connection specifically for this task
    conn = DBInterface.connect(db)
    while true
        println(DBInterface.execute(conn,
                "SELECT id, count(date) as count, max(date) as max_date
                FROM data group by id order by id") |> DataFrames.DataFrame)
        Threads.sleep(1)
    end
    DBInterface.close(conn)
end
# spawn one reader task
Threads.@spawn run_reader(db)

function run_inserter(db, id)
    # create a DuckDB connection specifically for this task
    conn = DBInterface.connect(db)
    for i in 1:1000
        Threads.sleep(0.01)
        DuckDB.execute(conn, "INSERT INTO data VALUES (current_timestamp, ?)"; id);
    end
    DBInterface.close(conn)
end
# spawn many insert tasks
for i in 1:100
    Threads.@spawn run_inserter(db, 1)
end

function run_appender(db, id)
    # create a DuckDB connection specifically for this task
    appender = DuckDB.Appender(db, "data")
    for i in 1:1000
        Threads.sleep(0.01)
        row = (Dates.now(Dates.UTC), id)
        for j in row
            DuckDB.append(appender, j);
        end
        DuckDB.end_row(appender);
        DuckDB.flush(appender);
    end
    DuckDB.close(appender);
end
# spawn many appender tasks
for i in 1:100
    Threads.@spawn run_appender(db, 2)
end
```

## Original Julia Connector

Credits to kimmolinna for the [original DuckDB Julia connector](https://github.com/kimmolinna/DuckDB.jl).
