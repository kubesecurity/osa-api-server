from src.parse_datetime import *

_TIMESTAMP = 0
_STR = '1970-01-01 00:00:00+00:00'

def test_from_date_str() -> int:
    assert from_date_str(_STR) == _TIMESTAMP

def test_to_date_str() -> str:
    assert to_date_str(_TIMESTAMP) == _STR

def test_to_date_str_with_empty_string_as_input() -> str:
    assert to_date_str('') == ''

def test_to_date_str_with_string_as_input() -> str:
    assert to_date_str('abcd') == ''

def test_to_date_str_with_string_num_as_input() -> str:
    assert to_date_str('{}'.format(_TIMESTAMP)) == _STR
