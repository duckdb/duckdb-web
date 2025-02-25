---
layout: docu
title: Analyzing a Git Repository
---

You can use DuckDB to analyze Git logs using the output of the [`git log` command](https://git-scm.com/docs/git-log).

We start by using a trick:
we select a character that doesn't occur in any part of commit log (author names, messages, etc).
Since version v1.2.0, DuckDB's CSV reader supports 4-byte delimiters, making it possible to use emojis.

We assume that the [Fish Cake with Swirl emoji (🍥)](https://emojipedia.org/fish-cake-with-swirl) is not a common occurrence in codebases and export the log as follows:

```bash
git log --date=iso-strict --pretty=format:%ad🍥%h🍥%an🍥%s > git-log.csv
```

The resulting file looks like this:

```text
2025-02-21T16:59:07+01:00🍥cd0d0da9b1🍥Mark🍥docs: tweak explanation of median for even cardinality inputs (#13726)
2025-02-21T16:53:53+01:00🍥c8a53c3307🍥Mark🍥Linux CLI: override platform for ARM manylinux (#16347)
2025-02-21T16:53:29+01:00🍥0e98b26009🍥Mark🍥[chore] No ccache for OSX Python (#16348)
2025-02-21T15:01:33+01:00🍥96db35892a🍥Carlo Piovesan🍥[chore] No ccache for OSX Python
2025-02-21T14:26:56+01:00🍥4addad3422🍥Carlo Piovesan🍥Linux CLI: override platform for ARM manylinux
```

Start DuckDB and read the log as a CSV (or “🍥SV”) file:

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
SELECT timestamp, author, message
FROM commits
LIMIT 5;
```

```text
┌─────────────────────┬────────────────┬────────────────────────────────────────────────────────────────────────┐
│      timestamp      │     author     │                                message                                 │
│      timestamp      │    varchar     │                                varchar                                 │
├─────────────────────┼────────────────┼────────────────────────────────────────────────────────────────────────┤
│ 2025-02-21 15:59:07 │ Mark           │ docs: tweak explanation of median for even cardinality inputs (#13726) │
│ 2025-02-21 15:53:53 │ Mark           │ Linux CLI: override platform for ARM manylinux (#16347)                │
│ 2025-02-21 15:53:29 │ Mark           │ [chore] No ccache for OSX Python (#16348)                              │
│ 2025-02-21 14:01:33 │ Carlo Piovesan │ [chore] No ccache for OSX Python                                       │
│ 2025-02-21 13:26:56 │ Carlo Piovesan │ Linux CLI: override platform for ARM manylinux                         │
└─────────────────────┴────────────────┴────────────────────────────────────────────────────────────────────────┘
```

We can analyze this table as any other in DuckDB.
For example, we can ask: **which topics were most commonly mentioned in the commit messages – CI, CLI, or Python?**

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
│ ci      │         826 │
│ python  │         664 │
│ cli     │          47 │
└─────────┴─────────────┘
```

We can also visualize the number of commits each year:

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
│  2025 │        1680 │ ██████▋                                                                          │
└───────┴─────────────┴──────────────────────────────────────────────────────────────────────────────────┘
```

Enjoy!
