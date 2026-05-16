---
layout: post
title: "DuckDB 1.5.3: Shipping Quack as a Core Extension"
author: "The DuckDB team"
thumb: "/images/blog/thumbs/duckdb-release-1-5-3.svg"
image: "/images/blog/thumbs/duckdb-release-1-5-3.png"
excerpt: "We are releasing DuckDB version v1.5.3 with Quack as a core extension, several bugfixes and performance improvements."
tags: ["release"]
---

In this blog post, we highlight a few important fixes in DuckDB v1.5.3, the third (and likely last) patch release in [DuckDB's v1.5 line]({% post_url 2026-03-09-announcing-duckdb-150 %}).
You can find the complete [release notes on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.5.3).

To install the new version, please visit the [installation page]({% link install/index.html %}).

## What's New

### Quack

On May 12, we introduced Quack, our new remote protocol that turns DuckDB into a client-server database.
If you are new to Quack and don't know where to start, check out the following resources:

* For a high-level overview, see the [Quack explainer page]({% link quack/index.html %}).
* For the rationale and history behind Quack, and for an introduction, see the [announcement blog post]({% post_url 2026-05-12-quack-remote-protocol %}).
* For the reference manual and setup guide, check out the [Quack documentation]({% link docs/current/quack/overview.md %}).

DuckDB v1.5.3 ships Quack as a core extension. This means you can now set up Quack with `INSTALL quack` from any client running DuckDB, and Quack will be transparently [autoloaded]({% link docs/current/extensions/overview.md %}#autoloading-extension) on first use.

<!-- markdownlint-disable MD001 -->

<div class="duck-diagram" markdown="1">

<div class="duck-diagram-box" markdown="1">

#### <svg class="icon"><use href="#database-01"></use></svg> DuckDB #1

```sql
INSTALL quack;

CALL quack_serve(
    'quack:localhost',
    token = 'super_secret'
);

CREATE TABLE hello AS
    FROM VALUES ('world') v(s);
```

</div>

<div class="duck-diagram-arrow">quack:</div>

<div class="duck-diagram-box" markdown="1">

#### <svg class="icon"><use href="#database-01"></use></svg> DuckDB #2

```sql
INSTALL quack;

CREATE SECRET (
    TYPE quack,
    TOKEN 'super_secret'
);

ATTACH 'quack:localhost' AS remote;
FROM remote.hello;
```

</div>

</div>

<!-- markdownlint-enable MD001 -->

Please note that Quack is still in beta state and breaking changes may happen in the protocol, in function names, etc.
We plan to release the production-ready version of Quack together with [DuckDB v2.0]({% link release_calendar.md %}) in fall 2026.

### AWS

The [AWS extension]({% link docs/current/core_extensions/aws.md %}) now supports the [`web_identity` chain type for IAM Roles for Service Accounts (IRSA) support](https://github.com/duckdb/duckdb-aws/pull/136).
This was made possible through a contribution by community member [Marcel Steinbach (@mst)](https://github.com/mst).

### Iceberg

TODO

## Coming Up

We have quite a few events coming up in the next few weeks:

**DuckCon #7.** On June 24, we'll host our next user conference, [DuckCon #7]({% link _events/2026-06-24-duckcon7.html %}), in Amsterdam's beautiful [Royal Tropical Institute](https://www.kit.nl/about-us/).

**Ubuntu Summit Talk.** Next week, Gábor Szárnyas of DuckDB Labs will give a talk titled [“DuckDB: Not Quack Science”]({% link _library/2026-05-27-duckdb-not-quack-science.md %}) at the [Ubuntu Summit](https://ubuntu.com/summit).

## Conclusion

This post is a short summary of the changes in v1.5.3. As usual, you can find the [full release notes on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.5.3).
