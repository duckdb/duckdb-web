---
layout: post
title: "Command Line Data Processing: Using DuckDB as a Unix Tool"
author: "Gabor Szarnyas"
thumb: "/images/blog/thumbs/240620.svg"
excerpt: "DuckDB's CLI client is portable to many platforms and architectures. It handles CSV files conveniently and offers users the same rich SQL syntax everywhere. These characteristics make DuckDB an ideal tool to complement traditional Unix tools for data processing in the command line."
---

In this blog post, we dive into the terminal to compare DuckDB with traditional tools used in Unix shells (Bash, Zsh, etc.).
We solve several problems requiring operations such as projection and filtering to demonstrate the differences between using SQL queries in DuckDB versus specialized command line tools.
In the process, we will show off some cool features such as DuckDB's [powerful CSV reader]({% link docs/data/csv/overview.md %}) and the [positional join operator](#duckdb-positional-join).
Let's get started!

## Table of Contents

* [Table of Contents](#table-of-contents)
* [The Unix Philosophy](#the-unix-philosophy)
* [Portability and Usability](#portability-and-usability)
* [Data Processing with Unix Tools and DuckDB](#data-processing-with-unix-tools-and-duckdb)
  * [Datasets](#datasets)
  * [Projecting Columns](#projecting-columns)
  * [Sorting Files](#sorting-files)
  * [Intersecting Columns](#intersecting-columns)
  * [Pasting Rows Together](#pasting-rows-together)
  * [Filtering](#filtering)
  * [Joining Files](#joining-files)
  * [Replacing Strings](#replacing-strings)
  * [Reading JSON](#reading-json)
* [Performance](#performance)
* [Summary](#summary)

## The Unix Philosophy

To set the stage, let's recall the [Unix philosophy](https://en.wikipedia.org/wiki/Unix_philosophy). This states that programs should:

* do one thing and do it well,
* work together, and
* handle text streams.

Unix-like systems such as macOS, Linux and [WSL in Windows](https://en.wikipedia.org/wiki/Windows_Subsystem_for_Linux) have embraced this philosophy.
Tools such as
[`grep`](https://man7.org/linux/man-pages/man1/grep.1.html),
[`sed`](https://man7.org/linux/man-pages/man1/sed.1.html), and
[`sort`](https://man7.org/linux/man-pages/man1/sort.1.html)
are ubiquitious and widely used in [shell scripts](https://en.wikipedia.org/wiki/Shell_script).

As a purpose-built data processing tool, DuckDB fits the Unix philosophy quite well.
First, it was designed to be a fast in-process analytical SQL database system _(do one thing and do it well)._
Second, it has a standalone [command line client]({% link docs/api/cli/overview.md %}), which can consume and produce CSV files _(work together),_
and also supports reading and writing text streams _(handle text streams)_.
Thanks to these, DuckDB works well in the ecosystem of Unix CLI tools, as
shown
[in](https://x.com/jooon/status/1781401858411565473)
[several](https://www.pgrs.net/2024/03/21/duckdb-as-the-new-jq/)
[posts](https://x.com/MarginaliaNu/status/1701532341225583044).

## Portability and Usability

While Unix CLI tools are fast, robust, and available on all major platforms, they often have cumbersome syntax that's difficult to remember.
To make matters worse, these tools often come with slight differences between systems – think of the [differences between GNU `sed` and macOS's `sed`](https://unix.stackexchange.com/a/131940/315847) or the differences between regex syntax among programs, which is aptly captured by Donald Knuth's quip [_“I define Unix as 30 definitions of regular expressions living under one roof.”_](https://en.wikiquote.org/wiki/Donald_Knuth#Quotes)

While there are shells specialized specifically for dataframe processing, such as the [Nushell project](https://github.com/nushell/nushell), older Unix shells (e.g., the Bourne shell `sh` and Bash) are still the most wide-spread, especially on servers.

At the same time, we have DuckDB, an extremely portable database system which uses the same SQL syntax on all platforms.
With [version 1.0.0 released recently]({% post_url 2024-06-03-announcing-duckdb-100 %}), DuckDB's syntax – based on the proven and widely used PostgeSQL dialect – is now in a stable state.
Another attractive feature of DuckDB is that it offers an interactive shell, which aids quick debugging. Moreover, DuckDB is available in [several host languages]({% link docs/api/overview.md %}) as well as in the browser [via WebAssembly](https://shell.duckdb.org/), so if you ever decide to use your SQL scripts outside of the shell, DuckDB SQL scripts can be ported to a wide variety of environments without any changes.

<hr/> <!-- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -->

## Data Processing with Unix Tools and DuckDB

In the following, we give examples for implementing simple data processing tasks using the CLI tools provided in most Unix shells and using DuckDB SQL queries.
We use DuckDB v1.0.0 and run it in [in-memory mode]({% link docs/connect/overview.md %}#in-memory-database).
This mode makes sense for the problems we are tackling, as we do not create any tables and the operations are not memory-intensive, so there is no data to persist or to spill on disk.

<hr/> <!-- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -->

### Datasets

We use the four input files capturing information on cities and airports in the Netherlands.

<details markdown='1'>
<summary markdown='span'>
    [`pop.csv`](/data/cli/pop.csv), the population of each of the top-10 most populous cities.
</summary>
```csv
city,province,population
Amsterdam,North Holland,905234
Rotterdam,South Holland,656050
The Hague,South Holland,552995
Utrecht,Utrecht,361924
Eindhoven,North Brabant,238478
Groningen,Groningen,234649
Tilburg,North Brabant,224702
Almere,Flevoland,218096
Breda,North Brabant,184716
Nijmegen,Gelderland,179073
```
</details>

<details markdown='1'>
<summary markdown='span'>
    [`area.csv`](/data/cli/area.csv), the area of each of the top-10 most populous cities.
</summary>
```csv
city,area
Amsterdam,219.32
Rotterdam,324.14
The Hague,98.13
Utrecht,99.21
Eindhoven,88.92
Groningen,197.96
Tilburg,118.13
Almere,248.77
Breda,128.68
Nijmegen,57.63
```
</details>

<details markdown='1'>
<summary markdown='span'>
    [`cities-airports.csv`](/data/cli/cities-airports.csv), the [IATA codes](https://en.wikipedia.org/wiki/IATA_airport_code) of civilian airports serving given cities.
</summary>
```csv
city,IATA
Amsterdam,AMS
Haarlemmermeer,AMS
Eindhoven,EIN
Groningen,GRQ
Eelde,GRQ
Maastricht,MST
Beek,MST
Rotterdam,RTM
The Hague,RTM
```
</details>

<details markdown='1'>
<summary markdown='span'>
    [`airport-names.csv`](/data/cli/airport-names.csv), the airport names belonging to given IATA codes.
</summary>
```csv
IATA,airport name
AMS,Amsterdam Airport Schiphol
EIN,Eindhoven Airport
GRQ,Groningen Airport Eelde
MST,Maastricht Aachen Airport
RTM,Rotterdam The Hague Airport
```
</details>

<!-- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -->

You can download all input files as a [single zip file](/data/cli/duckdb-cli-data.zip).

<hr/>

### Projecting Columns

Projecting columns is a very common data processing step. Let's take the `pop.csv` file and project the first and last columns, `city` and `population`.

#### Unix Shell: `cut`

In the Unix shell, we use the [`cut` command](https://man7.org/linux/man-pages/man1/cut.1.html) and specify the file's delimiter (`-d`) and the columns to be projected (`-f`).

```bash
cut -d , -f 1,3 pop.csv
```

This produces the following output:

```csv
city,population
Amsterdam,905234
Rotterdam,656050
The Hague,552995
Utrecht,361924
Eindhoven,238478
Groningen,234649
Tilburg,224702
Almere,218096
Breda,184716
Nijmegen,179073
```

#### DuckDB: `SELECT`

In DuckDB, we can use the CSV reader to load the data, then use the `SELECT` clause with column indexes (`#i`) to designate the columns to be projected:

```plsql
SELECT #1, #3 FROM 'pop.csv';
```

Note that we did not have to define any schema or load the data to a table.
Instead, we simply used `'pop.csv'` in the `FROM` clause as we would do with a regular table.
DuckDB detects that this is a CSV file and invokes the [`read_csv` function]({% link docs/data/csv/overview.md %}#csv-functions), which automatically infers the CSV file's dialect (delimiter, presence of quotes, etc.) as well as the schema of the table.
This allows us to simply project columns using `SELECT #1, #3`.
We could also use the more readable syntax `SELECT city, population`.

To make the output of the solutions using Unix tools and DuckDB equivalent, we wrap the query into a [`COPY ... TO` statement]({% link docs/sql/statements/copy.md %}#copy--to):

```plsql
COPY (
    SELECT #1, #3 FROM 'pop.csv'
  ) TO '/dev/stdout/';
```

This query produces the same result as the Unix command's output shown [above](#unix-shell-cut).

To turn this into a standalone CLI command, we can invoke the DuckDB command line client with the `-c ⟨query⟩` argument, which runs the SQL query and exits once it's finished.
Using this technique, the query above can be turned into the following one-liner:

```bash
duckdb -c "COPY (SELECT #1, #3 FROM 'pop.csv') TO '/dev/stdout/'"
```

In the following, we'll omit the code blocks using the standalone `duckdb` command: all solutions can be executed in the `duckdb -c ⟨query⟩` template and yield the same result as the solutions using Unix tools.

<hr/> <!-- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -->

### Sorting Files

Another common task is to sort files based on given columns.
Let's rank the cities within provinces based on their populations.
To do so, we need to sort the `pop.csv` file first based on the name of the `province` using an ascending order, then on the `population` using a descending order.
We then return the `province` column first, followed by the `city` and the `population` columns.

#### Unix Shell: `sort`

In the Unix shell, we rely on the [`sort`](https://man7.org/linux/man-pages/man1/sort.1.html) tool.
We specify the CSV file's separator with the `-t` argument and set the keys to sort on using `-k` arguments.
We first sort on the second column (`province`) with `-k 2,2`.
Then, we sort on the third column (`population`), setting the ordering to be reversed (`r`) and numeric (`n`) with `-k 3rn`.
Note that we need to handle the header of the file separately: we take the first row with `head -n 1` and the rest of the rows with `tail -n +2`, sort the latter, and glue them back together with the header.
Finally, we perform a projection to reorder the columns.
Unfortunately, the [`cut` command cannot reorder the columns](https://stackoverflow.com/questions/2129123/rearrange-columns-using-cut), so we use [`awk`](https://man7.org/linux/man-pages/man1/awk.1p.html) instead:

```bash
(head -n 1 pop.csv; tail -n +2 pop.csv \
    | sort -t , -k 2,2 -k 3rn) \
    | awk -F , '{ print $2 "," $1 "," $3}'
```

The result is the following:

```csv
province,city,population
Flevoland,Almere,218096
Gelderland,Nijmegen,179073
Groningen,Groningen,234649
North Brabant,Eindhoven,238478
North Brabant,Tilburg,224702
North Brabant,Breda,184716
North Holland,Amsterdam,905234
South Holland,Rotterdam,656050
South Holland,The Hague,552995
Utrecht,Utrecht,361924
```

#### DuckDB: `ORDER BY`

In DuckDB, we simply load the CSV and specify the column ordering via `SELECT province, city, population`, then set the sorting criteria on the selected columns (`province ASC` and `population DESC`).
The CSV reader automatically detects types, so the sorting is numeric by default. Finally, we surround the query with a `COPY` statement to print the results to the standard output.

```plsql
COPY (
    SELECT province, city, population
    FROM 'pop.csv'
    ORDER BY province ASC, population DESC
  ) TO '/dev/stdout/';
```

<hr/> <!-- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -->

### Intersecting Columns

A common task is to calculate the intersection of two columns, i.e., to find entities that are present in both.
Let's find the cities that are both in the top-10 most populous cities and have their own airports.

#### Unix Shell: `comm`

The Unix solution for intersection uses the [`comm` tool](https://linux.die.net/man/1/comm), intended to compare two _sorted_ files line-by-line.
We first `cut` the relevant colum from both files.
Due to the sorting requirement, we apply `sort` on both inputs before performing the intersection.
The intersection is performed using `comm -12` where the argument `-12` means that we only want to keep lines that are in both files.
We again rely on `head` and `tail` to treat the headers and the rest of the files separately during processing and glue them together at the end.

```bash
head -n 1 pop.csv | cut -d , -f 1; \
  comm -12 \
    <(tail -n +2 pop.csv | cut -d , -f 1 | sort) \
    <(tail -n +2 cities-airports.csv | cut -d , -f 1 | sort) 
```

The script produces the following output:

```csv
city
Amsterdam
Eindhoven
Groningen
Rotterdam
The Hague
```

#### DuckDB: `INTERSECT ALL`

The DuckDB solution reads the CSV files, projects the `city` fields and applies the [`INTERSECT ALL` clause]({% link docs/sql/query_syntax/setops.md %}#intersect-all-bag-semantics) to calculate the intersection:

```plsql
COPY (
    SELECT city FROM 'pop.csv'
    INTERSECT ALL
    SELECT city FROM 'cities-airports.csv'
  ) TO '/dev/stdout/';
```

<hr/> <!-- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -->

### Pasting Rows Together

Pasting rows together line-by-line is a recurring task.
In our example, we know that the `pop.csv` and the `area.csv` files have an equal number of rows, so we can produce a single file that contains both the population and the area of every city in the dataset.

#### Unix Shell: `paste`

In the Unix shell, we use the [`paste`](https://man7.org/linux/man-pages/man1/paste.1.html) command and remove the duplicate `city` field using `cut`:

```bash
paste -d , pop.csv area.csv | cut -d , -f 1,2,3,5
```

The output is the following:

```csv
city,province,population,area
Amsterdam,North Holland,905234,219.32
Rotterdam,South Holland,656050,324.14
The Hague,South Holland,552995,98.13
Utrecht,Utrecht,361924,99.21
Eindhoven,North Brabant,238478,88.92
Groningen,Groningen,234649,197.96
Tilburg,North Brabant,224702,118.13
Almere,Flevoland,218096,248.77
Breda,North Brabant,184716,128.68
Nijmegen,Gelderland,179073,57.63
```

#### DuckDB: `POSITIONAL JOIN`

In DuckDB, we can use a [`POSITIONAL JOIN`]({% link docs/sql/query_syntax/from.md %}#positional-joins).
This join type is one of DuckDB's [SQL extensions]({% link docs/guides/sql_features/friendly_sql.md %}) and it provides a concise syntax to combine tables row-by-row based on each row's position in the table.
Joining the two tables together using `POSITIONAL JOIN` results in two `city` columns – we use the [`EXCLUDE` clause]({% link docs/sql/expressions/star.md %}#exclude-clause) to remove the duplicate column:

```plsql
COPY (
    SELECT pop.*, area.* EXCLUDE city
    FROM 'pop.csv'
    POSITIONAL JOIN 'area.csv'
  ) TO '/dev/stdout/';
```

<hr/> <!-- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -->

### Filtering

Filtering is another very common operation. For this, we'll use [`cities-airports.csv` file](/data/cli/cities-airports.csv).
For each airport, this file contains its `IATA` code and the main cities that it serves:

```csv
city,IATA
Amsterdam,AMS
Haarlemmermeer,AMS
Eindhoven,EIN
...
```

Let's try to formulate two queries:

1. Find all cities whose name ends in `dam`.

2. Find all airports whose IATA code is equivalent to the first three letters of a served city's name, but the city's name does _not_ end in `dam`.

#### Unix Shell: `grep`

To answer the first question in the Unix shell, we use `grep` and the regular expression `^[^,]*dam,`:

```bash
grep "^[^,]*dam," cities-airports.csv
```

In this expression, `^` denotes the start of the line, `[^,]*` searches for a string that does not contain the comma character (the separator).
The expression `dam,` ensures that the end of the string in the first field is `dam`.
The output is:

```csv
Amsterdam,AMS
Rotterdam,RTM
```

Let's try to answer the second question. For this, we need to match the first three characters in the `city` field to the `IATA` field but we need to do so in a case-insensitive manner.
We also need to use a negative condition to exclude the lines where the city's name ends in `dam`.
Both of these requirements are difficult to achieve with a single `grep` or `egrep` command as they lack support for two features.
First, they do not support case-insensitive matching _using a backreference_ (`grep -i` alone is not sufficient to ensure this).
Second, they do not support [negative lookbehinds](https://www.regular-expressions.info/lookaround.html).
Therefore, we use [`pcregrep`](https://man7.org/linux/man-pages/man1/pcregrep.1.html), and formulate our question as follows:

```bash
pcregrep -i '^([a-z]{3}).*?(?<!dam),\1$' cities-airports.csv
```

Here, we call `pcregrep` with the case-insensitive flag (`-i`), which in `pcregrep` also affects backreferences such as `\1`.
We capture the first three letters with `([a-z]{3})` (e.g., `Ams`) and match it to the second field with the backreference: `,\1$`.
We use a non-greedy `.*?` to seek to the end of the first field, then apply a negative lookbehind with the `(?<!dam)` expression to ensure that the field does not end in `dam`.
The result is a single line:

```csv
Eindhoven,EIN
```

#### DuckDB: `WHERE ... LIKE`

Let's answer the questions now in DuckDB.
To answer the first question, we can use [`LIKE` for pattern matching]({% link docs/sql/functions/pattern_matching.md %}).
The header should not be part of the output, so we disable it with `HEADER false`.
The complete query looks like follows:

```plsql
COPY (
    FROM 'cities-airports.csv'
    WHERE city LIKE '%dam'
  ) TO '/dev/stdout/' (HEADER false);
```

For the second question, we use [string slicing]({% link docs/sql/functions/char.md %}#stringbeginend) to extract the first three characters, [`upper`]({% link docs/sql/functions/char.md %}#upperstring) to ensure case-insensitivity, and `NOT LIKE` for the negative condition:

```plsql
COPY (
    FROM 'cities-airports.csv'
    WHERE upper(city[1:3]) = IATA
      AND city NOT LIKE '%dam'
  ) TO '/dev/stdout/' (HEADER false);
```

These queries return exactly the same results as the solutions using `grep` and `pcregrep`.

In both of these queries, we used the [`FROM`-first syntax]({% link docs/sql/query_syntax/from.md %}#from-first-syntax).
If the `SELECT` clause is omitted, the query is executed as if `SELECT *` was used, i.e., it returns all columns.

<hr/> <!-- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -->

### Joining Files

Joining tables is an essential task in data processing. Our next example is going to use a join to return city name–airport name combinations.
This is achieved by joining the `cities-airports.csv` and the `airport-names.csv` files on their IATA code fields.

#### Unix Shell: `join`

Unix tools support joining files via the [`join` command](https://man7.org/linux/man-pages/man1/join.1.html), which joins lines of two _sorted_ inputs on a common field.
To make this work, we sort the files based on their `IATA` fields, then perform the join on the first file's 2nd column (`-1 2`) and the second file's 1st column (`-2 1`).
We have to omit the header for the `join` command to work, so we do just that and construct a new header with an `echo` command:

```bash
echo "IATA,city,airport name"; \
  join -t , -1 2 -2 1 \
    <(tail -n +2 cities-airports.csv | sort -t , -k 2,2) \
    <(tail -n +2 airport-names.csv   | sort -t , -k 1,1)
```

The result is the following:

```csv
IATA,city,airport name
AMS,Amsterdam,Amsterdam Airport Schiphol
AMS,Haarlemmermeer,Amsterdam Airport Schiphol
EIN,Eindhoven,Eindhoven Airport
GRQ,Eelde,Groningen Airport Eelde
GRQ,Groningen,Groningen Airport Eelde
MST,Beek,Maastricht Aachen Airport
MST,Maastricht,Maastricht Aachen Airport
RTM,Rotterdam,Rotterdam The Hague Airport
RTM,The Hague,Rotterdam The Hague Airport
```

#### DuckDB

In DuckDB, we load the CSV files and connect them using the [`NATURAL JOIN` clause]({% link docs/sql/query_syntax/from.md %}#natural-joins), which joins on column(s) with the same name.
To ensure that the result matches with that of the Unix solution, we use the [`ORDER BY ALL` clause]({% link docs/sql/query_syntax/orderby.md %}#order-by-all), which sorts the result on all columns, starting from the first one, and stepping through them for tie-breaking to the last column.

```plsql
COPY (
    SELECT "IATA", "city", "airport name"
    FROM 'cities-airports.csv'
    NATURAL JOIN 'airport-names.csv'
    ORDER BY ALL
  ) TO '/dev/stdout/';
```

<hr/> <!-- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -->

### Replacing Strings

You may have noticed that we are using very clean datasets. This is of course very unrealistic, so in an evil twist, let's reduce the data quality a bit:

* Replace the space in the province's name with an underscore, e.g., turning `North Holland` to `North_Holland`.
* Add thousand separating commas, e.g., turning `905234` to `905,234`.
* Change the CSV's separator to the semicolon character (`;`).

And while we're at it, also fetch the data set via HTTPS this time, using the URL [`https://duckdb.org/data/cli/pop.csv`](https://duckdb.org/data/cli/pop.csv).

#### Unix Shell: `curl` and `sed`

In Unix, remote data sets are typically fetched via [`curl`](https://man7.org/linux/man-pages/man1/curl.1.html).
The output of `curl` is piped into the subsequent processing steps, in this case, a bunch of [`sed`](https://man7.org/linux/man-pages/man1/sed.1.html) commands.

```bash
curl -s https://duckdb.org/data/cli/pop.csv \
    | sed 's/\([^,]*,.*\) \(.*,[^,]*\)/\1_\2/g' \
    | sed 's/,/;/g' \
    | sed 's/\([0-9][0-9][0-9]\)$/,\1/'
```

This results in the following output:

```csv
city;province;population
Amsterdam;North_Holland;905,234
Rotterdam;South_Holland;656,050
The Hague;South_Holland;552,995
Utrecht;Utrecht;361,924
Eindhoven;North_Brabant;238,478
Groningen;Groningen;234,649
Tilburg;North_Brabant;224,702
Almere;Flevoland;218,096
Breda;North_Brabant;184,716
Nijmegen;Gelderland;179,073
```

#### DuckDB: `httpfs` and `regexp_replace`

In DuckDB, we use the following query:

```plsql
COPY (
    SELECT
        city,
        replace(province, ' ', '_') AS province,
        regexp_replace(population::VARCHAR, '([0-9][0-9][0-9])$', ',\1')
            AS population
    FROM 'https://duckdb.org/data/cli/pop.csv'
  ) TO '/dev/stdout/' (DELIMITER ';');
```

Note that the `FROM` clause now has an HTTPS URL instead of a simple CSV file.
The presence of the `https://` prefix triggers DuckDB to load the [`httpfs` extension]({% link docs/extensions/httpfs/overview.md %}) and use it to fetch the JSON document.
We use the [`replace` function]({% link docs/sql/functions/char.md %}#replacestring-source-target) to substitute the spaces with underscores,
and the [`regexp_replace` function]({% link docs/sql/functions/char.md %}#regexp_replacestring-pattern-replacement) for the replacement using a regular expression.
(We could have also used string formatting functions such as [`format`]({% link docs/sql/functions/char.md %}#fmt-syntax) and [`printf`]({% link docs/sql/functions/char.md %}#printf-syntax)).
To change the separator to a semicolon, we serialize the file using the `COPY` statement with the `DELIMITER ';'` option.

<hr/> <!-- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -->

### Reading JSON

As a final exercise, let's query the number of stars given to the [`duckdb/duckdb` repository on GitHub](https://github.com/duckdb/duckdb).

#### Unix Shell: `curl` and `jq`

In Unix tools, we can use `curl` to get the JSON file from `https://api.github.com` and pipe its output to [`jq`](https://jqlang.github.io/jq/manual/) to query the JSON object.

```bash
curl -s https://api.github.com/repos/duckdb/duckdb \
    | jq ".stargazers_count"
```

#### DuckDB: `read_json`

In DuckDB, we use the [`read_json` function]({% link docs/data/json/overview.md %}), invoking it with the remote HTTPS endpoint's URL.
The schema of the JSON file is detected automatically, so we can simply use `SELECT` to return the required field.

```plsql
SELECT stargazers_count
  FROM read_json('https://api.github.com/repos/duckdb/duckdb');
```

#### Output

Both of these commands return the current number of stars of the repository.

<hr/> <!-- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -->

## Performance

At this point, you might be wondering about the performance of the DuckDB solutions.
After all, all of our prior examples have only consisted of a few lines, so benchmarking them against each other will not result in any measurable performance differences.
So, let's switch to the Dutch railway services dataset that we used in a [previous blog post]({% post_url 2024-05-31-analyzing-railway-traffic-in-the-netherlands %}) and formulate a different problem.

We'll use the [2023 railway services file (`services-2023.csv.gz`)](https://blobs.duckdb.org/nl-railway/services-2023.csv.gz) and count the number of Intercity services that operated in that year.

In Unix, we can use the [`gzcat`](https://www.unix.com/man-page/osf1/1/gzcat/) command to decompress the `csv.gz` file into a pipeline. Then, we can use `grep` or `pcregrep` (which is more performant), and top it off with the [`wc`](https://man7.org/linux/man-pages/man1/wc.1.html) command to count the number of lines (`-l`).
In DuckDB, the built-in CSV reader also supports [compressed CSV files]({% link docs/data/csv/overview.md %}#parameters), so we can use that without any extra configuration.

```batch
gzcat services-2023.csv.gz | grep '^[^,]*,[^,]*,Intercity,' | wc -l
gzcat services-2023.csv.gz | pcregrep '^[^,]*,[^,]*,Intercity,' | wc -l
duckdb -c "SELECT count(*) FROM 'services-2023.csv.gz' WHERE \"Service:Type\" = 'Intercity';"
```

We also test the tools on uncompressed input:

```batch
gunzip -k services-2023.csv.gz
grep '^[^,]*,[^,]*,Intercity,' services-2023.csv | wc -l
pcregrep '^[^,]*,[^,]*,Intercity,' services-2023.csv | wc -l
duckdb -c "SELECT count(*) FROM 'services-2023.csv' WHERE \"Service:Type\" = 'Intercity';"
```

To reduce the noise in the measurements, we used the [`hyperfine`](https://github.com/sharkdp/hyperfine) benchmarking tool and took the mean execution time of 10 runs.
The experiments were carried out on a MacBook Pro with a 12-core M2 Pro CPU and 32 GB RAM, running macOS Sonoma 14.5.
To reproduce them, run the [`grep-vs-duckdb-microbenchmark.sh` script](https://duckdb.org/microbenchmarks/grep-vs-duckdb-microbenchmark.sh).
The following table shows the runtimes of the solutions on both compressed and uncompressed inputs:

| Tool | Runtime (compressed) | Runtime (uncompressed) |
|---|--:|--:|
| grep 2.6.0-FreeBSD | 20.9 s | 20.5 s |
| pcregrep 8.45 | 3.1 s | 2.9 s |
| DuckDB 1.0.0 | 4.2 s | 1.2 s |

The results show that on compressed input, `grep` was the slowest, while DuckDB is slightly edged out by `gzcat`+`pcregrep`, which ran in 3.1 seconds compared to DuckDB's 4.2 seconds.
On uncompressed input, DuckDB can utilize all CPU cores from the get-go (instead of starting with a single-threaded decompression step), allowing it to outperform both `grep` and `pcregrep` by a significant margin: 2.5× faster than `pcregrep` and more than 15× faster than `grep`.

While this example is quite simple, as queries get more complex, there are more opportunities for optimization and larger intermediate dataset may be produced. While both of these can be tackled within a shell script (by manually implementing optimizations and writing the intermediate datasets to disk), these will likely be less efficient than what a DBMS can come up with. Shell scripts implementing complex pipelines can also be very brittle and need to be rethought even for small changes, making the performance advantage of using a database even more significant for more complex problems.

<hr/> <!-- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -->

## Summary

In this post, we used DuckDB as a standalone CLI application, and explored its abilities to complement or substitute existing command line tools (`sort`, `grep`, `comm`, `join`, etc.).
While we obviously like DuckDB a lot and prefer to use it in many cases, we also believe Unix tools have their place:
on most systems, they are already pre-installed and a well-chosen toolchain of Unix commands _can_ be
[fast](https://adamdrake.com/command-line-tools-can-be-235x-faster-than-your-hadoop-cluster.html),
[efficient](https://pesin.space/posts/2019-07-02/),
and portable (thanks to [POSIX-compliance](https://en.wikipedia.org/wiki/POSIX#POSIX-oriented_operating_systems)).
Additionally, they can be very concise for certain problems.
However, to reap their benefits, you will need to learn the syntax and quirks of each tool such as `grep` variants, [`awk`](https://man7.org/linux/man-pages/man1/awk.1p.html)
as well as advanced ones such as [`xargs`](https://man7.org/linux/man-pages/man1/xargs.1.html) and [`parallel`](https://www.gnu.org/software/parallel/).
In the meantime, DuckDB's SQL is easy-to-learn (you likely know quite a bit of it already) and DuckDB handles most of the optimization for you.

If you have a favorite CLI use case for DuckDB, let us know on social media or submit it to [DuckDB snippets](https://duckdbsnippets.com/). Happy hacking!
