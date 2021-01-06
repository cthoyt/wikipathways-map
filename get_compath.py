from typing import Iterable

from biomappings.resources import MappingTuple
from compath_resources import get_df

import pyobo
from utils import write


def _fix_relation(r):
    if r == 'equivalentTo':
        return 'skos:exactMatch'
    elif r == 'isPartOf':
        return 'partOf'
    raise ValueError


def iterate_compath_mappings() -> Iterable[MappingTuple]:
    df = get_df()
    del df['Source Name']
    del df['Target Name']
    df['Mapping Type'] = df['Mapping Type'].map(_fix_relation)
    for source_prefix, source_id, relation, target_prefix, target_id in df.values:
        if source_prefix == 'kegg':
            source_prefix = 'kegg.pathway'
            source_id = source_id.removeprefix('path:')
        if target_prefix == 'kegg':
            target_prefix = 'kegg.pathway'
            target_id = source_id.removeprefix('path:')
        if source_prefix == 'wikipathways' or target_prefix == 'wikipathways':
            yield MappingTuple(
                source_prefix,
                source_id,
                pyobo.get_name(source_prefix, source_id),
                relation,
                target_prefix,
                target_id,
                pyobo.get_name(target_prefix, target_id),
                'manual',
                'compath',
            )


if __name__ == '__main__':
    write(iterate_compath_mappings(), 'compath.tsv')
