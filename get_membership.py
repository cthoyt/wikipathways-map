from typing import Iterable

from biomappings.resources import MappingTuple

import pyobo
from pyobo.struct import has_part
from utils import write


def iterate_memberships() -> Iterable[MappingTuple]:
    df = pyobo.get_filtered_relations_df('wikipathways', has_part)
    for wp_id, target_ns, target_id in df.values:
        yield MappingTuple(
            source_prefix='wikipathways',
            source_id=wp_id,
            source_name=pyobo.get_name('wikipathways', wp_id),
            relation=has_part.name,
            target_prefix=target_ns,
            target_identifier=target_id,
            target_name=pyobo.get_name(target_ns, target_id),
            type='manual',
            source='wikipathways',
        )


if __name__ == '__main__':
    write(iterate_memberships(), 'members.tsv')
