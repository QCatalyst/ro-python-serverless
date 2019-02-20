import pytest

from handler import hello


def test_hello_200():
    res = hello({}, {})
    assert res.get('statusCode') == 200



