"""Abstracts data ingestion to graph db."""

from src.graph_traversel import Traversel
from src.ingestion_data import IngestionData
from src.gremlin import execute_query


def ingest_data_into_graph(data):
    """Ingests given json object to graph."""
    pcve = IngestionData(data)
    g = Traversel()  # pylint: disable=invalid-name
    query = (g.add_unique_node(pcve.dependency)
             .add_unique_node(pcve.version)
             .add_unique_node(pcve.security_event)
             .add_unique_node(pcve.probable_cve)
             .has_version(pcve.dependency, pcve.version)
             .triaged_to(pcve.security_event, pcve.probable_cve)
             .affects(pcve.probable_cve, pcve.version)
             .next())
    execute_query(query)
    return {'status': 'success'}
