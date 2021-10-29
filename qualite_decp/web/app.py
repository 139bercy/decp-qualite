import streamlit as st

from qualite_decp import conf

def run():
    """ Runs quality reporting web application.
    """

    st.set_page_config(
        page_title=conf.web.page_title,
        page_icon="qualite_decp/web/static/favicon.ico",
        layout="wide",
        initial_sidebar_state="auto",
    )

    st.text(conf.web.sample_text)