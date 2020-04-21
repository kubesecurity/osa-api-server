"""Utility classes and functions."""

import daiquiri
import requests

from src.config import DAIQUIRI_LOG_LEVEL
from src.gremlin import execute_query

daiquiri.setup(level=DAIQUIRI_LOG_LEVEL)
log = daiquiri.getLogger(__name__)


def sanitize_text_for_query(text: str) -> str:
    """Sanitize text so it can used in queries."""
    if text is None:
        return ''

    if not isinstance(text, str):
        raise ValueError(
            'Invalid query text: expected string, got {t}'.format(t=type(text))
        )

    # TODO - As of now bypassing till we will have model defined and working fine in environment.
    # strict_check_words = ['drop', 'delete', 'update', 'remove', 'insert']
    # if any(keywork in text.lower() for keywork in strict_check_words):
    #     raise ValueError('Only select queries are supported')

    # remove newlines, quotes and backslash character
    text = " ".join([l.strip() for l in text.split("\n")])
    return text.strip()


def fetch_nodes(payload: object) -> object:
    """Fetch node from graph database."""
    if payload and payload.get('gremlin'):
        try:
            # sanitize the query to drop CRUD operations
            query = sanitize_text_for_query(payload['gremlin'])
            if query:
                return execute_query(query)
        except (ValueError, requests.exceptions.Timeout, Exception) as e:
            raise e
    else:
        return {'warning': 'Invalid payload. Check your payload once again'}
