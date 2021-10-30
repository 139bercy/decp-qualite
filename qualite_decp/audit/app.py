""" Ce module contient les fonctions nécessaires à l'audit de qualité des données consolidées.
"""

import logging

from qualite_decp import download
from qualite_decp import conf


def run(rows: int = None):
    """Audite la donnée consolidée et stocke les résultats.

    Args:
        rows (int, optional): Nombre de lignes desquelles auditer la qualité. Defaults to None.
    """
    data = download.open_json(conf.download.consolidated_data_path)
    schema = download.open_json(conf.download.consolidated_data_schema_path)
    # Choix d'un sous-ensemble des marchés, si requis
    if rows is not None:
        data["marches"] = data["marches"][:rows]
    # Filtrage sur le _type 'marché'
    num_total = len(data["marches"])
    availables_types = set([m.get("_type") for m in data["marches"]])
    logging.debug("Valeurs de la colonne _type : %s", availables_types)
    logging.debug("Filtrage de la colonne _type sur la valeur 'marché'")
    data["marches"] = [
        m for m in data["marches"] if m.get("_type").lower() == "marché".lower()
    ]
    num_filtered = len(data["marches"])
    logging.debug(
        "Passage de %d à %d entrées suite au filtrage", num_total, num_filtered
    )
    # Audit par source
    available_sources = set([m.get("source") for m in data["marches"]])
    for source in conf.audit.sources:
        source_data = {
            "marches": [
                m for m in data["marches"] if m.get("source").lower() == source.lower()
            ]
        }
        logging.debug(
            "%d lignes pour la source %s", len(source_data["marches"]), source
        )
