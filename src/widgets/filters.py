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
        index=options.index(st.session_state['selected_establishment']),
    )


def inspection_score_range_filter():
    if 'score_range' not in st.session_state:
        st.session_state['score_range'] = (65, 100)

    def update_score_range():
        st.session_state['score_range'] = st.session_state._temp_score_range_filter

    st.slider(
        'Select an inspection score range',
        min_value=65,
        max_value=100,
        value=st.session_state['score_range'],
        step=1,
        key='_temp_score_range_filter',
        on_change=update_score_range,
    )


def category_filter():

    categories = st.session_state.establishments.filter(pl.col('category').is_not_null()).unique('category')['category'].to_list()
    categories = sorted(categories)
    categories.insert(0, 'ALL CATEGORIES')

    if 'selected_category' not in st.session_state:
        st.session_state['selected_category'] = 'ALL CATEGORIES'

    def update_category():
        st.session_state['selected_category'] = st.session_state._temp_category_filter

    st.selectbox(
        'Select a category',
        options=categories,
        key='_temp_category_filter',
        on_change=update_category,
        index=categories.index(st.session_state['selected_category']),
    )