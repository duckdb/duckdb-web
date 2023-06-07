---
layout: docu
title: CLI Charting - Using DuckDB with CLI tools
selected: CLI Charting - Using DuckDB with CLI tools
---

# How to use DuckDB with CLI tools

DuckDB can be used with CLI graphing tools to quickly pipe input to stdout to graph your data in one line.

[YouPlot](https://github.com/red-data-tools/YouPlot) is a Ruby-based CLI tool for drawing visually pleasing plots on the terminal. It can accept input from other programs by piping data from `stdin`. It takes tab-separated (or delimiter of your choice) data and can easily generate various types of plots including bar, line, histogram and scatter.

With DuckDB, you can write to the console (`stdout`) by using the `TO '/dev/stdout'` command. And you can also write comma-separated values by using `WITH (FORMAT 'csv', HEADER)`.

## Installing YouPlot

Installation instructions for YouPlot can be found on the main [YouPlot repository](https://github.com/red-data-tools/YouPlot#installation). If you're on a Mac, you can use:

```bash
brew install youplot
```

Run `uplot --help` to ensure you've installed it successfully!

## Piping DuckDB queries to stdout

By combining the [`COPY...TO`](https://duckdb.org/docs/sql/statements/copy#copy-to) function with a CSV output file, data can be read from any format supported by DuckDB and piped to YouPlot. There are three important steps to doing this.

1. As an example, this is how to read all data from `input.json`:

    ```bash
    duckdb -s "SELECT * FROM read_json_auto('input.json')"
    ```

2. To prepare the data for YouPlot, write a simple aggregate:

    ```bash
    duckdb -s "SELECT date, SUM(purchases) AS total_purchases FROM read_json_auto('input.json') GROUP BY 1 ORDER BY 2 DESC LIMIT 10"
    ```

3. Finally, wrap the `SELECT` in the `COPY...TO` function with an output location of `/dev/stdout`.

    The syntax looks like this:

    ```sql
    COPY (<YOUR_SELECT_QUERY>) TO '/dev/stdout' WITH (FORMAT 'csv', HEADER)
    ```

    The full DuckDB command below outputs the query in CSV format with a header:

    ```bash
    duckdb -s "COPY (SELECT date, SUM(purchases) AS total_purchases FROM read_json_auto('input.json') GROUP BY 1 ORDER BY 2 DESC LIMIT 10) TO '/dev/stdout' WITH (FORMAT 'csv', HEADER)"
    ```

## Connecting DuckDB to YouPlot

Finally, the data can now be piped to YouPlot! Let's assume we have an `input.json` file with dates and number of purchases made by somebody on that date. Using the query above, we'll pipe the data to the `uplot` command to draw a plot of the Top 10 Purchase Dates

```bash
duckdb -s "COPY (SELECT date, SUM(purchases) AS total_purchases FROM read_json_auto('input.json') GROUP BY 1 ORDER BY 2 DESC LIMIT 10) TO '/dev/stdout' WITH (FORMAT 'csv', HEADER)" | uplot bar -d, -H -t "Top 10 Purchase Dates"
```

This tells `uplot` to draw a bar plot, use a comma-seperated delimiter (`-d,`), that the data has a header (`-H`), and give the plot a title (`-t`).

![youplot-top-10](/images/guides/youplot/top-10-plot.png)

## Bonus round! stdin + stdout

Maybe you're piping some data through `jq`. Maybe you're downloading a JSON file from somewhere. You can also tell DuckDB to read the data from another proess by changing the filename to `/dev/stdin`.

Let's combine this with a quick `curl` from GitHub to see what a certain user has been up to lately.

```bash
curl -sL "https://api.github.com/users/dacort/events?per_page=100" \
    | duckdb -s "COPY (SELECT type, count(*) as event_count FROM read_json_auto('/dev/stdin') GROUP BY 1 ORDER BY 2 DESC LIMIT 10) TO '/dev/stdout' WITH (FORMAT 'csv', HEADER)" \
    | uplot bar -d, -H -t "GitHub Events for @dacort"
```

![github-events](/images/guides/youplot/github-events.png)

