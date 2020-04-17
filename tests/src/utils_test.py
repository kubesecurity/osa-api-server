"""Tests to cover utils code."""

from unittest.mock import patch

from src.utils import GraphPassThrough

gpt = GraphPassThrough()

graph_resp = {
    "requestId": "5cc29849-8e9b-4b66-90d0-f2569dc962b9",
    "status": {
        "message": "",
        "code": 200,
        "attributes": {}
    },
    "result": {
        "data": [],
        "meta": {}
    }
}


@patch("src.utils.requests.post", return_value=graph_resp)
def test_fetch_nodes(_mock1):
    """Test the GraphPassThrough fetch nodes module."""
    resp = gpt.fetch_nodes(data={})
    assert resp['warning'] == 'Invalid payload. Check your payload once again'
    resp = gpt.fetch_nodes(data={"query": "g.V().has('foo','bar').drop()')"})
    assert resp['error'] is not None
    query = "g.V().has('name','foo').valueMap();"
    resp = gpt.fetch_nodes(data={'query': query})
    assert resp is not None
