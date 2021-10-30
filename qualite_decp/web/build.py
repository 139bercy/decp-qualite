from audit import audit_results_one_source
import streamlit as st

from qualite_decp import conf
from qualite_decp.audit import audit_results
from qualite_decp.audit import measures


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


def page(
    current_results: audit_results_one_source.AuditResultsOneSource,
    old_results: audit_results_one_source.AuditResultsOneSource,
):
    """Construit la partie principale de la page"""
    st.image("qualite_decp/web/static/logo.png", width=300)
    st.title(conf.web.title)
    global_container(current_results, old_results)
    details_container(current_results)


def global_container(
    current_results: audit_results_one_source.AuditResultsOneSource,
    old_results: audit_results_one_source.AuditResultsOneSource,
):
    """Construit la section contenant les indicateurs de qualité globale"""
    global_container = st.container()
    global_container.subheader("Synthèse")
    (
        global_col_1,
        global_col_2,
        global_col_3,
        global_col_4,
        global_col_5,
        global_col_6,
        global_col_7,
    ) = global_container.columns([2, 1, 1, 1, 1, 1, 1])
    global_col_1.metric(
        "Qualité globale", current_results.general.valeur, old_results.general.valeur
    )
    global_col_1.markdown(f"*Rang source:* **{current_results.general.rang}**")
    global_col_2.metric(
        "Validité", current_results.validite.valeur, old_results.validite.valeur
    )
    global_col_2.markdown(f"*Rang:* **{current_results.validite.rang}**")
    global_col_3.metric(
        "Complétude", current_results.completude.valeur, old_results.completude.valeur
    )
    global_col_3.markdown(f"*Rang:* **{current_results.completude.rang}**")
    global_col_4.metric(
        "Conformité", current_results.conformite.valeur, old_results.conformite.valeur
    )
    global_col_4.markdown(f"*Rang:* **{current_results.conformite.rang}**")
    global_col_5.metric(
        "Cohérence", current_results.coherence.valeur, old_results.coherence.valeur
    )
    global_col_5.markdown(f"*Rang:* **{current_results.coherence.rang}**")
    global_col_6.metric(
        "Singularité",
        current_results.singularite.valeur,
        old_results.singularite.valeur,
    )
    global_col_6.markdown(f"*Rang:* **{current_results.singularite.rang}**")
    global_col_7.metric(
        "Exactitude", current_results.exactitude.valeur, old_results.exactitude.valeur
    )
    global_col_7.markdown(f"*Rang:* **{current_results.exactitude.rang}**")


def details_container(current_results: audit_results_one_source.AuditResultsOneSource):
    """Construit la section contenant les indicateurs de qualité détaillés"""
    details_container = st.container()
    details_container.subheader("Détails des indicateurs")
    details_col_1, details_col_2, details_col_3 = details_container.columns(3)
    detailed_singularite_container(details_col_1, current_results.singularite)
    detailed_validite_container(details_col_1, current_results.validite)
    detailed_completude_container(details_col_2, current_results.completude)
    detailed_conformite_container(details_col_2, current_results.conformite)
    detailed_exactitude_container(details_col_3, current_results.exactitude)
    detailed_coherence_container(details_col_3, current_results.coherence)


def detailed_singularite_container(parent_element, singularite: measures.Singularite):
    singularite_container = parent_element.container()
    singularite_container.markdown("**Singularité**")
    singularite_container.info(
        f"""
        **{singularite.identifiants_non_uniques}** identifiants non uniques
        """
    )
    singularite_container.info(
        f"""
        **{singularite.lignes_dupliquees}** lignes dupliquées
        """
    )


def detailed_validite_container(parent_element, validite: measures.Validite):
    validite_container = parent_element.container()
    validite_container.markdown("**Validité**")
    validite_container.info(
        f"""
        **{validite.jours_moyens_depuis_derniere_publication}** jours depuis la dernière publication
        """
    )
    validite_container.info(
        f"""
        **{validite.depassements_delai_entre_notification_et_publication}** dépassements du délai entre notification et publication
        """
    )


def detailed_completude_container(parent_element, completude: measures.Completude):
    completude_container = parent_element.container()
    completude_container.markdown("**Complétude**")
    completude_container.info(
        f"""
        **{completude.donnees_manquantes}** données manquantes
        """
    )
    completude_container.info(
        f"""
        **{completude.valeurs_non_renseignees}** valeurs non renseignées
        """
    )


def detailed_conformite_container(parent_element, conformite: measures.Conformite):
    conformite_container = parent_element.container()
    conformite_container.markdown("**Conformité**")
    conformite_container.info(
        f"""
        **{conformite.caracteres_mal_encodes}** caractères mal encodés ou illisibles
        """
    )
    conformite_container.info(
        f"""
        **{conformite.formats_non_valides}** formats non respectés
        """
    )
    conformite_container.info(
        f"""
        **{conformite.valeurs_non_valides}** valeurs invalides
        """
    )


def detailed_exactitude_container(parent_element, exactitude: measures.Exactitude):
    exactitude_container = parent_element.container()
    exactitude_container.markdown("**Exactitude**")
    exactitude_container.info(
        f"""
        **{exactitude.valeurs_aberrantes}** valeurs aberrantes
        """
    )
    exactitude_container.info(
        f"""
        **{exactitude.valeurs_extremes}** valeurs extrêmes
        """
    )


def detailed_coherence_container(parent_element, coherence: measures.Coherence):
    coherence_container = parent_element.container()
    coherence_container.markdown("**Cohérence**")
    coherence_container.info(
        f"""
        **{coherence.incoherences_temporelles}** incohérences temporelles entre notification et publication
        """
    )
    coherence_container.info(
        f"""
        **{coherence.incoherences_montant_duree}** incohérences entre montant et durée
        """
    )
