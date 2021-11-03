from typing import List

from qualite_decp import download
from qualite_decp.audit import audit_results_one_source


class AuditResults:
    def __init__(
        self, results: List[audit_results_one_source.AuditResultsOneSource] = None
    ):
        if results is None:
            results = list()
        self.results = results

    def extract_results_for_source(self, source: str):
        """Extrait les résultats d'audit pour une source.

        Args:
            source (str): Nom de la source

        Returns:
            [audit_results_one_source.AuditResultsOneSource]: Résultats d'audit
        """
        return [r for r in self.results if r.source == source][0]

    def add_results(
        self, source_results: audit_results_one_source.AuditResultsOneSource
    ):
        """Ajoute un résultat d'audit d'une source à l'instance

        Args:
            source_results (audit_results_one_source.AuditResultsOneSource): Résultats à ajouter
        """
        self.results.append(source_results)

    def compute_ranks(self):
        """Calcule les rangs des sources pour tous les indicateurs"""
        general_values = dict()
        validite_values = dict()
        completude_values = dict()
        conformite_values = dict()
        coherence_values = dict()
        singularite_values = dict()
        exactitude_values = dict()
        for res in self.results:
            general_values[res.source] = res.general.valeur
            validite_values[res.source] = res.validite.valeur
            completude_values[res.source] = res.completude.valeur
            conformite_values[res.source] = res.conformite.valeur
            coherence_values[res.source] = res.coherence.valeur
            singularite_values[res.source] = res.singularite.valeur
            exactitude_values[res.source] = res.exactitude.valeur
        for source, rank in self.rank_dict(general_values).items():
            self.extract_results_for_source(source).general.rang = rank
        for source, rank in self.rank_dict(validite_values).items():
            self.extract_results_for_source(source).validite.rang = rank
        for source, rank in self.rank_dict(completude_values).items():
            self.extract_results_for_source(source).completude.rang = rank
        for source, rank in self.rank_dict(conformite_values).items():
            self.extract_results_for_source(source).conformite.rang = rank
        for source, rank in self.rank_dict(coherence_values).items():
            self.extract_results_for_source(source).coherence.rang = rank
        for source, rank in self.rank_dict(singularite_values).items():
            self.extract_results_for_source(source).singularite.rang = rank
        for source, rank in self.rank_dict(exactitude_values).items():
            self.extract_results_for_source(source).exactitude.rang = rank

    def to_list(self):
        return [r.to_dict() for r in self.results]

    def to_json(self, path: str):
        """Sauvegarde la classe dans un fichier JSON.

        Args:
            path (str): Chemin vers le fichier .json
        """
        l = self.to_list()
        download.save_json(l, path)

    @classmethod
    def from_list(cls, l: list):
        results = [
            audit_results_one_source.AuditResultsOneSource.from_dict(le) for le in l
        ]
        return cls(results=results)

    @classmethod
    def from_json(cls, path: str):
        """Crée une instance de la classe depuis un fichier JSON.

        Args:
        path (str): Chemin du fichier .json

        Returns:
            AuditResults: Instance créée
        """
        l = download.open_json(path)
        return cls.from_list(l)

    @staticmethod
    def rank_dict(d):
        r = {key: rank for rank, key in enumerate(sorted(set(d.values())), 1)}
        r = {k: r[v] for k, v in d.items()}
        return r
