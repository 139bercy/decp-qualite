import streamlit as st

from decp_qualite import conf
from decp_qualite.web import build
from decp_qualite.web import artifacts


def run():
    """Lance l'application web de présentation des résultats"""
    build.page_config()
    results_artifacts_dict = artifacts.list_artifacts(conf.audit.nom_artifact_resultats)
    details_artifacts_dict = artifacts.list_artifacts(conf.audit.nom_artifact_details)
    available_sources = conf.audit.sources
    available_dates = results_artifacts_dict.keys()
    available_dates = artifacts.keep_one_date_per_month(available_dates)
    (
        selected_page,
        selected_source,
        selected_current_date,
        selected_comparison_date,
    ) = build.sidebar(available_sources, available_dates)
    if selected_page == conf.web.page_documentation:
        build.documentation_page()
    elif selected_page == conf.web.page_resultats:
        if len(results_artifacts_dict) > 0:
            # Récupération de la synthèse de l'audit et construction de la page principale
            current_results = artifacts.get_audit_results(
                selected_current_date,
                selected_source,
                buffer_path="./data/results-current.zip",
            )
            comparison_results = artifacts.get_audit_results(
                selected_comparison_date,
                selected_source,
                buffer_path="./data/results-compared.zip",
            )
            build.page(current_results, comparison_results)
            # Récupération des détails par marché de l'audit et construction du bouton de téléchargement
            details_url = details_artifacts_dict.get(selected_current_date)
            if details_url is not None:
                artifacts.download_artifact_archive_from_url(
                    details_url, path="./data/details.zip"
                )
                path_details = "./data/details.zip"
            else:
                path_details = None
            build.download_button(
                "./data/results-current.zip",
                path_details=path_details,
                parent_container=st.sidebar,
            )
        else:
            build.no_data_page()
