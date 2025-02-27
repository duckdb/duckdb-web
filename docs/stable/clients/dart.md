---
layout: docu
title: Dart Client
github_repository: https://github.com/TigerEyeLabs/duckdb-dart
redirect_from:
  - /docs/api/dart
  - /docs/api/dart/
---

DuckDB.Dart is the native Dart API for [DuckDB](https://duckdb.org/).

## Installation

DuckDB.Dart can be installed from [pub.dev](https://pub.dev/packages/dart_duckdb). Please see the [API Reference](https://pub.dev/documentation/dart_duckdb/latest/) for details.

### Use This Package as a Library

#### Depend on It

Add the dependency with Flutter:

```bash
flutter pub add dart_duckdb
```

This will add a line like this to your package's `pubspec.yaml` (and run an implicit `flutter pub get`):

```yaml
dependencies:
  dart_duckdb: ^1.1.3
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

void main() {
  final db = duckdb.open(":memory:");
  final connection = duckdb.connect(db);

  connection.execute('''
    CREATE TABLE users (id INTEGER, name VARCHAR, age INTEGER);
    INSERT INTO users VALUES (1, 'Alice', 30), (2, 'Bob', 25);
  ''');

  final result = connection.query("SELECT * FROM users WHERE age > 28").fetchAll();

  for (final row in result) {
    print(row);
  }

  connection.dispose();
  db.dispose();
}
```

### Queries on Background Isolates

```dart
import 'package:dart_duckdb/dart_duckdb.dart';

void main() {
  final db = duckdb.open(":memory:");
  final connection = duckdb.connect(db);

  await Isolate.spawn(backgroundTask, db.transferrable);

  connection.dispose();
  db.dispose();
}

void backgroundTask(TransferableDatabase transferableDb) {
  final connection = duckdb.connectWithTransferred(transferableDb);
  // Access database ...
  // fetch is needed to send the data back to the main isolate
}
```
