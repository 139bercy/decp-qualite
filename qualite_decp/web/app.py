import streamlit as st

from qualite_decp import conf


def build_page_config():
    """Construit la configuration Streamlit de la page"""
    st.set_page_config(
        page_title=conf.web.page_title,
        page_icon="qualite_decp/web/static/favicon.ico",
        layout="wide",
        initial_sidebar_state="auto",
    )


def build_sidebar(available_sources: list, available_dates: list):
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


def build_page():
    """Construit la partie principale de la page"""
    st.image("qualite_decp/web/static/logo.png", width=300)
    st.title(conf.web.title)
    build_global_container()
    build_details_container()


def build_global_container():
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


def build_details_container():
    """Construit la section contenant les indicateurs de qualité détaillés"""
    details_container = st.container()
    details_col_1, details_col_2, details_col_3 = details_container.columns(3)
    singularite_container = details_col_1.container()
    singularite_container.markdown("Singularité")
    validite_container = details_col_1.container()
    validite_container.markdown("Validité")
    completude_container = details_col_2.container()
    completude_container.markdown("Complétude")
    conformite_container = details_col_2.container()
    conformite_container.markdown("Conformité")
    exactitude_container = details_col_3.container()
    exactitude_container.markdown("Exactitude")
    coherence_container = details_col_3.container()
    coherence_container.markdown("Cohérence")


def run():
    """Lance l'application web de présentation des résultats"""
    build_page_config()
    available_sources = ["Exemple source 1", "Exemple source 2"]
    available_dates = ["Exemple date 1", "Exemple date 2", "Exemple date 3"]
    selected_source, current_date, old_date = build_sidebar(
        available_sources, available_dates
    )
    build_page()
