---
github_repository: https://github.com/duckdb/duckdb-quack
layout: docu
title: Quack Remote Protocol
---

The Quack extension turns a DuckDB instance into a server that other DuckDB instances (clients) can connect to over HTTP.

This page covers the protocol at a glance and walks through basic usage on both sides of the wire.
For the full list of functions, settings, and logging knobs, see the [Reference]({% link docs/preview/quack/reference.md %}). For configuring TLS and authentication / authorization, see [Security]({% link docs/preview/quack/security.md %}). For user guides, see [Guides]({% link docs/preview/quack/setup/overview.md %}).

## Quack in a Nutshell

In short, the Quack protocol and its interactions work as follows:

* **HTTP-based.** Quack messages travel over plain HTTP or HTTPS via a reverse proxy (see [Security]({% link docs/preview/quack/security.md %})). This means standard load balancers, firewalls, and reverse proxies handle Quack traffic the same way they handle any other HTTP service. There is no custom wire transport to operate.
* **Client-driven request and response.** Every interaction is initiated by the client. The server does not initiate interactions via pushing.
* **`application/duckdb` serialization.** Requests and responses are encoded with DuckDB's internal serialization primitives (the same code path used by the [Write-Ahead Log]({% post_url 2024-10-30-analytics-optimized-concurrent-transactions %}#write-ahead-logging-and-checkpointing)). This avoids round-tripping data through an interchange format and keeps complex types (nested, decimals, intervals, ...) lossless across the wire.
* **Single round-trip per query.** After the initial connection handshake, a query needs only one request–response pair. Large results stream back in chunks via follow-up `FETCH` requests, optionally parallelized on multiple threads.
* **Default port: `9494`.** All URIs use the `quack:` scheme, e.g., `quack:hostname:port` with the port defaulting to `9494`.

## Server-Side Usage

### Starting a Server

A server is started from an existing DuckDB session. Everything that the session can see (in-memory tables, attached files, schemas) becomes reachable over the remote protocol.

To start listening on localhost, run:

{:.codebox-server}
```sql
CALL quack_serve('quack:localhost');
```

The URI argument is optional: calling `quack_serve()` without it also listens on `quack:localhost`.

`quack_serve` returns the listen URI, the HTTP URL, and, when the default authentication function is in use, and the `auth_token` that clients need to connect.
This token can also be set explicitly before starting (see [Security]({% link docs/preview/quack/security.md %})).

> Tip The DuckDB CLI can start a server directly with the `-serve` argument and connect to one with `-connect`. See [Command Line Arguments]({% link docs/preview/clients/cli/arguments.md %}#serving-and-connecting-to-remote-databases).

By default the server refuses to bind anything other than a local hostname. To listen on an externally-reachable address, pass `allow_other_hostname => true`:

{:.codebox-server}
```sql
CALL quack_serve('quack:0.0.0.0:9494', allow_other_hostname => true);
```

When you do this you should front the server with a TLS-terminating reverse proxy. See [Securing Quack with a Reverse Proxy]({% link docs/preview/quack/setup/reverse_proxy.md %}).

### URI Format

Quack endpoints use the `quack:` URI scheme and `9494` as the default port. Some examples:

| URI                 | Host        | Port   | Comment |
| ------------------- | ----------- | ------ | ------- |
| `quack:localhost`   | `localhost` | `9494` |         |
| `quack://localhost` | `localhost` | `9494` |         |
| `quack:myhost:9000` | `myhost`    | `9000` |         |
| `quack:127.0.0.1`   | `127.0.0.1` | `9494` |         |
| `quack:[::1]:1234`  | `::1`       | `1234` | (IPv6)  |

You can parse and validate a URI with the `quack_uri_parser(uri, ssl)` scalar function.

### Stopping a Server

To stop a server, run:

{:.codebox-server}
```sql
CALL quack_stop('quack:localhost');
```

## Client-Side Usage

There are three ways to talk to a Quack server:

1. `ATTACH 'quack:host' AS name` followed by `CONNECT name`: [route the whole session to the remote](#routing-a-session-with-connect). This is the recommended approach.
2. `ATTACH 'quack:host' AS name`: [attach the remote as a full catalog](#attaching-a-remote-database) and query it by qualifying table names.
3. `quack_query(uri, query)`: [stateless querying](#stateless-queries-with-quack_query).

In all cases, you need to [authenticate](#authentication).

The client picks plain HTTP automatically for local URIs (`localhost`, `127.0.0.1`, `::1`) and HTTPS otherwise.
Either default can be overridden with the `DISABLE_SSL` configuration option.

### Stateless Queries with `quack_query`

You can run any SQL against a server without attaching it.
To query a local database via HTTP, run:

{:.codebox-client}
```sql
FROM quack_query(
    'quack:localhost',
    'SELECT 42',
    token = '⟨MY_QUACK_TOKEN_01234567890ABCDEF⟩');
```

Remote databases use HTTPS by default. To override on a plain-HTTP remote, run:

{:.codebox-client}
```sql
FROM quack_query(
    'quack:remote.com',
    'SELECT 42',
    token = '⟨MY_QUACK_TOKEN_01234567890ABCDEF⟩',
    disable_ssl => true
);
```

The query executes remotely and the server stream the result back.
Errors occurring on the server (parse errors, missing tables, etc.) are shown locally in the DuckDB client.

### Attaching a Remote Database

To attach a local database via HTTP, simply run:

{:.codebox-client}
```sql
ATTACH 'quack:localhost' AS remote_db (
    TOKEN '⟨MY_QUACK_TOKEN_01234567890ABCDEF⟩'
);
```

Attaching remote databases uses HTTPS by default. To override on a plain-HTTP remote:

{:.codebox-client}
```sql
ATTACH 'quack:remote.com' AS remote_db (
    TOKEN '⟨MY_QUACK_TOKEN_01234567890ABCDEF⟩',
    DISABLE_SSL true
);
```

Once attached, remote tables look and behave like local ones:

{:.codebox-client}
```sql
CREATE TABLE remote_db.t AS FROM range(10) r(i);  -- DDL on remote
INSERT INTO remote_db.t VALUES (42);              -- remote writes
```

You can run queries against the remote database:

{:.codebox-client}
```sql
FROM remote_db.t;              -- scan remote table
FROM remote_db.t WHERE i = 42; -- run filter remotely
BEGIN; ...; COMMIT;            -- transactions are forwarded
DETACH quack;                  -- detach from the remote database
```

The attached catalog also exposes a `query` table macro for ad-hoc SQL scoped to that attachment:

{:.codebox-client}
```sql
FROM remote_db.query('SELECT 42');
```

### Routing a Session with `CONNECT`

Once a remote is attached, the [`CONNECT` statement]({% link docs/preview/sql/statements/connect.md %}) routes the whole session to it, so that subsequent queries execute on the server and their results stream back. This is the recommended way to work with a remote Quack database: you write plain SQL without qualifying every table name with the attached catalog. `DISCONNECT` returns the session to the local database.

{:.codebox-client}
```sql
ATTACH 'quack:server.example.com' AS qk (TOKEN '⟨MY_QUACK_TOKEN_01234567890ABCDEF⟩');

CONNECT qk;
SELECT count(*) FROM events; -- executes on the server, results stream back
DISCONNECT;
```

`CONNECT` is not specific to Quack: it points the session at any remote database that supports remote execution. See the [`CONNECT` and `DISCONNECT` statements]({% link docs/preview/sql/statements/connect.md %}) page for details.

### Authentication

Clients pass the authentication token to the server in one of two ways: a `quack` secret scoped to the server URI or an explicit `TOKEN` option on `ATTACH` / `quack_query`.
See [Security]({% link docs/preview/quack/security.md %}) for the full picture.

We recommend using a [secret]({% link docs/preview/configuration/secrets_manager.md %}) scoped to the server URI:

{:.codebox-client}
```sql
CREATE SECRET (
    TYPE quack,
    TOKEN '⟨MY_QUACK_TOKEN_01234567890ABCDEF⟩',
    SCOPE 'quack:localhost'
);

ATTACH 'quack:localhost' AS remote_db (TYPE quack);
```

Alternatively, you can pass the token directly, which overrides any matching secret:

{:.codebox-client}
```sql
ATTACH 'quack:localhost' AS remote_db (
    TOKEN '⟨MY_QUACK_TOKEN_01234567890ABCDEF⟩'
);
```

### HTTP Connection Caching

By default, each Quack client request opens a fresh connection to the server — a new TCP and, with SSL, a costly TLS handshake. Connection caching reuses connections across requests, reducing per-query latency on repeated requests:

{:.codebox-client}
```sql
SET httpfs_connection_caching = true;
```

### Node Identity (`whoami`)

Each Quack node exposes a `whoami()` table macro that surfaces basic identity and runtime info, useful when proxying to a fleet of servers or when correlating logs:

{:.codebox-client}
```sql
FROM remote_db.query('FROM whoami()');
```

```text
┌─────────┬──────────┬──────────┬─────────┬─────────────────┬───────────────────────────────┬────────────────────────────────────────────────────┐
│  name   │ provider │ hostname │ region  │     uptime      │            ts_now             │                        meta                        │
│ varchar │ varchar  │ varchar  │ varchar │    interval     │   timestamp with time zone    │                        json                        │
├─────────┼──────────┼──────────┼─────────┼─────────────────┼───────────────────────────────┼────────────────────────────────────────────────────┤
│ NULL    │ NULL     │ NULL     │ NULL    │ 00:04:56.832456 │ 2026-05-22 15:59:38.631715+02 │ {"duckdb_version":"v2.0.0","platform":"osx_arm64"} │
└─────────┴──────────┴──────────┴─────────┴─────────────────┴───────────────────────────────┴────────────────────────────────────────────────────┘
```

Identity fields are populated either by setting `whoami_*` options directly or by calling the `quack_identify` helper:

{:.codebox-client}
```sql
CALL quack_identify(
    name => 'analytics-1',
    provider => 'ec2',
    region => 'eu-west-1',
    meta => '{"role": "worker"}'
);
```

`meta` is merged with auto-computed `duckdb_version` and `platform` keys; user-supplied keys win on conflict.
`whoami_started_at` (an ISO 8601 timestamp) overrides the uptime anchor, otherwise uptime is measured from extension load.
