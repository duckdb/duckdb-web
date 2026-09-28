---
layout: docu
title: 'ODBC 101: A Duck Themed Guide to ODBC'
---

## What is ODBC?

[ODBC](https://learn.microsoft.com/en-us/sql/odbc/microsoft-open-database-connectivity-odbc?view=sql-server-ver16) which stands for Open Database Connectivity, is a standard that allows different programs to talk to different databases including, of course, DuckDB. This makes it easier to build programs that work with many different databases, which saves time as developers don't have to write custom code to connect to each database. Instead, they can use the standardized ODBC interface, which reduces development time and costs, and programs are easier to maintain. However, ODBC can be slower than other methods of connecting to a database, such as using a native driver, as it adds an extra layer of abstraction between the application and the database. Furthermore, because DuckDB is column-based and ODBC is row-based, there can be some inefficiencies when using ODBC with DuckDB.

> There are links throughout this page to the official [Microsoft ODBC documentation](https://learn.microsoft.com/en-us/sql/odbc/reference/odbc-programmer-s-reference?view=sql-server-ver16), which is a great resource for learning more about ODBC.

## General Concepts

* [Handles](#handles)
* [Connecting](#connecting)
* [Error Handling and Diagnostics](#error-handling-and-diagnostics)
* [Buffers and Binding](#buffers-and-binding)

### Handles

A [handle](https://learn.microsoft.com/en-us/sql/odbc/reference/develop-app/handles?view=sql-server-ver16) is a pointer to a specific ODBC object which is used to interact with the database. There are several different types of handles, each with a different purpose, these are the environment handle, the connection handle, the statement handle, and the descriptor handle. Handles are allocated using the [`SQLAllocHandle`](https://learn.microsoft.com/en-us/sql/odbc/reference/syntax/sqlallochandle-function?view=sql-server-ver16) which takes as input the type of handle to allocate, and a pointer to the handle, the driver then creates a new handle of the specified type, which it returns to the application.

The DuckDB ODBC driver has the following handle types.

#### Environment

<div class="nostroke_table"></div>

| **Handle name** | [Environment](https://learn.microsoft.com/en-us/sql/odbc/reference/develop-app/environment-handles?view=sql-server-ver16) |
| **Type name** | `SQL_HANDLE_ENV` |
| **Description** | Manages the environment settings for ODBC operations, and provides a global context in which to access data. |
| **Use case** | Initializing ODBC, managing driver behavior, resource allocation. |
| **Additional information** | Must be [allocated](https://learn.microsoft.com/en-us/sql/odbc/reference/develop-app/allocating-the-environment-handle?view=sql-server-ver16) once per application upon starting, and freed at the end. |

#### Connection

<div class="nostroke_table"></div>

| **Handle name** | [Connection](https://learn.microsoft.com/en-us/sql/odbc/reference/develop-app/connection-handles?view=sql-server-ver16) |
| **Type name** | `SQL_HANDLE_DBC` |
| **Description** | Represents a connection to a data source. Used to establish, manage, and terminate connections. Defines both the driver and the data source to use within the driver. |
| **Use case** | Establishing a connection to a database, managing the connection state. |
| **Additional information** | Multiple connection handles can be [created](https://learn.microsoft.com/en-us/sql/odbc/reference/develop-app/allocating-a-connection-handle-odbc?view=sql-server-ver16) as needed, allowing simultaneous connections to multiple data sources. *Note:* Allocating a connection handle does not establish a connection, but must be allocated first, and then used once the connection has been established. |

#### Statement

<div class="nostroke_table"></div>

| **Handle name** | [Statement](https://learn.microsoft.com/en-us/sql/odbc/reference/develop-app/statement-handles?view=sql-server-ver16) |
| **Type name** | `SQL_HANDLE_STMT` |
| **Description** | Handles the execution of SQL statements, as well as the returned result sets. |
| **Use case** | Executing SQL queries, fetching result sets, managing statement options. |
| **Additional information** | To facilitate the execution of concurrent queries, multiple handles can be [allocated](https://learn.microsoft.com/en-us/sql/odbc/reference/develop-app/allocating-a-statement-handle-odbc?view=sql-server-ver16) per connection. |

#### Descriptor

<div class="nostroke_table"></div>

| **Handle name** | [Descriptor](https://learn.microsoft.com/en-us/sql/odbc/reference/develop-app/descriptor-handles?view=sql-server-ver16) |
| **Type name** | `SQL_HANDLE_DESC` |
| **Description** | Describes the attributes of a data structure or parameter, and allows the application to specify the structure of data to be bound/retrieved. |
| **Use case** | Describing table structures, result sets, binding columns to application buffers. |
| **Additional information** | Used in situations where data structures need to be explicitly defined, for example during parameter binding or result set fetching. They are automatically allocated when a statement is allocated, but can also be allocated explicitly. |

### Connecting

The first step is to connect to the data source so that the application can perform database operations. First the application must allocate an environment handle, and then a connection handle. The connection handle is then used to connect to the data source. There are two functions which can be used to connect to a data source, [`SQLDriverConnect`](https://learn.microsoft.com/en-us/sql/odbc/reference/syntax/sqldriverconnect-function?view=sql-server-ver16) and [`SQLConnect`](https://learn.microsoft.com/en-us/sql/odbc/reference/syntax/sqlconnect-function?view=sql-server-ver16). The former is used to connect to a data source using a connection string, while the latter is used to connect to a data source using a DSN.

#### Connection String

A [connection string](https://learn.microsoft.com/en-us/sql/odbc/reference/develop-app/connection-strings?view=sql-server-ver16) is a string which contains the information needed to connect to a data source. It is formatted as a semicolon separated list of key-value pairs, however DuckDB currently only utilizes the DSN and ignores the rest of the parameters.

#### DSN

A DSN (_Data Source Name_) is a string that identifies a database. It can be a file path, URL, or a database name. For example, `C:\Users\me\duckdb.db` and `DuckDB` are both valid DSNs. More information on DSNs can be found on the [“Choosing a Data Source or Driver” page of the SQL Server documentation](https://learn.microsoft.com/en-us/sql/odbc/reference/develop-app/choosing-a-data-source-or-driver?view=sql-server-ver16).

### Error Handling and Diagnostics

All functions in ODBC return a code which represents the success or failure of the function. This allows for easy error handling, as the application can simply check the return code of each function call to determine if it was successful. When unsuccessful, the application can then use the [`SQLGetDiagRec`](https://learn.microsoft.com/en-us/sql/odbc/reference/syntax/sqlgetdiagrec-function?view=sql-server-ver16) function to retrieve the error information. The following table defines the [return codes](https://learn.microsoft.com/en-us/sql/odbc/reference/develop-app/return-codes-odbc?view=sql-server-ver16):

| Return code             | Description                                        |
|-------------------------|----------------------------------------------------|
| `SQL_SUCCESS`           | The function completed successfully.                                                                                                           |
| `SQL_SUCCESS_WITH_INFO` | The function completed successfully, but additional information is available, including a warning.                                             |
| `SQL_ERROR`             | The function failed.                                                                                                                           |
| `SQL_INVALID_HANDLE`    | The handle provided was invalid, indicating a programming error, i.e., when a handle is not allocated before it is used, or is the wrong type. |
| `SQL_NO_DATA`           | The function completed successfully, but no more data is available.                                                                            |
| `SQL_NEED_DATA`         | More data is needed, such as when a parameter data is sent at execution time, or additional connection information is required.                |
| `SQL_STILL_EXECUTING`   | A function that was asynchronously executed is still executing.                                                                                |

### Buffers and Binding

A buffer is a block of memory used to store data. Buffers are used to store data retrieved from the database, or to send data to the database. Buffers are allocated by the application, and then bound to a column in a result set, or a parameter in a query, using the [`SQLBindCol`](https://learn.microsoft.com/en-us/sql/odbc/reference/syntax/sqlbindcol-function?view=sql-server-ver16) and [`SQLBindParameter`](https://learn.microsoft.com/en-us/sql/odbc/reference/syntax/sqlbindparameter-function?view=sql-server-ver16) functions. When the application fetches a row from the result set, or executes a query, the data is stored in the buffer. When the application sends a query to the database, the data in the buffer is sent to the database.

## Setting up an Application

The following is a step-by-step guide to setting up an application that uses ODBC to connect to a database, execute a query, and fetch the results in `C++`.

> To install the driver as well as anything else you will need follow these [instructions]({% link docs/preview/clients/odbc/overview.md %}).

### 1. Include the SQL Header Files

The first step is to include the SQL header files:

```cpp
#include <sql.h>
#include <sqlext.h>
```

These files contain the definitions of the ODBC functions, as well as the data types used by ODBC. To use these header files you have to have the `unixodbc` package installed:

On macOS:

```batch
brew install unixodbc
```

On Ubuntu and Debian:

```batch
sudo apt-get install -y unixodbc-dev
```

On Fedora, CentOS, and Red Hat:

```batch
sudo yum install -y unixODBC-devel
```

Remember to include the header file location in your `CFLAGS`.

For `MAKEFILE`:

```make
CFLAGS=-I/usr/local/include
# or
CFLAGS=-I/opt/homebrew/Cellar/unixodbc/2.3.11/include
```

For `CMAKE`:

```cmake
include_directories(/usr/local/include)
# or
include_directories(/opt/homebrew/Cellar/unixodbc/2.3.11/include)
```

You also have to link the library in your `CMAKE` or `MAKEFILE`.
For `CMAKE`:

```cmake
target_link_libraries(ODBC_application /path/to/duckdb_odbc/libduckdb_odbc.dylib)
```

For `MAKEFILE`:

```make
LDLIBS=-L/path/to/duckdb_odbc/libduckdb_odbc.dylib
```

### 2. Define the ODBC Handles and Connect to the Database

#### 2.a. Connecting with SQLConnect

Then set up the ODBC handles, allocate them, and connect to the database. First the environment handle is allocated, then the environment is set to ODBC version 3, then the connection handle is allocated, and finally the connection is made to the database. The following code snippet shows how to do this:

```cpp
SQLHANDLE env;
SQLHANDLE dbc;

SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, &env);

SQLSetEnvAttr(env, SQL_ATTR_ODBC_VERSION, (void*)SQL_OV_ODBC3, 0);

SQLAllocHandle(SQL_HANDLE_DBC, env, &dbc);

std::string dsn = "DSN=duckdbmemory";
SQLConnect(dbc, (SQLCHAR*)dsn.c_str(), SQL_NTS, NULL, 0, NULL, 0);

std::cout << "Connected!" << std::endl;
```

#### 2.b. Connecting with SQLDriverConnect

Alternatively, you can connect to the ODBC driver using [`SQLDriverConnect`](https://learn.microsoft.com/en-us/sql/odbc/reference/syntax/sqldriverconnect-function?view=sql-server-ver16).
`SQLDriverConnect` accepts a connection string in which you can configure the database using any of the available [DuckDB configuration options]({% link docs/preview/configuration/overview.md %}).

```cpp
SQLHANDLE env;
SQLHANDLE dbc;

SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, &env);

SQLSetEnvAttr(env, SQL_ATTR_ODBC_VERSION, (void*)SQL_OV_ODBC3, 0);

SQLAllocHandle(SQL_HANDLE_DBC, env, &dbc);

SQLCHAR str[1024];
SQLSMALLINT strl;
std::string dsn = "DSN=DuckDB;access_mode=READ_ONLY"
SQLDriverConnect(dbc, nullptr, (SQLCHAR*)dsn.c_str(), SQL_NTS, str, sizeof(str), &strl, SQL_DRIVER_COMPLETE)

std::cout << "Connected!" << std::endl;
```

### 3. Adding a Query

Now that the application is set up, we can add a query to it. First, we need to allocate a statement handle:

```cpp
SQLHANDLE stmt;
SQLAllocHandle(SQL_HANDLE_STMT, dbc, &stmt);
```

Then we can execute a query:

```cpp
SQLExecDirect(stmt, (SQLCHAR*)"SELECT * FROM integers", SQL_NTS);
```

### 4. Fetching Results

Now that we have executed a query, we can fetch the results. First, we need to bind the columns in the result set to buffers:

```cpp
SQLLEN int_val;
SQLLEN null_val;
SQLBindCol(stmt, 1, SQL_C_SLONG, &int_val, 0, &null_val);
```

Then we can fetch the results:

```cpp
SQLFetch(stmt);
```

### 5. Process the Results

Now that we have the results, we can do whatever we want with them. For example, we can print them:

```cpp
std::cout << "Value: " << int_val << std::endl;
```

You can also execute additional queries and perform other database operations such as inserting, updating, or deleting data.

### 6. Free the Handles and Disconnecting

Finally, we need to free the handles and disconnect from the database. First, we need to free the statement handle:

```cpp
SQLFreeHandle(SQL_HANDLE_STMT, stmt);
```

Then we need to disconnect from the database:

```cpp
SQLDisconnect(dbc);
```

And finally, we need to free the connection handle and the environment handle:

```cpp
SQLFreeHandle(SQL_HANDLE_DBC, dbc);
SQLFreeHandle(SQL_HANDLE_ENV, env);
```

Freeing the connection and environment handles can only be done after the connection to the database has been closed. Trying to free them before disconnecting from the database will result in an error.

## Sample Application

The following is a sample application that includes a `cpp` file that connects to the database, executes a query, fetches the results, and prints them. It also disconnects from the database and frees the handles, and includes a function to check the return value of ODBC functions. It also includes a `CMakeLists.txt` file that can be used to build the application.

### Sample `.cpp` File

```cpp
#include <iostream>
#include <sql.h>
#include <sqlext.h>

void check_ret(SQLRETURN ret, std::string msg) {
    if (ret != SQL_SUCCESS && ret != SQL_SUCCESS_WITH_INFO) {
        std::cout << ret << ": " << msg << " failed" << std::endl;
        exit(1);
    }
    if (ret == SQL_SUCCESS_WITH_INFO) {
        std::cout << ret << ": " << msg << " succeeded with info" << std::endl;
    }
}

int main() {
    SQLHANDLE env;
    SQLHANDLE dbc;
    SQLRETURN ret;

    ret = SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, &env);
    check_ret(ret, "SQLAllocHandle(env)");

    ret = SQLSetEnvAttr(env, SQL_ATTR_ODBC_VERSION, (void*)SQL_OV_ODBC3, 0);
    check_ret(ret, "SQLSetEnvAttr");

    ret = SQLAllocHandle(SQL_HANDLE_DBC, env, &dbc);
    check_ret(ret, "SQLAllocHandle(dbc)");

    std::string dsn = "DSN=duckdbmemory";
    ret = SQLConnect(dbc, (SQLCHAR*)dsn.c_str(), SQL_NTS, NULL, 0, NULL, 0);
    check_ret(ret, "SQLConnect");

    std::cout << "Connected!" << std::endl;

    SQLHANDLE stmt;
    ret = SQLAllocHandle(SQL_HANDLE_STMT, dbc, &stmt);
    check_ret(ret, "SQLAllocHandle(stmt)");

    ret = SQLExecDirect(stmt, (SQLCHAR*)"SELECT * FROM integers", SQL_NTS);
    check_ret(ret, "SQLExecDirect(SELECT * FROM integers)");

    SQLLEN int_val;
    SQLLEN null_val;
    ret = SQLBindCol(stmt, 1, SQL_C_SLONG, &int_val, 0, &null_val);
    check_ret(ret, "SQLBindCol");

    ret = SQLFetch(stmt);
    check_ret(ret, "SQLFetch");

    std::cout << "Value: " << int_val << std::endl;

    ret = SQLFreeHandle(SQL_HANDLE_STMT, stmt);
    check_ret(ret, "SQLFreeHandle(stmt)");

    ret = SQLDisconnect(dbc);
    check_ret(ret, "SQLDisconnect");

    ret = SQLFreeHandle(SQL_HANDLE_DBC, dbc);
    check_ret(ret, "SQLFreeHandle(dbc)");

    ret = SQLFreeHandle(SQL_HANDLE_ENV, env);
    check_ret(ret, "SQLFreeHandle(env)");
}
```

### Sample `CMakeLists.txt` File

```cmake
cmake_minimum_required(VERSION 3.25)
project(ODBC_Tester_App)

set(CMAKE_CXX_STANDARD 17)
include_directories(/opt/homebrew/Cellar/unixodbc/2.3.11/include)

add_executable(ODBC_Tester_App main.cpp)
target_link_libraries(ODBC_Tester_App /duckdb_odbc/libduckdb_odbc.dylib)
```
