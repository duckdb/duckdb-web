---
layout: docu
title: Rill Data Developer
selected: Rill Data Developer
---

## What is Rill? 

Rill Developer makes it effortless to transform your datasets with SQL and create powerful, opinionated dashboards. Rill's principles:

- _**feels good to use**_ – powered by Sveltekit & DuckDB = conversation-fast, not wait-ten-seconds-for-result-set fast
- _**works with your local and remote datasets**_ – imports and exports Parquet and CSV (s3, gcs, https, local)
- _**no more data analysis "side-quests"**_ – helps you build intuition about your dataset through automatic profiling
- _**no "run query" button required**_ – responds to each keystroke by re-profiling the resulting dataset
- _**radically simple dashboards**_ – thoughtful, opinionated defaults to help you quickly derive insights from your data
- _**dashboards as code**_ – each step from data to dashboard has versioning, git sharing, and easy project rehydration 

## Install
You can get started in less than 2 minutes with Rill's installation script (Mac and Linux):
```
curl -s https://cdn.rilldata.com/install.sh | bash
```

See [Rill's documentation](https://docs.rilldata.com) for more information about using Rill.

![home-demo](https://user-images.githubusercontent.com/5587788/180313797-ef50ec6e-fc2d-4072-bb77-b2acf59205d7.gif "770784519")


## Creating a project

In Rill, all data sources, data models, and dashboard definitions are saved as Rill project files on disk. You can edit these directly or check them into Git to share your project with others.

For this tutorial, let's checkout an example project from the git repository:

```
git clone https://github.com/rilldata/rill-developer-example.git
cd rill-developer-example
```

Alternatively, you can create a new, empty Rill project:

```
rill init --project my-project
cd my-project
```

## Starting the application

Now it's time to start the application:

```
rill start
```

When you run `rill start`, it parses your project and ingests any missing data sources into a local DuckDB database. After your project has been re-hydrated, it starts the Rill web app on `http://localhost:9009`.

![dashboards-are-code](https://user-images.githubusercontent.com/5587788/207376626-20af5eb9-3c47-47f9-ba7f-8163110d6a04.gif "780773077")


## Editing and sharing a project

You can use the Rill web app to add or edit data sources, data models, and dashboards. All changes you make in the UI and CLI are versionable because they are reflected as Rill project files stored on disk. You can share your Rill project files with others by pushing to a shared repository, and they'll be able to completely recreate your project just by running `rill start`.

Have fun exploring Rill!

![http-remote-source](https://user-images.githubusercontent.com/5587788/200923188-436ffd76-0a27-4b02-a713-1a5afbb0ddb2.gif "769076584")


## Rill wants to hear from you

You can [file an issue](https://github.com/rilldata/rill-developer/issues/new/choose) directly in Rill's repository or reach Rill in their [discord](https://bit.ly/3unvA05) channel. Please abide by the [rill community policy](https://github.com/rilldata/rill-developer/blob/main/COMMUNITY-POLICY.md).
