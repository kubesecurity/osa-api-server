"""Tests to cover utils code."""

from unittest.mock import patch

from src.utils import fetch_nodes


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

    return MockResponse(
        {"requestId": "5cc29849-8e9b-4b66-90d0-f2569dc962b9", "status": {"message": "", "code": 200, "attributes": {}},
         "result": {"data": [], "meta": {}}}, 200)


@patch("src.utils.requests.post", return_value=mocked_response())
def test_fetch_nodes_invalid_payload(_mock1):
    """Test fetch node method with invalid poayload."""
    resp = fetch_nodes(payload={})
    assert resp['warning'] == 'Invalid payload. Check your payload once again'


# # TODO need to enable once we will enable strict_check_words in fetch_nodes
# @patch("src.utils.requests.post", return_value=graph_resp)
# def test_fetch_nodes_with_error(_mock1):
#     """Test fetch node method status."""
#     resp = fetch_nodes(payload={"gremlin": "g.V().has('foo','bar').drop()')"})
#     assert resp['error'] is not None


@patch("src.utils.requests.post", return_value=mocked_response())
def test_fetch_nodes_data_not_none(_mock1):
    """Test fetch node method outcome."""
    query = "g.V().has('name','foo').valueMap();"
    resp = fetch_nodes(payload={'gremlin': query})
    assert resp is not None
