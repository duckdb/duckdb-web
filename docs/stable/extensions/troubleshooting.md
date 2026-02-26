---
layout: docu
redirect_from:
- /docs/extensions/troubleshooting
title: Troubleshooting of Extensions
---

You might be visiting this page directed via a DuckDB error message, similar to:

```sql
INSTALL non_existing;
```

```console
HTTP Error:
Failed to download extension "non_existing" at URL "http://extensions.duckdb.org/v1.4.0/osx_arm64/non_existing.duckdb_extension.gz" (HTTP 404)

Candidate extensions: "inet", "encodings", "core_functions", "sqlite_scanner", "postgres_scanner"
For more info, visit https://duckdb.org/docs/stable/extensions/troubleshooting?version=v1.4.0&platform=osx_arm64&extension=non_existing
```

There are multiple scenarios for which an extension might not be available in a given extension repository at a given time:
* the extension has not been uploaded yet, here some delay after a given release date might be expected. Consider checking the issues at [`duckdb/duckdb`](https://github.com/duckdb/duckdb) or [`duckdb/community-extensions`](https://github.com/duckdb/community-extensions), or creating one yourself.
* the extension is available, but in a different repository, try for example `INSTALL ⟨name⟩ FROM core;`{:.language-sql .highlight} or `INSTALL ⟨name⟩ FROM community;`{:.language-sql .highlight} or `INSTALL ⟨name⟩ FROM core_nightly;`{:.language-sql .highlight} (see the [Installing Extensions page]({% link docs/stable/extensions/installing_extensions.md %}#extension-repositories)).
* networking issues, so extension exists at the endpoint but it's not reachable from your local DuckDB. Here you can try visiting the given URL via a browser directly pasting the link from the error message in the search bar.

If you are on a development version of DuckDB, that is any version for which `PRAGMA version` returns a `library_version` not starting with a `v`, then extensions might not be available anymore on the default extension repository.

When in doubt, consider raising an issue in [`duckdb/duckdb`](https://github.com/duckdb/duckdb).

## Manual Process to Download Extensions via the Browser

To check if an extension is available, consider trying to download the relevant extension resource, for example via your browser visiting <https://extensions.duckdb.org/v1.4.4/osx_arm64/spatial.duckdb_extension.gz> or any other link that has been provided. Note that `http://` has been deprecated in favor of `https://`.

If successful, this will download and unpack the extension to the default `Downloads` folder, so that from SQL you can run:

```sql
INSTALL '~/Downloads/spatial.duckdb_extension';
-- or
FORCE INSTALL '~/Downloads/spatial.duckdb_extension';
```

and after this command the extension will be regularly installed.
