from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Dna:
    code: List[float]
    genes_features: List[List[float]]
    genes_control: List[bool]

    @staticmethod
    def read(data: str, gene_len: int = 1) -> "Dna":
        assert data and len(data.split(',')) > gene_len
        dna_code = Dna._read_dna_code_from(data)
        features, controls = Dna._read_genes_from(dna_code, gene_len)
        return Dna(code=dna_code, genes_features=features, genes_control=controls)

    @staticmethod
    def _read_dna_code_from(data: str) -> List[float]:
        return [float(gene) for gene in data.split(',')]

    @staticmethod
    def _read_genes_from(dna_code: List[float], gene_len: int) -> Tuple[List[List[float]], List[bool]]:
        features: List[List[float]] = []
        controls: List[bool] = []
        i, end = 0, len(dna_code)
        while i < end:
            features.append(dna_code[i:i+gene_len])
            i += gene_len
            end -= 1
        for i in range(end, len(dna_code)):
            controls.append(dna_code[i] > 0.5)
        return features, controls
