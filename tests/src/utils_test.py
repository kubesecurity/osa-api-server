"""Tests to cover utils code."""

from unittest.mock import patch

from src.utils import fetch_nodes, get_cves_from_text


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


@patch("src.utils.requests.Session.post", return_value=mocked_response())
def test_fetch_nodes_invalid_payload(_mock1):
    """Test fetch node method with invalid poayload."""
    resp = fetch_nodes(payload={})
    assert resp['warning'] == 'Invalid payload. Check your payload once again'


# # TODO need to enable once we will enable strict_check_words in fetch_nodes
# @patch("src.utils.requests.Session.post", return_value=graph_resp)
# def test_fetch_nodes_with_error(_mock1):
#     """Test fetch node method status."""
#     resp = fetch_nodes(payload={"gremlin": "g.V().has('foo','bar').drop()')"})
#     assert resp['error'] is not None


@patch("src.utils.requests.Session.post", return_value=mocked_response())
def test_fetch_nodes_data_not_none(_mock1):
    """Test fetch node method outcome."""
    query = "g.V().has('name','foo').valueMap();"
    resp = fetch_nodes(payload={'gremlin': query})
    assert resp is not None


def test_get_cves_from_text():
    """Test the retriving CVE logic."""
    text = """
            -----Valid CVEs-----
            CVE-2014-0001
            CVE-2014-0999
            CVE-2014-10000
            CVE-2014-100000
            CVE-2014-1000000
            CVE-2014-100000000
            CVE-2019-111111111
            CVE-2019-456132
            CVE-2019-54321
            CVE-2020-65537
            CVE-2020-7654321
            cve-1234-1234 - This is a valid CVE as we are converting text to uppercase for retriving CVEs
            -----Invalid CVEs Text-----
            CVE-0a34-9823
            CVE-2019-998a
            CVE-2020
            CVE-123-1234
            """
    cves = get_cves_from_text(text)
    assert len(cves) == 12


def test_get_cves_with_duplicate_data():
    """Test the duplicate logic."""
    text = "CVE-2019-0001 and CVE-2019-0001"
    cves = get_cves_from_text(text)
    assert len(cves) == 1
    assert 'CVE-2019-0001' in cves


def test_get_cves_with_extra_text():
    """Test logic with extra text as prefix and suffix."""
    text = """ Test CVE aCVE-2019-2341andCVE-2019-3546b CVE-2019- VE-2019-1234"""
    cves = get_cves_from_text(text)
    assert len(cves) == 2
    assert 'CVE-2019-2341' in cves
    assert 'CVE-2019-3546' in cves
