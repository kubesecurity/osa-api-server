"""Helper functions to unroll gremlin list property."""

from src.sanitizer import unsanitize


def value(keys):
    """Nested dictionary keys who's value to be unrolled."""
    def _get(obj) -> str:
        try:
            for key in keys.split('.'):
                obj = obj[key]
            # old versions of gremlin don't have proper way to
            # unroll a list to value who's size is 1.
            return obj[0]
        except (IndexError, TypeError, KeyError):
            pass
        return None
    return _get


def unsanitized_value(keys):
    """Nested dictionary keys who's value to be unrolled and unsanitized."""
    def _get(obj) -> str:
        try:
            return unsanitize(value(keys)(obj))
        except TypeError:
            return None
    return _get
