from typing import Iterable

from biomappings import load_mappings
from biomappings.resources import MappingTuple

from utils import write


def iterate_biomappings() -> Iterable[MappingTuple]:
    for mapping in load_mappings():
        mt = MappingTuple.from_dict(mapping)
        if mt.source_prefix == 'wikipathways' or mt.target_prefix == 'wikipathways':
            yield mt


if __name__ == '__main__':
    write(iterate_biomappings(), 'biomappings_subset.tsv')
