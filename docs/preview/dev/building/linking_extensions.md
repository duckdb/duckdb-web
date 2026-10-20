---
layout: docu
title: Statically Linking Extensions
---

This page is for client and binding authors, and for anyone who embeds `libduckdb` in their own application.
It describes how statically linking extensions changed in DuckDB v2.0 and what builders on top of DuckDB need to do.

> This change is independent of the new C API. It applies even if you continue to build against the existing (v1) C API: the difference is in how extension archives are linked and registered, not in which API your bindings call.

## What Changed in DuckDB v2.0

> New Link-time static linking of extensions is introduced in DuckDB 2.0.

Before v2.0, the set of statically linked extensions was a _compile-time_ decision.
The sources were compiled with knowledge of which extensions were included, so a build with `CORE_EXTENSIONS='json;parquet;icu'` could not reuse the object files of a build with `CORE_EXTENSIONS='json;parquet;icu;tpch'`, even though one is a subset of the other.

DuckDB v2.0 modularizes this into a _link-time_ decision ([`duckdb#25814`](https://github.com/duckdb/duckdb/pull/25814)).
Each extension is compiled once into its own static archive, for example:

```text
libduckdb_static.a
libcore_functions_extension.a
libparquet_extension.a
libjson_extension.a
libicu_extension.a
```

The list of extensions to link in is now chosen when linking, not when compiling.
As a follow-up, the extension loader and the built-in `httplib` also became opt-in at link time ([`duckdb#26188`](https://github.com/duckdb/duckdb/pull/26188)).

Two aspects that earlier builds relied on are gone:

* The `bundle-library` Makefile target that merged everything into a single `libduckdb_bundle.a`. Extensions, `httplib`, and loadable extensions are now separate archives.
* The generated loader that `libduckdb_static.a` used to register extensions automatically. `libduckdb_static.a` no longer registers extensions on its own.

## Registering Statically Linked Extensions

Because extension selection moved to link time, a client that statically links extensions must now _register_ them with the engine before any database is opened.
Each extension archive carries a generated describe function, `duckdb_extension_⟨name⟩_describe`, that fills a `duckdb_extension_descriptor` declared in the new public header `duckdb_static_extension.h`.
The descriptor carries a layout version, so the engine refuses an archive whose descriptor layout it does not support, with a clear message instead of misbehaving.

The engine exposes a C API call, `duckdb_register_static_extension(describe)`, which validates the descriptor and registers the extension for every database opened afterwards.
A generated loader (`static_extension_loader.c`) defines `duckdb_register_static_extensions()`, which passes every linked extension's describe function to `duckdb_register_static_extension` in turn.
Call it once at startup, before any database is opened, from any language that can call C:

```cpp
// Register the statically linked extensions before any database can be opened
if (duckdb_register_static_extensions() != 0) {
    throw std::runtime_error("Failed to register the statically linked DuckDB extensions");
}
```

If registration is skipped, the linked extensions (such as `core_functions`, `icu`, `json`, and `parquet`) are not loaded.
Queries that depend on them then fail at runtime. For example, `SELECT to_minutes(5)` reports that the function exists in the `core_functions` extension, even though that extension was linked in.

A program can also skip the generated loader and call `duckdb_register_static_extension` directly on the describe functions it declares itself.
An archive whose describe function is never registered contributes nothing, and a registered extension whose archive is missing fails the link.

### Calling the Loader Before `main`

A C++ program that wants registration to happen automatically before `main` compiles `extension/loader/static_extension_autoregister.cpp` alongside the loader.
Compile it into the program itself, not into an archive, or the linker drops it.

If you do package the loader and the auto-register object into an archive, keep the registration symbol from being discarded by forcing it onto the link line:

```bash
-Wl,-u,duckdb_register_static_extensions
```

## Build Options

When building DuckDB or `libduckdb`, select the extensions to compile with `BUILD_EXTENSIONS` (or `CORE_EXTENSIONS`):

```bash
BUILD_EXTENSIONS='core_functions;json;parquet;icu' GEN=ninja make
```

Which of the built extensions are statically linked is a separate decision.
By default the DuckDB targets link the extensions that the build configs mark for static linking, plus the ones named in `BUILD_EXTENSIONS` when you build with `LINK_CORE_EXTENSIONS=1`.
To link an explicit set instead, set `STATICALLY_LINK_EXTENSIONS` (the older name for this flag is `LINK_EXTENSIONS`):

```bash
STATICALLY_LINK_EXTENSIONS='core_functions;parquet;json;icu;tpch' make
```

Changing the linked set only re-generates the loader, compiles it, and re-links; it does not recompile the extensions themselves.
An extension that is built but not statically linked is still available: it is installed from the build's own extension repository and loaded the first time a query needs it.

### Linking the Archives by Hand

Outside CMake, link one archive per extension, compile the generated loader, and put the engine archive last:

```bash
LINK_EXTENSIONS='parquet;json' make static_extension_loader
cc -I src/include main.c build/release/static_extension_loader.c libparquet_extension.a libjson_extension.a libduckdb_static.a -lstdc++
```

The order matters: each extension archive must come before `libduckdb_static.a` on the link line.

See [Build Configuration]({% link docs/preview/dev/building/build_configuration.md %}) and [Building Extensions]({% link docs/preview/dev/building/building_extensions.md %}) for the full set of flags.

## Obtaining Prebuilt Archives

Rather than building `libduckdb` yourself, you can download the static and shared archives for DuckDB v2.0 and later using the [`duckdb-install-scripts`](https://github.com/duckdb/duckdb-install-scripts) tooling ([`duckdb-install-scripts#5`](https://github.com/duckdb/duckdb-install-scripts/pull/5)).
Setting `DUCKDB_INSTALL=static` installs the archives and headers under `~/.duckdb/lib/⟨version⟩/⟨build_type⟩_⟨platform⟩`:

```bash
DUCKDB_INSTALL=static DUCKDB_VERSION=alpha
```

This installs, for example:

```text
duckdb.h                      duckdb_v2.h
duckdb_extension.h            duckdb_extension_v2.h
duckdb_static_extension.h
libduckdb_static.a            libcore_functions_extension.a
libparquet_extension.a        libjson_extension.a
libicu_extension.a            libautocomplete_extension.a
libtpch_extension.a           libtpcds_extension.a
```

A pinned build can be installed with `DUCKDB_STAGED`, for example `DUCKDB_STAGED=31adc8b766/v2.0.0-alpha42839` or simply `DUCKDB_STAGED=31adc8b766`.

> For DuckDB v2.0 and later, most artifacts are distributed as `.tar.gz` files instead of `.zip` files ([`duckdb#24773`](https://github.com/duckdb/duckdb/pull/24773)).

## Reference Implementations for Clients

The following pull requests adapt the official clients to the v2.0 linking model.
They provide a path forward for anyone maintaining a binding or an application that links `libduckdb`.

<div class="monospace_table"></div>

| Client | Status | Reference pull requests |
|---|---|---|
| Python | Migrated | [`duckdb-python#634`](https://github.com/duckdb/duckdb-python/pull/634) |
| Rust | Migrated | [`duckdb-rs#834`](https://github.com/duckdb/duckdb-rs/pull/834), [`duckdb-rs#839`](https://github.com/duckdb/duckdb-rs/pull/839), [`duckdb-rs#883`](https://github.com/duckdb/duckdb-rs/pull/883), [`duckdb-rs#835`](https://github.com/duckdb/duckdb-rs/pull/835) |
| Node.js | Survey in progress | [`duckdb-node-neo#476`](https://github.com/duckdb/duckdb-node-neo/pull/476), [`duckdb-node-neo#508`](https://github.com/duckdb/duckdb-node-neo/pull/508) |
| Go | Planned, not yet started | [`duckdb-go-bindings#112`](https://github.com/duckdb/duckdb-go-bindings/issues/112) |
| Wasm | Not yet migrated | pending (pinned to the DuckDB v1.5 `v1.5-variegata` line at the time of writing) |

> The Python pull request is the clearest end-to-end example: it restores static linking of the default `BUILD_EXTENSIONS` set by calling `duckdb_register_static_extensions()` and shows how to override the linked set.

## See Also

* [Building Extensions]({% link docs/preview/dev/building/building_extensions.md %})
* [Build Configuration]({% link docs/preview/dev/building/build_configuration.md %})
* [C API Overview]({% link docs/preview/clients/c/overview.md %})
* [Extensions Overview]({% link docs/preview/extensions/overview.md %})
