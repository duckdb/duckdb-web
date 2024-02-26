---
layout: docu
title: Versioning of Extensions
---

## Extension versions
> An extension can have in-version upgrades.
> You can run `FORCE INSTALL <extension>` to ensure you're on the latest version of the extension.

DuckDB extensions currently don't have an internal version. This means that, in general, when staying on a DuckDB version, the version of the extension will be fixed. When a new version of DuckDB is released, this also marks a new release for all extension versions. However, there are 2 important sidenotes to make here:

Firstly, some DuckDB extension's may be updated within a DuckDB release in case of bugs. These are considered "hotfixes" and should not introduce compatibility breaking changes. This means that when running into issues with an extension, it makes sense to double-check that you are on the latest version of an extension by running `FORCE INSTALL <extension>`. 

Secondly, in the (near) future DuckDB aims to untie extension versions from DuckDB versions by adding version tags to extensions, the ability to inspect which versions are installed, and installing specific extension versions. So keep in mind that this is likely to change and in the future extension may introduce compatibility-breaking updates within a DuckDB release.   


## Target DuckDB version
Currently, when extensions are compiled, they are tied to a specific version of DuckDB. What this means is that an extension binary compiled for v0.9.2 does not work for v0.10.0 for example. In most cases, this will not cause any issues and is fully transparent; DuckDB will automatically ensure it installs the correct binary for its version. For extension developers, this means that they must ensure that new binaries are created whenever a new version of DuckDB is released. However, note that DuckDB provides an [extension-template](https://github.com/duckdb/extension-template) that makes this fairly simple.