---
layout: post
title: "Iceberg in the Browser"
author: "Carlo Piovesan, Tom Ebergen, Gábor Szárnyas"
thumb: "/images/blog/thumbs/iceberg-in-the-browser.svg"
image: "/images/blog/thumbs/iceberg-in-the-browser.png"
excerpt: "DuckDB is the first complete end-to-end interface to Iceberg REST Catalogs within a browser tab. You can now read and write tables in an Iceberg catalog without needing to manage any infrastructure – directly from a browser!"
tags: ["extension"]
---

In this blog post, we describe the state of Iceberg analytics and introduce a new possibility: interacting with an Iceberg REST Catalog can be as simple as navigating to a URL, no further setup or installs required.

## Interaction Models for Iceberg catalogs

![Iceberg analytics today](/images/blog/iceberg-wasm/iceberg-analytics-today-dark.svg){: .darkmode-img }
![Iceberg analytics today](/images/blog/iceberg-wasm/iceberg-analytics-today-light.svg){: .lightmode-img }

Iceberg is an _Open Table Format,_ which allows you to capture a mutable database table as static files on object storage such as AWS S3.
Iceberg catalogs allow you to track and organize Iceberg tables.
For example, Iceberg REST Catalogs provide these functionalities through a REST API.

There are two common ways to interact with Iceberg catalogs:

* The *client–server model,* where the compute part of the operation is delegated to a managed infrastructure – such as the cloud. Users can interact with the server by installing a native client or a lightweight client such as a browser.
* The *client-is-the-server model,* where the user first installs the relevant libraries, and then performs queries directly on their machine.

Both models have their tradeoffs. In the *client–server model,* clients can be lightweight, and the server is the uniform point of access allowing for potential efficiencies thanks to scale. However, the infrastructure introduces additional maintenance requirements. In the *client-is-the-server model,* latency is lower, users can leverage local compute resources, and integrate with local inputs and external data sources happens at the user's level. However, requiring users to run computation locally means transferring part of the burden on your users (e.g., setting up dependencies).

The implementation of existing Iceberg engines fall into these categories. Iceberg engines can run locally as binaries, or an organization can host them in their server infrastructure.

## Iceberg with DuckDB

![Iceberg with DuckDB](/images/blog/iceberg-wasm/iceberg-with-duckdb-dark.svg){: .darkmode-img }
![Iceberg with DuckDB](/images/blog/iceberg-wasm/iceberg-with-duckdb-light.svg){: .lightmode-img }

DuckDB supports both Iceberg interaction models, as the engine can run either in the *server* or as locally installable binary.
From a user's point of view, in the *client-server model*, the engine choice is transparent, while in the *client-is-the-server*, users will [install DuckDB locally]({% link install/index.html %}) and use it through its SQL interface to query Iceberg catalogs. For example: 

```sql
CREATE SECRET test_secret (
    TYPE S3, 
    KEY_ID '⟨...⟩', 
    SECRET '⟨...⟩'
);
ATTACH '⟨warehouse⟩' AS db (
    TYPE iceberg,
    ENDPOINT_URL '⟨https://your-iceberg-endpoint⟩',
);
SELECT sum(value) FROM db.table WHERE other_column = '⟨some_value⟩';
```

> You can discover the full DuckDB-Iceberg extension feature set, including insert and update capabilities, in our [earlier blog post]({% post_url 2025-11-28-iceberg-writes-in-duckdb %}).

## Iceberg with DuckDB in the Browser

We asked ourselves: would it be possible to run the *client-is-the-server* model directly from within a browser tab?
In other terms, would a zero-setup, no-infrastructure, properly serverless option viable for interacting with Iceberg catalogs?

![Iceberg with DuckDB-Wasm](/images/blog/iceberg-wasm/duckdb-iceberg-with-duckdb-wasm-dark.svg){: .darkmode-img }
![Iceberg with DuckDB-Wasm](/images/blog/iceberg-wasm/duckdb-iceberg-with-duckdb-wasm-light.svg){: .lightmode-img }

Luckily, DuckDB has a client that can run in any browser! [DuckDB-Wasm]({% link docs/stable/clients/wasm/overview.md %}) is a WebAssembly port of DuckDB, which [supports loading of extensions]({% post_url 2023-12-18-duckdb-extensions-in-wasm %}).

What does interacting with an Iceberg REST Catalog require? The ability to talk to a REST API over HTTP(S). The possibility of reading (or writing) `avro` and `parquet` files on object storage. Negotiating authentication to access those resources on behalf of the user. All of the above can be done also from a Browser, no native component is actually needed.

At a high level, the changes required were the following.

* In the core `duckdb` codebase, we redesigned HTTP interactions, so that extensions and clients have a uniform interface to the networking stack.
* In `duckdb-wasm`, we implemented such an interface, which in this case is a wrapper around the available JavaScript network stack.
* In `duckdb-iceberg`, we routed all networking through the common HTTP interface, so that both in native and Wasm the same logic is executed.

**The result is that you can now query Iceberg with DuckDB running directly in a browser!** Now you can access the same Iceberg catalog using *client–server*, *client-as-a-server*, or properly serverless from the isolation of a browser tab!

## Welcome to Serverless Iceberg Analytics

To see a demo of serverless Iceberg analytics, visit our table visualizer at [`duckdb.org/visualizer`]({% link visualizer/index.html %}?iceberg).

TODO - final URL and video

## Access Your Own Data

As of today, this demo works with [Amazon S3 Tables]({% link docs/stable/core_extensions/iceberg/amazon_s3_tables.md %}). This has been implemented through a collaboration with the Amazon S3 Tables team.

You can now provide your own Iceberg warehouse and a set of credentials that allows reads from the catalog, metadata and data (policy [`AmazonS3TablesReadOnlyAccess`](https://us-east-1.console.aws.amazon.com/iam/home?region=us-east-2#/policies/details/arn%3Aaws%3Aiam%3A%3Aaws%3Apolicy%2FAmazonS3TablesReadOnlyAccess)).
Computations are fully local, and the credentials and warehouse ID are only sent to the catalog endpoint specified in your `Attach` command.
Inputs are translated to SQL, and added to the hash segment of the URL.

What this means:

* no sensitive data is handled or sent to `duckdb.org`
* computations are local, fully in your browser
* interface is SQL, same snippet can be run everywhere DuckDB runs
* if you share the link, you might be sharing your credentials

## Conclusion

DuckDB-Iceberg extension is now supported in DuckDB-Wasm for Iceberg REST Catalogs. At the moment only one major implementation works out of the box, more hopefully to follow.

Iceberg in DuckDB-Wasm will allow users another path to access Iceberg catalogs in their browsers, no extra infrastructure or complexities to be maintained.

This will allow users to unlock the analytical powers of DuckDB on their Iceberg catalogs without having to install or manage any compute nodes, making Iceberg tables even simpler to access. If you would like to provide feedback or file issues, please reach out to us on either the [DuckDB-Wasm](https://github.com/duckdb/duckdb-wasm) or [DuckDB-Iceberg](https://github.com/duckdb/duckdb-iceberg) repository. If you are interested in using any part of this within your organization, feel free to [reach out](https://duckdblabs.com/contact/).
