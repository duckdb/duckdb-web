---
layout: docu
redirect_from:
- /docs/current/resources/resource_type_example
- /docs/lts/resources/resource_type_example
- /docs/preview/resources/resource_type_example
- /docs/stable/resources/resource_type_example
title: "Example: Scratch Databases for CI Runs"
---

<!-- ref: duckdb/duckdb#23731 duckdb/duckdb-web#7003 duckdb/duckdb#23736 duckdb/duckdb-web#7004 -->

This page shows the whole interface of [external resources]({% link docs/2.0/resources/overview.md %}) with one external resource type, `scratch_database`, defined in SQL. Its provider is a database service that is simulated in SQL as well, so the example runs in a single DuckDB session without any extension or remote service.

The scenario is a CI pipeline that needs a database of its own for each test run. The database is provisioned at the database service before the tests start, used by the tests, and torn down afterwards. A database left behind by a run that crashed stays at the service until it is found and torn down.

## Roles

| Role | In this example | Real or simulated |
|:--|:--|:--|
| Provider | the database service | simulated: macros that keep the service's records in the DuckDB log |
| Underlying resource | one scratch database at the service | simulated: a `create` entry in the service's records, not followed by a `delete` entry |
| External resource type | `scratch_database` | real |
| Lifecycle callbacks | `scratch_db_create`, `scratch_db_status`, `scratch_db_destroy`, `scratch_db_list` | real: they call the simulated service as they would call a real one |
| Handle | `{'id': '1'}`, the service's id for a database | real |
| Endpoint | `:memory:` | real: an in-memory DuckDB database |
| Resource registration | `ci_run_1` | real |

## The Simulated Database Service

A real database service keeps its databases and their state on its own side, and lifecycle callbacks reach it through its API, typically through the functions of an extension. The simulated service keeps its records as entries in the DuckDB log, with the log type `ExampleSimulatedProvider`. Its operations that create and delete a database write an entry with `write_log`; its operations that report on databases read the entries back with `duckdb_logs()`. The log is used because a table macro cannot run `INSERT` or `DELETE`, while it can call `write_log`, which is a scalar function. Like the resource registrations, the service's records end with the DuckDB instance.

The log also holds the evidence of what DuckDB does: DuckDB writes an entry with the log type `ExternalResource` for each lifecycle callback it calls.

## Part 1: The Database Service

This part is not part of the external resources feature: it stands in for the database service.

```sql
-- The simulated service keeps its records in the DuckDB log, next to the
-- ExternalResource entries that DuckDB writes for each lifecycle callback.
CALL enable_logging(level := 'info', storage := 'memory');

-- The service's id generator for new databases.
CREATE SEQUENCE database_ids;

-- Service operation: create a database. Returns the service's id for it.
-- A real service would start a database here.
CREATE MACRO service_create_database(
    requested_name  -- VARCHAR: the name the caller asks for, without spaces
) AS TABLE
    WITH new_database AS (
        SELECT nextval('database_ids')::VARCHAR AS id
    )
    SELECT write_log(
        'create ' || id || ' ' || requested_name,
        log_type := 'ExampleSimulatedProvider',
        level := 'info',
        return_value := id  -- the id is the result, so the log entry is always written
    ) AS id
    FROM new_database;

-- Service operation: delete a database. Returns its id.
-- A real service would stop and remove the database here.
CREATE MACRO service_delete_database(
    database_id  -- VARCHAR: the id the service returned when it created the database
) AS write_log(
    'delete ' || database_id,
    log_type := 'ExampleSimulatedProvider',
    level := 'info',
    return_value := database_id
);

-- The service's records: one row per create or delete.
CREATE MACRO service_events() AS TABLE
    SELECT
        split_part(message, ' ', 1) AS op,
        split_part(message, ' ', 2) AS id,
        split_part(message, ' ', 3) AS name,
        timestamp
    FROM duckdb_logs()
    WHERE type = 'ExampleSimulatedProvider';

-- The databases the service holds: created, and not deleted since.
CREATE MACRO service_databases() AS TABLE
    WITH created AS (
        SELECT id, name, timestamp AS created_at
        FROM service_events()
        WHERE op = 'create'
    ),
    deleted AS (
        SELECT id
        FROM service_events()
        WHERE op = 'delete'
    )
    SELECT id, name, created_at
    FROM created
    WHERE id NOT IN (SELECT id FROM deleted);

-- Service operation: the state of one database, in the service's own terms.
-- Mimics a service that needs time to start a database: a new database is
-- 'starting' for 2 seconds, then 'running'. A database that the service does
-- not hold is 'deleted'.
CREATE MACRO service_database_state(
    database_id  -- VARCHAR: the id the service returned when it created the database
) AS TABLE
    WITH database AS (
        SELECT created_at
        FROM service_databases()
        WHERE id = database_id
    )
    SELECT CASE
        WHEN NOT EXISTS (FROM database) THEN 'deleted'
        WHEN get_current_timestamp() - (SELECT created_at FROM database) < INTERVAL 2 SECOND THEN 'starting'
        ELSE 'running'
    END AS state;
```

## Part 2: The Lifecycle Callbacks

The lifecycle callbacks are the code that an integration writes for a provider. DuckDB calls them on an internal connection of its own, so they cannot be `TEMP` macros. Each lifecycle callback calls the service and translates between the service's terms and the ones DuckDB expects. The names of the columns they return are required by their contract.

```sql
-- Create callback.
-- Called by: CREATE EXTERNAL RESOURCE, once, to provision an underlying resource.
-- Result (contract): one row with the column handle, a MAP(VARCHAR, VARCHAR)
-- that is not NULL. DuckDB stores the handle with the resource registration and
-- passes it to the other lifecycle callbacks unchanged, without reading it.
CREATE MACRO scratch_db_create(
    params  -- MAP(VARCHAR, VARCHAR): the options of CREATE EXTERNAL RESOURCE, with
            -- the option names in lowercase: (NAME 'ci_run_1') is {'name': 'ci_run_1'}
) AS TABLE
    SELECT MAP {'id': id} AS handle  -- the service's id identifies the database
    FROM service_create_database(map_extract_value(params, 'name'));

-- Status callback.
-- Called by: CREATE EXTERNAL RESOURCE after the create callback, and
-- REGISTER EXTERNAL RESOURCE, repeatedly, until state is 'ready' or 'failed';
-- ATTACH TO EXTERNAL RESOURCE, once, for the endpoint to attach.
-- Result (contract): one row with the columns
--   state   VARCHAR: 'ready' or 'failed'; any other value makes DuckDB call the
--           status callback again after its poll interval
--   result  MAP(VARCHAR, VARCHAR): for an external resource type of kind
--           'catalog', the endpoint: the keys uri and attached_db_type
CREATE MACRO scratch_db_status(
    handle  -- MAP(VARCHAR, VARCHAR): the handle that the create callback returned
) AS TABLE
    SELECT
        -- The service's state, translated into the values DuckDB expects.
        CASE state
            WHEN 'starting' THEN 'pending'
            WHEN 'running'  THEN 'ready'
            ELSE 'failed'
        END AS state,
        -- A real service would return the connection string of its database.
        MAP {'uri': ':memory:', 'attached_db_type': 'duckdb'} AS result
    FROM service_database_state(map_extract_value(handle, 'id'));

-- Destroy callback.
-- Called by: DESTROY EXTERNAL RESOURCE, to tear down the underlying resource;
-- and by DuckDB itself when provisioning fails after the create callback.
-- Result (contract): DuckDB reads no column. An error means that the teardown
-- failed.
CREATE MACRO scratch_db_destroy(
    handle  -- MAP(VARCHAR, VARCHAR): the handle that the create callback returned
) AS TABLE
    SELECT service_delete_database(map_extract_value(handle, 'id')) AS deleted_id;

-- List callback.
-- Called by: SHOW ALL EXTERNAL RESOURCES, to list the underlying resources
-- that the service holds, including those without a resource registration.
-- Result (contract): one row per underlying resource, with the columns
--   handle     MAP(VARCHAR, VARCHAR): the handle, as the create callback returns it
--   name       VARCHAR: the service's name for the underlying resource
--   reference  VARCHAR: the service's reference for the underlying resource
--   state      VARCHAR: the service's state for the underlying resource, shown as is
CREATE MACRO scratch_db_list(
    params  -- MAP(VARCHAR, VARCHAR): DuckDB passes an empty map
) AS TABLE
    SELECT
        MAP {'id': databases.id} AS handle,
        databases.name AS name,
        'database-' || databases.id AS reference,
        database_state.state AS state
    FROM service_databases() AS databases,
         service_database_state(databases.id) AS database_state;
```

## Part 3: Registering the External Resource Type

```sql
CALL register_external_resource_type(
    'scratch_database',
    kind := 'catalog',  -- the status callback must return an endpoint
    create_function := 'scratch_db_create',
    status_function := 'scratch_db_status',
    destroy_function := 'scratch_db_destroy',
    list_function := 'scratch_db_list'
);
```

## Part 4: A Pipeline Run

`CREATE EXTERNAL RESOURCE` calls the create callback, which has the service create a database and returns the service's id as the handle. DuckDB then calls the status callback until it reports `ready`, and creates the resource registration `ci_run_1`. The service reports a new database as `starting` for 2 seconds, and DuckDB calls the status callback again after its poll interval of 5 seconds, so the statement takes about 5 seconds:

```sql
CREATE EXTERNAL RESOURCE scratch_database AS ci_run_1 (NAME 'ci_run_1');
SELECT name, type, handle, uri FROM (SHOW EXTERNAL RESOURCES);
```

| name | type | handle | uri |
|---|---|---|---|
| ci_run_1 | scratch_database | {id=1} | :memory: |

`ATTACH TO EXTERNAL RESOURCE` calls the status callback again and attaches the endpoint that it reports:

```sql
ATTACH TO EXTERNAL RESOURCE ci_run_1 AS ci;
SHOW DATABASES;
```

| database_name |
|---|
| ci |
| memory |

The tests use the attached database:

```sql
CREATE TABLE ci.results AS SELECT 42 AS answer;
SELECT * FROM ci.results;
```

| answer |
|---|
| 42 |

`DESTROY EXTERNAL RESOURCE` calls the destroy callback, removes the resource registration, and detaches `ci`:

```sql
DESTROY EXTERNAL RESOURCE ci_run_1;
SHOW DATABASES;
```

| database_name |
|---|
| memory |

The service's records show the database being created and deleted:

```sql
SELECT op, id, name FROM service_events() ORDER BY timestamp;
```

| op | id | name |
|---|---|---|
| create | 1 | ci_run_1 |
| delete | 1 | |

The `ExternalResource` entries show the lifecycle callbacks that DuckDB called. The first two status calls are from `CREATE EXTERNAL RESOURCE`, the third from `ATTACH TO EXTERNAL RESOURCE`:

```sql
SELECT operation, map_extract_value(extra_info, 'state') AS state
FROM duckdb_logs_parsed('ExternalResource')
ORDER BY timestamp;
```

| operation | state |
|---|---|
| create | NULL |
| status | pending |
| status | ready |
| status | ready |
| destroy | NULL |

## Part 5: When Things Go Wrong

### A Database Left Behind

A run that crashes after the service has created its database leaves that database at the service, without a resource registration. `SHOW ALL EXTERNAL RESOURCES` calls the list callback, and shows such a database with `managed` set to `false`:

```sql
CREATE EXTERNAL RESOURCE scratch_database AS ci_run_2 (NAME 'ci_run_2');
-- Simulates a run that crashed: the service created a database,
-- but no resource registration was created for it.
SELECT id AS leftover_id FROM service_create_database('ci_run_crashed');
SELECT name, managed, reference, state FROM (SHOW ALL EXTERNAL RESOURCES) ORDER BY name;
```

| name | managed | reference | state |
|---|---|---|---|
| ci_run_2 | true | NULL | NULL |
| ci_run_crashed | false | database-3 | starting |

The state `starting` is the service's own: the list callback reports it as is. To tear the database down, `REGISTER EXTERNAL RESOURCE` creates a resource registration from its handle, and `DESTROY EXTERNAL RESOURCE` tears it down:

```sql
REGISTER EXTERNAL RESOURCE scratch_database AS ci_run_crashed FROM MAP {'id': '3'};
DESTROY EXTERNAL RESOURCE ci_run_crashed;
DESTROY EXTERNAL RESOURCE ci_run_2;
SELECT count(*) AS databases_at_service FROM service_databases();
```

| databases_at_service |
|---|
| 0 |

### A Database Deleted Outside DuckDB

A resource registration does not change when its underlying resource does. After the service has deleted the database, `SHOW EXTERNAL RESOURCES` still lists `ci_run_3`:

```sql
CREATE EXTERNAL RESOURCE scratch_database AS ci_run_3 (NAME 'ci_run_3');
-- Simulates the database being deleted at the service, outside DuckDB.
SELECT service_delete_database('4') AS deleted_id;
SELECT name FROM (SHOW EXTERNAL RESOURCES);
```

| name |
|---|
| ci_run_3 |

The next `ATTACH TO EXTERNAL RESOURCE` calls the status callback, which reports `failed`:

```sql
ATTACH TO EXTERNAL RESOURCE ci_run_3 AS ci;
```

```console
IO Error: EXTERNAL RESOURCE: provisioning 'scratch_database' failed: IO Error: create_external_resource: resource "scratch_database" reported state 'failed'
```

The resource registration `ci_run_3` is still listed after the error.

### A Service That Is Too Slow

The `create_external_resource` function takes a `timeout_seconds` and a `poll_interval_seconds`; the statements take neither. When the status callback still reports `pending` at the timeout, the function fails, and DuckDB tears down the underlying resource that it provisioned:

```sql
SELECT handle
FROM create_external_resource(
    'scratch_database',
    params := MAP {'name': 'ci_run_4'},
    timeout_seconds := 1,
    poll_interval_seconds := 1
);
```

```console
IO Error: create_external_resource: timed out awaiting readiness for "scratch_database" (last state 'pending')
```

The service's records show that the database was created and deleted again:

```sql
SELECT op, id, name FROM service_events() WHERE id = '5' ORDER BY timestamp;
```

| op | id | name |
|---|---|---|
| create | 5 | ci_run_4 |
| delete | 5 | |
