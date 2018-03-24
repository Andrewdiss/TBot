import requests
import logging

log = logging.getLogger('bot_report')


class HandleBot(object):
    def __init__(self, config):
        self.config = config
        self.API_token = self.config.get('TelegramBotReg', 'api_token')
        self.url = "https://api.telegram.org/bot{0}/".format(self.API_token)

    def start_processing(self):
        try:
            udpades_json = self.get_updates_json()
            log.info('bot response is OK')
        except Exception as e:
            log.error("can`t get Updates")

        chat_id = self.get_chaT_id(self.last_update(udpades_json))
        self.send_message(chat_id, 'Zdarova eblan')

        return chat_id

    def get_updates_json(self):
        response_bot = requests.get(self.url + "getUpdates")
        return response_bot.json()

    @staticmethod
    def last_update(data):
        results = data['result']
        total_updates = len(results) - 1
        return results[total_updates]

    @staticmethod
    def get_chaT_id(update):
        chat_id = update['message']['chat']['id']
        return chat_id

    def send_message(self, chat, text):
        params = {'chat_id': chat, 'text': text}
        response = requests.post(self.url + 'sendMessage', data=params)
        return response

