import streamlit as st
import polars as pl


def establishments_filter():
    options = st.session_state.establishments_inspections_latest['name_address'].to_list()
    
    if 'selected_establishment' not in st.session_state:
        st.session_state['selected_establishment'] = 'Franklin Barbecue - 900 E 11TH ST AUSTIN'

    def update_selected_establishment():
        st.session_state['selected_establishment'] = st.session_state._temp_establishment_filter

    st.selectbox(
        'Select a restaurant',
        options=options,
        key='_temp_establishment_filter',
        on_change=update_selected_establishment,
        index=options.index('Franklin Barbecue - 900 E 11TH ST AUSTIN'),
    )