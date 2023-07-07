---
layout: docu
title: NodeJS API
selected: Client APIs
---
## Modules

<dl>
<dt><a href="#module_duckdb">duckdb</a></dt>
<dd></dd>
</dl>

## Typedefs

<dl>
<dt><a href="#ColumnInfo">ColumnInfo</a> : <code>object</code></dt>
<dd></dd>
<dt><a href="#TypeInfo">TypeInfo</a> : <code>object</code></dt>
<dd></dd>
<dt><a href="#DuckDbError">DuckDbError</a> : <code>object</code></dt>
<dd></dd>
<dt><a href="#HTTPError">HTTPError</a> : <code>object</code></dt>
<dd></dd>
</dl>

<a name="module_duckdb"></a>

## duckdb
**Summary**: these jsdoc annotations are still a work in progress - feedback and suggestions are welcome!  

* [duckdb](#module_duckdb)
    * [~Connection](#module_duckdb..Connection)
        * [.run(sql, ...params, callback)](#module_duckdb..Connection+run) ⇒ <code>void</code>
        * [.all(sql, ...params, callback)](#module_duckdb..Connection+all) ⇒ <code>void</code>
        * [.arrowIPCAll(sql, ...params, callback)](#module_duckdb..Connection+arrowIPCAll) ⇒ <code>void</code>
        * [.arrowIPCStream(sql, ...params, callback)](#module_duckdb..Connection+arrowIPCStream) ⇒
        * [.each(sql, ...params, callback)](#module_duckdb..Connection+each) ⇒ <code>void</code>
        * [.stream(sql, ...params)](#module_duckdb..Connection+stream)
        * [.register_udf(name, return_type, fun)](#module_duckdb..Connection+register_udf) ⇒ <code>void</code>
        * [.prepare(sql, ...params, callback)](#module_duckdb..Connection+prepare) ⇒ <code>Statement</code>
        * [.exec(sql, ...params, callback)](#module_duckdb..Connection+exec) ⇒ <code>void</code>
        * [.register_udf_bulk(name, return_type, callback)](#module_duckdb..Connection+register_udf_bulk) ⇒ <code>void</code>
        * [.unregister_udf(name, return_type, callback)](#module_duckdb..Connection+unregister_udf) ⇒ <code>void</code>
        * [.register_buffer(name, array, force, callback)](#module_duckdb..Connection+register_buffer) ⇒ <code>void</code>
        * [.unregister_buffer(name, callback)](#module_duckdb..Connection+unregister_buffer) ⇒ <code>void</code>
    * [~Statement](#module_duckdb..Statement)
        * [.sql](#module_duckdb..Statement+sql) ⇒
        * [.get()](#module_duckdb..Statement+get)
        * [.run(sql, ...params, callback)](#module_duckdb..Statement+run) ⇒ <code>void</code>
        * [.all(sql, ...params, callback)](#module_duckdb..Statement+all) ⇒ <code>void</code>
        * [.arrowIPCAll(sql, ...params, callback)](#module_duckdb..Statement+arrowIPCAll) ⇒ <code>void</code>
        * [.each(sql, ...params, callback)](#module_duckdb..Statement+each) ⇒ <code>void</code>
        * [.finalize(sql, ...params, callback)](#module_duckdb..Statement+finalize) ⇒ <code>void</code>
        * [.stream(sql, ...params)](#module_duckdb..Statement+stream)
        * [.columns()](#module_duckdb..Statement+columns) ⇒ [<code>Array.&lt;ColumnInfo&gt;</code>](#ColumnInfo)
    * [~QueryResult](#module_duckdb..QueryResult)
        * [.nextChunk()](#module_duckdb..QueryResult+nextChunk) ⇒
        * [.nextIpcBuffer()](#module_duckdb..QueryResult+nextIpcBuffer) ⇒
        * [.asyncIterator()](#module_duckdb..QueryResult+asyncIterator)
    * [~Database](#module_duckdb..Database)
        * [.close(callback)](#module_duckdb..Database+close) ⇒ <code>void</code>
        * [.close_internal(callback)](#module_duckdb..Database+close_internal) ⇒ <code>void</code>
        * [.wait(callback)](#module_duckdb..Database+wait) ⇒ <code>void</code>
        * [.serialize(callback)](#module_duckdb..Database+serialize) ⇒ <code>void</code>
        * [.parallelize(callback)](#module_duckdb..Database+parallelize) ⇒ <code>void</code>
        * [.connect(path)](#module_duckdb..Database+connect) ⇒ <code>Connection</code>
        * [.interrupt(callback)](#module_duckdb..Database+interrupt) ⇒ <code>void</code>
        * [.prepare(sql)](#module_duckdb..Database+prepare) ⇒ <code>Statement</code>
        * [.run(sql, ...params, callback)](#module_duckdb..Database+run) ⇒ <code>void</code>
        * [.scanArrowIpc(sql, ...params, callback)](#module_duckdb..Database+scanArrowIpc) ⇒ <code>void</code>
        * [.each(sql, ...params, callback)](#module_duckdb..Database+each) ⇒ <code>void</code>
        * [.all(sql, ...params, callback)](#module_duckdb..Database+all) ⇒ <code>void</code>
        * [.arrowIPCAll(sql, ...params, callback)](#module_duckdb..Database+arrowIPCAll) ⇒ <code>void</code>
        * [.arrowIPCStream(sql, ...params, callback)](#module_duckdb..Database+arrowIPCStream) ⇒ <code>void</code>
        * [.exec(sql, ...params, callback)](#module_duckdb..Database+exec) ⇒ <code>void</code>
        * [.register_udf(name, return_type, fun)](#module_duckdb..Database+register_udf) ⇒ <code>this</code>
        * [.register_buffer(name)](#module_duckdb..Database+register_buffer) ⇒ <code>this</code>
        * [.unregister_buffer(name)](#module_duckdb..Database+unregister_buffer) ⇒ <code>this</code>
        * [.unregister_udf(name)](#module_duckdb..Database+unregister_udf) ⇒ <code>this</code>
        * [.registerReplacementScan(fun)](#module_duckdb..Database+registerReplacementScan) ⇒ <code>this</code>
        * [.get()](#module_duckdb..Database+get)
    * [~ERROR](#module_duckdb..ERROR) : <code>number</code>
    * [~OPEN_READONLY](#module_duckdb..OPEN_READONLY) : <code>number</code>
    * [~OPEN_READWRITE](#module_duckdb..OPEN_READWRITE) : <code>number</code>
    * [~OPEN_CREATE](#module_duckdb..OPEN_CREATE) : <code>number</code>
    * [~OPEN_FULLMUTEX](#module_duckdb..OPEN_FULLMUTEX) : <code>number</code>
    * [~OPEN_SHAREDCACHE](#module_duckdb..OPEN_SHAREDCACHE) : <code>number</code>
    * [~OPEN_PRIVATECACHE](#module_duckdb..OPEN_PRIVATECACHE) : <code>number</code>

<a name="module_duckdb..Connection"></a>

### duckdb~Connection
**Kind**: inner class of [<code>duckdb</code>](#module_duckdb)  

* [~Connection](#module_duckdb..Connection)
    * [.run(sql, ...params, callback)](#module_duckdb..Connection+run) ⇒ <code>void</code>
    * [.all(sql, ...params, callback)](#module_duckdb..Connection+all) ⇒ <code>void</code>
    * [.arrowIPCAll(sql, ...params, callback)](#module_duckdb..Connection+arrowIPCAll) ⇒ <code>void</code>
    * [.arrowIPCStream(sql, ...params, callback)](#module_duckdb..Connection+arrowIPCStream) ⇒
    * [.each(sql, ...params, callback)](#module_duckdb..Connection+each) ⇒ <code>void</code>
    * [.stream(sql, ...params)](#module_duckdb..Connection+stream)
    * [.register_udf(name, return_type, fun)](#module_duckdb..Connection+register_udf) ⇒ <code>void</code>
    * [.prepare(sql, ...params, callback)](#module_duckdb..Connection+prepare) ⇒ <code>Statement</code>
    * [.exec(sql, ...params, callback)](#module_duckdb..Connection+exec) ⇒ <code>void</code>
    * [.register_udf_bulk(name, return_type, callback)](#module_duckdb..Connection+register_udf_bulk) ⇒ <code>void</code>
    * [.unregister_udf(name, return_type, callback)](#module_duckdb..Connection+unregister_udf) ⇒ <code>void</code>
    * [.register_buffer(name, array, force, callback)](#module_duckdb..Connection+register_buffer) ⇒ <code>void</code>
    * [.unregister_buffer(name, callback)](#module_duckdb..Connection+unregister_buffer) ⇒ <code>void</code>

<a name="module_duckdb..Connection+run"></a>

#### connection.run(sql, ...params, callback) ⇒ <code>void</code>
Run a SQL statement and trigger a callback when done

**Kind**: instance method of [<code>Connection</code>](#module_duckdb..Connection)  

| Param | Type |
| --- | --- |
| sql |  | 
| ...params | <code>\*</code> | 
| callback |  | 

<a name="module_duckdb..Connection+all"></a>

#### connection.all(sql, ...params, callback) ⇒ <code>void</code>
Run a SQL query and triggers the callback once for all result rows

**Kind**: instance method of [<code>Connection</code>](#module_duckdb..Connection)  

| Param | Type |
| --- | --- |
| sql |  | 
| ...params | <code>\*</code> | 
| callback |  | 

<a name="module_duckdb..Connection+arrowIPCAll"></a>

#### connection.arrowIPCAll(sql, ...params, callback) ⇒ <code>void</code>
Run a SQL query and serialize the result into the Apache Arrow IPC format (requires arrow extension to be loaded)

**Kind**: instance method of [<code>Connection</code>](#module_duckdb..Connection)  

| Param | Type |
| --- | --- |
| sql |  | 
| ...params | <code>\*</code> | 
| callback |  | 

<a name="module_duckdb..Connection+arrowIPCStream"></a>

#### connection.arrowIPCStream(sql, ...params, callback) ⇒
Run a SQL query, returns a IpcResultStreamIterator that allows streaming the result into the Apache Arrow IPC format
(requires arrow extension to be loaded)

**Kind**: instance method of [<code>Connection</code>](#module_duckdb..Connection)  
**Returns**: Promise<IpcResultStreamIterator>  

| Param | Type |
| --- | --- |
| sql |  | 
| ...params | <code>\*</code> | 
| callback |  | 

<a name="module_duckdb..Connection+each"></a>

#### connection.each(sql, ...params, callback) ⇒ <code>void</code>
Runs a SQL query and triggers the callback for each result row

**Kind**: instance method of [<code>Connection</code>](#module_duckdb..Connection)  

| Param | Type |
| --- | --- |
| sql |  | 
| ...params | <code>\*</code> | 
| callback |  | 

<a name="module_duckdb..Connection+stream"></a>

#### connection.stream(sql, ...params)
**Kind**: instance method of [<code>Connection</code>](#module_duckdb..Connection)  

| Param | Type |
| --- | --- |
| sql |  | 
| ...params | <code>\*</code> | 

<a name="module_duckdb..Connection+register_udf"></a>

#### connection.register\_udf(name, return_type, fun) ⇒ <code>void</code>
Register a User Defined Function

**Kind**: instance method of [<code>Connection</code>](#module_duckdb..Connection)  
**Note**: this follows the wasm udfs somewhat but is simpler because we can pass data much more cleanly  

| Param |
| --- |
| name | 
| return_type | 
| fun | 

<a name="module_duckdb..Connection+prepare"></a>

#### connection.prepare(sql, ...params, callback) ⇒ <code>Statement</code>
Prepare a SQL query for execution

**Kind**: instance method of [<code>Connection</code>](#module_duckdb..Connection)  

| Param | Type |
| --- | --- |
| sql |  | 
| ...params | <code>\*</code> | 
| callback |  | 

<a name="module_duckdb..Connection+exec"></a>

#### connection.exec(sql, ...params, callback) ⇒ <code>void</code>
Execute a SQL query

**Kind**: instance method of [<code>Connection</code>](#module_duckdb..Connection)  

| Param | Type |
| --- | --- |
| sql |  | 
| ...params | <code>\*</code> | 
| callback |  | 

<a name="module_duckdb..Connection+register_udf_bulk"></a>

#### connection.register\_udf\_bulk(name, return_type, callback) ⇒ <code>void</code>
Register a User Defined Function

**Kind**: instance method of [<code>Connection</code>](#module_duckdb..Connection)  

| Param |
| --- |
| name | 
| return_type | 
| callback | 

<a name="module_duckdb..Connection+unregister_udf"></a>

#### connection.unregister\_udf(name, return_type, callback) ⇒ <code>void</code>
Unregister a User Defined Function

**Kind**: instance method of [<code>Connection</code>](#module_duckdb..Connection)  

| Param |
| --- |
| name | 
| return_type | 
| callback | 

<a name="module_duckdb..Connection+register_buffer"></a>

#### connection.register\_buffer(name, array, force, callback) ⇒ <code>void</code>
Register a Buffer to be scanned using the Apache Arrow IPC scanner
(requires arrow extension to be loaded)

**Kind**: instance method of [<code>Connection</code>](#module_duckdb..Connection)  

| Param |
| --- |
| name | 
| array | 
| force | 
| callback | 

<a name="module_duckdb..Connection+unregister_buffer"></a>

#### connection.unregister\_buffer(name, callback) ⇒ <code>void</code>
Unregister the Buffer

**Kind**: instance method of [<code>Connection</code>](#module_duckdb..Connection)  

| Param |
| --- |
| name | 
| callback | 

<a name="module_duckdb..Statement"></a>

### duckdb~Statement
**Kind**: inner class of [<code>duckdb</code>](#module_duckdb)  

* [~Statement](#module_duckdb..Statement)
    * [.sql](#module_duckdb..Statement+sql) ⇒
    * [.get()](#module_duckdb..Statement+get)
    * [.run(sql, ...params, callback)](#module_duckdb..Statement+run) ⇒ <code>void</code>
    * [.all(sql, ...params, callback)](#module_duckdb..Statement+all) ⇒ <code>void</code>
    * [.arrowIPCAll(sql, ...params, callback)](#module_duckdb..Statement+arrowIPCAll) ⇒ <code>void</code>
    * [.each(sql, ...params, callback)](#module_duckdb..Statement+each) ⇒ <code>void</code>
    * [.finalize(sql, ...params, callback)](#module_duckdb..Statement+finalize) ⇒ <code>void</code>
    * [.stream(sql, ...params)](#module_duckdb..Statement+stream)
    * [.columns()](#module_duckdb..Statement+columns) ⇒ [<code>Array.&lt;ColumnInfo&gt;</code>](#ColumnInfo)

<a name="module_duckdb..Statement+sql"></a>

#### statement.sql ⇒
**Kind**: instance property of [<code>Statement</code>](#module_duckdb..Statement)  
**Returns**: sql contained in statement  
**Field**:   
<a name="module_duckdb..Statement+get"></a>

#### statement.get()
Not implemented

**Kind**: instance method of [<code>Statement</code>](#module_duckdb..Statement)  
<a name="module_duckdb..Statement+run"></a>

#### statement.run(sql, ...params, callback) ⇒ <code>void</code>
**Kind**: instance method of [<code>Statement</code>](#module_duckdb..Statement)  

| Param | Type |
| --- | --- |
| sql |  | 
| ...params | <code>\*</code> | 
| callback |  | 

<a name="module_duckdb..Statement+all"></a>

#### statement.all(sql, ...params, callback) ⇒ <code>void</code>
**Kind**: instance method of [<code>Statement</code>](#module_duckdb..Statement)  

| Param | Type |
| --- | --- |
| sql |  | 
| ...params | <code>\*</code> | 
| callback |  | 

<a name="module_duckdb..Statement+arrowIPCAll"></a>

#### statement.arrowIPCAll(sql, ...params, callback) ⇒ <code>void</code>
**Kind**: instance method of [<code>Statement</code>](#module_duckdb..Statement)  

| Param | Type |
| --- | --- |
| sql |  | 
| ...params | <code>\*</code> | 
| callback |  | 

<a name="module_duckdb..Statement+each"></a>

#### statement.each(sql, ...params, callback) ⇒ <code>void</code>
**Kind**: instance method of [<code>Statement</code>](#module_duckdb..Statement)  

| Param | Type |
| --- | --- |
| sql |  | 
| ...params | <code>\*</code> | 
| callback |  | 

<a name="module_duckdb..Statement+finalize"></a>

#### statement.finalize(sql, ...params, callback) ⇒ <code>void</code>
**Kind**: instance method of [<code>Statement</code>](#module_duckdb..Statement)  

| Param | Type |
| --- | --- |
| sql |  | 
| ...params | <code>\*</code> | 
| callback |  | 

<a name="module_duckdb..Statement+stream"></a>

#### statement.stream(sql, ...params)
**Kind**: instance method of [<code>Statement</code>](#module_duckdb..Statement)  

| Param | Type |
| --- | --- |
| sql |  | 
| ...params | <code>\*</code> | 

<a name="module_duckdb..Statement+columns"></a>

#### statement.columns() ⇒ [<code>Array.&lt;ColumnInfo&gt;</code>](#ColumnInfo)
**Kind**: instance method of [<code>Statement</code>](#module_duckdb..Statement)  
**Returns**: [<code>Array.&lt;ColumnInfo&gt;</code>](#ColumnInfo) - - Array of column names and types  
<a name="module_duckdb..QueryResult"></a>

### duckdb~QueryResult
**Kind**: inner class of [<code>duckdb</code>](#module_duckdb)  

* [~QueryResult](#module_duckdb..QueryResult)
    * [.nextChunk()](#module_duckdb..QueryResult+nextChunk) ⇒
    * [.nextIpcBuffer()](#module_duckdb..QueryResult+nextIpcBuffer) ⇒
    * [.asyncIterator()](#module_duckdb..QueryResult+asyncIterator)

<a name="module_duckdb..QueryResult+nextChunk"></a>

#### queryResult.nextChunk() ⇒
**Kind**: instance method of [<code>QueryResult</code>](#module_duckdb..QueryResult)  
**Returns**: data chunk  
<a name="module_duckdb..QueryResult+nextIpcBuffer"></a>

#### queryResult.nextIpcBuffer() ⇒
Function to fetch the next result blob of an Arrow IPC Stream in a zero-copy way.
(requires arrow extension to be loaded)

**Kind**: instance method of [<code>QueryResult</code>](#module_duckdb..QueryResult)  
**Returns**: data chunk  
<a name="module_duckdb..QueryResult+asyncIterator"></a>

#### queryResult.asyncIterator()
**Kind**: instance method of [<code>QueryResult</code>](#module_duckdb..QueryResult)  
<a name="module_duckdb..Database"></a>

### duckdb~Database
Main database interface

**Kind**: inner property of [<code>duckdb</code>](#module_duckdb)  

| Param | Description |
| --- | --- |
| path | path to database file or :memory: for in-memory database |
| access_mode | access mode |
| config | the configuration object |
| callback | callback function |


* [~Database](#module_duckdb..Database)
    * [.close(callback)](#module_duckdb..Database+close) ⇒ <code>void</code>
    * [.close_internal(callback)](#module_duckdb..Database+close_internal) ⇒ <code>void</code>
    * [.wait(callback)](#module_duckdb..Database+wait) ⇒ <code>void</code>
    * [.serialize(callback)](#module_duckdb..Database+serialize) ⇒ <code>void</code>
    * [.parallelize(callback)](#module_duckdb..Database+parallelize) ⇒ <code>void</code>
    * [.connect(path)](#module_duckdb..Database+connect) ⇒ <code>Connection</code>
    * [.interrupt(callback)](#module_duckdb..Database+interrupt) ⇒ <code>void</code>
    * [.prepare(sql)](#module_duckdb..Database+prepare) ⇒ <code>Statement</code>
    * [.run(sql, ...params, callback)](#module_duckdb..Database+run) ⇒ <code>void</code>
    * [.scanArrowIpc(sql, ...params, callback)](#module_duckdb..Database+scanArrowIpc) ⇒ <code>void</code>
    * [.each(sql, ...params, callback)](#module_duckdb..Database+each) ⇒ <code>void</code>
    * [.all(sql, ...params, callback)](#module_duckdb..Database+all) ⇒ <code>void</code>
    * [.arrowIPCAll(sql, ...params, callback)](#module_duckdb..Database+arrowIPCAll) ⇒ <code>void</code>
    * [.arrowIPCStream(sql, ...params, callback)](#module_duckdb..Database+arrowIPCStream) ⇒ <code>void</code>
    * [.exec(sql, ...params, callback)](#module_duckdb..Database+exec) ⇒ <code>void</code>
    * [.register_udf(name, return_type, fun)](#module_duckdb..Database+register_udf) ⇒ <code>this</code>
    * [.register_buffer(name)](#module_duckdb..Database+register_buffer) ⇒ <code>this</code>
    * [.unregister_buffer(name)](#module_duckdb..Database+unregister_buffer) ⇒ <code>this</code>
    * [.unregister_udf(name)](#module_duckdb..Database+unregister_udf) ⇒ <code>this</code>
    * [.registerReplacementScan(fun)](#module_duckdb..Database+registerReplacementScan) ⇒ <code>this</code>
    * [.get()](#module_duckdb..Database+get)

<a name="module_duckdb..Database+close"></a>

#### database.close(callback) ⇒ <code>void</code>
Closes database instance

**Kind**: instance method of [<code>Database</code>](#module_duckdb..Database)  

| Param |
| --- |
| callback | 

<a name="module_duckdb..Database+close_internal"></a>

#### database.close\_internal(callback) ⇒ <code>void</code>
Internal method. Do not use, call Connection#close instead

**Kind**: instance method of [<code>Database</code>](#module_duckdb..Database)  

| Param |
| --- |
| callback | 

<a name="module_duckdb..Database+wait"></a>

#### database.wait(callback) ⇒ <code>void</code>
Triggers callback when all scheduled database tasks have completed.

**Kind**: instance method of [<code>Database</code>](#module_duckdb..Database)  

| Param |
| --- |
| callback | 

<a name="module_duckdb..Database+serialize"></a>

#### database.serialize(callback) ⇒ <code>void</code>
TODO: what does this do?

**Kind**: instance method of [<code>Database</code>](#module_duckdb..Database)  

| Param |
| --- |
| callback | 

<a name="module_duckdb..Database+parallelize"></a>

#### database.parallelize(callback) ⇒ <code>void</code>
TODO: what does this do?

**Kind**: instance method of [<code>Database</code>](#module_duckdb..Database)  

| Param |
| --- |
| callback | 

<a name="module_duckdb..Database+connect"></a>

#### database.connect(path) ⇒ <code>Connection</code>
Create a new database connection

**Kind**: instance method of [<code>Database</code>](#module_duckdb..Database)  

| Param | Description |
| --- | --- |
| path | the database to connect to, either a file path, or `:memory:` |

<a name="module_duckdb..Database+interrupt"></a>

#### database.interrupt(callback) ⇒ <code>void</code>
Supposedly interrupt queries, but currently does not do anything.

**Kind**: instance method of [<code>Database</code>](#module_duckdb..Database)  

| Param |
| --- |
| callback | 

<a name="module_duckdb..Database+prepare"></a>

#### database.prepare(sql) ⇒ <code>Statement</code>
Prepare a SQL query for execution

**Kind**: instance method of [<code>Database</code>](#module_duckdb..Database)  

| Param |
| --- |
| sql | 

<a name="module_duckdb..Database+run"></a>

#### database.run(sql, ...params, callback) ⇒ <code>void</code>
Convenience method for Connection#run using a built-in default connection

**Kind**: instance method of [<code>Database</code>](#module_duckdb..Database)  

| Param | Type |
| --- | --- |
| sql |  | 
| ...params | <code>\*</code> | 
| callback |  | 

<a name="module_duckdb..Database+scanArrowIpc"></a>

#### database.scanArrowIpc(sql, ...params, callback) ⇒ <code>void</code>
Convenience method for Connection#scanArrowIpc using a built-in default connection

**Kind**: instance method of [<code>Database</code>](#module_duckdb..Database)  

| Param | Type |
| --- | --- |
| sql |  | 
| ...params | <code>\*</code> | 
| callback |  | 

<a name="module_duckdb..Database+each"></a>

#### database.each(sql, ...params, callback) ⇒ <code>void</code>
**Kind**: instance method of [<code>Database</code>](#module_duckdb..Database)  

| Param | Type |
| --- | --- |
| sql |  | 
| ...params | <code>\*</code> | 
| callback |  | 

<a name="module_duckdb..Database+all"></a>

#### database.all(sql, ...params, callback) ⇒ <code>void</code>
Convenience method for Connection#apply using a built-in default connection

**Kind**: instance method of [<code>Database</code>](#module_duckdb..Database)  

| Param | Type |
| --- | --- |
| sql |  | 
| ...params | <code>\*</code> | 
| callback |  | 

<a name="module_duckdb..Database+arrowIPCAll"></a>

#### database.arrowIPCAll(sql, ...params, callback) ⇒ <code>void</code>
Convenience method for Connection#arrowIPCAll using a built-in default connection

**Kind**: instance method of [<code>Database</code>](#module_duckdb..Database)  

| Param | Type |
| --- | --- |
| sql |  | 
| ...params | <code>\*</code> | 
| callback |  | 

<a name="module_duckdb..Database+arrowIPCStream"></a>

#### database.arrowIPCStream(sql, ...params, callback) ⇒ <code>void</code>
Convenience method for Connection#arrowIPCStream using a built-in default connection

**Kind**: instance method of [<code>Database</code>](#module_duckdb..Database)  

| Param | Type |
| --- | --- |
| sql |  | 
| ...params | <code>\*</code> | 
| callback |  | 

<a name="module_duckdb..Database+exec"></a>

#### database.exec(sql, ...params, callback) ⇒ <code>void</code>
**Kind**: instance method of [<code>Database</code>](#module_duckdb..Database)  

| Param | Type |
| --- | --- |
| sql |  | 
| ...params | <code>\*</code> | 
| callback |  | 

<a name="module_duckdb..Database+register_udf"></a>

#### database.register\_udf(name, return_type, fun) ⇒ <code>this</code>
Register a User Defined Function

Convenience method for Connection#register_udf

**Kind**: instance method of [<code>Database</code>](#module_duckdb..Database)  

| Param |
| --- |
| name | 
| return_type | 
| fun | 

<a name="module_duckdb..Database+register_buffer"></a>

#### database.register\_buffer(name) ⇒ <code>this</code>
Register a buffer containing serialized data to be scanned from DuckDB.

Convenience method for Connection#unregister_buffer

**Kind**: instance method of [<code>Database</code>](#module_duckdb..Database)  

| Param |
| --- |
| name | 

<a name="module_duckdb..Database+unregister_buffer"></a>

#### database.unregister\_buffer(name) ⇒ <code>this</code>
Unregister a Buffer

Convenience method for Connection#unregister_buffer

**Kind**: instance method of [<code>Database</code>](#module_duckdb..Database)  

| Param |
| --- |
| name | 

<a name="module_duckdb..Database+unregister_udf"></a>

#### database.unregister\_udf(name) ⇒ <code>this</code>
Unregister a UDF

Convenience method for Connection#unregister_udf

**Kind**: instance method of [<code>Database</code>](#module_duckdb..Database)  

| Param |
| --- |
| name | 

<a name="module_duckdb..Database+registerReplacementScan"></a>

#### database.registerReplacementScan(fun) ⇒ <code>this</code>
Register a table replace scan function

**Kind**: instance method of [<code>Database</code>](#module_duckdb..Database)  

| Param | Description |
| --- | --- |
| fun | Replacement scan function |

<a name="module_duckdb..Database+get"></a>

#### database.get()
Not implemented

**Kind**: instance method of [<code>Database</code>](#module_duckdb..Database)  
<a name="module_duckdb..ERROR"></a>

### duckdb~ERROR : <code>number</code>
Check that errno attribute equals this to check for a duckdb error

**Kind**: inner constant of [<code>duckdb</code>](#module_duckdb)  
<a name="module_duckdb..OPEN_READONLY"></a>

### duckdb~OPEN\_READONLY : <code>number</code>
Open database in readonly mode

**Kind**: inner constant of [<code>duckdb</code>](#module_duckdb)  
<a name="module_duckdb..OPEN_READWRITE"></a>

### duckdb~OPEN\_READWRITE : <code>number</code>
Currently ignored

**Kind**: inner constant of [<code>duckdb</code>](#module_duckdb)  
<a name="module_duckdb..OPEN_CREATE"></a>

### duckdb~OPEN\_CREATE : <code>number</code>
Currently ignored

**Kind**: inner constant of [<code>duckdb</code>](#module_duckdb)  
<a name="module_duckdb..OPEN_FULLMUTEX"></a>

### duckdb~OPEN\_FULLMUTEX : <code>number</code>
Currently ignored

**Kind**: inner constant of [<code>duckdb</code>](#module_duckdb)  
<a name="module_duckdb..OPEN_SHAREDCACHE"></a>

### duckdb~OPEN\_SHAREDCACHE : <code>number</code>
Currently ignored

**Kind**: inner constant of [<code>duckdb</code>](#module_duckdb)  
<a name="module_duckdb..OPEN_PRIVATECACHE"></a>

### duckdb~OPEN\_PRIVATECACHE : <code>number</code>
Currently ignored

**Kind**: inner constant of [<code>duckdb</code>](#module_duckdb)  
<a name="ColumnInfo"></a>

## ColumnInfo : <code>object</code>
**Kind**: global typedef  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| name | <code>string</code> | Column name |
| type | [<code>TypeInfo</code>](#TypeInfo) | Column type |

<a name="TypeInfo"></a>

## TypeInfo : <code>object</code>
**Kind**: global typedef  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| id | <code>string</code> | Type ID |
| [alias] | <code>string</code> | SQL type alias |
| sql_type | <code>string</code> | SQL type name |

<a name="DuckDbError"></a>

## DuckDbError : <code>object</code>
**Kind**: global typedef  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| errno | <code>number</code> | -1 for DuckDB errors |
| message | <code>string</code> | Error message |
| code | <code>string</code> | 'DUCKDB_NODEJS_ERROR' for DuckDB errors |
| errorType | <code>string</code> | DuckDB error type code (eg, HTTP, IO, Catalog) |

<a name="HTTPError"></a>

## HTTPError : <code>object</code>
**Kind**: global typedef  
**Extends**: [<code>DuckDbError</code>](#DuckDbError)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| statusCode | <code>number</code> | HTTP response status code |
| reason | <code>string</code> | HTTP response reason |
| response | <code>string</code> | HTTP response body |
| headers | <code>object</code> | HTTP headers |

