---
layout: docu
title: Securing Quack with a Reverse Proxy
---

The Quack server speaks plain HTTP only and binds to localhost by default. See [Security]({% link docs/current/quack/security.md %}) for the rationale behind these configurations.
For any deployment beyond local-only, the recommended pattern is the same as for any other HTTP-based database / application server: put a proven HTTP reverse proxy in front of it, and let the proxy terminate TLS.

The Quack client cooperates with this: for non-local URIs it assumes HTTPS by default, so a properly fronted server “just works” from the client side too.

This guide walks through three setups, in order of likely usefulness:

1. A **local TLS test setup** with Caddy, so you can exercise the full HTTPS path on your machine.
2. **nginx + Let's Encrypt** in production.
3. **Caddy + Let's Encrypt** in production.

The two production setups are interchangeable. Pick whichever fits your operational stack.

## Local Test Setup with Caddy

You can exercise the full HTTPS path on your own machine using Caddy. Caddy issues itself a certificate for `localhost` from a local CA and installs the CA root into your system trust store, so DuckDB's HTTPS client trusts the cert without any extra config.

### 1. Run Caddy

Save this `Caddyfile`:

```text
localhost:8443 {
    reverse_proxy 127.0.0.1:9494 {
        flush_interval -1
    }

    request_body {
        max_size 256MB
    }
}
```

Then start Caddy:

```bash
brew install caddy # macOS, for other platforms see https://caddyserver.com/docs/install
caddy run --config Caddyfile
```

The first run will prompt for elevation to install Caddy's local CA into your system trust store. After that, certs issued by Caddy for `localhost` are trusted system-wide.

### 2. Start Quack and Connect Through the Proxy

In one DuckDB session, start the server (this prints an authentication token):

{:.codebox-server}
```sql
CALL quack_serve('quack:localhost');
```

In the client session, connect through Caddy on `:8443`. Local URIs default to plain HTTP, so you have to **force SSL on** explicitly:

{:.codebox-server}
```sql
ATTACH 'quack:localhost:8443' AS quack (
    TOKEN '⟨authentication_token-from-quack_serve⟩',
    DISABLE_SSL false
);

FROM quack.query('SELECT 42');
```

If the round-trip succeeds, your traffic just went out as TLS to Caddy, got terminated, and was forwarded as plain HTTP to Quack on `:9494`.


## Nginx + Let's Encrypt

We expect this to be the most common choice. A minimal site for a Quack server listening on the loopback interface looks as follows:

```text
# /etc/nginx/sites-enabled/quack.example.com
server {
    listen 443 ssl http2;
    server_name quack.example.com;

    ssl_certificate     /etc/letsencrypt/live/quack.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/quack.example.com/privkey.pem;

    # Quack RPC bodies can be large: PREPARE carries SQL, APPEND carries
    # inserted DataChunks. The 1 MiB nginx default will fail mid-INSERT.
    client_max_body_size 256M;

    # Long-running queries can sit on the wire between FETCHes for
    # minutes. Raise the timeouts above nginx's default 60s.
    proxy_read_timeout 600s;
    proxy_send_timeout 600s;

    location / {
        proxy_pass http://127.0.0.1:9494;

        # Keep-alive against upstream. Quack relies on persistent
        # connections to keep server-side `quack_connection_id` state alive.
        proxy_http_version 1.1;
        proxy_set_header Connection "";

        # Quack streams results via repeated FETCH responses; buffering
        # through nginx defeats the streaming and inflates memory.
        proxy_buffering off;
    }
}
```

On the Quack side, start the server bound to localhost (the default):

{:.codebox-server}
```sql
CALL quack_serve('quack:localhost');
```

Issue the certificate with `certbot --nginx -d quack.example.com`.
Clients connect over HTTPS automatically:

{:.codebox-client}
```sql
ATTACH 'quack:quack.example.com' AS quack;   -- HTTPS auto-selected
```

## Caddy + Let's Encrypt

[Caddy](https://caddyserver.com/) auto-provisions certificates from Let's Encrypt and needs almost no configuration. A complete public-facing Quack proxy:

```text
# /etc/caddy/Caddyfile
quack.example.com {
    reverse_proxy 127.0.0.1:9494 {
        # Equivalent of nginx `proxy_buffering off`. Required so Quack's
        # streamed FETCH responses pass through immediately instead of
        # being buffered in Caddy.
        flush_interval -1
    }

    # Equivalent of nginx `client_max_body_size`. PREPARE / APPEND bodies
    # can be much larger than the default request body cap.
    request_body {
        max_size 256MB
    }
}
```

Caddy handles certificate issuance and renewal automatically. No `certbot` step is required.

On the Quack side, start the server bound to localhost (the default):

{:.codebox-server}
```sql
CALL quack_serve('quack:localhost');
```

Clients connect over HTTPS automatically:

{:.codebox-client}
```sql
ATTACH 'quack:quack.example.com' AS quack;   -- HTTPS auto-selected
```
