import configparser
import os
import sys
import logging
from datetime import datetime
from firstBot.handle_bot import HandleBot

greetings = ('hello', 'hi', 'good day to you!', 'привет', "ку")
now = datetime.now()


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

    # bot declaration
    bot_handler = HandleBot(conf)
    new_offset = None
    today = now.day
    while True:
        bot_handler.get_updates(new_offset)
        last_update = bot_handler.last_update()

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']

        if last_chat_text.lower() in greetings and today == now.day:
            bot_handler.send_message(last_chat_id, "Здарова! {}".format(last_chat_name))
            today += 1

        elif last_chat_text.lower() in greetings and today == now.day+1:
            word_list = ["...", "уже здоровались вроде",
                         "Ох епта. Ну добрый день {}!".format(last_chat_name), "Так, хуль те нада?"]
            for word in word_list:
                bot_handler.send_message(last_chat_id, "{}".format(word))
                continue
            today += 1
        new_offset = last_update_id + 1


if __name__ == "__main__":
    bot = init_bot()
    try:
        init_bot()
    except KeyboardInterrupt:
        exit()
