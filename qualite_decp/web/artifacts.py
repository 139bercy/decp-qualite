from datetime import datetime
import logging
import zipfile
import json
import os

import streamlit as st
import requests

from qualite_decp import conf
from qualite_decp import download
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
    artifacts = load_json_from_url(url)
    return artifacts


def load_json_from_url(url: str):
    """Charge un fichier JSON en mémoire depuis une URL

    Args:
        url (str): URL du fichier

    Returns:
        dict: Dictionnaire issu du fichier JSON
    """
    response = requests.get(url)
    if response.status_code == 403:
        raise Exception(f"Erreur 403 en requêtant {url} : {response.content}")
    return response.json()


def get_github_auth():
    """Obtient un tuple d'authentification pour l'API GitHub.

    Returns:
        (str, str): Tuple (utilisateur, jeton) à utiliser lors des appels API
    """
    username = os.environ["GITHUB_USERNAME"]
    token = os.environ["GITHUB_TOKEN"]
    return (username, token)


def list_artifacts(artifact_name: str):
    """Liste les artifacts disponible (1 par date).

    Returns:
        dict: Dictionnaire des artifacts disponible (date:url)
    """
    artifacts = get_artifacts()
    num_artifacts = artifacts.get("total_count")
    logging.debug(f"{num_artifacts} artifacts disponibles sur le projet")
    artifacts = [
        a
        for a in artifacts.get("artifacts")
        if a.get("name") == artifact_name and a.get("expired") == False
    ]
    logging.debug(f"{len(artifacts)} artifacts ayant pour nom {artifact_name}")
    results = dict()
    for artifact in artifacts:
        artifact_date = artifact.get("created_at")
        artifact_url = artifact.get("archive_download_url")
        artifact_date = datetime.strptime(artifact_date, "%Y-%m-%dT%H:%M:%SZ").date()
        results[artifact_date] = artifact_url
    logging.debug(f"{len(results)} artifacts avec date unique")
    results = dict(sorted(results.items()))
    return results


@st.cache
def download_artifact_archive_from_url(archive_url: str, path: str):
    """Télécharge un artifact archivé sous forme de dictionnaire depuis une URL.

    Args:
        archive_url (str): URL vers un artifact de type JSON archivé (ZIP)
        path (str): Chemin vers le fichier téléchargé
    """
    auth = get_github_auth()
    download.download_data_from_url_to_file(archive_url, path, stream=True, auth=auth)


@st.cache
def load_artifact_archive_from_url(
    archive_url: str, buffer_path: str = "./data/artifact.zip"
):
    """Charge un artifact archivé sous forme de dictionnaire depuis une URL.

    Args:
        archive_url (str): URL vers un artifact de type JSON archivé (ZIP)

    Returns:
        dict: Fichier chargé
    """
    download_artifact_archive_from_url(archive_url, buffer_path)
    with zipfile.ZipFile(buffer_path, "r") as z:
        for filename in z.namelist():
            with z.open(filename) as f:
                data = f.read()
                d = json.loads(data)
                return d


def get_audit_results(
    date: datetime.date, source: str, buffer_path: str = None
) -> audit_results_one_source.AuditResultsOneSource:
    """Récupère le résultat de l'audit de qualité pour la source et la date selectionnées.

    Args:
        date (str): Date de l'audit voulu
        source (str): Source auditée

    Returns:
        audit_results_one_source.AuditResultsOneSource: Résultats d'audit
    """
    artifacts_dict = list_artifacts(conf.audit.nom_artifact_resultats)
    url = artifacts_dict[date]
    artifact = load_artifact_archive_from_url(url, buffer_path=buffer_path)
    results = audit_results.AuditResults.from_list(artifact)
    result = results.extract_results_for_source(source)
    return result
