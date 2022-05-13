import pytest

import Forms_functions

@pytest.fixture
def run_test():
    pol = ['ą', 'ę', 'ó', 'ź', 'ł', 'ń', 'ś']
    result = Forms_functions.forms_generator(words=['kot'])
    for word in result:
        for pl in pol:
            if pl in word:
                result.remove(word)
    result = list(dict.fromkeys(result))

    return result

def test(run_test):

    expected = ['kot', 'kota', 'kotowi', 'kotem', 'kocie', 'kotowie', 'kotom', 'kotami', 'kotach', 'kotu', 'koty']
    assert run_test == expected
