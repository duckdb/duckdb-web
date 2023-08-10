---
layout: docu
title: Evidence - Business Intelligence as Code
selected: Evidence - Business Intelligence as Code
---

[Evidence](https://evidence.dev/) is an open-source, code-based alternative to drag-and-drop BI tools.

It enables you to build reports and analyses using just SQL and markdown.

![Evidence](/images/guides/evidence/code-and-preview-border.png)

## Why Evidence?

Evidence aims to enable data analysts to deliver reliable, clear, and valuable reporting products driven by live data.

It equips analysts with a higher leverage workflow than dragging-and-dropping charts and filters onto a dashboard:

- **Code-driven workflows**: Use your IDE, version control, and CI/CD tools
- **First-class text support**: Add context, explanation and insight to your reports using markdown
- **Control structures**: Use loops, conditionals, and templated pages to create content from data
- **Performance**: Evidence projects build into fast and reliable web application
- **Lightweight setup**: Install locally and start building reports immediately

## Install & Run

1. Download Evidence from the [VSCode Marketplace](https://marketplace.visualstudio.com/items?itemName=Evidence.evidence-vscode)
1. In the Command Palette (F1) enter `Evidence: New Evidence Project`
1. Click `Start Evidence` in the status bar (bottom left)

[Other install options](https://docs.evidence.dev/getting-started/install-evidence): Command line, Docker, and alongside dbt.


## Connect DuckDB

You can connect Evidence to a local database or Motherduck. Evidence also comes with a pre-installed local duckdb database `needful_things.duckdb`. 

### Local DB

1. Add your `.duckdb` file to the root of your project
2. Open the Evidence settings menu ([http://localhost:3000/settings](http://localhost:3000/settings))
3. Select DuckDB, and enter the name of your database file

### Motherduck

1. Retrieve your Motherduck [service token](https://motherduck.com/docs/authenticating-to-motherduck/#authentication-using-a-service-token)
2. Open the Evidence settings menu ([http://localhost:3000/settings](http://localhost:3000/settings))
3. Select DuckDB and enter `md:?motherduck_token=<your_token>` (No extension)

![Connect to DuckDB](/images/guides/evidence/connect-duckdb.png)

## Publish

You can host your Evidence project on [Netlify](https://docs.evidence.dev/deployment/netlify) or [Vercel](https://docs.evidence.dev/deployment/vercel). [Evidence Cloud](https://docs.evidence.dev/deployment/netlify) offers authentication, scheduled refreshing and other enterprise features.

## Support

If you need help or encounter an issue:
- Read the [Evidence docs](https://docs.evidence.dev/)
- Message the team on [Slack](https://join.slack.com/t/evidencedev/shared_invite/zt-uda6wp6a-hP6Qyz0LUOddwpXW5qG03Q)
- Open an issue on [GitHub](https://github.com/evidence-dev/evidence)
