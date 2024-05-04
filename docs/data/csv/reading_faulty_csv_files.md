---
layout: docu
title: Reading Faulty CSV Files
redirect_from:
---

Reading erroneous CSV files is possible by utilizing the `ignore_errors` option. With that option set, rows containing data that would otherwise cause the CSV Parser to generate an error will be ignored.

## Using the `ignore_errors` Option

For example, consider the following CSV file, [`faulty.csv`](/data/faulty.csv):

```csv
Pedro,31
Oogie Boogie, three
```

If you read the CSV file, specifying that the first column is a `VARCHAR` and the second column is an `INTEGER`, loading the file would fail, as the string `three` cannot be converted to an `INTEGER`.

For example, the following query will throw a casting error.

```sql
FROM read_csv('faulty.csv', columns = {'name': 'VARCHAR', 'age': 'INTEGER'});
```

However, with `ignore_errors` set, the second row of the file is skipped, outputting only the complete first row. For example:

```sql
FROM read_csv(
    'faulty.csv',
    columns = {'name': 'VARCHAR', 'age': 'INTEGER'},
    ignore_errors = true
);
```

Outputs:

<div class="narrow_table"></div>

| name  | age |
|-------|-----|
| Pedro | 31  |

One should note that the CSV Parser is affected by the projection pushdown optimization. Hence, if we were to select only the name column, both rows would be considered valid, as the casting error on the age would never occur. For example:

```sql
SELECT name
FROM read_csv('faulty.csv', columns = {'name': 'VARCHAR', 'age': 'INTEGER'});
```

Outputs:

<div class="narrow_table"></div>

|     name     |
|--------------|
|     Pedro    |
| Oogie Boogie |

## Retrieving Faulty CSV Lines

Being able to read faulty CSV files is important, but for many data cleaning operations, it is also necessary to know exactly which lines are corrupted and what errors the parser discovered on them. For scenarios like these, it is possible to use DuckDB's CSV Rejects Table feature. It is important to note that the Rejects Table can only be used when `ignore_errors` is set, and currently, only stores casting errors and does not save errors when the number of columns differ.

The CSV Rejects Table returns the following information:

<div class="narrow_table"></div>

| Column name | Description | Type |
|:--|:-----|:-|
| `file` | File path. | `VARCHAR` |
| `line` | Line number, from the CSV File, where the error occured. | `INTEGER` |
| `column` | Column number, from the CSV File, where the error occured. | `INTEGER` |
| `column_name` | Column name, from the CSV File, where the error occured. | `VARCHAR` |
| `parsed_value` | The value, where the casting error happened, in a string format. | `VARCHAR` |
| `recovery_columns` | An optional primary key of the CSV File. | `STRUCT {NAME: VALUE}` |
| `error` | Exact error encountered by the parser. | `VARCHAR` |

## Parameters

<div class="narrow_table"></div>

The parameters listed below are used in the `read_csv` function to configure the CSV Rejects Table.

| Name | Description | Type | Default |
|:--|:-----|:-|:-|
| `rejects_table` | Name of a temporary table where the information of the faulty lines of a CSV file are stored. | `VARCHAR` | (empty) |
| `rejects_limit` | Upper limit on the number of faulty records from a CSV file that will be recorded in the rejects table. 0 is used when no limit should be applied. | `BIGINT` | 0 |
| `rejects_recovery_columns` | Column values that serve as a primary key to the CSV file. The are stored in the CSV Rejects Table to help identify the faulty tuples. | `VARCHAR[]` | (empty) |

To store the information of the faulty CSV lines in a rejects table, the user must simply provide the rejects table name in the`rejects_table` option. For example:

```sql
FROM read_csv(
    'faulty.csv',
    columns = {'name': 'VARCHAR', 'age': 'INTEGER'},
    rejects_table = 'rejects_table',
    ignore_errors = true
);
```

You can then query the `rejects_table` table, to retrieve information about the rejected tuples. For example:

```sql
FROM rejects_table;
```

Outputs:

<div class="narrow_table"></div>

|    file    | line | column | column_name | parsed_value |                     error                      |
|------------|------|--------|-------------|--------------|------------------------------------------------|
| faulty.csv |  2   |    1   |     age     |     three    | Could not convert string ' three' to 'INTEGER' |


Additionally, the `name` column could also be provided as a primary key via the `rejects_recovery_columns` option to provide more information over the faulty lines. For example:

```sql
FROM read_csv(
    'faulty.csv',
    columns = {'name': 'VARCHAR', 'age': 'INTEGER'},
    rejects_table = 'rejects_table',
    rejects_recovery_columns = '[name]',
    ignore_errors = true
);
```

Reading from the `rejects_table` will return:

<div class="narrow_table"></div>

|    file    | line | column | column_name | parsed_value |     recovery_columns     |                     error                      |
|------------|------|--------|-------------|--------------|--------------------------|------------------------------------------------|
| faulty.csv |  2   |    1   |     age     |     three    | {'name': 'Oogie Boogie'} | Could not convert string ' three' to 'INTEGER' |
