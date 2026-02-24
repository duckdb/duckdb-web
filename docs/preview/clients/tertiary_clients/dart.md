---
github_repository: https://github.com/TigerEyeLabs/duckdb-dart
layout: docu
title: Dart Client
---

> The latest stable version of the DuckDB Dart client is {{ site.current_duckdb_dart_version }}.

DuckDB.Dart is the native Dart API for DuckDB.

## Installation

DuckDB.Dart can be installed from [pub.dev](https://pub.dev/packages/dart_duckdb). Please see the [API Reference](https://pub.dev/documentation/dart_duckdb/latest/) for details.

### Use This Package as a Library

#### Depend on It

Add the dependency with Flutter:

```batch
flutter pub add dart_duckdb
```

This will add a line like this to your package's `pubspec.yaml` (and run an implicit `flutter pub get`):

```yaml
dependencies:
  dart_duckdb: ^{{ site.current_duckdb_dart_version }}
```

Alternatively, your editor might support `flutter pub get`. Check the docs for your editor to learn more.

#### Import It

Now in your Dart code, you can import it:

```dart
import 'package:dart_duckdb/dart_duckdb.dart';
```

## Usage Examples

See the example projects in the [`duckdb-dart` repository](https://github.com/TigerEyeLabs/duckdb-dart/):

* [`cli`](https://github.com/TigerEyeLabs/duckdb-dart/tree/main/examples/cli): command-line application
* [`duckdbexplorer`](https://github.com/TigerEyeLabs/duckdb-dart/tree/main/examples/duckdbexplorer): GUI application which builds for desktop operating systems as well as Android and iOS.

Here are some common code snippets for DuckDB.Dart:

### Querying an In-Memory Database

```dart
import 'package:dart_duckdb/dart_duckdb.dart';

void main() async {
  final db = await duckdb.open(":memory:");
  final connection = await duckdb.connect(db);

  await connection.execute('''
    CREATE TABLE users (id INTEGER, name VARCHAR, age INTEGER);
    INSERT INTO users VALUES (1, 'Alice', 30), (2, 'Bob', 25);
  ''');

  final result = (await connection.query("SELECT * FROM users WHERE age > 28")).fetchAll();

  for (final row in result) {
    print(row);
  }

  connection.dispose();
  db.dispose();
}
```

### Using Multiple Connections

DuckDB.Dart automatically manages dedicated background isolates per connection, enabling efficient non-blocking I/O for concurrent queries. Each connection handles its own isolate internally, so you can simply create multiple connections for parallel operations:

```dart
import 'package:dart_duckdb/dart_duckdb.dart';

void main() async {
  final db = await duckdb.open(":memory:");

  // Create a table
  final con1 = await duckdb.connect(db);
  await con1.execute('''
    CREATE TABLE users (id INTEGER, name VARCHAR);
    INSERT INTO users VALUES (1, 'Alice'), (2, 'Bob');
  ''');

  // Query from multiple connections concurrently
  final con2 = await duckdb.connect(db);
  final con3 = await duckdb.connect(db);

  final future1 = con2.query("SELECT * FROM users WHERE id = 1");
  final future2 = con3.query("SELECT * FROM users WHERE id = 2");

  final result1 = (await future1).fetchAll();
  final result2 = (await future2).fetchAll();

  print(result1);
  print(result2);

  con1.dispose();
  con2.dispose();
  con3.dispose();
  db.dispose();
}
```

## Web Support

DuckDB.Dart supports web platforms through DuckDB WASM. For Flutter web builds, you need to configure the necessary JavaScript dependencies.

### Setup for Flutter Web

Add the following to `web/index.html` inside the `<head>` section to load DuckDB WASM and Apache Arrow:

```html
<script type="importmap">
  {
    "imports": {
      "apache-arrow": "https://cdn.jsdelivr.net/npm/apache-arrow@17.0.0/+esm"
    }
  }
</script>
<script type="module">
  import * as duckdb from "https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm@1.29.1-dev222.0/+esm";
  import * as arrow from "apache-arrow";
  window.duckdbWasmReady = new Promise((resolve) => {
    window.duckdbduckdbWasm = duckdb;
    window.ArrowTable = arrow.Table;
    resolve();
  });
</script>
```

### Usage in Flutter Web

Once configured, you can use DuckDB the same way as on other platforms:

```dart
import 'package:dart_duckdb/dart_duckdb.dart';

void main() async {
  final db = await duckdb.open(":memory:");
  final connection = await duckdb.connect(db);

  await connection.execute('''
    CREATE TABLE data (id INTEGER, value VARCHAR);
    INSERT INTO data VALUES (1, 'hello'), (2, 'world');
  ''');

  final result = (await connection.query("SELECT * FROM data")).fetchAll();
  for (final row in result) {
    print(row);
  }

  connection.dispose();
  db.dispose();
}
```

For more platform-specific details, see the [Building Instructions](https://github.com/TigerEyeLabs/duckdb-dart/blob/main/BUILDING.md).
