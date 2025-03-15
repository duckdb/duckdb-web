---
layout: docu
redirect_from:
- /docs/api/python/reference/index
- /docs/api/python/reference/index/
- /docs/clients/python/reference/index
title: Python Client API
---

The API reference documentations is structured as follows:

1. [DuckDB Class Methods](#class-duckdb)
2. [DuckDBPyConnection](#duckdbpyconnection)
3. [DuckDBPyRelation](#duckdbpyrelation)
4. [Expressions](#expressions)
5. [Values](#values)
6. [Exceptions](#exceptions)



## Class duckdb


### aggregate

aggregate(df: pandas.DataFrame, aggr_expr: object, group_expr: str = '', *, connection: duckdb.DuckDBPyConnection = None) -> duckdb.duckdb.DuckDBPyRelation

Compute the aggregate aggr_expr by the optional groups group_expr on the relation

**Type**: builtin_function_or_method





### alias

alias(df: pandas.DataFrame, alias: str, *, connection: duckdb.DuckDBPyConnection = None) -> duckdb.duckdb.DuckDBPyRelation

Rename the relation object to new alias

**Type**: builtin_function_or_method





### append

append(table_name: str, df: pandas.DataFrame, *, by_name: bool = False, connection: duckdb.DuckDBPyConnection = None) -> duckdb.DuckDBPyConnection

Append the passed DataFrame to the named table

**Type**: builtin_function_or_method





### array_type

array_type(type: duckdb.duckdb.typing.DuckDBPyType, size: int, *, connection: duckdb.DuckDBPyConnection = None) -> duckdb.duckdb.typing.DuckDBPyType

Create an array type object of 'type'

**Type**: builtin_function_or_method





### arrow

arrow(*args, **kwargs)
Overloaded function.

1. arrow(rows_per_batch: int = 1000000, *, connection: duckdb.DuckDBPyConnection = None) -> pyarrow.lib.Table

Fetch a result as Arrow table following execute()

2. arrow(rows_per_batch: int = 1000000, *, connection: duckdb.DuckDBPyConnection = None) -> pyarrow.lib.Table

Fetch a result as Arrow table following execute()

3. arrow(arrow_object: object, *, connection: duckdb.DuckDBPyConnection = None) -> duckdb.duckdb.DuckDBPyRelation

Create a relation object from an Arrow object

**Type**: builtin_function_or_method





### begin

begin(*, connection: duckdb.DuckDBPyConnection = None) -> duckdb.DuckDBPyConnection

Start a new transaction

**Type**: builtin_function_or_method





### checkpoint

checkpoint(*, connection: duckdb.DuckDBPyConnection = None) -> duckdb.DuckDBPyConnection

Synchronizes data in the write-ahead log (WAL) to the database data file (no-op for in-memory connections)

**Type**: builtin_function_or_method





### close

close(*, connection: duckdb.DuckDBPyConnection = None) -> None

Close the connection

**Type**: builtin_function_or_method





### commit

commit(*, connection: duckdb.DuckDBPyConnection = None) -> duckdb.DuckDBPyConnection

Commit changes performed within a transaction

**Type**: builtin_function_or_method





### connect

connect(database: object = ':memory:', read_only: bool = False, config: dict = None) -> duckdb.DuckDBPyConnection

Create a DuckDB database instance. Can take a database file name to read/write persistent data and a read_only flag if no changes are desired

**Type**: builtin_function_or_method





### create_function

create_function(name: str, function: Callable, parameters: object = None, return_type: duckdb.duckdb.typing.DuckDBPyType = None, *, type: duckdb.duckdb.functional.PythonUDFType = <PythonUDFType.NATIVE: 0>, null_handling: duckdb.duckdb.functional.FunctionNullHandling = <FunctionNullHandling.DEFAULT: 0>, exception_handling: duckdb.duckdb.PythonExceptionHandling = <PythonExceptionHandling.DEFAULT: 0>, side_effects: bool = False, connection: duckdb.DuckDBPyConnection = None) -> duckdb.DuckDBPyConnection

Create a DuckDB function out of the passing in Python function so it can be used in queries

**Type**: builtin_function_or_method





### cursor

cursor(*, connection: duckdb.DuckDBPyConnection = None) -> duckdb.DuckDBPyConnection

Create a duplicate of the current connection

**Type**: builtin_function_or_method





### decimal_type

decimal_type(width: int, scale: int, *, connection: duckdb.DuckDBPyConnection = None) -> duckdb.duckdb.typing.DuckDBPyType

Create a decimal type with 'width' and 'scale'

**Type**: builtin_function_or_method





### default_connection

default_connection() -> duckdb.DuckDBPyConnection

Retrieve the connection currently registered as the default to be used by the module

**Type**: builtin_function_or_method





### description

description(*, connection: duckdb.DuckDBPyConnection = None) -> typing.Optional[list]

Get result set attributes, mainly column names

**Type**: builtin_function_or_method





### df

df(*args, **kwargs)
Overloaded function.

1. df(*, date_as_object: bool = False, connection: duckdb.DuckDBPyConnection = None) -> pandas.DataFrame

Fetch a result as DataFrame following execute()

2. df(*, date_as_object: bool = False, connection: duckdb.DuckDBPyConnection = None) -> pandas.DataFrame

Fetch a result as DataFrame following execute()

3. df(df: pandas.DataFrame, *, connection: duckdb.DuckDBPyConnection = None) -> duckdb.duckdb.DuckDBPyRelation

Create a relation object from the DataFrame df

**Type**: builtin_function_or_method





### distinct

distinct(df: pandas.DataFrame, *, connection: duckdb.DuckDBPyConnection = None) -> duckdb.duckdb.DuckDBPyRelation

Retrieve distinct rows from this relation object

**Type**: builtin_function_or_method





### dtype

dtype(type_str: str, *, connection: duckdb.DuckDBPyConnection = None) -> duckdb.duckdb.typing.DuckDBPyType

Create a type object by parsing the 'type_str' string

**Type**: builtin_function_or_method





### duplicate

duplicate(*, connection: duckdb.DuckDBPyConnection = None) -> duckdb.DuckDBPyConnection

Create a duplicate of the current connection

**Type**: builtin_function_or_method





### enum_type

enum_type(name: str, type: duckdb.duckdb.typing.DuckDBPyType, values: list, *, connection: duckdb.DuckDBPyConnection = None) -> duckdb.duckdb.typing.DuckDBPyType

Create an enum type of underlying 'type', consisting of the list of 'values'

**Type**: builtin_function_or_method





### execute

execute(query: object, parameters: object = None, *, connection: duckdb.DuckDBPyConnection = None) -> duckdb.DuckDBPyConnection

Execute the given SQL query, optionally using prepared statements with parameters set

**Type**: builtin_function_or_method





### executemany

executemany(query: object, parameters: object = None, *, connection: duckdb.DuckDBPyConnection = None) -> duckdb.DuckDBPyConnection

Execute the given prepared statement multiple times using the list of parameter sets in parameters

**Type**: builtin_function_or_method





### extract_statements

extract_statements(query: str, *, connection: duckdb.DuckDBPyConnection = None) -> list

Parse the query string and extract the Statement object(s) produced

**Type**: builtin_function_or_method





### fetch_arrow_table

fetch_arrow_table(rows_per_batch: int = 1000000, *, connection: duckdb.DuckDBPyConnection = None) -> pyarrow.lib.Table

Fetch a result as Arrow table following execute()

**Type**: builtin_function_or_method





### fetch_df

fetch_df(*, date_as_object: bool = False, connection: duckdb.DuckDBPyConnection = None) -> pandas.DataFrame

Fetch a result as DataFrame following execute()

**Type**: builtin_function_or_method





### fetch_df_chunk

fetch_df_chunk(vectors_per_chunk: int = 1, *, date_as_object: bool = False, connection: duckdb.DuckDBPyConnection = None) -> pandas.DataFrame

Fetch a chunk of the result as DataFrame following execute()

**Type**: builtin_function_or_method





### fetch_record_batch

fetch_record_batch(rows_per_batch: int = 1000000, *, connection: duckdb.DuckDBPyConnection = None) -> pyarrow.lib.RecordBatchReader

Fetch an Arrow RecordBatchReader following execute()

**Type**: builtin_function_or_method





### fetchall

fetchall(*, connection: duckdb.DuckDBPyConnection = None) -> list

Fetch all rows from a result following execute

**Type**: builtin_function_or_method





### fetchdf

fetchdf(*, date_as_object: bool = False, connection: duckdb.DuckDBPyConnection = None) -> pandas.DataFrame

Fetch a result as DataFrame following execute()

**Type**: builtin_function_or_method





### fetchmany

fetchmany(size: int = 1, *, connection: duckdb.DuckDBPyConnection = None) -> list

Fetch the next set of rows from a result following execute

**Type**: builtin_function_or_method





### fetchnumpy

fetchnumpy(*, connection: duckdb.DuckDBPyConnection = None) -> dict

Fetch a result as list of NumPy arrays following execute

**Type**: builtin_function_or_method





### fetchone

fetchone(*, connection: duckdb.DuckDBPyConnection = None) -> typing.Optional[tuple]

Fetch a single row from a result following execute

**Type**: builtin_function_or_method





### filesystem_is_registered

filesystem_is_registered(name: str, *, connection: duckdb.DuckDBPyConnection = None) -> bool

Check if a filesystem with the provided name is currently registered

**Type**: builtin_function_or_method





### filter

filter(df: pandas.DataFrame, filter_expr: object, *, connection: duckdb.DuckDBPyConnection = None) -> duckdb.duckdb.DuckDBPyRelation

Filter the relation object by the filter in filter_expr

**Type**: builtin_function_or_method





### from_arrow

from_arrow(arrow_object: object, *, connection: duckdb.DuckDBPyConnection = None) -> duckdb.duckdb.DuckDBPyRelation

Create a relation object from an Arrow object

**Type**: builtin_function_or_method





### from_csv_auto

from_csv_auto(path_or_buffer: object, **kwargs) -> duckdb.duckdb.DuckDBPyRelation

Create a relation object from the CSV file in 'name'

**Type**: builtin_function_or_method





### from_df

from_df(df: pandas.DataFrame, *, connection: duckdb.DuckDBPyConnection = None) -> duckdb.duckdb.DuckDBPyRelation

Create a relation object from the DataFrame in df

**Type**: builtin_function_or_method





### from_parquet

from_parquet(*args, **kwargs)
Overloaded function.

1. from_parquet(file_glob: str, binary_as_string: bool = False, *, file_row_number: bool = False, filename: bool = False, hive_partitioning: bool = False, union_by_name: bool = False, compression: object = None, connection: duckdb.DuckDBPyConnection = None) -> duckdb.duckdb.DuckDBPyRelation

Create a relation object from the Parquet files in file_glob

2. from_parquet(file_globs: list[str], binary_as_string: bool = False, *, file_row_number: bool = False, filename: bool = False, hive_partitioning: bool = False, union_by_name: bool = False, compression: object = None, connection: duckdb.DuckDBPyConnection = None) -> duckdb.duckdb.DuckDBPyRelation

Create a relation object from the Parquet files in file_globs

**Type**: builtin_function_or_method





### from_query

from_query(query: object, *, alias: str = '', params: object = None, connection: duckdb.DuckDBPyConnection = None) -> duckdb.duckdb.DuckDBPyRelation

Run a SQL query. If it is a SELECT statement, create a relation object from the given SQL query, otherwise run the query as-is.

**Type**: builtin_function_or_method





### get_table_names

get_table_names(query: str, *, connection: duckdb.DuckDBPyConnection = None) -> set[str]

Extract the required table names from a query

**Type**: builtin_function_or_method





### install_extension

install_extension(extension: str, *, force_install: bool = False, repository: object = None, repository_url: object = None, version: object = None, connection: duckdb.DuckDBPyConnection = None) -> None

Install an extension by name, with an optional version and/or repository to get the extension from

**Type**: builtin_function_or_method





### interrupt

interrupt(*, connection: duckdb.DuckDBPyConnection = None) -> None

Interrupt pending operations

**Type**: builtin_function_or_method





### limit

limit(df: pandas.DataFrame, n: int, offset: int = 0, *, connection: duckdb.DuckDBPyConnection = None) -> duckdb.duckdb.DuckDBPyRelation

Only retrieve the first n rows from this relation object, starting at offset

**Type**: builtin_function_or_method





### list_filesystems

list_filesystems(*, connection: duckdb.DuckDBPyConnection = None) -> list

List registered filesystems, including builtin ones

**Type**: builtin_function_or_method





### list_type

list_type(type: duckdb.duckdb.typing.DuckDBPyType, *, connection: duckdb.DuckDBPyConnection = None) -> duckdb.duckdb.typing.DuckDBPyType

Create a list type object of 'type'

**Type**: builtin_function_or_method





### load_extension

load_extension(extension: str, *, connection: duckdb.DuckDBPyConnection = None) -> None

Load an installed extension

**Type**: builtin_function_or_method





### map_type

map_type(key: duckdb.duckdb.typing.DuckDBPyType, value: duckdb.duckdb.typing.DuckDBPyType, *, connection: duckdb.DuckDBPyConnection = None) -> duckdb.duckdb.typing.DuckDBPyType

Create a map type object from 'key_type' and 'value_type'

**Type**: builtin_function_or_method





### order

order(df: pandas.DataFrame, order_expr: str, *, connection: duckdb.DuckDBPyConnection = None) -> duckdb.duckdb.DuckDBPyRelation

Reorder the relation object by order_expr

**Type**: builtin_function_or_method





### pl

pl(rows_per_batch: int = 1000000, *, connection: duckdb.DuckDBPyConnection = None) -> duckdb::PolarsDataFrame

Fetch a result as Polars DataFrame following execute()

**Type**: builtin_function_or_method





### project

project(df: pandas.DataFrame, *args, groups: str = '', connection: duckdb.DuckDBPyConnection = None) -> duckdb.duckdb.DuckDBPyRelation

Project the relation object by the projection in project_expr

**Type**: builtin_function_or_method





### query

query(query: object, *, alias: str = '', params: object = None, connection: duckdb.DuckDBPyConnection = None) -> duckdb.duckdb.DuckDBPyRelation

Run a SQL query. If it is a SELECT statement, create a relation object from the given SQL query, otherwise run the query as-is.

**Type**: builtin_function_or_method





### query_df

query_df(df: pandas.DataFrame, virtual_table_name: str, sql_query: str, *, connection: duckdb.DuckDBPyConnection = None) -> duckdb.duckdb.DuckDBPyRelation

Run the given SQL query in sql_query on the view named virtual_table_name that refers to the relation object

**Type**: builtin_function_or_method





### read_csv

read_csv(path_or_buffer: object, **kwargs) -> duckdb.duckdb.DuckDBPyRelation

Create a relation object from the CSV file in 'name'

**Type**: builtin_function_or_method





### read_json

read_json(path_or_buffer: object, *, columns: typing.Optional[object] = None, sample_size: typing.Optional[object] = None, maximum_depth: typing.Optional[object] = None, records: typing.Optional[str] = None, format: typing.Optional[str] = None, date_format: typing.Optional[object] = None, timestamp_format: typing.Optional[object] = None, compression: typing.Optional[object] = None, maximum_object_size: typing.Optional[object] = None, ignore_errors: typing.Optional[object] = None, convert_strings_to_integers: typing.Optional[object] = None, field_appearance_threshold: typing.Optional[object] = None, map_inference_threshold: typing.Optional[object] = None, maximum_sample_files: typing.Optional[object] = None, filename: typing.Optional[object] = None, hive_partitioning: typing.Optional[object] = None, union_by_name: typing.Optional[object] = None, hive_types: typing.Optional[object] = None, hive_types_autocast: typing.Optional[object] = None, connection: duckdb.DuckDBPyConnection = None) -> duckdb.duckdb.DuckDBPyRelation

Create a relation object from the JSON file in 'name'

**Type**: builtin_function_or_method





### read_parquet

read_parquet(*args, **kwargs)
Overloaded function.

1. read_parquet(file_glob: str, binary_as_string: bool = False, *, file_row_number: bool = False, filename: bool = False, hive_partitioning: bool = False, union_by_name: bool = False, compression: object = None, connection: duckdb.DuckDBPyConnection = None) -> duckdb.duckdb.DuckDBPyRelation

Create a relation object from the Parquet files in file_glob

2. read_parquet(file_globs: list[str], binary_as_string: bool = False, *, file_row_number: bool = False, filename: bool = False, hive_partitioning: bool = False, union_by_name: bool = False, compression: object = None, connection: duckdb.DuckDBPyConnection = None) -> duckdb.duckdb.DuckDBPyRelation

Create a relation object from the Parquet files in file_globs

**Type**: builtin_function_or_method





### register

register(view_name: str, python_object: object, *, connection: duckdb.DuckDBPyConnection = None) -> duckdb.DuckDBPyConnection

Register the passed Python Object value for querying with a view

**Type**: builtin_function_or_method





### register_filesystem

register_filesystem(filesystem: fsspec.AbstractFileSystem, *, connection: duckdb.DuckDBPyConnection = None) -> None

Register a fsspec compliant filesystem

**Type**: builtin_function_or_method





### remove_function

remove_function(name: str, *, connection: duckdb.DuckDBPyConnection = None) -> duckdb.DuckDBPyConnection

Remove a previously created function

**Type**: builtin_function_or_method





### rollback

rollback(*, connection: duckdb.DuckDBPyConnection = None) -> duckdb.DuckDBPyConnection

Roll back changes performed within a transaction

**Type**: builtin_function_or_method





### row_type

row_type(fields: object, *, connection: duckdb.DuckDBPyConnection = None) -> duckdb.duckdb.typing.DuckDBPyType

Create a struct type object from 'fields'

**Type**: builtin_function_or_method





### rowcount

rowcount(*, connection: duckdb.DuckDBPyConnection = None) -> int

Get result set row count

**Type**: builtin_function_or_method





### set_default_connection

set_default_connection(connection: duckdb.DuckDBPyConnection) -> None

Register the provided connection as the default to be used by the module

**Type**: builtin_function_or_method





### sql

sql(query: object, *, alias: str = '', params: object = None, connection: duckdb.DuckDBPyConnection = None) -> duckdb.duckdb.DuckDBPyRelation

Run a SQL query. If it is a SELECT statement, create a relation object from the given SQL query, otherwise run the query as-is.

**Type**: builtin_function_or_method





### sqltype

sqltype(type_str: str, *, connection: duckdb.DuckDBPyConnection = None) -> duckdb.duckdb.typing.DuckDBPyType

Create a type object by parsing the 'type_str' string

**Type**: builtin_function_or_method





### string_type

string_type(collation: str = '', *, connection: duckdb.DuckDBPyConnection = None) -> duckdb.duckdb.typing.DuckDBPyType

Create a string type with an optional collation

**Type**: builtin_function_or_method





### struct_type

struct_type(fields: object, *, connection: duckdb.DuckDBPyConnection = None) -> duckdb.duckdb.typing.DuckDBPyType

Create a struct type object from 'fields'

**Type**: builtin_function_or_method





### table

table(table_name: str, *, connection: duckdb.DuckDBPyConnection = None) -> duckdb.duckdb.DuckDBPyRelation

Create a relation object for the named table

**Type**: builtin_function_or_method





### table_function

table_function(name: str, parameters: object = None, *, connection: duckdb.DuckDBPyConnection = None) -> duckdb.duckdb.DuckDBPyRelation

Create a relation object from the named table function with given parameters

**Type**: builtin_function_or_method





### tf

tf(*, connection: duckdb.DuckDBPyConnection = None) -> dict

Fetch a result as dict of TensorFlow Tensors following execute()

**Type**: builtin_function_or_method





### tokenize

tokenize(query: str) -> list

Tokenizes a SQL string, returning a list of (position, type) tuples that can be used for e.g., syntax highlighting

**Type**: builtin_function_or_method





### torch

torch(*, connection: duckdb.DuckDBPyConnection = None) -> dict

Fetch a result as dict of PyTorch Tensors following execute()

**Type**: builtin_function_or_method





### type

type(type_str: str, *, connection: duckdb.DuckDBPyConnection = None) -> duckdb.duckdb.typing.DuckDBPyType

Create a type object by parsing the 'type_str' string

**Type**: builtin_function_or_method





### union_type

union_type(members: object, *, connection: duckdb.DuckDBPyConnection = None) -> duckdb.duckdb.typing.DuckDBPyType

Create a union type object from 'members'

**Type**: builtin_function_or_method





### unregister

unregister(view_name: str, *, connection: duckdb.DuckDBPyConnection = None) -> duckdb.DuckDBPyConnection

Unregister the view name

**Type**: builtin_function_or_method





### unregister_filesystem

unregister_filesystem(name: str, *, connection: duckdb.DuckDBPyConnection = None) -> None

Unregister a filesystem

**Type**: builtin_function_or_method





### values

values(*args, connection: duckdb.DuckDBPyConnection = None) -> duckdb.duckdb.DuckDBPyRelation

Create a relation object from the passed values

**Type**: builtin_function_or_method





### view

view(view_name: str, *, connection: duckdb.DuckDBPyConnection = None) -> duckdb.duckdb.DuckDBPyRelation

Create a relation object for the named view

**Type**: builtin_function_or_method





### write_csv

write_csv(df: pandas.DataFrame, filename: str, *, sep: object = None, na_rep: object = None, header: object = None, quotechar: object = None, escapechar: object = None, date_format: object = None, timestamp_format: object = None, quoting: object = None, encoding: object = None, compression: object = None, overwrite: object = None, per_thread_output: object = None, use_tmp_file: object = None, partition_by: object = None, write_partition_columns: object = None, connection: duckdb.DuckDBPyConnection = None) -> None

Write the relation object to a CSV file in 'file_name'

**Type**: builtin_function_or_method





## ANALYZE

Members:

INVALID

SELECT

INSERT

UPDATE

CREATE

DELETE

PREPARE

EXECUTE

ALTER

TRANSACTION

COPY

ANALYZE

VARIABLE_SET

CREATE_FUNC

EXPLAIN

DROP

EXPORT

PRAGMA

VACUUM

CALL

SET

LOAD

RELATION

EXTENSION

LOGICAL_PLAN

ATTACH

DETACH

MULTI

COPY_DATABASE

**Type**: StatementType





## COLUMNS

Members:

ROWS

COLUMNS

**Type**: RenderMode





## CSVLineTerminator

Members:

LINE_FEED

CARRIAGE_RETURN_LINE_FEED

**Type**: pybind11_type

**Bases**: pybind11_object



### CARRIAGE_RETURN_LINE_FEED

Members:

LINE_FEED

CARRIAGE_RETURN_LINE_FEED

**Type**: CSVLineTerminator





### LINE_FEED

Members:

LINE_FEED

CARRIAGE_RETURN_LINE_FEED

**Type**: CSVLineTerminator



































































### name

name(self: object) -> str

**Type**: property





### value



**Type**: property





## DEFAULT

Members:

DEFAULT

RETURN_NULL

**Type**: PythonExceptionHandling





## DuckDBPyConnection



**Type**: pybind11_type

**Bases**: pybind11_object































































### append

append(self: duckdb.duckdb.DuckDBPyConnection, table_name: str, df: pandas.DataFrame, *, by_name: bool = False) -> duckdb.duckdb.DuckDBPyConnection

Append the passed DataFrame to the named table

**Type**: instancemethod





### array_type

array_type(self: duckdb.duckdb.DuckDBPyConnection, type: duckdb.duckdb.typing.DuckDBPyType, size: int) -> duckdb.duckdb.typing.DuckDBPyType

Create an array type object of 'type'

**Type**: instancemethod





### arrow

arrow(self: duckdb.duckdb.DuckDBPyConnection, rows_per_batch: int = 1000000) -> pyarrow.lib.Table

Fetch a result as Arrow table following execute()

**Type**: instancemethod





### begin

begin(self: duckdb.duckdb.DuckDBPyConnection) -> duckdb.duckdb.DuckDBPyConnection

Start a new transaction

**Type**: instancemethod





### checkpoint

checkpoint(self: duckdb.duckdb.DuckDBPyConnection) -> duckdb.duckdb.DuckDBPyConnection

Synchronizes data in the write-ahead log (WAL) to the database data file (no-op for in-memory connections)

**Type**: instancemethod





### close

close(self: duckdb.duckdb.DuckDBPyConnection) -> None

Close the connection

**Type**: instancemethod





### commit

commit(self: duckdb.duckdb.DuckDBPyConnection) -> duckdb.duckdb.DuckDBPyConnection

Commit changes performed within a transaction

**Type**: instancemethod





### create_function

create_function(self: duckdb.duckdb.DuckDBPyConnection, name: str, function: Callable, parameters: object = None, return_type: duckdb.duckdb.typing.DuckDBPyType = None, *, type: duckdb.duckdb.functional.PythonUDFType = <PythonUDFType.NATIVE: 0>, null_handling: duckdb.duckdb.functional.FunctionNullHandling = <FunctionNullHandling.DEFAULT: 0>, exception_handling: duckdb.duckdb.PythonExceptionHandling = <PythonExceptionHandling.DEFAULT: 0>, side_effects: bool = False) -> duckdb.duckdb.DuckDBPyConnection

Create a DuckDB function out of the passing in Python function so it can be used in queries

**Type**: instancemethod





### cursor

cursor(self: duckdb.duckdb.DuckDBPyConnection) -> duckdb.duckdb.DuckDBPyConnection

Create a duplicate of the current connection

**Type**: instancemethod





### decimal_type

decimal_type(self: duckdb.duckdb.DuckDBPyConnection, width: int, scale: int) -> duckdb.duckdb.typing.DuckDBPyType

Create a decimal type with 'width' and 'scale'

**Type**: instancemethod





### description

Get result set attributes, mainly column names

**Type**: property





### df

df(self: duckdb.duckdb.DuckDBPyConnection, *, date_as_object: bool = False) -> pandas.DataFrame

Fetch a result as DataFrame following execute()

**Type**: instancemethod





### dtype

dtype(self: duckdb.duckdb.DuckDBPyConnection, type_str: str) -> duckdb.duckdb.typing.DuckDBPyType

Create a type object by parsing the 'type_str' string

**Type**: instancemethod





### duplicate

duplicate(self: duckdb.duckdb.DuckDBPyConnection) -> duckdb.duckdb.DuckDBPyConnection

Create a duplicate of the current connection

**Type**: instancemethod





### enum_type

enum_type(self: duckdb.duckdb.DuckDBPyConnection, name: str, type: duckdb.duckdb.typing.DuckDBPyType, values: list) -> duckdb.duckdb.typing.DuckDBPyType

Create an enum type of underlying 'type', consisting of the list of 'values'

**Type**: instancemethod





### execute

execute(self: duckdb.duckdb.DuckDBPyConnection, query: object, parameters: object = None) -> duckdb.duckdb.DuckDBPyConnection

Execute the given SQL query, optionally using prepared statements with parameters set

**Type**: instancemethod





### executemany

executemany(self: duckdb.duckdb.DuckDBPyConnection, query: object, parameters: object = None) -> duckdb.duckdb.DuckDBPyConnection

Execute the given prepared statement multiple times using the list of parameter sets in parameters

**Type**: instancemethod





### extract_statements

extract_statements(self: duckdb.duckdb.DuckDBPyConnection, query: str) -> list

Parse the query string and extract the Statement object(s) produced

**Type**: instancemethod





### fetch_arrow_table

fetch_arrow_table(self: duckdb.duckdb.DuckDBPyConnection, rows_per_batch: int = 1000000) -> pyarrow.lib.Table

Fetch a result as Arrow table following execute()

**Type**: instancemethod





### fetch_df

fetch_df(self: duckdb.duckdb.DuckDBPyConnection, *, date_as_object: bool = False) -> pandas.DataFrame

Fetch a result as DataFrame following execute()

**Type**: instancemethod





### fetch_df_chunk

fetch_df_chunk(self: duckdb.duckdb.DuckDBPyConnection, vectors_per_chunk: int = 1, *, date_as_object: bool = False) -> pandas.DataFrame

Fetch a chunk of the result as DataFrame following execute()

**Type**: instancemethod





### fetch_record_batch

fetch_record_batch(self: duckdb.duckdb.DuckDBPyConnection, rows_per_batch: int = 1000000) -> pyarrow.lib.RecordBatchReader

Fetch an Arrow RecordBatchReader following execute()

**Type**: instancemethod





### fetchall

fetchall(self: duckdb.duckdb.DuckDBPyConnection) -> list

Fetch all rows from a result following execute

**Type**: instancemethod





### fetchdf

fetchdf(self: duckdb.duckdb.DuckDBPyConnection, *, date_as_object: bool = False) -> pandas.DataFrame

Fetch a result as DataFrame following execute()

**Type**: instancemethod





### fetchmany

fetchmany(self: duckdb.duckdb.DuckDBPyConnection, size: int = 1) -> list

Fetch the next set of rows from a result following execute

**Type**: instancemethod





### fetchnumpy

fetchnumpy(self: duckdb.duckdb.DuckDBPyConnection) -> dict

Fetch a result as list of NumPy arrays following execute

**Type**: instancemethod





### fetchone

fetchone(self: duckdb.duckdb.DuckDBPyConnection) -> typing.Optional[tuple]

Fetch a single row from a result following execute

**Type**: instancemethod





### filesystem_is_registered

filesystem_is_registered(self: duckdb.duckdb.DuckDBPyConnection, name: str) -> bool

Check if a filesystem with the provided name is currently registered

**Type**: instancemethod





### from_arrow

from_arrow(self: duckdb.duckdb.DuckDBPyConnection, arrow_object: object) -> duckdb.duckdb.DuckDBPyRelation

Create a relation object from an Arrow object

**Type**: instancemethod





### from_csv_auto

from_csv_auto(self: duckdb.duckdb.DuckDBPyConnection, path_or_buffer: object, **kwargs) -> duckdb.duckdb.DuckDBPyRelation

Create a relation object from the CSV file in 'name'

**Type**: instancemethod





### from_df

from_df(self: duckdb.duckdb.DuckDBPyConnection, df: pandas.DataFrame) -> duckdb.duckdb.DuckDBPyRelation

Create a relation object from the DataFrame in df

**Type**: instancemethod





### from_parquet

from_parquet(*args, **kwargs)
Overloaded function.

1. from_parquet(self: duckdb.duckdb.DuckDBPyConnection, file_glob: str, binary_as_string: bool = False, *, file_row_number: bool = False, filename: bool = False, hive_partitioning: bool = False, union_by_name: bool = False, compression: object = None) -> duckdb.duckdb.DuckDBPyRelation

Create a relation object from the Parquet files in file_glob

2. from_parquet(self: duckdb.duckdb.DuckDBPyConnection, file_globs: list[str], binary_as_string: bool = False, *, file_row_number: bool = False, filename: bool = False, hive_partitioning: bool = False, union_by_name: bool = False, compression: object = None) -> duckdb.duckdb.DuckDBPyRelation

Create a relation object from the Parquet files in file_globs

**Type**: instancemethod





### from_query

from_query(self: duckdb.duckdb.DuckDBPyConnection, query: object, *, alias: str = '', params: object = None) -> duckdb.duckdb.DuckDBPyRelation

Run a SQL query. If it is a SELECT statement, create a relation object from the given SQL query, otherwise run the query as-is.

**Type**: instancemethod





### get_table_names

get_table_names(self: duckdb.duckdb.DuckDBPyConnection, query: str) -> set[str]

Extract the required table names from a query

**Type**: instancemethod





### install_extension

install_extension(self: duckdb.duckdb.DuckDBPyConnection, extension: str, *, force_install: bool = False, repository: object = None, repository_url: object = None, version: object = None) -> None

Install an extension by name, with an optional version and/or repository to get the extension from

**Type**: instancemethod





### interrupt

interrupt(self: duckdb.duckdb.DuckDBPyConnection) -> None

Interrupt pending operations

**Type**: instancemethod





### list_filesystems

list_filesystems(self: duckdb.duckdb.DuckDBPyConnection) -> list

List registered filesystems, including builtin ones

**Type**: instancemethod





### list_type

list_type(self: duckdb.duckdb.DuckDBPyConnection, type: duckdb.duckdb.typing.DuckDBPyType) -> duckdb.duckdb.typing.DuckDBPyType

Create a list type object of 'type'

**Type**: instancemethod





### load_extension

load_extension(self: duckdb.duckdb.DuckDBPyConnection, extension: str) -> None

Load an installed extension

**Type**: instancemethod





### map_type

map_type(self: duckdb.duckdb.DuckDBPyConnection, key: duckdb.duckdb.typing.DuckDBPyType, value: duckdb.duckdb.typing.DuckDBPyType) -> duckdb.duckdb.typing.DuckDBPyType

Create a map type object from 'key_type' and 'value_type'

**Type**: instancemethod





### pl

pl(self: duckdb.duckdb.DuckDBPyConnection, rows_per_batch: int = 1000000) -> duckdb::PolarsDataFrame

Fetch a result as Polars DataFrame following execute()

**Type**: instancemethod





### query

query(self: duckdb.duckdb.DuckDBPyConnection, query: object, *, alias: str = '', params: object = None) -> duckdb.duckdb.DuckDBPyRelation

Run a SQL query. If it is a SELECT statement, create a relation object from the given SQL query, otherwise run the query as-is.

**Type**: instancemethod





### read_csv

read_csv(self: duckdb.duckdb.DuckDBPyConnection, path_or_buffer: object, **kwargs) -> duckdb.duckdb.DuckDBPyRelation

Create a relation object from the CSV file in 'name'

**Type**: instancemethod





### read_json

read_json(self: duckdb.duckdb.DuckDBPyConnection, path_or_buffer: object, *, columns: typing.Optional[object] = None, sample_size: typing.Optional[object] = None, maximum_depth: typing.Optional[object] = None, records: typing.Optional[str] = None, format: typing.Optional[str] = None, date_format: typing.Optional[object] = None, timestamp_format: typing.Optional[object] = None, compression: typing.Optional[object] = None, maximum_object_size: typing.Optional[object] = None, ignore_errors: typing.Optional[object] = None, convert_strings_to_integers: typing.Optional[object] = None, field_appearance_threshold: typing.Optional[object] = None, map_inference_threshold: typing.Optional[object] = None, maximum_sample_files: typing.Optional[object] = None, filename: typing.Optional[object] = None, hive_partitioning: typing.Optional[object] = None, union_by_name: typing.Optional[object] = None, hive_types: typing.Optional[object] = None, hive_types_autocast: typing.Optional[object] = None) -> duckdb.duckdb.DuckDBPyRelation

Create a relation object from the JSON file in 'name'

**Type**: instancemethod





### read_parquet

read_parquet(*args, **kwargs)
Overloaded function.

1. read_parquet(self: duckdb.duckdb.DuckDBPyConnection, file_glob: str, binary_as_string: bool = False, *, file_row_number: bool = False, filename: bool = False, hive_partitioning: bool = False, union_by_name: bool = False, compression: object = None) -> duckdb.duckdb.DuckDBPyRelation

Create a relation object from the Parquet files in file_glob

2. read_parquet(self: duckdb.duckdb.DuckDBPyConnection, file_globs: list[str], binary_as_string: bool = False, *, file_row_number: bool = False, filename: bool = False, hive_partitioning: bool = False, union_by_name: bool = False, compression: object = None) -> duckdb.duckdb.DuckDBPyRelation

Create a relation object from the Parquet files in file_globs

**Type**: instancemethod





### register

register(self: duckdb.duckdb.DuckDBPyConnection, view_name: str, python_object: object) -> duckdb.duckdb.DuckDBPyConnection

Register the passed Python Object value for querying with a view

**Type**: instancemethod





### register_filesystem

register_filesystem(self: duckdb.duckdb.DuckDBPyConnection, filesystem: fsspec.AbstractFileSystem) -> None

Register a fsspec compliant filesystem

**Type**: instancemethod





### remove_function

remove_function(self: duckdb.duckdb.DuckDBPyConnection, name: str) -> duckdb.duckdb.DuckDBPyConnection

Remove a previously created function

**Type**: instancemethod





### rollback

rollback(self: duckdb.duckdb.DuckDBPyConnection) -> duckdb.duckdb.DuckDBPyConnection

Roll back changes performed within a transaction

**Type**: instancemethod





### row_type

row_type(self: duckdb.duckdb.DuckDBPyConnection, fields: object) -> duckdb.duckdb.typing.DuckDBPyType

Create a struct type object from 'fields'

**Type**: instancemethod





### rowcount

Get result set row count

**Type**: property





### sql

sql(self: duckdb.duckdb.DuckDBPyConnection, query: object, *, alias: str = '', params: object = None) -> duckdb.duckdb.DuckDBPyRelation

Run a SQL query. If it is a SELECT statement, create a relation object from the given SQL query, otherwise run the query as-is.

**Type**: instancemethod





### sqltype

sqltype(self: duckdb.duckdb.DuckDBPyConnection, type_str: str) -> duckdb.duckdb.typing.DuckDBPyType

Create a type object by parsing the 'type_str' string

**Type**: instancemethod





### string_type

string_type(self: duckdb.duckdb.DuckDBPyConnection, collation: str = '') -> duckdb.duckdb.typing.DuckDBPyType

Create a string type with an optional collation

**Type**: instancemethod





### struct_type

struct_type(self: duckdb.duckdb.DuckDBPyConnection, fields: object) -> duckdb.duckdb.typing.DuckDBPyType

Create a struct type object from 'fields'

**Type**: instancemethod





### table

table(self: duckdb.duckdb.DuckDBPyConnection, table_name: str) -> duckdb.duckdb.DuckDBPyRelation

Create a relation object for the named table

**Type**: instancemethod





### table_function

table_function(self: duckdb.duckdb.DuckDBPyConnection, name: str, parameters: object = None) -> duckdb.duckdb.DuckDBPyRelation

Create a relation object from the named table function with given parameters

**Type**: instancemethod





### tf

tf(self: duckdb.duckdb.DuckDBPyConnection) -> dict

Fetch a result as dict of TensorFlow Tensors following execute()

**Type**: instancemethod





### torch

torch(self: duckdb.duckdb.DuckDBPyConnection) -> dict

Fetch a result as dict of PyTorch Tensors following execute()

**Type**: instancemethod





### type

type(self: duckdb.duckdb.DuckDBPyConnection, type_str: str) -> duckdb.duckdb.typing.DuckDBPyType

Create a type object by parsing the 'type_str' string

**Type**: instancemethod





### union_type

union_type(self: duckdb.duckdb.DuckDBPyConnection, members: object) -> duckdb.duckdb.typing.DuckDBPyType

Create a union type object from 'members'

**Type**: instancemethod





### unregister

unregister(self: duckdb.duckdb.DuckDBPyConnection, view_name: str) -> duckdb.duckdb.DuckDBPyConnection

Unregister the view name

**Type**: instancemethod





### unregister_filesystem

unregister_filesystem(self: duckdb.duckdb.DuckDBPyConnection, name: str) -> None

Unregister a filesystem

**Type**: instancemethod





### values

values(self: duckdb.duckdb.DuckDBPyConnection, *args) -> duckdb.duckdb.DuckDBPyRelation

Create a relation object from the passed values

**Type**: instancemethod





### view

view(self: duckdb.duckdb.DuckDBPyConnection, view_name: str) -> duckdb.duckdb.DuckDBPyRelation

Create a relation object for the named view

**Type**: instancemethod





## DuckDBPyRelation



**Type**: pybind11_type

**Bases**: pybind11_object



































































### aggregate

aggregate(self: duckdb.duckdb.DuckDBPyRelation, aggr_expr: object, group_expr: str = '') -> duckdb.duckdb.DuckDBPyRelation

Compute the aggregate aggr_expr by the optional groups group_expr on the relation

**Type**: instancemethod





### alias

Get the name of the current alias

**Type**: property





### any_value

any_value(self: duckdb.duckdb.DuckDBPyRelation, column: str, groups: str = '', window_spec: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Returns the first non-null value from a given column

**Type**: instancemethod





### apply

apply(self: duckdb.duckdb.DuckDBPyRelation, function_name: str, function_aggr: str, group_expr: str = '', function_parameter: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Compute the function of a single column or a list of columns by the optional groups on the relation

**Type**: instancemethod





### arg_max

arg_max(self: duckdb.duckdb.DuckDBPyRelation, arg_column: str, value_column: str, groups: str = '', window_spec: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Finds the row with the maximum value for a value column and returns the value of that row for an argument column

**Type**: instancemethod





### arg_min

arg_min(self: duckdb.duckdb.DuckDBPyRelation, arg_column: str, value_column: str, groups: str = '', window_spec: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Finds the row with the minimum value for a value column and returns the value of that row for an argument column

**Type**: instancemethod





### arrow

arrow(self: duckdb.duckdb.DuckDBPyRelation, batch_size: int = 1000000) -> pyarrow.lib.Table

Execute and fetch all rows as an Arrow Table

**Type**: instancemethod





### avg

avg(self: duckdb.duckdb.DuckDBPyRelation, column: str, groups: str = '', window_spec: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes the average on a given column

**Type**: instancemethod





### bit_and

bit_and(self: duckdb.duckdb.DuckDBPyRelation, column: str, groups: str = '', window_spec: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes the bitwise AND of all bits present in a given column

**Type**: instancemethod





### bit_or

bit_or(self: duckdb.duckdb.DuckDBPyRelation, column: str, groups: str = '', window_spec: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes the bitwise OR of all bits present in a given column

**Type**: instancemethod





### bit_xor

bit_xor(self: duckdb.duckdb.DuckDBPyRelation, column: str, groups: str = '', window_spec: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes the bitwise XOR of all bits present in a given column

**Type**: instancemethod





### bitstring_agg

bitstring_agg(self: duckdb.duckdb.DuckDBPyRelation, column: str, min: typing.Optional[object] = None, max: typing.Optional[object] = None, groups: str = '', window_spec: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes a bitstring with bits set for each distinct value in a given column

**Type**: instancemethod





### bool_and

bool_and(self: duckdb.duckdb.DuckDBPyRelation, column: str, groups: str = '', window_spec: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes the logical AND of all values present in a given column

**Type**: instancemethod





### bool_or

bool_or(self: duckdb.duckdb.DuckDBPyRelation, column: str, groups: str = '', window_spec: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes the logical OR of all values present in a given column

**Type**: instancemethod





### close

close(self: duckdb.duckdb.DuckDBPyRelation) -> None

Closes the result

**Type**: instancemethod





### columns

Return a list containing the names of the columns of the relation.

**Type**: property





### count

count(self: duckdb.duckdb.DuckDBPyRelation, column: str, groups: str = '', window_spec: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes the number of elements present in a given column

**Type**: instancemethod





### create

create(self: duckdb.duckdb.DuckDBPyRelation, table_name: str) -> None

Creates a new table named table_name with the contents of the relation object

**Type**: instancemethod





### create_view

create_view(self: duckdb.duckdb.DuckDBPyRelation, view_name: str, replace: bool = True) -> duckdb.duckdb.DuckDBPyRelation

Creates a view named view_name that refers to the relation object

**Type**: instancemethod





### cross

cross(self: duckdb.duckdb.DuckDBPyRelation, other_rel: duckdb.duckdb.DuckDBPyRelation) -> duckdb.duckdb.DuckDBPyRelation

Create cross/cartesian product of two relational objects

**Type**: instancemethod





### cume_dist

cume_dist(self: duckdb.duckdb.DuckDBPyRelation, window_spec: str, projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes the cumulative distribution within the partition

**Type**: instancemethod





### dense_rank

dense_rank(self: duckdb.duckdb.DuckDBPyRelation, window_spec: str, projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes the dense rank within the partition

**Type**: instancemethod





### describe

describe(self: duckdb.duckdb.DuckDBPyRelation) -> duckdb.duckdb.DuckDBPyRelation

Gives basic statistics (e.g., min, max) and if NULL exists for each column of the relation.

**Type**: instancemethod





### description

Return the description of the result

**Type**: property





### df

df(self: duckdb.duckdb.DuckDBPyRelation, *, date_as_object: bool = False) -> pandas.DataFrame

Execute and fetch all rows as a pandas DataFrame

**Type**: instancemethod





### distinct

distinct(self: duckdb.duckdb.DuckDBPyRelation) -> duckdb.duckdb.DuckDBPyRelation

Retrieve distinct rows from this relation object

**Type**: instancemethod





### dtypes

Return a list containing the types of the columns of the relation.

**Type**: property





### except_

except_(self: duckdb.duckdb.DuckDBPyRelation, other_rel: duckdb.duckdb.DuckDBPyRelation) -> duckdb.duckdb.DuckDBPyRelation

Create the set except of this relation object with another relation object in other_rel

**Type**: instancemethod





### execute

execute(self: duckdb.duckdb.DuckDBPyRelation) -> duckdb.duckdb.DuckDBPyRelation

Transform the relation into a result set

**Type**: instancemethod





### explain

explain(self: duckdb.duckdb.DuckDBPyRelation, type: duckdb.duckdb.ExplainType = 'standard') -> str

**Type**: instancemethod





### favg

favg(self: duckdb.duckdb.DuckDBPyRelation, column: str, groups: str = '', window_spec: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes the average of all values present in a given column using a more accurate floating point summation (Kahan Sum)

**Type**: instancemethod





### fetch_arrow_reader

fetch_arrow_reader(self: duckdb.duckdb.DuckDBPyRelation, batch_size: int = 1000000) -> pyarrow.lib.RecordBatchReader

Execute and return an Arrow Record Batch Reader that yields all rows

**Type**: instancemethod





### fetch_arrow_table

fetch_arrow_table(self: duckdb.duckdb.DuckDBPyRelation, batch_size: int = 1000000) -> pyarrow.lib.Table

Execute and fetch all rows as an Arrow Table

**Type**: instancemethod





### fetch_df_chunk

fetch_df_chunk(self: duckdb.duckdb.DuckDBPyRelation, vectors_per_chunk: int = 1, *, date_as_object: bool = False) -> pandas.DataFrame

Execute and fetch a chunk of the rows

**Type**: instancemethod





### fetchall

fetchall(self: duckdb.duckdb.DuckDBPyRelation) -> list

Execute and fetch all rows as a list of tuples

**Type**: instancemethod





### fetchdf

fetchdf(self: duckdb.duckdb.DuckDBPyRelation, *, date_as_object: bool = False) -> pandas.DataFrame

Execute and fetch all rows as a pandas DataFrame

**Type**: instancemethod





### fetchmany

fetchmany(self: duckdb.duckdb.DuckDBPyRelation, size: int = 1) -> list

Execute and fetch the next set of rows as a list of tuples

**Type**: instancemethod





### fetchnumpy

fetchnumpy(self: duckdb.duckdb.DuckDBPyRelation) -> dict

Execute and fetch all rows as a Python dict mapping each column to one numpy arrays

**Type**: instancemethod





### fetchone

fetchone(self: duckdb.duckdb.DuckDBPyRelation) -> typing.Optional[tuple]

Execute and fetch a single row as a tuple

**Type**: instancemethod





### filter

filter(self: duckdb.duckdb.DuckDBPyRelation, filter_expr: object) -> duckdb.duckdb.DuckDBPyRelation

Filter the relation object by the filter in filter_expr

**Type**: instancemethod





### first

first(self: duckdb.duckdb.DuckDBPyRelation, column: str, groups: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Returns the first value of a given column

**Type**: instancemethod





### first_value

first_value(self: duckdb.duckdb.DuckDBPyRelation, column: str, window_spec: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes the first value within the group or partition

**Type**: instancemethod





### fsum

fsum(self: duckdb.duckdb.DuckDBPyRelation, column: str, groups: str = '', window_spec: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes the sum of all values present in a given column using a more accurate floating point summation (Kahan Sum)

**Type**: instancemethod





### geomean

geomean(self: duckdb.duckdb.DuckDBPyRelation, column: str, groups: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes the geometric mean over all values present in a given column

**Type**: instancemethod





### histogram

histogram(self: duckdb.duckdb.DuckDBPyRelation, column: str, groups: str = '', window_spec: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes the histogram over all values present in a given column

**Type**: instancemethod





### insert

insert(self: duckdb.duckdb.DuckDBPyRelation, values: object) -> None

Inserts the given values into the relation

**Type**: instancemethod





### insert_into

insert_into(self: duckdb.duckdb.DuckDBPyRelation, table_name: str) -> None

Inserts the relation object into an existing table named table_name

**Type**: instancemethod





### intersect

intersect(self: duckdb.duckdb.DuckDBPyRelation, other_rel: duckdb.duckdb.DuckDBPyRelation) -> duckdb.duckdb.DuckDBPyRelation

Create the set intersection of this relation object with another relation object in other_rel

**Type**: instancemethod





### join

join(self: duckdb.duckdb.DuckDBPyRelation, other_rel: duckdb.duckdb.DuckDBPyRelation, condition: object, how: str = 'inner') -> duckdb.duckdb.DuckDBPyRelation

Join the relation object with another relation object in other_rel using the join condition expression in join_condition. Types supported are 'inner' and 'left'

**Type**: instancemethod





### lag

lag(self: duckdb.duckdb.DuckDBPyRelation, column: str, window_spec: str, offset: int = 1, default_value: str = 'NULL', ignore_nulls: bool = False, projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes the lag within the partition

**Type**: instancemethod





### last

last(self: duckdb.duckdb.DuckDBPyRelation, column: str, groups: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Returns the last value of a given column

**Type**: instancemethod





### last_value

last_value(self: duckdb.duckdb.DuckDBPyRelation, column: str, window_spec: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes the last value within the group or partition

**Type**: instancemethod





### lead

lead(self: duckdb.duckdb.DuckDBPyRelation, column: str, window_spec: str, offset: int = 1, default_value: str = 'NULL', ignore_nulls: bool = False, projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes the lead within the partition

**Type**: instancemethod





### limit

limit(self: duckdb.duckdb.DuckDBPyRelation, n: int, offset: int = 0) -> duckdb.duckdb.DuckDBPyRelation

Only retrieve the first n rows from this relation object, starting at offset

**Type**: instancemethod





### list

list(self: duckdb.duckdb.DuckDBPyRelation, column: str, groups: str = '', window_spec: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Returns a list containing all values present in a given column

**Type**: instancemethod





### map

map(self: duckdb.duckdb.DuckDBPyRelation, map_function: Callable, *, schema: typing.Optional[object] = None) -> duckdb.duckdb.DuckDBPyRelation

Calls the passed function on the relation

**Type**: instancemethod





### max

max(self: duckdb.duckdb.DuckDBPyRelation, column: str, groups: str = '', window_spec: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Returns the maximum value present in a given column

**Type**: instancemethod





### mean

mean(self: duckdb.duckdb.DuckDBPyRelation, column: str, groups: str = '', window_spec: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes the average on a given column

**Type**: instancemethod





### median

median(self: duckdb.duckdb.DuckDBPyRelation, column: str, groups: str = '', window_spec: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes the median over all values present in a given column

**Type**: instancemethod





### min

min(self: duckdb.duckdb.DuckDBPyRelation, column: str, groups: str = '', window_spec: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Returns the minimum value present in a given column

**Type**: instancemethod





### mode

mode(self: duckdb.duckdb.DuckDBPyRelation, column: str, groups: str = '', window_spec: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes the mode over all values present in a given column

**Type**: instancemethod





### n_tile

n_tile(self: duckdb.duckdb.DuckDBPyRelation, window_spec: str, num_buckets: int, projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Divides the partition as equally as possible into num_buckets

**Type**: instancemethod





### nth_value

nth_value(self: duckdb.duckdb.DuckDBPyRelation, column: str, window_spec: str, offset: int, ignore_nulls: bool = False, projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes the nth value within the partition

**Type**: instancemethod





### order

order(self: duckdb.duckdb.DuckDBPyRelation, order_expr: str) -> duckdb.duckdb.DuckDBPyRelation

Reorder the relation object by order_expr

**Type**: instancemethod





### percent_rank

percent_rank(self: duckdb.duckdb.DuckDBPyRelation, window_spec: str, projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes the relative rank within the partition

**Type**: instancemethod





### pl

pl(self: duckdb.duckdb.DuckDBPyRelation, batch_size: int = 1000000) -> duckdb::PolarsDataFrame

Execute and fetch all rows as a Polars DataFrame

**Type**: instancemethod





### product

product(self: duckdb.duckdb.DuckDBPyRelation, column: str, groups: str = '', window_spec: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Returns the product of all values present in a given column

**Type**: instancemethod





### project

project(self: duckdb.duckdb.DuckDBPyRelation, *args, groups: str = '') -> duckdb.duckdb.DuckDBPyRelation

Project the relation object by the projection in project_expr

**Type**: instancemethod





### quantile

quantile(self: duckdb.duckdb.DuckDBPyRelation, column: str, q: object = 0.5, groups: str = '', window_spec: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes the exact quantile value for a given column

**Type**: instancemethod





### quantile_cont

quantile_cont(self: duckdb.duckdb.DuckDBPyRelation, column: str, q: object = 0.5, groups: str = '', window_spec: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes the interpolated quantile value for a given column

**Type**: instancemethod





### quantile_disc

quantile_disc(self: duckdb.duckdb.DuckDBPyRelation, column: str, q: object = 0.5, groups: str = '', window_spec: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes the exact quantile value for a given column

**Type**: instancemethod





### query

query(self: duckdb.duckdb.DuckDBPyRelation, virtual_table_name: str, sql_query: str) -> duckdb.duckdb.DuckDBPyRelation

Run the given SQL query in sql_query on the view named virtual_table_name that refers to the relation object

**Type**: instancemethod





### rank

rank(self: duckdb.duckdb.DuckDBPyRelation, window_spec: str, projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes the rank within the partition

**Type**: instancemethod





### rank_dense

rank_dense(self: duckdb.duckdb.DuckDBPyRelation, window_spec: str, projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes the dense rank within the partition

**Type**: instancemethod





### record_batch

record_batch(self: duckdb.duckdb.DuckDBPyRelation, batch_size: int = 1000000) -> pyarrow.lib.RecordBatchReader

Execute and return an Arrow Record Batch Reader that yields all rows

**Type**: instancemethod





### row_number

row_number(self: duckdb.duckdb.DuckDBPyRelation, window_spec: str, projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes the row number within the partition

**Type**: instancemethod





### select

select(self: duckdb.duckdb.DuckDBPyRelation, *args, groups: str = '') -> duckdb.duckdb.DuckDBPyRelation

Project the relation object by the projection in project_expr

**Type**: instancemethod





### select_dtypes

select_dtypes(self: duckdb.duckdb.DuckDBPyRelation, types: object) -> duckdb.duckdb.DuckDBPyRelation

Select columns from the relation, by filtering based on type(s)

**Type**: instancemethod





### select_types

select_types(self: duckdb.duckdb.DuckDBPyRelation, types: object) -> duckdb.duckdb.DuckDBPyRelation

Select columns from the relation, by filtering based on type(s)

**Type**: instancemethod





### set_alias

set_alias(self: duckdb.duckdb.DuckDBPyRelation, alias: str) -> duckdb.duckdb.DuckDBPyRelation

Rename the relation object to new alias

**Type**: instancemethod





### shape

Tuple of # of rows, # of columns in relation.

**Type**: property





### show

show(self: duckdb.duckdb.DuckDBPyRelation, *, max_width: typing.Optional[int] = None, max_rows: typing.Optional[int] = None, max_col_width: typing.Optional[int] = None, null_value: typing.Optional[str] = None, render_mode: object = None) -> None

Display a summary of the data

**Type**: instancemethod





### sort

sort(self: duckdb.duckdb.DuckDBPyRelation, *args) -> duckdb.duckdb.DuckDBPyRelation

Reorder the relation object by the provided expressions

**Type**: instancemethod





### sql_query

sql_query(self: duckdb.duckdb.DuckDBPyRelation) -> str

Get the SQL query that is equivalent to the relation

**Type**: instancemethod





### std

std(self: duckdb.duckdb.DuckDBPyRelation, column: str, groups: str = '', window_spec: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes the sample standard deviation for a given column

**Type**: instancemethod





### stddev

stddev(self: duckdb.duckdb.DuckDBPyRelation, column: str, groups: str = '', window_spec: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes the sample standard deviation for a given column

**Type**: instancemethod





### stddev_pop

stddev_pop(self: duckdb.duckdb.DuckDBPyRelation, column: str, groups: str = '', window_spec: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes the population standard deviation for a given column

**Type**: instancemethod





### stddev_samp

stddev_samp(self: duckdb.duckdb.DuckDBPyRelation, column: str, groups: str = '', window_spec: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes the sample standard deviation for a given column

**Type**: instancemethod





### string_agg

string_agg(self: duckdb.duckdb.DuckDBPyRelation, column: str, sep: str = ',', groups: str = '', window_spec: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Concatenates the values present in a given column with a separator

**Type**: instancemethod





### sum

sum(self: duckdb.duckdb.DuckDBPyRelation, column: str, groups: str = '', window_spec: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes the sum of all values present in a given column

**Type**: instancemethod





### tf

tf(self: duckdb.duckdb.DuckDBPyRelation) -> dict

Fetch a result as dict of TensorFlow Tensors

**Type**: instancemethod





### to_arrow_table

to_arrow_table(self: duckdb.duckdb.DuckDBPyRelation, batch_size: int = 1000000) -> pyarrow.lib.Table

Execute and fetch all rows as an Arrow Table

**Type**: instancemethod





### to_csv

to_csv(self: duckdb.duckdb.DuckDBPyRelation, file_name: str, *, sep: object = None, na_rep: object = None, header: object = None, quotechar: object = None, escapechar: object = None, date_format: object = None, timestamp_format: object = None, quoting: object = None, encoding: object = None, compression: object = None, overwrite: object = None, per_thread_output: object = None, use_tmp_file: object = None, partition_by: object = None, write_partition_columns: object = None) -> None

Write the relation object to a CSV file in 'file_name'

**Type**: instancemethod





### to_df

to_df(self: duckdb.duckdb.DuckDBPyRelation, *, date_as_object: bool = False) -> pandas.DataFrame

Execute and fetch all rows as a pandas DataFrame

**Type**: instancemethod





### to_parquet

to_parquet(self: duckdb.duckdb.DuckDBPyRelation, file_name: str, *, compression: object = None, field_ids: object = None, row_group_size_bytes: object = None, row_group_size: object = None, overwrite: object = None, per_thread_output: object = None, use_tmp_file: object = None, partition_by: object = None, write_partition_columns: object = None, append: object = None) -> None

Write the relation object to a Parquet file in 'file_name'

**Type**: instancemethod





### to_table

to_table(self: duckdb.duckdb.DuckDBPyRelation, table_name: str) -> None

Creates a new table named table_name with the contents of the relation object

**Type**: instancemethod





### to_view

to_view(self: duckdb.duckdb.DuckDBPyRelation, view_name: str, replace: bool = True) -> duckdb.duckdb.DuckDBPyRelation

Creates a view named view_name that refers to the relation object

**Type**: instancemethod





### torch

torch(self: duckdb.duckdb.DuckDBPyRelation) -> dict

Fetch a result as dict of PyTorch Tensors

**Type**: instancemethod





### type

Get the type of the relation.

**Type**: property





### types

Return a list containing the types of the columns of the relation.

**Type**: property





### union

union(self: duckdb.duckdb.DuckDBPyRelation, union_rel: duckdb.duckdb.DuckDBPyRelation) -> duckdb.duckdb.DuckDBPyRelation

Create the set union of this relation object with another relation object in other_rel

**Type**: instancemethod





### unique

unique(self: duckdb.duckdb.DuckDBPyRelation, unique_aggr: str) -> duckdb.duckdb.DuckDBPyRelation

Number of distinct values in a column.

**Type**: instancemethod





### update

update(self: duckdb.duckdb.DuckDBPyRelation, set: object, *, condition: object = None) -> None

Update the given relation with the provided expressions

**Type**: instancemethod





### value_counts

value_counts(self: duckdb.duckdb.DuckDBPyRelation, column: str, groups: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes the number of elements present in a given column, also projecting the original column

**Type**: instancemethod





### var

var(self: duckdb.duckdb.DuckDBPyRelation, column: str, groups: str = '', window_spec: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes the sample variance for a given column

**Type**: instancemethod





### var_pop

var_pop(self: duckdb.duckdb.DuckDBPyRelation, column: str, groups: str = '', window_spec: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes the population variance for a given column

**Type**: instancemethod





### var_samp

var_samp(self: duckdb.duckdb.DuckDBPyRelation, column: str, groups: str = '', window_spec: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes the sample variance for a given column

**Type**: instancemethod





### variance

variance(self: duckdb.duckdb.DuckDBPyRelation, column: str, groups: str = '', window_spec: str = '', projected_columns: str = '') -> duckdb.duckdb.DuckDBPyRelation

Computes the sample variance for a given column

**Type**: instancemethod





### write_csv

write_csv(self: duckdb.duckdb.DuckDBPyRelation, file_name: str, *, sep: object = None, na_rep: object = None, header: object = None, quotechar: object = None, escapechar: object = None, date_format: object = None, timestamp_format: object = None, quoting: object = None, encoding: object = None, compression: object = None, overwrite: object = None, per_thread_output: object = None, use_tmp_file: object = None, partition_by: object = None, write_partition_columns: object = None) -> None

Write the relation object to a CSV file in 'file_name'

**Type**: instancemethod





### write_parquet

write_parquet(self: duckdb.duckdb.DuckDBPyRelation, file_name: str, *, compression: object = None, field_ids: object = None, row_group_size_bytes: object = None, row_group_size: object = None, overwrite: object = None, per_thread_output: object = None, use_tmp_file: object = None, partition_by: object = None, write_partition_columns: object = None, append: object = None) -> None

Write the relation object to a Parquet file in 'file_name'

**Type**: instancemethod





## ExpectedResultType

Members:

QUERY_RESULT

CHANGED_ROWS

NOTHING

**Type**: pybind11_type

**Bases**: pybind11_object



### CHANGED_ROWS

Members:

QUERY_RESULT

CHANGED_ROWS

NOTHING

**Type**: ExpectedResultType





### NOTHING

Members:

QUERY_RESULT

CHANGED_ROWS

NOTHING

**Type**: ExpectedResultType





### QUERY_RESULT

Members:

QUERY_RESULT

CHANGED_ROWS

NOTHING

**Type**: ExpectedResultType



































































### name

name(self: object) -> str

**Type**: property





### value



**Type**: property





## ExplainType

Members:

STANDARD

ANALYZE

**Type**: pybind11_type

**Bases**: pybind11_object



### ANALYZE

Members:

STANDARD

ANALYZE

**Type**: ExplainType





### STANDARD

Members:

STANDARD

ANALYZE

**Type**: ExplainType



































































### name

name(self: object) -> str

**Type**: property





### value



**Type**: property





## Expression



**Type**: pybind11_type

**Bases**: pybind11_object





































































































### alias

alias(self: duckdb.duckdb.Expression, arg0: str) -> duckdb.duckdb.Expression


Create a copy of this expression with the given alias.

Parameters:
        name: The alias to use for the expression, this will affect how it can be referenced.

Returns:
        Expression: self with an alias.

**Type**: instancemethod





### asc

asc(self: duckdb.duckdb.Expression) -> duckdb.duckdb.Expression


Set the order by modifier to ASCENDING.

**Type**: instancemethod





### between

between(self: duckdb.duckdb.Expression, lower: duckdb.duckdb.Expression, upper: duckdb.duckdb.Expression) -> duckdb.duckdb.Expression

**Type**: instancemethod





### cast

cast(self: duckdb.duckdb.Expression, type: duckdb.duckdb.typing.DuckDBPyType) -> duckdb.duckdb.Expression


Create a CastExpression to type from self

Parameters:
        type: The type to cast to

Returns:
        CastExpression: self::type

**Type**: instancemethod





### collate

collate(self: duckdb.duckdb.Expression, collation: str) -> duckdb.duckdb.Expression

**Type**: instancemethod





### desc

desc(self: duckdb.duckdb.Expression) -> duckdb.duckdb.Expression


Set the order by modifier to DESCENDING.

**Type**: instancemethod





### get_name

get_name(self: duckdb.duckdb.Expression) -> str


Return the stringified version of the expression.

Returns:
        str: The string representation.

**Type**: instancemethod





### isin

isin(self: duckdb.duckdb.Expression, *args) -> duckdb.duckdb.Expression


Return an IN expression comparing self to the input arguments.

Returns:
        DuckDBPyExpression: The compare IN expression

**Type**: instancemethod





### isnotin

isnotin(self: duckdb.duckdb.Expression, *args) -> duckdb.duckdb.Expression


Return a NOT IN expression comparing self to the input arguments.

Returns:
        DuckDBPyExpression: The compare NOT IN expression

**Type**: instancemethod





### isnotnull

isnotnull(self: duckdb.duckdb.Expression) -> duckdb.duckdb.Expression


Create a binary IS NOT NULL expression from self

Returns:
        DuckDBPyExpression: self IS NOT NULL

**Type**: instancemethod





### isnull

isnull(self: duckdb.duckdb.Expression) -> duckdb.duckdb.Expression


Create a binary IS NULL expression from self

Returns:
        DuckDBPyExpression: self IS NULL

**Type**: instancemethod





### nulls_first

nulls_first(self: duckdb.duckdb.Expression) -> duckdb.duckdb.Expression


Set the NULL order by modifier to NULLS FIRST.

**Type**: instancemethod





### nulls_last

nulls_last(self: duckdb.duckdb.Expression) -> duckdb.duckdb.Expression


Set the NULL order by modifier to NULLS LAST.

**Type**: instancemethod





### otherwise

otherwise(self: duckdb.duckdb.Expression, value: duckdb.duckdb.Expression) -> duckdb.duckdb.Expression


Add an ELSE <value> clause to the CaseExpression.

Parameters:
        value: The value to use if none of the WHEN conditions are met.

Returns:
        CaseExpression: self with an ELSE clause.

**Type**: instancemethod





### show

show(self: duckdb.duckdb.Expression) -> None


Print the stringified version of the expression.

**Type**: instancemethod





### when

when(self: duckdb.duckdb.Expression, condition: duckdb.duckdb.Expression, value: duckdb.duckdb.Expression) -> duckdb.duckdb.Expression


Add an additional WHEN <condition> THEN <value> clause to the CaseExpression.

Parameters:
        condition: The condition that must be met.
        value: The value to use if the condition is met.

Returns:
        CaseExpression: self with an additional WHEN clause.

**Type**: instancemethod





## PythonExceptionHandling

Members:

DEFAULT

RETURN_NULL

**Type**: pybind11_type

**Bases**: pybind11_object



### DEFAULT

Members:

DEFAULT

RETURN_NULL

**Type**: PythonExceptionHandling





### RETURN_NULL

Members:

DEFAULT

RETURN_NULL

**Type**: PythonExceptionHandling



































































### name

name(self: object) -> str

**Type**: property





### value



**Type**: property





## RETURN_NULL

Members:

DEFAULT

RETURN_NULL

**Type**: PythonExceptionHandling





## ROWS

Members:

ROWS

COLUMNS

**Type**: RenderMode





## RenderMode

Members:

ROWS

COLUMNS

**Type**: pybind11_type

**Bases**: pybind11_object



### COLUMNS

Members:

ROWS

COLUMNS

**Type**: RenderMode





### ROWS

Members:

ROWS

COLUMNS

**Type**: RenderMode



































































### name

name(self: object) -> str

**Type**: property





### value



**Type**: property





## STANDARD

Members:

STANDARD

ANALYZE

**Type**: ExplainType





## Statement



**Type**: pybind11_type

**Bases**: pybind11_object

























































### expected_result_type

Get the expected type of result produced by this statement, actual type may vary depending on the statement.

**Type**: property





### named_parameters

Get the map of named parameters this statement has.

**Type**: property





### query

Get the query equivalent to this statement.

**Type**: property





### type

Get the type of the statement.

**Type**: property





## StatementType

Members:

INVALID

SELECT

INSERT

UPDATE

CREATE

DELETE

PREPARE

EXECUTE

ALTER

TRANSACTION

COPY

ANALYZE

VARIABLE_SET

CREATE_FUNC

EXPLAIN

DROP

EXPORT

PRAGMA

VACUUM

CALL

SET

LOAD

RELATION

EXTENSION

LOGICAL_PLAN

ATTACH

DETACH

MULTI

COPY_DATABASE

**Type**: pybind11_type

**Bases**: pybind11_object



### ALTER

Members:

INVALID

SELECT

INSERT

UPDATE

CREATE

DELETE

PREPARE

EXECUTE

ALTER

TRANSACTION

COPY

ANALYZE

VARIABLE_SET

CREATE_FUNC

EXPLAIN

DROP

EXPORT

PRAGMA

VACUUM

CALL

SET

LOAD

RELATION

EXTENSION

LOGICAL_PLAN

ATTACH

DETACH

MULTI

COPY_DATABASE

**Type**: StatementType





### ANALYZE

Members:

INVALID

SELECT

INSERT

UPDATE

CREATE

DELETE

PREPARE

EXECUTE

ALTER

TRANSACTION

COPY

ANALYZE

VARIABLE_SET

CREATE_FUNC

EXPLAIN

DROP

EXPORT

PRAGMA

VACUUM

CALL

SET

LOAD

RELATION

EXTENSION

LOGICAL_PLAN

ATTACH

DETACH

MULTI

COPY_DATABASE

**Type**: StatementType





### ATTACH

Members:

INVALID

SELECT

INSERT

UPDATE

CREATE

DELETE

PREPARE

EXECUTE

ALTER

TRANSACTION

COPY

ANALYZE

VARIABLE_SET

CREATE_FUNC

EXPLAIN

DROP

EXPORT

PRAGMA

VACUUM

CALL

SET

LOAD

RELATION

EXTENSION

LOGICAL_PLAN

ATTACH

DETACH

MULTI

COPY_DATABASE

**Type**: StatementType





### CALL

Members:

INVALID

SELECT

INSERT

UPDATE

CREATE

DELETE

PREPARE

EXECUTE

ALTER

TRANSACTION

COPY

ANALYZE

VARIABLE_SET

CREATE_FUNC

EXPLAIN

DROP

EXPORT

PRAGMA

VACUUM

CALL

SET

LOAD

RELATION

EXTENSION

LOGICAL_PLAN

ATTACH

DETACH

MULTI

COPY_DATABASE

**Type**: StatementType





### COPY

Members:

INVALID

SELECT

INSERT

UPDATE

CREATE

DELETE

PREPARE

EXECUTE

ALTER

TRANSACTION

COPY

ANALYZE

VARIABLE_SET

CREATE_FUNC

EXPLAIN

DROP

EXPORT

PRAGMA

VACUUM

CALL

SET

LOAD

RELATION

EXTENSION

LOGICAL_PLAN

ATTACH

DETACH

MULTI

COPY_DATABASE

**Type**: StatementType





### COPY_DATABASE

Members:

INVALID

SELECT

INSERT

UPDATE

CREATE

DELETE

PREPARE

EXECUTE

ALTER

TRANSACTION

COPY

ANALYZE

VARIABLE_SET

CREATE_FUNC

EXPLAIN

DROP

EXPORT

PRAGMA

VACUUM

CALL

SET

LOAD

RELATION

EXTENSION

LOGICAL_PLAN

ATTACH

DETACH

MULTI

COPY_DATABASE

**Type**: StatementType





### CREATE

Members:

INVALID

SELECT

INSERT

UPDATE

CREATE

DELETE

PREPARE

EXECUTE

ALTER

TRANSACTION

COPY

ANALYZE

VARIABLE_SET

CREATE_FUNC

EXPLAIN

DROP

EXPORT

PRAGMA

VACUUM

CALL

SET

LOAD

RELATION

EXTENSION

LOGICAL_PLAN

ATTACH

DETACH

MULTI

COPY_DATABASE

**Type**: StatementType





### CREATE_FUNC

Members:

INVALID

SELECT

INSERT

UPDATE

CREATE

DELETE

PREPARE

EXECUTE

ALTER

TRANSACTION

COPY

ANALYZE

VARIABLE_SET

CREATE_FUNC

EXPLAIN

DROP

EXPORT

PRAGMA

VACUUM

CALL

SET

LOAD

RELATION

EXTENSION

LOGICAL_PLAN

ATTACH

DETACH

MULTI

COPY_DATABASE

**Type**: StatementType





### DELETE

Members:

INVALID

SELECT

INSERT

UPDATE

CREATE

DELETE

PREPARE

EXECUTE

ALTER

TRANSACTION

COPY

ANALYZE

VARIABLE_SET

CREATE_FUNC

EXPLAIN

DROP

EXPORT

PRAGMA

VACUUM

CALL

SET

LOAD

RELATION

EXTENSION

LOGICAL_PLAN

ATTACH

DETACH

MULTI

COPY_DATABASE

**Type**: StatementType





### DETACH

Members:

INVALID

SELECT

INSERT

UPDATE

CREATE

DELETE

PREPARE

EXECUTE

ALTER

TRANSACTION

COPY

ANALYZE

VARIABLE_SET

CREATE_FUNC

EXPLAIN

DROP

EXPORT

PRAGMA

VACUUM

CALL

SET

LOAD

RELATION

EXTENSION

LOGICAL_PLAN

ATTACH

DETACH

MULTI

COPY_DATABASE

**Type**: StatementType





### DROP

Members:

INVALID

SELECT

INSERT

UPDATE

CREATE

DELETE

PREPARE

EXECUTE

ALTER

TRANSACTION

COPY

ANALYZE

VARIABLE_SET

CREATE_FUNC

EXPLAIN

DROP

EXPORT

PRAGMA

VACUUM

CALL

SET

LOAD

RELATION

EXTENSION

LOGICAL_PLAN

ATTACH

DETACH

MULTI

COPY_DATABASE

**Type**: StatementType





### EXECUTE

Members:

INVALID

SELECT

INSERT

UPDATE

CREATE

DELETE

PREPARE

EXECUTE

ALTER

TRANSACTION

COPY

ANALYZE

VARIABLE_SET

CREATE_FUNC

EXPLAIN

DROP

EXPORT

PRAGMA

VACUUM

CALL

SET

LOAD

RELATION

EXTENSION

LOGICAL_PLAN

ATTACH

DETACH

MULTI

COPY_DATABASE

**Type**: StatementType





### EXPLAIN

Members:

INVALID

SELECT

INSERT

UPDATE

CREATE

DELETE

PREPARE

EXECUTE

ALTER

TRANSACTION

COPY

ANALYZE

VARIABLE_SET

CREATE_FUNC

EXPLAIN

DROP

EXPORT

PRAGMA

VACUUM

CALL

SET

LOAD

RELATION

EXTENSION

LOGICAL_PLAN

ATTACH

DETACH

MULTI

COPY_DATABASE

**Type**: StatementType





### EXPORT

Members:

INVALID

SELECT

INSERT

UPDATE

CREATE

DELETE

PREPARE

EXECUTE

ALTER

TRANSACTION

COPY

ANALYZE

VARIABLE_SET

CREATE_FUNC

EXPLAIN

DROP

EXPORT

PRAGMA

VACUUM

CALL

SET

LOAD

RELATION

EXTENSION

LOGICAL_PLAN

ATTACH

DETACH

MULTI

COPY_DATABASE

**Type**: StatementType





### EXTENSION

Members:

INVALID

SELECT

INSERT

UPDATE

CREATE

DELETE

PREPARE

EXECUTE

ALTER

TRANSACTION

COPY

ANALYZE

VARIABLE_SET

CREATE_FUNC

EXPLAIN

DROP

EXPORT

PRAGMA

VACUUM

CALL

SET

LOAD

RELATION

EXTENSION

LOGICAL_PLAN

ATTACH

DETACH

MULTI

COPY_DATABASE

**Type**: StatementType





### INSERT

Members:

INVALID

SELECT

INSERT

UPDATE

CREATE

DELETE

PREPARE

EXECUTE

ALTER

TRANSACTION

COPY

ANALYZE

VARIABLE_SET

CREATE_FUNC

EXPLAIN

DROP

EXPORT

PRAGMA

VACUUM

CALL

SET

LOAD

RELATION

EXTENSION

LOGICAL_PLAN

ATTACH

DETACH

MULTI

COPY_DATABASE

**Type**: StatementType





### INVALID

Members:

INVALID

SELECT

INSERT

UPDATE

CREATE

DELETE

PREPARE

EXECUTE

ALTER

TRANSACTION

COPY

ANALYZE

VARIABLE_SET

CREATE_FUNC

EXPLAIN

DROP

EXPORT

PRAGMA

VACUUM

CALL

SET

LOAD

RELATION

EXTENSION

LOGICAL_PLAN

ATTACH

DETACH

MULTI

COPY_DATABASE

**Type**: StatementType





### LOAD

Members:

INVALID

SELECT

INSERT

UPDATE

CREATE

DELETE

PREPARE

EXECUTE

ALTER

TRANSACTION

COPY

ANALYZE

VARIABLE_SET

CREATE_FUNC

EXPLAIN

DROP

EXPORT

PRAGMA

VACUUM

CALL

SET

LOAD

RELATION

EXTENSION

LOGICAL_PLAN

ATTACH

DETACH

MULTI

COPY_DATABASE

**Type**: StatementType





### LOGICAL_PLAN

Members:

INVALID

SELECT

INSERT

UPDATE

CREATE

DELETE

PREPARE

EXECUTE

ALTER

TRANSACTION

COPY

ANALYZE

VARIABLE_SET

CREATE_FUNC

EXPLAIN

DROP

EXPORT

PRAGMA

VACUUM

CALL

SET

LOAD

RELATION

EXTENSION

LOGICAL_PLAN

ATTACH

DETACH

MULTI

COPY_DATABASE

**Type**: StatementType





### MULTI

Members:

INVALID

SELECT

INSERT

UPDATE

CREATE

DELETE

PREPARE

EXECUTE

ALTER

TRANSACTION

COPY

ANALYZE

VARIABLE_SET

CREATE_FUNC

EXPLAIN

DROP

EXPORT

PRAGMA

VACUUM

CALL

SET

LOAD

RELATION

EXTENSION

LOGICAL_PLAN

ATTACH

DETACH

MULTI

COPY_DATABASE

**Type**: StatementType





### PRAGMA

Members:

INVALID

SELECT

INSERT

UPDATE

CREATE

DELETE

PREPARE

EXECUTE

ALTER

TRANSACTION

COPY

ANALYZE

VARIABLE_SET

CREATE_FUNC

EXPLAIN

DROP

EXPORT

PRAGMA

VACUUM

CALL

SET

LOAD

RELATION

EXTENSION

LOGICAL_PLAN

ATTACH

DETACH

MULTI

COPY_DATABASE

**Type**: StatementType





### PREPARE

Members:

INVALID

SELECT

INSERT

UPDATE

CREATE

DELETE

PREPARE

EXECUTE

ALTER

TRANSACTION

COPY

ANALYZE

VARIABLE_SET

CREATE_FUNC

EXPLAIN

DROP

EXPORT

PRAGMA

VACUUM

CALL

SET

LOAD

RELATION

EXTENSION

LOGICAL_PLAN

ATTACH

DETACH

MULTI

COPY_DATABASE

**Type**: StatementType





### RELATION

Members:

INVALID

SELECT

INSERT

UPDATE

CREATE

DELETE

PREPARE

EXECUTE

ALTER

TRANSACTION

COPY

ANALYZE

VARIABLE_SET

CREATE_FUNC

EXPLAIN

DROP

EXPORT

PRAGMA

VACUUM

CALL

SET

LOAD

RELATION

EXTENSION

LOGICAL_PLAN

ATTACH

DETACH

MULTI

COPY_DATABASE

**Type**: StatementType





### SELECT

Members:

INVALID

SELECT

INSERT

UPDATE

CREATE

DELETE

PREPARE

EXECUTE

ALTER

TRANSACTION

COPY

ANALYZE

VARIABLE_SET

CREATE_FUNC

EXPLAIN

DROP

EXPORT

PRAGMA

VACUUM

CALL

SET

LOAD

RELATION

EXTENSION

LOGICAL_PLAN

ATTACH

DETACH

MULTI

COPY_DATABASE

**Type**: StatementType





### SET

Members:

INVALID

SELECT

INSERT

UPDATE

CREATE

DELETE

PREPARE

EXECUTE

ALTER

TRANSACTION

COPY

ANALYZE

VARIABLE_SET

CREATE_FUNC

EXPLAIN

DROP

EXPORT

PRAGMA

VACUUM

CALL

SET

LOAD

RELATION

EXTENSION

LOGICAL_PLAN

ATTACH

DETACH

MULTI

COPY_DATABASE

**Type**: StatementType





### TRANSACTION

Members:

INVALID

SELECT

INSERT

UPDATE

CREATE

DELETE

PREPARE

EXECUTE

ALTER

TRANSACTION

COPY

ANALYZE

VARIABLE_SET

CREATE_FUNC

EXPLAIN

DROP

EXPORT

PRAGMA

VACUUM

CALL

SET

LOAD

RELATION

EXTENSION

LOGICAL_PLAN

ATTACH

DETACH

MULTI

COPY_DATABASE

**Type**: StatementType





### UPDATE

Members:

INVALID

SELECT

INSERT

UPDATE

CREATE

DELETE

PREPARE

EXECUTE

ALTER

TRANSACTION

COPY

ANALYZE

VARIABLE_SET

CREATE_FUNC

EXPLAIN

DROP

EXPORT

PRAGMA

VACUUM

CALL

SET

LOAD

RELATION

EXTENSION

LOGICAL_PLAN

ATTACH

DETACH

MULTI

COPY_DATABASE

**Type**: StatementType





### VACUUM

Members:

INVALID

SELECT

INSERT

UPDATE

CREATE

DELETE

PREPARE

EXECUTE

ALTER

TRANSACTION

COPY

ANALYZE

VARIABLE_SET

CREATE_FUNC

EXPLAIN

DROP

EXPORT

PRAGMA

VACUUM

CALL

SET

LOAD

RELATION

EXTENSION

LOGICAL_PLAN

ATTACH

DETACH

MULTI

COPY_DATABASE

**Type**: StatementType





### VARIABLE_SET

Members:

INVALID

SELECT

INSERT

UPDATE

CREATE

DELETE

PREPARE

EXECUTE

ALTER

TRANSACTION

COPY

ANALYZE

VARIABLE_SET

CREATE_FUNC

EXPLAIN

DROP

EXPORT

PRAGMA

VACUUM

CALL

SET

LOAD

RELATION

EXTENSION

LOGICAL_PLAN

ATTACH

DETACH

MULTI

COPY_DATABASE

**Type**: StatementType



































































### name

name(self: object) -> str

**Type**: property





### value



**Type**: property



































## apilevel

str(object='') -> str
str(bytes_or_buffer[, encoding[, errors]]) -> str

Create a new string object from the given object. If encoding or
errors is specified, then the object must expose a data buffer
that will be decoded using the given encoding and error handler.
Otherwise, returns the result of object.__str__() (if defined)
or repr(object).
encoding defaults to sys.getdefaultencoding().
errors defaults to 'strict'.

**Type**: str





## comment

Members:

identifier

numeric_const

string_const

operator

keyword

comment

**Type**: token_type





## identifier

Members:

identifier

numeric_const

string_const

operator

keyword

comment

**Type**: token_type





## keyword

Members:

identifier

numeric_const

string_const

operator

keyword

comment

**Type**: token_type





## numeric_const

Members:

identifier

numeric_const

string_const

operator

keyword

comment

**Type**: token_type





## operator

Members:

identifier

numeric_const

string_const

operator

keyword

comment

**Type**: token_type





## paramstyle

str(object='') -> str
str(bytes_or_buffer[, encoding[, errors]]) -> str

Create a new string object from the given object. If encoding or
errors is specified, then the object must expose a data buffer
that will be decoded using the given encoding and error handler.
Otherwise, returns the result of object.__str__() (if defined)
or repr(object).
encoding defaults to sys.getdefaultencoding().
errors defaults to 'strict'.

**Type**: str





## string_const

Members:

identifier

numeric_const

string_const

operator

keyword

comment

**Type**: token_type





## threadsafety

int([x]) -> integer
int(x, base=10) -> integer

Convert a number or string to an integer, or return 0 if no arguments
are given.  If x is a number, return x.__int__().  For floating point
numbers, this truncates towards zero.

If x is not a number or if base is given, then x must be a string,
bytes, or bytearray instance representing an integer literal in the
given base.  The literal can be preceded by '+' or '-' and be surrounded
by whitespace.  The base defaults to 10.  Valid bases are 0 and 2-36.
Base 0 means to interpret the base from the string as an integer literal.
>>> int('0b100', base=0)
4

**Type**: int





## token_type

Members:

identifier

numeric_const

string_const

operator

keyword

comment

**Type**: pybind11_type

**Bases**: pybind11_object



































































### comment

Members:

identifier

numeric_const

string_const

operator

keyword

comment

**Type**: token_type





### identifier

Members:

identifier

numeric_const

string_const

operator

keyword

comment

**Type**: token_type





### keyword

Members:

identifier

numeric_const

string_const

operator

keyword

comment

**Type**: token_type





### name

name(self: object) -> str

**Type**: property





### numeric_const

Members:

identifier

numeric_const

string_const

operator

keyword

comment

**Type**: token_type





### operator

Members:

identifier

numeric_const

string_const

operator

keyword

comment

**Type**: token_type





### string_const

Members:

identifier

numeric_const

string_const

operator

keyword

comment

**Type**: token_type





### value



**Type**: property




## Expressions


### CaseExpression

CaseExpression(condition: duckdb.duckdb.Expression, value: duckdb.duckdb.Expression) -> duckdb.duckdb.Expression

**Type**: builtin_function_or_method





### CoalesceOperator

CoalesceOperator(*args) -> duckdb.duckdb.Expression

**Type**: builtin_function_or_method





### ColumnExpression

ColumnExpression(*args) -> duckdb.duckdb.Expression

Create a column reference from the provided column name

**Type**: builtin_function_or_method





### ConstantExpression

ConstantExpression(value: object) -> duckdb.duckdb.Expression

Create a constant expression from the provided value

**Type**: builtin_function_or_method





### DefaultExpression

DefaultExpression() -> duckdb.duckdb.Expression

**Type**: builtin_function_or_method





### FunctionExpression

FunctionExpression(function_name: str, *args) -> duckdb.duckdb.Expression

**Type**: builtin_function_or_method





### LambdaExpression

LambdaExpression(lhs: object, rhs: duckdb.duckdb.Expression) -> duckdb.duckdb.Expression

**Type**: builtin_function_or_method





### StarExpression

StarExpression(*args, **kwargs)
Overloaded function.

1. StarExpression(*, exclude: object = None) -> duckdb.duckdb.Expression

2. StarExpression() -> duckdb.duckdb.Expression

**Type**: builtin_function_or_method




## Values


### BinaryValue



**Type**: type

**Bases**: Value



### BitValue



**Type**: type

**Bases**: Value



### BlobValue



**Type**: type

**Bases**: Value



### BooleanValue



**Type**: type

**Bases**: Value



### DateValue



**Type**: type

**Bases**: Value



### DecimalValue



**Type**: type

**Bases**: Value



### DoubleValue



**Type**: type

**Bases**: Value



### FloatValue



**Type**: type

**Bases**: Value



### HugeIntegerValue



**Type**: type

**Bases**: Value



### IntegerValue



**Type**: type

**Bases**: Value



### IntervalValue



**Type**: type

**Bases**: Value



### LongValue



**Type**: type

**Bases**: Value



### NullValue



**Type**: type

**Bases**: Value



### ShortValue



**Type**: type

**Bases**: Value



### StringValue



**Type**: type

**Bases**: Value



### TimeTimeZoneValue



**Type**: type

**Bases**: Value



### TimeValue



**Type**: type

**Bases**: Value



### TimestampMilisecondValue



**Type**: type

**Bases**: Value



### TimestampNanosecondValue



**Type**: type

**Bases**: Value



### TimestampSecondValue



**Type**: type

**Bases**: Value



### TimestampTimeZoneValue



**Type**: type

**Bases**: Value



### TimestampValue



**Type**: type

**Bases**: Value



### UUIDValue



**Type**: type

**Bases**: Value



### UnsignedBinaryValue



**Type**: type

**Bases**: Value



### UnsignedIntegerValue



**Type**: type

**Bases**: Value



### UnsignedLongValue



**Type**: type

**Bases**: Value



### UnsignedShortValue



**Type**: type

**Bases**: Value



### Value



**Type**: type

**Bases**: object


## Exceptions


### BinderException

Common base class for all non-exit exceptions.

**Type**: type

**Bases**: ProgrammingError



### CatalogException

Common base class for all non-exit exceptions.

**Type**: type

**Bases**: ProgrammingError



### ConnectionException

Common base class for all non-exit exceptions.

**Type**: type

**Bases**: OperationalError



### ConstraintException

Common base class for all non-exit exceptions.

**Type**: type

**Bases**: IntegrityError



### ConversionException

Common base class for all non-exit exceptions.

**Type**: type

**Bases**: DataError



### DataError

Common base class for all non-exit exceptions.

**Type**: type

**Bases**: DatabaseError



### Error

Common base class for all non-exit exceptions.

**Type**: type

**Bases**: Exception



### FatalException

Common base class for all non-exit exceptions.

**Type**: type

**Bases**: DatabaseError



### HTTPException

Thrown when an error occurs in the httpfs extension, or whilst downloading an extension.

**Type**: type

**Bases**: IOException



### IOException

Common base class for all non-exit exceptions.

**Type**: type

**Bases**: OperationalError



### IntegrityError

Common base class for all non-exit exceptions.

**Type**: type

**Bases**: DatabaseError



### InternalError

Common base class for all non-exit exceptions.

**Type**: type

**Bases**: DatabaseError



### InternalException

Common base class for all non-exit exceptions.

**Type**: type

**Bases**: InternalError



### InterruptException

Common base class for all non-exit exceptions.

**Type**: type

**Bases**: DatabaseError



### InvalidInputException

Common base class for all non-exit exceptions.

**Type**: type

**Bases**: ProgrammingError



### InvalidTypeException

Common base class for all non-exit exceptions.

**Type**: type

**Bases**: ProgrammingError



### NotImplementedException

Common base class for all non-exit exceptions.

**Type**: type

**Bases**: NotSupportedError



### NotSupportedError

Common base class for all non-exit exceptions.

**Type**: type

**Bases**: DatabaseError



### OperationalError

Common base class for all non-exit exceptions.

**Type**: type

**Bases**: DatabaseError



### OutOfMemoryException

Common base class for all non-exit exceptions.

**Type**: type

**Bases**: OperationalError



### OutOfRangeException

Common base class for all non-exit exceptions.

**Type**: type

**Bases**: DataError



### ParserException

Common base class for all non-exit exceptions.

**Type**: type

**Bases**: ProgrammingError



### PermissionException

Common base class for all non-exit exceptions.

**Type**: type

**Bases**: DatabaseError



### ProgrammingError

Common base class for all non-exit exceptions.

**Type**: type

**Bases**: DatabaseError



### SequenceException

Common base class for all non-exit exceptions.

**Type**: type

**Bases**: DatabaseError



### SerializationException

Common base class for all non-exit exceptions.

**Type**: type

**Bases**: OperationalError



### SyntaxException

Common base class for all non-exit exceptions.

**Type**: type

**Bases**: ProgrammingError



### TransactionException

Common base class for all non-exit exceptions.

**Type**: type

**Bases**: OperationalError



### TypeMismatchException

Common base class for all non-exit exceptions.

**Type**: type

**Bases**: DataError



### Warning

Common base class for all non-exit exceptions.

**Type**: type

**Bases**: Exception
