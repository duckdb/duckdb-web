# Pragmas
The PRAGMA statement is an SQL extension adopted by DuckDB from SQLite. PRAGMA statements can be issued in a similar manner to regular SQL statements. PRAGMA commands may alter the internal state of the database engine, and can influence the subsequent execution or behavior of the engine.

# List of supported PRAGMA statements
Below is a list of supported PRAGMA statements.


### table_info
```sql
PRAGMA table_info('table_name');
-- equivalent to the following SQL: SELECT * FROM pragma_table_info('table_name');
```

Returns information about the columns of the table with name *table_name*. The exact format of the table returned is given below:

```sql
cid INTEGER,        -- cid of the column
name VARCHAR,       -- name fo the column
type VARCHAR,       -- type of the column
notnull BOOLEAN,    -- if the column is marked as NOT NULL
dflt_value VARCHAR, -- default value of the column, or NULL if not specified
pk BOOLEAN          -- part of the primary key or not
```

### enable_profiling, disable_profiling, profiling_output
```sql
-- enable profiling
PRAGMA enable_profiling
-- enable profiling in a specified format
PRAGMA enable_profiling=[json, query_tree]
-- disable profiling
PRAGMA disable_profiling;
-- specifies a directory to save the profiling output to
PRAGMA profiling_output=/path/to/directory;
```

Enable the gathering and printing of profiling information after the execution of a query. Optionally, the format of the resulting profiling information can be specified as either *json* or *query_tree*. The default format is *query_tree*, which prints the physical operator tree together with the timings and cardinalities of each operator in the tree to the screen.

Below is an example output of the profiling information for the simple query ```SELECT 42```:

```
<<Query Profiling Information>>
SELECT 42;
<<Operator Tree>>
--------------------
|    PROJECTION    |
|        42        |
|      (0.00s)     |
|         1        |
--------------------
--------------------
|    DUMMY_SCAN    |
|      (0.00s)     |
|         1        |
--------------------
```

The printing of profiling information can be disabled again using *disable_profiling*.

By default, profiling information is printed to the console. However, if you prefer to write the profiling information to a file the pragma **profiling_output** can be used to write to a specified file. **Note that the file contents will be overwritten for every new query that is issued, hence the file will only contain the profiling information of the last query that is run.**

