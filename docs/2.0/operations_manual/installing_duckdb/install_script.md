---
layout: docu
redirect_from:
- /docs/stable/operations_manual/installing_duckdb/install_script
- /docs/current/operations_manual/installing_duckdb/install_script
- /docs/lts/operations_manual/installing_duckdb/install_script
- /docs/preview/operations_manual/installing_duckdb/install_script
title: Install Script
---

You can install the [DuckDB CLI client]({% link docs/2.0/clients/cli/overview.md %}) using an install script.

## Linux and macOS

To use the [DuckDB install script](https://install.duckdb.org) on Linux and macOS, run:

```bash
curl https://install.duckdb.org | bash
```

<!-- markdownlint-disable MD040 MD046 -->

<details markdown='1'>
<summary markdown='span'>
Click to see the output of the install script.
</summary>
```text
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 13209  100 13209    0     0   126k      0 --:--:-- --:--:-- --:--:--  127k

*** DuckDB Linux/MacOS installation script, version 2.0.0 ***


         .;odxdl,
       .xXXXXXXXXKc
       0XXXXXXXXXXXd  cooo:
      ,XXXXXXXXXXXXK  OXXXXd
       0XXXXXXXXXXXo  cooo:
       .xXXXXXXXXKc
         .;odxdl,


######################################################################## 100.0%

Successfully installed DuckDB 2.0.0 to /Users/your_user/.duckdb/cli/2.0.0/duckdb
Updated symlink from /Users/your_user/.duckdb/cli/latest/duckdb to
                     /Users/your_user/.duckdb/cli/2.0.0/duckdb

Hint: Append the following line to your shell profile:
export PATH="/Users/your_user/.duckdb/cli/latest":$PATH

To launch DuckDB 2.0.0 now, type
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
curl https://install.duckdb.org | DUCKDB_VERSION=1.2.2 bash
```

### Installing the C/C++ Libraries

Starting with DuckDB 2.0, the install script can also install the DuckDB C/C++ headers and libraries using the `DUCKDB_INSTALL` variable. It takes a comma-separated list of components: `cli` (default), `static`, and `shared`. For example, to install the static library and the CLI, run:

```bash
curl https://install.duckdb.org | DUCKDB_INSTALL=static,cli bash
```

The libraries and headers are installed to `~/.duckdb/lib/⟨version⟩/release_⟨platform⟩`, e.g., `~/.duckdb/lib/2.0.0/release_osx_arm64`. For more details, see [Linking Extensions]({% link docs/2.0/dev/building/linking_extensions.md %}).

## Windows

On Windows, we provide a beta install script. To use it, run the following command from the Run menu (Win+R) or the Command Prompt:

```bash
powershell -NoExit -ExecutionPolicy Bypass -Command "irm https://install.duckdb.org/install.ps1 | iex"
```
