---
layout: docu
title: NodeJS API
selected: Client APIs
---
<a name="module_duckdb"></a>

## duckdb
**Summary**: these jsdoc annotations are still a work in progress - feedback and suggestions are welcome!  

* [duckdb](#module_duckdb)
    * [~Connection](#module_duckdb..Connection)
        * [.run(sql, ...params, callback)](#module_duckdb..Connection+run) ⇒ <code>void</code>
        * [.all(sql, ...params, callback)](#module_duckdb..Connection+all) ⇒ <code>void</code>
        * [.each(sql, ...params, callback)](#module_duckdb..Connection+each) ⇒ <code>void</code>
        * [.stream(sql, ...params)](#module_duckdb..Connection+stream)
        * [.register(name, return_type, fun)](#module_duckdb..Connection+register) ⇒ <code>void</code>
        * [.prepare(sql, ...params, callback)](#module_duckdb..Connection+prepare) ⇒ <code>Statement</code>
        * [.exec(sql, ...params, callback)](#module_duckdb..Connection+exec) ⇒ <code>void</code>
        * [.register_bulk(name, return_type, callback)](#module_duckdb..Connection+register_bulk) ⇒ <code>void</code>
        * [.unregister(name, return_type, callback)](#module_duckdb..Connection+unregister) ⇒ <code>void</code>
    * [~Statement](#module_duckdb..Statement)
        * [.get()](#module_duckdb..Statement+get)
        * [.run(sql, ...params, callback)](#module_duckdb..Statement+run) ⇒ <code>void</code>
        * [.all(sql, ...params, callback)](#module_duckdb..Statement+all) ⇒ <code>void</code>
        * [.each(sql, ...params, callback)](#module_duckdb..Statement+each) ⇒ <code>void</code>
        * [.finalize(sql, ...params, callback)](#module_duckdb..Statement+finalize) ⇒ <code>void</code>
        * [.stream(sql, ...params)](#module_duckdb..Statement+stream)
    * [~QueryResult](#module_duckdb..QueryResult)
        * [.nextChunk()](#module_duckdb..QueryResult+nextChunk) ⇒
        * [.asyncIterator()](#module_duckdb..QueryResult+asyncIterator)
    * [~Database](#module_duckdb..Database)
        * [.close(callback)](#module_duckdb..Database+close) ⇒ <code>void</code>
        * [.wait(callback)](#module_duckdb..Database+wait) ⇒ <code>void</code>
        * [.serialize(callback)](#module_duckdb..Database+serialize) ⇒ <code>void</code>
        * [.parallelize(callback)](#module_duckdb..Database+parallelize) ⇒ <code>void</code>
        * [.connect(path)](#module_duckdb..Database+connect) ⇒ <code>Connection</code>
        * [.interrupt(callback)](#module_duckdb..Database+interrupt) ⇒ <code>void</code>
        * [.prepare(sql)](#module_duckdb..Database+prepare) ⇒ <code>Statement</code>
        * [.run(sql, ...params, callback)](#module_duckdb..Database+run) ⇒ <code>void</code>
        * [.each(sql, ...params, callback)](#module_duckdb..Database+each) ⇒ <code>void</code>
        * [.all(sql, ...params, callback)](#module_duckdb..Database+all) ⇒ <code>void</code>
        * [.exec(sql, ...params, callback)](#module_duckdb..Database+exec) ⇒ <code>void</code>
        * [.register(name, return_type, fun)](#module_duckdb..Database+register) ⇒ <code>this</code>
        * [.unregister(name)](#module_duckdb..Database+unregister) ⇒ <code>this</code>
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
    * [.each(sql, ...params, callback)](#module_duckdb..Connection+each) ⇒ <code>void</code>
    * [.stream(sql, ...params)](#module_duckdb..Connection+stream)
    * [.register(name, return_type, fun)](#module_duckdb..Connection+register) ⇒ <code>void</code>
    * [.prepare(sql, ...params, callback)](#module_duckdb..Connection+prepare) ⇒ <code>Statement</code>
    * [.exec(sql, ...params, callback)](#module_duckdb..Connection+exec) ⇒ <code>void</code>
    * [.register_bulk(name, return_type, callback)](#module_duckdb..Connection+register_bulk) ⇒ <code>void</code>
    * [.unregister(name, return_type, callback)](#module_duckdb..Connection+unregister) ⇒ <code>void</code>

<a name="module_duckdb..Connection+run"></a>

#### connection.run(sql, ...params, callback) ⇒ <code>void</code>
**Kind**: instance method of [<code>Connection</code>](#module_duckdb..Connection)  

| Param | Type |
| --- | --- |
| sql |  | 
| ...params | <code>\*</code> | 
| callback |  | 

<a name="module_duckdb..Connection+all"></a>

#### connection.all(sql, ...params, callback) ⇒ <code>void</code>
**Kind**: instance method of [<code>Connection</code>](#module_duckdb..Connection)  

| Param | Type |
| --- | --- |
| sql |  | 
| ...params | <code>\*</code> | 
| callback |  | 

<a name="module_duckdb..Connection+each"></a>

#### connection.each(sql, ...params, callback) ⇒ <code>void</code>
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

<a name="module_duckdb..Connection+register"></a>

#### connection.register(name, return_type, fun) ⇒ <code>void</code>
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
**Kind**: instance method of [<code>Connection</code>](#module_duckdb..Connection)  

| Param | Type |
| --- | --- |
| sql |  | 
| ...params | <code>\*</code> | 
| callback |  | 

<a name="module_duckdb..Connection+exec"></a>

#### connection.exec(sql, ...params, callback) ⇒ <code>void</code>
**Kind**: instance method of [<code>Connection</code>](#module_duckdb..Connection)  

| Param | Type |
| --- | --- |
| sql |  | 
| ...params | <code>\*</code> | 
| callback |  | 

<a name="module_duckdb..Connection+register_bulk"></a>

#### connection.register\_bulk(name, return_type, callback) ⇒ <code>void</code>
Register a User Defined Function

**Kind**: instance method of [<code>Connection</code>](#module_duckdb..Connection)  

| Param |
| --- |
| name | 
| return_type | 
| callback | 

<a name="module_duckdb..Connection+unregister"></a>

#### connection.unregister(name, return_type, callback) ⇒ <code>void</code>
Unregister a User Defined Function

**Kind**: instance method of [<code>Connection</code>](#module_duckdb..Connection)  

| Param |
| --- |
| name | 
| return_type | 
| callback | 

<a name="module_duckdb..Statement"></a>

### duckdb~Statement
**Kind**: inner class of [<code>duckdb</code>](#module_duckdb)  

* [~Statement](#module_duckdb..Statement)
    * [.get()](#module_duckdb..Statement+get)
    * [.run(sql, ...params, callback)](#module_duckdb..Statement+run) ⇒ <code>void</code>
    * [.all(sql, ...params, callback)](#module_duckdb..Statement+all) ⇒ <code>void</code>
    * [.each(sql, ...params, callback)](#module_duckdb..Statement+each) ⇒ <code>void</code>
    * [.finalize(sql, ...params, callback)](#module_duckdb..Statement+finalize) ⇒ <code>void</code>
    * [.stream(sql, ...params)](#module_duckdb..Statement+stream)

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

<a name="module_duckdb..QueryResult"></a>

### duckdb~QueryResult
**Kind**: inner class of [<code>duckdb</code>](#module_duckdb)  

* [~QueryResult](#module_duckdb..QueryResult)
    * [.nextChunk()](#module_duckdb..QueryResult+nextChunk) ⇒
    * [.asyncIterator()](#module_duckdb..QueryResult+asyncIterator)

<a name="module_duckdb..QueryResult+nextChunk"></a>

#### queryResult.nextChunk() ⇒
**Kind**: instance method of [<code>QueryResult</code>](#module_duckdb..QueryResult)  
**Returns**: data chunk  
<a name="module_duckdb..QueryResult+asyncIterator"></a>

#### queryResult.asyncIterator()
**Kind**: instance method of [<code>QueryResult</code>](#module_duckdb..QueryResult)  
<a name="module_duckdb..Database"></a>

### duckdb~Database
Main database interface

**Kind**: inner property of [<code>duckdb</code>](#module_duckdb)  

* [~Database](#module_duckdb..Database)
    * [.close(callback)](#module_duckdb..Database+close) ⇒ <code>void</code>
    * [.wait(callback)](#module_duckdb..Database+wait) ⇒ <code>void</code>
    * [.serialize(callback)](#module_duckdb..Database+serialize) ⇒ <code>void</code>
    * [.parallelize(callback)](#module_duckdb..Database+parallelize) ⇒ <code>void</code>
    * [.connect(path)](#module_duckdb..Database+connect) ⇒ <code>Connection</code>
    * [.interrupt(callback)](#module_duckdb..Database+interrupt) ⇒ <code>void</code>
    * [.prepare(sql)](#module_duckdb..Database+prepare) ⇒ <code>Statement</code>
    * [.run(sql, ...params, callback)](#module_duckdb..Database+run) ⇒ <code>void</code>
    * [.each(sql, ...params, callback)](#module_duckdb..Database+each) ⇒ <code>void</code>
    * [.all(sql, ...params, callback)](#module_duckdb..Database+all) ⇒ <code>void</code>
    * [.exec(sql, ...params, callback)](#module_duckdb..Database+exec) ⇒ <code>void</code>
    * [.register(name, return_type, fun)](#module_duckdb..Database+register) ⇒ <code>this</code>
    * [.unregister(name)](#module_duckdb..Database+unregister) ⇒ <code>this</code>
    * [.get()](#module_duckdb..Database+get)

<a name="module_duckdb..Database+close"></a>

#### database.close(callback) ⇒ <code>void</code>
**Kind**: instance method of [<code>Database</code>](#module_duckdb..Database)  

| Param |
| --- |
| callback | 

<a name="module_duckdb..Database+wait"></a>

#### database.wait(callback) ⇒ <code>void</code>
**Kind**: instance method of [<code>Database</code>](#module_duckdb..Database)  

| Param | Description |
| --- | --- |
| callback | TODO: what does this do? |

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
**Kind**: instance method of [<code>Database</code>](#module_duckdb..Database)  

| Param | Description |
| --- | --- |
| path | the database to connect to, either a file path, or `:memory:` |

<a name="module_duckdb..Database+interrupt"></a>

#### database.interrupt(callback) ⇒ <code>void</code>
TODO: what does this do?

**Kind**: instance method of [<code>Database</code>](#module_duckdb..Database)  

| Param |
| --- |
| callback | 

<a name="module_duckdb..Database+prepare"></a>

#### database.prepare(sql) ⇒ <code>Statement</code>
**Kind**: instance method of [<code>Database</code>](#module_duckdb..Database)  

| Param |
| --- |
| sql | 

<a name="module_duckdb..Database+run"></a>

#### database.run(sql, ...params, callback) ⇒ <code>void</code>
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

<a name="module_duckdb..Database+register"></a>

#### database.register(name, return_type, fun) ⇒ <code>this</code>
Register a User Defined Function

Convenience method for Connection#register

**Kind**: instance method of [<code>Database</code>](#module_duckdb..Database)  

| Param |
| --- |
| name | 
| return_type | 
| fun | 

<a name="module_duckdb..Database+unregister"></a>

#### database.unregister(name) ⇒ <code>this</code>
Unregister a User Defined Function

Convenience method for Connection#unregister

**Kind**: instance method of [<code>Database</code>](#module_duckdb..Database)  

| Param |
| --- |
| name | 

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
