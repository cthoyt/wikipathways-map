import os
from typing import Iterable

from biomappings.resources import MAPPINGS_HEADER, MappingTuple, _write_helper

HERE = os.path.abspath(os.path.dirname(__file__))
RESOURCES = os.path.join(HERE, 'resources')
os.makedirs(RESOURCES, exist_ok=True)


def write(mapping_tuples: Iterable[MappingTuple], name: str) -> None:
    _write_helper(MAPPINGS_HEADER, (m.as_dict() for m in mapping_tuples), os.path.join(RESOURCES, name), 'w')
