---
layout: post
title: "Reading and Writing Google Sheets in DuckDB"
author: "Archie Wood and Alex Monahan"
# thumb: "/images/blog/thumbs/union-all-by-name.svg"
# image: "/images/blog/thumbs/union-all-by-name.png"
excerpt: "The GSheets extension allows DuckDB to read from and write to Google Sheets. Authentication is as easy as logging into Google in a browser."
tags: ["using DuckDB"]
---

## Spreadsheets Are Everywhere

Is anything more polarizing for data folks than spreadsheets? 
Wait, don't answer that, we don't have time to talk about leading and trailing commas again...

The fact is that spreadsheets are everywhere. 
Love them or hate them, they are key enablers of business across the globe.
It is estimated that there are over an order of magnitude more spreadsheet users than programmers (of all languages put together). 

Now, you can use DuckDB to seamlessly bridge the gap between data-y folks and business-y folks!
With a simple in-browser authentication flow, or an automateable Python flow, you can both query from and load into Google Sheets.

## Benefits

There are a number of ways that using a spreadsheet can improve a data workflow.
Blasphemy you say! 
Well, imagine if your database could actually read those spreadsheets.

Spreadsheets are often the best place to manually edit data.
Marketing may have a custom-built list of users that need to be enrolled in a specific campaign.
Engineering might have several batches of product that should receive extra quality checks.
Don't forget the custom calculations from the finance team that need to be accounted for in the automated dashboards owned by the data team.
Pulling from a Google Sheet is likely much easier than granting access to S3 or another central shared file location.
And your future self would really prefer that you not add them all into a giant `CASE WHEN` statement. 

The benefits quickly accumulate once those teams' data can be ingested into existing data engineering or data science workflows.
Dashboards begin to actually reflect the reality of the business.
Business processes that used to require days of error-prone manual spreadsheet manipulation can become scheduled SQL or dbt scripts in source control. 

There are also great ways to take advantage of writing into Google Sheets. 
Often, the output of a data workflow is used to inform business decision making.
This is especially true with machine learning or forecasting processes (oh, sorry, I seem to have misspelled AI).
The consumers of the analysis have the final say and often adjust the forecast with data sources that the model did not account for.
"I talked with the CEO of that company last week and they are changing their strategy in this way."
Good luck getting that insight into your model without a spreadsheet!
Spreadsheets are a powerful way to collect the adjustments made to that data.
Those decisions could even be re-ingested so that the forecast can be improved over time.
"The predictions for products in this category tend to always get adjusted. 
What other data sources should we pull in to improve our model?"

Storing configuration information in a Google Sheet might be much easier and faster to edit than a file in git (and the history is still saved!).
This is especially true if the configuration needs to be edited by multiple people at once.
Do you really want to have to teach all of your stakeholders how to handle git merge conflicts?

There are many simpler use cases as well: data validation, data annotation, checklists, communication with external teams, dummy dataset generation, etc.
Maybe pushing and pulling directly to Google Sheets will get folks to stop having to click "export to csv" on your team's dashboards!

## Getting Started with the GSheets Extension

Querying data from a Google Sheet can be as easy as:

```sql
INSTALL gsheets FROM community;
LOAD gsheets;

-- Authenticate with Google Account in the browser (default)
CREATE SECRET (TYPE gsheet);
```

As a part of the `CREATE SECRET` command, a browser window will open and allow for a login and copying a temporary token to then paste back into DuckDB.

<!-- 

SCREENSHOTS 

-->

Now that you are authenticated, DuckDB can query any Sheet that your Google account has access to.

```sql
-- Copy the URL of the Sheet to query
FROM read_gsheet('https://docs.google.com/spreadsheets/d/...');
```

Or, you can write the results of any DuckDB query to a Google Sheet!

> The entire Sheet will be replaced with the output of the query, starting in cell A1.

```sql
COPY (
    SELECT * FROM ...
) TO 'https://docs.google.com/spreadsheets/d/...' (FORMAT gsheet);
```

### Automated Workflows

If you want to schedule an interaction with Google Sheets, a private key will be needed instead of the in browser authentication method.
The process to acquire this private key has a number of steps, but the README in the GSheets extension repo has a clear set of instructions.
However, this persistent key must be converted to a temporary token every hour or so.
The Python script below can complete that conversion and load it into a DuckDB Secret.

```python
import duckdb 
from google.oauth2 import service_account
from google.auth.transport.requests import Request

def get_token_from_user_file(user_file_path):
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

    credentials = service_account.Credentials.from_service_account_file(
        user_file_path,
        scopes=SCOPES
        )

    request = Request()
    credentials.refresh(request)
    return credentials.token

def set_gsheet_secret(duckdb_con, user_file_path):
    token = get_token_from_user_file(user_file_path)
    duckdb_con.sql(f"""
        create or replace secret gsheet_secret (
            TYPE gsheet,
            token '{token}'
        )""")

duckdb_con = duckdb.connect()
duckdb_con.sql("""
    INSTALL gsheets FROM community;
    LOAD gsheets;
""")

# The user_file_path points to the private key JSON file pulled from Google 
# (See the GSheets extension README for details)
user_file_path = "credentials.json"
set_gsheet_secret(duckdb_con, user_file_path)

# Query away!
```

## Developing the Extension

The Google Sheets extension is a good example of how DuckDB's extension GitHub template and CI/CD workflows can let even non-C++ experts contribute to the community!
Neither of us would be considered "C++ programmers", but the combination of a great template, examples from other extensions, and a little help from some LLM-powered junior devs made it possible.
We encourage you to give your extension idea a shot and reach out on Discord if you need some help!

## Roadmap


## Closing Thoughts

Happy analyzing!
