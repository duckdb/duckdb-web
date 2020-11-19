---
layout: docu
title: Create Sequence
selected: Documentation/SQL/Create Sequence
expanded: SQL
railroad: statements/createsequence.js
---
`CREATE SEQUENCE` creates a new sequence number generator.

### Examples
Create an ascending sequence called serial, starting at 101:

```sql
CREATE SEQUENCE serial START 101;
```

Select the next number from this sequence:
```sql
SELECT nextval('serial');

 nextval
---------
     101
```

Use this sequence in an `INSERT` command:

```sql
INSERT INTO distributors VALUES (nextval('serial'), 'nothing');
```

### Syntax
<div id="rrdiagram"></div>

`CREATE SEQUENCE` creates a new sequence number generator.

If a schema name is given then the sequence is created in the specified schema. Otherwise it is created in the current schema. Temporary sequences exist in a special schema, so a schema name may not be given when creating a temporary sequence. The sequence name must be distinct from the name of any other sequence in the same schema.

After a sequence is created, you use the function `nextval` to operate on the sequence.

## Parameters

| Name | Description |
|:---|:---|
| `TEMPORARY` or `TEMP` | If specified, the sequence object is created only for this session, and is automatically dropped on session exit. Existing permanent sequences with the same name are not visible (in this session) while the temporary sequence exists, unless they are referenced with schema-qualified names. |
| name | The name (optionally schema-qualified) of the sequence to be created. |
| `increment` | The optional clause `INCREMENT BY increment` specifies which value is added to the current sequence value to create a new value. A positive value will make an ascending sequence, a negative one a descending sequence. The default value is 1. |
| `minvalue` | The optional clause `MINVALUE minvalue` determines the minimum value a sequence can generate. If this clause is not supplied or `NO MINVALUE` is specified, then defaults will be used. The defaults are 1 and -(2^63 - 1) for ascending and descending sequences, respectively. |
| `maxvalue` | The optional clause `MAXVALUE maxvalue` determines the maximum value for the sequence. If this clause is not supplied or `NO MAXVALUE` is specified, then default values will be used. The defaults are 2^63 - 1 and -1 for ascending and descending sequences, respectively. |
| `start` | The optional clause `START WITH start` allows the sequence to begin anywhere. The default starting value is `minvalue` for ascending sequences and `maxvalue` for descending ones. |
| `CYCLE` or `NO CYCLE` | The `CYCLE` option allows the sequence to wrap around when the `maxvalue` or `minvalue` has been reached by an ascending or descending sequence respectively. If the limit is reached, the next number generated will be the `minvalue` or `maxvalue`, respectively. |

If `NO CYCLE` is specified, any calls to nextval after the sequence has reached its maximum value will return an error. If neither `CYCLE` or `NO CYCLE` are specified, `NO CYCLE` is the default.

> Use `DROP SEQUENCE` to remove a sequence. 
> Sequences are based on `BIGINT` arithmetic, so the range cannot exceed the range of an eight-byte integer (-9223372036854775808 to 9223372036854775807).

<!-- Update the sequence value after a `COPY FROM`:

```sql
BEGIN;
COPY distributors FROM 'input_file';
SELECT setval('serial', max(id)) FROM distributors;
END;
``` -->
