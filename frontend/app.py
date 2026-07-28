import streamlit as st

from styles.theme import (
    PAGE_TITLE,
    PAGE_ICON,
    LAYOUT,
    SIDEBAR_STATE,
)

from utils.helpers import load_css

from components.sidebar import render_sidebar

from components.header import render_header

from views.analytics import render_analytics

from views.history import render_history

from views.settings import render_settings

st.set_page_config(

    page_title=PAGE_TITLE,

    page_icon=PAGE_ICON,

    layout=LAYOUT,

    initial_sidebar_state=SIDEBAR_STATE

)

load_css()

page = render_sidebar()

render_header()

from views.dashboard import render_dashboard

if page == "Dashboard":

    render_dashboard()

elif page == "Analytics":

    render_analytics()

elif page == "History":

    render_history()

elif page == "Settings":

    render_settings()
