import pytest

import Extractor_callback

@pytest.fixture
def run_test():
    result = Extractor_callback.Callback.extract(file='test.txt')
    return result

def test(run_test):

    expected = 'Testing text extractor.\nLine 1\nLine 2'
    assert run_test == expected