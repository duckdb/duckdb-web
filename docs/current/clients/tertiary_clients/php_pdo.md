---
github_repository: https://github.com/thomas-0816/pdo-duckdb-php
layout: docu
redirect_from:
title: PHP Client (PDO)
---

> The PHP DuckDB PDO extension is a tertiary client and is maintained by a third-party.
>
> To use `pdo_duckdb`, follow the [instructions below](#installation).
>
> The latest version of `pdo_duckdb` supports DuckDB {{ site.current_duckdb_php_version }}.

`pdo_duckdb` is a native DuckDB database driver for the [PHP Data Objects (PDO)](https://www.php.net/manual/en/book.pdo.php) interface.

Any application or framework compatible with PDO can directly use `pdo_duckdb`.\
It is thread safe and fully tested with FrankenPHP (PHP-ZTS).

As a native PHP extension, it is implemented in C/C++ and does not require PHP FFI or preloading.\
The [release packages](https://github.com/thomas-0816/pdo-duckdb-php/releases/latest) contain pre-compiled binaries for all supported platforms and DuckDB is directly included.\
DuckDB extensions work the same way as they do in DuckDB CLI.

Supported PHP versions: [8.2 or newer](https://www.php.net/supported-versions.php)

Operating systems: Ubuntu 24+, Debian 12+, Fedora 42+, openSUSE 16+, AmazonLinux 2023+, Wolfi OS, Windows Server 2022+ (x64), macOS 14+ (arm64)

All DuckDB types are supported:\
Text, Numeric, Date, Time, Interval, JSON, Array, Struct, Map, List, Enum, Variant, Geometry, Union, Bitstring, Blob and Boolean

GitHub: [pdo-duckdb-php](https://github.com/thomas-0816/pdo-duckdb-php)

Packagist: [pdo-duckdb-php](https://packagist.org/packages/thomas-0816/pdo-duckdb-php)

## Installation

`pdo_duckdb` is fully compatible with the PHP Installer for Extensions ([PIE](https://github.com/php/pie)) and can be installed with:


```bash
pie install thomas-0816/pdo-duckdb-php
```

Testing:

```php
php -m | grep duckdb
php -r 'print_r((new PDO("duckdb::memory:"))->query("SELECT 42 as n")->fetch(PDO::FETCH_ASSOC));'

# Array
# (
#     [n] => 42
# )
```

## Examples

### Basic usage

```php
<?php

$duckDb = new PDO('duckdb::memory:');
$duckDb->exec('CREATE TABLE table1 (id INTEGER, amount DECIMAL(10, 2), description VARCHAR)');

$statement = $duckDb->prepare('INSERT INTO table1 VALUES (?, ?, ?)');
$statement->execute([1, 42.21, 'Hello DuckDB! 🐘 💓 🦆']);

$statement = $duckDb->query('SELECT * FROM table1');
print_r($statement->fetchAll(PDO::FETCH_ASSOC));

# Array
# (
#     [0] => Array
#         (
#             [id] => 1
#             [amount] => 42.21
#             [description] => Hello DuckDB! 🐘 💓 🦆
#         )
# )
```

### Open databases from disk or in-memory

```php
<?php

$db = new PDO('duckdb::memory:'); // open in-memory database

$db = new PDO('duckdb:/tmp/test.db'); // open database file from disk

// open database file as read-only
$db = new PDO('duckdb:/tmp/test.db', null, null, [PDO::DUCKDB_ATTR_CONFIG => ['access_mode' => 'read_only']]);
```

### Read and write Parquet files

```php
<?php

$db = new PDO('duckdb::memory:');
$db->exec('CREATE TABLE table1 (id INTEGER, text VARCHAR USING COMPRESSION zstd, data JSON)');

$statement = $db->prepare('INSERT INTO table1 VALUES (?, ?, ?)');
$statement->execute([1, 'Hello DuckDB 🦆', ['foo' => 'bar', 'baz' => 42]]);

$db->exec("COPY (SELECT * FROM table1) TO '/tmp/table1.parquet' (COMPRESSION zstd)");

foreach ($db->query("SELECT * FROM '/tmp/table1.parquet'", PDO::FETCH_ASSOC) as $row) {
    print_r($row);
}

# Array
# (
#     [id] => 1
#     [text] => Hello DuckDB 🦆
#     [data] => Array
#         (
#             [foo] => bar
#             [baz] => 42
#         )
# )
```

### Read CSV files

```php
<?php

$list = [
    ['aaa', 'bbb', 'ccc'],
    ['123', '456', '789'],
    ['aaa', 'bbb', 'ccc']
];
$fp = fopen('/tmp/test.csv', 'w');
foreach ($list as $fields) {
    fputcsv($fp, $fields, ',', '"', '');
}
fclose($fp);

$db = new PDO('duckdb::memory:');
$statement = $db->query("SELECT * FROM '/tmp/test.csv'");
print_r($statement->fetchAll(PDO::FETCH_ASSOC));

# Array
# (
#     [0] => Array
#         (
#             [aaa] => 123
#             [bbb] => 456
#             [ccc] => 789
#         )
#     [1] => Array
#         (
#             [aaa] => aaa
#             [bbb] => bbb
#             [ccc] => ccc
#         )
# )
```

### Read JSON files

```php
<?php

file_put_contents('/tmp/logs.json', json_encode(['log' => 'log text']) . PHP_EOL, FILE_APPEND);
file_put_contents('/tmp/logs.json', json_encode(['log' => 'log text 2']) . PHP_EOL, FILE_APPEND);

$db = new PDO('duckdb::memory:');
$statement = $db->query("SELECT * FROM '/tmp/logs.json'");
print_r($statement->fetchAll(PDO::FETCH_ASSOC));

# Array
# (
#     [0] => Array
#         (
#             [log] => log text
#         )
#     [1] => Array
#         (
#             [log] => log text 2
#         )
# )

$db->exec("COPY (SELECT * FROM '/tmp/logs.json') TO '/tmp/logs_json.parquet' (COMPRESSION zstd)");
```

### Use structured columns with a fixed schema

```php
<?php

# s is array{v: string, i: int, a: string[], d: float}

$db = new PDO('duckdb::memory:');
$db->exec('CREATE TABLE table1 (s STRUCT(v VARCHAR, i INTEGER, a VARCHAR[], d DECIMAL))');

$statement = $db->prepare('INSERT INTO table1 VALUES (?)');
$statement->execute([['v' => 'foo', 'i' => 21, 'a' => ['b', 'c'], 'd' => 42.21]]);

$statement = $db->query('SELECT * FROM table1');
print_r($statement->fetch(PDO::FETCH_ASSOC));

# Array
# (
#     [s] => Array
#         (
#             [v] => foo
#             [i] => 21
#             [a] => Array
#                 (
#                     [0] => b
#                     [1] => c
#                 )
#             [d] => 42.21
#         )
# )
```

### Auto increment columns

```php
<?php

$db = new PDO('duckdb::memory:');
$db->exec('CREATE SEQUENCE table1_id');
$db->exec("CREATE TABLE table1 (id INTEGER PRIMARY KEY DEFAULT nextval('table1_id'))");
$statement = $db->query('INSERT INTO table1 VALUES (default) RETURNING *');
print_r($statement->fetch(PDO::FETCH_ASSOC));

# Array
# (
#     [id] => 1
# )
```
