---
layout: docu
title: Tableau - A Data Visualisation Tool
selected: Tableau - A Data Visualisation Tool
---

# Visualising DuckDB databases with Tableau

[Tableau](https://www.tableau.com/) is a popular commercial data visualisation tool. 
In addition to a large number of built in connectors,
it also provides generic database connectivity via ODBC and JDBC connectors.

Tableau has two main versions: Desktop and Online (Server).
* For Desktop, connecting to a DuckDB database is similar to working in an embedded environemnt like Python.
* For Online, since DuckDB is in-process, the data needs to be either on the server itself
or in a remote data bucket that is accessible from the server.

## Database Creation

The Tableau connection process requires a physical DuckDB database,
so all data sets need to be created and saved within a DuckDB database file.
The data sets do not actually need to be imported into DuckDB tables;
it suffices to create views of the data.
For example, this will create a view of the `h2oai` parquet test file in the current DuckDB code base:

```sql
CREATE VIEW h2oai AS (
    FROM read_parquet('/Users/username/duckdb/data/parquet-testing/h2oai/h2oai_group_small.parquet')
);
```


Note that you should use full path names to local files so that they can be found from inside Tableau.
Also note that you will need to use a version of the driver that is compatible (i.e., from the same release) 
as the database format you are using.

# Connecting Tableau Desktop to DuckDB

Tableau provides documentation on how to [install a JDBC driver](https://help.tableau.com/current/pro/desktop/en-us/jdbc_tableau.htm) for Tableau to use.
Note that Tableau needs to be restarted any time you add or modify drivers.

## MacOS

As of this writing, the MacOS DuckDB ODBC Driver seems to crash 
the Tableau Protocol Server (a sub-process used to isolate drivers from the main application).
This means you should use the JDBC driver for now.

### Install the DuckDB JDBC Driver:

1. [Download](https://github.com/duckdb/duckdb/releases/download/{{ site.currentduckdbversion }}/duckdb_jdbc-osx-universal.jar) the DuckDB JDBC driver. This is a file called `duckdb_jdbc-osx-universal.jar`. Make sure this is from the same build as the version of DuckDB used to create the database file!
2. Follow the [Tableau directions](https://help.tableau.com/current/pro/desktop/en-us/jdbc_tableau.htm) and copy this file to either `/Library/JDBC` (for access by all users) or `~/Library/JDBC` (for access by your login alone) (e.g., `cp ~/Downloads/duckdb_jdbc-osx-universal.jar ~/Library/JDBC`)

### Connect to your data

3. Create a  DuckDB file containing your views and/or data.
4. Launch Tableau
5. Under Connect > To a Server > More... click on "Other Databases (JDBC)"  This will bring up the connection dialogue box. For the URL, enter `jdbc:duckdb:/User/username/path/to/database.db`. For the Dialect, choose `PostgreSQL`. the rest of the fields can be ignored:

![tableau-osx-jdbc](/images/guides/tableau/tableau-osx-jdbc.png)


# Output

Once loaded, you can run queries against your data!
Here is the result of the first h2oai benchmark query from the parquet test file:

![tableau-parquet](/images/guides/tableau/h2oai-group-by-1.png)
