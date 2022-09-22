---
layout: docu
title: C API - Startup & Shutdown
selected: Startup
---
To use DuckDB, you must first initialize a `duckdb_database` handle using `duckdb_open()`. `duckdb_open()` takes as parameter the database file to read and write from. The special value `NULL` (`nullptr`) can be used to create an **in-memory database**. Note that for an in-memory database no data is persisted to disk (i.e. all data is lost when you exit the process).

With the `duckdb_database` handle, you can create one or many `duckdb_connection` using `duckdb_connect()`. While individual connections are thread-safe, they will be locked during querying. It is therefore recommended that each thread uses its own connection to allow for the best parallel performance.

All `duckdb_connection`s have to explicitly be disconnected with `duckdb_disconnect()` and the `duckdb_database` has to be explicitly closed with `duckdb_close()` to avoid memory and file handle leaking.

### Example
```c
duckdb_database db;
duckdb_connection con;

if (duckdb_open(NULL, &db) == DuckDBError) {
	// handle error
}
if (duckdb_connect(db, &con) == DuckDBError) {
	// handle error
}

// run queries...

// cleanup
duckdb_disconnect(&con);
duckdb_close(&db);
```

## API Reference
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_open">duckdb_open</a></span>(<span class="kt">const</span> <span class="kt">char</span> *<span class="k">path</span>, <span class="kt">duckdb_database</span> *<span class="k">out_database</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_open_ext">duckdb_open_ext</a></span>(<span class="kt">const</span> <span class="kt">char</span> *<span class="k">path</span>, <span class="kt">duckdb_database</span> *<span class="k">out_database</span>, <span class="kt">duckdb_config</span> <span class="k">config</span>, <span class="kt">char</span> **<span class="k">out_error</span>);
<span class="kt">void</span> <span class="nf"><a href="#duckdb_close">duckdb_close</a></span>(<span class="kt">duckdb_database</span> *<span class="k">database</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_connect">duckdb_connect</a></span>(<span class="kt">duckdb_database</span> <span class="k">database</span>, <span class="kt">duckdb_connection</span> *<span class="k">out_connection</span>);
<span class="kt">void</span> <span class="nf"><a href="#duckdb_disconnect">duckdb_disconnect</a></span>(<span class="kt">duckdb_connection</span> *<span class="k">connection</span>);
</code></pre></div></div>
### duckdb_open
---
Creates a new database or opens an existing database file stored at the the given path.
If no path is given a new in-memory database is created instead.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_open</span>(<span class="k">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="k">path</span>,<span class="k">
</span>  <span class="kt">duckdb_database</span> *<span class="k">out_database
</span>);
</code></pre></div></div>
#### Parameters
---
* `path`

Path to the database file on disk, or `nullptr` or `:memory:` to open an in-memory database.
* `out_database`

The result database object.
* `returns`

`DuckDBSuccess` on success or `DuckDBError` on failure.

<br>

### duckdb_open_ext
---
Extended version of duckdb_open. Creates a new database or opens an existing database file stored at the the given path.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_open_ext</span>(<span class="k">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="k">path</span>,<span class="k">
</span>  <span class="kt">duckdb_database</span> *<span class="k">out_database</span>,<span class="k">
</span>  <span class="kt">duckdb_config</span> <span class="k">config</span>,<span class="k">
</span>  <span class="kt">char</span> **<span class="k">out_error
</span>);
</code></pre></div></div>
#### Parameters
---
* `path`

Path to the database file on disk, or `nullptr` or `:memory:` to open an in-memory database.
* `out_database`

The result database object.
* `config`

(Optional) configuration used to start up the database system.
* `out_error`

If set and the function returns DuckDBError, this will contain the reason why the start-up failed.
Note that the error must be freed using `duckdb_free`.
* `returns`

`DuckDBSuccess` on success or `DuckDBError` on failure.

<br>

### duckdb_close
---
Closes the specified database and de-allocates all memory allocated for that database.
This should be called after you are done with any database allocated through `duckdb_open`.
Note that failing to call `duckdb_close` (in case of e.g. a program crash) will not cause data corruption.
Still it is recommended to always correctly close a database object after you are done with it.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="k">duckdb_close</span>(<span class="k">
</span>  <span class="kt">duckdb_database</span> *<span class="k">database
</span>);
</code></pre></div></div>
#### Parameters
---
* `database`

The database object to shut down.

<br>

### duckdb_connect
---
Opens a connection to a database. Connections are required to query the database, and store transactional state
associated with the connection.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_connect</span>(<span class="k">
</span>  <span class="kt">duckdb_database</span> <span class="k">database</span>,<span class="k">
</span>  <span class="kt">duckdb_connection</span> *<span class="k">out_connection
</span>);
</code></pre></div></div>
#### Parameters
---
* `database`

The database file to connect to.
* `out_connection`

The result connection object.
* `returns`

`DuckDBSuccess` on success or `DuckDBError` on failure.

<br>

### duckdb_disconnect
---
Closes the specified connection and de-allocates all memory allocated for that connection.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="k">duckdb_disconnect</span>(<span class="k">
</span>  <span class="kt">duckdb_connection</span> *<span class="k">connection
</span>);
</code></pre></div></div>
#### Parameters
---
* `connection`

The connection to close.

<br>

