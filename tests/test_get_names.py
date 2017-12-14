# These tests assumes a normal stdlib installation

import pytest

from ultan.get_names import get_names

PATTERNS = ['http', 'uuid']


@pytest.fixture(params=PATTERNS)
def pattern(request):
    return request.param


def test_get_names_only_returns_pattern_matches(pattern):
    names = get_names(pattern)
    for name in names:
        assert pattern in name


def test_gets_all_names_mathing_a_pattern(pattern):
    expected = [name for name in get_names() if pattern in name]
    names = list(get_names(pattern))
    assert expected == names
