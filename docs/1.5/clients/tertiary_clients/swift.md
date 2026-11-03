---
github_repository: https://github.com/duckdb/duckdb-swift
layout: docu
title: Swift Client
---

DuckDB has a Swift client. See the [announcement post]({% post_url 2023-04-21-swift %}) for details.

## Instantiating DuckDB

DuckDB supports both in-memory and persistent databases.
To work with an in-memory database, run:

```swift
let database = try Database(store: .inMemory)
```

To work with a persistent database, run:

```swift
let database = try Database(store: .file(at: "test.db"))
```

Queries can be issued through a database connection.

```swift
let connection = try database.connect()
```

DuckDB supports multiple connections per database.

## Application Example

The rest of the page is based on the example of our [announcement post]({% post_url 2023-04-21-swift %}), which uses raw data from [NASA's Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu) loaded directly into DuckDB.

### Creating an Application-Specific Type

We first create an application-specific type that we'll use to house our database and connection and through which we'll eventually define our app-specific queries.

```swift
import DuckDB

final class ExoplanetStore {

  let database: Database
  let connection: Connection

  init(database: Database, connection: Connection) {
    self.database = database
    self.connection = connection
  }
}
```

### Loading a CSV File

We load the data from [NASA's Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu):

```text
wget https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+pl_name+,+disc_year+from+pscomppars&format=csv -O downloaded_exoplanets.csv
```

Once we have our CSV downloaded locally, we can use the following SQL command to load it as a new table to DuckDB:

```sql
CREATE TABLE exoplanets AS
    SELECT * FROM read_csv('downloaded_exoplanets.csv');
```

Let's package this up as a new asynchronous factory method on our `ExoplanetStore` type:

```swift
import DuckDB
import Foundation

final class ExoplanetStore {

  // Factory method to create and prepare a new ExoplanetStore
  static func create() async throws -> ExoplanetStore {

  // Create our database and connection as described above
    let database = try Database(store: .inMemory)
    let connection = try database.connect()

  // Download the CSV from the exoplanet archive
  let (csvFileURL, _) = try await URLSession.shared.download(
    from: URL(string: "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+pl_name+,+disc_year+from+pscomppars&format=csv")!)

  // Issue our first query to DuckDB
  try connection.execute("""
      CREATE TABLE exoplanets AS
          SELECT * FROM read_csv('\(csvFileURL.path)');
  """)

  // Create our pre-populated ExoplanetStore instance
    return ExoplanetStore(
    database: database,
      connection: connection
  )
  }

  // Let's make the initializer we defined previously
  // private. This prevents anyone accidentally instantiating
  // the store without having pre-loaded our Exoplanet CSV
  // into the database
  private init(database: Database, connection: Connection) {
  ...
  }
}
```

### Querying the Database

The following example queries DuckDB from within Swift via an async function. This means the callee won't be blocked while the query is executing. We'll then cast the result columns to Swift native types using DuckDB's `ResultSet` `cast(to:)` family of methods, before finally wrapping them up in a `DataFrame` from the TabularData framework.

```swift
...

import TabularData

extension ExoplanetStore {

  // Retrieves the number of exoplanets discovered by year
  func groupedByDiscoveryYear() async throws -> DataFrame {

  // Issue the query we described above
    let result = try connection.query("""
      SELECT disc_year, count(disc_year) AS Count
        FROM exoplanets
        GROUP BY disc_year
        ORDER BY disc_year
      """)

    // Cast our DuckDB columns to their native Swift
    // equivalent types
    let discoveryYearColumn = result[0].cast(to: Int.self)
    let countColumn = result[1].cast(to: Int.self)

    // Use our DuckDB columns to instantiate TabularData
    // columns and populate a TabularData DataFrame
    return DataFrame(columns: [
      TabularData.Column(discoveryYearColumn).eraseToAnyColumn(),
      TabularData.Column(countColumn).eraseToAnyColumn(),
    ])
  }
}
```

### Complete Project

For the complete example project, clone the [DuckDB Swift repository](https://github.com/duckdb/duckdb-swift) and open up the runnable app project located in [`Examples/SwiftUI/ExoplanetExplorer.xcodeproj`](https://github.com/duckdb/duckdb-swift/tree/main/Examples/SwiftUI/ExoplanetExplorer.xcodeproj).
