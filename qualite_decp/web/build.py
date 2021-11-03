""" Module contenant les fonctions pour construire les différents éléments de la page Web streamlit.
"""


from audit import audit_results_one_source
import streamlit as st

from qualite_decp import conf
from qualite_decp.audit import audit_results
from qualite_decp.audit import measures


def page_config():
    """Construit la configuration Streamlit de la page"""
    st.set_page_config(
        page_title=conf.web.titre_page,
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
    st.sidebar.markdown(conf.web.texte_haut_barre_laterale)
    selected_source = st.sidebar.selectbox("Source à analyser", available_sources)
    sidebar_column_1, sidebar_column_2 = st.sidebar.columns(2)
    with sidebar_column_1:
        current_date = st.selectbox(
            "Date courante", available_dates, index=len(available_dates) - 1
        )
    with sidebar_column_2:
        old_date = st.selectbox("Date à comparer", available_dates, index=0)
    st.sidebar.markdown(conf.web.texte_bas_barre_laterale)
    return selected_source, current_date, old_date


def page(
    current_results: audit_results_one_source.AuditResultsOneSource,
    old_results: audit_results_one_source.AuditResultsOneSource,
):
    """Construit la partie principale de la page"""
    st.image("qualite_decp/web/static/logo.png", width=300)
    st.title(conf.web.titre)
    global_container(current_results, old_results)
    details_container(current_results)


def get_metric_value_delta(current_value: float, old_value: float):
    """Construit les valeurs pour un élément 'streamlit.metric' à partir de la valeur courante et  ancienne

    Args:
        current_value (float): Valeur actuelle
        old_value (float): Ancienne valeure

    Returns:
        str, str: Chaîne pour la valeur et le delta de l'élément
    """
    current_value = int(current_value * 100)
    old_value = int(old_value * 100)
    value = f"{current_value} %"
    delta = f"{current_value - old_value} pts"
    return value, delta


def to_percentage(number: float):
    """Formatte un nombre en pourcentage. Exemple : 0.28 -> 28%

    Args:
        number (float): Nombre à convertir

    Returns:
        str: Pourcentage
    """
    number = int(number * 100)
    percentage = f"{number}" + "%"
    return percentage


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
        "Qualité globale",
        *get_metric_value_delta(
            current_results.general.valeur, old_results.general.valeur
        ),
    )
    global_col_1.markdown(f"*Rang source:* **{current_results.general.rang}**")
    global_col_2.metric(
        "Validité",
        *get_metric_value_delta(
            current_results.validite.valeur, old_results.validite.valeur
        ),
    )
    global_col_2.markdown(f"*Rang:* **{current_results.validite.rang}**")
    global_col_3.metric(
        "Complétude",
        *get_metric_value_delta(
            current_results.completude.valeur, old_results.completude.valeur
        ),
    )
    global_col_3.markdown(f"*Rang:* **{current_results.completude.rang}**")
    global_col_4.metric(
        "Conformité",
        *get_metric_value_delta(
            current_results.conformite.valeur, old_results.conformite.valeur
        ),
    )
    global_col_4.markdown(f"*Rang:* **{current_results.conformite.rang}**")
    global_col_5.metric(
        "Cohérence",
        *get_metric_value_delta(
            current_results.coherence.valeur, old_results.coherence.valeur
        ),
    )
    global_col_5.markdown(f"*Rang:* **{current_results.coherence.rang}**")
    global_col_6.metric(
        "Singularité",
        *get_metric_value_delta(
            current_results.singularite.valeur, old_results.singularite.valeur
        ),
    )
    global_col_6.markdown(f"*Rang:* **{current_results.singularite.rang}**")
    global_col_7.metric(
        "Exactitude",
        *get_metric_value_delta(
            current_results.exactitude.valeur, old_results.exactitude.valeur
        ),
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
        **{to_percentage(singularite.identifiants_non_uniques)}** identifiants non uniques
        """
    )
    singularite_container.info(
        f"""
        **{to_percentage(singularite.lignes_dupliquees)}** lignes dupliquées
        """
    )


def detailed_validite_container(parent_element, validite: measures.Validite):
    validite_container = parent_element.container()
    validite_container.markdown("**Validité**")
    validite_container.info(
        f"""
        **{to_percentage(validite.jours_depuis_derniere_publication)}** jours depuis la dernière publication
        """
    )
    validite_container.info(
        f"""
        **{to_percentage(validite.depassements_delai_entre_notification_et_publication)}** dépassements du délai entre notification et publication
        """
    )


def detailed_completude_container(parent_element, completude: measures.Completude):
    completude_container = parent_element.container()
    completude_container.markdown("**Complétude**")
    completude_container.info(
        f"""
        **{to_percentage(completude.donnees_manquantes)}** données manquantes
        """
    )
    completude_container.info(
        f"""
        **{to_percentage(completude.valeurs_non_renseignees)}** valeurs non renseignées
        """
    )


def detailed_conformite_container(parent_element, conformite: measures.Conformite):
    conformite_container = parent_element.container()
    conformite_container.markdown("**Conformité**")
    conformite_container.info(
        f"""
        **{to_percentage(conformite.caracteres_mal_encodes)}** caractères mal encodés ou illisibles
        """
    )
    conformite_container.info(
        f"""
        **{to_percentage(conformite.formats_non_valides)}** formats non respectés
        """
    )
    conformite_container.info(
        f"""
        **{to_percentage(conformite.valeurs_non_valides)}** valeurs invalides
        """
    )


def detailed_exactitude_container(parent_element, exactitude: measures.Exactitude):
    exactitude_container = parent_element.container()
    exactitude_container.markdown("**Exactitude**")
    exactitude_container.info(
        f"""
        **{to_percentage(exactitude.valeurs_aberrantes)}** valeurs aberrantes
        """
    )
    exactitude_container.info(
        f"""
        **{to_percentage(exactitude.valeurs_extremes)}** valeurs extrêmes
        """
    )


def detailed_coherence_container(parent_element, coherence: measures.Coherence):
    coherence_container = parent_element.container()
    coherence_container.markdown("**Cohérence**")
    coherence_container.info(
        f"""
        **{to_percentage(coherence.incoherences_temporelles)}** incohérences temporelles entre notification et publication
        """
    )
    coherence_container.info(
        f"""
        **{to_percentage(coherence.incoherences_montant_duree)}** incohérences entre montant et durée
        """
    )
