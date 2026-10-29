---
layout: docu
redirect_from:
- /docs/current/guides/sql_editors/visualeaf
- /docs/lts/guides/sql_editors/visualeaf
- /docs/preview/guides/sql_editors/visualeaf
- /docs/stable/guides/sql_editors/visualeaf
title: VisuaLeaf SQL Editor
---

[VisuaLeaf](https://visualeaf.com/database/duckdb/) is a cross-platform desktop database client for Windows, macOS, and Linux. Besides a SQL editor, it includes a visual query builder, entity-relationship diagrams, and charts built from query results. VisuaLeaf ships with the DuckDB JDBC driver, so no separate driver installation is required. It offers a free Community Edition as well as paid editions with additional features.

## Installing VisuaLeaf

1. Download and install VisuaLeaf from the [download page](https://visualeaf.com/download).

## Connecting to a DuckDB Database

1. Open VisuaLeaf and click **New Connection** on the welcome screen.

    <img src="{% link images/guides/VisuaLeaf_new_connection.png %}" alt="VisuaLeaf New Connection dialog" title="VisuaLeaf New Connection dialog"/>

2. Type `duckdb` in the search box and select **DuckDB**.

    <img src="{% link images/guides/VisuaLeaf_select_duckdb.png %}" alt="VisuaLeaf DuckDB selected" title="VisuaLeaf DuckDB selected"/>

3. Give the connection a name and enter the path to your DuckDB database file in **Database File Path**, or click **Browse** to pick it. To create a new database file instead, click **New DB**.

    <img src="{% link images/guides/VisuaLeaf_database_file.png %}" alt="VisuaLeaf Database File Path field" title="VisuaLeaf Database File Path field"/>

4. Click **Test Connection** to confirm the file can be opened, then click **Save & Connect**.

    <img src="{% link images/guides/VisuaLeaf_test_connection.png %}" alt="VisuaLeaf Test Connection success" title="VisuaLeaf Test Connection success"/>

    > DuckDB allows only one process to open a database file for writing at a time. If another process (for example, the DuckDB CLI) has the file open, close it before connecting.

5. The connection appears in the **Connections** panel. Expand it to browse the schemas, tables, views, and sequences in the database.

    <img src="{% link images/guides/VisuaLeaf_object_tree.png %}" alt="VisuaLeaf object tree" title="VisuaLeaf object tree"/>

6. Right-click the database and choose **New SQL Editor**, write a query, and click **Run All** to see the results.

    <img src="{% link images/guides/VisuaLeaf_query_results.png %}" alt="VisuaLeaf query results" title="VisuaLeaf query results"/>

Now you are ready to query DuckDB with VisuaLeaf.
