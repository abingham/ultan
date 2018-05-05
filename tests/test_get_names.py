# These tests assumes a normal stdlib installation

import pytest
from ultan.name_index import NameIndex


PATTERNS = ['http', 'uuid']


@pytest.fixture(params=PATTERNS)
def pattern(request):
    return request.param


@pytest.fixture(scope="module")
def name_index():
    return NameIndex()


def test_get_names_only_returns_pattern_matches(name_index, pattern):
    names = name_index.get_names(pattern)
    for name in names:
        assert pattern in name


def test_gets_all_names_matching_a_pattern(name_index, pattern):
    expected = [name for name
                in name_index.get_names()
                if pattern in name]
    names = list(name_index.get_names(pattern))
    assert expected == names
