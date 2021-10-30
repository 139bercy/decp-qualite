from qualite_decp.audit import measures


class AuditResultsOneSource:
    def __init__(
        self,
        source: str,
        general: measures.General = measures.General(),
        validite: measures.Validite = measures.Validite(),
        completude: measures.Completude = measures.Completude(),
        conformite: measures.Conformite = measures.Conformite(),
        coherence: measures.Coherence = measures.Coherence(),
        singularite: measures.Singularite = measures.Singularite(),
        exactitude: measures.Exactitude = measures.Exactitude(),
    ):
        self.source = source
        self.general = general
        self.validite = validite
        self.completude = completude
        self.conformite = conformite
        self.coherence = coherence
        self.singularite = singularite
        self.exactitude = exactitude

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
