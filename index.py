import configparser
import os
import sys
import logging
from datetime import datetime
from firstBot.handle_bot import HandleBot


def init_bot():
    conf = configparser.ConfigParser()
    try:
        conf.read(sys.argv[1])
    except NameError:
        print('Unable to read configuration!')

    """ Configure logging """
    log_file = 'TeleBot_log{0}.log' \
        .format(datetime.now().strftime('_%m.%d-%H.%M.%S'))
    log_file = os.path.join(conf.get('logging', 'path'), log_file)

    log = logging.getLogger('bot_report')
    log.setLevel(logging.INFO)

    bot_handler = HandleBot(conf)

    try:
        debug = conf.get('debug', 'debug')
        if debug.strip().lower() in ['true', '1']:
            log.setLevel(logging.DEBUG)
    except Exception as e:
        pass

    formatter = logging.Formatter('%(asctime)s [%(pathname)s:%(lineno)d] %(levelname)8s: %(message)s')
    log_handler = logging.FileHandler(log_file)
    log_handler.setFormatter(formatter)
    log.addHandler(log_handler)

    return bot_handler


if __name__ == "__main__":
    bot = init_bot()
    bot.start_processing()
