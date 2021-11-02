from qualite_decp.audit import measures
from qualite_decp.audit import app


class AuditResultsOneSource:
    def __init__(
        self,
        source: str,
        general: measures.General = None,
        validite: measures.Validite = None,
        completude: measures.Completude = None,
        conformite: measures.Conformite = None,
        coherence: measures.Coherence = None,
        singularite: measures.Singularite = None,
        exactitude: measures.Exactitude = None,
    ):
        if general is None:
            general = measures.General()
        if validite is None:
            validite = measures.Validite()
        if completude is None:
            completude = measures.Completude()
        if conformite is None:
            conformite = measures.Conformite()
        if coherence is None:
            coherence = measures.Coherence()
        if singularite is None:
            singularite = measures.Singularite()
        if exactitude is None:
            exactitude = measures.Exactitude()

        self.source = source
        self.general = general
        self.validite = validite
        self.completude = completude
        self.conformite = conformite
        self.coherence = coherence
        self.singularite = singularite
        self.exactitude = exactitude

    def compute_general(self):
        """Calcule les indicateurs généraux pour cette source."""
        self.compute_values()
        self.general.valeur = app.divide_and_round(
            self.validite.valeur
            + self.exactitude.valeur
            + self.completude.valeur
            + self.conformite.valeur
            + self.coherence.valeur
            + self.singularite.valeur,
            6,
        )

    def compute_values(self):
        self.validite.compute_value()
        self.completude.compute_value()
        self.conformite.compute_value()
        self.coherence.compute_value()
        self.singularite.compute_value()
        self.exactitude.compute_value()

    def to_dict(self):
        return {
            "source": self.source,
            "general": self.general.to_dict(),
            "validite": self.validite.to_dict(),
            "completude": self.completude.to_dict(),
            "conformite": self.conformite.to_dict(),
            "coherence": self.coherence.to_dict(),
            "singularite": self.singularite.to_dict(),
            "exactitude": self.exactitude.to_dict(),
        }

    @classmethod
    def from_dict(cls, d):
        """Crée une instance de la classe depuis un dictionnaire.

        Args:
            d (dict): Dictionnaire

        Returns:
            AuditResultsOneSource: Instance créée
        """
        source = d["source"]
        general = measures.General.from_dict(d["general"])
        validite = measures.Validite.from_dict(d["validite"])
        completude = measures.Completude.from_dict(d["completude"])
        conformite = measures.Conformite.from_dict(d["conformite"])
        coherence = measures.Coherence.from_dict(d["coherence"])
        singularite = measures.Singularite.from_dict(d["singularite"])
        exactitude = measures.Exactitude.from_dict(d["exactitude"])
        return cls(
            source,
            general,
            validite,
            completude,
            conformite,
            coherence,
            singularite,
            exactitude,
        )
