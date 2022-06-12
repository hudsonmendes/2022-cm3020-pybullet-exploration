from dataclasses import dataclass
from abc import ABCMeta
from typing import List, Union, Optional

import json
import os
from pathlib import Path

from dna import Dna
from evolution import Evolution

import logging

from hyperparams import Hyperparams
LOGGER = logging.getLogger(__name__)


@dataclass
class PersistenceSettings:
    folder: Path


class BaseRepository(ABCMeta):
    settings: PersistenceSettings

    def __init__(self, settings: PersistenceSettings):
        self.settings = settings

    @staticmethod
    def ensure_file_dir(filepath: Path):
        dir = filepath.parent
        if not os.path.isdir(dir):
            os.makedirs(dir)


class DnaRepository(BaseRepository):

    def filepath(self, species: str) -> Path:
        return self.settings.folder / f"{species}.dna"

    """
    Reads and Writes DNA into files, with options to append/override
    as well as reading specific individuals from the store.
    """

    def read(self, species: str, individual: Optional[int] = None) -> Optional[Dna]:
        """
        Read a particular individual or the top one of a species DNA file.
        """
        if not individual:
            individual = 0
        filepath = self.filepath(species)
        self.ensure_file_dir(filepath)
        if os.path.isfile(filepath):
            with open(filepath, 'r+', encoding='utf-8') as fh:
                for i, line in enumerate(fh):
                    if i == individual:
                        LOGGER.info(f"DNA, {species}.dna, reading line {individual}: {line}")
                        return Dna.parse_dna(line)
        return None

    def write(self, species: str, dna_code: Union[List[float], str], override: bool = False):
        """
        Overrides or appends to a species DNA file.
        """
        filepath = self.filepath(species)
        with open(filepath, 'w+' if override else 'a+', encoding='utf-8') as fh:
            line = dna_code if isinstance(dna_code, str) else ",".join([str(base) for base in dna_code])
            fh.write(f"{line}\n")
            LOGGER.info(f"DNA, {species}.dna, {'overriden' if override else 'appended'}: {line}")


class EvolutionRepository(BaseRepository):
    """
    Keeps Record of the Fitness Map and Hyperparams across generations,
    so the results can be observed later.
    """

    class EvolutionDecoder(json.JSONDecoder):
        pass

    class EvolutionEncoder(json.JSONEncoder):
        pass

    def filepath(self, generation_id) -> Path:
        return self.settings.folder / f'generation-{generation_id}.evo'

    def read(self, generation_id: int) -> Optional[Evolution]:
        filepath = self.filepath(generation_id)
        self.ensure_file_dir(filepath)
        if os.path.isfile(filepath):
            with open(filepath, 'r', encoding='utf-8') as fh:
                return json.load(fh, cls=EvolutionRepository.EvolutionDecoder)
        return None

    def write(self, record: Evolution):
        filepath = self.filepath(record.generation_id)
        self.ensure_file_dir(filepath)
        with open(filepath, 'w+', encoding='utf-8') as fh:
            json.dump(record, fh, cls=EvolutionRepository.EvolutionEncoder)