---
layout: docu
redirect_from:
- /docs/stable/extensions/python_packages
- /docs/current/extensions/python_packages
- /docs/preview/extensions/python_packages
title: Extensions as Python Packages
---

The DuckDB command line client and every core extension are available as Python packages on [PyPI](https://pypi.org/project/duckdb-cli/). Installing an extension this way puts its binary into the Python environment, so DuckDB loads it without downloading from the extension repository. This serves environments without network access, environments behind a mirror that proxies only PyPI, and projects that pin their dependencies in a lockfile.

## Installing the CLI and Extensions with pip

The package `duckdb-cli` installs the `duckdb` command. Each core extension is a package `duckdb-core-ext-⟨name⟩`{:.language-sql .highlight}, and `duckdb-cli` declares one extra per extension, so an extension is one more name in the install command:

```bash
pip install "duckdb-cli[httpfs,spatial]==2.0.0"
duckdb -c "LOAD httpfs; LOAD spatial;"
```

The extension packages carry the DuckDB version they are built for, and the extras pin them to the same version as the CLI. An extension built for one DuckDB version does not load in another, so keep the versions equal when you install packages one by one:

```bash
pip install "duckdb-cli==2.0.0" "duckdb-core-ext-httpfs==2.0.0"
```

The extras use the extension names, with a few aliases: `s3`, `http` and `https` install `httpfs`; `postgres`, `mysql` and `sqlite` install the scanner of that name; `md` installs `motherduck`. The extensions compiled into the CLI (`autocomplete`, `core_functions`, `icu`, `json`, `parquet`) have no package. The [status page](https://duckdb.github.io/duckdb-python-extensions/) lists which extension packages exist for which DuckDB version and platform.

Both the CLI and the extension wheels are tagged `py3-none-⟨platform⟩`{:.language-sql .highlight}: they contain no Python code that depends on the interpreter version, and pip picks the wheel for the operating system and architecture it runs on. Wheels exist for Linux on x86-64 and arm64 (glibc and musl), macOS on x86-64 and arm64, and Windows on x86-64 and arm64.

## What the Packages Install

An extension package installs its binary at

```text
site-packages/.duckdb_extensions/v⟨DuckDB version⟩/⟨platform⟩/⟨name⟩.duckdb_extension
```

This is the layout DuckDB uses for its own extension directory, by default `~/.duckdb/extensions`. The `duckdb` command from `duckdb-cli` adds `site-packages/.duckdb_extensions` to the [`extension_directories`]({% link docs/2.0/extensions/installing_extensions.md %}#installation-location) setting when that directory exists, after the directories DuckDB already searches. `LOAD` searches every listed directory, so `LOAD httpfs` finds the pip-installed file and loads it without a download.

Each package also installs a small Python module, `duckdb_core_ext_⟨name⟩`{:.language-sql .highlight}, with two functions: `get_extensions_dir()` returns the `.duckdb_extensions` directory, and `get_extension_load_path()` returns the path of the binary.

## Limitations

* DuckDB's automatic installation of a missing extension checks only the first directory of `extension_directories` before downloading. A query that needs an extension that was not loaded with `LOAD` may therefore download it again into `~/.duckdb/extensions`, and without network access that automatic load fails. An explicit `LOAD` always works. This changes once DuckDB treats an extension present in any configured directory as installed.
* The `duckdb` Python module does not search `site-packages/.duckdb_extensions` yet. In Python, pass the directory yourself:

  ```python
  import duckdb
  import duckdb_core_ext_httpfs

  con = duckdb.connect(config={"extension_directories": [duckdb_core_ext_httpfs.get_extensions_dir()]})
  con.execute("LOAD httpfs")
  ```

* Nothing in a wheel tells pip which DuckDB the user runs. A wheel installed for another DuckDB version than the one in use is not found by `LOAD`, or refused.

## Signatures

A wheel changes nothing about DuckDB's signature check: DuckDB loads an extension from the pip directory under the same rules as from anywhere else. An extension signed with a core key, which is every binary on extensions.duckdb.org, loads as is. A [community extension]({% link docs/2.0/extensions/community_extensions.md %}) loads when the install information file described below is beside it. An extension that nobody signed, for example one you built yourself and did not submit to the community repository, loads only when the user allows unsigned extensions, with `duckdb -unsigned` or `SET allow_unsigned_extensions = true`; the package installs either way, the engine refuses the load. See [Extension Signing]({% link docs/2.0/extensions/extension_distribution.md %}#extensions-signing).

## Packaging Your Own Extension

The tool that builds the core extension packages is published as [`duckdb-extension-wheel`](https://pypi.org/project/duckdb-extension-wheel/) for any extension author. It reads the platform, the DuckDB version and the ABI type from the extension binary's metadata footer and takes from you what the binary cannot say: the project name, the wheel version, and the dependencies.

```bash
pip install duckdb-extension-wheel
duckdb-extension-wheel build --name acme-duckdb-geo --version 0.3.1 \
    --requires "duckdb-cli==2.0.0" \
    build/release/extension/geo/geo.duckdb_extension
duckdb-extension-wheel check dist/acme_duckdb_geo-0.3.1-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
```

`build` writes one wheel per binary you pass, so run it with the binaries of every platform you build for, or once per platform in your CI. Versioning and dependencies are yours: the wheel version is any version you choose, and a dependency on `duckdb-cli` is optional. `check` installs a wheel into a fresh virtual environment, downloads the DuckDB command line of the binary's version, and loads the extension from the environment's directory; run it on each platform.

Two things the tool needs to know for some binaries:

* A [community extension]({% link docs/2.0/extensions/community_extensions.md %}), or any extension not signed with a core key, needs the install information file DuckDB writes beside an installed extension, `⟨name⟩.duckdb_extension.info`{:.language-sql .highlight}: DuckDB 2.0 reads it to decide which signing keys to trust. Install the extension once per platform with `INSTALL ⟨name⟩ FROM community` and copy the file from `~/.duckdb/extensions/v⟨version⟩/⟨platform⟩/` next to the binary, where the tool picks it up, or name it with `--info`. A binary signed with a core key needs none; say `--core-extension`.
* An extension built against the stable C API carries no DuckDB version in its footer; give it with `--duckdb-version`. Such a wheel still holds one DuckDB version, since the binary lands in that version's directory.

The full contract a wheel follows, with everything the tool decides and everything it leaves to you, is the [protocol document](https://github.com/duckdb/duckdb-python-extensions/blob/main/PROTOCOL.md) in the repository that publishes the core extension packages. DuckDB before 1.5.0 has no `extension_directories` setting, so the tool refuses binaries built for older versions.
