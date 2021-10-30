""" Ce module contient les fonctions nécessaires au téléchargement des données consolidées.
"""

import logging

import requests

from qualite_decp import conf


def run():
    """Télécharge la donnée consolidée (.json depuis data.gouv.fr)."""
    logging.info("Téléchargement des données consolidées...")
    download_data_from_url_to_file(
        conf.download.consolidated_data_url,
        conf.download.consolidated_data_path,
        stream=True,
    )
    logging.info("Téléchargement du schéma de données...")
    download_data_from_url_to_file(
        conf.download.consolidated_data_schema_url,
        conf.download.consolidated_data_schema_path,
        stream=True,
    )


def download_data_from_url_to_file(url: str, path: str, stream: bool = True):
    """Télécharge un fichier de données depuis une URL.

    Args:
        url (str): URL du fichier à télécharger
        path (str): Chemin vers un fichier local
        stream (bool, optional): Si la donnée doit être streamée (recommandé pour les fichiers volumineux). Defaults to True.
    """
    response = requests.get(url, allow_redirects=True, verify=True, stream=stream)
    with open(path, "wb") as file_writer:
        if stream:
            for counter, chunk in enumerate(response.iter_content(chunk_size=4096)):
                file_writer.write(chunk)
                # print(".", end="", flush=True)
        else:
            file_writer.write(response.content)
