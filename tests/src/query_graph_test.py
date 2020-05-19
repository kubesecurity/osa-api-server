"""Class that contains test cases for query_graph.py logic."""
import json
from unittest.mock import patch

from src.graph_model import EcosystemType
from src.query_graph import query_graph, _query_template, _get_security_event_query_filters
from src.sanitizer import sanitize

args = {
    'ecosystem': 'OPENSHIFT',
    'repo': ['org25/repo10'],
    'updated_date': [20191109, 20191110],
    'updated_yearmonth': [201911],
    'feedback': None,
    'status': None,
    'event_type': None
}


def get_sample_data():
    """Get Sample data by reading json file."""
    sample_security_event_url = 'tests/data/gremlin_get_pvce_sample.json'
    with open(sample_security_event_url) as file:
        security_events = json.load(file)
    return security_events


def mocked_response():
    """Mock response for gremlin output."""
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

        @staticmethod
        def raise_for_status():
            return None

    return MockResponse(get_sample_data(), 200)


def get_security_event_by_url(data, url):
    """Get security events by url."""
    return next(x for x in data if x["url"][0] == sanitize(url))


def test_query_string():
    """Test case to check query string generation."""
    expected_query = '''
                g.V()
                .has('ecosystem', '{ecosystem}')
                .has('probable_cve', 1)
                .has('repo_name', within({repo_name}))
                .has('updated_date', within({updated_date}))
                .has('updated_yearmonth', within({updated_yearmonth}))
             .as('security_event').select('security_event')
             .by(valueMap())'''\
        .format(ecosystem=EcosystemType[args['ecosystem']].value, repo_name=sanitize(args['repo']),
                updated_date=args['updated_date'], updated_yearmonth=args['updated_yearmonth'])
    expected_query_single_line = "".join(expected_query.replace(" ", "").splitlines())

    query = _query_template().format(security_event_query=_get_security_event_query_filters(args))
    query_single_line = "".join(query.replace(" ", "").splitlines())

    assert(query_single_line == expected_query_single_line)


@patch("src.utils.requests.Session.post", return_value=mocked_response())
def test_query_graph_with_basic_conditions(_mock_data):
    """Test query graph code."""
    data = query_graph(args)

    assert(len(data) == 12)


@patch("src.utils.requests.Session.post", return_value=mocked_response())
def test_query_graph_with_all_conditions(_mock_data):
    """Test query graph code."""
    mix_args = {
        'ecosystem': 'OPENSHIFT',
        'repo': ['org25/repo10'],
        'updated_date': [20191109, 20191110],
        'feedback': 'POSITIVE',
        'status': 'OPENED',
        'updated_yearmonth': [201911],
        'event_type': 'PULL_REQUEST',
    }

    data = query_graph(mix_args)

    assert (len(data) == 4)
    assert (get_security_event_by_url(data, 'https://github.com/org25/repo10/issues/52623') is not None)
    assert (get_security_event_by_url(data, 'https://github.com/org25/repo10/issues/52737') is not None)
    assert (get_security_event_by_url(data, 'https://github.com/org25/repo10/issues/18638') is not None)
    assert (get_security_event_by_url(data, 'https://github.com/org25/repo10/issues/73139') is not None)
