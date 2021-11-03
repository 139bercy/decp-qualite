""" Ce module contient les fonctions nécessaires à l'audit de qualité des données consolidées.
"""

import logging
from datetime import datetime

import jsonschema
import pandas

from qualite_decp import download
from qualite_decp import conf
from qualite_decp.audit import audit_results
from qualite_decp.audit import audit_results_one_source
from qualite_decp.audit import measures


def audit_against_schema(data: dict, schema: dict):
    """Audit la conformité de donnée par rapport à un schéma de définition.

    Args:
        data (dict): Donnée à auditer. Doit contenir un champ "marches"
        schema (dict): Schéma de donnée (format http://json-schema.org/draft-04/schema#)

    Raises:
        Exception: [description]

    Returns:
        dict: Dictionnaire {uid: {errors: ..., failed_validators: ...}}
    """
    if len(data["marches"]) == 0:
        return {}
    # Choix de Draft4Validator car "$schema": "http://json-schema.org/draft-04/schema#"
    validator = jsonschema.Draft4Validator(schema)
    errors = dict()
    keep_index_any_of = None
    for index, any_of in enumerate(schema["properties"]["marches"]["items"]["anyOf"]):
        if any_of["$ref"] == "#/definitions/marche":
            keep_index_any_of = index
    if keep_index_any_of is None:
        raise Exception(
            "Impossible de trouver la valeur #/definitions/marche dans properties.marches.items.anyOf"
        )
    for root_error in validator.iter_errors(data):
        instance_uid = root_error.instance.get("uid")
        instance_suberrors = []
        if root_error.context is None or len(root_error.context) == 0:
            logging.warning("Des défauts de qualité inattendus ont pu être omis")
        else:
            for error in root_error.context:
                if error.schema_path[0] == keep_index_any_of:
                    if len(error.context) > 0:
                        logging.warning(
                            "Des défauts de qualité inattendus ont pu être omis"
                        )
                    error_details = {
                        "message": error.message,
                        "validator": error.validator,
                    }
                    instance_suberrors.append(error_details)
        failed_validators = list(
            set([suberror["validator"] for suberror in instance_suberrors])
        )
        instance_errors = {
            "errors": instance_suberrors,
            "failed_validators": failed_validators,
        }
        errors[instance_uid] = instance_errors
    return errors


def divide_and_round(dividend, divisor):
    """Divise deux nombres et arrondit le quotient à deux décimales.

    Args:
        dividend (int ou float ou str): Nombre à diviser
        divisor (int ou float ou str): Diviseur

    Returns:
        float: Quotient arrondi
    """
    quotient = float(dividend) / float(divisor)
    rounded_quotient = round(quotient, 2)
    return rounded_quotient


def is_after(date_1: str, date_2: str):
    """Vérifie si une date_1 est strictement ultérieure à date_2.

    Args:
        date_1 (str): Première date (YYYY-MM-DD)
        date_2 (str): Seconde date (YYYY-MM-DD)

    Returns:
        bool: True si date_1 est ultérieure à date_2, False sinon.
    """
    date_1 = str_to_datetime_date(date_1)
    date_2 = str_to_datetime_date(date_2)
    return date_1 > date_2


def str_to_datetime_date(date_str: str):
    """Convertit une date sous forme de chaîne en objet datetime.

    Args:
        date_str (str): Date à convertir (YYYY-MM-DD)

    Returns:
        datetime.datetime: Date convertie
    """
    date = str(date_str)[:10]
    return datetime.strptime(date, "%Y-%m-%d").date()


def is_market_publishing_delay_overdue(notification_date: str, publishing_date: str):
    """Vérifie si le délai maximal entre notification et publication est dépassé.

    Args:
        notification_date (str): Date de notification (YYYY-MM-DD)
        publishing_date (str): Date de publication (YYYY-MM-DD)

    Returns:
        bool: True si le délai est dépassé, False sinon
    """
    notification_date = str_to_datetime_date(notification_date)
    publishing_date = str_to_datetime_date(publishing_date)
    delta = publishing_date - notification_date
    return int(delta.days) > conf.audit.delai_publication


def is_market_amount_abnormal(amount: int):
    """Vérifie si le montant du marché est anormal.

    Args:
        amount (int): Montant du marché en euros

    Returns:
        bool: True si le montant est anormal, False sinon.
    """
    return not (
        conf.audit.bornes_montant_aberrant.borne_inf
        < amount
        < conf.audit.bornes_montant_aberrant.borne_sup
    )


def are_market_amount_and_duration_inconsistent(amount: int, duration: int):
    """Varifie si le montant et la durée d'un marché son incohérents.

    Args:
        amount (int): Montant du marché (euros)
        duration (int): Durée du marché (mois)

    Returns:
        bool: True si incohérence, False sinon
    """
    if duration == amount:
        return True
    elif amount / max(duration, 1) < 100:
        return True
    elif amount / max(duration, 1) < 1000 and amount < 200000:
        return True
    elif duration in [360, 365, 366] and amount < 10000000:
        return True
    elif duration > 120 and amount < 2000000:
        return True
    else:
        return False


def has_unsupported_character(text: str):
    """Vérifie si une chaîne contient des caractères mal encodés.

    Args:
        text (str): La chaîne à vérifier

    Returns:
        bool: True si la chaîne contient au moins un caractère mal encodé, False sinon
    """
    return "�" in text


def count_duplicated_lines(dataframe: pandas.DataFrame):
    """Compte le nombre de lignes étant dupliquées sur les coolonnes configurées

    Args:
        dataframe (pandas.DataFrame): Dataframe contenant les données

    Returns:
        int: Nombre de lignes étant duliquées
    """
    exclude_columns = conf.audit.lignes_dupliquees.colonnes_excluses
    include_columns = [c for c in dataframe.columns if c not in exclude_columns]
    logging.debug(
        "Comptage des informations dupliquées dans les colonnes : %s", include_columns
    )
    duplicates = dataframe.duplicated(keep=False, subset=include_columns)
    num_duplicates = duplicates.sum()
    duplicates_uids = duplicates[duplicates == True].index.to_list()
    logging.debug(
        "%d lignes dupliquées trouvées, UIDs : %s", num_duplicates, duplicates_uids
    )
    return num_duplicates


def get_days_since_last_publishing(dataframe: pandas.DataFrame):
    """Calcule le nombre de jour depuis la dernière publication.

    Args:
        dataframe (pandas.DataFrame): Dataframe contenant les données

    Returns:
        int: Nombre de jours depuis dernière publication
    """
    dataframe["datePublicationDonnees"] = pandas.to_datetime(
        dataframe["datePublicationDonnees"], format="%Y-%m-%d", errors="coerce"
    )
    most_recent_date = dataframe["datePublicationDonnees"].max().date()
    logging.debug("Dernière publication : %s", most_recent_date)
    today_date = datetime.now().date()
    delta_days = (today_date - most_recent_date).days
    logging.debug("Ecart avec aujourd'hui : %d jours", delta_days)
    return delta_days


def count_extreme_values(dataframe: pandas.DataFrame):
    """Compte le nombre de lignes possédant des valeurs extrêmes dans les colonnes configurées

    Args:
        dataframe (pandas.DataFrame): Dataframe contenant les données

    Returns:
        int: Nombre de lignes contenant au moins une valeur extrême
    """
    include_columns = conf.audit.valeurs_extremes.colonnes_incluses
    extrem_values_lines_uids = list()
    num_stdev = conf.audit.valeurs_extremes.nombre_deviations_standards
    for col in include_columns:
        series = dataframe[col]
        series = series.dropna()
        series = pandas.to_numeric(series, errors="coerce")
        series = series.abs()
        extreme_values = series[(series - series.mean()) > (num_stdev * series.std())]
        extrem_values_lines_uids += extreme_values.index.to_list()
    extrem_values_lines_uids = list(set(extrem_values_lines_uids))
    num_extrem_values_lines = len(extrem_values_lines_uids)
    logging.debug(
        "%d lignes avec valeurs extrêmes trouvées, UIDs: %s",
        num_extrem_values_lines,
        extrem_values_lines_uids,
    )
    return num_extrem_values_lines


def audit_source_quality(source_name: str, source_data: dict, schema: dict):
    """Audite la donnée consolidée pour une source.

    Args:
        source_name (str): Nom de la source
        source_data (dict): Donnée à auditer. Doit contenir un champ "marches"
        schema (dict): Schéma de donnée (format http://json-schema.org/draft-04/schema#)

    Returns:
        audit_results_one_source.AuditResultsOneSource: Résultats de l'audit pour la source.
    """

    num_lines = len(source_data["marches"])
    uids = [marche["uid"] for marche in source_data["marches"]]
    non_unique_uids = [uid for uid in uids if len([u for u in uids if u == uid]) > 1]
    num_non_unique_uids = len(non_unique_uids)
    logging.info("%d lignes pour la source %s", num_lines, source_name)
    if len(source_data["marches"]) == 0:
        identifiants_non_uniques = 0.0
        formats_non_valides = 0.0
        valeurs_non_valides = 0.0
        donnees_manquantes = 0.0
        valeurs_non_renseignees = 0.0
        lignes_dupliquees = 0.0
        caracteres_mal_encodes = 0.0
        jours_depuis_derniere_publication = 0.0
        depassements_delai_entre_notification_et_publication = 0.0
        incoherences_temporelles = 0.0
        incoherences_montant_duree = 0.0
        valeurs_aberrantes = 0.0
        valeurs_extremes = 0.0
    else:
        schema_audit_results = audit_against_schema(source_data, schema)
        identifiants_non_uniques = num_non_unique_uids
        formats_non_valides = 0
        valeurs_non_valides = 0
        donnees_manquantes = 0
        valeurs_non_renseignees = 0
        lignes_dupliquees = 0
        caracteres_mal_encodes = 0
        jours_depuis_derniere_publication = 0
        depassements_delai_entre_notification_et_publication = 0
        incoherences_temporelles = 0
        incoherences_montant_duree = 0
        valeurs_aberrantes = 0
        valeurs_extremes = 0

        dataframe = download.json_dict_to_dataframe(
            source_data, record_path="marches", index_column="uid"
        )
        lignes_dupliquees = count_duplicated_lines(dataframe)
        jours_depuis_derniere_publication = get_days_since_last_publishing(dataframe)
        jours_depuis_derniere_publication = max(jours_depuis_derniere_publication, 100)
        valeurs_extremes = count_extreme_values(dataframe)

        # Analyse ligne par ligne
        for marche in source_data["marches"]:

            # Confrontation au schéma - Formats, valeurs
            marche_uid = marche["uid"]
            marche_schema_audit_results = schema_audit_results.get(marche_uid)
            if marche_schema_audit_results is not None:
                failed_validators = marche_schema_audit_results["failed_validators"]
                for v in failed_validators:
                    if v == "minLength" or v == "maxLength" or v == "pattern":
                        formats_non_valides += 1
                    elif v == "enum" or v == "minimum" or v == "maximum":
                        valeurs_non_valides += 1
                    elif v == "required":
                        donnees_manquantes += 1
                        valeurs_non_renseignees += 1
                    else:
                        logging.warning("Validateur non géré : %s", v)

            # Cohérence temporelle
            if (
                "dateNotification" in marche.keys()
                and "datePublicationDonnees" in marche.keys()
            ):
                if is_after(
                    marche["dateNotification"], marche["datePublicationDonnees"]
                ):
                    incoherences_temporelles += 1

            # Valeurs aberrantes
            if "montant" in marche.keys():
                if is_market_amount_abnormal(marche["montant"]):
                    valeurs_aberrantes += 1

            # Incohérences montant/durée
            if "montant" in marche.keys() and "dureeMois" in marche.keys():
                if are_market_amount_and_duration_inconsistent(
                    marche["montant"], marche["dureeMois"]
                ):
                    incoherences_montant_duree += 1

            # Caractères non supportés (utf8 non respecté)
            if "objet" in marche.keys():
                if has_unsupported_character(marche["objet"]):
                    caracteres_mal_encodes += 1

            # Dépassement du délai reglemntaire entre notification et publication
            if (
                "dateNotification" in marche.keys()
                and "datePublicationDonnees" in marche.keys()
            ):
                if is_market_publishing_delay_overdue(
                    marche["dateNotification"], marche["datePublicationDonnees"]
                ):
                    depassements_delai_entre_notification_et_publication += 1

        # Conversion vers un pourcentage des lignes concernées
        identifiants_non_uniques = divide_and_round(identifiants_non_uniques, num_lines)
        formats_non_valides = divide_and_round(formats_non_valides, num_lines)
        valeurs_non_valides = divide_and_round(valeurs_non_valides, num_lines)
        donnees_manquantes = divide_and_round(donnees_manquantes, num_lines)
        valeurs_non_renseignees = divide_and_round(valeurs_non_renseignees, num_lines)
        lignes_dupliquees = divide_and_round(lignes_dupliquees, num_lines)
        caracteres_mal_encodes = divide_and_round(caracteres_mal_encodes, num_lines)
        jours_depuis_derniere_publication = divide_and_round(
            jours_depuis_derniere_publication, num_lines
        )
        depassements_delai_entre_notification_et_publication = divide_and_round(
            depassements_delai_entre_notification_et_publication, num_lines
        )
        incoherences_temporelles = divide_and_round(incoherences_temporelles, num_lines)
        incoherences_montant_duree = divide_and_round(
            incoherences_montant_duree, num_lines
        )
        valeurs_aberrantes = divide_and_round(valeurs_aberrantes, num_lines)
        valeurs_extremes = divide_and_round(valeurs_extremes, num_lines)

    singularite = measures.Singularite(
        identifiants_non_uniques=identifiants_non_uniques,
        lignes_dupliquees=lignes_dupliquees,
    )
    conformite = measures.Conformite(
        caracteres_mal_encodes=caracteres_mal_encodes,
        formats_non_valides=formats_non_valides,
        valeurs_non_valides=valeurs_non_valides,
    )
    completude = measures.Completude(
        donnees_manquantes=donnees_manquantes,
        valeurs_non_renseignees=valeurs_non_renseignees,
    )
    validite = measures.Validite(
        jours_depuis_derniere_publication=jours_depuis_derniere_publication,
        depassements_delai_entre_notification_et_publication=depassements_delai_entre_notification_et_publication,
    )
    coherence = measures.Coherence(
        incoherences_temporelles=incoherences_temporelles,
        incoherences_montant_duree=incoherences_montant_duree,
    )
    exactitude = measures.Exactitude(
        valeurs_aberrantes=valeurs_aberrantes, valeurs_extremes=valeurs_extremes
    )

    new_source_results = audit_results_one_source.AuditResultsOneSource(
        source=source_name,
        singularite=singularite,
        conformite=conformite,
        completude=completude,
        validite=validite,
        coherence=coherence,
        exactitude=exactitude,
    )

    new_source_results.compute_general()
    return new_source_results


def run(rows: int = None):
    """Audite la donnée consolidée et stocke les résultats.

    Args:
        rows (int, optional): Nombre de lignes desquelles auditer la qualité. Defaults to None.
    """
    data = download.open_json(conf.download.chemin_donnes_consolidees)
    schema = download.open_json(conf.download.chemin_schema_donnees)
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
    results = audit_results.AuditResults()
    for source in conf.audit.sources:
        logging.info("Audit de la qualité pour la source %s...", source)
        source_data = {
            "marches": [
                m for m in data["marches"] if m.get("source").lower() == source.lower()
            ]
        }
        new_source_results = audit_source_quality(source, source_data, schema)
        results.add_results(new_source_results)

    results.compute_ranks()
    results.to_json(conf.audit.chemin_resultats)
