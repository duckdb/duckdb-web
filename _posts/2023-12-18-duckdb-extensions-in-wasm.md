---
layout: post
title:  "Extensions for DuckDB-Wasm"
author: Carlo Piovesan
excerpt_separator: <!--more-->
---


_TL;DR: DuckDB-Wasm users can now load DuckDB extensions, allowing them to run extensions in the browser._

In this blog post, we will go over two exciting DuckDB features: the DuckDB-Wasm client and DuckDB extensions. I will discuss how these disjoint features have now been adapted to work together. These features are now available for DuckDB-Wasm users and you can try them out at [shell.duckdb.org](https://shell.duckdb.org).

## DuckDB Extensions

DuckDB’s philosophy is to have a lean core system to ensure robustness and portability.
However, a competing design goal is to be flexible and allow powerful third-party libraries to be used to transform and process data within the database.
In this regard, DuckDB was inspired by [SQLite](https://www.sqlite.org/)'s extensions:
it has an extension mechanism that allows installing and loading extensions during runtime.

### Running DuckDB Extensions Locally

For DuckDB, here is a simple end-to-end example, using the [command line interface](/docs/api/cli):

```sql
INSTALL tpch;
LOAD tpch;
CALL dbgen(sf=0.1);
PRAGMA tpch(7);
```

This script first installs the [TPC-H extension](/docs/extensions/tpch) from the official extension repository, which implements the popular TPC-H benchmark. It then loads the TPC-H extension, uses it to populate the database with generated data using the `dbgen` function, then we run [TPC-H query 7](https://github.com/duckdb/duckdb/blob/v0.9.2/extension/tpch/dbgen/queries/q07.sql).

This example demonstrates a case where we install an extension to complement DuckDB with a new feature (the TPC-H data generator), which is not part of the base DuckDB executable. Instead, it is downloaded from the extension repository, then loaded and executed it locally within the framework of DuckDB.

Currently, DuckDB has several extensions that deal with filesystems ([HTTP(S) and AWS S3](/docs/extensions/httpfs), [Azure](/docs/extensions/azure), etc.), file formats ([Parquet](/docs/extensions/parquet), [JSON](/docs/extensions/json), and [Arrow](/docs/extensions/arrow)), database protocols ([sqlite](/docs/extensions/sqlite), [mysql](/docs/extensions/mysql), and [postgresql](/docs/extensions/postgres)), utility functions ([ICU for handling time zones](/docs/extensions/icu) and [FTS for full text search](/docs/extensions/full_text_search)). Extensions can also extend the parser and type system (e.g., the [spatial extension](/docs/extensions/spatial)).

## DuckDB-Wasm

In an effort spearheaded by André Kohn, [DuckDB has been ported to the WebAssembly platform](/2021/10/29/duckdb-wasm.html) in 2021. [WebAssembly](https://webassembly.org/), also known as Wasm, is a W3C standard language developed in recent years. Think of it as a machine-independent binary format that you can execute from within the sandbox of a web browser.

Thanks to DuckDB-Wasm, anyone has access to a DuckDB instance only a browser tab away, with all computation being executed locally within your browser and no data leaving your device. DuckDB-Wasm is a library that can be used in various deployments (e.g., [notebooks that run inside your browser without a server](https://observablehq.com/@cmudig/duckdb)). For simplicity, in this post we will use the Web shell, where SQL statements are entered by the user line by line, with the behavior modeled after the DuckDB [CLI shell](/docs/api/cli/).

## DuckDB Extensions, in DuckDB-Wasm!

DuckDB-Wasm now supports DuckDB extensions.
To demonstrate this, we will again use the [TPC-H data generation example](#running-duckdb-extensions-locally).
To run this script in your browser, [start an online DuckDB shell that runs these commands](https://shell.duckdb.org/#queries=v0,INSTALL-tpch~,LOAD-tpch~,CALL-dbgen(sf%3D1)~,DESCRIBE~,COPY-customer-TO-'customer.parquet'~). The script will generate the TPC-H data set at scale factor 0.1, which corresponds to 100MB in uncompressed CSV format.

Once the script finished, you can keep executing queries, or you could even download the `customer.parquet` file (1MB) using the following commands:

```sql
COPY customer TO 'customer.parquet';
.files download customer.parquet
```

This will first copy the `customer.parquet` to the DuckDB-Wasm file system, then download it via your browser.

In short, your DuckDB instance, which _runs entirely within your browser,_ first installed and loaded the TPC-H extension. It then used the extension logic to generate data and convert it to a Parquet file, that you could then save as a regular file to your local file system.

<img src="/images/wasm-blog-post-shell-tpch.png"
     alt="Wasm shell using the TPC-H extension"
     width="820"
     />

TODO replace

## Key Features

DuckDB-Wasm’s new extension support comes with the following key features:
the DuckDB-Wasm library can be compiled with dynamic extension support.
DuckDB extensions can be compiled to a single WebAssembly module.
If they share the same DuckDB version, the DuckDB-Wasm library and the extension will work together.
Users and developers working with DuckDB-Wasm can now pick and choose the set of extensions they load.
Moreover, the DuckDB-Wasm shell's features are now much closer to the native [CLI functionality](/docs/api/cli).

## Architecture

Let’s dig into how this all works.

<img src="/images/wasm-blog-post-overview.png"
     alt="Overview of the architecture of DuckDB-Wasm"
     width="600"
     />


When you load DuckDB-Wasm in your browser, there are two components that will be set up:
A library that handles interactions with the user or code using DuckDB-Wasm. This component lives in the main thread, and one of its first tasks is to initialize the second component.
A DuckDB engine due to execute queries. This component lives in a Web Worker, and communicates with the main thread component via messages. This component has a JavaScript layer that handles messages but it’s mostly comprised of the original C++ DuckDB logic compiled down as a single WebAssembly file.


What about adding extensions to the mix?

Extensions for DuckDB-Wasm are composed of a single WebAssembly module, that will both encode the logic and data of the extensions, the list of functions that are going to be imported and exported, and custom section encoding metadata that allows to verify the extension.

To make extension loading work, the DuckDB engine component should block, fetch, validate external WebAssembly code, then plug it in, wiring together import and export, and then the system will be connected and set to keep executing as if it were a single codebase that just gained some new functionality.




The central code block for this to be possible are the following:


```c++
EM_ASM(
    {
        const xhr = new XMLHttpRequest();
        xhr.open("GET", UTF8ToString($0), false);
        xhr.responseType = "arraybuffer";
        xhr.send(null);
        var uInt8Array = xhr.response;
        // Check signatures / version compatibility left as an exercise
        WebAssembly.validate(uInt8Array);
        // Here we add the uInt8Array to Emscripten's filesystem,
        // for it to be found by dlopen
        FS.writeFile(UTF8ToString($1), new Uint8Array(uInt8Array));
    },
    filename.c_str(), basename.c_str()
);

auto lib_hdl = dlopen(basename.c_str(), RTLD_NOW | RTLD_LOCAL);
if (!lib_hdl) {
    throw IOException(
      "Extension \"%s\" could not be loaded: %s",
      filename,
      GetDLError()
    );
}
```

Here we rely on two powerful feature of [Emscripten](https://emscripten.org/), the compiler toolchain we are using to compile DuckDB to WebAssembly.

First, `EM_ASM` allows to inline JavaScript code directly in C++ code. It means that during runtime when we get to that block of code, the WebAssembly component will go back to JavaScript land, perform a blocking `XMLHttpRequest` on a URL such as [https://extensions.duckdb.org/.../tpch.duckdb_extension.wasm](https://extensions.duckdb.org/duckdb-wasm/v0.9.2/wasm_eh/tpch.duckdb_extension.wasm),
then validate that what has been just fetched is actually a valid WebAssembly module.

Second, we leverage Emscripten’s [`dlopen` implementation](https://emscripten.org/docs/compiling/Dynamic-Linking.html), which enables compatible WebAssembly modules to be linked together and act as a single composable codebase.


<img src="/images/wasm-blog-post-extensions.png"
     alt="Overview of the architecture of DuckDB-Wasm with extensions"
     width="828"
     />

## Developer Guide

We see two main groups of developers using extensions with DuckDB-Wasm.

* Developers working with DuckDB-Wasm: If you are building a website or a library that wraps DuckDB-Wasm, the new extension support means that there is now a wider range of functionality that can be exposed to your users.
* Developers working on DuckDB extensions: If you have written a DuckDB extension already, or are thinking of doing so, consider porting that also to DuckDB-Wasm. It might be the easiest way to get your extension at the hands of users.

In any case, the [`duckdb/extension-template` repository](https://github.com/duckdb/extension-template) is the place where to start.

## The Spatial Extension

To show the possibilities unlocked by duckdb-wasm extensions, and test the capabilities of what’s possible, what about compiling the spatial extension to duckdb-wasm?
The [spatial extension](/docs/extensions/spatial) implements geospatial types and functions that allow it to work with geospatial data and relevant workloads.

To install and load spatial in DuckDB-Wasm (or in regular DuckDB), as usual what’s required is only:

```sql
INSTALL spatial;
LOAD spatial;
```

And then, for example, the following query should compute some aggregate metrics on the New York taxi dataset: 

```sql
CREATE TABLE nyc AS
    SELECT
        borough,
        st_union_agg(geom) AS full_geom,
        st_area(full_geom) AS area,
        st_centroid(full_geom) AS centroid,
        count(*) AS count FROM
st_read('https://raw.githubusercontent.com/duckdb/duckdb_spatial/main/test/data/nyc_taxi/taxi_zones/taxi_zones.shp')
GROUP BY borough;
SELECT borough, area, centroid::VARCHAR, count
FROM nyc;
```

Both in your local DuckDB client and the [online DuckDB shell](https://shell.duckdb.org/#queries=v0,INSTALL-spatial~,LOAD-spatial~,CREATE-TABLE-nyc-AS-SELECT-borough%2C-st_union_agg(geom)-AS-full_geom%2C-st_area(full_geom)-AS-area%2C-st_centroid(full_geom)-AS-centroid%2C-count(*)-AS-count-FROM-st_read('https%3A%2F%2Fraw.githubusercontent.com%2Fduckdb%2Fduckdb_spatial%2Fmain%2Ftest%2Fdata%2Fnyc_taxi%2Ftaxi_zones%2Ftaxi_zones.shp')-GROUP-BY-borough~,SELECT-borough%2C-area%2C-centroid%3A%3AVARCHAR%2C-count-FROM-nyc~) should produce the same results.

Both will produce the same results.

## Limitations

DuckDB-Wasm extensions have a few inherent limitations. For example, it is not possible to communicate with native executables living on your machine, which is required by (e.g.,) the [`aws`](/docs/extensions/aws) or [`azure`](/docs/extensions/azure) extensions. Moreover, 
compilation to Wasm may not be currently supported for some libraries you are relying on, or capabilities might not be one-to-one with local executables due to additional requirements imposed on the browser, in particular around [non-secure HTTP requests](https://duckdb.org/docs/api/wasm/extensions#httpfs).

## Conclusions

In this blog post, we explained how DuckDB-Wasm supports extensions, and demonstrated with with multiple extensions: [TPC-H](/docs/extensions/tpch), [Parquet](/docs/extensions/parquet), and [spatial](/docs/extensions/spatial).

For updates on the latest developments, follow this blog and join the Wasm channel in [our Discord](https://discord.duckdb.org). If you have an example of what’s possible with extensions in DuckDB, let us know!
