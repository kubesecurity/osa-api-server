"""Config as env variable."""
import os

GREMLIN_DEFAULT_HOST = os.environ.get('GREMLIN_DEFAULT_HOST', 'localhost')
GREMLIN_DEFAULT_PORT = os.environ.get('GREMLIN_DEFAULT_PORT', 8182)
GREMLIN_SCHEME = os.environ.get('GREMLIN_SCHEME', 'http')
DAIQUIRI_LOG_LEVEL = os.environ.get('DAIQUIRI_LOG_LEVEL', 'INFO').upper()

GREMLIN_URL = '{scheme}://{host}:{port}'.format(scheme=GREMLIN_SCHEME, host=GREMLIN_DEFAULT_HOST,
                                                port=GREMLIN_DEFAULT_PORT)

SECURE_DEPLOYMENT = os.environ.get('SECURE_DEPLOYMENT', 'true').lower() == "true"
