from typing import get_type_hints, Dict, List

from src.graph_model import SecurityEvent, EventType, Dependency
from src.graph_traversel import Traversel
from src.parse_datetime import from_date_str
from src.gremlin import execute_query

# (fixme) traversel should start from ecosystem node
def _query_template():
    return '''
        g.V().hasLabel('security_event').{security_event_query}.
          as('feedback', 'security_event').
            outE('triaged_to').inV().hasLabel('probable_vulnerability').{probable_vulnerability_query}.
          as('probable_vulnerability').
            outE('affects').inV().hasLabel('dependency_version').
          as('dependency_version').
            inE('has_version').outV().hasLabel('dependency').{dependency_query}.
          as('dependency').
          select('feedback', 'security_event', 'probable_vulnerability', 'dependency_version', 'dependency').
          by(inE().outV().valueMap().by(unfold()).fold()).
          by(valueMap().by(unfold())).
          by(valueMap().by(unfold())).
          by(valueMap().by(unfold())).
          by(valueMap().by(unfold()))'''

def _get_security_event_query_filters(args: Dict) -> str:
    assert 'updated_at' in get_type_hints(SecurityEvent)
    query = []
    from_date = args['from_date']
    to_date = args['to_date']
    if from_date and to_date:
        query.append(
                '''has('updated_at', between({from_date}, {to_date}))'''.format(
                    from_date=from_date, to_date=to_date))
    event_type = args['event_type']
    if event_type:
        query.append('''has('event_type', '{event_type}')'''.format(event_type=EventType[event_type].value))
    return 'identity()' if len(query) is 0 else '.'.join(query)

def _get_probable_vuln_query_filters(args: Dict) -> str:
    query = []
    return 'identity()' if len(query) is 0 else '.'.join(query)

def _get_dependency_query_filters(args: Dict) -> str:
    assert 'dependency_name' in get_type_hints(Dependency)
    query = []
    repo = args['repo']
    if repo is not None:
        query.append('''has('dependency_name', '{repo}')'''.format(repo=repo))

    return 'identity()' if len(query) is 0 else '.'.join(query)

def query_graph(args: Dict):
    query = _query_template().format(
            security_event_query=_get_security_event_query_filters(args),
            probable_vulnerability_query=_get_probable_vuln_query_filters(args),
            dependency_query=_get_dependency_query_filters(args))
    result = execute_query(query)['result']['data']
    return result

