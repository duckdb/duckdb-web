import duckdb
import folium
import streamlit as st
from streamlit_folium import st_folium

from utils import get_duckdb_conn

from constants import DEFAULT_LAT, DEFAULT_LNG


def main():
    if "clicked_map" not in st.session_state:
        st.session_state.clicked_map = True
        st.session_state.clicked_location_lat = DEFAULT_LAT
        st.session_state.clicked_location_lng = DEFAULT_LNG
        st.session_state.clicked_location_zoom = 8

    st.subheader(
        f"Closest 5 train stations to [{st.session_state.clicked_location_lat:.2f}, {st.session_state.clicked_location_lng:.2f}]",
        anchor=False,
    )

    # display the map together with the markers
    user_map = st_folium(
        get_map(
            lat=st.session_state.clicked_location_lat,
            lng=st.session_state.clicked_location_lng,
            zoom=st.session_state.clicked_location_zoom,
        ),
        key="user-map",
        height=600,
        width=800
    )

    # rerun the application on click
    if user_map.get("last_clicked"):
        st.session_state.clicked_location_lat = user_map["last_clicked"]["lat"]
        st.session_state.clicked_location_lng = user_map["last_clicked"]["lng"]
        st.session_state.clicked_location_zoom = user_map["zoom"]
        st.rerun()


def get_map(lat, lng, zoom):
    # create the folium map, with the center at the latitude and longitude provided as input
    folium_map = folium.Map(
        location=[
            lat,
            lng,
        ],
        zoom_start=zoom,
        height=600,
        width=800
    )

    # add a marker of blue color and user icon at the location provided
    folium.Marker(
        location=[
            lat,
            lng,
        ],
        icon=folium.Icon(icon="user", prefix="fa", color="blue"),
        draggable=False,
    ).add_to(folium_map)

    # get the closest train stations to the location provided

    duckdb_conn = get_duckdb_conn()
    closest_stations_detailed_query,_ = get_closest_stations_detailed_query(duckdb_conn, lat, lng)

    # iterate over the list of records
    for x in closest_stations_detailed_query.fetchall():
        # for each train station add a marker to the map at the location of the train station
        # and add to the popup the information about the train station
        folium.Marker(
            location=[x[1], x[2]],
            draggable=False,
            icon=folium.Icon(color=x[6]),
            popup=folium.Popup(
                f"""
                <strong>Station</strong>: {x[0]} <br>
                <strong>Location</strong>: [{x[1]},{x[2]}] <br>
                <strong>Distance</strong>: {x[3]} km <br>
                <strong>Number of Services</strong>: {x[4]:,} <br>
                <strong>Number of Cancellations</strong>: {x[5]:,} <br>
            """,
                max_width=200,
            ),
        ).add_to(folium_map)

    return folium_map



def get_closest_stations_query(duckdb_conn, lat, lng):
    stations_selection = duckdb_conn.sql("""
        select name_long as station_name, geo_lat, geo_lng, code 
        from stations st 
        where exists (
                select count(*) 
                from services sv 
                where st.code = sv."Stop:Station code" 
                having count(*)>100
            )
    """)

    return (
        stations_selection.project(f"""
            code as station_code,
            station_name,
            geo_lat, 
            geo_lng, 
            station_geo_point: st_point(geo_lng, geo_lat),
            clicked_geo_point: st_point({lng}, {lat}),
            distance_in_m: st_distance_sphere(st_point(geo_lng, geo_lat), clicked_geo_point),
            distance_in_km: round(distance_in_m/1000,2)
        """)
        .order("distance_in_km")
        .limit(5)
    )


def get_closest_stations_detailed_query(duckdb_conn, lat, lng):
    services = duckdb_conn.sql("from services").set_alias("services")
    closest_stations = get_closest_stations_query(duckdb_conn, lat, lng).set_alias("closest_stations")

    return (
        services.join(
            closest_stations,
            'services."Stop:Station code" = closest_stations.station_code',
        )
        .aggregate("""
            station_name,
            geo_lat, 
            geo_lng,
            distance_in_km,
            num_cancelled_at_departure: sum(coalesce("Stop:Departure cancelled", false)),
            num_cancelled_at_arrival: sum(coalesce("Stop:Arrival cancelled", false)),
            num_services: count(*) 
        """)
        .select("""
            station_name,
            geo_lat,
            geo_lng,
            distance_in_km,
            num_services,
            num_cancellations: num_cancelled_at_arrival + num_cancelled_at_departure,
            color: case row_number() over (order by num_services desc) 
                when 1 then 'darkred' 
                when 2 then 'red'
                when 3 then 'orange'
                when 4 then 'darkgreen'
                when 5 then 'green'
            else 'green' end
        """)
    ), duckdb_conn



if __name__ == "__main__":
    main()
