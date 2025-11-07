---
layout: post
title: "Efficient Data Upserts with DuckDB: The Power of MERGE Explained"
author: "Ian Fogelman"
thumb: "/images/blog/thumbs/duckdb-merge.svg"
image: "/images/blog/thumbs/duckdb-merge.png"
excerpt: "You can now use the MERGE statement in DuckDB. In this post, we show you how."
---

In version 1.4.0 of DuckDB released support for the `MERGE` statement. The `MERGE` statement allows you to insert, update, or delete records from a source (incoming) table into a target (master) table. The `MERGE` statement is also commonly referred to as an `UPSERT`, meaning that if there is a matching primary key in the target table you can optionally update it, and if not you can insert a new record. 

# Use Case

The `MERGE` statement is useful for building type 2 [slowly changing dimensions](https://en.wikipedia.org/wiki/Slowly_changing_dimension), which can help represent a tables primary key changes over time. With additional date columns, you can determine when changes happened to a record, for how long those changes affected the primary key, and easily determine what the current state of the primary key is.

The `MERGE` statement is useful for data warehousing OLTP databases, a few common use cases include: 

 - Slowly Changing Dimensions Type 2 (SCD Type 2), type 2 SCDs tracks full history by expiring old records with begin dates, end dates and is_current flags, enabling audit trails without hard deletes.

 - Reduce code complexity, using a known SQL syntax such as `MERGE` is easiest to understand and to code in SQL than alternative in raw Python or an in-memory framework such as Pandas. 

 - Building out your OLTP data warehouse, `MERGE` is great for doing the heavy lifting for transaction data and getting analytical value.

When using `MERGE` you choose the specified clauses, what exactly happens to the records. It's important to note that the Id field you choose must be a primary key and guarantee uniqueness. If your records are not completely unique for your incoming and master data sets, `MERGE` will not work.

# Workflow Diagram

The following diagram shows a visual representation of the SQL `MERGE` flow:

<img src="{% link images/blog/merge/sql-merge-statement-workflow.png %}" width="800" />

# Terminology

When working with the `MERGE` statement it is important to understand the keywords that are unique to the statement.

| Term                        | Definition |
|-----------------------------|------------|
| **MERGE INTO**              | The clause that specifies the target table into which data will be merged. It identifies the table that will receive inserts, updates, or deletes based on the merge logic. In this blog this will also be refered to as the master table. |
| **USING**                   | The clause that specifies the source table, view, or subquery providing the data to be merged into the target table. In this blog this will be refered to as the incoming table. |
| **WHEN MATCHED**            | The clause that defines actions (typically `UPDATE` or `DELETE`) to take when a row in the source matches a row in the target based on the `ON` condition. |
| **WHEN NOT MATCHED**        | The clause that defines actions (typically `INSERT`) to take when a row in the source does not match any row in the target based on the `ON` condition. |
| **RETURNING merge_action** | This optional clause returns the action performed (`INSERT`, `UPDATE`, or `DELETE`) along with the affected row data for each row processed in the merge. |
| **Source / Target**         | **Source** (incoming): The dataset (table, view, or query) providing incoming data.<br>**Target** (master): The existing table being modified by the merge operation. |

> Note: `WHEN MATCHED` and `WHEN NOT MATCHED` can specify either `SOURCE` or `TARGET` and you can specify logic for either.

# Example

Alright, now that we have the formal definitions out of the way, lets get on with a real world example of using DuckDB's `MERGE`.

First we must create an example incoming data table. You can think of this table as a transactional table that you want to start tracking history for.
And of course, in keeping with the DuckDB tradition ([all major LTS releases are named after breeds of ducks](https://duckdb.org/release_calendar#lts-releases)) we will be using duck data!

> DuckDB has a frontend notebook UI, this is great for managing several SQL statements and segmenting your code.
> The UI ships with the DuckDB CLI, so if you have the CLI installed you can use the front end.
> To start the notebook front end just run: `duckdb -ui` and you can navigate to [http://localhost:4213/](http://localhost:4213/) to start writing your SQL code inside of your notebooks.

Create the source `incoming_ducks` table:

```sql
CREATE TABLE IF NOT EXISTS incoming_ducks (
    duck_id INTEGER,
    duck_name VARCHAR,
    breed VARCHAR,
    location VARCHAR,
    begin_date DATE,
    end_date DATE,
    is_current BOOLEAN
);
```

Insert data into the `incoming_ducks` table:

```sql
INSERT INTO incoming_ducks VALUES
    (101, 'Quackers', 'Mallard', 'Pond B', current_date - INTERVAL 1 DAY, NULL, true),
    (102, 'Waddles', 'Pekin', 'Pond A', current_date - INTERVAL 1 DAY, NULL, true),
    (104, 'Splash', 'Muscovy', 'Pond C', current_date - INTERVAL 1 DAY, NULL, true),
    (105, 'Puddles', 'Indian Runner', 'Relocated', current_date - INTERVAL 1 DAY, NULL, true);
```

Create the target `master_ducks` table:

```sql
CREATE TABLE IF NOT EXISTS master_ducks (
    record_id INTEGER PRIMARY KEY,
    duck_id INTEGER NOT NULL,
    duck_name VARCHAR,
    breed VARCHAR,
    location VARCHAR,
    begin_date DATE NOT NULL,
    end_date DATE,
    is_current BOOLEAN NOT NULL DEFAULT true
);
```

Insert data into the `master_ducks` table:

```sql
-- Create sequence for primary key
CREATE SEQUENCE IF NOT EXISTS duck_record_seq START 1;

-- Insert  master data
INSERT INTO master_ducks VALUES
    (nextval('duck_record_seq'), 101, 'Quackers', 'Mallard', 'Pond A', current_date - INTERVAL 2 DAY, NULL, true),
    (nextval('duck_record_seq'), 102, 'Waddles', 'Pekin', 'Pond A', current_date - INTERVAL 2 DAY, NULL, true),
    (nextval('duck_record_seq'), 103, 'Feathers', 'Rouen', 'Pond B', current_date - INTERVAL 2 DAY, NULL, true),
    (nextval('duck_record_seq'), 105, 'Puddles', 'Indian Runner', 'Pond A', current_date - INTERVAL 2 DAY, NULL, true);
```

At this point we have two tables, `incoming_ducks` and `master_ducks`. Lets examine the `MERGE` syntax in the following 
SQL statement:

```sql
MERGE INTO master_ducks
USING incoming_ducks
ON master_ducks.duck_id = incoming_ducks.duck_id AND master_ducks.is_current = true
WHEN MATCHED AND (master_ducks.duck_name <> incoming_ducks.duck_name 
                   OR master_ducks.breed <> incoming_ducks.breed 
                   OR master_ducks.location <> incoming_ducks.location) THEN 
    UPDATE SET 
        end_date = current_date - INTERVAL 1 DAY,
        is_current = false
WHEN NOT MATCHED BY SOURCE AND master_ducks.is_current = true THEN 
    UPDATE SET 
        end_date = current_date - INTERVAL 1 DAY,
        is_current = false
WHEN NOT MATCHED BY TARGET THEN 
    INSERT (record_id, duck_id, duck_name, breed, location, begin_date, end_date, is_current)
    VALUES (nextval('duck_record_seq'), incoming_ducks.duck_id, incoming_ducks.duck_name, 
            incoming_ducks.breed, incoming_ducks.location, incoming_ducks.begin_date, 
            incoming_ducks.end_date, incoming_ducks.is_current)
RETURNING merge_action, *;
```

- `MERGE INTO` this specifies what table is being used as a `TARGET`, in this case `master_ducks`.
- `USING` this line specifies what table is being used as a `SOURCE`, in this case `incoming_ducks`.
- `ON` this line specifies the join condition of the two tables, in this case the primary key `duck_id` is matched between the two tables and only the records which are also marked as `is_current` = `true`.
- `WHEN MATCHED AND ` this line specifies the logic when data is joined between the two tables and the additional conditions. In this case if the `name`, `breed`, or `location` have changed the `UPDATE` within the `WHEN MATCHED` block will execute. This logic sets `end_date` to the current date - 1 day and the `is_current` indicator is set to `false`.
- `WHEN NOT MATCHED BY SOURCE` this line handles "soft" deletions. When a duck exists in our master table but is missing from the incoming data, we close out that record by marking it as no longer current and setting the end_date.
- `WHEN NOT MATCHED BY TARGET` this line specifies that if the incoming duck is completly new, then to insert it into the `TARGET` master table.
- `RETURNING merge_action, *` this line is optional and if provided will return all rows of affected by the `MERGE` along with the type of update that row recieved such as `INSERT` or `UPDATE`.

You may also want your expired records present in the `TARGET` master_ducks table. This will allow you to see the historical changes of each duck in a single table. In order to do this perform a post update insert, which compares both tables and grabs the expired records from the `MERGE`.

```sql
-- Insert new versions for records that were just closed
INSERT INTO master_ducks (record_id, duck_id, duck_name, breed, location, begin_date, end_date, is_current)
SELECT 
    nextval('duck_record_seq'),
    incoming_ducks.duck_id,
    incoming_ducks.duck_name,
    incoming_ducks.breed,
    incoming_ducks.location,
    current_date AS begin_date,
    incoming_ducks.end_date,
    true AS is_current
FROM incoming_ducks
INNER JOIN master_ducks 
    ON incoming_ducks.duck_id = master_ducks.duck_id
WHERE master_ducks.is_current = false
  AND master_ducks.end_date = current_date - INTERVAL '1 DAY';
```

Now let's query `master_ducks` to examine the results. Notice how both current and historical records coexist in the 
same table - this is the essence of SCD Type 2:

```sql
-- Query to see all records (current and historical)
SELECT * FROM master_ducks ORDER BY duck_id, begin_date DESC;
```

To view only the current records, run the following query:

```sql
-- Query to see only current records
SELECT * FROM master_ducks WHERE is_current = true;
```

To view only the expired historical records, run the following query:

```sql
-- Query to see expired records only
SELECT * FROM master_ducks WHERE is_current = false ORDER BY duck_id, begin_date DESC;
```

# Conclusion

DuckDB in addition to all its great existing features now also supports the `MERGE` statement. Because of DuckDB's ability to connect to so many data sources, the fact that it supports `MERGE` opens up a lot of analytical use cases. This statement is useful for building out historical views of your data. In this blog we reviewed the detailed syntax and walked through a practical example of implementing the statement with example data.



