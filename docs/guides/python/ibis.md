---
layout: docu
title: DuckDB with Ibis
selected: DuckDB with Ibis
---

[Ibis](https://ibis-project.org/) is a Python library that allows queries to be written in a pythonic relational style and then be compiled into SQL.
Ibis supports multiple database backends, including [DuckDB](https://ibis-project.org/docs/dev/backends/DuckDB/) by using [DuckDB's SQLAlchemy driver](https://github.com/Mause/duckdb_engine). 

# Installation
To install only the DuckDB backend for Ibis, use the commands below. See the [Ibis DuckDB installation instructions](https://ibis-project.org/docs/dev/backends/DuckDB/) for a conda alternative. Note that DuckDB support was added in Ibis version 3.0.0.
```python
pip install 'ibis-framework[duckdb]' # duckdb, sqlalchemy, duckdb_engine and more are installed as dependencies
```

# Querying DuckDB with Ibis
The following example is loosely borrowed from the [Introduction to Ibis tutorial](https://ibis-project.org/docs/dev/tutorial/01-Introduction-to-Ibis/), which uses SQLite.  
First, we import Ibis, set it to interactive mode (just for demo purposes - it is faster to not use this option!), and then connect to an in-memory DuckDB instance. We can then inspect the tables in our database. 

```python
import ibis
ibis.options.interactive = True # Use eager evaluation. Use only for demo purposes!

connection = ibis.duckdb.connect(':memory:') # Use an In Memory DuckDB
# connection = ibis.duckdb.connect('/path/to/my_db.db') # Use or create a physical DuckDB at this path

print(connection.list_tables())
```
```python
# Output:
['pragma_database_list', 'duckdb_tables', 'duckdb_views', 'duckdb_indexes',
 'sqlite_master', 'sqlite_schema', 'sqlite_temp_master', 'sqlite_temp_schema', 
 'duckdb_constraints', 'duckdb_columns', 'duckdb_schemas', 'duckdb_types']
```
We then create a handler to a specific table to be able to explore it further. Here we use a built in table called duckdb_types for simplicity. The first thing we want to see is a list of columns.
```python
duckdb_types_table = connection.table('duckdb_types')
print(duckdb_types_table.columns)
```
```python
# Output:
['schema_name', 'schema_oid', 'type_oid', 'type_name', 'type_size', 'type_category', 'internal']
```
To access only certain columns, use bracket syntax on the table handler. We can also apply functions to transform the data, for example to show only distinct values. Use the `compile` function to see the SQL query that Ibis generates.
```python
print(duckdb_types_table['type_category', 'type_size'].distinct())
print(duckdb_types_table['type_category', 'type_size'].distinct().compile())
```

| type_category | type_size |
|---------------|-----------|
| BOOLEAN       | 1         |
| NUMERIC       | 1         |
| NUMERIC       | 2         |
| NUMERIC       | 4         |
| NUMERIC       | 8         |
| DATETIME      | 4         |
| DATETIME      | 8         |
| STRING        | 16        |
| NaN           | 16        |
| DATETIME      | 16        |
| NUMERIC       | 16        |
| COMPOSITE     | 16        |
| COMPOSITE     | 0         |
| NUMERIC       | NaN       |

```sql
SELECT DISTINCT t0.type_category, t0.type_size 
FROM duckdb_types AS t0
```

Multiple methods can be chained together to build up more complex expressions. This statement selects a subset of columns, filters to rows containing a specific value in one column, and sorts by another column. The Ibis-generated SQL is shown below. Note that it uses a parameter as a part of the filter function.

```python
print(duckdb_types_table['type_name','type_category', 'type_size']
    .filter(duckdb_types_table['type_category'] == 'NUMERIC')
    .sort_by('type_size'))

print(duckdb_types_table['type_name','type_category', 'type_size']
    .filter(duckdb_types_table['type_category'] == 'NUMERIC')
    .sort_by('type_size').compile())
```

| type_name | type_category | type_size |
|-----------|---------------|-----------|
| DECIMAL   | NUMERIC       | NaN       |
| TINYINT   | NUMERIC       | 1         |
| UTINYINT  | NUMERIC       | 1         |
| SMALLINT  | NUMERIC       | 2         |
| USMALLINT | NUMERIC       | 2         |
| INTEGER   | NUMERIC       | 4         |
| FLOAT     | NUMERIC       | 4         |
| UINTEGER  | NUMERIC       | 4         |
| BIGINT    | NUMERIC       | 8         |
| DOUBLE    | NUMERIC       | 8         |
| UBIGINT   | NUMERIC       | 8         |
| HUGEINT   | NUMERIC       | 16        |

```sql
SELECT t0.type_name, t0.type_category, t0.type_size 
FROM (SELECT t1.type_name AS type_name, t1.type_category AS type_category, t1.type_size AS type_size 
FROM duckdb_types AS t1 
WHERE t1.type_category = CAST(? AS TEXT)) AS t0 ORDER BY t0.type_size
```
# Combining SQL and Ibis Expressions

Ibis can also be used to combine SQL and relational operators. SQL can precede or follow Ibis relational operations. 

```python
print(duckdb_types_table.sql("""
    SELECT 
        *,
        dense_rank() over (order by type_size) as size_rank 
    FROM duckdb_types""")
    .group_by('type_category')   
    .aggregate(avg_size_rank=lambda t:t.size_rank.mean())

print(duckdb_types_table.sql("""
    SELECT 
        *,
        dense_rank() over (order by type_size) as size_rank 
    FROM duckdb_types""")
    .group_by('type_category')   
    .aggregate(avg_size_rank=lambda t:t.size_rank.mean()).compile())
```  

| type_category |   avg_size_rank    |
|---------------|--------------------|
| NUMERIC       | 4.583333333333333  |
| COMPOSITE     | 3.6666666666666665 |
| BOOLEAN       | 3.0                |
| DATETIME      | 6.0                |
| STRING        | 7.0                |
| NaN           | 7.0                |

```sql
WITH _ibis_view_11 AS 
(
    SELECT 
        *,
        dense_rank() over (order by type_size) as size_rank 
    FROM duckdb_types)
 SELECT t0.type_category, avg(t0.size_rank) AS avg_size_rank 
FROM _ibis_view_11 AS t0 GROUP BY t0.type_category
```

To learn more about Ibis, feel free to continue with the [Ibis introductory tutorial](https://ibis-project.org/docs/dev/tutorial/02-Aggregates-Joins/)! 