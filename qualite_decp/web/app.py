import logging
import datetime

import streamlit as st

from qualite_decp import conf
from qualite_decp import download
from qualite_decp.web import build
from qualite_decp.web import artifacts
from qualite_decp.audit import audit_results
from qualite_decp.audit import audit_results_one_source


def run():
    """Lance l'application web de présentation des résultats"""
    build.page_config()
    artifacts_dict = artifacts.list_artifacts()
    available_sources = conf.audit.sources
    available_dates = artifacts_dict.keys()
    selected_source, selected_current_date, selected_comparison_date = build.sidebar(
        available_sources, available_dates
    )
    current_results = artifacts.get_audit_results(
        selected_current_date, selected_source
    )
    comparison_results = artifacts.get_audit_results(
        selected_comparison_date, selected_source
    )
    build.page(current_results, comparison_results)
