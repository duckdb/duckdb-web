---
layout: docu
title: MySQL Import
---

To run a query directly on a running MySQL database, the [`mysql` extension](../../extensions/mysql) is required.

## Installation and Loading

The extension can be installed use the `INSTALL` SQL command. This only needs to be run once.

```sql
INSTALL mysql;
```

To load the `mysql` extension for usage, use the `LOAD` SQL command:

```sql
LOAD mysql;
```

## Usage

After the `mysql` extension is installed, you can attach to a MySQL database using the following command:

```sql
ATTACH 'host=localhost user=root port=0 database=mysqlscanner' AS mysql_db (TYPE mysql_scanner, READ_ONLY);
USE mysqlscanner;
```

The string used by `ATTACH` is a PostgreSQL-style connection string (_not_ a MySQL connection string!). It is a list of connection arguments provided in `{key}={value}` format. Below is a list of valid arguments. Any options not provided are replaced by their default values.

| Setting  |   Default    |
|----------|--------------|
| host     | localhost    |
| user     | current user |
| password |              |
| database | NULL         |
| port     | 0            |
| socket   | NULL         |

You can directly read and write the MySQL database:

```sql
CREATE TABLE tbl(id INTEGER, name VARCHAR);
INSERT INTO tbl VALUES (42, 'DuckDB');
```

For a list of supported operations, see the [MySQL extension documentation](../../extensions/mysql#supported-operations).
