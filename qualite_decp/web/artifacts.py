from datetime import datetime
import logging

import streamlit as st
import requests

from qualite_decp import conf
from qualite_decp.audit import audit_results_one_source
from qualite_decp.audit import audit_results


@st.cache
def get_artifacts(today_date: datetime.date = datetime.now().date()):
    """Obtient les artifacts depuis le projet GitHub.

    Args:
        today_date (datetime.date, optional): Date du jour. Defaults to datetime.now().date().

    Returns:
        dict: Dictionnaire d'artifacts
    """
    github_repo = conf.web.projet_github
    url = f"https://api.github.com/repos/{github_repo}/actions/artifacts"
    artifacts = download_json_from_url(url)
    return artifacts


@st.cache
def download_json_from_url(url: str):
    """Charge un fichier JSON en mémoire depuis une URL

    Args:
        url (str): URL du fichier

    Returns:
        dict: Dictionnaire issu du fichier JSON
    """
    print("Requesting", url)
    response = requests.get(url)
    if response.status_code == 403:
        raise Exception(f"Erreur 403 en requêtant {url} : {response.content}")
    return response.json()


def list_artifacts():
    """Liste les artifacts disponible (1 par date).

    Returns:
        dict: Dictionnaire des artifacts disponible (date:url)
    """
    artifacts = get_artifacts()
    nom_artifact = conf.audit.nom_artifact_resultats
    num_artifacts = artifacts.get("total_count")
    logging.debug(f"{num_artifacts} artifacts disponibles sur le projet")
    artifacts = [
        a
        for a in artifacts.get("artifacts")
        if a.get("name") == nom_artifact and a.get("expired") == False
    ]
    logging.debug(f"{len(artifacts)} artifacts de résultats d'audit")
    results = dict()
    for artifact in artifacts:
        artifact_date = artifact.get("created_at")
        artifact_url = artifact.get("url")
        artifact_date = datetime.strptime(artifact_date, "%Y-%m-%dT%H:%M:%SZ").date()
        results[artifact_date] = artifact_url
    logging.debug(f"{len(results)} artifacts avec date unique")
    results = dict(sorted(results.items()))
    return results


def get_audit_results(
    date: datetime.date, source: str
) -> audit_results_one_source.AuditResultsOneSource:
    """Récupère le résultat de l'audit de qualité pour la source et la date selectionnées.

    Args:
        date (str): Date de l'audit voulu
        source (str): Source auditée

    Returns:
        audit_results_one_source.AuditResultsOneSource: Résultats d'audit
    """
    artifacts_dict = list_artifacts()
    url = artifacts_dict[date]
    res_dict = download_json_from_url(url)
    # TODO
    # results = audit_results.AuditResults.from_list(res_dict)
    results = audit_results.AuditResults.from_json("./data/audit.json")
    result = results.extract_results_for_source(source)
    return result
