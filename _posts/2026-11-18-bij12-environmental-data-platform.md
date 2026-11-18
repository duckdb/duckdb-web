---
layout: post
title: "Preserving Nature Data for the Next Century With DuckDB and Open Formats"
authors:
  - Geertjan Wielenga
  - Tim Cox
  - Bart Zwemmer
thumb: /images/blog/thumbs/bij12-environmental-platform.svg
image: /images/blog/thumbs/bij12-environmental-platform.png
excerpt: "BIJ12 is building a long-lived environmental data platform in the Netherlands that uses DuckDB and GeoParquet to make fragmented nature-monitoring data discoverable and queryable across decades, without tying its preservation to any single database vendor."
tag: case-study
---

> Quote
>
> We can store data as Parquet files on S3 but still allow SQL access to the data
>
> — Bart Zwemmer, data engineer, BIJ12
{: .quote-large}

In the Netherlands, nature-monitoring data comes from many organizations: the twelve provinces, the Ministry of Defense, [Rijkswaterstaat](https://www.rijkswaterstaat.nl/) (the national water agency), research institutions and conservation groups. Each contributes observations in different formats. Researchers who need to understand ecological changes across years or decades often spend roughly three-quarters of their time just finding and assembling the data they need.

[BIJ12](https://www.bij12.nl/), which supports the Netherlands' provinces in standardizing environmental and biodiversity information, is building a data platform to solve this problem. The platform's goal is audacious: preserve this data in a form that researchers can find, query and reanalyze for the next 50 to 100 years—without tying the archive's long-term readability to any particular database product or vendor.

Bart Zwemmer, a data engineer working with BIJ12, explains the architectural strategy: store normalized data as open-format files (GeoParquet) on object storage, use DuckDB as the SQL interface for ingestion and querying, and maintain the data lake independently from any single query engine. As Bart puts it, "We can store data as Parquet files on S3 but still allow SQL access to the data." This keeps the barrier to entry low for future maintainers and preserves flexibility as technology evolves.

## The Problem: Fragmented Data Across Jurisdictions

Monitoring biodiversity and habitat health across a country requires long historical records. Changes in endangered species populations, wetland composition or bird migration patterns can take decades to observe with confidence. But the Netherlands' nature-monitoring ecosystem is fragmented: CSV files, Excel sheets, specialized GIS formats (GeoPackage), Parquet tables and web service APIs all coexist across the 14-organization network.

> **Note:** BIJ12 is part of the "[Verbeterprogramma VHR-monitoring](https://www.bij12.nl/actueel/kijk-de-demosessie-van-9-juli-terug/)" (VVM), an intergovernmental effort to make national nature-monitoring data consistent and available. The platform is designed to support [Natura 2000](https://ec.europa.eu/environment/nature/natura2000/) site monitoring. The organization's data platform, version 1.0, launched publicly in June 2026.

Even when data exists, researchers spend enormous effort locating it. Bart observed that stakeholders at coordination meetings report spending most of their research time on data discovery—not analysis. A centralized catalog with unified query access can change that.

A second concern is sensitivity. Some records—like the exact locations of endangered species—must remain restricted to authorized researchers, while public sightings of common birds can be openly shared. Some data carries seasonal restrictions: mushroom locations might be hidden during peak foraging season. The platform needs to enforce these access rules while maintaining historical context for reproducibility.

## The Architecture: File-First Storage, SQL Access

The BIJ12 platform's design prioritizes long-term maintainability and vendor independence. As Bart explains it, the team wants to avoid "vendor lock-in for your data."

1. **Ingest sources** include CSV, Excel, GeoPackage, Parquet, web services and specialized APIs.
2. **Lightweight orchestration** uses Python and TypeScript code, scheduled with Apache Airflow. Many transformation operations run as DuckDB SQL queries.
3. **Normalization to [GeoParquet](https://duckdb.org/docs/extensions/spatial/overview.html)** creates a standardized, archival data lake stored as files on S3-compatible object storage. Bart describes the standardization process: "We transform all of those to GeoParquet." The files themselves form the durable archive, independent of any query engine.
4. **A catalog layer** provides discoverability, descriptions and policy-aware access control.
5. **Query paths** include DuckDB for SQL-based analysis and joins across Parquet files, and a companion PostgreSQL instance for use cases that need richer spatial functionality or dashboard integrations.

> **Why file-first?** Bart notes that "storing the data separate from the query engine in this case was very beneficial." Parquet files on object storage remain readable even if the query engine changes. Future maintainers can query the same files with whatever SQL tools are available in 2050 or 2075. It's a bet on file formats and SQL as long-lived standards, compared to proprietary database schemas.

This design serves another goal: **operational simplicity for handover**. BIJ12 is currently staffed by freelance data engineers, but the platform will eventually need to be maintained by BIJ12's own team. Standardizing around SQL and DuckDB means future operators need to understand fewer moving parts. Bart emphasizes that the team "doesn't want to have many services running," which reduces the surface area for long-term maintenance and succession planning.

## DuckDB's Role: SQL Processing and Standardization

In this architecture, DuckDB handles several layers of work:

* **Ingestion and transformation.** Python or TypeScript scripts use DuckDB to query incoming data, transform it and write normalized GeoParquet files. This approach keeps most data operations in SQL, reducing the number of languages the team needs to maintain.
* **Querying and joining.** Analysts can use DuckDB to query, filter, aggregate and join archived Parquet files directly. They see a familiar SQL interface regardless of the underlying source format. As Bart says, "They can use DuckDB again to query those Parquet files, to join them, to aggregate them."
* **Standardization across the team.** Everyone works in SQL, which lowers the cognitive load during staff transitions.

Bart emphasizes this consistency: "Always a DuckDB query in our case." This approach uses DuckDB as the standard processing layer rather than scattered scripting languages.

## PostgreSQL's Role in the Architecture

A compelling aspect of this story is that **BIJ12 deliberately chose to use both DuckDB and PostgreSQL**. This isn't a DuckDB-only success story; it's a credible, practical tale of choosing the right tool for each job.

DuckDB Spatial is powerful, but it doesn't yet cover all the curved geometry types relevant to environmental data. Some imported curves must currently be approximated as many line segments, which can lose geometric precision—a concern for an archive that should preserve data fidelity. PostgreSQL and PostGIS, with their mature spatial capabilities, handle these cases.

BIJ12 plans to use [Metabase](https://www.metabase.com/) for dashboards, which integrates more smoothly with PostgreSQL than with DuckDB at present. The team also explored [Shaper](https://taleshape.com/shaper/docs/), an open-source DuckDB-driven dashboard tool, but PostgreSQL remained the more pragmatic choice for their current timeline.

This willingness to use multiple tools actually strengthens the platform's credibility. The team selected technologies based on which ones solved problems best, not on vendor allegiance or architectural purity.

## Access Control and Historical Reproducibility

The platform's catalog enforces role-based and time-based access rules. Bart explains how the "catalog layer allows us to filter out what you can see and what not based on time of year." A researcher might see:

* All public bird sightings and aggregate habitat surveys.
* Filtered locations of protected species (exact coordinates hidden; bounding boxes shown instead).
* Seasonal visibility rules—mushroom locations concealed during foraging season.
* Historical versions of datasets, so analyses conducted in 2024 can be exactly reproduced in 2027 using the same underlying data and definitions. As Bart notes, "You can exactly reproduce that."

This combination of access control and version history supports both conservation (sensitive species locations are protected) and scientific integrity (researchers can revisit the evidence behind earlier conclusions)

> **Caution on reproducibility** This is a property of the platform's overall data and metadata design, not a built-in time-travel feature in DuckDB. It requires careful version control and documentation alongside the query engine.

## Limitations and What Comes Next

Bart identified several areas where DuckDB—and the broader data-engineering tooling landscape—could mature:

* **Curved geometries.** Bart notes that "we are missing spatial features," particularly for curved geometry types. Better support would reduce precision loss in transformed spatial data. As he explains, "you have to transform your data in such a way and you lose precision."
* **Visualization integrations.** Dashboard tools designed around DuckDB are still early, more mature integrations would reduce reliance on PostgreSQL for dashboarding workflows.
* **Operational evidence.** The platform is live and growing, but quantified evidence of researcher productivity gains and long-term retention strategies is still accumulating.

BIJ12 is actively gathering stakeholder feedback and integrating new data sources. The team is also exploring additional access-control policies and visualization enhancements.

## Design Principles for Long-Lived Data Infrastructure

The BIJ12 effort addresses a challenge that extends beyond the Netherlands: **how to design public data infrastructure for decades, not years**. Technology vendors come and go. Staff members retire. Infrastructure patterns shift. A platform built on open file formats and portable SQL has a much better chance of surviving 50 or 100 years than one trapped in a proprietary schema.

The choice to standardize around DuckDB (and SQL broadly) isn't about loyalty to any product. It's about operational simplicity, future maintainability and the principle that scientific data should outlast the technologies used to collect or process it. That's a strong lesson for any organization stewarding long-lived archives.

Thanks to Bart Zwemmer and [BIJ12](https://www.bij12.nl/) for discussing their work and architecture. If you're building data infrastructure for environmental science, public records or long-term archives, DuckDB's SQL interface and ability to query open file formats can help you design for durability and independence. Learn more about [DuckDB Spatial](https://duckdb.org/docs/extensions/spatial/overview.html) and [GeoParquet](https://duckdb.org/docs/extensions/spatial/overview.html) in the documentation.

