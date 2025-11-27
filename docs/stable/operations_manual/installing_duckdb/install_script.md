---
layout: docu
title: Install Script
---

You can install the [DuckDB CLI client]({% link docs/stable/clients/cli/overview.md %}) using an install script.

## Linux and macOS

To use the [DuckDB install script](https://install.duckdb.org) on Linux and macOS, run:

```bash
curl https://install.duckdb.org | sh
```

<!-- markdownlint-disable MD040 MD046 -->

<details markdown='1'>
<summary markdown='span'>
Click to see the output of the install script.
</summary>
```text
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  3507  100  3507    0     0  34367      0 --:--:-- --:--:-- --:--:-- 34382
https://install.duckdb.org/v1.4.1/duckdb_cli-osx-universal.gz

*** DuckDB Linux/MacOS installation script, version 1.4.1 ***


         .;odxdl,
       .xXXXXXXXXKc
       0XXXXXXXXXXXd  cooo:
      ,XXXXXXXXXXXXK  OXXXXd
       0XXXXXXXXXXXo  cooo:
       .xXXXXXXXXKc
         .;odxdl,


######################################################################## 100.0%

Successfully installed DuckDB binary to /Users/your_user/.duckdb/cli/1.4.1/duckdb
  with a link from                      /Users/your_user/.duckdb/cli/latest/duckdb

Hint: Append the following line to your shell profile:
export PATH='/Users/your_user/.duckdb/cli/latest':$PATH


To launch DuckDB now, type
/Users/your_user/.duckdb/cli/latest/duckdb
```
</details>

<!-- markdownlint-enable MD040 MD046 -->

By default, this installs the latest stable version of DuckDB to `~/.duckdb/cli/latest/duckdb`.
To add the DuckDB binary to your path, append the following line to your shell profile or RC file (e.g., `~/.bashrc`, `~/.zshrc`):

```bash
export PATH="~/.duckdb/cli/latest":$PATH
```

You can install [past DuckDB releases]({% link release_calendar.md %}#past-releases) (all the way back to v1.0.0) using the `DUCKDB_VERSION` variable. For example, to install v1.2.2, run:

```bash
curl https://install.duckdb.org | DUCKDB_VERSION=1.2.2 sh
```

## Windows

The DuckDB install script is currently not available for Windows.
