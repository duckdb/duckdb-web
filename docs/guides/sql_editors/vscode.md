---
layout: docu
title: "VSCode Extension: SQLTools for DuckDB"
selected: "VSCode Extension: SQLTools for DuckDB"
---

![SQLTools for DuckDB](/images/guides/vscode/sqltools-for-duckdb-dark.png)

## Why SQLTools?

SQLTools is an open-source VSCode extension that allows you to explore your database, write SQL and run SQL queries without leaving VSCode. 

It removes the need for a standalone SQL editor or console when using your database.



## Install and Connect

1. Install the [SQLTools extension](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools).
1. Install the [DuckDB Driver](https://marketplace.visualstudio.com/items?itemName=evidence.sqltools-duckdb-driver).
1. Click on SQLTools (the database icon) in the left sidebar.
1. Click `Add New Connection`, select `DuckDB` and follow the instructions.

_The first time you use the extension, you may be prompted to install DuckDB._

![Install and Connect](/images/guides/vscode/install.gif)

## Features

1. **Connect** to a local, in-memory or MotherDuck (via service token) DuckDB instance
1. **Run queries** against a DuckDB instance
1. **Explore** DB tables and columns in the sidebar
1. **View table results** by selecting them in the sidebar
1. **Autocomplete** for common keywords (e.g. SELECT, FROM, WHERE) and table names


## Documentation

Full documentation for SQLTools for DuckDB is available [here](https://github.com/evidence-dev/sqltools-duckdb-driver/).

## Troubleshooting

This extension is maintained by [Evidence](https://evidence.dev/), for support:
- Open an issue on [GitHub](https://github.com/evidence-dev/sqltools-duckdb-driver)
- Ask a question in the [Slack #sqltools channel](https://join.slack.com/t/evidencedev/shared_invite/zt-uda6wp6a-hP6Qyz0LUOddwpXW5qG03Q)