---
github_repository: https://github.com/duckdb/duckdb-wasm
layout: docu
title: Deploying DuckDB Wasm
---

A DuckDB-Wasm deployment needs to access the following components
* the DuckDB-Wasm main library component, distributed as TypeScript and compiled to JavaScript code
* the DuckDB-Wasm Worker component, compiled to JavaScript code, possibly instantiated multiple times for threaded environments
* the DuckDB-Wasm module, compiled as a WebAssembly file and instantiated by the browser
* any relevant DuckDB-Wasm extension


#### Main library component

This is distributed as either TypeScript code or Common-js JavaScript code in the `npm` duckdb-wasm package, and can be either bundled together with a given application, served in a same origin [sub-] domain and included at runtime or served from a third party CDN like JSDelivery.
This do need some form of transpilation, and can't be served as-is, given it needs to know the location of the follow up files for this to be functional.
Details will depend on your given setup, examples can be found at https://github.com/duckdb/duckdb-wasm/tree/main/examples.
Example deployment could be for example https://shell.duckdb.org, that transpile the main library componenent together with shell code (first approach). Or the `bare-browser` example at https://github.com/duckdb/duckdb-wasm/tree/main/examples/bare-browser.


#### JS Worker component

This is distributed as a JavaScript file in 3 different flavors, `mvp`, `eh` and `threads`, and needs to be served as is, and the main library components needs to be informed of the actual location.

There are 3 variants for 3 different `platforms`:
- MVP targets WebAssembly 1.0 spec
- EH targets WebAssembly 1.0 spec WITH Wasm-level exceptions handling added, that improves performances
- THREADS targets WebAssembly spec WITH exception and threading constructs

You could serve all 3, and feature detect, or serve a single variant and instruct duckdb-wasm library on which one to use


#### Wasm worker component

Same as the JS Worker component, 3 different flavors, `mvp`, `eh` and `threads`, each one is needed by the relevant JS component. These WebAssembly modules needs to be served as-is at an arbitrary [sub-] domain that is reachable from the main one.


#### DuckDB extensions

DuckDB extensions for duckdb-wasm, similar for the native cases, are served signed at the default extension endpoint: `https://extensions.duckdb.org`.
If you are deploying duckdb-wasm you can consider mirroring relevant extensions at a different endpoint, possibly allowing for air-tight deployments on internal networks.

```sql
SET custom_extension_repository = '<https://some.endpoint.org/path/to/repository';
```
Changes the default extension repository from the public `https://extensons.duckdb.org` to the one specified. Note that extensions are still signed, so the best path is downloading and serving the extensions with a similar structure to the original repository. See additional notes at https://duckdb.org/docs/stable/extensions/extension_distribution#creating-a-custom-repository.


Community extensions are served at https://community-extensioions.duckdb.org, and they are signed with a different key, so they can be disabled with a one way SQL statement such as:
```sql
SET allow_community_extensions = false;
```
This will allow loading ONLY of core duckdb extensions. Note that the failure is at LOAD time, not at INSTALL time.

Please review https://duckdb.org/docs/stable/extensions/extension_distribution for general information about extensions.


#### Note of caution

Deploying DuckDB-Wasm with access to your own data means whoever has access to SQL can access the data that DuckDB-Wasm can access. Also DuckDB-Wasm in default setting can access to remote endpoints, so have visible effect on external word even from within the sandbox.
