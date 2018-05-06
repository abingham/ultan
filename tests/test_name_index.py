# These tests assumes a normal stdlib installation

import pytest
from ultan.name_index import NameIndex
from time import sleep


PATTERNS = ['http', 'uuid']


@pytest.fixture(params=PATTERNS)
def pattern(request):
    return request.param


@pytest.fixture(scope="module")
def name_index():
    index = NameIndex()
    while not index.ready:
        sleep(0.1)
    return index


class TestNameIndex:
    def test_get_names_only_returns_pattern_matches(self, name_index, pattern):
        matches = name_index.get_names(pattern)
        for (name, module_name) in matches:
            assert pattern in name

    def test_gets_all_names_matching_a_pattern(self, name_index, pattern):
        expected = [name for (name, _)
                    in name_index.get_names()
                    if pattern in name]
        names = [name for (name, _) in name_index.get_names(pattern)]
        assert expected == names

    def test_get_names_returns_empty_sequence_when_not_ready(self, pattern):
        index = NameIndex(build_cache=False)
        assert not index.ready
        assert list(index.get_names(pattern)) == []
