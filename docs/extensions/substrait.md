---
layout: docu
title: Substrait
selected: Documentation/Substrait
---

The main goal of this extension is to support a both production and consumption of substrait query plans in DuckDB.

This extension is mainly exposed via 3 different APIs. 1) The SQL API, 2) The Python API, 3) The R API.
Here we depict how to consume and produce substrait query plans in each API.

Additionally, see the [repo](https://github.com/duckdblabs/substrait) for further usage details.

### SQL
In the SQL API, users can generate substrait plans (into a blob or a JSON) and consume substrait plans.

Before using the extension, you must always properly install and load it. 
To install and load the released version of the substrait library, you must execute the following SQL commands.
```sql
INSTALL('substrait');
LOAD('substrait')
```

1) Blob Generation
     
     To generate a substrait blob the ```get_substrait(SQL)``` function must be called with a valid SQL select query.
     ```sql
     CREATE TABLE crossfit (exercise text,dificulty_level int);
     INSERT INTO crossfit VALUES ('Push Ups', 3), ('Pull Ups', 5) , (' Push Jerk', 7), ('Bar Muscle Up', 10);
     
     CALL get_substrait('select count(exercise) as exercise from crossfit where dificulty_level <=5')
     ----
     \x12\x09\x1A\x07\x10\x01\x1A\x03lte\x12\x11\x1A\x0F\x10\x02\x1A\x0Bis_not_null\x12\x09\x1A\x07\x10\x03\x1A\x03and\x12\x10\x1A\x0E\x10\x04\x1A\x0Acount_star\x1A\xCB\x01\x12\xC8\x01\x0A\xBB\x01:\xB8\x01\x12\xAB\x01"\xA8\x01\x12\x97\x01\x0A\x94\x01\x12.\x0A\x08exercise\x0A\x0Fdificulty_level\x12\x11\x0A\x07\xB2\x01\x04\x08\x0D\x18\x01\x0A\x04*\x02\x10\x01\x18\x02\x1AJ\x1AH\x08\x03\x1A\x04\x0A\x02\x10\x01""\x1A \x1A\x1E\x08\x01\x1A\x04*\x02\x10\x01"\x0C\x1A\x0A\x12\x08\x0A\x04\x12\x02\x08\x01"\x00"\x06\x1A\x04\x0A\x02(\x05"\x1A\x1A\x18\x1A\x16\x08\x02\x1A\x04*\x02\x10\x01"\x0C\x1A\x0A\x12\x08\x0A\x04\x12\x02\x08\x01"\x00"\x0A\x0A\x06\x0A\x02\x08\x01\x0A\x00\x10\x01:\x0A\x0A\x08crossfit\x1A\x00"\x0A\x0A\x08\x08\x04*\x04:\x02\x10\x01\x1A\x08\x12\x06\x0A\x02\x12\x00"\x00\x12\x08exercise
     ```
2) Json Generation
     
     To generate a json representing  the substrait plan the ```get_substrait_json(SQL)``` function must be called with a valid SQL select query.
     ```sql
     CALL get_substrait_json('select count(exercise) as exercise from crossfit where dificulty_level <=5')
     ----
     {"extensions":[{"extensionFunction":{"functionAnchor":1,"name":"lte"}},{"extensionFunction":{"functionAnchor":2,"name":"is_not_null"}},{"extensionFunction":{"functionAnchor":3,"name":"and"}},{"extensionFunction":{"functionAnchor":4,"name":"count_star"}}],"relations":[{"root":{"input":{"project":{"input":{"aggregate":{"input":{"read":{"baseSchema":{"names":["exercise","dificulty_level"],"struct":{"types":[{"varchar":{"length":13,"nullability":"NULLABILITY_NULLABLE"}},{"i32":{"nullability":"NULLABILITY_NULLABLE"}}],"nullability":"NULLABILITY_REQUIRED"}},"filter":{"scalarFunction":{"functionReference":3,"outputType":{"bool":{"nullability":"NULLABILITY_NULLABLE"}},"arguments":[{"value":{"scalarFunction":{"functionReference":1,"outputType":{"i32":{"nullability":"NULLABILITY_NULLABLE"}},"arguments":[{"value":{"selection":{"directReference":{"structField":{"field":1}},"rootReference":{}}}},{"value":{"literal":{"i32":5}}}]}}},{"value":{"scalarFunction":{"functionReference":2,"outputType":{"i32":{"nullability":"NULLABILITY_NULLABLE"}},"arguments":[{"value":{"selection":{"directReference":{"structField":{"field":1}},"rootReference":{}}}}]}}}]}},"projection":{"select":{"structItems":[{"field":1},{}]},"maintainSingularStruct":true},"namedTable":{"names":["crossfit"]}}},"groupings":[{}],"measures":[{"measure":{"functionReference":4,"outputType":{"i64":{"nullability":"NULLABILITY_NULLABLE"}}}}]}},"expressions":[{"selection":{"directReference":{"structField":{}},"rootReference":{}}}]}},"names":["exercise"]}}]}
     ```
3) Blob Consumption
     
     To consume a substrait blob the ```from_substrait(blob)``` function must be called with a valid substrait BLOB plan.
     ```sql
     CALL from_substrait('\x12\x07\x1A\x05\x1A\x03lte\x12\x11\x1A\x0F\x10\x01\x1A\x0Bis_not_null\x12\x09\x1A\x07\x10\x02\x1A\x03and\x12\x10\x1A\x0E\x10\x03\x1A\x0Acount_star\x1A\xA4\x01\x12\xA1\x01\x0A\x94\x01:\x91\x01\x12\x86\x01"\x83\x01\x12y:w\x12c\x12a\x12+\x0A)\x12\x1B\x0A\x08exercise\x0A\x0Fdificulty_level:\x0A\x0A\x08crossfit\x1A2\x1A0\x08\x02"\x18\x1A\x16\x1A\x14"\x0A\x1A\x08\x12\x06\x0A\x04\x12\x02\x08\x01"\x06\x1A\x04\x0A\x02(\x05"\x12\x1A\x10\x1A\x0E\x08\x01"\x0A\x1A\x08\x12\x06\x0A\x04\x12\x02\x08\x01\x1A\x08\x12\x06\x0A\x04\x12\x02\x08\x01\x1A\x06\x12\x04\x0A\x02\x12\x00\x1A\x00"\x04\x0A\x02\x08\x03\x1A\x06\x12\x04\x0A\x02\x12\x00\x12\x08exercise'::BLOB)
     ----
     2
   ```

### Python
Before using the extension you must remember to properly load it. To load an extension in python, you must execute the sql commands within a connection.
```python
import duckdb

con = duckdb.connect()
con.execute("INSTALL('substrait')");
con.execute("LOAD('substrait')")
```

1) Blob Generation
     
     To generate a substrait blob the ```get_substrait(SQL)``` function must be called, from a connection, with a valid SQL select query.
     ```python
     con.execute('CREATE TABLE crossfit (exercise text,dificulty_level int);')
     con.execute("INSERT INTO crossfit VALUES ('Push Ups', 3), ('Pull Ups', 5) , (' Push Jerk', 7), ('Bar Muscle Up', 10);")
     
     proto_bytes =  con.get_substrait("select count(exercise) as exercise from crossfit where dificulty_level <=5")     
   ```
2) Json Generation
     
     To generate a json representing  the substrait plan the ```get_substrait_json(SQL)``` function, from a connection, must be called with a valid SQL select query.
     ```python
     json =  con.get_substrait_json("select count(exercise) as exercise from crossfit where dificulty_level <=5").fetchone()[0]
     ```
3) Blob Consumption
     
     To consume a substrait blob the ```from_substrait(blob)``` function must be called, from the connection, with a valid substrait BLOB plan.
     ```python
     query_result = con.from_substrait(proto_bytes)
    ```

### R
Before using the extension you must remember to properly load it. To load an extension in R, you must execute the sql commands within a connection.
```r
con <- dbConnect(duckdb::duckdb())
dbExecute(con, "INSTALL('substrait')"))
dbExecute(con, "LOAD('substrait')")
```
1) Blob Generation
     
     To generate a substrait blob the ```duckdb_get_substrait(con,SQL)``` function must be called, with a connection and a valid SQL select query.
     ```r
     dbExecute(con, "CREATE TABLE crossfit (exercise text,dificulty_level int);")
     dbExecute(con, "INSERT INTO crossfit VALUES ('Push Ups', 3), ('Pull Ups', 5) , (' Push Jerk', 7), ('Bar Muscle Up', 10);")
     
     proto_bytes <- duckdb::duckdb_get_substrait(con, "select * from integers limit 5")    
   ```
2) Json Generation
     
     To generate a json representing  the substrait plan  ```duckdb_get_substrait_json(con,SQL)``` function, with a connection and a valid SQL select query.
     ```r
     json <- duckdb::duckdb_get_substrait_json(con, "select count(exercise) as exercise from crossfit where dificulty_level <=5")
     ```
3) Blob Consumption
     
     To consume a substrait blob the ```duckdb_prepare_substrait(con,blob)``` function must be called, with a connection and a valid substrait BLOB plan.
     ```r
      result <- duckdb::duckdb_prepare_substrait(con, proto_bytes)
      df <- dbFetch(result)
    ```
