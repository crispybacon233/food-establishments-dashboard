# src/widgets/graphs.py

import streamlit as st
import polars as pl
import plotly.express as px


inspections = st.session_state.inspections
establishments_inspections_latest = st.session_state.establishments_inspections_latest



def inspections_map():
    fig = px.scatter_map(
        establishments_inspections_latest,
        lat='latitude',
        lon='longitude',
        color='score',
        text='google_name',
        color_continuous_scale=['Red', 'LightGreen'],
        zoom=10,
        range_color=[65, 100],
        height=700,
        # map_style='carto-darkmatter',
    ).update_layout(coloraxis_showscale=False)
    
    return fig


def inspections_time_series():
    selected_establishment_data = (
        establishments_inspections_latest
        .filter(pl.col('name_address') == st.session_state.selected_establishment).to_dicts()
    )

    temp_df = (
        inspections
        .filter(pl.col('facility_id') == selected_establishment_data[0]['facility_id'])
        .sort('inspection_date')
    )

    return px.line(
        temp_df,
        x='inspection_date',
        y='score',
        title=f'Scores Over Time for {selected_establishment_data[0]["google_name"]}',
        markers=True,
    )