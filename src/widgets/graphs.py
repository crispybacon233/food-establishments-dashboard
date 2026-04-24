# src/widgets/graphs.py

import streamlit as st
import polars as pl
import plotly.express as px


inspections = st.session_state.inspections
establishments_inspections_latest = st.session_state.establishments_inspections_latest



def inspections_map():  
    score_range = st.session_state['score_range']
    selected_category = st.session_state['selected_category']

    temp_df = (
        establishments_inspections_latest
        .filter(pl.col('score').is_between(score_range[0], score_range[1]))
    )
    if selected_category != 'ALL CATEGORIES':
        temp_df = temp_df.filter(pl.col('category') == selected_category)

    fig = px.scatter_map(
        temp_df,
        lat='latitude',
        lon='longitude',
        color='score',
        text='google_name',
        color_continuous_scale=['Red', 'Orange', 'Green'],
        zoom=10,
        range_color=[65, 100],
        height=700,
        custom_data=['google_name', 'inspection_date', 'score', 'average_rating'],
        # map_style='carto-darkmatter',
    ).update_layout(
        coloraxis_showscale=False
    ).update_traces(
        hovertemplate=(
        '%{customdata[0]}<br>'
        'Inspection Date: %{customdata[1]}<br>'
        'Inspection Score: %{customdata[2]}<br>'
        'Average Google Rating: %{customdata[3]}'
        ),
        marker=dict(size=10),
        textfont=dict(color='black')
    )
    
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