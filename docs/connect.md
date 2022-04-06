---
layout: docu
title: Connect
---
### Connect or Create a Database
To use DuckDB, you must first create a connection to a database. The exact process varies by client. Most clients take a parameter pointing to a database file to read and write from (the file extension may be anything, e.g. `.db`, `.duckdb`, etc.). If the database file does not exist, it will be created. The special value `:memory:` can be used to create an in-memory database where no data is persisted to disk (i.e. all data is lost when you exit the process). 

See the [API docs](http://docs/api/overview) for client-specific details.