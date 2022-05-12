import sys
import os

if __name__ == "__main__":

    dir = os.path.dirname(os.getcwd())
    sys.path.insert(1, dir)

    from wordsServices_textExtractor_config import run_config
    import Forms_functions

    log_name = "wordsForms"
    exchange = 'words'
    host = 'rabbitmq'
    queue = 'words.forms'
    function = Forms_functions.forms_generator

    run_config.run_app(log_name, exchange, host, queue, function)