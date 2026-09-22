---
layout: docu
title: Beekeeper Studio SQL Editor
---

[Beekeeper Studio](https://www.beekeeperstudio.io/db/duckdb-client/) is a free, open-source SQL editor and database manager with a modern, easy-to-use interface. It is available for Windows, macOS, and Linux, and also offers a paid Ultimate tier with cloud sync and team-sharing features. Beekeeper Studio connects to DuckDB natively rather than through a JDBC or ODBC driver, so no separate driver installation is required.

## Installing Beekeeper Studio

1. Install Beekeeper Studio using the download links and instructions found at their [download page](https://www.beekeeperstudio.io/get).

## Connecting to a DuckDB Database

1. Open Beekeeper Studio and click **New Connection**.

    <img src="{% link images/guides/Beekeeper_Studio_new_connection.png %}" alt="Beekeeper Studio New Connection" title="Beekeeper Studio New Connection"/>

2. Select **DuckDB** from the connection type dropdown.

    <img src="{% link images/guides/Beekeeper_Studio_select_duckdb.png %}" alt="Beekeeper Studio Select DuckDB" title="Beekeeper Studio Select DuckDB"/>

3. Enter the path to your DuckDB database file, or click **Create** to create a new one.

    <img src="{% link images/guides/Beekeeper_Studio_database_file.png %}" alt="Beekeeper Studio Database File" title="Beekeeper Studio Database File"/>

4. Optionally, name the connection and choose a color for the connection.

5. Click **Connect**.

    <img src="{% link images/guides/Beekeeper_Studio_connect.png %}" alt="Beekeeper Studio Connect" title="Beekeeper Studio Connect"/>

6. Once connected, you can browse tables and views in the left-hand sidebar.

    <img src="{% link images/guides/Beekeeper_Studio_object_tree.png %}" alt="Beekeeper Studio Object Tree" title="Beekeeper Studio Object Tree"/>

7. Open a new SQL tab, write a query, and run it to see the results.

    <img src="{% link images/guides/Beekeeper_Studio_query_results.png %}" alt="Beekeeper Studio Query Results" title="Beekeeper Studio Query Results"/>

Now you're ready to query DuckDB with Beekeeper Studio.
