"""Implements search from graph API."""

from typing import get_type_hints, Dict

from src.graph_model import SecurityEvent, EventType, FeedBackType, EcosystemType, StatusType
from src.gremlin import execute_query
from src.sanitizer import sanitize

from src.config import DAIQUIRI_LOG_LEVEL

import daiquiri

daiquiri.setup(level=DAIQUIRI_LOG_LEVEL)
log = daiquiri.getLogger(__name__)


def _query_template():
    return '''
            g.V()
            .{security_event_query}
            .as('security_event').select('security_event')
            .by(valueMap())'''


def _identity_or_conditional(query) -> str:
    return 'identity()' if len(query) == 0 else '.'.join(query)


def _get_security_event_query_filters(args: Dict) -> str:
    assert 'updated_at' in get_type_hints(SecurityEvent)
    query = []

    ecosystem = args['ecosystem']
    query.append('''has('ecosystem', '{ecosystem}')'''.format(ecosystem=EcosystemType[ecosystem].value))

    # will retrive only probable cve data
    query.append('''has('probable_cve', 1)''')

    repo = args['repo']
    if isinstance(repo, list) and len(repo) > 0:
        repo = sanitize(repo)
        query.append('''has('repo_name', within({repo}))'''.format(repo=repo))

    updated_dates = args['updated_date']
    if isinstance(updated_dates, list) and len(updated_dates) > 0:
        query.append('''has('updated_date', within({updated_dates}))'''.format(updated_dates=updated_dates))

    updated_yearmonth = args['updated_yearmonth']
    if isinstance(updated_yearmonth, list) and len(updated_yearmonth) > 0:
        query.append('''has('updated_yearmonth', within({updated_yearmonth}))'''
                     .format(updated_yearmonth=updated_yearmonth))

    return _identity_or_conditional(query)


def _filter_data_for_other_condition(args: Dict, data):
    updated_data = []
    for item in data:

        if _is_valid_feedback(args, item) and \
                _is_valid_event_type(args, item) and \
                _is_valid_status(args, item):
            updated_data.append(item)

    log.info("After filtering other condition got data count as {count}".format(count=len(updated_data)))
    return updated_data


def _is_valid_feedback(args: Dict, item) -> bool:
    feedback = args['feedback']
    return True if feedback is None \
        else ('overall_feedback' in item and item['overall_feedback'][0]) == FeedBackType[feedback].value


def _is_valid_event_type(args: Dict, item) -> bool:
    event_type = args['event_type']
    return True if event_type is None else item['event_type'][0] == EventType[event_type].value


def _is_valid_status(args: Dict, item) -> bool:
    status = args['status']
    return True if status is None else item['status'][0] == StatusType[status].value


def query_graph(args: Dict):
    """Retrives graph nodes based on the given criteria."""
    query = _query_template().format(security_event_query=_get_security_event_query_filters(args))
    result = execute_query(query)['result']['data']
    log.info("Before filtering other condition data count as {count}".format(count=len(result)))

    return _filter_data_for_other_condition(args, result)
