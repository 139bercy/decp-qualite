import streamlit as st

from qualite_decp import conf


def page_config():
    """Construit la configuration Streamlit de la page"""
    st.set_page_config(
        page_title=conf.web.page_title,
        page_icon="qualite_decp/web/static/favicon.ico",
        layout="wide",
        initial_sidebar_state="auto",
    )


def sidebar(available_sources: list, available_dates: list):
    """Construit la barre latérale de la page.

    Args:
        available_sources (list): Listes de sources disponibles dans les données
        available_dates (list): Listes de dates pour lesquelles la donnée est disponible

    Returns:
        str, str, str: Source, date courante et date de comparaison sélectionnées
    """
    st.sidebar.markdown(conf.web.sidebar_top_text_markdown)
    selected_source = st.sidebar.selectbox("Source à analyser", available_sources)
    sidebar_column_1, sidebar_column_2 = st.sidebar.columns(2)
    with sidebar_column_1:
        current_date = st.selectbox(
            "Date courante", available_dates, index=len(available_dates) - 1
        )
    with sidebar_column_2:
        old_date = st.selectbox("Date à comparer", available_dates, index=0)
    st.sidebar.markdown(conf.web.sidebar_bottom_text_markdown)
    return selected_source, current_date, old_date


def page():
    """Construit la partie principale de la page"""
    st.image("qualite_decp/web/static/logo.png", width=300)
    st.title(conf.web.title)
    global_container()
    details_container()


def global_container():
    """Construit la section contenant les indicateurs de qualité globale"""
    global_container = st.container()
    (
        global_col_1,
        global_col_2,
        global_col_3,
        global_col_4,
        global_col_5,
        global_col_6,
        global_col_7,
    ) = global_container.columns([2, 1, 1, 1, 1, 1, 1])


def details_container():
    """Construit la section contenant les indicateurs de qualité détaillés"""
    details_container = st.container()
    details_col_1, details_col_2, details_col_3 = details_container.columns(3)
    detailed_singularite_container(details_col_1)
    detailed_validite_container(details_col_1)
    detailed_completude_container(details_col_2)
    detailed_conformite_container(details_col_2)
    detailed_exactitude_container(details_col_3)
    detailed_coherence_container(details_col_3)


def detailed_singularite_container(parent_element):
    singularite_container = parent_element.container()
    singularite_container.markdown("Singularité")


def detailed_validite_container(parent_element):
    validite_container = parent_element.container()
    validite_container.markdown("Validité")


def detailed_completude_container(parent_element):
    completude_container = parent_element.container()
    completude_container.markdown("Complétude")


def detailed_conformite_container(parent_element):
    conformite_container = parent_element.container()
    conformite_container.markdown("Conformité")


def detailed_exactitude_container(parent_element):
    exactitude_container = parent_element.container()
    exactitude_container.markdown("Exactitude")


def detailed_coherence_container(parent_element):
    coherence_container = parent_element.container()
    coherence_container.markdown("Cohérence")
