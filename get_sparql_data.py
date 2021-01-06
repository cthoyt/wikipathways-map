"""Get data from Wikipathways SPARQL."""

from typing import Iterable

from biomappings.resources import MappingTuple

import pyobo
from pyobo.xrefdb.sources.wikidata import _run_query
from utils import write

BASE = 'http://sparql.wikipathways.org/sparql'


def iterate_pathway_disease_pairs() -> Iterable[MappingTuple]:
    for wp_id, do_id in _q('diseaseOntologyTag', 'http://purl.obolibrary.org/obo/DOID_'):
        yield MappingTuple(
            source_prefix='wikipathways',
            source_id=wp_id,
            source_name=pyobo.get_name('wikipathways', wp_id),
            relation='aboutDisease',
            target_prefix='doid',
            target_identifier=do_id,
            target_name=pyobo.get_name('doid', do_id),
            type='manual',
            source='wikipathways',
        )


def iterate_pathway_pw_pairs() -> Iterable[MappingTuple]:
    for wp_id, pw_id in _q('pathwayOntologyTag', 'http://purl.obolibrary.org/obo/PW_'):
        yield MappingTuple(
            source_prefix='wikipathways',
            source_id=wp_id,
            source_name=pyobo.get_name('wikipathways', wp_id),
            relation='speciesSpecific',
            target_prefix='pw',
            target_identifier=pw_id,
            target_name=pyobo.get_name('pw', pw_id),
            type='manual',
            source='wikipathways',
        )


def _q(tag, url_prefix):
    query = f"""
    select ?identifier ?xref where {{
      ?pathway a wp:Pathway .
      ?pathway dcterms:identifier ?identifier .
      ?pathway wp:{tag} ?xref
    }}
    """
    for row in _run_query(query, base=BASE):
        wp_id = row['identifier']['value']
        xref_id = row['xref']['value'].removeprefix(url_prefix)
        yield wp_id, xref_id


def main():
    write(iterate_pathway_pw_pairs(), 'pw.tsv')
    write(iterate_pathway_disease_pairs(), 'diseases.tsv')


if __name__ == '__main__':
    main()
