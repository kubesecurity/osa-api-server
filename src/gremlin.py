import os
from gremlin_connect.gremlin_adapter import GremlinAdapter

_GREMLIN_DEFAULT_HOST = os.environ.get('GREMLIN_DEFAULT_HOST', 'localhost')
_GREMLIN_DEFAULT_PORT = os.environ.get('GREMLIN_DEFAULT_PORT', 8182)

GREMLIN = GremlinAdapter(_GREMLIN_DEFAULT_HOST, int(_GREMLIN_DEFAULT_PORT))

