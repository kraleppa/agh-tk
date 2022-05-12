import sys
import os

if __name__ == "__main__":

    dir = os.path.dirname(os.getcwd())
    sys.path.insert(1, dir)

    from wordsServices_textExtractor_config import run_config
    import Synonyms_functions

    log_name = "wordsSynonyms"
    exchange = 'words'
    host = 'rabbitmq'
    queue = 'words.synonyms'
    function = Synonyms_functions.find_synonyms

    run_config.run_app(log_name, exchange, host, queue, function)

