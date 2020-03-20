"""Helper functions to sanitize/unsanitize str, List[str]."""

# (fixme) remove once we move to gremlin driver

from typing import Union, List
from urllib.parse import quote, unquote


def sanitize(string: Union[str, List[str]]) -> str:
    """Sanitizes the input string."""
    if isinstance(string, str):
        return quote(string)
    if isinstance(string, list):
        # sanitize
        string = map(lambda x: "'{}'".format(quote(x)), string)
        # convert as string
        return ', '.join(string)
    raise Exception('Unexpected type {}'.format(type(string)))


def unsanitize(string: str) -> str:
    """Unsanitizies the input string."""
    return unquote(string)
