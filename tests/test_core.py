import pytest
from pyamlenium import *

@pytest.mark.parametrize("data, required_keys, option_keys, result", [
    ({"aa": 10, "bb":20}, ["aa", "bb"], None, True),
    ({"aa": 10, "bb":20, "cc": 30}, ["aa", "bb"], None, True),
    ({"aa": 10, "bb":20, "cc": 30}, ["aa", "bb"], ["cc"], True),
    ({"aa": 10, "cc": 30}, [], None, True),
    ({}, [], None, True),
    ({}, [], ["aa"], True),
    ({}, ["aa", "bb"], None, False),
    ({"aa": 10}, ["aa", "bb"], None, False),
    ({"aa": 10}, [], ["bb"], False),
    ({"aa": 10, "cc": 30}, ["aa", "bb"], None, False),
    ({"aa": 10, "cc": 30}, ["aa", "bb"], ["cc"], False),
])
def test_validate_keys(data, required_keys, option_keys, result):
    assert validate_keys(data, required_keys, option_keys) == result

