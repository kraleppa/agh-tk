import sys
import os

if __name__ == "__main__":

    dir = os.path.dirname(os.getcwd())
    sys.path.insert(1, dir)

    from wordsServices_textExtractor_config import run_config
    import Typos_functions

    log_name = "wordsTypos"
    exchange = 'words'
    host = 'rabbitmq'
    queue = 'words.typos'
    function = Typos_functions.create_typos_list

    run_config.run_app(log_name, exchange, host, queue, function)
