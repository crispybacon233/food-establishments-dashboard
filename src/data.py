# src/data.py
import streamlit as st
import polars as pl

GCS_BUCKET = st.secrets['GCS_BUCKET']
KEY_ID = st.secrets['KEY_ID']
SECRET = st.secrets['SECRET']


storage_options = {
    "aws_access_key_id": KEY_ID,
    "aws_secret_access_key": SECRET,
    "endpoint_url": "https://storage.googleapis.com"
}


@st.cache_data
def load_data(path, _storage_options):
    return pl.read_parquet(path, storage_options=_storage_options)


def get_establishments():
    return load_data(
        f"s3://{GCS_BUCKET}/output-files/atx_establishments.parquet",
        storage_options,
    )


def get_inspections():
    return load_data(
        f"s3://{GCS_BUCKET}/output-files/atx_inspections.parquet",
        storage_options,
    )


@st.cache_data
def get_establishments_inspections_latest(establishments, inspections):
    latest_inspections = (
        inspections
        .filter(pl.col('inspection_date').dt.year() >= 2024)
    )
    establishments_inspections_latest = (
        establishments
        .join(latest_inspections, on='facility_id', how='left')
        .filter(pl.col("inspection_date") == pl.col("inspection_date").max().over("facility_id"))
        .with_columns(name_address = pl.col('google_name').fill_null(pl.col('restaurant_name')) + ' - ' + pl.col('address'))
        .sort('name_address')
    )
    return establishments_inspections_latest


def init_session_states():
    print('initializing session states...')
    if 'establishments' not in st.session_state:
        print('initializing establishments...')
        st.session_state.establishments = get_establishments()

    if 'inspections' not in st.session_state:
        print('initializing inspections...')
        st.session_state.inspections = get_inspections()

    if 'establishments_inspections_latest' not in st.session_state:
        print('initializing establishments_inspections_latest...')
        st.session_state.establishments_inspections_latest = get_establishments_inspections_latest(st.session_state.establishments, st.session_state.inspections)

    if 'selected_establishment' not in st.session_state:
        st.session_state.selected_establishment = 'Franklin Barbecue - 900 E 11TH ST AUSTIN'


def reset_session_states():
    st.session_state.selected_establishment = 'Franklin Barbecue - 900 E 11TH ST AUSTIN'
    st.session_state.selected_category = 'ALL CATEGORIES'
    st.session_state.score_range = (65, 100)