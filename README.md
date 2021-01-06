# wikipathways-map

This repository contains several python scripts to build
a network of relations between WikiPathways pathways and
external vocabularies.

Presentation given to WikiPathways Developer Conference Call
on January 6th, 2021: http://bit.ly/3neYZ5O

## Data

| File | Description |
| ---- | ----------- |
| [biomappings_subset.tsv](https://github.com/cthoyt/wikipathways-map/blob/main/resources/biomappings_subset.tsv) | Manually curated relationships from Biomappings relvant for WikiPathways |
| [compath_subset.tsv](https://github.com/cthoyt/wikipathways-map/blob/main/resources/compath_subset.tsv) | Manually curated relationships from ComPath relvant for WikiPathways |
| [diseases.tsv](https://github.com/cthoyt/wikipathways-map/blob/main/resources/diseases.tsv) | WikiPathway toDOID relationships extracted from WikiPathways SPARQL endpoint |
| [pw.tsv](https://github.com/cthoyt/wikipathways-map/blob/main/resources/pw.tsv) | WikiPathway to Pathway Ontology relationships extracted from WikiPathways SPARQL endpoint |
| [orthologs.tsv](https://github.com/cthoyt/wikipathways-map/blob/main/resources/orthologs.tsv) | Orthologous pathways inside WikiPathways generated by lexical matching with [Gilda](https://github.com/indralab/gilda) |

## Licensing

- Data from Biomappings are licensed under the CC-0 license
- Data from ComPath are licensed under the MIT License
- Data from WikiPathways are licensed under the CC-0 license
- Original data in this repo are licensed under the CC-0 license
- Code in this repo is licensed under the MIT License

## Visualization

The network can be viewed on [NDEx](https://public.ndexbio.org/viewer/networks/2b3ed6af-5031-11eb-9e72-0ac135e8bacf)

## Sources

- WikiPathways
- [BioMappings](https://github.com/biomappings/biomappings)
- [ComPath](https://github.com/compath/compath-resources)
