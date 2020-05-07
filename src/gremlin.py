"""Abstracts access to gremlin server through REST calls."""

import json
import requests
import daiquiri
from gremlin_python.structure.io import graphsonV3d0
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from src.config import (GREMLIN_DEFAULT_HOST, GREMLIN_DEFAULT_PORT, GREMLIN_SCHEME,
                        DAIQUIRI_LOG_LEVEL)

# from src.utils import get_session_retry

daiquiri.setup(level=DAIQUIRI_LOG_LEVEL)
log = daiquiri.getLogger(__name__)  # pylint: disable=invalid-name

_READER = graphsonV3d0.GraphSONReader()
_GREMLIN_URL = '{scheme}://{host}:{port}'.format(scheme=GREMLIN_SCHEME,
                                                 host=GREMLIN_DEFAULT_HOST,
                                                 port=GREMLIN_DEFAULT_PORT)


def test_connection() -> bool:
    """Test connection to gremlin server."""
    response = requests.get(_GREMLIN_URL)
    # Everything except "not found" is acceptable.
    return response.status_code != 404


def execute_query(query):
    """Post given Traversel to gremlin server."""
    response = get_session_retry().post(_GREMLIN_URL,
                                        data=json.dumps({"gremlin": str(query)}))
    log.info('Gremin Query:"{}", status_code:{}'.format(query,
                                                        response.status_code))
    response.raise_for_status()
    return _READER.toObject(response.json())


def get_session_retry(retries=3, backoff_factor=0.5, status_forcelist=(404, 500, 502, 504),
                      session=None):
    """Set HTTP Adapter with retries to session."""
    session = session or requests.Session()
    retry = Retry(total=retries, read=retries, connect=retries,
                  backoff_factor=backoff_factor, status_forcelist=status_forcelist)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    return session
