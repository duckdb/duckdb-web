---
layout: docu
redirect_from:
- /docs/stable/guides/sql_editors/dbine
title: DBine SQL Editor
how_to_topic: tools-meta
---

[DBine](https://dbine.com) is a free, open-source (Apache 2.0) desktop database manager for Windows, macOS, and Linux that works with 130+ databases and cloud services. Besides a SQL editor, it includes notebooks, charts built from query results, and schema compare. DBine downloads the official DuckDB library the first time a DuckDB connection is opened, so no separate driver installation is required.

## Installing DBine

1. Download and install DBine from the [releases page](https://github.com/addlayer-io/dbine/releases).

## Connecting to a DuckDB Database

1. Open DBine and click **New connection**, then select **DuckDB** from the list of engines.
2. Give the connection a name and enter the path to your DuckDB database file in **Database file**, or click the folder button to pick it. Leave the field empty or enter `:memory:` to open an in-memory database.
3. Click **Test connection** to confirm the file can be opened, then click **Save and connect**.

    <img src="{% link images/guides/DBine_new_connection.png %}" alt="DBine new connection form for DuckDB" title="DBine new connection form for DuckDB"/>

    > DuckDB allows only one process to open a database file for writing at a time. If another process (for example, the DuckDB CLI) has the file open, close it before connecting.

4. The connection appears in the **Explorer**. Expand it to browse the schemas, tables, views, and columns of the database.
5. Right-click the database and choose **New query**, write a query, and click **Run** to see the results. Parquet, CSV, and JSON files can be queried directly from the editor:

    ```sql
    SELECT * FROM 'sales_2026.parquet' LIMIT 10;
    ```

    <img src="{% link images/guides/DBine_query_results.png %}" alt="DBine query results" title="DBine query results"/>

Now you are ready to query DuckDB with DBine.
