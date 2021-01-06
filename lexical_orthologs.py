# -*- coding: utf-8 -*-

"""Generate orthologous relations based on lexical matching."""

from typing import Iterable

from biomappings.resources import MappingTuple
from biomappings.utils import get_script_url
from gilda.process import normalize
from tqdm.contrib.itertools import product

import pyobo
from utils import write


def iterate_orthologous_lexical_matches(prefix) -> Iterable[MappingTuple]:
    """Generate orthologous relations between lexical matches from different species."""
    names = pyobo.get_id_name_mapping(prefix)
    species = pyobo.get_id_species_mapping(prefix)
    provenance = get_script_url(__file__)

    count = 0
    it = product(names.items(), names.items(), unit_scale=True, desc=f'matching {prefix}')
    for (source_id, source_name), (target_id, target_name) in it:
        if species[source_id] == species[target_id]:
            continue
        if source_id > target_id:  # make canonical order
            continue
        if _lexical_exact_match(source_name, target_name):
            count += 1
            yield MappingTuple(
                prefix, source_id, source_name,
                'orthologous',
                prefix, target_id, target_name,
                'lexical',
                provenance,
            )
    print(f'Identified {count} orthologs in {prefix}')


def _lexical_exact_match(name1: str, name2: str) -> bool:
    return normalize(name1) == normalize(name2)


if __name__ == '__main__':
    write(iterate_orthologous_lexical_matches('wikipathways'), 'orthologs.tsv')
