import duckdb
import streamlit as st


@st.cache_resource
def get_duckdb_conn():
    duckdb_conn = duckdb.connect()
    duckdb_conn.sql(
        "attach 'https://blobs.duckdb.org/nl-railway/train_stations_and_services.duckdb' as external_db"
    )
    duckdb_conn.sql("use external_db")
    duckdb_conn.sql("install spatial")
    duckdb_conn.sql("load spatial")

    return duckdb_conn


def get_stations_services_query(duckdb_conn):
    # create a relation for the station selection
    stations_selection = duckdb_conn.sql(
        "select name_long as station_name, geo_lat, geo_lng, code from stations"
    ).set_alias("stations_selection")

    # create a relation for the services selection
    services_selection = (
        duckdb_conn.sql("from services")
        .aggregate(
            """
            station_code: "Stop:Station code",
            service_date: "Service:Date",
            service_date_format: strftime(service_date, '%d-%b (%A)'),
            num_services: count(*)
        """
        )
        .set_alias("services")
    )

    # return the query with joining stations and services and the duckdb_conn
    return (
        (
            stations_selection.join(
                services_selection, "services.station_code = stations_selection.code"
            ).select(
                """
            service_date,
            service_date_format,
            station_name,
            geo_lat,
            geo_lng,
            num_services
        """
            )
        ),
        duckdb_conn,
    )
