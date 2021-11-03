""" Ce module contient les fonctions nécessaires au téléchargement des données consolidées.
"""

import logging
import json

import requests
import pandas

from qualite_decp import conf


def run():
    """Télécharge la donnée consolidée (.json depuis data.gouv.fr)."""
    logging.info("Téléchargement des données consolidées...")
    download_data_from_url_to_file(
        conf.download.url_donnees_consolidees,
        conf.download.chemin_donnes_consolidees,
        stream=True,
    )
    logging.info("Téléchargement du schéma de données...")
    download_data_from_url_to_file(
        conf.download.url_schema_donnees,
        conf.download.chemin_schema_donnees,
        stream=False,
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


def open_json(path: str):
    """Charge un fichier JSON sous forme de dictionnaire

    Args:
        path (str): CHemin vers un fichier JSON (utf8)

    Returns:
        dict: Données du fichier
    """
    with open(path, "rb") as file_reader:
        return json.loads(file_reader.read().decode("utf-8"))


def save_json(data: dict, path: str):
    """Stocke un dictionnaire sous forme de fichier JSON

    Args:
        data (dict): Dictionnaire à stocker
        path (str): Chemin vers le fichier (utf8)
    """
    with open(path, "w", encoding="utf-8") as file_writer:
        json.dump(data, file_writer, ensure_ascii=False, indent=2)


def json_dict_to_dataframe(
    data: dict, record_path: str = None, index_column: str = None
):
    """Convertit de la donnée JSON semi-structurée vers un DataFrame.

    Args:
        data (dict): Donnée issue d'un JSON
        record_path (str): Chemin vers la liste d'entrées

    Returns:
        pandas.DataFrame: Donnée aplatie dans un DataFrame.
    """
    dataframe = pandas.json_normalize(data, record_path=record_path)
    if index_column is not None:
        dataframe = dataframe.set_index(index_column)
    return dataframe
