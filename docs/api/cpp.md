---
layout: docu
title: C++ API
selected: C++
---
## Installation
The DuckDB C++ API can be installed as part of the `libduckdb` packages. Please see the [installation page](/docs/installation?environment=cplusplus) for details.

## Basic API Usage
DuckDB implements a custom C++ API. This is built around the abstractions of a database instance (`DuckDB` class), multiple `Connection`s to the database instance and `QueryResult` instances as the result of queries. The header file for the C++ API is `duckdb.hpp`. 

> The standard source distribution of `libduckdb` contains an "amalgamation" of the DuckDB sources, which combine all sources into two files `duckdb.hpp` and `duckdb.cpp`. The `duckdb.hpp` header is much larger in this case. Regardless of whether you are using the amalgamation or not, just include `duckdb.hpp`.

### Startup & Shutdown

To use DuckDB, you must first initialize a `DuckDB` instance using its constructor. `DuckDB()` takes as parameter the database file to read and write from. The special value `nullptr` can be used to create an **in-memory database**. Note that for an in-memory database no data is persisted to disk (i.e. all data is lost when you exit the process). The second parameter to the `DuckDB` constructor is an optional `DBConfig` object. In `DBConfig`, you can set various database parameters, for example the read/write mode or memory limits. The `DuckDB` constructor may throw exceptions, for example if the database file is not usable.

With the `DuckDB` instance, you can create one or many `Connection` instances using the `Connection()` constructor. While connections should be thread-safe, they will be locked during querying. It is therefore recommended that each thread uses its own connection if you are in a multithreaded environment.


```c++
DuckDB db(nullptr);
Connection con(db);
```

### Querying
Connections expose the `Query()` method to send a SQL query string to DuckDB from C++. `Query()` fully materializes the query result as a `MaterializedQueryResult` in memory before returning at which point the query result can be consumed. There is also a streaming API for queries, see further below.

```c++
// create a table
con.Query("CREATE TABLE integers(i INTEGER, j INTEGER)");

// insert three rows into the table
con.Query("INSERT INTO integers VALUES (3, 4), (5, 6), (7, NULL)";

MaterializedQueryResult result = con.Query("SELECT * FROM integers");
if (!result->success) {
	cerr << result->error;
}
```

The `MaterializedQueryResult` instance contains firstly two fields that indicate whether the query was successful. `Query` will not throw exceptions under normal circumstances. Instead, invalid queries or other issues will lead to the `success` boolean field in the query result instance to be set to `false`. In this case an error message may be available in `error` as a string. If successful, other fields are set: The type of statement that was just executed (e.g. `StatementType::INSERT_STATEMENT`) is contained in `statement_type`. The high-level ("SQL type") types of the result set columns are in `sql_types` and the low-level data representation types are in `types`. The names of the result columns are in the `names` string vector. In case multiple result sets are returned, for example because the result set contained multiple statements, the result set can be chained using the `next` field. 

```c++
// TODO
```

DuckDB also supports prepared statements in the C++ API with the `Prepare()` method. This returns an instance of `PreparedStatement`. This instance can be used to execute the prepared statement with parameters. Below is an example:

```c++
// TODO
```

> Do **not** use prepared statements to insert large amounts of data into DuckDB. See [the data import documentation](/docs/data/overview) for better options.

### Streaming Queries


### UDF API

The UDF API is exposed in duckdb:Connection through the methods: `CreateScalarFunction()` and `CreateVectorizedFunction()` and variants. 
These methods created UDFs into the temporary schema (TEMP_SCHEMA) of the owner connection that is the only one allowed to use and change them.

#### CreateScalarFunction

The user can code an ordinary scalar function and invoke the `CreateScalarFunction()` to register and afterward use the UDF in a _SELECT_ statement, for instance:

```c++
bool bigger_than_four(int value) {
    return value > 4;
}

connection.CreateScalarFunction<bool, int>("bigger_than_four", &bigger_than_four);

connection.Query("SELECT bigger_than_four(i) FROM (VALUES(3), (5)) tbl(i)")->Print();
```

The `CreateScalarFunction()` methods automatically creates vectorized scalar UDFs so they are as efficient as built-in functions, we have two variants of this method interface as follows:

**1.** `template<typename TR, typename... Args>\ void CreateScalarFunction(string name, TR (*udf_func)(Args…))`

- template parameters:
    - **TR** is the return type of the UDF function;
    - **Args** are the arguments up to 3 for the UDF function (this method only supports until ternary functions);
- **name**: is the name to register the UDF function;
- **udf_func**: is a pointer to the UDF function.

This method automatically discovers from the template typenames the corresponding SQLTypes:

- bool → SQLType::BOOLEAN;
- int8_t → SQLType::TINYINT;
- int16_t → SQLType::SMALLINT
- int32_t → SQLType::INTEGER
- int64_t  → SQLType::BIGINT
- float → SQLType::FLOAT
- double → SQLType::DOUBLE
- string_t → SQLType::VARCHAR

*In DuckDB some primitive types, e.g., _int32_t_, are mapped to the same SQLType: INTEGER, TIME and DATE, then for disambiguation the users can use the following overloaded method.

**2.** `template<typename TR, typename... Args> void CreateScalarFunction(string name, vector<SQLType> args, SQLType ret_type, TR (*udf_func)(Args…))`

An example of use would be:

```c++
int32_t udf_date(int32_t a) {
	return a;
}

con.Query("CREATE TABLE dates (d DATE)");
con.Query("INSERT INTO dates VALUES ('1992-01-01')");

con.CreateScalarFunction<int32_t, int32_t>("udf_date", {SQLType::DATE}, SQLType::DATE, &udf_date);

con.Query("SELECT udf_date(d) FROM dates")->Print();

```

- template parameters:
    - **TR** is the return type of the UDF function;
    - **Args** are the arguments up to 3 for the UDF function (this method only supports until ternary functions);
- **name**: is the name to register the UDF function;
- **args**: are the SQLType arguments that the function uses, which should match with the template Args types;
- **ret_type**: is the SQLType of return of the function, which should match with the template TR type;
- **udf_func**: is a pointer to the UDF function.

This function checks the template types against the SQLTypes passed as arguments and they must match as follow:

- SQLTypeId::BOOLEAN → bool
- SQLTypeId::TINYINT → int8_t
- SQLTypeId::SMALLINT → int16_t
- SQLTypeId::DATE, SQLTypeId::TIME, SQLTypeId::INTEGER → int32_t
- SQLTypeId::BIGINT, SQLTypeId::TIMESTAMP → int64_t
- SQLTypeId::FLOAT, SQLTypeId::DOUBLE, SQLTypeId::DECIMAL → double
- SQLTypeId::VARCHAR, SQLTypeId::CHAR, SQLTypeId::BLOB → string_t
- SQLTypeId::VARBINARY → blob_t

#### CreateVectorizedFunction

The `CreateVectorizedFunction()` methods register a vectorized UDF such as:

```c++
/*
* This vectorized function copies the input values to the result vector
*/
template<typename TYPE>
static void udf_vectorized(DataChunk &args, ExpressionState &state, Vector &result) {
	// set the result vector type
	result.vector_type = VectorType::FLAT_VECTOR;
	// get a raw array from the result
	auto result_data = FlatVector::GetData<TYPE>(result);

	// get the solely input vector
	auto &input = args.data[0];
	// now get an orrified vector
	VectorData vdata;
	input.Orrify(args.size(), vdata);

	// get a raw array from the orrified input
	auto input_data = (TYPE *)vdata.data;

	// handling the data
	for (idx_t i = 0; i < args.size(); i++) {
		auto idx = vdata.sel->get_index(i);
		if ((*vdata.nullmask)[idx]) {
			continue;
		}
		result_data[i] = input_data[idx];
	}
}

con.Query("CREATE TABLE integers (i INTEGER)");
con.Query("INSERT INTO integers VALUES (1), (2), (3), (999)");

con.CreateVectorizedFunction<int, int>("udf_vectorized_int", &&udf_vectorized<int>);

con.Query("SELECT udf_vectorized_int(i) FROM integers")->Print();
```

The Vectorized UDF is a pointer of the type _scalar_function_t_:

`typedef std::function<void(DataChunk &args, ExpressionState &expr, Vector &result)> scalar_function_t;`

- **args** is a [DataChunk](https://github.com/cwida/duckdb/blob/master/src/include/duckdb/common/types/data_chunk.hpp) that holds a set of input vectors for the UDF that all have the same length;
- **expr** is an [ExpressionState](https://github.com/cwida/duckdb/blob/master/src/include/duckdb/execution/expression_executor_state.hpp) that provides information to the query's expression state;
- **result**: is a [Vector](https://github.com/cwida/duckdb/blob/master/src/include/duckdb/common/types/vector.hpp) to store the result values.

There are different vector types to handle in a Vectorized UDF:
- ConstantVector;
- DictionaryVector;
- FlatVector;
- ListVector;
- StringVector;
- StructVector;
- SequenceVector.


The general API of the `CreateVectorizedFunction()` method is as follows:

**1.** `template<typename TR, typename... Args> void CreateVectorizedFunction(string name, scalar_function_t udf_func, SQLType varargs = SQLType::INVALID)`

- template parameters:
    - **TR** is the return type of the UDF function;
    - **Args** are the arguments up to 3 for the UDF function.
- **name** is the name to register the UDF function;
- **udf_func** is a _vectorized_ UDF function;
- **varargs** The type of varargs to support, or SQLTypeId::INVALID (default value) if the function does not accept variable length arguments. 

This method automatically discovers from the template typenames the corresponding SQLTypes:

- bool → SQLType::BOOLEAN;
- int8_t → SQLType::TINYINT;
- int16_t → SQLType::SMALLINT
- int32_t → SQLType::INTEGER
- int64_t  → SQLType::BIGINT
- float → SQLType::FLOAT
- double → SQLType::DOUBLE
- string_t → SQLType::VARCHAR

**2.** `template<typename TR, typename... Args> void CreateVectorizedFunction(string name, vector<SQLType> args, SQLType ret_type, scalar_function_t udf_func, SQLType varargs = SQLType::INVALID)`

```c++
// TODO
```