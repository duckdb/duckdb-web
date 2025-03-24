import plotly.express as px
import streamlit as st

from utils import get_duckdb_conn, get_stations_services_query


def main():

    st.title("Analyzing Dutch Railway Data")

    duckdb_conn = get_duckdb_conn()

    # using Streamlit charts
    st.subheader("Number of train services in 2024")
    st.line_chart(
        duckdb_conn.sql("from services")
        .aggregate(
            """
            service_date: "Service:Date",
            service_month: monthname(service_date),
            service_month_id: month(service_date),
            num_services: count(distinct "Service:RDT-ID")
        """
        )
        .order("service_month_id")
        .df(),
        x="service_date",
        y="num_services",
        color="service_month",
    )

    # using Plotly charts
    st.plotly_chart(
        px.bar(
            get_top_5_stations_data(),
            x="service_month",
            y="num_services",
            color="station_name",
            barmode="group",
            title="Top 5 Busiest Train Stations 2024",
            labels={
                "service_month": "Month",
                "num_services": "Number Train Trips",
                "station_name": "Station Name",
            },
        )
    )


def get_top_5_stations_data():
    stations_query, _ = get_stations_services_query(get_duckdb_conn())

    return (
        stations_query.aggregate(
            """
                station_name, 
                service_month: monthname(service_date), 
                service_month_id: month(service_date), 
                num_services: sum(num_services)
            """
        )
        .select(
            """
                station_name, 
                service_month, 
                service_month_id, 
                num_services, 
                rn: row_number() over (partition by service_month order by num_services desc)
            """
        )
        .filter("rn <= 5")
        .order("service_month_id, station_name")
        .df()
    )


if __name__ == "__main__":
    main()
