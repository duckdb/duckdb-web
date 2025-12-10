---
layout: post
title: "Iceberg in the Browser"
author: "Carlo Piovesan, Tom Ebergen, Gábor Szárnyas"
thumb: "/images/blog/thumbs/iceberg-in-the-browser.svg"
image: "/images/blog/thumbs/iceberg-in-the-browser.png"
excerpt: "DuckDB is the first complete end-to-end interface to Iceberg REST Catalogs within a browser tab. You can now read and write tables in an Iceberg catalog without needing to manage any infrastructure – directly from a browser!"
tags: ["extension"]
---

In this blog post, we describe the state of Iceberg analytics and introduce a new possibility: interacting with an Iceberg REST Catalog can be as simple as navigating to an URL, no further setup or installs required.

## Interaction Models for Iceberg Catalogs

![Iceberg analytics today](/images/blog/iceberg-wasm/iceberg-analytics-today-dark.svg){: .darkmode-img }
![Iceberg analytics today](/images/blog/iceberg-wasm/iceberg-analytics-today-light.svg){: .lightmode-img }

Iceberg is an Open Table Format, that is to say a database stored as a collection of Parquet files (on object storage), metadata on those files (also static files on object storage) and a REST API to orchestrate data and metadata.

There are two common ways to interact with Iceberg catalogs:
* The *client–server model,* where the compute part of the operation is delegated to a managed infrastructure – such as the cloud. Users can interact with the server by installing a native client or a lightweight client such as a browser.
* The *client-is-the-server model,* where the user first installs the relevant libraries, and then performs queries directly on their machine.

Obviously, both models have tradeoffs. In the client–server model, clients can be lightweight, and the server is the uniform point of access allowing for potential efficiencies thanks to scale. However, the infrastructure introduces additional maintenance requirements. In the client-is-the-server model, latency is lower, users can leverage local compute resources, and integrating with local inputs and external data sources happens at user level. However, requiring users to run computation locally means transferring part of the burden on your users (e.g., setting up dependencies).

The implementation of existing Iceberg engines follow these categories. Iceberg engines can run locally as binaries, or an organization can host them in their server infrastructure.

## Iceberg with DuckDB

![Iceberg with DuckDB](/images/blog/iceberg-wasm/iceberg-with-duckdb-dark.svg){: .darkmode-img }
![Iceberg with DuckDB](/images/blog/iceberg-wasm/iceberg-with-duckdb-light.svg){: .lightmode-img }

DuckDB supports both Iceberg interaction models, as engine run either in the *server* or as locally installable *client-is-the-server*.
From a user point of view, in the *client-server model* engine choice is transparent, while in the *client-is-the-server*, users will [install DuckDB locally](https://duckdb.org/install/) and use it through its SQL interface to query Iceberg Catalogs. For example: 

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

We asked ourselves: what would it take to expose Iceberg analytics, without any required setup for users or maintenance of any managed infrastructure, in a *truly serverless* manner?

![Iceberg with DuckDB-Wasm](/images/blog/duckdb-iceberg-with-duckdb-wasm-dark.svg){: .darkmode-img }
![Iceberg with DuckDB-Wasm](/images/blog/duckdb-iceberg-with-duckdb-wasm-light.svg){: .lightmode-img }

DuckDB has a client that can run in any browser: [DuckDB-Wasm](https://duckdb.org/docs/stable/clients/wasm/overview) is a WebAssembly port of DuckDB, does [supports loading of extensions](https://duckdb.org/2023/12/18/duckdb-extensions-in-wasm) in general, but not yet of the Iceberg one.

What does interacting with an Iceberg REST Catalog require? The ability to talk to a REST API over HTTP(S). The possibility of reading (or writing) `avro` and `parquet` files on object storage. Negotiating authentication to access those resources on behalf of the user. All of the above can be done also from a Browser, no native component is actually needed.

At a high level, the changes required were:
* In the core `duckdb` codebase, we redesigned HTTP interactions, so that extensions and clients have an uniform interface to the networking stack.
* In `duckdb-wasm`, we implemented such an interface, that in this case is a wrapper around the available JavaScript network stack
* In `duckdb-iceberg`, we routed all networking through the common HTTP interface, so that both in native and Wasm the same logic is executed

The result is that you can now query Iceberg with DuckDB running directly on a Browser.

Now you can access the same Iceberg Catalog using *client–server*, *client-as-a-server*, or properly serverless from the isolation of a single tab running on your browser!

## Welcome to Serverless Iceberg Analytics

To see a demo of serverless Iceberg analytics, visit our table visualizer at [`duckdb.org/visualizer`](https://duckdb.org/visualizer/?iceberg).

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
