---
layout: docu
title: Security
---

This page covers Quack's security posture end to end: what the server exposes, what stays local, the role of a TLS-terminating reverse proxy, and the authentication / authorization callbacks the server runs on every connection and every query.

## Exposure Model

A Quack server exposes the full SQL surface of the underlying DuckDB instance, including read and write access to every table the server's session can see. Because of this, the extension ships with conservative defaults that prevent accidental exposure:

* The server generates a **random authentication token** at startup, which the client has to supply on every connection.
* The server binds to `localhost` only, non-local hostnames require an explicit `allow_other_hostname => true`.
* The server does **not** use TLS itself. Involving the TLS for localhost communication only adds dependencies for no real benefit.

> Bestpractice For any deployment beyond local-only, do not expose Quack directly to the internet. We recommend you to put a proven HTTP reverse proxy in front of it and let the proxy terminate TLS.

The Quack client is shipped with these assumptions in mind: for non-local URIs it assumes HTTPS by default, so a properly fronted server "just works" from the client side too.
See [Securing Quack with a Reverse Proxy]({% link docs/current/quack/setup/reverse_proxy.md %}) for [nginx](https://nginx.org/) and [Caddy recipes](https://caddyserver.com/) (production and local-test).

## Authentication and Authorization

For every database call, there are two distinct decisions to be made:

* **Authentication**: *who* is the caller? Establishes identity, usually by having the caller supply a credential (e.g., a token, a password, a client certificate).
* **Authorization**: *may they do this?* Establishes whether an already authenticated caller is allowed to run a particular query, against a particular set of objects.

Quack runs these as two separate hooks: the authenticatiopn when a client first connects and the authorization before each query the client wants to issue.

### Default Configuration

Both hooks ship with built-in defaults that are suitable for local development and single-user deployments, and each is exposed as an overridable callback for deployments with stricter requirements.

Out of the box, they come with the following configuration:

* **Authentication is token-based.** When you call `quack_serve`, the server generates a random token and returns it in the `auth_token` column (or you can supply one explicitly via `quack_serve(uri, token := '...')`). Clients have to present this token on every connection, either through a `quack` secret scoped to the server URI or via the explicit `TOKEN` option in the `ATTACH` statement / `quack_query` function call. The default authentication callback compares the client-supplied token against the server's stored token.
* **Authorization is permissive.** The default authorization callback returns `true` for every query. No further filtering happens.

Both callbacks can be replaced with user-supplied code, including plain SQL macros. See the examples below.

### The Callback Contract

Two settings hold the **name** of the function to call as a hook for authentication / authorization:

| Setting                         | Default                   | Called when                                   |
| ------------------------------- | ------------------------- | --------------------------------------------- |
| `quack_authentication_function` | `quack_check_token`       | A new client connects (`CONNECTION_REQUEST`). |
| `quack_authorization_function`  | `quack_nop_authorization` | A client issues a query (`PREPARE_REQUEST`).  |

Both calls need to provide a `BOOLEAN` return: `true` admits the request, anything else (including a query error) rejects it with `Authentication failed` / `Authorization failed`.
Anything resolvable as a function with the matching arity and returning a `BOOLEAN` return type will work: built-in scalar functions, scalar UDFs registered by another extension, or SQL macros.
Authentication takes `(VARCHAR, VARCHAR, VARCHAR)`, authorization takes `(VARCHAR, VARCHAR)`.

The callbacks run in a **fresh, transient server-side connection**. That means they can read tables, call other UDFs, and reference extensions, but each invocation starts a new session and cannot rely on session-local state.

### Authentication Hook

The server invokes the authentication function by issuing the following SQL statement on every `CONNECTION_REQUEST` call:

```sql
SELECT ⟨quack_authentication_function⟩(⟨session_id⟩, ⟨client_token⟩, ⟨server_token⟩);
```

The arguments are defined as follows:

* `session_id`: Server-generated session id (random 32-char string). Becomes the `quack_connection_id` for that client.
* `client_token`: The token the client sent.
* `server_token`: The token configured on the server (via `quack_serve(token := ...)` or auto-generated).

#### Overriding Authentication

The cleanest way to plug in custom authentication is through using a [`MACRO`]({% link docs/current/sql/statements/create_macro.md %}).

##### Example: Multi-Token Table

Authenticate against a small table of allowed tokens (e.g., one per user):

```sql
CREATE TABLE quack_tokens (auth_token VARCHAR, user_name VARCHAR);
INSERT INTO quack_tokens VALUES
    ('alice-key-123', 'alice'),
    ('bob-key-456',   'bob');

CREATE MACRO check_token(sid, client_token, server_token) AS (
    EXISTS (SELECT 1 FROM quack_tokens WHERE auth_token = client_token)
);

SET GLOBAL quack_authentication_function = 'check_token';
```

Now any client whose token is in `quack_tokens` is admitted, everyone else is rejected. Adding / removing users is a regular `INSERT` / `DELETE` operation.

##### Example: Developer Mode (Always Allow)

When developing locally in a sandboxed environment, you can consider using “developer mode” authentication, which allows every incoming connection:

```sql
CREATE MACRO developer_mode_auth(sid, client_token, server_token) AS true;
SET GLOBAL quack_authentication_function = 'developer_mode_auth';
```

### Authorization Hook

The server invokes the authorization function by issuing the following SQL statement on every `PREPARE_RESPONSE` call:

```sql
SELECT ⟨quack_authorization_function⟩(⟨connection_id⟩, ⟨query⟩);
```

The arguments are defined as follows:

* `connection_id`: The `quack_connection_id` of the calling client (i.e., the same id the [authentication hook](#authentication-hook) saw as its `session_id` argument).
* `query`: The full SQL text the client wants to execute.

#### Overriding Authorization

Authorization runs once per `PREPARE_REQUEST`, with the connection id and the full SQL text. Common shapes:

##### Example: Read-Only

```sql
CREATE MACRO read_only(sid, query) AS
    regexp_matches(upper(trim(query)), '^(SELECT|FROM|WITH|EXPLAIN|DESCRIBE|SHOW)\b');

SET GLOBAL quack_authorization_function = 'read_only';
```

For more involved authorization functions, see the [Beyond SQL Macros](#beyond-sql-macros) section.

## Beyond SQL Macros

SQL macros cover most authentication and authorization cases, but a macro body is restricted to a single expression and cannot execute DML directly: there is no `INSERT`, `UPDATE`, or `DELETE` inside a macro.
For policies that need to record every call to a table, maintain in-process state across calls, or otherwise drive imperative logic, register a scalar function via a DuckDB extension instead.

DuckDB extensions can be written in C++ (the primary language) or any language with bindings to DuckDB's C extension API, including Rust, C, and Go. The registered authentication or authorization function must expose the same `(VARCHAR, ...) → BOOLEAN` signature as the SQL macros above. Once the extension is loaded, point `quack_authentication_function` or `quack_authorization_function` at the function name.

> Python UDFs registered through `con.create_function` are scoped to the connection that created them. Quack invokes each callback on a fresh server-side connection, so Python UDFs are not visible at dispatch time and cannot be used as authentication or authorization callbacks. Register the function via a DuckDB extension to make it globally visible.

### Example: Read-Only Queriers

A self-contained example: a server that requires per-user tokens and limits each user to read-only queries.

```sql
CREATE TABLE quack_tokens (auth_token VARCHAR, user_name VARCHAR);
INSERT INTO quack_tokens VALUES ('analytics-team-token', 'analytics');

CREATE MACRO check_token(sid, client_token, server_token) AS (
    EXISTS (SELECT 1 FROM quack_tokens WHERE auth_token = client_token)
);

CREATE MACRO read_only(sid, query) AS (
    regexp_matches(upper(trim(query)), '^(SELECT|FROM|WITH|EXPLAIN)\b')
);

CALL quack_serve('quack:localhost', token => 'analytics-team-token');

SET GLOBAL quack_authentication_function = 'check_token';
SET GLOBAL quack_authorization_function  = 'read_only';
```

A client with the right token now connects and can run `SELECT`s, but `INSERT INTO quack.t ...` issued through the standard SQL path will fail at authorization time.

### Example: Per-User Access Control List

To implement per-user access control list (ACL), create a custom authentication hook that records `sid` → `user` pairs so authorization can look up who is asking.
Because macros can't write, the recording side has to be a scalar UDF defined e.g. by a custom DuckDB extension. The authorization side can be a macro:

```sql
-- (populated by the auth UDF when a client connects)
CREATE TABLE quack_sessions (sid VARCHAR PRIMARY KEY, user_name VARCHAR);

-- per-user query allowlist (your own data model)
CREATE TABLE quack_user_acls (user_name VARCHAR, query_kind VARCHAR);

CREATE MACRO acl_check(sid, query) AS (
    EXISTS (
        SELECT 1
        FROM quack_sessions s
        JOIN quack_user_acls a ON a.user_name = s.user_name
        WHERE s.sid = sid
          AND regexp_matches(upper(trim(query)), '^' || a.query_kind || '\b')
    )
);

SET GLOBAL quack_authorization_function = 'acl_check';
```
