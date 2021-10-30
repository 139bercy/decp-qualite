import streamlit as st

from qualite_decp import conf
from qualite_decp import download
from qualite_decp.web import build


def get_audit_results(date):
    # temporary code
    if date == "Exemple date 1":
        return download.open_json("./data/audit_results_date_1.json")
    if date == "Exemple date 1":
        return download.open_json("./data/audit_results_date_2.json")


def run():
    """Lance l'application web de présentation des résultats"""
    build.page_config()
    available_sources = ["Exemple source 1", "Exemple source 2"]
    available_dates = ["Exemple date 1", "Exemple date 2"]
    selected_source, current_date, old_date = build.sidebar(
        available_sources, available_dates
    )
    current_results = get_audit_results(current_date)
    old_results = get_audit_results(old_date)
    build.page()
