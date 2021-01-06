"""Uploads the resources to an NDEx Network.

.. seealso:: https://public.ndexbio.org/viewer/networks/2b3ed6af-5031-11eb-9e72-0ac135e8bacf
"""

import itertools as itt
import os

import pandas as pd
from biomappings.utils import MiriamValidator
from ndex2 import NiceCXBuilder
from tqdm import tqdm

import pyobo
import pystow
from utils import RESOURCES


def main():
    dfs = [
        pd.read_csv(os.path.join(RESOURCES, name), sep='\t')
        for name in os.listdir(RESOURCES)
        if name.endswith('.tsv')
    ]
    sdf = pd.concat(dfs)
    upload(sdf)


def upload(df: pd.DataFrame):
    cx = NiceCXBuilder()
    cx.set_name('Wikipathways Pathway Landscape')
    cx.add_network_attribute(
        'description',
        'Integrative resource of pathway definitions and equivalences touching WikiPathways',
    )
    cx.add_network_attribute('author', 'Charles Tapley Hoyt')

    miriam_validator = MiriamValidator()
    prefixes = set(itt.chain(df['source prefix'], df['target prefix']))
    context = {
        'orcid': 'https://identifiers.org/orcid:',
        'ncbitaxon': 'https://identifiers.org/taxonomy:',
    }
    for prefix in prefixes:
        if prefix in miriam_validator.entries:
            if miriam_validator.namespace_embedded(prefix):
                prefix = prefix.upper()
            context[prefix] = f'https://identifiers.org/{prefix}:'
        else:
            pass  # TODO
    cx.set_context(context)

    curie_to_id = {}
    curies = set(map(tuple, itt.chain(
        df[['source prefix', 'source identifier', 'source name']].values,
        df[['target prefix', 'target identifier', 'target name']].values,
    )))
    for prefix, identifier, name in tqdm(curies, desc='Adding nodes', unit_scale=True, unit='node'):
        if name and name != 'None':
            label = f'{name} ({prefix}:{identifier})'
        else:
            tqdm.write(f'no name for {prefix}:{identifier}')
            label = f'{prefix}:{identifier}'

        curie_to_id[prefix, identifier] = cx.add_node(name=label, represents=f'{prefix}:{identifier}')
        cx.add_node_attribute(curie_to_id[prefix, identifier], 'database', prefix)
        cx.add_node_attribute(curie_to_id[prefix, identifier], 'identifier', str(identifier))
        if prefix not in {'ncbigene', 'doid', 'pw', 'go', 'mesh', 'efo'}:
            species = pyobo.get_species(prefix, identifier)
            cx.add_node_attribute(curie_to_id[prefix, identifier], 'species', f'ncbitaxon:{species}')

    it = tqdm(
        df.values,
        unit_scale=True,
        unit='edge',
        desc='Adding relations',
    )
    for source_ns, source_id, _, relation, target_ns, target_id, _, mtype, provenance in it:
        edge = cx.add_edge(
            source=curie_to_id[source_ns, source_id],
            target=curie_to_id[target_ns, target_id],
            interaction=relation,
        )
        cx.add_edge_attribute(edge, 'provenance', provenance)
        cx.add_edge_attribute(edge, 'type', mtype)

    nice_cx = cx.get_nice_cx()
    nice_cx.update_to(
        uuid='2b3ed6af-5031-11eb-9e72-0ac135e8bacf',
        server='http://public.ndexbio.org',
        username=pystow.get_config('ndex', 'username'),
        password=pystow.get_config('ndex', 'password'),
    )


if __name__ == '__main__':
    main()
