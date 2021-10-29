import streamlit as st

from qualite_decp import conf


def run():
    """Lance l'application web de présentation des résultats"""

    st.set_page_config(
        page_title=conf.web.page_title,
        page_icon="qualite_decp/web/static/favicon.ico",
        layout="wide",
        initial_sidebar_state="auto",
    )

    st.text(conf.web.sample_text)
