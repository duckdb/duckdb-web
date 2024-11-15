---
layout: docu
title: Dart API
github_repository: https://github.com/TigerEyeLabs/duckdb-dart
---

DuckDB.dart is the native Dart API for [DuckDB](https://duckdb.org/).

## Installation

DuckDB.dart can be installed from [pub.dev](https://pub.dev/packages/dart_duckdb). Please see the [API Reference](https://pub.dev/documentation/dart_duckdb/latest/) for details.

### Use This Package as a Library

#### Depend on It

Run this command:

With Flutter:

```bash
flutter pub add dart_duckdb
```

This will add a line like this to your package's `pubspec.yaml` (and run an implicit `flutter pub get`):

```text
dependencies:
  dart_duckdb: ^1.1.3
```

Alternatively, your editor might support `flutter pub get.` Check the docs for your editor to learn more.

#### Import It

Now in your Dart code, you can use:

`import 'package:dart_duckdb/dart_duckdb.dart';`

## Usage Examples

Here are some common use cases for DuckDB.Dart:

### Querying an In-Memory Database

```dart
import 'package:dart_duckdb/dart_duckdb.dart';

void main() {
  final db = duckdb.open(":memory:");
  final connection = db.connect();

  connection.execute('''
    CREATE TABLE users (id INTEGER, name VARCHAR, age INTEGER);
    INSERT INTO users VALUES (1, 'Alice', 30), (2, 'Bob', 25);
  ''');

  final result = connection.query("SELECT * FROM users WHERE age > 28").fetchAll();

  for (final row in result) {
    print(row);
  }

  connection.close();
  db.close();
}
```

### Queries on Background Isolates

```dart
import 'package:dart_duckdb/dart_duckdb.dart';

void main() {
  final db = duckdb.open(":memory:");
  final connection = db.connect();

  await Isolate.spawn(backgroundTask, db.transferrable);

  connection.close();
  db.close();
}

void backgroundTask(TransferableDatabase transferableDb) {
  final connection = duckdb.connectWithTransferred(transferableDb);
  // Access database ...
  // fetch is needed to send the data back to the main isolate
}
```
