"""Tests list property unroller."""

import pytest

from src.unroll_property import value, unsanitized_value

# pylint: disable=missing-function-docstring
VALUE_TESTDATA = [
        ({}, 'foo', None),
        (None, 'foo', None),
        ('', 'foo', None),
        ({'foo': 1}, 'foo', None),
        ({'foo': [1]}, 'foo', 1),
        ({'foo': ['hello']}, 'foo', 'hello'),
        ({}, 'foo.bar', None),
        (None, 'foo.bar', None),
        ('', 'foo.bar', None),
        ({'foo': {'bar': 1}}, 'foo.bar', None),
        ({'foo': {'bar': [1]}}, 'foo.bar', 1),
        ({'foo': {'bar': ['hello']}}, 'foo.bar', 'hello'),
]
@pytest.mark.parametrize("obj,key,expected", VALUE_TESTDATA)
def test_value(obj, key, expected):
    """Test sanitized value."""
    get = value(key)
    assert expected == get(obj)


UNSANITIZED_VALUE_TESTDATA = [
        ({}, 'foo', None),
        (None, 'foo', None),
        ('', 'foo', None),
        ({'foo': 1}, 'foo', None),
        ({'foo': ['hello%20world']}, 'foo', 'hello world'),
        ({}, 'foo.bar', None),
        (None, 'foo.bar', None),
        ('', 'foo.bar', None),
        ({'foo': {'bar': 1}}, 'foo.bar', None),
        ({'foo': {'bar': ['hello%20world']}}, 'foo.bar', 'hello world'),
]
@pytest.mark.parametrize("obj,key,expected", UNSANITIZED_VALUE_TESTDATA)
def test_unsanitized_value(obj, key, expected):
    """Test unsanitized value."""
    get = unsanitized_value(key)
    assert expected == get(obj)
