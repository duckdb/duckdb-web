---
layout: docu
title: Reference
---

This page lists every function, setting, and log type exposed by the [quack extension]({% link docs/current/core_extensions/quack.md %}).
For a tour of the protocol, start with the [Overview]({% link docs/current/quack/overview.md %}).

## Function Reference

### Server Management

| Function                                                                                        | Description                                                                                                                                                                                                           |
| ----------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `quack_serve(uri, token := 'token_value', allow_other_hostname := false, disable_ssl := false)` | Start a server on `uri`. Localhost-only by default. Pass `token` to set the server's authentication token explicitly (minimum 4 characters), otherwise one is generated. Returns listen URI, URL, and the auth token. |
| `quack_stop(uri)`                                                                               | Stop the server listening on `uri`.                                                                                                                                                                                   |
| `quack_identify(name, provider, hostname, region, meta)`                                        | Set this node's `whoami` identity fields. Any subset can be supplied.                                                                                                                                                 |
| `whoami()`                                                                                      | Table macro returning identity + runtime info for the current node.                                                                                                                                                   |

### Client Queries

| Function                                                                | Description                                                                                                             |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `quack_query(uri, query, token := 'token_value', disable_ssl := false)` | Run `query` on remote `uri`, stream result back. Pass `token` to override any matching quack secret on the client side. |
| `quack_query_by_name(catalog, query)`                                   | Run `query` against an already-attached Quack catalog (used by `⟨catalog⟩.query()`{:.language-sql .highlight}).         |

### Utility

| Function                                             | Description                                                                                            |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `quack_uri_parser(uri, ssl)`                         | Parse a Quack URI into a `STRUCT(host, port, ipv6, ssl, url)` entry                                    |
| `quack_check_token(sid, client_token, server_token)` | Default authentication callback, compares the client-supplied token against the server's stored token. |
| `quack_nop_authorization(sid, query)`                | Default authorization callback, always allows.                                                         |

### `ATTACH` Options

| Option        | Type      | Default                        | Description                                                                   |
| ------------- | --------- | ------------------------------ | ----------------------------------------------------------------------------- |
| `TOKEN`       | `VARCHAR` | (unset)                        | Authentication token. Overrides any matching quack secret on the client side. |
| `DISABLE_SSL` | `BOOLEAN` | `true` for local, else `false` | Force the client transport. Local URIs default to plain HTTP.                 |
| `TYPE`        | `VARCHAR` | inferred                       | Pin the secret type used for token resolution (e.g., `quack`).                |

## Settings

All settings are regular DuckDB session / global options. Set with `SET ⟨name⟩ = ⟨value⟩`{:.language-sql .highlight} or `SET GLOBAL`{:.language-sql .highlight}.

### Authentication / Authorization

The auth callbacks are evaluated on a fresh server-side connection every time, so the two settings below are **global-scoped** (`SET GLOBAL`). A plain `SET` on these is forwarded to the global slot automatically. Use `RESET GLOBAL` to restore the default, a plain `RESET` only clears the session view and the auth path will keep reading the stale global value.

| Setting                         | Type      | Default                   | Description                                                                                                                |
| ------------------------------- | --------- | ------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `quack_authentication_function` | `VARCHAR` | `quack_check_token`       | Name of a 3-arg scalar function `(sid, client_token, server_token) -> BOOLEAN` used by the server to authenticate clients. |
| `quack_authorization_function`  | `VARCHAR` | `quack_nop_authorization` | Name of a 2-arg scalar function `(sid, query) -> BOOLEAN` used by the server to authorize each query.                      |

You can plug in your own auth by creating any scalar function with the expected signature and pointing the setting at it. See [Security]({% link docs/current/quack/security.md %}) for examples.

### `FETCH` Batching (Server-Side)

The server batches multiple `DataChunk`s into each `FETCH` response to reduce per-chunk overhead.

| Setting                    | Type      | Default | Description                                                  |
| -------------------------- | --------- | ------- | ------------------------------------------------------------ |
| `quack_fetch_batch_chunks` | `UBIGINT` | `12`    | Maximum number of `DataChunk`s shipped per `FETCH` response. |

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

| context_id | scope      | connection_id | transaction_id | query_id | thread_id | timestamp                     | type  | log_level | message_type       | quack_connection_id              | client_query_id | query     | server                | duration_ms | response_type       | error |
| ---------: | ---------- | ------------: | -------------: | -------: | --------: | ----------------------------- | ----- | --------- | ------------------ | -------------------------------- | --------------: | --------- | --------------------- | ----------: | ------------------- | ----- |
|         60 | CONNECTION |             2 |             18 |       18 |      NULL | 2026-05-10 09:06:19.841623+02 | Quack | DEBUG     | CONNECTION_REQUEST |                                  |              18 | NULL      | http://localhost:9494 |          41 | CONNECTION_RESPONSE | NULL  |
|         60 | CONNECTION |             2 |             18 |       18 |      NULL | 2026-05-10 09:06:19.842407+02 | Quack | DEBUG     | PREPARE_REQUEST    | 091A003553E7E67B615B73D6BE81FD2E |              18 | SELECT 42 | http://localhost:9494 |           0 | PREPARE_RESPONSE    | NULL  |


Fields on each entry:

| Field                 | Description                                                           |
| --------------------- | --------------------------------------------------------------------- |
| `message_type`        | Request type: `PREPARE_REQUEST`, `FETCH_REQUEST`, etc.                |
| `quack_connection_id` | Server-issued connection id (stable across requests in one `ATTACH`). |
| `client_query_id`     | Monotonic id assigned by the client, correlates client / server logs. |
| `query`               | SQL payload for `PREPARE_REQUEST`s.                                   |
| `server`              | HTTP URL on client-side logs, `NULL` on server-side logs.             |
| `duration_ms`         | Round-trip time (client) or handling time (server).                   |
| `response_type`       | Response type  or `ERROR`.                                            |
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

| type | url                         | status |
| ---- | --------------------------- | ------ |
| POST | http://localhost:9494/quack | OK_200 |
| POST | http://localhost:9494/quack | OK_200 |

Requests are `POST`s to a `/quack` endpoint.

### Persisting Logs for Querying

`duckdb_logs_parsed` reads from DuckDB's in-memory log buffer. For non-trivial sessions you'll want to persist logs:

```sql
CALL enable_logging(
    'Quack',
    storage => 'file',
    storage_config => {'path': '/tmp/duckdb-rpc-logs'}
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
