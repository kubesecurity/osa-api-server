"""To test sanitizer"""

import pytest

from src.sanitizer import sanitize, unsanitize

# pylint: disable=missing-function-docstring
def test_string_sanitization_with_empty():
    assert sanitize('') == ''

def test_string_sanitization_with_none():
    with pytest.raises(Exception) as exception:
        sanitize(None)
    assert "Unexpected type" in str(exception.value)

def test_string_sanitization_with_normal_chars():
    assert sanitize('foo') == 'foo'

def test_string_sanitization_with_special_chars():
    assert sanitize('foo)"bar') == 'foo%29%22bar'

def test_string_sanitization_with_empty_list():
    assert sanitize([]) == ''

def test_string_sanitization_with_none_list():
    with pytest.raises(Exception):
        sanitize([None])

def test_string_sanitization_with_a_list():
    assert sanitize(['a', 'b']) == "'a', 'b'"

def test_string_sanitization_with_special_char_list():
    assert sanitize(['foo)"bar', 'b']) == "'foo%29%22bar', 'b'"

def test_string_sanitization_with_special_char_list_1():
    assert sanitize(['foo)"bar', 'b b']) == "'foo%29%22bar', 'b%20b'"

def test_string_unsanitization_with_none():
    with pytest.raises(Exception):
        assert unsanitize(None) == ''

def test_string_unsanitization_with_empty():
    assert unsanitize('') == ''

def test_string_unsanitization_with_normal_chars():
    assert unsanitize('foo') == 'foo'

def test_string_unsanitization_with_special_chars():
    assert unsanitize('foo%29%22bar') == 'foo)"bar'
