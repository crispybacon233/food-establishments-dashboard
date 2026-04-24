# apps/map/map.py

import streamlit as st
import polars as pl

from src.widgets import filters, graphs
from src.data import reset_session_states

establishments = st.session_state.establishments
inspections = st.session_state.inspections
establishments_inspections_latest = st.session_state.establishments_inspections_latest

with st.sidebar:
    st.header('Restaurant Filter')
    filters.establishments_filter()
    button_container = st.empty()

    st.header('Map Filter')
    filters.category_filter()
    filters.inspection_score_range_filter()


map_tab, time_tab = st.tabs(['Map', 'Scores Over Time'])

with map_tab:
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
        st.plotly_chart(
            fig, 
            selection_mode='points',
        )


with time_tab:
    fig = graphs.inspections_time_series()
    st.plotly_chart(fig)
