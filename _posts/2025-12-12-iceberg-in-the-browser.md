---
layout: post
title: "Iceberg in the Browser"
author: "Carlo Piovesan, Tom Ebergen, Gábor Szárnyas"
thumb: "/images/blog/thumbs/iceberg-in-the-browser.svg"
image: "/images/blog/thumbs/iceberg-in-the-browser.png"
excerpt: "DuckDB is the first end-to-end interface to Iceberg REST Catalogs within a browser tab. You can now read and write tables in Iceberg catalogs without needing to manage any infrastructure – directly from your browser!"
tags: ["deep dive"]
---

Accessing an Iceberg REST Catalogs can be a complex operation requiring multiple moving parts.
In this post, we describe the current patterns for interacting with Iceberg Catalogs, after which we ask the question, could it be done from a Browser?
After elaborating on the DuckDB ecosystem changes required to unlock this capability, we demonstrate our browser only approach to interacting with an Iceberg REST Catalog, no extra setup required.

## Interaction Models for Iceberg Catalogs

![Iceberg analytics today](/images/blog/iceberg-wasm/iceberg-analytics-today-dark.svg){: .darkmode-img }
![Iceberg analytics today](/images/blog/iceberg-wasm/iceberg-analytics-today-light.svg){: .lightmode-img }

_Iceberg_ is an _Open Table Format,_ which allows you to capture a mutable database table as a set of static files on object storage (such as AWS S3).
_Iceberg catalogs_ allow you to track and organize Iceberg tables.
For example, [Iceberg REST Catalogs](https://iceberg.apache.org/rest-catalog-spec/) provide these functionalities through a REST API.

There are two common ways to interact with Iceberg catalogs:

* The *client–server model,* where the compute part of the operation is delegated to a managed infrastructure (such as the cloud). Users can interact with the server by installing a local client or using a lightweight client such as a browser.
* The *client-is-the-server model,* where the user first installs the relevant libraries, and then performs queries directly on their machine.

Both models have their tradeoffs. In the *client–server model,* clients can be lightweight, and the server is the uniform point of access allowing for potential efficiencies thanks to scale. However, the infrastructure necessitates additional maintenance. In the *client-is-the-server model,* the query latency is lower, users can leverage local compute resources, and integration between local inputs and external data sources happens at the user level. This requires users to run computation locally, which means transferring part of the burden to your users (e.g., setting up dependencies).

Iceberg engine implementations work using either of those interaction models: they are either run natively in managed compute infrastructure or they are are run locally to the user.

Let's see how things look with DuckDB in the mix!

## Iceberg with DuckDB

![Iceberg with DuckDB](/images/blog/iceberg-wasm/iceberg-with-duckdb-dark.svg){: .darkmode-img }
![Iceberg with DuckDB](/images/blog/iceberg-wasm/iceberg-with-duckdb-light.svg){: .lightmode-img }

DuckDB supports both Iceberg interaction models.
In the _client–server model,_ DuckDB runs on the server to read the Iceberg datasets.
From the user's point of view, the choice of engine is transparent, and DuckDB is just one of many engines that the server could use in the background.
The *client-is-the-server* model is more interesting:
here, users [install a DuckDB client locally]({% link install/index.html %})
and use it through its SQL interface to query Iceberg catalogs.
For example:

```sql
CREATE SECRET test_secret (
    TYPE S3, 
    KEY_ID '⟨AKIAIOSFODNN7EXAMPLE⟩',
    SECRET '⟨wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY⟩'
);

ATTACH '⟨warehouse⟩' AS db (
    TYPE iceberg,
    ENDPOINT_URL '⟨https://your-iceberg-endpoint⟩',
);

SELECT sum(value)
FROM db.table
WHERE other_column = '⟨some_value⟩';
```

> You can discover the full DuckDB-Iceberg extension feature set, including insert and update capabilities, in our [earlier blog post]({% post_url 2025-11-28-iceberg-writes-in-duckdb %}).

## Iceberg with DuckDB in the Browser

While setting up a local DuckDB installation is quite simple, opening a browser tab is even quicker.
Therefore, we asked ourselves: could we support the *client-is-the-server* model directly from within a browser tab?
This could provide zero-setup, no-infrastructure, properly serverless option for interacting with Iceberg catalogs.

![Iceberg with DuckDB-Wasm](/images/blog/iceberg-wasm/duckdb-iceberg-with-duckdb-wasm-dark.svg){: .darkmode-img }
![Iceberg with DuckDB-Wasm](/images/blog/iceberg-wasm/duckdb-iceberg-with-duckdb-wasm-light.svg){: .lightmode-img }

Luckily, DuckDB has a client that can run in any browser!
[DuckDB-Wasm]({% link docs/stable/clients/wasm/overview.md %}) is a WebAssembly port of DuckDB, which [supports loading of extensions]({% post_url 2023-12-18-duckdb-extensions-in-wasm %}).

Interacting with an Iceberg REST Catalog requires a number of functionalities; the ability to talk to a REST API over HTTP(S), the ability to read and write `avro` and `parquet` files on object storage, and finally, the ability to negotiate authentication to access those resources on behalf of the user. All of these must be done from a within a browser without calling any native components.

To support these functionalities, we implemented the following high-level changes:

* In the core `duckdb` codebase, we redesigned HTTP interactions, so that extensions and clients have a uniform interface to the networking stack.
* In `duckdb-wasm`, we implemented such an interface, which in this case is a wrapper around the available JavaScript network stack.
* In `duckdb-iceberg`, we routed all networking through the common HTTP interface, so that native DuckDB and DuckDB-Wasm execute the same logic.

**The result is that you can now query Iceberg with DuckDB running directly in a browser!** Now you can access the same Iceberg catalog using *client–server*, *client-as-a-server*, or properly serverless from the isolation of a browser tab!

## Welcome to Serverless Iceberg Analytics

To see a demo of serverless Iceberg analytics, visit our table visualizer at [`duckdb.org/visualizer`]({% link visualizer/index.html %}?iceberg).

<video autoplay loop muted playsinline style="max-width:100%; height:auto;">
  <source src="images/blog/wasm-blog-post.mp4" type="video/mp4">
</video>

## Access Your Own Data

As of today, this demo works with [Amazon S3 Tables]({% link docs/stable/core_extensions/iceberg/amazon_s3_tables.md %}). This has been implemented through a collaboration with the Amazon S3 Tables team.

You can now provide your own Iceberg warehouse and a set of credentials which allow reads from the catalog, metadata and data (policy [`AmazonS3TablesReadOnlyAccess`](https://us-east-1.console.aws.amazon.com/iam/home?region=us-east-2#/policies/details/arn%3Aaws%3Aiam%3A%3Aaws%3Apolicy%2FAmazonS3TablesReadOnlyAccess)).
Computations are fully local, and the credentials and warehouse ID are only sent to the catalog endpoint specified in your `Attach` command.
Inputs are translated to SQL, and added to the hash segment of the URL.

This means that:

* no sensitive data is handled or sent to `duckdb.org`
* computations are local, fully in your browser
* you can use the familiar SQL interface with the same code snippets can be run everywhere DuckDB runs
* if you share the link, you might be sharing your credentials

## Conclusion

The DuckDB-Iceberg extension is now supported in DuckDB-Wasm and it can read and edit Iceberg REST Catalogs.
This allows users to unlock the analytical powers of DuckDB on their Iceberg catalogs without having to install or manage any compute nodes, making Iceberg tables even simpler to access.

At the moment one major implementation (Amazon S3 Tables) works out of the box, but hopefully more will follow.

If you would like to provide feedback or file issues, please reach out to us on either the [DuckDB-Wasm](https://github.com/duckdb/duckdb-wasm) or [DuckDB-Iceberg](https://github.com/duckdb/duckdb-iceberg) repository. If you are interested in using any part of this within your organization, feel free to [reach out](https://duckdblabs.com/contact/).

## Bonus

Another demo of DuckDB querying S3Tables from a Browser was presented at AWS Re:Invent 2025, you can view it [here](https://www.youtube.com/watch?t=2570&v=Pi82g0YGklU&feature=youtu.be). To learn more about S3Tables, how to get started and their feature set, you can take a look at their [product page](https://aws.amazon.com/s3/features/tables/) or [documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables.html).