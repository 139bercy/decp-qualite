from typing import List

from qualite_decp import download
from qualite_decp.audit import audit_results_one_source


class AuditResults:
    def __init__(
        self, results: List[audit_results_one_source.AuditResultsOneSource] = list()
    ):
        self.results = results

    def extract_results_for_source(self, source: str):
        return [r for r in self.results if r.source == source][0]

    def add_results(self, results: audit_results_one_source.AuditResultsOneSource):
        self.results.append(results)

    def to_list(self):
        return [r.to_dict() for r in self.results]

    def to_json(self, path):
        l = self.to_list()
        download.save_json(l, path)

    @classmethod
    def from_list(cls, l):
        results = [
            audit_results_one_source.AuditResultsOneSource.from_dict(le) for le in l
        ]
        return cls(results=results)

    @classmethod
    def from_json(cls, path):
        l = download.open_json(path)
        return cls.from_list(l)
