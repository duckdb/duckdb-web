---
layout: docu
redirect_from:
- /docs/extensions/substrait
title: Substrait Extension
---

The main goal of the `substrait` extension is to support both production and consumption of Substrait query plans in DuckDB.

This extension is mainly exposed via 3 different APIs - the SQL API, the Python API, and the R API.
Here we depict how to consume and produce Substrait query plans in each API.

> The Substrait integration is currently experimental. Support is currently only available on request.
> If you have not asked for permission to ask for support, [contact us prior to opening an issue](https://duckdblabs.com/contact/).
> If you open an issue without doing so, we will close it without further review.

## Installing and Loading

The Substrait extension is an autoloadable extensions, meaning that it will be loaded at runtime whenever one of the substrait functions is called. To explicitly install and load the released version of the Substrait extension, you can also use the following SQL commands.

```sql
INSTALL substrait;
LOAD substrait;
```

## SQL

In the SQL API, users can generate Substrait plans (into a BLOB or a JSON) and consume Substrait plans.

### BLOB Generation

To generate a Substrait BLOB the `get_substrait(sql)` function must be called with a valid SQL select query.
```sql
CREATE TABLE crossfit (exercise TEXT, difficulty_level INT);
INSERT INTO crossfit VALUES ('Push Ups', 3), ('Pull Ups', 5) , ('Push Jerk', 7), ('Bar Muscle Up', 10);
```
```sql
.mode line
CALL get_substrait('SELECT count(exercise) AS exercise FROM crossfit WHERE difficulty_level <= 5');
```
```text
Plan BLOB = \x12\x09\x1A\x07\x10\x01\x1A\x03lte\x12\x11\x1A\x0F\x10\x02\x1A\x0Bis_not_null\x12\x09\x1A\x07\x10\x03\x1A\x03and\x12\x0B\x1A\x09\x10\x04\x1A\x05count\x1A\xC8\x01\x12\xC5\x01\x0A\xB8\x01:\xB5\x01\x12\xA8\x01\x22\xA5\x01\x12\x94\x01\x0A\x91\x01\x12/\x0A\x08exercise\x0A\x10difficulty_level\x12\x11\x0A\x07\xB2\x01\x04\x08\x0D\x18\x01\x0A\x04*\x02\x10\x01\x18\x02\x1AJ\x1AH\x08\x03\x1A\x04\x0A\x02\x10\x01\x22\x22\x1A \x1A\x1E\x08\x01\x1A\x04*\x02\x10\x01\x22\x0C\x1A\x0A\x12\x08\x0A\x04\x12\x02\x08\x01\x22\x00\x22\x06\x1A\x04\x0A\x02(\x05\x22\x1A\x1A\x18\x1A\x16\x08\x02\x1A\x04*\x02\x10\x01\x22\x0C\x1A\x0A\x12\x08\x0A\x04\x12\x02\x08\x01\x22\x00\x22\x06\x0A\x02\x0A\x00\x10\x01:\x0A\x0A\x08crossfit\x1A\x00\x22\x0A\x0A\x08\x08\x04*\x04:\x02\x10\x01\x1A\x08\x12\x06\x0A\x02\x12\x00\x22\x00\x12\x08exercise2\x0A\x10\x18*\x06DuckDB
```

### JSON Generation

To generate a JSON representing the Substrait plan the `get_substrait_json(sql)` function must be called with a valid SQL select query.
```sql
CALL get_substrait_json('SELECT count(exercise) AS exercise FROM crossfit WHERE difficulty_level <= 5');
```
```json
 Json = {"extensions":[{"extensionFunction":{"functionAnchor":1,"name":"lte"}},{"extensionFunction":{"functionAnchor":2,"name":"is_not_null"}},{"extensionFunction":{"functionAnchor":3,"name":"and"}},{"extensionFunction":{"functionAnchor":4,"name":"count"}}],"relations":[{"root":{"input":{"project":{"input":{"aggregate":{"input":{"read":{"baseSchema":{"names":["exercise","difficulty_level"],"struct":{"types":[{"varchar":{"length":13,"nullability":"NULLABILITY_NULLABLE"}},{"i32":{"nullability":"NULLABILITY_NULLABLE"}}],"nullability":"NULLABILITY_REQUIRED"}},"filter":{"scalarFunction":{"functionReference":3,"outputType":{"bool":{"nullability":"NULLABILITY_NULLABLE"}},"arguments":[{"value":{"scalarFunction":{"functionReference":1,"outputType":{"i32":{"nullability":"NULLABILITY_NULLABLE"}},"arguments":[{"value":{"selection":{"directReference":{"structField":{"field":1}},"rootReference":{}}}},{"value":{"literal":{"i32":5}}}]}}},{"value":{"scalarFunction":{"functionReference":2,"outputType":{"i32":{"nullability":"NULLABILITY_NULLABLE"}},"arguments":[{"value":{"selection":{"directReference":{"structField":{"field":1}},"rootReference":{}}}}]}}}]}},"projection":{"select":{"structItems":[{}]},"maintainSingularStruct":true},"namedTable":{"names":["crossfit"]}}},"groupings":[{}],"measures":[{"measure":{"functionReference":4,"outputType":{"i64":{"nullability":"NULLABILITY_NULLABLE"}}}}]}},"expressions":[{"selection":{"directReference":{"structField":{}},"rootReference":{}}}]}},"names":["exercise"]}}],"version":{"minorNumber":24,"producer":"DuckDB"}}
```

### BLOB Consumption

To consume a Substrait BLOB the `from_substrait(blob)` function must be called with a valid Substrait BLOB plan.
```sql
CALL from_substrait('\x12\x09\x1A\x07\x10\x01\x1A\x03lte\x12\x11\x1A\x0F\x10\x02\x1A\x0Bis_not_null\x12\x09\x1A\x07\x10\x03\x1A\x03and\x12\x0B\x1A\x09\x10\x04\x1A\x05count\x1A\xC8\x01\x12\xC5\x01\x0A\xB8\x01:\xB5\x01\x12\xA8\x01\x22\xA5\x01\x12\x94\x01\x0A\x91\x01\x12/\x0A\x08exercise\x0A\x10difficulty_level\x12\x11\x0A\x07\xB2\x01\x04\x08\x0D\x18\x01\x0A\x04*\x02\x10\x01\x18\x02\x1AJ\x1AH\x08\x03\x1A\x04\x0A\x02\x10\x01\x22\x22\x1A \x1A\x1E\x08\x01\x1A\x04*\x02\x10\x01\x22\x0C\x1A\x0A\x12\x08\x0A\x04\x12\x02\x08\x01\x22\x00\x22\x06\x1A\x04\x0A\x02(\x05\x22\x1A\x1A\x18\x1A\x16\x08\x02\x1A\x04*\x02\x10\x01\x22\x0C\x1A\x0A\x12\x08\x0A\x04\x12\x02\x08\x01\x22\x00\x22\x06\x0A\x02\x0A\x00\x10\x01:\x0A\x0A\x08crossfit\x1A\x00\x22\x0A\x0A\x08\x08\x04*\x04:\x02\x10\x01\x1A\x08\x12\x06\x0A\x02\x12\x00\x22\x00\x12\x08exercise2\x0A\x10\x18*\x06DuckDB'::BLOB);
```
```text
exercise = 2
```

## Python

Substrait extension is autoloadable, but if you prefer to do so explicitly, you can use the relevant Python syntax within a connection:
```python
import duckdb

con = duckdb.connect()
con.install_extension("substrait")
con.load_extension("substrait")
```

### BLOB Generation

To generate a Substrait BLOB the `get_substrait(sql)` function must be called, from a connection, with a valid SQL select query.
```python
con.execute(query = "CREATE TABLE crossfit (exercise TEXT, difficulty_level INT)")
con.execute(query = "INSERT INTO crossfit VALUES ('Push Ups', 3), ('Pull Ups', 5) , ('Push Jerk', 7), ('Bar Muscle Up', 10)")

proto_bytes = con.get_substrait(query="SELECT count(exercise) AS exercise FROM crossfit WHERE difficulty_level <= 5").fetchone()[0]
```


### Json Generation

To generate a JSON representing the Substrait plan the `get_substrait_json(sql)` function, from a connection, must be called with a valid SQL select query.
```python
json = con.get_substrait_json("SELECT count(exercise) AS exercise FROM crossfit WHERE difficulty_level <= 5").fetchone()[0]
```

### BLOB Consumption

To consume a Substrait BLOB the `from_substrait(blob)` function must be called, from the connection, with a valid Substrait BLOB plan.
```python
query_result = con.from_substrait(proto=proto_bytes)
```

## R

By default the extension will be autoloaded on first use. To explicitly install and load this extension in R, use the following commands:

```r
library("duckdb")
con <- dbConnect(duckdb::duckdb())
dbExecute(con, "INSTALL substrait")
dbExecute(con, "LOAD substrait")
```

### BLOB Generation

To generate a Substrait BLOB the `duckdb_get_substrait(con, sql)` function must be called, with a connection and a valid SQL select query.
```r
dbExecute(con, "CREATE TABLE crossfit (exercise TEXT, difficulty_level INT)")
dbExecute(con, "INSERT INTO crossfit VALUES ('Push Ups', 3), ('Pull Ups', 5) , ('Push Jerk', 7), ('Bar Muscle Up', 10)")

proto_bytes <- duckdb::duckdb_get_substrait(con, "SELECT * FROM crossfit LIMIT 5")
```

### JSON Generation

To generate a JSON representing the Substrait plan `duckdb_get_substrait_json(con, sql)` function, with a connection and a valid SQL select query.
```r
json <- duckdb::duckdb_get_substrait_json(con, "SELECT count(exercise) AS exercise FROM crossfit WHERE difficulty_level <= 5")
```

### BLOB Consumption

To consume a Substrait BLOB the `duckdb_prepare_substrait(con, blob)` function must be called, with a connection and a valid Substrait BLOB plan.
```r
result <- duckdb::duckdb_prepare_substrait(con, proto_bytes)
df <- dbFetch(result)
```

## GitHub Repository

[<span class="github">GitHub</span>](https://github.com/duckdb/substrait)
