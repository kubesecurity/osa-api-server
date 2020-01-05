from src.graph_model import Traversel
from src.ingestion_data import IngestionData

def _ingest_pcve(pcve):
    g = Traversel()
    # (fixme) create ecosystem node if not present
    # (fixme) use ecosystem node as well
    # n.create_ecosystem_node(ecosystem_name=pcve['ecosystem'])
    (g.addV(pcve.dependency()).as_('dependency')
     .addV(pcve.version()).as_('version')
     .addV(pcve.security_event()).as_('security_event')
     .addV(pcve.probable_cve()).as_('pcve')
     .has_version('dependency', 'version')
     .triaged_to('security_event', 'pcve')
     .affects('pcve', 'version')
     .next())
    print(str(g))

def ingest_data_into_graph(data):
    for pcve in data:
        _ingest_pcve(IngestionData(pcve))

if __name__ == '__main__':
    PCVES = [{
        "ecosystem": "golang",
        "repo_name": "Azure/azure-sdk-for-go",
        "event_type": "IssuesEvent",
        "status": "closed",
        "url": "https://github.com/Azure/azure-sdk-for-go/issues/1204",
        "security_model_flag": 0,
        "cve_model_flag": 0,
        "triage_is_security": 0,
        "triage_is_cve": 0,
        "triage_feedback_comments": "",
        "id": 302919731,
        "number": 1204,
        "api_url": "https://api.github.com/repos/Azure/azure-sdk-for-go/issues/1204",
        "created_at": "2018-03-07 00:27:11+00:00",
        "updated_at": "2019-12-03 09:03:36+00:00",
        "closed_at": "2019-12-03 09:03:36+00:00",
        "creator_name": "vladbarosan",
        "creator_url": "https://github.com/vladbarosan"
    }]
    ingest_data_into_graph(PCVES)
