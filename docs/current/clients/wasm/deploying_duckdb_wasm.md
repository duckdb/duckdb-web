---
layout: docu
redirect_from:
- /docs/preview/clients/wasm/deploying_duckdb_wasm
- /docs/stable/clients/wasm/deploying_duckdb_wasm
title: Deploy DuckDB-Wasm
---

## Overview

Deploying DuckDB-Wasm means serving its components so that the browser can fetch and instantiate them. This page describes each component a deployment needs to serve, how the worker and WebAssembly variants relate, how extensions are served and mirrored, and the security considerations involved.

A DuckDB-Wasm deployment needs to access the following components:

* the DuckDB-Wasm main library component, distributed as TypeScript and compiled to JavaScript code
* the DuckDB-Wasm Worker component, compiled to JavaScript code, possibly instantiated multiple times for threaded environments
* the DuckDB-Wasm module, compiled as a WebAssembly file and instantiated by the browser
* any relevant DuckDB-Wasm extension

## Main Library Component

This is distributed as either TypeScript code or CommonJS JavaScript code in the `npm` duckdb-wasm package, and can be either bundled together with a given application, served in a same origin (sub-)domain and included at runtime or served from a third party CDN like jsDelivr.
This does need some form of transpilation and can't be served as-is, given it needs to know the location of the follow up files for this to be functional.
Details will depend on your given setup, examples can be found at <https://github.com/duckdb/duckdb-wasm/tree/main/examples>.
An example deployment is <https://shell.duckdb.org>, which transpiles the main library component together with shell code (first approach). Or the `bare-browser` example at <https://github.com/duckdb/duckdb-wasm/tree/main/examples/bare-browser>.

## JS Worker Component

This is distributed as a JavaScript file in three different flavors, `mvp`, `eh` and `coi`, and needs to be served as-is. The main library component needs to be informed of the actual location.

The three variants target three different WebAssembly feature sets:

* `mvp` targets the WebAssembly 1.0 (MVP) spec
* `eh` targets WebAssembly with Wasm-level exception handling added, which improves performance
* `coi` targets WebAssembly with exception handling and threading, which enables parallel query execution; it requires the deployment to be cross-origin isolated (see [Cross-Origin Isolation](#cross-origin-isolation))

You can serve all three and let the library feature-detect the best one with `selectBundle`, or serve a single variant and instruct the DuckDB-Wasm library on which one to use. The served artifacts are named after the flavor, for example `duckdb-browser-coi.worker.js`. The `coi` flavor corresponds to the `wasm_threads` extension platform.

## Wasm Worker Component

Same as the JS Worker component, three different flavors, `mvp`, `eh` and `coi` (for example `duckdb-coi.wasm`), each one is needed by the relevant JS component. These WebAssembly modules need to be served as-is at an arbitrary [sub-]domain that is reachable from the main one.

## DuckDB Extensions

DuckDB extensions for DuckDB-Wasm, similar for the native cases, are served signed at the default extension endpoint: `https://extensions.duckdb.org`.
If you are deploying duckdb-wasm you can consider mirroring relevant extensions at a different endpoint, possibly allowing for air-tight deployments on internal networks.

```sql
SET custom_extension_repository = '⟨https://some.endpoint.org/path/to/repository⟩';
```

Changes the default extension repository from the public `https://extensions.duckdb.org` to the one specified. Note that extensions are still signed, so the best path is downloading and serving the extensions with a similar structure to the original repository. See our additional notes on [Creating a Custom Repository]({% link docs/current/extensions/extension_distribution.md %}#creating-a-custom-repository).

Community extensions are served at <https://community-extensions.duckdb.org>, and they are signed with a different key, so they can be disabled with a one way SQL statement such as:

```sql
SET allow_community_extensions = false;
```

This will allow loading **only** of core duckdb extensions. Note that the failure is at `LOAD` time, not at `INSTALL` time.

Please review the [Extension Distribution page]({% link docs/current/extensions/extension_distribution.md %}) for general information about extensions.

## Cross-Origin Isolation

The `coi` bundle runs multiple threads, which relies on `SharedArrayBuffer`. Browsers only expose `SharedArrayBuffer` to pages that are [cross-origin isolated](https://web.dev/articles/coop-coep). To serve the threaded bundle, the top-level document must be delivered with the following HTTP headers:

```text
Cross-Origin-Embedder-Policy: require-corp
Cross-Origin-Opener-Policy: same-origin
```

These headers isolate the document from other cross-origin documents and require any cross-origin resource it embeds to explicitly opt in. Because many third-party endpoints do not yet send the headers needed to be embedded under these policies, most deployments run on non-isolated pages, where DuckDB-Wasm falls back to the single-threaded `mvp` or `eh` bundle.

## Security Considerations

> Warning Deploying DuckDB-Wasm with access to your own data means whoever has access to SQL can access the data that DuckDB-Wasm can access. Also, DuckDB-Wasm in the default setting can access remote endpoints, so it can have a visible effect on the external world even from within the sandbox.

## Further Reading

* [Instantiate DuckDB-Wasm]({% link docs/current/clients/wasm/instantiation.md %}) — how the library, worker, and WebAssembly components served here are wired together at runtime.
* [Load Extensions]({% link docs/current/clients/wasm/extensions.md %}) — how extensions are fetched, signed, and served from a custom repository.
* [Extension Distribution]({% link docs/current/extensions/extension_distribution.md %}) — general information about extension repositories and creating a custom one.
* [DuckDB Wasm Client]({% link docs/current/clients/wasm/overview.md %}) — the layered API and example deployments this page builds on.
