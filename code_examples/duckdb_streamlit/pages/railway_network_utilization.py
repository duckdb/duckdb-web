import plotly.express as px
import streamlit as st

from constants import DEFAULT_LAT, DEFAULT_LNG
from utils import (
    get_duckdb_conn,
    get_stations_services_query,
)


def main():

    duckdb_conn = get_duckdb_conn()

    with st.expander("Show railway network utilization during the year"):

        st.plotly_chart(get_utilization_during_year(duckdb_conn))

    with st.expander("Show overall railway network utilization across the country"):
        st.plotly_chart(get_utilization_across_country(duckdb_conn))

    with st.expander(
        "Show animation of railway network utilization across the country"
    ):
        st.plotly_chart(get_animated_utilization_across_country(duckdb_conn))


def get_utilization_during_year(duckdb_conn):
    heatmap_df = get_stations_services_data(duckdb_conn)
    heatmap_df.set_index("service_day", inplace=True)

    fig = px.imshow(
        heatmap_df.to_numpy(),
        x=list(heatmap_df.columns),
        y=list(heatmap_df.index),
        color_continuous_scale="viridis",
        text_auto=".2s",
        aspect="auto",
    )
    fig.update_xaxes(side="top", title="Number of train rides in 2024")

    return fig


@st.cache_data
def get_stations_services_data(_duckdb_conn):
    query = _duckdb_conn.sql("from services").aggregate("""
            service_day: dayname("Service:Date"),
            service_day_isodow: isodow("Service:Date"),
            service_month: monthname("Service:Date"),
            num_services: count(distinct "Service:RDT-ID")
        """)

    return (
        _duckdb_conn.sql(f"""
            pivot ({query.sql_query()})
            on service_month
            using sum(num_services)
            group by service_day, service_day_isodow
            order by service_day_isodow
        """)
        .select(
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
            "service_day",
        )
        .df()
    )

def get_utilization_across_country(duckdb_conn):
    stations_query, _ = get_stations_services_query(duckdb_conn)
    stations_agg_df = stations_query.aggregate(
        "geo_lat, geo_lng, num_services: sum(num_services)"
    ).df()

    return px.density_map(
        stations_agg_df,
        lat="geo_lat",
        lon="geo_lng",
        z="num_services",
        radius=5,
        center=dict(lat=DEFAULT_LAT, lon=DEFAULT_LNG),
        zoom=6.5,
        map_style="open-street-map",
        color_continuous_scale="viridis",
        range_color=[0, 100000],
        width=1000,
        height=600,
        title="Railway Network Utilization 2024",
    )


def get_animated_utilization_across_country(duckdb_conn):
    stations_query, _ = get_stations_services_query(duckdb_conn)

    stations_df = stations_query.filter("month(service_date) = 7").order("service_date").df()

    fig = px.density_map(
        stations_df,
        lat="geo_lat",
        lon="geo_lng",
        z="num_services",
        radius=7,
        center=dict(lat=DEFAULT_LAT, lon=DEFAULT_LNG),
        zoom=5,
        map_style="open-street-map",
        color_continuous_scale="viridis",
        range_color=[0, 700],
        animation_frame="service_date_format",
        title="Railway Network Utilization, July 2024",
    )

    fig.update_layout(
        width=1000,
        height=600,
        sliders=[{"currentvalue": {"prefix": None, "font": {"size": 16}}}],
        updatemenus=[
            {
                "buttons": [
                    {
                        "args": [
                            None,
                            {
                                "frame": {"duration": 300, "redraw": True},
                                "fromcurrent": True,
                            },
                        ],
                        "label": "Play",
                        "method": "animate",
                    },
                    {
                        "args": [
                            [None],
                            {
                                "frame": {"duration": 0, "redraw": True},
                                "mode": "immediate",
                                "transition": {"duration": 0},
                            },
                        ],
                        "label": "Stop",
                        "method": "animate",
                    },
                    {
                        "args": [
                            None,
                            {
                                "frame": {"duration": 100, "redraw": True},
                                "fromcurrent": True,
                            },
                        ],
                        "label": "Speed x 3",
                        "method": "animate",
                    },
                ],
            }
        ],
    )

    return fig



if __name__ == "__main__":
    main()
