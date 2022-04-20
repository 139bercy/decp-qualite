""" Ce module contient les fonctions nécessaires au téléchargement des données consolidées.
"""

import logging
import pandas

from decp_qualite import conf
from decp_qualite.download import utils

pandas.set_option("display.max_columns", 500)


def run():
    """Télécharge la donnée consolidée (.json depuis data.gouv.fr)."""
    logging.info("Téléchargement des données consolidées...")
    utils.download_data_from_url_to_file(
        conf.download.url_donnees_consolidees,
        conf.download.chemin_donnes_consolidees,
        stream=True,
    )
    logging.info("Téléchargement du schéma de données...")
    utils.download_data_from_url_to_file(
        conf.download.url_schema_donnees,
        conf.download.chemin_schema_donnees,
        stream=False,
    )
