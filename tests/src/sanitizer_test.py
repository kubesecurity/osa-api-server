"""To test sanitizer."""

import pytest

from src.sanitizer import sanitize, unsanitize


def test_string_sanitization_with_empty():
    """Test Empty String."""
    assert sanitize('') == ''


def test_string_sanitization_with_none():
    """Test None."""
    with pytest.raises(Exception) as exception:
        sanitize(None)
    assert "Unexpected type" in str(exception.value)


def test_string_sanitization_with_normal_chars():
    """Test normal characters."""
    assert sanitize('foo') == 'foo'


def test_string_sanitization_with_special_chars():
    """Test Special characters."""
    assert sanitize('foo)"bar') == 'foo%29%22bar'


def test_string_sanitization_with_empty_list():
    """Test with Empty list."""
    assert sanitize([]) == ''


def test_string_sanitization_with_none_list():
    """Test with None list."""
    with pytest.raises(Exception):
        sanitize([None])


def test_string_sanitization_with_a_list():
    """Test with normal list."""
    assert sanitize(['a', 'b']) == "'a', 'b'"


def test_string_sanitization_with_special_char_list():
    """Test with special character in list."""
    assert sanitize(['foo)"bar', 'b']) == "'foo%29%22bar', 'b'"


def test_string_sanitization_with_special_char_list_1():
    """Test with special character in list."""
    assert sanitize(['foo)"bar', 'b b']) == "'foo%29%22bar', 'b%20b'"


def test_string_unsanitization_with_none():
    """Test with None."""
    with pytest.raises(Exception):
        assert unsanitize(None) == ''


def test_string_unsanitization_with_empty():
    """Test with empty string."""
    assert unsanitize('') == ''


def test_string_unsanitization_with_normal_chars():
    """Test with normal string."""
    assert unsanitize('foo') == 'foo'


def test_string_unsanitization_with_special_chars():
    """Test with special character."""
    assert unsanitize('foo%29%22bar') == 'foo)"bar'
