---
layout: docu
redirect_from:
- /docs/current/quack/reference
- /docs/lts/quack/reference
- /docs/preview/quack/reference
title: Reference
---

This page lists the functions, settings, and log types exposed by the [quack extension]({% link docs/2.0/core_extensions/quack.md %}).
For a tour of the protocol, start with the [Overview]({% link docs/2.0/quack/overview.md %}).

## Function Reference

### Server Management

| Function | Description |
| -------- | ----------- |
| `quack_serve(⟨listen_uri⟩, ...)` | Start a server on `listen_uri`, which defaults to `quack:localhost` when omitted. Localhost-only by default. Returns the listen URI, the listen URL, and the authentication token. See the [`quack_serve` parameters](#quack_serve-parameters) below. |
| `quack_stop(listen_uri)` | Stop the server listening on `listen_uri`. |
| `quack_server_list()` | List the servers running in this instance: listen URI and URL, host, port, number of active connections, and additional info (IPv6, SSL). |
| `quack_active_connections()` | List the client connections of the servers running in this instance: server, `quack_connection_id`, last query, state, hashed client id, cached rows, and query start time. |
| `quack_generate_keys(directory = ⟨path⟩)` | Generate a self-signed certificate (`server.pem`) and private key (`private_key.pem`) for serving over SSL. Defaults to `~/.duckdb/extension_data/quack`; existing key files are not overwritten. Returns the file paths and the certificate fingerprint. |
| `quack_identify(name, provider, hostname, region, meta)` | Set this node's `whoami` identity fields. Any subset can be supplied. |
| `whoami()` | Table macro returning identity + runtime info for the current node. |

#### `quack_serve` Parameters

| Parameter | Type | Default | Description |
| --------- | ---- | ------- | ----------- |
| `listen_uri` | `VARCHAR` | `quack:localhost` | Positional. The Quack URI to listen on. |
| `allow_other_hostname` | `BOOLEAN` | `false` | Allow binding to a non-local hostname, e.g., `0.0.0.0`. |
| `token` | `VARCHAR` | (generated) | Authentication token clients have to present (minimum 4 characters). If omitted, the token of the default `quack` secret is used if one exists, otherwise a random token is generated. |
| `secret` | `VARCHAR` | (unset) | Name of an existing `quack` secret whose token the server uses. |
| `create_secret_if_not_exists` | `BOOLEAN` | `false` | If no token is given and no default `quack` secret exists, store the generated token in a persistent default `quack` secret, so that subsequent servers reuse it. |
| `disable_ssl` | `BOOLEAN` | `true` for local, else `false` | Serve plain HTTP. Local URIs default to plain HTTP, other URIs to HTTPS. |
| `ssl_cert_file` | `VARCHAR` | (generated) | Certificate file used when serving over SSL. If omitted, a self-signed certificate is generated (see `quack_generate_keys`). |
| `ssl_key_file` | `VARCHAR` | (generated) | Private key file used when serving over SSL. |

### Client Queries

| Function | Description |
| -------- | ----------- |
| `quack_query(uri, query, ...)` | Run `query` on remote `uri`, stream result back. Accepts the named parameters `token`, `disable_ssl`, `ssl_fingerprint`, `client_id` and `heartbeat_timeout`, which behave like the [`ATTACH` options](#attach-options) of the same name. Pass `token` to override any matching quack secret on the client side. |
| `quack_query_by_name(catalog, query)` | Run `query` against an already-attached Quack catalog (used by `⟨catalog⟩.query()`{:.language-sql .highlight}). Also accepts the named parameters `use_transaction` and `refresh_catalog` (both `BOOLEAN`). |
| `quack_connection_id(catalog)` | Return the server-issued `quack_connection_id` of an attached Quack catalog. |
| `quack_cancel(catalog, connection_id)` | Cancel the running query of the connection `connection_id` on the server of the attached Quack catalog `catalog`. Returns the connection id and whether the cancellation succeeded. |

### Utility

| Function | Description |
| -------- | ----------- |
| `quack_uri_parser(uri, ssl)` | Parse a Quack URI into a `STRUCT(host, port, ipv6, ssl, url)` entry. |
| `quack_check_token(sid, client_token, server_token)` | Default authentication callback, compares the client-supplied token against the server's stored token. |
| `quack_nop_authorization(sid, query)` | Default authorization callback, always allows. |
| `quack_clear_cache()` | Clear the cache. This also forces the DuckDB client to refresh its catalog. |

### `ATTACH` Options

| Option        | Type      | Default                        | Description                                                                   |
| ------------- | --------- | ------------------------------ | ----------------------------------------------------------------------------- |
| `TOKEN`       | `VARCHAR` | (unset)                        | Authentication token. Overrides any matching quack secret on the client side. |
| `DISABLE_SSL` | `BOOLEAN` | `true` for local, else `false` | Force the client transport. Local URIs default to plain HTTP.                 |
| `TYPE`        | `VARCHAR` | inferred                       | Pin the secret type used for token resolution (e.g., `quack`).                |
| `SSL_FINGERPRINT` | `VARCHAR` | (unset)                    | Expected fingerprint of the server's certificate, e.g., the `fingerprint` returned by `quack_generate_keys`. Use this to connect to a server with a self-signed certificate. |
| `CLIENT_ID`   | `VARCHAR` | `quack_default_client_id`      | Client identifier sent to the server (minimum 4 characters).                  |
| `HEARTBEAT_TIMEOUT` | `UBIGINT` | `quack_default_heartbeat_timeout` | Heartbeat lease timeout in seconds requested from the server.    |

## Settings

All settings are regular DuckDB session / global options. Set with `SET ⟨name⟩ = ⟨value⟩`{:.language-sql .highlight} or `SET GLOBAL`{:.language-sql .highlight}.

### Authentication / Authorization

The auth callbacks are evaluated on a fresh server-side connection every time, so the two settings below are **global-scoped** (`SET GLOBAL`). A plain `SET` on these is forwarded to the global slot automatically. Use `RESET GLOBAL` to restore the default, a plain `RESET` only clears the session view and the auth path will keep reading the stale global value.

| Setting                         | Type      | Default                   | Description                                                                                                                |
| ------------------------------- | --------- | ------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `quack_authentication_function` | `VARCHAR` | `quack_check_token`       | Name of a 3-arg scalar function `(sid, client_token, server_token) -> BOOLEAN` used by the server to authenticate clients. |
| `quack_authorization_function`  | `VARCHAR` | `quack_nop_authorization` | Name of a 2-arg scalar function `(sid, query) -> BOOLEAN` used by the server to authorize each query.                      |

You can plug in your own auth by creating any scalar function with the expected signature and pointing the setting at it. See [Security]({% link docs/2.0/quack/security.md %}) for examples.

### Data Transfer

These settings control how results and inserted data are batched and buffered.

| Setting | Type | Default | Description |
| ------- | ---- | ------- | ----------- |
| `quack_target_batch_bytes` | `UBIGINT` | `33554432` (32 MiB) | Target in-memory size of one batch (one wire message payload). Batches are cut when they reach this size. |
| `quack_prepare_inline_rows` | `UBIGINT` | `24576` | Rows returned inline in the `PREPARE` response before the remainder is left to `FETCH`. Drains whole batches, so it may overshoot to a batch boundary. |
| `quack_fetch_read_ahead` | `UBIGINT` | `0` | Number of `FETCH` requests the client keeps in flight ahead of the scan. `0` uses the number of async threads. |
| `quack_rebalance_buffer_bytes` | `UBIGINT` | `0` | Pending bytes the batch rebalancer buffers before gating non-minimum producers. `0` means automatic, governed by the memory manager. |
| `quack_server_stream_buffer_bytes` | `UBIGINT` | `268435456` (256 MiB) | Server-side per-stream byte budget, at most a quarter of `memory_limit`. `FETCH` counts serialized payload bytes, `INSERT` counts decoded chunk allocations. `0` disables the limit. |

### Server Connections

| Setting | Type | Default | Description |
| ------- | ---- | ------- | ----------- |
| `quack_server_max_connections` | `UBIGINT` | `1024` | Maximum number of concurrent connections the server accepts. Beyond this, new connections are refused. |
| `quack_server_keep_alive_timeout` | `UBIGINT` | `300` | Seconds an idle keep-alive connection is kept open by the server. |

### Client Identity and Reconnects

| Setting | Type | Default | Description |
| ------- | ---- | ------- | ----------- |
| `quack_default_client_id` | `VARCHAR` | (random per instance) | Client id used when `ATTACH` / `quack_query` omit one. Computed at load time from the `QUACK_CLIENT_ID` environment variable, or a random per-instance id if the variable is not set. Set to `''` to opt out. |
| `quack_default_heartbeat_timeout` | `UBIGINT` | `60` | Heartbeat lease timeout in seconds requested by clients when `ATTACH` / `quack_query` omit `heartbeat_timeout`. |
| `quack_enable_reconnects` | `BOOLEAN` | `false` | Enable reconnect support: clients acknowledge results and the server caches the last result until it is acknowledged. |
| `quack_result_ttl` | `UBIGINT` | `3600` | Seconds an idle cached result is kept before it is dropped (`0` = never). |
| `quack_cache_max_rows` | `UBIGINT` | `100000` | Maximum number of rows the server retains in the result cache (`0` = unlimited). |

The extension also registers several `quack_debug_*` settings, which are intended for testing the protocol and should not be used in production.

### Node Identity

These settings back the `whoami()` macro. `quack_identify(...)` is sugar that updates them.

| Setting              | Type      | Default                              | Description                                               |
| -------------------- | --------- | ------------------------------------ | --------------------------------------------------------- |
| `whoami_name`        | `VARCHAR` | (empty)                              | Human-readable node name.                                 |
| `whoami_provider`    | `VARCHAR` | (empty)                              | Deployment provider (`ec2`, `docker`, `local`, ...).      |
| `whoami_hostname`    | `VARCHAR` | (empty)                              | Network hostname / public address.                        |
| `whoami_region`      | `VARCHAR` | (empty)                              | Deployment region.                                        |
| `whoami_started_at`  | `VARCHAR` | (empty)                              | Node start time (ISO 8601 timestamp). Anchors `uptime`.   |
| `whoami_meta`        | `VARCHAR` | `{}`                                 | Provider-specific metadata as JSON.                       |
| `quack_loaded_at_us` | `BIGINT`  | Epoch microseconds at extension load | Fallback uptime anchor when `whoami_started_at` is empty. |

## Logging

Two log types are registered by the extension. Enable them to debug connectivity or measure request timing.

### Quack Log

Structured log of every Quack message (both client- and server-side):

```sql
CALL enable_logging('Quack');

FROM quack_query('quack:localhost', 'SELECT 42');

SELECT * FROM duckdb_logs_parsed('Quack');
```

<div class="monospace_table"></div>

<!-- markdownlint-disable MD034 -->

| context_id | scope      | connection_id | transaction_id | query_id | thread_id | timestamp                     | type  | log_level | message_type       | quack_connection_id              | client_query_id | query     | server                | duration_ms | response_type       | error |
| ---------: | ---------- | ------------: | -------------: | -------: | --------: | ----------------------------- | ----- | --------- | ------------------ | -------------------------------- | --------------: | --------- | --------------------- | ----------: | ------------------- | ----- |
|         60 | CONNECTION |             2 |             18 |       18 |      NULL | 2026-05-10 09:06:19.841623+02 | Quack | DEBUG     | CONNECTION_REQUEST |                                  |              18 | NULL      | http://localhost:9494 |          41 | CONNECTION_RESPONSE | NULL  |
|         60 | CONNECTION |             2 |             18 |       18 |      NULL | 2026-05-10 09:06:19.842407+02 | Quack | DEBUG     | PREPARE_REQUEST    | 091A003553E7E67B615B73D6BE81FD2E |              18 | SELECT 42 | http://localhost:9494 |           0 | PREPARE_RESPONSE    | NULL  |

<!-- markdownlint-enable MD034 -->

Fields on each entry:

| Field                 | Description                                                           |
| --------------------- | --------------------------------------------------------------------- |
| `message_type`        | Request type: `PREPARE_REQUEST`, `FETCH_REQUEST`, etc.                |
| `quack_connection_id` | Server-issued connection id (stable across requests in one `ATTACH`). |
| `client_query_id`     | Monotonic id assigned by the client, correlates client / server logs. |
| `query`               | SQL payload for `PREPARE_REQUEST`s.                                   |
| `server`              | HTTP URL on client-side logs, `NULL` on server-side logs.             |
| `duration_ms`         | Round-trip time (client) or handling time (server).                   |
| `response_type`       | Response type or `ERROR`.                                             |
| `error`               | Error message if the request failed.                                  |

To correlate a client request with its server-side handling, join on `(quack_connection_id, client_query_id)`.

### HTTP Log

The underlying HTTP transport can be logged separately:

```sql
CALL enable_logging('HTTP');
FROM quack_query('quack:localhost', 'SELECT 1');
SELECT request.type, request.url, response.status
FROM duckdb_logs_parsed('HTTP');
```

<div class="monospace_table"></div>

<!-- markdownlint-disable MD034 -->

| type | url                         | status |
| ---- | --------------------------- | ------ |
| POST | http://localhost:9494/quack | OK_200 |
| POST | http://localhost:9494/quack | OK_200 |

<!-- markdownlint-enable MD034 -->

Requests are `POST`s to a `/quack` endpoint.

### Persisting Logs for Querying

`duckdb_logs_parsed` reads from DuckDB's in-memory log buffer. For non-trivial sessions you'll want to persist logs:

```sql
CALL enable_logging(
    'Quack',
    storage = 'file',
    storage_config = {'path': '/tmp/duckdb-rpc-logs'}
);
```

To clear the log between runs, use:

```sql
CALL truncate_duckdb_logs();
```

To turn logging off, run:

```sql
CALL disable_logging();
```
