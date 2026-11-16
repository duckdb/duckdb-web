---
github_repository: https://github.com/Giorgi/DuckDB.NET
layout: docu
redirect_from:
- /docs/stable/clients/dotnet
- /docs/current/clients/dotnet
- /docs/lts/clients/dotnet
- /docs/preview/clients/dotnet
title: C# (.NET) Client
---

> Warning Version 2.0.0 of the DuckDB C# client is currently available in [preview](https://www.nuget.org/packages/DuckDB.NET.Data.Full/2.0.0-preview.1). The stable 2.0.0 release is planned for the end of November 2026.
> To install it, run `dotnet add package DuckDB.NET.Data.Full --prerelease`.

> Installation To use the DuckDB C# client, install the [`DuckDB.NET.Data.Full` NuGet package](https://www.nuget.org/packages/DuckDB.NET.Data.Full).
>
> {% include install/latest_client.html client="csharp" %}The latest stable version of the DuckDB C# client is {{ latest_version }}.

[DuckDB.NET](https://duckdb.net/) is an open-source [ADO.NET](https://learn.microsoft.com/en-us/dotnet/framework/data/adonet/) provider for DuckDB. It also includes a low-level .NET wrapper around the [DuckDB C API]({% link docs/2.0/clients/c/overview.md %}). The client is maintained by [Giorgi Dalakishvili](https://github.com/Giorgi). For the full documentation, see the [DuckDB.NET website](https://duckdb.net/docs/introduction.html).

## Installation

DuckDB.NET is distributed in four NuGet packages. The ADO.NET provider (`DuckDB.NET.Data`) is built on top of the low-level bindings library (`DuckDB.NET.Bindings`) and is the recommended way to use DuckDB from .NET. Both are available in a _Full_ variant, which bundles the DuckDB native library, and in a managed-only variant, which does not include the native library.

| Package | ADO.NET provider | Includes DuckDB native library |
| ------- | ---------------- | ------------------------------ |
| [`DuckDB.NET.Bindings`](https://www.nuget.org/packages/DuckDB.NET.Bindings)           | no  | no  |
| [`DuckDB.NET.Bindings.Full`](https://www.nuget.org/packages/DuckDB.NET.Bindings.Full) | no  | yes |
| [`DuckDB.NET.Data`](https://www.nuget.org/packages/DuckDB.NET.Data)                   | yes | no  |
| [`DuckDB.NET.Data.Full`](https://www.nuget.org/packages/DuckDB.NET.Data.Full)         | yes | yes |

To install the ADO.NET provider along with the DuckDB native library, run:

```batch
dotnet add package DuckDB.NET.Data.Full
```

The packages target .NET 8.0 and later.

## Basic Usage

DuckDB.NET follows the ADO.NET provider model. To run SQL statements, create a `DuckDBConnection`, open it, and create a command. Then, execute the command using one of the following methods:

* `ExecuteNonQuery`: executes statements that do not return results, such as DDL statements and `INSERT`, `UPDATE`, or `DELETE` statements.
* `ExecuteScalar`: executes a query that returns a single scalar value.
* `ExecuteReader`: executes a query and returns a `DuckDBDataReader`, which can be used to consume the result set.

```cs
using DuckDB.NET.Data;

using var connection = new DuckDBConnection("Data Source=file.db");
connection.Open();

using var command = connection.CreateCommand();

command.CommandText = "CREATE TABLE integers (foo INTEGER, bar INTEGER);";
command.ExecuteNonQuery();

command.CommandText = "INSERT INTO integers VALUES (3, 4), (5, 6), (7, NULL);";
command.ExecuteNonQuery();

command.CommandText = "SELECT count(*) FROM integers;";
var count = command.ExecuteScalar();
Console.WriteLine($"Number of rows: {count}");

command.CommandText = "SELECT foo, bar FROM integers;";
using var reader = command.ExecuteReader();
while (reader.Read())
{
    var foo = reader.GetInt32(0);
    var bar = reader.IsDBNull(1) ? "NULL" : reader.GetInt32(1).ToString();
    Console.WriteLine($"{foo} {bar}");
}
```

### Parameterized Queries

To protect against SQL injection, use parameterized queries instead of string concatenation. DuckDB.NET supports all three [prepared statement syntaxes]({% link docs/2.0/sql/query_syntax/prepared_statements.md %}): auto-incremented (`?`), positional (`$1`), and named (`$param`) parameters.

```cs
using var command = connection.CreateCommand();
command.CommandText = "SELECT * FROM integers WHERE foo >= $minimum_foo;";
command.Parameters.Add(new DuckDBParameter("minimum_foo", 5));

using var reader = command.ExecuteReader();
```

### Multiple Statements

To execute multiple statements in a single command, separate them with semicolons. If the statements return results, use the `NextResult` method of the data reader to move to the next result set.

### Streaming Mode

By default, DuckDB.NET executes queries in materialized mode, which fetches the entire result set into memory. To reduce memory usage for large results, set the command's `UseStreamingMode` property to `true`. In streaming mode, DuckDB fetches the result set chunk by chunk, which may result in slower query execution.

```cs
command.UseStreamingMode = true;
```

## Connection Strings

DuckDB.NET connection strings follow the standard [ADO.NET syntax](https://learn.microsoft.com/en-us/dotnet/framework/data/adonet/connection-strings), i.e., a semicolon-separated list of keywords and values. The `DataSource` (or `Data Source`) keyword specifies the path to the database file. If the file does not exist, it is created when the connection is first opened.

To use an in-memory database, set the data source to `:memory:`. Each in-memory connection creates a new, isolated database. To share an in-memory database between connections, use `:memory:?cache=shared`.

All other keywords are treated as DuckDB [configuration options]({% link docs/2.0/configuration/overview.md %}), which are set when the database is opened. Options that cannot be set at startup can be changed using the [`SET` statement]({% link docs/2.0/sql/statements/set.md %}) after opening the connection.

| Connection string | Description |
| ----------------- | ----------- |
| `DataSource=:memory:` | Connect to a new in-memory database |
| `DataSource=:memory:?cache=shared` | Connect to a shared in-memory database |
| `DataSource=train_services.db` | Connect to `train_services.db` |
| `DataSource=train_services.db;access_mode=READ_ONLY` | Connect to `train_services.db` in read-only mode |
| `DataSource=train_services.db;threads=8;memory_limit=10GB` | Connect to `train_services.db`, limit the number of threads to 8 and the memory usage to 10 GB |

Connection strings can also be created with the `DuckDBConnectionStringBuilder` class, which has typed properties for commonly used configuration options:

```cs
var builder = new DuckDBConnectionStringBuilder
{
    DataSource = "train_services.db",
    AccessMode = DuckDBAccessMode.ReadOnly,
    Threads = 8,
    MemoryLimit = "10GB"
};

using var connection = new DuckDBConnection(builder.ConnectionString);
connection.Open();
```

## Further Features

DuckDB.NET supports several further features, which are described in its documentation:

* [Apache Arrow](https://duckdb.net/docs/arrow.html) result streaming
* [Bulk data loading](https://duckdb.net/docs/bulk-data-loading.html) using the [appender]({% link docs/2.0/data/appender.md %})
* [Type mappings](https://duckdb.net/docs/type-mapping.html) between DuckDB and .NET types
* [Composite types and enums](https://duckdb.net/docs/composite-types.html)
* [User-defined functions](https://duckdb.net/docs/user-defined-functions.html), including scalar and table functions written in C#

To build DuckDB extensions in C#, see the [DuckDB.ExtensionKit](https://github.com/Giorgi/DuckDB.ExtensionKit) project and its [introductory blog post]({% post_url 2026-03-20-duckdb-extensionkit-csharp %}).

## Getting Help

To ask questions about DuckDB.NET, join the [DuckDB Discord](https://discord.duckdb.org/) and post your question in the `dotnet` channel. To report a bug, [open an issue](https://github.com/Giorgi/DuckDB.NET/issues/new) in the DuckDB.NET repository and include a [minimal, reproducible example](https://stackoverflow.com/help/minimal-reproducible-example).
