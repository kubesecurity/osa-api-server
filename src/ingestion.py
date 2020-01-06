from gremlin_connect.gremlin_adapter import GremlinAdapter

from src.graph_model import Traversel
from src.ingestion_data import IngestionData

gremlin_adapter = GremlinAdapter()
def _ingest_pcve(pcve):
    g = Traversel()
    query = str(g.add_unique_node(pcve.dependency)
     .add_unique_node(pcve.version)
     .add_unique_node(pcve.security_event)
     .add_unique_node(pcve.probable_cve)
     .has_version(pcve.dependency, pcve.version)
     .triaged_to(pcve.security_event, pcve.probable_cve)
     .affects(pcve.probable_cve, pcve.version)
     .next())
    return gremlin_adapter.execute_query(query)

def ingest_data_into_graph(data):
    for pcve in data:
        _ingest_pcve(IngestionData(pcve))
