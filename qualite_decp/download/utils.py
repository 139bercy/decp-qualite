import json

import requests
import pandas


def download_data_from_url_to_file(url: str, path: str, stream: bool = True, auth=None):
    """Télécharge un fichier de données depuis une URL.

    Args:
        url (str): URL du fichier à télécharger
        path (str): Chemin vers un fichier local
        stream (bool, optional): Si la donnée doit être streamée (recommandé pour les fichiers volumineux). Defaults to True.
    """
    response = requests.get(
        url, allow_redirects=True, verify=True, stream=stream, auth=auth
    )
    with open(path, "wb") as file_writer:
        if stream:
            for chunk in response.iter_content(chunk_size=4096):
                file_writer.write(chunk)
        else:
            file_writer.write(response.content)


def get_safe_filename(string: str, separator="_"):
    filename = "".join([c if c.isalnum() else separator for c in string])
    return filename


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
