---
layout: docu
title: C++ API
---

> Tip To use the DuckDB C++ API, download the [`libduckdb` archive]({% link install/index.html %}?environment=c) for your platform.
>
> The latest stable version of the DuckDB C++ API is {{ site.current_duckdb_version }}.

> Warning DuckDB's C++ API is internal.
> It is not guaranteed to be stable and can change without notice.
> If you would like to build an application on DuckDB, we recommend using the [C API]({% link docs/preview/clients/c/overview.md %}).

## Installation

The DuckDB C++ API can be installed as part of the `libduckdb` packages. Please see the [installation page]({% link install/index.html %}?environment=cplusplus) for details.

## Basic API Usage

DuckDB implements a custom C++ API. This is built around the abstractions of a database instance (`DuckDB` class), multiple `Connection`s to the database instance and `QueryResult` instances as the result of queries. The header file for the C++ API is `duckdb.hpp`.

### Startup & Shutdown

To use DuckDB, you must first initialize a `DuckDB` instance using its constructor. `DuckDB()` takes as parameter the database file to read and write from. The special value `nullptr` can be used to create an **in-memory database**. Note that for an in-memory database no data is persisted to disk (i.e., all data is lost when you exit the process). The second parameter to the `DuckDB` constructor is an optional `DBConfig` object. In `DBConfig`, you can set various database parameters, for example the read/write mode or memory limits. The `DuckDB` constructor may throw exceptions, for example if the database file is not usable.

With the `DuckDB` instance, you can create one or many `Connection` instances using the `Connection()` constructor. While connections should be thread-safe, they will be locked during querying. It is therefore recommended that each thread uses its own connection if you are in a multithreaded environment.

```cpp
DuckDB db(nullptr);
Connection con(db);
```

### Querying

Connections expose the `Query()` method to send a SQL query string to DuckDB from C++. `Query()` fully materializes the query result as a `MaterializedQueryResult` in memory before returning at which point the query result can be consumed. There is also a streaming API for queries, see further below.

```cpp
// create a table
con.Query("CREATE TABLE integers (i INTEGER, j INTEGER)");

// insert three rows into the table
con.Query("INSERT INTO integers VALUES (3, 4), (5, 6), (7, NULL)");

auto result = con.Query("SELECT * FROM integers");
if (result->HasError()) {
    cerr << result->GetError() << endl;
} else {
    cout << result->ToString() << endl;
}
```

The `MaterializedQueryResult` instance contains firstly two fields that indicate whether the query was successful. `Query` will not throw exceptions under normal circumstances. Instead, invalid queries or other issues will lead to the `success` Boolean field in the query result instance to be set to `false`. In this case an error message may be available in `error` as a string. The methods `GetErrorType()` and `GetErrorObject()` are also available for any `QueryResult` instance which may aid in more explicit error handling. 

```cpp
auto result = con.Query("INSERT INTO integers VALUES (1, 2)");
if (result->HasError()) {
    auto errorType = result->GetErrorType();
    switch (errorType) {
    case duckdb::ExceptionType::CONSTRAINT: {
        // Example handling
        auto errorObject = result->GetErrorObject();
        errorObject.ConvertErrorToJSON(); 
        std::cout << errorObject.Message() << std::endl;
        break;
    }
    // More handling
    }
} else {
    // Normal code
}
```

If successful, other fields are set: the type of statement that was just executed (e.g., `StatementType::INSERT_STATEMENT`) is contained in `statement_type`. The high-level (“Logical type”/“SQL type”) types of the result set columns are in `types`. The names of the result columns are in the `names` string vector. In case multiple result sets are returned, for example because the result set contained multiple statements, the result set can be chained using the `next` field.

DuckDB also supports prepared statements in the C++ API with the `Prepare()` method. This returns an instance of `PreparedStatement`. This instance can be used to execute the prepared statement with parameters. Below is an example:

```cpp
std::unique_ptr<PreparedStatement> prepare = con.Prepare("SELECT count(*) FROM a WHERE i = $1");
std::unique_ptr<QueryResult> result = prepare->Execute(12);
```

> Warning Do **not** use prepared statements to insert large amounts of data into DuckDB. See the [data import documentation]({% link docs/preview/data/overview.md %}) for better options.

### UDF API

The UDF API allows the definition of user-defined functions. It is exposed in `duckdb:Connection` through the methods: `CreateScalarFunction()`, `CreateVectorizedFunction()`, and variants.
These methods create UDFs in the temporary schema (`TEMP_SCHEMA`) of the owner connection that is the only one allowed to use and change them.

#### CreateScalarFunction

The user can code an ordinary scalar function and invoke the `CreateScalarFunction()` to register and afterward use the UDF in a `SELECT` statement, for instance:

```cpp
bool bigger_than_four(int value) {
    return value > 4;
}

connection.CreateScalarFunction<bool, int>("bigger_than_four", &bigger_than_four);

connection.Query("SELECT bigger_than_four(i) FROM (VALUES (3), (5)) tbl(i)")->Print();
```

The `CreateScalarFunction()` methods automatically create vectorized scalar UDFs so they are as efficient as built-in functions, we have two variants of this method interface as follows:

**1.**

```cpp
template<typename TR, typename... Args>
void CreateScalarFunction(string name, TR (*udf_func)(Args…))
```

* template parameters:
    * **TR** is the return type of the UDF function.
    * **Args** are the arguments up to 3 for the UDF function (this method only supports until ternary functions).
* **name** is the name to register the UDF function.
* **udf_func** is a pointer to the UDF function.

This method automatically discovers from the template typenames the corresponding LogicalTypes:

* `bool` → `LogicalType::BOOLEAN`
* `int8_t` → `LogicalType::TINYINT`
* `int16_t` → `LogicalType::SMALLINT`
* `int32_t` → `LogicalType::INTEGER`
* `int64_t` → `LogicalType::BIGINT`
* `float` → `LogicalType::FLOAT`
* `double` → `LogicalType::DOUBLE`
* `string_t` → `LogicalType::VARCHAR`

In DuckDB some primitive types, e.g., `int32_t`, are mapped to the same `LogicalType`: `INTEGER`, `TIME` and `DATE`, then for disambiguation the users can use the following overloaded method.

**2.**

```cpp
template<typename TR, typename... Args>
void CreateScalarFunction(string name, vector<LogicalType> args, LogicalType ret_type, TR (*udf_func)(Args…))
```

An example of use would be:

```cpp
int32_t udf_date(int32_t a) {
    return a;
}

con.Query("CREATE TABLE dates (d DATE)");
con.Query("INSERT INTO dates VALUES ('1992-01-01')");

con.CreateScalarFunction<int32_t, int32_t>("udf_date", {LogicalType::DATE}, LogicalType::DATE, &udf_date);

con.Query("SELECT udf_date(d) FROM dates")->Print();
```

* template parameters:
    * **TR** is the return type of the UDF function.
    * **Args** are the arguments up to 3 for the UDF function (this method only supports until ternary functions).
* **name** is the name to register the UDF function.
* **args** are the LogicalType arguments that the function uses, which should match with the template Args types.
* **ret_type** is the LogicalType of return of the function, which should match with the template TR type.
* **udf_func** is a pointer to the UDF function.

This function checks the template types against the LogicalTypes passed as arguments and they must match as follows:

* LogicalTypeId::BOOLEAN → bool
* LogicalTypeId::TINYINT → int8_t
* LogicalTypeId::SMALLINT → int16_t
* LogicalTypeId::DATE, LogicalTypeId::TIME, LogicalTypeId::INTEGER → int32_t
* LogicalTypeId::BIGINT, LogicalTypeId::TIMESTAMP → int64_t
* LogicalTypeId::FLOAT, LogicalTypeId::DOUBLE, LogicalTypeId::DECIMAL → double
* LogicalTypeId::VARCHAR, LogicalTypeId::CHAR, LogicalTypeId::BLOB → string_t
* LogicalTypeId::VARBINARY → blob_t

#### CreateVectorizedFunction

The `CreateVectorizedFunction()` methods register a vectorized UDF such as:

```cpp
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

```cpp
typedef std::function<void(DataChunk &args, ExpressionState &expr, Vector &result)> scalar_function_t;
```

* **args** is a [DataChunk](https://github.com/duckdb/duckdb/blob/main/src/include/duckdb/common/types/data_chunk.hpp) that holds a set of input vectors for the UDF that all have the same length.
* **expr** is an [ExpressionState](https://github.com/duckdb/duckdb/blob/main/src/include/duckdb/execution/expression_executor_state.hpp) that provides information to the query's expression state.
* **result** is a [Vector](https://github.com/duckdb/duckdb/blob/main/src/include/duckdb/common/types/vector.hpp) to store the result values.

There are different vector types to handle in a Vectorized UDF:

* ConstantVector
* DictionaryVector
* FlatVector
* ListVector
* StringVector
* StructVector
* SequenceVector

The general API of the `CreateVectorizedFunction()` method is as follows:

**1.**

```cpp
template<typename TR, typename... Args>
void CreateVectorizedFunction(string name, scalar_function_t udf_func, LogicalType varargs = LogicalType::INVALID)
```

* template parameters:
    * **TR** is the return type of the UDF function.
    * **Args** are the arguments up to 3 for the UDF function.
* **name** is the name to register the UDF function.
* **udf_func** is a _vectorized_ UDF function.
* **varargs** The type of varargs to support, or LogicalTypeId::INVALID (default value) if the function does not accept variable length arguments.

This method automatically discovers from the template typenames the corresponding LogicalTypes:

* `bool` → `LogicalType::BOOLEAN`
* `int8_t` → `LogicalType::TINYINT`
* `int16_t` → `LogicalType::SMALLINT`
* `int32_t` → `LogicalType::INTEGER`
* `int64_t` → `LogicalType::BIGINT`
* `float` → `LogicalType::FLOAT`
* `double` → `LogicalType::DOUBLE`
* `string_t` → `LogicalType::VARCHAR`

**2.**

```cpp
template<typename TR, typename... Args>
void CreateVectorizedFunction(string name, vector<LogicalType> args, LogicalType ret_type, scalar_function_t udf_func, LogicalType varargs = LogicalType::INVALID)
```
