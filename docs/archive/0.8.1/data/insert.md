---
layout: docu
title: Insert Statements
---

Insert statements are the standard way of loading data into a relational database. When using insert statements, the values are supplied row-by-row. While simple, there is significant overhead involved in parsing and processing individual insert statements. This makes lots of individual row-by-row insertions very inefficient for bulk insertion.
  
> As a rule-of-thumb, avoid using lots of individual row-by-row insert statements when inserting more than a few rows (i.e. avoid using insert statements as part of a loop). When bulk inserting data, try to maximize the amount of data that is inserted per statement.

If you must use insert statements to load data in a loop, avoid executing the statements in auto-commit mode. After every commit, the database is required to sync the changes made to disk to ensure no data is lost. In auto-commit mode every single statement will be wrapped in a separate transaction, meaning `fsync` will be called for every statement. This is typically unnecessary when bulk loading and will significantly slow down your program.
 
> If you absolutely must use insert statements in a loop to load data, wrap them in calls to `BEGIN TRANSACTION` and `COMMIT`.

## Syntax
An example of using `INSERT INTO` to load data in a table is as follows:

```sql
CREATE TABLE people(id INTEGER, name VARCHAR);
INSERT INTO people VALUES (1, 'Mark'), (2, 'Hannes');
```

A more detailed description together with syntax diagram can be found [here](../sql/statements/insert).
