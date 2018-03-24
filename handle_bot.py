import requests
import logging

log = logging.getLogger('bot_report')


class HandleBot(object):
    def __init__(self, config):
        self.config = config
        self.API_token = self.config.get('TelegramBotReg', 'api_token')
        self.url = "https://api.telegram.org/bot{0}/".format(self.API_token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        response_bot = requests.get(self.url + method, data=params)
        result_json = response_bot.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        method = 'sendMessage'
        params = {'chat_id': chat_id, 'text': text}
        response = requests.post(self.url + method, data=params)
        return response

    def last_update(self):
        get_result = self.get_updates()
        if len(get_result) > 0:
            last_upd = get_result[-1]
        else:
            last_upd = get_result[len(get_result)]
        return last_upd
