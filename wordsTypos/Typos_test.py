import pytest

import Typos_functions

@pytest.fixture
def run_test():
    pol = ['ą', 'ę', 'ó', 'ź', 'ł', 'ń', 'ś']
    result = Typos_functions.create_typos_list(words=['wir'])
    for word in result:
        for pl in pol:
            if pl in word:
                word = word.replace(pl,'x')
    result = list(dict.fromkeys(result))

    return result

def test(run_test):

    expected = ['wir', 'sir', 'wiv', 'cir', 'wlr', 'wmr']
    assert len(run_test) == len(expected)
