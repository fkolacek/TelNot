#
# Author: Frantisek Kolacek <work@kolacek.it
# Version: 1.0
#

import logging

from flask import Flask, request, make_response
import telegram

from .config import TelNotConfig
from .exception import TelNotException


class TelNot:

    config = None
    bots = {}

    def __init__(self, config_name='config.ini'):
        try:
            self.config = TelNotConfig(config_name)

            self.init_logging()
            self.init_bots()

            self.app = Flask((__name__.split('.')[0]))

            self.app.add_url_rule('/', 'process_index', self.process_index)
            self.app.add_url_rule('/notify', 'process_notify', self.process_notify, methods=['GET', 'POST'])

        except TelNotException:
            raise

    def init_logging(self):
        level = logging.DEBUG if self.config['main']['debug'] else logging.INFO

        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=level)

    def init_bots(self):
        logging.info('Loading bots')
        self.bots = {}

        try:
            for bot in self.config['bots']:
                logging.info('Loading bot: {}'.format(bot['name']))
                self.bots[bot['name']] = telegram.Bot(token=bot['token'])
        except telegram.error.InvalidToken:
            raise TelNotException('Invalid token for bot "{}"'.format(bot['name'])) from None

    def process_index(self):
        logging.info('Processing: index')
        return make_response('There is nothing, go away!', 200)

    def process_notify(self):
        logging.info('Processing: notify')
        if request.method == 'GET':
            return make_response('There is nothing, go away!', 200)

        bot_name = request.form.get('bot')
        token = request.form.get('token')
        message = request.form.get('message')

        if not all([bot_name, token, message]):
            return make_response('Invalid request', 400)

        # Check if token is valid
        users = [user for user in self.config['users'] if user['token'] == token]

        if not users:
            return make_response('Unauthorized', 403)

        user = users[0]

        # Check if bot exists
        bots = [b for b in self.config['bots'] if b['name'] == bot_name]

        if not bots:
            return make_response('Not found', 404)

        # Check if user can use particular bot
        if bot_name not in user['bots']:
            return make_response('Unauthorized', 403)

        self.send_message(bots[0], message)

        return make_response('Success', 200)

    def send_message(self, bot, message):
        logging.info('Sending message [{}] {}'.format(bot['name'], message))
        b = self.bots[bot['name']]
        b.send_message(chat_id=bot['chatid'], text=message)

    def run(self):
        logging.info('Starting application')
        self.app.run(**self.config['main'])

