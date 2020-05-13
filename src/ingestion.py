"""Abstracts data ingestion to graph db."""

from src.graph_traversel import Traversel
from src.ingestion_data import IngestionData
from src.gremlin import execute_query


def ingest_data_into_graph(data):
    """Ingests given json object to graph."""
    pcve = IngestionData(data)
    g = Traversel()  # pylint: disable=invalid-name
    query = (g
             .add_update_unique_node_with_diff_properties(pcve.security_event, pcve.updated_security_event)
             .next())

    execute_query(query)
    return {'status': 'success'}
