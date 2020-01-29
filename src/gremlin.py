"""Abstracts access to gremlin server through REST calls"""

from gremlin_python.structure.io import graphsonV3d0

from gremlin_connect.gremlin_adapter import GremlinAdapter
from src.config import GREMLIN_DEFAULT_HOST, GREMLIN_DEFAULT_PORT

_GREMLIN = GremlinAdapter(GREMLIN_DEFAULT_HOST, int(GREMLIN_DEFAULT_PORT))
_READER = graphsonV3d0.GraphSONReader()

def execute_query(query):
    """Posts given Traversel to gremlin server"""
    response = _GREMLIN.execute_query(str(query))
    return _READER.toObject(response)
