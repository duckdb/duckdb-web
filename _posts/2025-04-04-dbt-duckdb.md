---
layout: post
title: "Transforming Data with DuckDB and dbt"
author: Petrica Leuca
thumb: "/images/blog/thumbs/duckdb-dbt.svg"
image: "/images/blog/thumbs/duckdb-dbt.png"
excerpt: "In this post, we implement data transformation and reverse ETL pipelines with DuckDB and dbt using the `dbt-duckdb` adapter."
tags: ["using DuckDB"]
---

## Introduction

The [Data Build Tool](https://www.getdbt.com/), `dbt`, is an open-source transformation framework, which enables data teams to adopt software engineering best practices in the code they deliver, such as Git workflow and unit testing. Other notable features of `dbt` are data lineage, documentation and data testing as part of the execution pipeline.

In this article we will demonstrate how data can be processed with dbt and DuckDB, by using the [`dbt-duckdb`](https://github.com/duckdb/dbt-duckdb) adapter. The `dbt-duckdb` adapter is the integration of `dbt` and DuckDB, offering the means of implementing data transformation pipelines according to the `dbt` standard and by making use of DuckDB's processing power.

### Data Model

We use two open datasets in this post: railway services, provided by the team behind the [Rijden de Treinen *(Are the trains running?)* application](https://www.rijdendetreinen.nl/en/about) and cartography information about the Netherlands provided by [cartomap](https://github.com/cartomap/nl).
The datasets are organized into:

- a persisted DuckDB database, in which we store the railway services data from 2024, hosted on Cloudfare;
- a provinces GeoJSON file, containing the geographic information about the Dutch provinces, hosted on GitHub;
- a municipalities GeoJSON file, containing the geographic information about Dutch municipalities, stored together with the code.

After doing an initial exploration of the above data, we can observe that a province can have one or many municipalities, a municipality can have none or many train stations and a train service record is connected to one and only one train station. Therefore we decide on the following data model:

- a dimension table, `dim_nl_provinces`, to hold information about the Dutch provinces;
- a dimension table, `dim_nl_municipalities`, to hold information about the Dutch municipalities, linked to `dim_nl_provinces`;
- a dimension table, `dim_nl_train_stations`, to hold information about the train stations in the Netherlands, linked to `dim_nl_municipalities`;
- a fact table, `fact_services`, to hold information about the train services, linked to `dim_nl_train_stations`.

<div align="center" style="margin:10px">
    <a href="/images/blog/dbt-duckdb/data_model.svg">
        <img
          src="/images/blog/dbt-duckdb/data_model.svg"
          alt="Transformation Layer Data Model"
          width=700
        />
    </a>
</div>

The purpose of processing the train services and the Netherlands cartography data is to organize the data in a structure which can easily be used in future railway data analysis use cases. Such curated data structures are often called [_data marts_](https://en.wikipedia.org/wiki/Data_mart).

> Tip The following code is available on [GitHub](https://github.com/duckdb/duckdb-blog-examples/tree/main/dbt_duckdb).

## Processing Data with DuckDB and dbt

After we have [initialized](https://docs.getdbt.com/reference/commands/init) our project, we configure the connection details for DuckDB in the `profiles.yml` file. Along with specifying if the database should be in memory or persisted to disk, we also specify:

- which extensions are required for the data processing, e.g., [spatial]({% link docs/stable/extensions/spatial/overview.md %});
- external databases, attached from the local disk or other storage solutions.

```yaml
dutch_railway_network:

  outputs:
    dev:
      type: duckdb
      path: data/dutch_railway_network.duckdb
      extensions:
        - spatial
        - httpfs
      threads: 5
      attach:
        - path: 'https://blobs.duckdb.org/nl-railway/train_stations_and_services.duckdb'
          type: duckdb
          alias: external_db
  target: dev
```

We then configure the `sources.yml` file under the `models` directory by
specifying external sources (such as files) and table definitions
from the attached database(s):

```yaml
version: 2
sources:
  - name: geojson_external
    tables:
      - name: nl_provinces
        config:
          external_location: "https://cartomap.github.io/nl/wgs84/provincie_2025.geojson"
      - name: nl_municipalities
        config:
          external_location: "seeds/gemeente_2025.geojson"
  - name: external_db
    database: external_db
    schema: main
    tables:
      - name: stations
      - name: services
```

> The `external_location` can be any [DuckDB data source]({% link docs/stable/data/data_sources.md %}) (e.g., CSV or Parquet).

With both the profile and source defined, we can now load the data.

### Loading Data to DuckDB

In `dbt` the way of storing the data in the target system is called `materialization`. The `dbt-duckdb` adapter provides the following materialization options:

- `table`, replacing the target table at each run;
- `incremental`, with `append` and `delete+insert` options, modifying the data in the table, but not the table itself (if it exists);
- `snapshot`, implementing a [Slowly Changing Dimension Type 2](https://en.wikipedia.org/wiki/Slowly_changing_dimension) table with time validity intervals;
- `view`, replacing the target view at each run.

Another feature of using the above adapter is that the SQL dialect used in the data processing scripts has all the [friendly SQL extensions]({% link docs/stable/sql/dialect/friendly_sql.md %}) DuckDB has to offer.

To refresh the data in the `dim_nl_provinces` table, we use  the `st_read` spatial function, which reads and parses automatically the `nl_provinces` GeoJSON file, defined in `sources.yml`.

{% raw %}
```sql
{{ config(materialized='table') }}

SELECT
    {{ dbt_utils.generate_surrogate_key(['id']) }} AS province_sk,
    id AS province_id,
    statnaam AS province_name,
    geom AS province_geometry,
    {{ common_columns() }}
FROM st_read({{ source("geojson_external", "nl_provinces") }}) AS src;
```
{% endraw %}

Similarly, we fully refresh the data for `dim_nl_municipalities` and `fact_services`.

To build the relation between a train station location and a municipality,
we use the `st_contains` spatial function, which returns `true` when a geometry contains another geometry:

{% raw %}
```sql
{{ config(materialized='table') }}

SELECT
    {{ dbt_utils.generate_surrogate_key(['tr_st.code']) }} AS station_sk,
    tr_st.id AS station_id,
    tr_st.code AS station_code,
    tr_st.name_long AS station_name,
    tr_st.type AS station_type,
    st_point(tr_st.geo_lng, tr_st.geo_lat) AS station_geo_location,
    coalesce(dim_mun.municipality_sk, 'unknown') AS municipality_sk,
    {{ common_columns() }}
FROM {{ source("external_db", "stations") }} AS tr_st
LEFT JOIN {{ ref ("dim_nl_municipalities") }} AS dim_mun
       ON st_contains(
           dim_mun.municipality_geometry,
           st_point(tr_st.geo_lng, tr_st.geo_lat)
       )
WHERE tr_st.country = 'NL';
```
{% endraw %}

>To read from the external sources, we reference the source by providing the source and table names.

## Exporting Data from DuckDB

One major benefit of using DuckDB for data processing is the ability to export data to files (such as CSV, JSON and Parquet) and to refresh data directly in PostgreSQL or MySQL databases.

### External Files

The feature of exporting data to files is enabled by the `dbt-duckdb` adapter with the [`external` materialization](https://github.com/duckdb/dbt-duckdb?tab=readme-ov-file#writing-to-external-files). With the `external` materialization, we are able to export data to CSV, JSON and Parquet file types to a specified storage location (local or external). The load type is `full refresh`, therefore existing files are overwritten.

In the following processing step, we export aggregated train service data at month level, to a Parquet file, partitioned by year and month:

{% raw %}
```sql
{{
    config(
        materialized='external',
        location="data/exports/nl_train_services_aggregate",
        options={
            "partition_by": "service_year, service_month",
            "overwrite": True
        }
    )
}}

SELECT
    year(service_date) AS service_year,
    month(service_date) AS service_month,
    service_type,
    service_company,
    tr_st.station_sk,
    tr_st.station_name,
    m.municipality_sk,
    m.municipality_name,
    p.province_sk,
    p.province_name,
    count(*) AS number_of_rides
FROM {{ ref ("fact_services") }} AS srv
INNER JOIN {{ ref("dim_nl_train_stations") }} AS tr_st
        ON srv.station_sk = tr_st.station_sk
INNER JOIN {{ ref("dim_nl_municipalities") }} AS m
        ON tr_st.municipality_sk = m.municipality_sk
INNER JOIN {{ ref("dim_nl_provinces") }} AS p
        ON m.province_sk = p.province_sk
WHERE service_year = {{ var('execution_year') }}
GROUP BY ALL
```
{% endraw %}

The exported files are placed in [Hive partitioned directory structure]({% link docs/stable/data/partitioning/hive_partitioning.md %}).

```text
./service_year=2024/service_month=1:
49255 Apr  2 14:54 data_0.parquet

...

./service_year=2024/service_month=12:
48031 Apr  2 14:54 data_0.parquet
```

### PostgreSQL

After we process the data into our railway services data mart, we can generate from it a daily aggregate at train station level, organized into a star schema model, by having the dimension keys part of the data:

{% raw %}
```sql
{{
    config(
        materialized='incremental',
        incremental_strategy='delete+insert',
        unique_key="""
            service_date,
            service_type,
            service_company,
            station_sk
        """
    )
}}

SELECT
    service_date,
    service_type,
    service_company,
    srv.station_sk,
    mn.municipality_sk,
    province_sk,
    count(*) AS number_of_rides,
    {{ common_columns() }}
FROM {{ ref ("fact_services") }} AS srv
INNER JOIN {{ ref("rep_dim_nl_train_stations") }} AS tr_st
        ON srv.station_sk = tr_st.station_sk
INNER JOIN {{ ref("rep_dim_nl_municipalities") }} AS mn
        ON tr_st.municipality_sk = mn.municipality_sk
WHERE NOT service_arrival_cancelled;

  {% if is_incremental() %}
    AND srv.invocation_id = (
        SELECT invocation_id
        FROM {{ ref("fact_services") }}
        ORDER BY last_updated_dt DESC
        LIMIT 1
    )
  {% endif %}
GROUP BY ALL
```
{% endraw %}

Thanks to DuckDB's ability to connect and write to a PostgreSQL database, we can add the above processing step to our `dbt` project, under the directory `models/reverse_etl`.

To connect to a PostgreSQL database, we need to specify in `profiles.yml`:

- the [`postgres` extension]({% link docs/stable/extensions/postgres.md %});
- the PostgreSQL connection string in the `attach` section.

{% raw %}
```yaml
dutch_railway_network:

  outputs:
    dev:
      type: duckdb
      path: data/dutch_railway_network.duckdb
      extensions:
        ...
        - postgres
      threads: 5
      attach:
        ...
        - path: "postgresql://postgres:{{ env_var('DBT_DUCKDB_PG_PWD') }}@localhost:5466/postgres"
          type: postgres
          alias: postgres_db
  target: dev
```
{% endraw %}

We also have to configure the model's database details in `dbt_project.yml`:

```yaml
models:
  dutch_railway_network:
    transformation:
      schema: main
      +docs:
        node_color: 'silver'
    reverse_etl:
      database: postgres_db
      schema: public
      +docs:
        node_color: '#d5b85a'
```

With this configuration, all the models from the `transformation` directory will be executed on the `main_main` schema, while the models from `reverse_etl` will be executed on the `main_public` schema.

After executing the models with `dbt run --model +reverse_etl`, the data is available to query from PostgreSQL:

```bash
psql -U postgres
```

```sql
SELECT count(*), sum(number_of_rides)
FROM main_public.rep_fact_train_services_daily_agg;
```

```text
 count  |   sum    
--------+----------
 240826 | 17438151
```

> It is important to mention that while PostgreSQL is the target database and `dbt` provides `merge` as an incremental strategy for it; the execution of the above pipeline is happening in DuckDB, therefore the incremental load can be done only with `append` or `delete+insert` strategies.

## Execution Details

The above implementation consists of 10 models and 20 data tests, processing 400 MB of data from the attached DuckDB database, together with small data organized in GeoJSON files. The total execution time, on a single thread and on a MacBook Pro of 12 GB, is between 40 and 45 seconds. From the total execution time, approximatively 30 seconds are spent to process the train services data and 4 seconds to write the aggregated data to PostgreSQL:

```text
05:48:07  Running with dbt=1.9.3
05:48:08  Registered adapter: duckdb=1.9.2
05:48:08  Found 10 models, 20 data tests, 4 sources, 565 macros
05:48:08  
05:48:08  Concurrency: 1 threads (target='dev')
...
05:48:45  19 of 30 OK created sql table model main_main.fact_services .................... [OK in 32.60s]
...
05:48:50  26 of 30 OK created sql incremental model postgres_db.main_public.rep_fact_train_services_daily_agg  [OK in 3.74s]
...
05:48:51  Finished running 2 external models, 1 incremental model, 7 table models, 20 data tests in 0 hours 0 minutes and 42.63 seconds (42.63s).
05:48:51  
05:48:51  Completed successfully
05:48:51  
05:48:51  Done. PASS=30 WARN=0 ERROR=0 SKIP=0 TOTAL=30
```

## Conclusion

In this post we have demonstrated how DuckDB integrates with `dbt` and how it is part of the data processing ecosystem by showcasing data mart creation, file exports and reverse ETL to a PostgreSQL database.
