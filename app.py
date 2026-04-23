import streamlit as st

from src.styles import apply_base_style
from src.data import init_session_states


st.set_page_config(
    page_title='Food Establishment Inspection Scores',
    page_icon='🍔🍟🍕',
    layout='centered',
    initial_sidebar_state='expanded',
)


apply_base_style()
init_session_states()


st.title('Food Establishment Inspection Scores')
st.caption('Explore food establishment inspection scores for Austin, Texas.')

apps = {
    'Map': [st.Page('apps/map/map.py', title='Map of Food Establishments', icon='🌍')],
    'Analytics': [st.Page('apps/analytics/analytics.py', title='Analytics', icon='📊')],
}

pg = st.navigation(apps)
pg.run()