---
github_repository: https://github.com/duckdb/duckdb-ui
layout: docu
title: UI Extension
---

The `ui` extension adds a user interface for your local DuckDB instance.

The UI is built and maintained by [MotherDuck](https://motherduck.com/).
An overview of its features can be found
[here](https://motherduck.com/docs/getting-started/motherduck-quick-tour/).

## Requirements

- An environment with a browser.
- Any DuckDB client except Wasm, v1.2.1 or later.

## Usage

To start the UI from the command line:

```bash
duckdb -ui
```

To start the UI from SQL:

```sql
CALL start_ui();
```

Running either of these will open the UI in your default browser.

The UI connects to the DuckDB instance it was started from,
so any data you’ve already loaded will be available.
Since this instance is a native process (not Wasm), it can leverage all
the resources of your local environment: all cores, memory, and files.
Closing this instance will cause the UI to stop working.

The UI is served from an HTTP server embedded in DuckDB.
To start this server without launching the browser, run:

```sql
CALL start_ui_server();
```

You can then load the UI in your browser by navigating to
`http://localhost:4213`.

To stop the HTTP server, run:

```sql
CALL stop_ui_server();
```

## Local Query Execution

By default, the DuckDB UI runs your queries fully locally: your queries and data never leave your computer.
If you would like to use [MotherDuck](https://motherduck.com/) through the UI, you have to opt-in explicitly and sign into MotherDuck.

## Configuration

### Local Port

The local port of the HTTP server can be configured with a SQL command like:

```sql
SET ui_local_port = 4213;
```

The environment variable `ui_local_port` can also be used.

The default port is 4213. (Why? 4 = D, 21 = U, 3 = C)

### Remote URL

The local HTTP server fetches the files for the UI from a remote HTTP
server so they can be kept up-to-date.

The default URL for the remote server is <https://ui.duckdb.org>.

An alternate remote URL can be configured with a SQL command like:

```sql
SET ui_remote_url = 'https://ui.duckdb.org';
```

The environment variable `ui_remote_port` can also be used.

This setting is available mainly for testing purposes.

Be sure you trust any URL you configure, as the application can access
the data you load into DuckDB.

Because of this risk, the setting is only respected
if `allow_unsigned_extensions` is enabled.

### Polling Interval

The UI extension polls for some information on a background thread.
It watches for changes to the list of attached databases,
and it detects when you connect to MotherDuck.

These checks take very little time to complete, so the default polling
interval is short (284 milliseconds).
You can configure it with a SQL command like:

```sql
SET ui_polling_interval = 284;
```

The environment variable `ui_polling_interval` can also be used.

Setting the polling interval to 0 will disable polling entirely.
This is not recommended, as the list of databases in the UI could get
out of date, and some ways of connecting to MotherDuck will not work
properly.

## Tips

### Opening a CSV File with the DuckDB UI

Using the [DuckDB CLI client]({% link docs/preview/clients/cli/overview.md %}),
you can start the UI with a CSV available as a view using the [`-cmd` argument]({% link docs/preview/clients/cli/arguments.md %}):

```bash
duckdb -cmd "CREATE VIEW ⟨view_name⟩ AS FROM '⟨filename⟩.csv';" -ui
```

## Limitations

* The UI currently does not support the ARM-based Windows platforms (`windows_arm64` and `windows_arm64_mingw`).
* The UI uses DuckDB as a storage internally (e.g., for saving notebooks), therefore, it [does not support read-only mode](https://github.com/duckdb/duckdb-ui/issues/61).
