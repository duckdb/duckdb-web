---
layout: docu
redirect_from:
- /docs/guides/python/ibis
title: Integration with Ibis
---

[Ibis](https://ibis-project.org) is a Python dataframe library that supports 20+ backends, with DuckDB as the default. Ibis with DuckDB provides a Pythonic interface for SQL with great performance.

## Installation

You can pip install Ibis with the DuckDB backend:

```batch
pip install 'ibis-framework[duckdb,examples]' # examples is only required to access the sample data Ibis provides
```

or use conda:

```batch
conda install ibis-framework
```

or use mamba:

```batch
mamba install ibis-framework
```

## Create a Database File

Ibis can work with several file types, but at its core, it connects to existing databases and interacts with the data there. You can get started with your own DuckDB databases or create a new one with example data.

```python
import ibis

con = ibis.connect("duckdb://penguins.ddb")
con.create_table(
    "penguins", ibis.examples.penguins.fetch().to_pyarrow(), overwrite = True
)
```

```python
# Output:
DatabaseTable: penguins
  species           string
  island            string
  bill_length_mm    float64
  bill_depth_mm     float64
  flipper_length_mm int64
  body_mass_g       int64
  sex               string
  year              int64
```

You can now see the example dataset copied over to the database:

```python
# reconnect to the persisted database (dropping temp tables)
con = ibis.connect("duckdb://penguins.ddb")
con.list_tables()
```

```python
# Output:
['penguins']
```

There's one table, called `penguins`. We can ask Ibis to give us an object that we can interact with.

```python
penguins = con.table("penguins")
penguins
```

```text
# Output:
DatabaseTable: penguins
  species           string
  island            string
  bill_length_mm    float64
  bill_depth_mm     float64
  flipper_length_mm int64
  body_mass_g       int64
  sex               string
  year              int64
```

Ibis is lazily evaluated, so instead of seeing the data, we see the schema of the table. To peek at the data, we can call `head` and then `to_pandas` to get the first few rows of the table as a pandas DataFrame.

```python
penguins.head().to_pandas()
```

```text
  species     island  bill_length_mm  bill_depth_mm  flipper_length_mm  body_mass_g     sex  year
0  Adelie  Torgersen            39.1           18.7              181.0       3750.0    male  2007
1  Adelie  Torgersen            39.5           17.4              186.0       3800.0  female  2007
2  Adelie  Torgersen            40.3           18.0              195.0       3250.0  female  2007
3  Adelie  Torgersen             NaN            NaN                NaN          NaN    None  2007
4  Adelie  Torgersen            36.7           19.3              193.0       3450.0  female  2007
```

`to_pandas` takes the existing lazy table expression and evaluates it. If we leave it off, you'll see the Ibis representation of the table expression that `to_pandas` will evaluate (when you're ready!).

```python
penguins.head()
```

```python
# Output:
r0 := DatabaseTable: penguins
  species           string
  island            string
  bill_length_mm    float64
  bill_depth_mm     float64
  flipper_length_mm int64
  body_mass_g       int64
  sex               string
  year              int64

Limit[r0, n=5]
```

Ibis returns results as a pandas DataFrame using `to_pandas`, but isn't using pandas to perform any of the computation. The query is executed by DuckDB. Only when `to_pandas` is called does Ibis then pull back the results and convert them into a DataFrame.

## Interactive Mode

For the rest of this intro, we'll turn on interactive mode, which partially executes queries to give users a preview of the results. There is a small difference in the way the output is formatted, but otherwise this is the same as calling `to_pandas` on the table expression with a limit of 10 result rows returned.

```python
ibis.options.interactive = True
penguins.head()
```

```text
┏━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━┓
┃ species ┃ island    ┃ bill_length_mm ┃ bill_depth_mm ┃ flipper_length_mm ┃ body_mass_g ┃ sex    ┃ year  ┃
┡━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━┩
│ string  │ string    │ float64        │ float64       │ int64             │ int64       │ string │ int64 │
├─────────┼───────────┼────────────────┼───────────────┼───────────────────┼─────────────┼────────┼───────┤
│ Adelie  │ Torgersen │           39.1 │          18.7 │               181 │        3750 │ male   │  2007 │
│ Adelie  │ Torgersen │           39.5 │          17.4 │               186 │        3800 │ female │  2007 │
│ Adelie  │ Torgersen │           40.3 │          18.0 │               195 │        3250 │ female │  2007 │
│ Adelie  │ Torgersen │            nan │           nan │              NULL │        NULL │ NULL   │  2007 │
│ Adelie  │ Torgersen │           36.7 │          19.3 │               193 │        3450 │ female │  2007 │
└─────────┴───────────┴────────────────┴───────────────┴───────────────────┴─────────────┴────────┴───────┘
```

## Common Operations

Ibis has a collection of useful table methods to manipulate and query the data in a table.

### filter

`filter` allows you to select rows based on a condition or set of conditions.

We can filter so we only have penguins of the species Gentoo:

```python
penguins.filter(penguins.species == "Gentoo")
```

```text
┏━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━┓
┃ species ┃ island ┃ bill_length_mm ┃ bill_depth_mm ┃ flipper_length_mm ┃ body_mass_g ┃ sex    ┃ year  ┃
┡━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━┩
│ string  │ string │ float64        │ float64       │ int64             │ int64       │ string │ int64 │
├─────────┼────────┼────────────────┼───────────────┼───────────────────┼─────────────┼────────┼───────┤
│ Gentoo  │ Biscoe │           46.1 │          13.2 │               211 │        4500 │ female │  2007 │
│ Gentoo  │ Biscoe │           50.0 │          16.3 │               230 │        5700 │ male   │  2007 │
│ Gentoo  │ Biscoe │           48.7 │          14.1 │               210 │        4450 │ female │  2007 │
│ Gentoo  │ Biscoe │           50.0 │          15.2 │               218 │        5700 │ male   │  2007 │
│ Gentoo  │ Biscoe │           47.6 │          14.5 │               215 │        5400 │ male   │  2007 │
│ Gentoo  │ Biscoe │           46.5 │          13.5 │               210 │        4550 │ female │  2007 │
│ Gentoo  │ Biscoe │           45.4 │          14.6 │               211 │        4800 │ female │  2007 │
│ Gentoo  │ Biscoe │           46.7 │          15.3 │               219 │        5200 │ male   │  2007 │
│ Gentoo  │ Biscoe │           43.3 │          13.4 │               209 │        4400 │ female │  2007 │
│ Gentoo  │ Biscoe │           46.8 │          15.4 │               215 │        5150 │ male   │  2007 │
│ …       │ …      │              … │             … │                 … │           … │ …      │     … │
└─────────┴────────┴────────────────┴───────────────┴───────────────────┴─────────────┴────────┴───────┘
```

Or filter for Gentoo penguins that have a body mass larger than 6 kg.

```python
penguins.filter((penguins.species == "Gentoo") & (penguins.body_mass_g > 6000))
```

```text
┏━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━┓
┃ species ┃ island ┃ bill_length_mm ┃ bill_depth_mm ┃ flipper_length_mm ┃ body_mass_g ┃ sex    ┃ year  ┃
┡━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━┩
│ string  │ string │ float64        │ float64       │ int64             │ int64       │ string │ int64 │
├─────────┼────────┼────────────────┼───────────────┼───────────────────┼─────────────┼────────┼───────┤
│ Gentoo  │ Biscoe │           49.2 │          15.2 │               221 │        6300 │ male   │  2007 │
│ Gentoo  │ Biscoe │           59.6 │          17.0 │               230 │        6050 │ male   │  2007 │
└─────────┴────────┴────────────────┴───────────────┴───────────────────┴─────────────┴────────┴───────┘
```

You can use any Boolean comparison in a filter (although if you try to do something like use `<` on a string, Ibis will yell at you).

### select

Your data analysis might not require all the columns present in a given table. `select` lets you pick out only those columns that you want to work with.

To select a column you can use the name of the column as a string:

```python
penguins.select("species", "island", "year").limit(3)
```

```text
┏━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━┓
┃ species ┃ island    ┃ year  ┃
┡━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━┩
│ string  │ string    │ int64 │
├─────────┼───────────┼───────┤
│ Adelie  │ Torgersen │  2007 │
│ Adelie  │ Torgersen │  2007 │
│ Adelie  │ Torgersen │  2007 │
│ …       │ …         │     … │
└─────────┴───────────┴───────┘
```

Or you can use column objects directly (this can be convenient when paired with tab-completion):

```python
penguins.select(penguins.species, penguins.island, penguins.year).limit(3)
```

```text
┏━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━┓
┃ species ┃ island    ┃ year  ┃
┡━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━┩
│ string  │ string    │ int64 │
├─────────┼───────────┼───────┤
│ Adelie  │ Torgersen │  2007 │
│ Adelie  │ Torgersen │  2007 │
│ Adelie  │ Torgersen │  2007 │
│ …       │ …         │     … │
└─────────┴───────────┴───────┘
```

Or you can mix-and-match:

```python
penguins.select("species", "island", penguins.year).limit(3)
```

```text
┏━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━┓
┃ species ┃ island    ┃ year  ┃
┡━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━┩
│ string  │ string    │ int64 │
├─────────┼───────────┼───────┤
│ Adelie  │ Torgersen │  2007 │
│ Adelie  │ Torgersen │  2007 │
│ Adelie  │ Torgersen │  2007 │
│ …       │ …         │     … │
└─────────┴───────────┴───────┘
```

### mutate

`mutate` lets you add new columns to your table, derived from the values of existing columns.

```python
penguins.mutate(bill_length_cm=penguins.bill_length_mm / 10)
```

```text
┏━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ species ┃ island    ┃ bill_length_mm ┃ bill_depth_mm ┃ flipper_length_mm ┃ body_mass_g ┃ sex    ┃ year  ┃ bill_length_cm ┃
┡━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ string  │ string    │ float64        │ float64       │ int64             │ int64       │ string │ int64 │ float64        │
├─────────┼───────────┼────────────────┼───────────────┼───────────────────┼─────────────┼────────┼───────┼────────────────┤
│ Adelie  │ Torgersen │           39.1 │          18.7 │               181 │        3750 │ male   │  2007 │           3.91 │
│ Adelie  │ Torgersen │           39.5 │          17.4 │               186 │        3800 │ female │  2007 │           3.95 │
│ Adelie  │ Torgersen │           40.3 │          18.0 │               195 │        3250 │ female │  2007 │           4.03 │
│ Adelie  │ Torgersen │            nan │           nan │              NULL │        NULL │ NULL   │  2007 │            nan │
│ Adelie  │ Torgersen │           36.7 │          19.3 │               193 │        3450 │ female │  2007 │           3.67 │
│ Adelie  │ Torgersen │           39.3 │          20.6 │               190 │        3650 │ male   │  2007 │           3.93 │
│ Adelie  │ Torgersen │           38.9 │          17.8 │               181 │        3625 │ female │  2007 │           3.89 │
│ Adelie  │ Torgersen │           39.2 │          19.6 │               195 │        4675 │ male   │  2007 │           3.92 │
│ Adelie  │ Torgersen │           34.1 │          18.1 │               193 │        3475 │ NULL   │  2007 │           3.41 │
│ Adelie  │ Torgersen │           42.0 │          20.2 │               190 │        4250 │ NULL   │  2007 │           4.20 │
│ …       │ …         │              … │             … │                 … │           … │ …      │     … │              … │
└─────────┴───────────┴────────────────┴───────────────┴───────────────────┴─────────────┴────────┴───────┴────────────────┘
```

Notice that the table is a little too wide to display all the columns now (depending on your screen-size). `bill_length` is now present in millimeters _and_ centimeters. Use a `select` to trim down the number of columns we're looking at.

```python
penguins.mutate(bill_length_cm=penguins.bill_length_mm / 10).select(
    "species",
    "island",
    "bill_depth_mm",
    "flipper_length_mm",
    "body_mass_g",
    "sex",
    "year",
    "bill_length_cm",
)
```

```text
┏━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ species ┃ island    ┃ bill_depth_mm ┃ flipper_length_mm ┃ body_mass_g ┃ sex    ┃ year  ┃ bill_length_cm ┃
┡━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ string  │ string    │ float64       │ int64             │ int64       │ string │ int64 │ float64        │
├─────────┼───────────┼───────────────┼───────────────────┼─────────────┼────────┼───────┼────────────────┤
│ Adelie  │ Torgersen │          18.7 │               181 │        3750 │ male   │  2007 │           3.91 │
│ Adelie  │ Torgersen │          17.4 │               186 │        3800 │ female │  2007 │           3.95 │
│ Adelie  │ Torgersen │          18.0 │               195 │        3250 │ female │  2007 │           4.03 │
│ Adelie  │ Torgersen │           nan │              NULL │        NULL │ NULL   │  2007 │            nan │
│ Adelie  │ Torgersen │          19.3 │               193 │        3450 │ female │  2007 │           3.67 │
│ Adelie  │ Torgersen │          20.6 │               190 │        3650 │ male   │  2007 │           3.93 │
│ Adelie  │ Torgersen │          17.8 │               181 │        3625 │ female │  2007 │           3.89 │
│ Adelie  │ Torgersen │          19.6 │               195 │        4675 │ male   │  2007 │           3.92 │
│ Adelie  │ Torgersen │          18.1 │               193 │        3475 │ NULL   │  2007 │           3.41 │
│ Adelie  │ Torgersen │          20.2 │               190 │        4250 │ NULL   │  2007 │           4.20 │
│ …       │ …         │             … │                 … │           … │ …      │     … │              … │
└─────────┴───────────┴───────────────┴───────────────────┴─────────────┴────────┴───────┴────────────────┘
```

### selectors

Typing out _all_ of the column names _except_ one is a little annoying. Instead of doing that again, we can use a `selector` to quickly select or deselect groups of columns.

```python
import ibis.selectors as s

penguins.mutate(bill_length_cm=penguins.bill_length_mm / 10).select(
    ~s.matches("bill_length_mm")
    # match every column except `bill_length_mm`
)
```

```text
┏━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ species ┃ island    ┃ bill_depth_mm ┃ flipper_length_mm ┃ body_mass_g ┃ sex    ┃ year  ┃ bill_length_cm ┃
┡━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ string  │ string    │ float64       │ int64             │ int64       │ string │ int64 │ float64        │
├─────────┼───────────┼───────────────┼───────────────────┼─────────────┼────────┼───────┼────────────────┤
│ Adelie  │ Torgersen │          18.7 │               181 │        3750 │ male   │  2007 │           3.91 │
│ Adelie  │ Torgersen │          17.4 │               186 │        3800 │ female │  2007 │           3.95 │
│ Adelie  │ Torgersen │          18.0 │               195 │        3250 │ female │  2007 │           4.03 │
│ Adelie  │ Torgersen │           nan │              NULL │        NULL │ NULL   │  2007 │            nan │
│ Adelie  │ Torgersen │          19.3 │               193 │        3450 │ female │  2007 │           3.67 │
│ Adelie  │ Torgersen │          20.6 │               190 │        3650 │ male   │  2007 │           3.93 │
│ Adelie  │ Torgersen │          17.8 │               181 │        3625 │ female │  2007 │           3.89 │
│ Adelie  │ Torgersen │          19.6 │               195 │        4675 │ male   │  2007 │           3.92 │
│ Adelie  │ Torgersen │          18.1 │               193 │        3475 │ NULL   │  2007 │           3.41 │
│ Adelie  │ Torgersen │          20.2 │               190 │        4250 │ NULL   │  2007 │           4.20 │
│ …       │ …         │             … │                 … │           … │ …      │     … │              … │
└─────────┴───────────┴───────────────┴───────────────────┴─────────────┴────────┴───────┴────────────────┘
```

You can also use a `selector` alongside a column name.

```python
penguins.select("island", s.numeric())
```

```text
┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ island    ┃ bill_length_mm ┃ bill_depth_mm ┃ flipper_length_mm ┃ body_mass_g ┃ year  ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│ string    │ float64        │ float64       │ int64             │ int64       │ int64 │
├───────────┼────────────────┼───────────────┼───────────────────┼─────────────┼───────┤
│ Torgersen │           39.1 │          18.7 │               181 │        3750 │  2007 │
│ Torgersen │           39.5 │          17.4 │               186 │        3800 │  2007 │
│ Torgersen │           40.3 │          18.0 │               195 │        3250 │  2007 │
│ Torgersen │            nan │           nan │              NULL │        NULL │  2007 │
│ Torgersen │           36.7 │          19.3 │               193 │        3450 │  2007 │
│ Torgersen │           39.3 │          20.6 │               190 │        3650 │  2007 │
│ Torgersen │           38.9 │          17.8 │               181 │        3625 │  2007 │
│ Torgersen │           39.2 │          19.6 │               195 │        4675 │  2007 │
│ Torgersen │           34.1 │          18.1 │               193 │        3475 │  2007 │
│ Torgersen │           42.0 │          20.2 │               190 │        4250 │  2007 │
│ …         │              … │             … │                 … │           … │     … │
└───────────┴────────────────┴───────────────┴───────────────────┴─────────────┴───────┘
```

You can read more about [`selectors`](https://ibis-project.org/reference/selectors/) in the docs!

### `order_by`

`order_by` arranges the values of one or more columns in ascending or descending order.

By default, `ibis` sorts in ascending order:

```python
penguins.order_by(penguins.flipper_length_mm).select(
    "species", "island", "flipper_length_mm"
)
```

```text
┏━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┓
┃ species   ┃ island    ┃ flipper_length_mm ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━┩
│ string    │ string    │ int64             │
├───────────┼───────────┼───────────────────┤
│ Adelie    │ Biscoe    │               172 │
│ Adelie    │ Biscoe    │               174 │
│ Adelie    │ Torgersen │               176 │
│ Adelie    │ Dream     │               178 │
│ Adelie    │ Dream     │               178 │
│ Adelie    │ Dream     │               178 │
│ Chinstrap │ Dream     │               178 │
│ Adelie    │ Dream     │               179 │
│ Adelie    │ Torgersen │               180 │
│ Adelie    │ Biscoe    │               180 │
│ …         │ …         │                 … │
└───────────┴───────────┴───────────────────┘
```

You can sort in descending order using the `desc` method of a column:

```python
penguins.order_by(penguins.flipper_length_mm.desc()).select(
    "species", "island", "flipper_length_mm"
)
```

```text
┏━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┓
┃ species ┃ island ┃ flipper_length_mm ┃
┡━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━┩
│ string  │ string │ int64             │
├─────────┼────────┼───────────────────┤
│ Gentoo  │ Biscoe │               231 │
│ Gentoo  │ Biscoe │               230 │
│ Gentoo  │ Biscoe │               230 │
│ Gentoo  │ Biscoe │               230 │
│ Gentoo  │ Biscoe │               230 │
│ Gentoo  │ Biscoe │               230 │
│ Gentoo  │ Biscoe │               230 │
│ Gentoo  │ Biscoe │               230 │
│ Gentoo  │ Biscoe │               229 │
│ Gentoo  │ Biscoe │               229 │
│ …       │ …      │                 … │
└─────────┴────────┴───────────────────┘
```

Or you can use `ibis.desc`

```python
penguins.order_by(ibis.desc("flipper_length_mm")).select(
    "species", "island", "flipper_length_mm"
)
```

```text
┏━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┓
┃ species ┃ island ┃ flipper_length_mm ┃
┡━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━┩
│ string  │ string │ int64             │
├─────────┼────────┼───────────────────┤
│ Gentoo  │ Biscoe │               231 │
│ Gentoo  │ Biscoe │               230 │
│ Gentoo  │ Biscoe │               230 │
│ Gentoo  │ Biscoe │               230 │
│ Gentoo  │ Biscoe │               230 │
│ Gentoo  │ Biscoe │               230 │
│ Gentoo  │ Biscoe │               230 │
│ Gentoo  │ Biscoe │               230 │
│ Gentoo  │ Biscoe │               229 │
│ Gentoo  │ Biscoe │               229 │
│ …       │ …      │                 … │
└─────────┴────────┴───────────────────┘
```

### aggregate

Ibis has several aggregate functions available to help summarize data.

`mean`, `max`, `min`, `count`, `sum` (the list goes on).

To aggregate an entire column, call the corresponding method on that column.

```python
penguins.flipper_length_mm.mean()
```

```python
# Output:
200.91520467836258
```

You can compute multiple aggregates at once using the `aggregate` method:

```python
penguins.aggregate([penguins.flipper_length_mm.mean(), penguins.bill_depth_mm.max()])
```

```text
┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┓
┃ Mean(flipper_length_mm) ┃ Max(bill_depth_mm) ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━┩
│ float64                 │ float64            │
├─────────────────────────┼────────────────────┤
│              200.915205 │               21.5 │
└─────────────────────────┴────────────────────┘
```

But `aggregate` _really_ shines when it's paired with `group_by`.

### `group_by`

`group_by` creates groupings of rows that have the same value for one or more columns.

But it doesn't do much on its own -- you can pair it with `aggregate` to get a result.

```python
penguins.group_by("species").aggregate()
```

```text
┏━━━━━━━━━━━┓
┃ species   ┃
┡━━━━━━━━━━━┩
│ string    │
├───────────┤
│ Adelie    │
│ Gentoo    │
│ Chinstrap │
└───────────┘
```

We grouped by the `species` column and handed it an “empty” aggregate command. The result of that is a column of the unique values in the `species` column.

If we add a second column to the `group_by`, we'll get each unique pairing of the values in those columns.

```python
penguins.group_by(["species", "island"]).aggregate()
```

```text
┏━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ species   ┃ island    ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━┩
│ string    │ string    │
├───────────┼───────────┤
│ Adelie    │ Torgersen │
│ Adelie    │ Biscoe    │
│ Adelie    │ Dream     │
│ Gentoo    │ Biscoe    │
│ Chinstrap │ Dream     │
└───────────┴───────────┘
```

Now, if we add an aggregation function to that, we start to really open things up.

```python
penguins.group_by(["species", "island"]).aggregate(penguins.bill_length_mm.mean())
```

```text
┏━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃ species   ┃ island    ┃ Mean(bill_length_mm) ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
│ string    │ string    │ float64              │
├───────────┼───────────┼──────────────────────┤
│ Adelie    │ Torgersen │            38.950980 │
│ Adelie    │ Biscoe    │            38.975000 │
│ Adelie    │ Dream     │            38.501786 │
│ Gentoo    │ Biscoe    │            47.504878 │
│ Chinstrap │ Dream     │            48.833824 │
└───────────┴───────────┴──────────────────────┘
```

By adding that `mean` to the `aggregate`, we now have a concise way to calculate aggregates over each of the distinct groups in the `group_by`. And we can calculate as many aggregates as we need.

```python
penguins.group_by(["species", "island"]).aggregate(
    [penguins.bill_length_mm.mean(), penguins.flipper_length_mm.max()]
)
```

```text
┏━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ species   ┃ island    ┃ Mean(bill_length_mm) ┃ Max(flipper_length_mm) ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│ string    │ string    │ float64              │ int64                  │
├───────────┼───────────┼──────────────────────┼────────────────────────┤
│ Adelie    │ Torgersen │            38.950980 │                    210 │
│ Adelie    │ Biscoe    │            38.975000 │                    203 │
│ Adelie    │ Dream     │            38.501786 │                    208 │
│ Gentoo    │ Biscoe    │            47.504878 │                    231 │
│ Chinstrap │ Dream     │            48.833824 │                    212 │
└───────────┴───────────┴──────────────────────┴────────────────────────┘
```

If we need more specific groups, we can add to the `group_by`.

```python
penguins.group_by(["species", "island", "sex"]).aggregate(
    [penguins.bill_length_mm.mean(), penguins.flipper_length_mm.max()]
)
```

```text
┏━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ species ┃ island    ┃ sex    ┃ Mean(bill_length_mm) ┃ Max(flipper_length_mm) ┃
┡━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│ string  │ string    │ string │ float64              │ int64                  │
├─────────┼───────────┼────────┼──────────────────────┼────────────────────────┤
│ Adelie  │ Torgersen │ male   │            40.586957 │                    210 │
│ Adelie  │ Torgersen │ female │            37.554167 │                    196 │
│ Adelie  │ Torgersen │ NULL   │            37.925000 │                    193 │
│ Adelie  │ Biscoe    │ female │            37.359091 │                    199 │
│ Adelie  │ Biscoe    │ male   │            40.590909 │                    203 │
│ Adelie  │ Dream     │ female │            36.911111 │                    202 │
│ Adelie  │ Dream     │ male   │            40.071429 │                    208 │
│ Adelie  │ Dream     │ NULL   │            37.500000 │                    179 │
│ Gentoo  │ Biscoe    │ female │            45.563793 │                    222 │
│ Gentoo  │ Biscoe    │ male   │            49.473770 │                    231 │
│ …       │ …         │ …      │                    … │                      … │
└─────────┴───────────┴────────┴──────────────────────┴────────────────────────┘
```

## Chaining It All Together

We've already chained some Ibis calls together. We used `mutate` to create a new column and then `select` to only view a subset of the new table. We were just chaining `group_by` with `aggregate`.

There's nothing stopping us from putting all of these concepts together to ask questions of the data.

How about:

* What was the largest female penguin (by body mass) on each island in the year 2008?

```python
penguins.filter((penguins.sex == "female") & (penguins.year == 2008)).group_by(
    ["island"]
).aggregate(penguins.body_mass_g.max())
```

```text
┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ island    ┃ Max(body_mass_g) ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ string    │ int64            │
├───────────┼──────────────────┤
│ Biscoe    │             5200 │
│ Torgersen │             3800 │
│ Dream     │             3900 │
└───────────┴──────────────────┘
```

* What about the largest male penguin (by body mass) on each island for each year of data collection?

```python
penguins.filter(penguins.sex == "male").group_by(["island", "year"]).aggregate(
    penguins.body_mass_g.max().name("max_body_mass")
).order_by(["year", "max_body_mass"])
```

```text
┏━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ island    ┃ year  ┃ max_body_mass ┃
┡━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━┩
│ string    │ int64 │ int64         │
├───────────┼───────┼───────────────┤
│ Dream     │  2007 │          4650 │
│ Torgersen │  2007 │          4675 │
│ Biscoe    │  2007 │          6300 │
│ Torgersen │  2008 │          4700 │
│ Dream     │  2008 │          4800 │
│ Biscoe    │  2008 │          6000 │
│ Torgersen │  2009 │          4300 │
│ Dream     │  2009 │          4475 │
│ Biscoe    │  2009 │          6000 │
└───────────┴───────┴───────────────┘
```

## Learn More

That's all for this quick-start guide. If you want to learn more, check out the [Ibis documentation](https://ibis-project.org).
