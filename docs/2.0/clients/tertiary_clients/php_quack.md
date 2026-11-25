---
github_repository: https://github.com/thomas-0816/duckdb-quack-protocol-php
layout: docu
redirect_from:
- /docs/current/clients/tertiary_clients/php_quack
- /docs/lts/clients/tertiary_clients/php_quack
- /docs/preview/clients/tertiary_clients/php_quack
- /docs/stable/clients/tertiary_clients/php_quack
title: PHP Client (Quack Remote Protocol)
---

> The PHP client for DuckDB Quack Remote Protocol is a tertiary client and is maintained by a third-party.
>
> To use the PHP client, follow the [instructions below](#installation-and-setup-client).
>
> The latest version of the client supports DuckDB {{ site.maintained_duckdb_php_quack_version }}.

The [PHP client for DuckDB Quack Remote Protocol](https://github.com/thomas-0816/duckdb-quack-protocol-php) is a pure PHP implementation of the DuckDB Quack Remote Protocol (DuckDB client).\
It implements Quack Remote Protocol v3. As a pure PHP implementation, it does not include FFI or C code.\
The HTTP transport uses plain PHP streams or the curl extension (curl preferred).

All DuckDB types are supported: Text, Numeric, Date, Time, Interval, JSON, Array, Struct, Map, List, Tuple, Type, Enum, Variant, Geometry, Union, Bitstring, Blob, and Boolean.

Supported PHP versions: [8.2 or newer](https://www.php.net/supported-versions.php)

GitHub: [duckdb-quack-protocol-php](https://github.com/thomas-0816/duckdb-quack-protocol-php)

Packagist: [duckdb-quack-protocol-php](https://packagist.org/packages/thomas-0816/duckdb-quack-protocol-php)

## Installation and Setup (Client)

```bash
composer require thomas-0816/duckdb-quack-protocol-php
```

## Installation and Setup (Server)

Start the DuckDB Server:

```bash
# localhost, port 9494, HTTP
duckdb --cmd "CALL quack_serve('quack:127.0.0.1:9494', token='secret');"

# public server, port 9495, HTTPs, creates self-signed certificates
duckdb --cmd "CALL quack_serve('quack:0.0.0.0:9495', token='secret', allow_other_hostname=true, disable_ssl=false);"
```

Read more about [Quack Remote Protocol](/docs/2.0/quack/overview).

## Usage Examples

```php
use DuckDB\Quack\QuackClient;

require __DIR__ . '/vendor/autoload.php';

// http-connect-timeout 3s, http-timeout 10s
$db = QuackClient::connect('http://127.0.0.1:9494', 'secret', 3, 10);
$db->execute('CREATE TABLE IF NOT EXISTS table1 (id INTEGER, amount DECIMAL(10, 2), description VARCHAR)');

$db->beginTransaction();
$db->execute('INSERT INTO table1 VALUES (?, ?, ?)', [1, 42.21, 'Hello DuckDB! 🐘 💓 🦆']);
$db->execute('INSERT INTO table1 VALUES (?, ?, ?)', [2, 21.01, 'Hello PHP! 🐘']);
$db->commit();

print_r($db->fetchAll('SELECT * FROM table1'));

# Array
#     [0] => Array
#         [id] => 1
#         [amount] => 42.21
#         [description] => Hello DuckDB! 🐘 💓 🦆
#     [1] => Array
#         [id] => 2
#         [amount] => 21.01
#         [description] => Hello PHP! 🐘

print_r($db->fetchOne('SELECT * FROM table1'));

# Array
#     [id] => 1
#     [amount] => 42.21
#     [description] => Hello DuckDB! 🐘 💓 🦆

print_r($db->fetchValue('SELECT id FROM table1'));

# 1

print_r($db->fetchAllKeyValue('SELECT id, amount FROM table1'));

# Array
#     [1] => 42.21
#     [2] => 21.01

print_r($db->fetchColumn('SELECT description FROM table1'));

# Array
#     [0] => Hello DuckDB! 🐘 💓 🦆
#     [1] => Hello PHP! 🐘

foreach ($db->fetchIterator('SELECT * FROM table1') as $row) {
    print_r($row);
}

# Array
#     [id] => 1
#     [amount] => 42.21
#     [description] => Hello DuckDB! 🐘 💓 🦆
# Array
#     [id] => 2
#     [amount] => 21.01
#     [description] => Hello PHP! 🐘

// named parameter binding
$db->execute("SET VARIABLE foo = 'bar'");
print_r($db->fetchOne('SELECT :id as a, :amount as b, $foo as c', ['id' => 1, 'amount' => 12.34]));

# Array
#     [a] => 1
#     [b] => 12.34
#     [c] => bar

unset($db); // Disconnect
```

More examples can be found in the [readme](https://github.com/thomas-0816/duckdb-quack-protocol-php).

## Timeout Configuration

```php
// HTTP connect timeout 3s
// HTTP timeout 10s
$db = QuackClient::connect('http://127.0.0.1:9494', 'secret', 3, 10);
```

HTTP connect timeout and HTTP timeout (total request time) are applied per request.
One query can span over multiple requests.

## HTTPs Connections with Self-Signed certificates

```php
use DuckDB\Quack\QuackClient;

require __DIR__ . '/../vendor/autoload.php';

// file location of self-signed public key
$pemFile = getenv('HOME') . '/.duckdb/extension_data/quack/server.pem';

$db = QuackClient::connect('https://localhost:9495', 'secret', 3, 10, [], $pemFile);
echo $db->fetchValue('SELECT 42'), PHP_EOL;
```

Read more about [Quack Security](/docs/2.0/quack/security).

## Monitoring

```php
use DuckDB\Quack\QuackClient;

require __DIR__ . '/vendor/autoload.php';

$db = QuackClient::connect('http://127.0.0.1:9494', 'secret', 3, 10);

print_r($db->fetchAll('SELECT * FROM quack_active_connections()'));

# Array
#     [0] => Array
#         [server_id] => quack:127.0.0.1:9494
#         [connection_id] => 83FA7408F5D392C23C6CADDDB1F579F2
#         [query] => SELECT * FROM quack_active_connections()
#         [state] => active
#         [query_started_at] => 2026-11-17 02:22:16.402055
```

### License

MIT License
