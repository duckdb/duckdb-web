---
layout: docu
redirect_from:
- docs/archive/0.9.2/api/nodejs/overview
- docs/archive/0.9.2/api/nodejs
title: Node.js API
---

This package provides a Node.js API for DuckDB.
The API for this client is somewhat compliant to the SQLite node.js client for easier transition.

Load the package and create a database object:

```js
const duckdb = require('duckdb');
const db = new duckdb.Database(':memory:'); // or a file name for a persistent DB
```

All options as described on [Database configuration](../../sql/configuration#configuration-reference) can be (optionally) supplied to the `Database` constructor as second argument. The third argument can be optionally supplied to get feedback on the given options.

```js
const db = new duckdb.Database(':memory:', {
    "access_mode": "READ_WRITE",
    "max_memory": "512MB",
    "threads": "4"
}, (err) => {
  if (err) {
    console.error(err);
  }
});
```

Then you can run a query:

```js
db.all('SELECT 42 AS fortytwo', function(err, res) {
  if (err) {
    throw err;
  }
  console.log(res[0].fortytwo)
});
```

Other available methods are `each`, where the callback is invoked for each row, `run` to execute a single statement without results and `exec`, which can execute several SQL commands at once but also does not return results. All those commands can work with prepared statements, taking the values for the parameters as additional arguments. For example like so:

```js
db.all('SELECT ?::INTEGER AS fortytwo, ?::STRING AS hello', 42, 'Hello, World', function(err, res) {
  if (err) {
    throw err;
  }
  console.log(res[0].fortytwo)
  console.log(res[0].hello)
});
```

However, these are all shorthands for something much more elegant. A database can have multiple `Connection`s, those are created using `db.connect()`.

```js
const con = db.connect();
```

You can create multiple connections, each with their own transaction context.


`Connection` objects also contain shorthands to directly call `run()`, `all()` and `each()` with parameters and callbacks, respectively, for example:

```js
con.all('SELECT 42 AS fortytwo', function(err, res) {
  if (err) {
    throw err;
  }
  console.log(res[0].fortytwo)
});
```

From connections, you can create prepared statements (and only that) using `con.prepare()`:

```js
const stmt = con.prepare('select ?::INTEGER as fortytwo');
``` 

To execute this statement, you can call for example `all()` on the `stmt` object:

```js
stmt.all(42, function(err, res) {
  if (err) {
    throw err;
  }
  console.log(res[0].fortytwo)
});
```

You can also execute the prepared statement multiple times. This is for example useful to fill a table with data:

```js
con.run('CREATE TABLE a (i INTEGER)');
const stmt = con.prepare('INSERT INTO a VALUES (?)');
for (let i = 0; i < 10; i++) {
  stmt.run(i);
}
stmt.finalize();
con.all('SELECT * FROM a', function(err, res) {
  if (err) {
    throw err;
  }
  console.log(res)
});
```

`prepare()` can also take a callback which gets the prepared statement as an argument:

```js
const stmt = con.prepare('select ?::INTEGER as fortytwo', function(err, stmt) {
  stmt.all(42, function(err, res) {
    if (err) {
      throw err;
    }
    console.log(res[0].fortytwo)
  });
});
```

[Apache Arrow](https://duckdb.org/docs/guides/python/sql_on_arrow) can be used to insert data into DuckDB without making a copy:

```js
const arrow = require('apache-arrow');
const db = new duckdb.Database(':memory:');

const jsonData = [
  {"userId":1,"id":1,"title":"delectus aut autem","completed":false},
  {"userId":1,"id":2,"title":"quis ut nam facilis et officia qui","completed":false}
];

// note; doesn't work on Windows yet
db.exec(`INSTALL arrow; LOAD arrow;`, (err) => {
    if (err) {
        throw err;
    }

    const arrowTable = arrow.tableFromJSON(jsonData);
    db.register_buffer("jsonDataTable", [arrow.tableToIPC(arrowTable)], true, (err, res) => {
        if (err) {
            throw err;
        }

        // `SELECT * FROM jsonDataTable` would return the entries in `jsonData`
    });
});

```