---
layout: docu
title: DuckDB Full Text Search
selected: DuckDB Full Text Search
---

A full text index allows for a query to quickly search for all occurences of individual words within longer text strings.
Here's an example of building a full text index of Shakespeare's plays.

```sql
create table corpus as
  select * from read_parquet(
    'https://github.com/marhar/duckdb_tools/raw/main/full-text-shakespeare/shakespeare.parquet');
```

```sql
describe corpus;
```
```
┌─────────────┬─────────────┬─────────┐
│ column_name │ column_type │  null   │
├─────────────┼─────────────┼─────────┤
│ line_id     │ VARCHAR     │ YES     │
│ play_name   │ VARCHAR     │ YES     │
│ line_number │ VARCHAR     │ YES     │
│ speaker     │ VARCHAR     │ YES     │
│ text_entry  │ VARCHAR     │ YES     │
└─────────────┴─────────────┴─────────┘
```

the text of each line is in `text_entry`, and a unique key for each
line is in `line_id`.

First, we create the index, specifying the table name, the unique id
column, and the column(s) to index.  We will just index the single column
`text_entry`, which contains the text of the lines in the play.

```sql
INSTALL 'fts';
LOAD fts;
PRAGMA create_fts_index('corpus', 'line_id', 'text_entry');
```

The table is now ready to query using the
[Okapi BM25](https://en.wikipedia.org/wiki/Okapi_BM25)
ranking function.  Rows with no match return a null score.

What does Shakespeare say about butter?

```sql
SELECT fts_main_corpus.match_bm25(line_id, 'butter') AS score,
    line_id,play_name,speaker,text_entry
  FROM corpus
  WHERE score IS NOT NULL
  ORDER BY score;
```
```
┌───────────────────┬─────────────┬──────────────────────┬──────────────┬──────────────────────────────────────────────┐
│       score       │   line_id   │      play_name       │   speaker    │                  text_entry                  │
│      double       │   varchar   │       varchar        │   varchar    │                   varchar                    │
├───────────────────┼─────────────┼──────────────────────┼──────────────┼──────────────────────────────────────────────┤
│ 2.683490686835495 │ H4/2.4.115  │ Henry IV             │ PRINCE HENRY │ Didst thou never see Titan kiss a dish of …  │
│ 3.781282331450016 │ H4/1.2.21   │ Henry IV             │ FALSTAFF     │ prologue to an egg and butter.               │
│ 3.781282331450016 │ H4/2.1.55   │ Henry IV             │ Chamberlain  │ They are up already, and call for eggs and…  │
│ 3.781282331450016 │ H4/4.2.21   │ Henry IV             │ FALSTAFF     │ toasts-and-butter, with hearts in their be…  │
│ 3.781282331450016 │ H4/4.2.62   │ Henry IV             │ PRINCE HENRY │ already made thee butter. But tell me, Jac…  │
│ 3.781282331450016 │ AWW/4.1.40  │ Alls well that end…  │ PAROLLES     │ butter-womans mouth and buy myself another…  │
│ 3.781282331450016 │ AWW/5.2.9   │ Alls well that end…  │ Clown        │ henceforth eat no fish of fortunes butteri…  │
│ 3.781282331450016 │ AYLI/3.2.93 │ As you like it       │ TOUCHSTONE   │ right butter-womens rank to market.          │
│ 3.781282331450016 │ KL/2.4.132  │ King Lear            │ Fool         │ kindness to his horse, buttered his hay.     │
│ 3.781282331450016 │ MWW/2.2.260 │ Merry Wives of Win…  │ FALSTAFF     │ Hang him, mechanical salt-butter rogue! I …  │
│ 3.781282331450016 │ MWW/2.2.284 │ Merry Wives of Win…  │ FORD         │ rather trust a Fleming with my butter, Par…  │
│ 3.781282331450016 │ MWW/3.5.7   │ Merry Wives of Win…  │ FALSTAFF     │ Ill have my brains taen out and buttered, …  │
│ 3.781282331450016 │ MWW/3.5.102 │ Merry Wives of Win…  │ FALSTAFF     │ to heat as butter; a man of continual diss…  │
│ 6.399093176300027 │ H4/2.4.494  │ Henry IV             │ Carrier      │ As fat as butter.                            │
├───────────────────┴─────────────┴──────────────────────┴──────────────┴──────────────────────────────────────────────┤
│ 14 rows                                                                                                    5 columns │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Unlike standard indexes, full text indexes don't auto-update as the underlying data is changed, so you need to
`PRAGMA drop_fts_index(my_fts_index)` and recreate it when appropriate.

## Note on generating the corpus table

Details are [here](https://duckdb.blogspot.com/2023/04/generating-shakespeare-corpus-for-full.html)
- The Columns are:  line_id, play_name, line_number, speaker, text_entry.
- We need a unique key for each row in order for full text searching to work.
- The line_id "KL/2.4.132" means King Lear, Act 2, Scene 4, Line 132.
