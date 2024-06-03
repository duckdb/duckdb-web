---
layout: docu
title: Full-Text Search
---

DuckDB supports full-text search via the [`fts` extension](../../extensions/full_text_search).
A full-text index allows for a query to quickly search for all occurrences of individual words within longer text strings.

## Example: Shakespeare Corpus

Here's an example of building a full-text index of Shakespeare's plays.

```sql
CREATE TABLE corpus AS
    SELECT * FROM 'https://blobs.duckdb.org/data/shakespeare.parquet';
```

```sql
DESCRIBE corpus;
```

| column_name | column_type | null | key  | default | extra |
|-------------|-------------|------|------|---------|-------|
| line_id     | VARCHAR     | YES  | NULL | NULL    | NULL  |
| play_name   | VARCHAR     | YES  | NULL | NULL    | NULL  |
| line_number | VARCHAR     | YES  | NULL | NULL    | NULL  |
| speaker     | VARCHAR     | YES  | NULL | NULL    | NULL  |
| text_entry  | VARCHAR     | YES  | NULL | NULL    | NULL  |

The text of each line is in `text_entry`, and a unique key for each line is in `line_id`.

## Creating a Full-Text Search Index

First, we create the index, specifying the table name, the unique id column, and the column(s) to index. We will just index the single column `text_entry`, which contains the text of the lines in the play.

```sql
PRAGMA create_fts_index('corpus', 'line_id', 'text_entry');
```

The table is now ready to query using the [Okapi BM25](https://en.wikipedia.org/wiki/Okapi_BM25) ranking function.  Rows with no match return a null score.

What does Shakespeare say about butter?

```sql
SELECT
    fts_main_corpus.match_bm25(line_id, 'butter') AS score,
    line_id, play_name, speaker, text_entry
FROM corpus
WHERE score IS NOT NULL
ORDER BY score DESC;
```

|       score        |   line_id   |        play_name         |   speaker    |                     text_entry                     |
|-------------------:|-------------|--------------------------|--------------|----------------------------------------------------|
| 4.427313429798464  | H4/2.4.494  | Henry IV                 | Carrier      | As fat as butter.                                  |
| 3.836270302568675  | H4/1.2.21   | Henry IV                 | FALSTAFF     | prologue to an egg and butter.                     |
| 3.836270302568675  | H4/2.1.55   | Henry IV                 | Chamberlain  | They are up already, and call for eggs and butter; |
| 3.3844488405497115 | H4/4.2.21   | Henry IV                 | FALSTAFF     | toasts-and-butter, with hearts in their bellies no |
| 3.3844488405497115 | H4/4.2.62   | Henry IV                 | PRINCE HENRY | already made thee butter. But tell me, Jack, whose |
| 3.3844488405497115 | AWW/4.1.40  | Alls well that ends well | PAROLLES     | butter-womans mouth and buy myself another of      |
| 3.3844488405497115 | AYLI/3.2.93 | As you like it           | TOUCHSTONE   | right butter-womens rank to market.                |
| 3.3844488405497115 | KL/2.4.132  | King Lear                | Fool         | kindness to his horse, buttered his hay.           |
| 3.0278411214953107 | AWW/5.2.9   | Alls well that ends well | Clown        | henceforth eat no fish of fortunes buttering.      |
| 3.0278411214953107 | MWW/2.2.260 | Merry Wives of Windsor   | FALSTAFF     | Hang him, mechanical salt-butter rogue! I will     |
| 3.0278411214953107 | MWW/2.2.284 | Merry Wives of Windsor   | FORD         | rather trust a Fleming with my butter, Parson Hugh |
| 3.0278411214953107 | MWW/3.5.7   | Merry Wives of Windsor   | FALSTAFF     | Ill have my brains taen out and buttered, and give |
| 3.0278411214953107 | MWW/3.5.102 | Merry Wives of Windsor   | FALSTAFF     | to heat as butter; a man of continual dissolution  |
| 2.739219044070792  | H4/2.4.115  | Henry IV                 | PRINCE HENRY | Didst thou never see Titan kiss a dish of butter?  |

Unlike standard indexes, full-text indexes don't auto-update as the underlying data is changed, so you need to `PRAGMA drop_fts_index(my_fts_index)` and recreate it when appropriate.

## Note on Generating the Corpus Table

For more details, see the ["Generating a Shakespeare corpus for full-text searching from JSON" blog post](https://duckdb.blogspot.com/2023/04/generating-shakespeare-corpus-for-full.html)
* The Columns are: line_id, play_name, line_number, speaker, text_entry.
* We need a unique key for each row in order for full-text searching to work.
* The line_id "KL/2.4.132" means King Lear, Act 2, Scene 4, Line 132.