---
layout: post
title: "Reading and Writing Google Sheets in DuckDB"
author: "Alex Monahan and Archie Wood"
# thumb: "/images/blog/thumbs/union-all-by-name.svg"
# image: "/images/blog/thumbs/union-all-by-name.png"
excerpt: "Read from and write to Google Sheets directly in DuckDB! For ad hoc querying, authentication is as easy as logging into Google from a browser. Scheduled workflows can use persistent DuckDB Secrets. SQL-on-Sheets has arrived!"
tags: ["using DuckDB"]
---

## Spreadsheets Are Everywhere

Is anything more polarizing for data folks than spreadsheets? 
Wait, don't answer that, we don't have time to talk about leading and trailing commas again...

The fact is that spreadsheets are everywhere. 
It is estimated that there are over [750 million spreadsheet users](https://thenewstack.io/microsoft-excel-becomes-a-programming-language/), compared to just [20](https://www.jetbrains.com/lp/devecosystem-data-playground/#global_population) to [30 million programmers](https://www.statista.com/statistics/627312/worldwide-developer-population/) (that's all languages put together). 

Now, you can use DuckDB to seamlessly bridge the gap between data-y folks and business-y folks!
With a simple in-browser authentication flow, or an automateable private key file flow, you can both query from and load into Google Sheets.

Feel free to have a look at the [GSheets extension repo](https://github.com/evidence-dev/duckdb_gsheets) or jump to [the examples](#getting-started-with-the-gsheets-extension)!

## Benefits

There are a number of ways that using a spreadsheet can improve a data workflow.
Blasphemy you say! 
Well, imagine if your database could actually read those spreadsheets.

### Reading from Sheets

#### Manual Data Entry

Spreadsheets are often the best place to manually edit data.
Marketing may have a custom-built list of users that need to be enrolled in a specific campaign.
Don't forget the custom calculations from the finance team that need to be accounted for in the automated dashboards owned by the data team.
Pulling from a Google Sheet is likely much easier than granting access to S3 or another central shared file location.

#### Config Files Without Git

Storing configuration information in a Google Sheet might be much easier and faster to edit than a file in git (and the history is still saved!).
This is especially true if the configuration needs to be edited by multiple people at once.
Do you really want to have to teach all of your stakeholders how to handle git merge conflicts?

#### Dashboards that Reflect Reality

The benefits quickly accumulate once those teams' data can be ingested into existing data engineering or data science workflows.
Dashboards begin to actually reflect the reality of the business.
Business processes that used to require days of error-prone manual spreadsheet manipulation can become scheduled SQL or dbt scripts in source control. 

### Writing to Sheets 

Often, the output of a data workflow is used to inform business decision making.
This is especially true with machine learning or forecasting processes (oh, sorry, I seem to have misspelled AI).
"I talked with the CEO of that company last week and they are changing their strategy in this way."
Good luck getting that insight into your model without a spreadsheet!
Those decisions could even be re-ingested into DuckDB so that the forecast can be improved over time.

There are many simpler use cases as well: data validation, data annotation, checklists, communication with external teams, dummy dataset generation, and more.
Maybe pushing directly to Google Sheets will get folks to stop having to click "export to csv" on your team's dashboards!

## Getting Started with the GSheets Extension

The first few steps are to install the extension and authenticate with Google.

```sql
INSTALL gsheets FROM community;
LOAD gsheets;

-- Authenticate with a Google Account in the browser (default)
CREATE SECRET (TYPE gsheet);
```

As a part of the `CREATE SECRET` command, a browser window will open and allow for a login and copying a temporary token to then paste back into DuckDB.

<img src="/images/blog/gsheets_oauth_browser_screenshot.png"
     alt="In-browser OAuth flow to generate token."
     width="680"
     />

## Examples of Reading from Sheets

Now that you are authenticated, DuckDB can query any Sheet that your Google account has access to.
This includes any publicly available sheets like the one below, so give it a run!

```sql
FROM 'https://docs.google.com/spreadsheets/d/1B4RFuOnZ4ITZ-nR9givZ7vWVOTVddC3VTKuSqgifiyE/edit?gid=0#gid=0';
```

|                 Gotham Wisdom                  |
|------------------------------------------------|
| You either die a hero                          |
| or live long enough to query from spreadsheets |

Copy the URL of the Sheet to query when viewing the sheet of interest within the workbook.
The 'gid' query string parameter is the id of that specific sheet.

There are 2 ways to pass in additional parameters.
You may either add them to the end of the URL as query string parameters, or use the `read_gsheet` table function and specify them as separate SQL parameters.
The repo README has a variety of examples and some are included below!

> Query string parameters must be placed after a `?`.
> Each parameter is formatted as a `key=value` pair, and multiple are separated with `&`.

### Reading a Specific Sheet and Range

By default, the GSheets extension will read all data on the first sheet in the workbook.
The `sheet` and `range` parameters (or their query string equivalents) allow for targeted reads.

For example, to read only the first 3 cells on the `We <3 Ducks` sheet, these two statements are equivalent:

```sql
-- The sheet with the gid of 0 is named 'We <3 Ducks' (because of course it is!)
FROM read_gsheet(
    'https://docs.google.com/spreadsheets/d/1B4RFuOnZ4ITZ-nR9givZ7vWVOTVddC3VTKuSqgifiyE/edit',
    sheet = 'We <3 Ducks',
    range = 'A1:A3'
    );

FROM 'https://docs.google.com/spreadsheets/d/1B4RFuOnZ4ITZ-nR9givZ7vWVOTVddC3VTKuSqgifiyE/edit?gid=0#gid=0&range=A1:A3';
```

The Google Sheets API helpfully skips empty rows at the end of a dataset or empty columns to the right.
Feel free to specify a slightly bigger `range` if your data may grow!
Additionally, the `range` can be specified as a set of columns (e.g. `D:X`) to be friendlier to a variable number of rows.

### Data Types

The extension will sample the first row of data in the sheet to attempt to determine the data types of the columns.
(We have plans to improve this sampling and are open to contributions!) 
To skip this step and define the data types within SQL, set the `all_varchar` parameter to `true`.
The example below also demonstrates that the full URL is not needed - only the Google Workbook identifier.

```sql
FROM read_gsheet(
    '1B4RFuOnZ4ITZ-nR9givZ7vWVOTVddC3VTKuSqgifiyE',
    sheet = 'We <3 Ducks',
    range = 'A:A',
    all_varchar = true
    );
```

It is also possible to query data without a header row by setting the `header` parameter to false.
Columns will be given default names and can be renamed in SQL.

## Examples of Writing to a GSheet

Another key capability of the GSheets extension is to write the results of any DuckDB query to a Google Sheet!

> By default, the entire Sheet will be replaced with the output of the query (including a header row for column names), starting in cell A1 of the first sheet.
> See below for examples that adjust this behavior!


```sql
-- Here you will need to specify your own Sheet to experiment with!
-- (We can't predict what folks would write to a public Sheet...
-- Probably just memes, but there is always that one person, you know?)
COPY (FROM range(10))
TO 'https://docs.google.com/spreadsheets/d/...'  (
    FORMAT gsheet
);
```

### Writing to a Specific Sheet and Range

As with reading, both query string parameters and SQL parameters can be used to write to a specific `sheet` or `range`. 
Similarly, the SQL parameters take precedence. These examples are equivalent:

```sql
COPY (FROM range(10))
TO 'https://docs.google.com/spreadsheets/d/...?' (
    FORMAT gsheet,
    sheet 'The sheet name!',
    range 'A2:Z10000'
);

COPY (FROM range(10))
TO 'https://docs.google.com/spreadsheets/d/...?gid=123#gid=123&range=A2:Z10000' (
    FORMAT gsheet
);
```

The `header` boolean parameter can also be used to determine whether the column names should be written out or not. 

### Overwriting or Appending

At times, it is helpful to avoid clearing out other data in a Sheet before copying.
This is especially handy when writing to specific ranges.
Perhaps columns C and D can come from DuckDB and the remainder can be spreadsheet formulas.
It would be great to just clear out columns C and D!

To adjust this behavior, pass in these boolean parameters to the `COPY` function.
`OVERWRITE_SHEET` is the default where the entire sheet is cleared out prior to copying.
`OVERWRITE_RANGE` will only clear out the specified range.

If both are set to `false`, then data will be appended without any other cells being cleared out.
Typically, when appending it is not desirable to include the column headers in the output.
Helpfully, the `header` parameter defaults to `false` in the append case, but it can be adjusted if needed.

```sql
-- To append, set both flags to false.
COPY (FROM range(10))
TO 'https://docs.google.com/spreadsheets/d/...?gid=123#gid=123&range=A2:Z10000' (
    FORMAT gsheet,
    OVERWRITE_SHEET = false,
    OVERWRITE_RANGE = false
    -- header = false is the default in this case!
);
```

## Automated Workflows

Working with spreadsheets is great for ad hoc work, but it can also be powerful when ingrained in automated processes.
If you want to schedule an interaction with Google Sheets, a key file containing a private key will be needed instead of the in browser authentication method.

<details markdown='1'>
<summary markdown='span'>
    The process to acquire this key file has a number of steps, outlined below. Luckily they only need to be done once! This is also available in the repo README.
</summary>

To connect DuckDB to Google Sheets via an access token, you’ll need to create a Service Account through the Google API Console. 
The GSheets extension will use it to generate an access token periodically.

1. Navigate to the [Google API Console](https://console.developers.google.com/apis/library).
2. Create a new project.
3. Search for the Google Sheets API and enable it.
4. In the left-hand navigation, go to the **Credentials** tab.
5. Click **+ Create Credentials** and select **Service Account**.
6. Name the Service Account and assign it the **Owner** role for your project. Click **Done** to save.
7. From the **Service Accounts** page, click on the Service Account you just created.
8. Go to the **Keys** tab, then click **Add Key** > **Create New Key**.
9. Choose **JSON**, then click **Create**. The JSON file will download automatically.
10. Open your Google Sheet and share it with the Service Account email.
</details>

After aquiring this key file, the persistent private key must be converted to a temporary token once every 30 minutes.
That process is now automated with the `key_file` `SECRET` `provider`.
Create the secret with a command like below, pointing to the JSON file exported from Google. 

```sql
CREATE OR REPLACE PERSISTENT SECRET my_secret (
    TYPE gsheet,
    PROVIDER key_file,
    FILEPATH 'credentials.json'
);
```

As the secret is created, the private key is stored in DuckDB and a temporary token is created.
The secret can be stored in memory or optionally persisted to disk (unencrypted) using the `PERSISTENT` keyword.
The temporary token is cached within the `SECRET` as well and is recreated if it is over 30 minutes old.

This unlocks the use of the GSheets extension within pipelines, like GitHub Actions (GHA) or other orchestrators like dbt.
The best practice is to store the `credentials.json` file as a secret within your orchestrator and write it out to a temporary file.
An [example GHA workflow is here](https://github.com/Alex-Monahan/duckdb-gsheets/blob/main/.github/workflows/python-app.yml), which uses [this Python script to query a Sheet](https://github.com/Alex-Monahan/duckdb-gsheets/blob/main/ci_scripts/set_env_vars_for_tests.py).

## Developing the Extension

The Google Sheets extension is a good example of how DuckDB's extension GitHub template and CI/CD workflows can let even non-C++ experts contribute to the community!
Several of the folks who have contributed thus far (thank you!!) would not be considered "C++ programmers", but the combination of a great template, examples from other extensions, and a little help from some LLM-powered "junior devs" made it possible.
We encourage you to give your extension idea a shot and reach out on Discord if you need some help!

## Roadmap

There are a few more fun features we are thinking about for the extension - we are open to PRs and collaborators!

We would like to use a better heuristic for detecting data types when reading from a Sheet.
The DuckDB type system is more advanced than Sheets, so it would be beneficial to be more precise.

Enabling the GSheets extension to work in Wasm would allow in-browser applications to query Sheets directly - no server needed! 
Several `http` functions need some modification to work in a browser environment.

The OAuth flow that powers the browser-based login may be useful for authenticating to other APIs.
We are wondering if maybe it would be possible to have a generic OAuth extension for DuckDB.
There are no concrete plans for this at the moment, but if anyone is interested, please reach out!

## Closing Thoughts

At MotherDuck (where Alex works), we have this extension running in production for several internal data pipelines!
We have automated exports of forecasts from our warehouse into Sheets and continually load manually collected customer support data into our (MotherDuck powered) data warehouse.
As a result, our KPI dashboards include context from folks talking directly to customers!

[Michael Harris](https://www.linkedin.com/in/mharrisb1/) has also contributed to the extension (thank you!), and [Definite](https://www.definite.app/) has deployed GSheets scheduled jobs into production for multiple customers!

Thanks to the GSheets DuckDB extension, it is easier than ever to use spreadsheets and DuckDB together.
Now go automate that Sheet with some SQL!
