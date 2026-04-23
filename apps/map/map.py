# apps/map/map.py

import streamlit as st
import polars as pl

from src.widgets import filters, graphs


establishments = st.session_state.establishments
inspections = st.session_state.inspections
establishments_inspections_latest = st.session_state.establishments_inspections_latest

filters.establishments_filter()

map_tab, time_tab = st.tabs(['Map', 'Scores Over Time'])

with map_tab:
    button_container = st.empty()
    map_container = st.empty()


    fig = graphs.inspections_map()
    with button_container:
        if st.button('Go to Food Establishment'):
            selected_establishment_data = establishments_inspections_latest.filter(pl.col('name_address') == st.session_state.selected_establishment).to_dicts()
            print(selected_establishment_data)
            lat = selected_establishment_data[0]['latitude']
            lon = selected_establishment_data[0]['longitude']
            print(lat, lon)
            if lat and lon:
                fig.update_layout(
                    map_center={"lat": lat, "lon": lon},
                    map_zoom=15,
                )
            else:
                st.error('No latitude or longitude found for the selected establishment')

    with map_container:
        st.plotly_chart(fig)


with time_tab:
    fig = graphs.inspections_time_series()
    st.plotly_chart(fig)
