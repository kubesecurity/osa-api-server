from gremlin_connect.gremlin_adapter import GremlinAdapter

from src.graph_model import Traversel
from src.ingestion_data import IngestionData

gremlin_adapter = GremlinAdapter()
def _ingest_pcve(pcve):
    g = Traversel()
    # (fixme) create ecosystem node if not present
    # (fixme) use ecosystem node as well
    # n.create_ecosystem_node(ecosystem_name=pcve['ecosystem'])
    query = str(g.addV(pcve.dependency).as_('dependency')
     .addV(pcve.version).as_('version')
     .addV(pcve.security_event).as_('security_event')
     .addV(pcve.probable_cve).as_('pcve')
     .has_version('dependency', 'version')
     .triaged_to('security_event', 'pcve')
     .affects('pcve', 'version')
     .next())
    return gremlin_adapter.execute_query(query)

def ingest_data_into_graph(data):
    for pcve in data:
        _ingest_pcve(IngestionData(pcve))
