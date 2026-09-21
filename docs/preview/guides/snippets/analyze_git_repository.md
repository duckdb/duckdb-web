---
layout: docu
title: Analyzing a Git Repository
---

You can use DuckDB to analyze Git logs using the output of the [`git log` command](https://git-scm.com/docs/git-log).

## Exporting the Git Log

We start by picking a character that doesn't occur in any part of the commit log (author names, messages, etc).
Since version v1.2.0, DuckDB's CSV reader supports [4-byte delimiters]({% post_url 2025-02-05-announcing-duckdb-120 %}#csv-features), making it possible to use emojis! 🎉

Despite being featured in the [Emoji Movie](https://www.imdb.com/title/tt4877122/) (IMDb rating: 3.4),
we can assume that the [Fish Cake with Swirl emoji (🍥)](https://emojipedia.org/fish-cake-with-swirl) is not a common occurrence in most Git logs.
So, let's clone the [`duckdb/duckdb` repository](https://github.com/duckdb/duckdb) and export its log as follows:

```batch
git log --date=iso-strict --pretty=format:%ad🍥%h🍥%an🍥%s > git-log.csv
```

The resulting file looks like this:

```text
2025-02-25T18:12:54+01:00🍥d608a31e13🍥Mark🍥MAIN_BRANCH_VERSIONING: Adopt also for Python build and amalgamation (#16400)
2025-02-25T15:05:56+01:00🍥920b39ad96🍥Mark🍥Read support for Parquet Float16 (#16395)
2025-02-25T13:43:52+01:00🍥61f55734b9🍥Carlo Piovesan🍥MAIN_BRANCH_VERSIONING: Adopt also for Python build and amalgamation
2025-02-25T12:35:28+01:00🍥87eff7ebd3🍥Mark🍥Fix issue #16377 (#16391)
2025-02-25T10:33:49+01:00🍥35af26476e🍥Hannes Mühleisen🍥Read support for Parquet Float16
```

## Loading the Git Log into DuckDB

Start DuckDB and read the log as a <s>CSV</s> 🍥SV:

```sql
CREATE TABLE commits AS 
    FROM read_csv(
            'git-log.csv',
            delim = '🍥',
            header = false,
            column_names = ['timestamp', 'hash', 'author', 'message']
        );
```

This will result in a nice DuckDB table:

```sql
FROM commits
LIMIT 5;
```

```text
┌─────────────────────┬────────────┬──────────────────┬───────────────────────────────────────────────────────────────────────────────┐
│      timestamp      │    hash    │      author      │                                    message                                    │
│      timestamp      │  varchar   │     varchar      │                                    varchar                                    │
├─────────────────────┼────────────┼──────────────────┼───────────────────────────────────────────────────────────────────────────────┤
│ 2025-02-25 17:12:54 │ d608a31e13 │ Mark             │ MAIN_BRANCH_VERSIONING: Adopt also for Python build and amalgamation (#16400) │
│ 2025-02-25 14:05:56 │ 920b39ad96 │ Mark             │ Read support for Parquet Float16 (#16395)                                     │
│ 2025-02-25 12:43:52 │ 61f55734b9 │ Carlo Piovesan   │ MAIN_BRANCH_VERSIONING: Adopt also for Python build and amalgamation          │
│ 2025-02-25 11:35:28 │ 87eff7ebd3 │ Mark             │ Fix issue #16377 (#16391)                                                     │
│ 2025-02-25 09:33:49 │ 35af26476e │ Hannes Mühleisen │ Read support for Parquet Float16                                              │
└─────────────────────┴────────────┴──────────────────┴───────────────────────────────────────────────────────────────────────────────┘
```

## Analyzing the Log

We can analyze the table as any other in DuckDB.

### Common Topics

Let's start with a simple question: which topic was the most commonly mentioned in the commit messages: CI, CLI, or Python?

```sql
SELECT
    message.lower().regexp_extract('\b(ci|cli|python)\b') AS topic,
    count(*) AS num_commits
FROM commits
WHERE topic <> ''
GROUP BY ALL
ORDER BY num_commits DESC;
```

```text
┌─────────┬─────────────┐
│  topic  │ num_commits │
│ varchar │    int64    │
├─────────┼─────────────┤
│ ci      │         828 │
│ python  │         666 │
│ cli     │          49 │
└─────────┴─────────────┘
```

Out of these three topics, commits related to continuous integration dominate the log!

We can also do a more exploratory analysis by looking at all words in the commit messages.
To do so, we first tokenize the messages:

```sql
CREATE TABLE words AS
    SELECT unnest(
        message
            .lower()
            .regexp_replace('\W', ' ')
            .trim(' ')
            .string_split_regex('\W')
        ) AS word    
FROM commits;
```

Then, we remove stopwords using a pre-defined list:

```sql
CREATE TABLE stopwords AS
    SELECT unnest(['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'can', 'did', 'do', 'does', 'doing', 'don', 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', 'has', 'have', 'having', 'he', 'her', 'here', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'itself', 'just', 'me', 'more', 'most', 'my', 'myself', 'no', 'nor', 'not', 'now', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 's', 'same', 'she', 'should', 'so', 'some', 'such', 't', 'than', 'that', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'these', 'they', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'you', 'your', 'yours', 'yourself', 'yourselves']) AS word;

CREATE OR REPLACE TABLE words AS
    FROM words
    NATURAL ANTI JOIN stopwords
    WHERE word != '';
```

> We use the `NATURAL ANTI JOIN` clause here, which allows us to elegantly filter out values that occur in the `stopwords` table.

Finally, we select the top-20 most common words.

```sql
SELECT word, count(*) AS count FROM words
GROUP BY ALL
ORDER BY count DESC
LIMIT 20;
```

```text
┌──────────┬───────┐
│    w     │ count │
│ varchar  │ int64 │
├──────────┼───────┤
│ merge    │ 12550 │
│ fix      │  6402 │
│ branch   │  6005 │
│ pull     │  5950 │
│ request  │  5945 │
│ add      │  5687 │
│ test     │  3801 │
│ master   │  3289 │
│ tests    │  2339 │
│ issue    │  1971 │
│ main     │  1935 │
│ remove   │  1884 │
│ format   │  1819 │
│ duckdb   │  1710 │
│ use      │  1442 │
│ mytherin │  1410 │
│ fixes    │  1333 │
│ hawkfish │  1147 │
│ feature  │  1139 │
│ function │  1088 │
├──────────┴───────┤
│     20 rows      │
└──────────────────┘
```

As expected, there are many Git terms (`merge`, `branch`, `pull`, etc.), followed by terminology related to development (`fix`, `test`/`tests`, `issue`, `format`).
We also see the account names of some developers ([`mytherin`](https://github.com/Mytherin), [`hawkfish`](https://github.com/hawkfish)), which are likely there due to commit messages for merging pull requests (e.g., [”Merge pull request #13776 from Mytherin/expressiondepth”](https://github.com/duckdb/duckdb/commit/4d18b9d05caf88f0420dbdbe03d35a0faabf4aa7)).
Finally, we also see some DuckDB-related terms such as `duckdb` (shocking!) and `function`.

### Visualizing the Number of Commits

Let's visualize the number of commits each year:

```sql
SELECT
    year(timestamp) AS year,
    count(*) AS num_commits,
    num_commits.bar(0, 20_000) AS num_commits_viz
FROM commits
GROUP BY ALL
ORDER BY ALL;
```

```text
┌───────┬─────────────┬──────────────────────────────────────────────────────────────────────────────────┐
│ year  │ num_commits │                                 num_commits_viz                                  │
│ int64 │    int64    │                                     varchar                                      │
├───────┼─────────────┼──────────────────────────────────────────────────────────────────────────────────┤
│  2018 │         870 │ ███▍                                                                             │
│  2019 │        1621 │ ██████▍                                                                          │
│  2020 │        3484 │ █████████████▉                                                                   │
│  2021 │        6488 │ █████████████████████████▉                                                       │
│  2022 │        9817 │ ███████████████████████████████████████▎                                         │
│  2023 │       14585 │ ██████████████████████████████████████████████████████████▎                      │
│  2024 │       15949 │ ███████████████████████████████████████████████████████████████▊                 │
│  2025 │        1788 │ ███████▏                                                                         │
└───────┴─────────────┴──────────────────────────────────────────────────────────────────────────────────┘
```

We see a steady growth over the years –
especially considering that many of DuckDB's functionalities and clients, which were originally part of the main repository, are now maintained in separate repositories
(e.g., [Java](https://github.com/duckdb/duckdb-java), [R](https://github.com/duckdb/duckdb-r)).

Happy hacking!
