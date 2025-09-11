---
layout: post
title: "Solving Letter Scramble Puzzles with DuckDB"
author: "Gabor Szarnyas"
tags: ["using DuckDB"]
thumb: "/images/blog/thumbs/letter-scramble-puzzle.svg"
image: "/images/blog/thumbs/letter-scramble-puzzle.png"
excerpt: "In this lighthearted post, we solve a puzzle type that's on display in Dutch trains."
---

The [Dutch National Railway Services (NS)](https://www.ns.nl/) is releasing a “letter scramble”-style puzzle every week where
they give a term whose letters can be found in a Dutch train station's name.
In order to have a match, it doesn't have to be a perfect anagram – for example, `Amsterdam` (9 letters) matches both `mastered` (8 letters) and `Dream Master` (11 letters) because all three terms contain the same letters, just with different amounts of repetitions. Let's call this a “weak anagram”.

The puzzle in the first week of September was `Clumsy Rental Red`. Let's try to find the solution using DuckDB!

## Letter Scrambling Macro

First, let's create a [macro]({% link docs/stable/sql/statements/create_macro.md %}) that turns a string into an ordered list of unique characters:

```sql
CREATE MACRO order_letters(s) AS 
    lower(s)                  -- convert all characters to lowercase
    .regexp_replace(
        '[^\p{L}]', '', 'g'
    )                         -- remove all non-Unicode characters
    .string_to_array('')      -- turn the string into a list
    .list_distinct()          -- eliminate unique elements from the list
    .list_sort();             -- sort the list
```

We can use this to see whether to terms match:

```sql
SELECT
    order_letters('Amsterdam') AS letters_1,
    order_letters('mastered') AS letters_2,
    order_letters('Dream Master') AS letters_3,
    letters_1 = letters_2 AS matches_1,
    letters_1 = letters_3 AS matches_2;
```

|       letters_1       |       letters_2       |       letters_3       | matches_1 | matches_2 |
|-----------------------|-----------------------|-----------------------|----------:|----------:|
| [a, d, e, m, r, s, t] | [a, d, e, m, r, s, t] | [a, d, e, m, r, s, t] | true      | true      |

Indeed, both expressions match do!

## Station Names

To solve the puzzle, we need a list of train stations.
Luckily, one of our go-to datasets at DuckDB is the [Dutch railway datasets]({% link docs/stable/guides/snippets/dutch_railway_datasets.md %}), including its services and train stations. We can create a table with the station names:

```sql
CREATE TABLE stations AS
    FROM 'https://blobs.duckdb.org/nl-railway/stations-2023-09.csv';
```

Then, we can select the 

```sql
SELECT name_long
FROM stations
WHERE order_letters(name_long) = order_letters('Clumsy Rental Red');
```

<details markdown='1'>
<summary markdown='span'>
Click to see the solution
</summary>
[Lelystad Centrum](https://en.wikipedia.org/wiki/Lelystad_Centrum_railway_station)
</details>

## Solve with a Table Macro

To find a weak anagram station name, we can use a [table macro]({% link docs/stable/sql/statements/create_macro.md %}#table-macros):

```sql
CREATE MACRO find_weak_anagram(s) AS TABLE
    SELECT name_long
    FROM stations
    WHERE order_letters(name_long) = order_letters(s);
```

Then, we can find the solution with a short SQL statement:

```sql
FROM find_weak_anagram('Clumsy Rental Red');
```

## Weak Anagrams Station Pairs

We got curious: are there two stations that are weak anagrams of each other?
We can create a Cartesian product from the station names and compare their ordered letters to find out:

```sql
SELECT s1.name_long AS station_1, s2.name_long AS station_2
FROM stations s1, stations s2
WHERE s1.name_long.order_letters() = s2.name_long.order_letters()
  -- ensure symmetry-breaking
  AND s1.name_long < s2.name_long
  -- make sure the station names don't contain each other
  AND NOT s1.name_long.contains(s2.name_long)
  AND NOT s2.name_long.contains(s1.name_long);
```

There are in fact three station pairs:

|  station_1  | station_2  |
|-------------|------------|
| Melsele     | Selm       |
| Etten-Leur  | Lunteren   |
| Diemen Zuid | Emmen Zuid |

## Cleaning Up

Most of the time, you don't have to clean up after running a simple DuckDB script:
you simply close the in-memory database session, which takes care of the cleanup.
However, it's worth pointing out that macros in DuckDB are persisted and this can get in the way
– e.g., when copying the database into a [DuckLake](https://ducklake.select/):

```sql
ATTACH 'ducklake:metadata.ducklake' AS my_ducklake;
COPY FROM DATABASE memory TO my_ducklake;
```

DuckLake [does not support macros (functions)](https://ducklake.select/docs/stable/duckdb/unsupported_features.html#likely-to-be-supported-in-the-future), and throws the following error message:

```console
Not implemented Error:
DuckLake does not support functions
```

You can drop the macros with the following commands:

```sql
DROP MACRO order_letters;
DROP MACRO TABLE find_weak_anagram;
```

With this, the `COPY FROM DATABASE` call succeeds.

## Summary

That was our quick guide to solving the NS puzzle!
Is this a database problem? Not really, but you DuckDB's SQL allows you to succinctly solve take care of it.
Happy puzzle solving!

> This week, the puzzle is `Zere Tanda Voozan`.
> You can find the weekly puzzle's solution on the [NS website](https://www.ns.nl/dagje-uit/ontspanning/puzzel.html).
