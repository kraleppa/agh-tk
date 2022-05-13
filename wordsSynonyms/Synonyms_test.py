import pytest

import Synonyms_functions

@pytest.fixture
def run_test():
    pol = ['ą', 'ę', 'ó', 'ź', 'ł', 'ń', 'ś']
    result = Synonyms_functions.find_synonyms(words=['kot'])
    for word in result:
        for pl in pol:
            if pl in word:
                result.remove(word)
    result = list(dict.fromkeys(result))

    return result

def test(run_test):

    expected = ['kot', 'mruczek', 'dachowiec']
    assert run_test == expected




