from abc import ABC, abstractmethod

from qualite_decp.audit import app


class General:
    def __init__(self, valeur: float = None, rang: int = None):
        self.valeur = valeur
        self.rang = rang

    def to_dict(self):
        return {"valeur": self.valeur, "rang": self.rang}

    @classmethod
    def from_dict(cls, d: dict):
        """Instancie une classe depuis un dictionnaire.

        Args:
            d (dict): Dictionnaire

        Returns:
            General: Instance créée
        """
        valeur = d["valeur"]
        rang = d["rang"]
        return cls(valeur, rang)


class Measure(ABC):
    """Abstract class working as an interface for measure classes."""

    @abstractmethod
    def compute_value(self):
        pass

    @abstractmethod
    def to_dict(self):
        pass

    @abstractmethod
    def from_dict(d):
        pass


class Coherence(Measure):
    def __init__(
        self,
        valeur: float = None,
        rang: int = None,
        incoherences_temporelles=None,
        incoherences_montant_duree=None,
    ):
        self.valeur = valeur
        self.rang = rang
        self.incoherences_temporelles = incoherences_temporelles
        self.incoherences_montant_duree = incoherences_montant_duree

    def compute_value(self):
        self.valeur = app.divide_and_round(
            self.incoherences_temporelles + self.incoherences_montant_duree, 2
        )

    def to_dict(self):
        return {
            "synthese": {"valeur": self.valeur, "rang": self.rang},
            "detail": {
                "incoherences_temporelles": self.incoherences_temporelles,
                "incoherences_montant_duree": self.incoherences_montant_duree,
            },
        }

    @classmethod
    def from_dict(cls, d: dict):
        """Instancie une classe depuis un dictionnaire.

        Args:
            d (dict): Dictionnaire

        Returns:
            Coherence: Instance créée
        """
        valeur = d["synthese"]["valeur"]
        rang = d["synthese"]["rang"]
        incoherences_temporelles = d["detail"]["incoherences_temporelles"]
        incoherences_montant_duree = d["detail"]["incoherences_montant_duree"]
        return cls(valeur, rang, incoherences_temporelles, incoherences_montant_duree)


class Exactitude(Measure):
    def __init__(
        self,
        valeur: float = None,
        rang: int = None,
        valeurs_aberrantes=None,
        valeurs_extremes=None,
    ):
        self.valeur = valeur
        self.rang = rang
        self.valeurs_aberrantes = valeurs_aberrantes
        self.valeurs_extremes = valeurs_extremes

    def compute_value(self):
        self.valeur = app.divide_and_round(
            self.valeurs_aberrantes + self.valeurs_extremes, 2
        )

    def to_dict(self):
        return {
            "synthese": {"valeur": self.valeur, "rang": self.rang},
            "detail": {
                "valeurs_aberrantes": self.valeurs_aberrantes,
                "valeurs_extremes": self.valeurs_extremes,
            },
        }

    @classmethod
    def from_dict(cls, d: dict):
        """Instancie une classe depuis un dictionnaire.

        Args:
            d (dict): Dictionnaire

        Returns:
            Exactitude: Instance créée
        """
        valeur = d["synthese"]["valeur"]
        rang = d["synthese"]["rang"]
        valeurs_aberrantes = d["detail"]["valeurs_aberrantes"]
        valeurs_extremes = d["detail"]["valeurs_extremes"]
        return cls(valeur, rang, valeurs_aberrantes, valeurs_extremes)


class Validite(Measure):
    def __init__(
        self,
        valeur: float = None,
        rang: int = None,
        jours_depuis_derniere_publication: float = None,
        depassements_delai_entre_notification_et_publication: float = None,
    ):
        self.valeur = valeur
        self.rang = rang
        self.jours_depuis_derniere_publication = jours_depuis_derniere_publication
        self.depassements_delai_entre_notification_et_publication = (
            depassements_delai_entre_notification_et_publication
        )

    def compute_value(self):
        self.valeur = app.divide_and_round(
            self.jours_depuis_derniere_publication
            + self.depassements_delai_entre_notification_et_publication,
            2,
        )

    def to_dict(self):
        return {
            "synthese": {"valeur": self.valeur, "rang": self.rang},
            "detail": {
                "jours_depuis_derniere_publication": self.jours_depuis_derniere_publication,
                "depassements_delai_entre_notification_et_publication": self.depassements_delai_entre_notification_et_publication,
            },
        }

    @classmethod
    def from_dict(cls, d: dict):
        """Instancie une classe depuis un dictionnaire.

        Args:
            d (dict): Dictionnaire

        Returns:
            Validite: Instance créée
        """
        valeur = d["synthese"]["valeur"]
        rang = d["synthese"]["rang"]
        jours_depuis_derniere_publication = d["detail"][
            "jours_depuis_derniere_publication"
        ]
        depassements_delai_entre_notification_et_publication = d["detail"][
            "depassements_delai_entre_notification_et_publication"
        ]
        return cls(
            valeur,
            rang,
            jours_depuis_derniere_publication,
            depassements_delai_entre_notification_et_publication,
        )


class Completude(Measure):
    def __init__(
        self,
        valeur: float = None,
        rang: int = None,
        donnees_manquantes=None,
        valeurs_non_renseignees=None,
    ):
        self.valeur = valeur
        self.rang = rang
        self.donnees_manquantes = donnees_manquantes
        self.valeurs_non_renseignees = valeurs_non_renseignees

    def compute_value(self):
        self.valeur = app.divide_and_round(
            self.donnees_manquantes + self.valeurs_non_renseignees, 2
        )

    def to_dict(self):
        return {
            "synthese": {"valeur": self.valeur, "rang": self.rang},
            "detail": {
                "donnees_manquantes": self.donnees_manquantes,
                "valeurs_non_renseignees": self.valeurs_non_renseignees,
            },
        }

    @classmethod
    def from_dict(cls, d: dict):
        """Instancie une classe depuis un dictionnaire.

        Args:
            d (dict): Dictionnaire

        Returns:
            Completude: Instance créée
        """
        valeur = d["synthese"]["valeur"]
        rang = d["synthese"]["rang"]
        donnees_manquantes = d["detail"]["donnees_manquantes"]
        valeurs_non_renseignees = d["detail"]["valeurs_non_renseignees"]
        return cls(valeur, rang, donnees_manquantes, valeurs_non_renseignees)


class Conformite(Measure):
    def __init__(
        self,
        valeur: float = None,
        rang: int = None,
        caracteres_mal_encodes=None,
        formats_non_valides=None,
        valeurs_non_valides=None,
    ):
        self.valeur = valeur
        self.rang = rang
        self.caracteres_mal_encodes = caracteres_mal_encodes
        self.formats_non_valides = formats_non_valides
        self.valeurs_non_valides = valeurs_non_valides

    def compute_value(self):
        self.valeur = app.divide_and_round(
            self.caracteres_mal_encodes
            + self.formats_non_valides
            + self.valeurs_non_valides,
            3,
        )

    def to_dict(self):
        return {
            "synthese": {"valeur": self.valeur, "rang": self.rang},
            "detail": {
                "caracteres_mal_encodes": self.caracteres_mal_encodes,
                "formats_non_valides": self.formats_non_valides,
                "valeurs_non_valides": self.valeurs_non_valides,
            },
        }

    @classmethod
    def from_dict(cls, d: dict):
        """Instancie une classe depuis un dictionnaire.

        Args:
            d (dict): Dictionnaire

        Returns:
            Conformite: Instance créée
        """
        valeur = d["synthese"]["valeur"]
        rang = d["synthese"]["rang"]
        caracteres_mal_encodes = d["detail"]["caracteres_mal_encodes"]
        formats_non_valides = d["detail"]["formats_non_valides"]
        valeurs_non_valides = d["detail"]["valeurs_non_valides"]
        return cls(
            valeur,
            rang,
            caracteres_mal_encodes,
            formats_non_valides,
            valeurs_non_valides,
        )


class Singularite(Measure):
    def __init__(
        self,
        valeur: float = None,
        rang: int = None,
        identifiants_non_uniques=None,
        lignes_dupliquees=None,
    ):
        self.valeur = valeur
        self.rang = rang
        self.identifiants_non_uniques = identifiants_non_uniques
        self.lignes_dupliquees = lignes_dupliquees

    def compute_value(self):
        self.valeur = app.divide_and_round(
            self.identifiants_non_uniques + self.lignes_dupliquees, 2
        )

    def to_dict(self):
        return {
            "synthese": {"valeur": self.valeur, "rang": self.rang},
            "detail": {
                "identifiants_non_uniques": self.identifiants_non_uniques,
                "lignes_dupliquees": self.lignes_dupliquees,
            },
        }

    @classmethod
    def from_dict(cls, d: dict):
        """Instancie une classe depuis un dictionnaire.

        Args:
            d (dict): Dictionnaire

        Returns:
            Singularite: Instance créée
        """
        valeur = d["synthese"]["valeur"]
        rang = d["synthese"]["rang"]
        identifiants_non_uniques = d["detail"]["identifiants_non_uniques"]
        lignes_dupliquees = d["detail"]["lignes_dupliquees"]
        return cls(valeur, rang, identifiants_non_uniques, lignes_dupliquees)
