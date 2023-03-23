---
layout: docu
title: Relational API
selected: Client APIs
---

The Relational API is an alternative API that can be used to incrementally construct queries. The API is centered around `DuckDBPyRelation` nodes. The relations can be seen as symbolic representations of SQL queries. They do not hold any data - and nothing is executed - until a method that triggers execution is called.

#### Constructing Relations
Relations can be created from SQL queries using the `duckdb.sql` method. Alternatively, they can be created from the various data ingestion methods (`read_parquet`, `read_csv`, `read_json`).

For example, here we create a relation from a SQL query:

```py
import duckdb
rel = duckdb.sql('SELECT * FROM range(10000000000) tbl(id)');
rel.show()
```
```
┌────────────────────────┐
│           id           │
│         int64          │
├────────────────────────┤
│                      0 │
│                      1 │
│                      2 │
│                      3 │
│                      4 │
│                      5 │
│                      6 │
│                      7 │
│                      8 │
│                      9 │
│                      · │
│                      · │
│                      · │
│                   9990 │
│                   9991 │
│                   9992 │
│                   9993 │
│                   9994 │
│                   9995 │
│                   9996 │
│                   9997 │
│                   9998 │
│                   9999 │
├────────────────────────┤
│         ? rows         │
│ (>9999 rows, 20 shown) │
└────────────────────────┘
```

Note how we are constructing a relation that computes an immense amount of data (`10B` rows, or `74GB` of data). The relation is constructed instantly - and we can even print the relation instantly.

When printing a relation using `show` or displaying it in the terminal, the first `10K` rows are fetched. If there are more than `10K` rows, the output window will show `>9999 rows` (as the amount of rows in the relation is unknown).

#### Data Ingestion

Outside of SQL queries, the following methods are provided to construct relation objects from external data.

* **from_arrow**
* **from_df**
* **read_csv**
* **read_json**
* **read_parquet**

#### SQL Queries

Relation objects can be queried through SQL through so-called **replacement scans**. If you have a relation object stored in a variable, you can refer to that variable as if it was a SQL table (in the `FROM` clause). This allows you to incrementally build queries using relation objects.

```py
import duckdb
rel = duckdb.sql('SELECT * FROM range(1000000) tbl(id)');
duckdb.sql('SELECT SUM(id) FROM rel').show()
```
```
┌──────────────┐
│   sum(id)    │
│    int128    │
├──────────────┤
│ 499999500000 │
└──────────────┘
```

#### Operations
There are a number of operations that can be performed on relations. These are all short-hand for running the SQL queries - and will return relations again themselves.

##### **aggregate(expr, groups = {})**
Apply an (optionally grouped) aggregate over the relation. The system will automatically group by any columns that are not aggregates.

```py
import duckdb
rel = duckdb.sql('SELECT * FROM range(1000000) tbl(id)');
rel.aggregate('id % 2 AS g, sum(id), min(id), max(id)')
```
```
┌───────┬──────────────┬─────────┬─────────┐
│   g   │   sum(id)    │ min(id) │ max(id) │
│ int64 │    int128    │  int64  │  int64  │
├───────┼──────────────┼─────────┼─────────┤
│     0 │ 249999500000 │       0 │  999998 │
│     1 │ 250000000000 │       1 │  999999 │
└───────┴──────────────┴─────────┴─────────┘
```

##### **except_(rel)**
Select all rows in the first relation, that do not occur in the second relation. The relations must have the same number of columns.

```py
import duckdb
r1 = duckdb.sql('SELECT * FROM range(10) tbl(id)');
r2 = duckdb.sql('SELECT * FROM range(5) tbl(id)');
r1.except_(r2).show()
```
```
┌───────┐
│  id   │
│ int64 │
├───────┤
│     5 │
│     6 │
│     7 │
│     8 │
│     9 │
└───────┘
```

##### **filter(condition)**

Apply the given condition to the relation, filtering any rows that do not satisfy the condition.

```py
import duckdb
rel = duckdb.sql('SELECT * FROM range(1000000) tbl(id)');
rel.filter('id > 5').limit(3).show()
```
```
┌───────┐
│  id   │
│ int64 │
├───────┤
│     6 │
│     7 │
│     8 │
└───────┘
```

##### **intersect(rel)**
Select the intersection of two relations - returning all rows that occur in both relations. The relations must have the same number of columns.

```py
import duckdb
r1 = duckdb.sql('SELECT * FROM range(10) tbl(id)');
r2 = duckdb.sql('SELECT * FROM range(5) tbl(id)');
r1.intersect(r2).show()
```
```
┌───────┐
│  id   │
│ int64 │
├───────┤
│     0 │
│     1 │
│     2 │
│     3 │
│     4 │
└───────┘
```

##### **join(rel, condition, type = 'inner')**
Combine two relations, joining them based on the provided condition. 

```py
import duckdb
r1 = duckdb.sql('SELECT * FROM range(5) tbl(id)').set_alias('r1');
r2 = duckdb.sql('SELECT * FROM range(10, 15) tbl(id)').set_alias('r2');
r1.join(r2, 'r1.id + 10 = r2.id').show()
```
```
┌───────┬───────┐
│  id   │  id   │
│ int64 │ int64 │
├───────┼───────┤
│     0 │    10 │
│     1 │    11 │
│     2 │    12 │
│     3 │    13 │
│     4 │    14 │
└───────┴───────┘
```

##### **limit(n, offset = 0)**

Select the first *n* rows, optionally offset by *offset*.

```py
import duckdb
rel = duckdb.sql('SELECT * FROM range(1000000) tbl(id)');
rel.limit(3).show()
```
```
┌───────┐
│  id   │
│ int64 │
├───────┤
│     0 │
│     1 │
│     2 │
└───────┘
```

##### **order(expr)**

Sort the relation by the given set of expressions.

```py
import duckdb
rel = duckdb.sql('SELECT * FROM range(1000000) tbl(id)');
rel.order('id DESC').limit(3).show()
```
```
┌────────┐
│   id   │
│ int64  │
├────────┤
│ 999999 │
│ 999998 │
│ 999997 │
└────────┘
```

##### **project(expr)**

Apply the given expression to each row in the relation.

```py
import duckdb
rel = duckdb.sql('SELECT * FROM range(1000000) tbl(id)');
rel.project('id + 10 AS id_plus_ten').limit(3).show()
```
```
┌─────────────┐
│ id_plus_ten │
│    int64    │
├─────────────┤
│          10 │
│          11 │
│          12 │
└─────────────┘
```

##### **union(rel)**
Combine two relations, returning all rows in `r1` followed by all rows in `r2`. The relations must have the same number of columns.

```py
import duckdb
r1 = duckdb.sql('SELECT * FROM range(5) tbl(id)');
r2 = duckdb.sql('SELECT * FROM range(10, 15) tbl(id)');
r1.union(r2).show()
```
```
┌───────┐
│  id   │
│ int64 │
├───────┤
│     0 │
│     1 │
│     2 │
│     3 │
│     4 │
│    10 │
│    11 │
│    12 │
│    13 │
│    14 │
└───────┘
```


#### Result Output
The result of relations can be converted to various types of Python structures, see the [result conversion page](result_conversion) for more information.

The result of relations can also be directly written to files using the below methods.

* **write_csv**
* **write_parquet**
