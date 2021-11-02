import logging

import streamlit as st

from qualite_decp import conf
from qualite_decp import download
from qualite_decp.web import build
from qualite_decp.audit import audit_results
from qualite_decp.audit import audit_results_one_source


def get_audit_results(
    date: str, source: str
) -> audit_results_one_source.AuditResultsOneSource:
    """Récupère le résultat de l'audit de qualité pour la source et la date selectionnées.

    Args:
        date (str): Date de l'audit voulu
        source (str): Source auditée

    Returns:
        audit_results_one_source.AuditResultsOneSource: Résultats d'audit
    """
    # TODO
    if date == "Exemple date 1":
        path = "./data/audit.json"
    elif date == "Exemple date 2":
        path = "./data/audit_old.json"
    results = audit_results.AuditResults.from_json(path)
    result = results.extract_results_for_source(source)
    return result


def run():
    """Lance l'application web de présentation des résultats"""
    build.page_config()
    available_sources = conf.audit.sources
    available_dates = ["Exemple date 1", "Exemple date 2"]
    selected_source, current_date, old_date = build.sidebar(
        available_sources, available_dates
    )
    current_results = get_audit_results(current_date, selected_source)
    old_results = get_audit_results(old_date, selected_source)
    build.page(current_results, old_results)
