---
layout: docu
title: LibreDB Studio SQL Editor
---

[LibreDB Studio](https://github.com/libredb/libredb-studio) is an open-source, self-hosted, browser-based SQL editor. It runs as a single server, either via `npx`, Docker, or a native package, and is reached through the browser rather than installed as a desktop application. LibreDB Studio connects to DuckDB directly through its native Node.js binding, so it queries a DuckDB database file (or an in-memory database) without going through a JDBC or ODBC driver.

## Installing LibreDB Studio

1. Start LibreDB Studio with `npx`, which downloads and runs the latest release:

    ```bash
    npx @libredb/studio
    ```

    Docker, Homebrew, and other install options are listed in the [project's README](https://github.com/libredb/libredb-studio#getting-started).

2. Open `http://localhost:3000` in a browser. On first run, the admin password is printed to the console.

## Connecting to a DuckDB Database

1. Click the **+** button next to the LibreDB Studio logo in the sidebar to open the New Connection dialog.

    <img src="{% link images/guides/LibreDB_Studio_new_connection.png %}" alt="LibreDB Studio New Connection dialog" title="LibreDB Studio New Connection dialog"/>

2. Select **DuckDB** from the database type grid, and give the connection a name.

    <img src="{% link images/guides/LibreDB_Studio_select_duckdb.png %}" alt="LibreDB Studio DuckDB selected" title="LibreDB Studio DuckDB selected"/>

3. Enter the path to the DuckDB database file in **Database File Path**. To use an in-memory database, enter `:memory:`. Since LibreDB Studio runs as a server, the path is resolved on the machine running the server, not on the machine running the browser.

    <img src="{% link images/guides/LibreDB_Studio_database_path.png %}" alt="LibreDB Studio Database File Path field" title="LibreDB Studio Database File Path field"/>

4. Click **Test Connection** to confirm the file can be opened, then click **Establish Connection** to save it.

    <img src="{% link images/guides/LibreDB_Studio_test_connection.png %}" alt="LibreDB Studio Test Connection success" title="LibreDB Studio Test Connection success"/>

5. The connection appears in the sidebar. Expand it to browse the tables, views, macros, and sequences in the database.

    <img src="{% link images/guides/LibreDB_Studio_object_tree.png %}" alt="LibreDB Studio object tree" title="LibreDB Studio object tree"/>

6. Open a query tab, write SQL, and run it with **Run** or <kbd>Ctrl</kbd>+<kbd>Enter</kbd> (<kbd>Cmd</kbd>+<kbd>Enter</kbd> on macOS).

    <img src="{% link images/guides/LibreDB_Studio_query_results.png %}" alt="LibreDB Studio query results" title="LibreDB Studio query results"/>

Now you are ready to query DuckDB with LibreDB Studio.
