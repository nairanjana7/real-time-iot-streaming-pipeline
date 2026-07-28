from pathlib import Path

import streamlit as st


def load_css():

    css_path = (
        Path(__file__)
        .resolve()
        .parent.parent
        / "styles"
        / "custom.css"
    )

    with open(css_path, encoding="utf-8") as css:

        st.markdown(

            f"<style>{css.read()}</style>",

            unsafe_allow_html=True

        )
