---
layout: docu
redirect_from:
- /docs/clients/go/known_issues
- /docs/stable/clients/go/known_issues
- /docs/current/clients/go/troubleshoot
- /docs/lts/clients/go/troubleshoot
- /docs/preview/clients/go/troubleshoot
- /docs/stable/clients/go/troubleshoot
title: Troubleshoot
---

## Overview

This page collects common issues encountered when using the DuckDB Go client, together with their workarounds. Because the client uses [cgo](https://pkg.go.dev/cmd/cgo) to embed DuckDB, most build problems are cgo or linker problems. If you run into a problem that is not covered here, search the [client's issue tracker](https://github.com/duckdb/duckdb-go/issues) on GitHub.

## Classifying DuckDB Errors

The client returns a `*duckdb.Error` for errors reported by DuckDB. Use [`errors.As`](https://pkg.go.dev/errors#As) to handle these errors by category without parsing their messages:

```go
_, err := db.Exec(query)
if err != nil {
    var duckdbError *duckdb.Error
    if errors.As(err, &duckdbError) {
        switch duckdbError.Type {
        case duckdb.ErrorTypeCatalog:
            // Handle a missing table, view, or other catalog entry.
        case duckdb.ErrorTypeConstraint:
            // Handle a constraint violation.
        }
    }
}
```

`duckdb.Error.Type` is a `duckdb.ErrorType`. Other categories include `ErrorTypeBinder`, `ErrorTypeParser`, `ErrorTypeConversion`, `ErrorTypeIO`, `ErrorTypeOutOfRange`, and `ErrorTypeInvalidInput`. The `Msg` field contains the error message.

## `undefined: conn` and Other cgo Errors

An `undefined: conn` error while building means the Go compiler has decided cgo is unavailable, so the DuckDB bindings were not compiled. There are two common causes:

* **Build tools are missing.** cgo needs a C compiler and toolchain. On Debian or Ubuntu, install them with:

    ```bash
    sudo apt-get update && sudo apt-get install build-essential
    ```

* **Cross-compiling disables cgo.** The Go compiler turns cgo off automatically when cross-compiling. Re-enable it and point at the right cross-compiler:

    ```bash
    CC=⟨c_cross_compiler⟩ CGO_ENABLED=1 go build
    ```

## Windows Setup

On Windows you need a compatible version of `gcc` and the necessary runtime libraries. One way is [MSYS2](https://www.msys2.org/): install it, then open an MSYS2 shell and install the UCRT64 toolchain:

```bash
pacman -S mingw-w64-ucrt-x86_64-gcc
```

Add `gcc` to the path, for example in PowerShell:

```text
$env:PATH = "C:\msys64\ucrt64\bin;$env:PATH"
```

The package then compiles on Windows.

## Linking DuckDB

By default the client statically links a pre-built DuckDB library into the binary, which increases the binary size but requires no separate DuckDB installation. Pre-built libraries ship for macOS (amd64, arm64), Linux (amd64, arm64), and Windows (amd64). If none of the pre-built libraries fit, link a custom library instead.

### Linking a Custom Static Library

Build DuckDB from source. Starting with DuckDB 2.0, the `bundle-library` Makefile target and the merged `libduckdb_bundle.a` archive no longer exist: the build produces `libduckdb_static.a` plus one static archive per extension (e.g., `libparquet_extension.a`), and statically linked extensions have to be registered at startup. See [Statically Linking Extensions]({% link docs/2.0/dev/building/linking_extensions.md %}) for the archives, the required link order, and the extension registration.

Then build the Go module against these archives with the `duckdb_use_static_lib` [build tag]({% link docs/2.0/clients/go/overview.md %}#build-tags), passing the archives in `CGO_LDFLAGS`, with the extension archives listed before `libduckdb_static.a`.

This is also how a local DuckDB checkout is validated from the Go client, and how the client's own `Makefile` and CI build. It is required to target platforms without a pre-built library, including FreeBSD, for which DuckDB publishes no bundled library.

### Linking a Dynamic Library

Alternatively, link dynamically against a `libduckdb` shared library on the system with the `duckdb_use_lib` build tag. Download the shared library (`.so` on Linux, `.dylib` on macOS) from the DuckDB [releases page](https://github.com/duckdb/duckdb/releases), then build and run with the library on the loader path:

```bash
# On Linux.
CGO_ENABLED=1 CGO_LDFLAGS="-lduckdb -L/path/to/libs" go build -tags=duckdb_use_lib main.go
LD_LIBRARY_PATH=/path/to/libs ./main

# On macOS.
CGO_ENABLED=1 CGO_LDFLAGS="-lduckdb -L/path/to/libs" go build -tags=duckdb_use_lib main.go
DYLD_LIBRARY_PATH=/path/to/libs ./main
```

## `TIMESTAMP` versus `TIMESTAMP_TZ`

In the C API, DuckDB stores both `TIMESTAMP` and `TIMESTAMP_TZ` as the same instant, a number of microseconds since 1970-01-01 UTC, without offset information. When a `time.Time` is passed to the client, it is converted to that instant with `UnixMicro()`, even for `TIMESTAMP_TZ`, and scanning either type back returns an instant, because SQL types do not model a per-value time zone.

A bare `time.Time` binds as `TIMESTAMP_TZ` by default. When a different timestamp type is required, for example binding against a `TIMESTAMP_NS` column, force the type with `duckdb.Typed()`:

```go
row := db.QueryRow(query,
    duckdb.Typed(start, duckdb.TYPE_TIMESTAMP_NS),
    duckdb.Typed(end, duckdb.TYPE_TIMESTAMP_NS),
)
```

See [Run Queries]({% link docs/2.0/clients/go/querying.md %}#forcing-a-parameter-type) for the full example.

## Scanning JSON Values

Starting with v2, scanning a [`JSON`]({% link docs/2.0/data/json/overview.md %}) value directly into a `string` or `[]byte` is no longer supported. Scan into `any` or into the `duckdb.Composite` wrapper instead, as shown in [Run Queries]({% link docs/2.0/clients/go/querying.md %}#reading-nested-and-composite-types). If a plain string or byte result is needed and the JSON structure is not, cast the column to `::VARCHAR` or `::BLOB` in SQL before scanning.

## Further Reading

* [Go Client]({% link docs/2.0/clients/go/overview.md %}) — installation, build tags, and the bundled extensions.
* [Connect]({% link docs/2.0/clients/go/connecting.md %}) — opening databases and the connection lifetime, whose failures are often build or linking problems.
* [Run Queries]({% link docs/2.0/clients/go/querying.md %}) — parameter binding, including the `duckdb.Typed()` hint and JSON scanning.
