---
layout: docu
redirect_from:
- /docs/preview/clients/wasm/deploying_duckdb_wasm
- /docs/stable/clients/wasm/deploying_duckdb_wasm
title: Deploy
---

## Overview

Deploying DuckDB-Wasm means serving its components so that the browser can fetch and instantiate them. This page describes each component a deployment needs to serve, how the worker and WebAssembly variants relate, how extensions are served and mirrored, and the security considerations involved.

A DuckDB-Wasm deployment needs to access the following components:

* **Main Library Component.** Distributed as TypeScript and compiled to JavaScript code. [For further details, see below.](#main-library-component)
* **JS Worker Component.** Compiled to JavaScript code, possibly instantiated multiple times for threaded environments. [For further details, see below.](#js-worker-component)
* **Wasm Worker Component.** Compiled as a WebAssembly file and instantiated by the browser. [For further details, see below.](#wasm-worker-component)
* **DuckDB Extensions.** Any relevant extensions the deployment loads. [For further details, see below.](#duckdb-extensions)

## Main Library Component

This component is distributed as TypeScript or CommonJS JavaScript in the npm [`@duckdb/duckdb-wasm`](https://www.npmjs.com/package/@duckdb/duckdb-wasm) package. You can deploy it in one of three ways:

* Bundled together with your application
* Served from a same-origin (sub-)domain and included at runtime
* Served from a third-party CDN such as jsDelivr

It cannot be served as-is: it requires transpilation, because it needs to know the location of the follow-up files — the worker and WebAssembly components — in order to work. The exact steps depend on your setup; see the [examples in the repository](https://github.com/duckdb/duckdb-wasm/tree/main/examples). For instance, the [shell.duckdb.org](https://shell.duckdb.org) deployment transpiles the main library together with the shell code (the first approach above), while the [`bare-browser` example](https://github.com/duckdb/duckdb-wasm/tree/main/examples/bare-browser) shows a minimal setup.

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

* [Instantiate]({% link docs/current/clients/wasm/instantiation.md %}) — how the library, worker, and WebAssembly components served here are wired together at runtime.
* [Load Extensions]({% link docs/current/clients/wasm/extensions.md %}) — how extensions are fetched, signed, and served from a custom repository.
* [Extension Distribution]({% link docs/current/extensions/extension_distribution.md %}) — general information about extension repositories and creating a custom one.
* [DuckDB Wasm Client]({% link docs/current/clients/wasm/overview.md %}) — the layered API and example deployments this page builds on.
