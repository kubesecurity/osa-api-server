import os

from gremlin_python.structure.io import graphsonV3d0

from gremlin_connect.gremlin_adapter import GremlinAdapter
from src.config import GREMLIN_DEFAULT_HOST, GREMLIN_DEFAULT_PORT

_GREMLIN = GremlinAdapter(GREMLIN_DEFAULT_HOST, int(GREMLIN_DEFAULT_PORT))
_reader = graphsonV3d0.GraphSONReader()

def execute_query(query):
    response = _GREMLIN.execute_query(str(query))
    return _reader.toObject(response)

