from typing import get_type_hints, Dict, List

from gremlin_python.structure.io import graphsonV3d0

from src.graph_model import SecurityEvent, Traversel
from src.parse_datetime import from_date_str
from src.gremlin import GREMLIN

# (fixme) traversel should start from ecosystem node
def _query_template():
    return '''
        g.V().hasLabel('security_event').{security_event_query}.
          as('security_event').
          map(
            outE('triaged_to').inV().hasLabel('probable_vulnerability').{probable_vulnerability_query}
            ).as('probable_vulnerability').
          map(
            outE('affects').inV().hasLabel('dependency_version')
          ).as('dependency_version').
          map(
            inE('has_version').outV().hasLabel('dependency').{dependency_query}
          ).as('dependency').
          select('security_event', 'probable_vulnerability', 'dependency_version', 'dependency').
          by(elementMap()).
          by(elementMap()).
          by(elementMap()).
          by(elementMap())'''

def _get_security_event_query_filters(args: Dict) -> str:
    assert 'updated_at' in get_type_hints(SecurityEvent)
    query = []
    from_date = from_date_str(args['from_date'])
    to_date = from_date_str(args['to_date'])
    if from_date > 0 and to_date > 0:
        query.append('''has('updated_at', between({from_date}, {to_date}))'''.format(from_date=from_date, to_date=to_date))
    return 'identity()' if len(query) is 0 else '.'.join(query)

def _get_probable_vul_query_filters(args: Dict) -> str:
    query = []
    return 'identity()' if len(query) is 0 else '.'.join(query)

def _get_dependency_query_filters(args: Dict) -> str:
    query = []
    return 'identity()' if len(query) is 0 else '.'.join(query)

def _to_response_model(gremlin_response: Dict) -> Dict:
    reader = graphsonV3d0.GraphSONReader()
    rsp = reader.toObject(gremlin_response)
    print(rsp)
    return rsp['result']['data']

def query_graph(args: Dict):
    query = _query_template().format(
            security_event_query=_get_security_event_query_filters(args),
            probable_vulnerability_query=_get_probable_vul_query_filters(args),
            dependency_query=_get_dependency_query_filters(args))
    rsp = _to_response_model(GREMLIN.execute_query(query))
    return rsp

