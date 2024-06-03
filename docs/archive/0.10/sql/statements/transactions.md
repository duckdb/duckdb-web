---
layout: docu
title: Transaction Management
---

DuckDB supports [ACID database transactions](https://en.wikipedia.org/wiki/Database_transaction).
Transactions provide isolation, i.e., changes made by a transaction are not visible from concurrent transactions until it is committed.
A transaction can also be aborted, which discards any changes it made so far.

## Statements

DuckDB provides the following statements for transaction management.

### Starting a Transaction

To start a transaction, run:

```sql
BEGIN TRANSACTION;
```

### Committing a Transaction

You can commit a transaction to make it visible to other transactions and to write it to persistent storage (if using DuckDB in persistent mode).
To commit a transaction, run:

```sql
COMMIT;
```

If you are not in an active transaction, the `COMMIT` statement will fail.

### Rolling Back a Transaction

You can abort a transaction.
This operation, also known as rolling back, will discard any changes the transaction made to the database.
To abort a transaction, run:

```sql
ROLLBACK;
```

You can also use the abort command, which has an identical behavior:

```sql
ABORT;
```

If you are not in an active transaction, the `ROLLBACK` and `ABORT` statements will fail.

### Example

We illustrate the use of transactions through a simple example.

```sql
CREATE TABLE person (name VARCHAR, age BIGINT);

BEGIN TRANSACTION;
INSERT INTO person VALUES ('Ada', 52);
COMMIT;

BEGIN TRANSACTION;
DELETE FROM person WHERE name = 'Ada';
INSERT INTO person VALUES ('Bruce', 39);
ROLLBACK;

SELECT * FROM person;
```

The first transaction (inserting "Ada") was committed but the second (deleting "Ada" and inserting "Bruce") was aborted.
Therefore, the resulting table will only contain `<'Ada', 52>`.