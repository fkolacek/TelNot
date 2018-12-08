#
# Author: Frantisek Kolacek <work@kolacek.it
# Version: 1.0
#

import configparser

from .exception import TelNotConfigException


class TelNotConfig:

    config = {
        'main': {
            'debug': False,
            'host': '127.0.0.1',
            'port': 5000,
        },
        'bots': [],
        'users': [],
    }

    def __init__(self, config_name):
        conf = configparser.ConfigParser()

        try:
            conf.read(config_name)
        except configparser.Error:
            raise TelNotConfigException('Unable to parse config "{}"'.format(config_name)) from None

        for section in conf.sections():
            if section == 'main':
                self._parse_main(conf, section)
            elif section.startswith('bot_'):
                self._parse_bot(conf, section)
            elif section.startswith('user_'):
                self._parse_user(conf, section)
            else:
                raise TelNotConfigException('Invalid section in config file: "{}"'.format(section))

    def _parse_main(self, conf, section):
        for key in conf[section]:
            if key == 'debug':
                self.config[section][key] = conf[section][key].lower() == 'true'
            elif key == 'host':
                self.config[section][key] = conf[section][key]
            elif key == 'port':
                self.config[section][key] = int(conf[section][key])
            else:
                raise TelNotConfigException('Found invalid key "{}" in "{}" section'.format(key, section))

    def _parse_bot(self, conf, section):
        bot_name = section.replace('bot_', '')

        bot = {
            'name': bot_name,
            'chatid': None,
            'token': None,
        }

        for key in conf[section]:
            if key == 'chatid':
                bot[key] = int(conf[section][key])
            elif key == 'token':
                bot[key] = conf[section][key]
            else:
                raise TelNotConfigException('Found invalid key "{}" in "{}" section'.format(key, section))

        if not bot['chatid'] or not bot['token']:
            raise TelNotConfigException('Bot "{}" configuration is not complete - either chatid or token is missing')

        self.config['bots'].append(bot)

    def _parse_user(self, conf, section):
        user_name = section.replace('user_', '')

        user = {
            'name': user_name,
            'token': None,
            'bots': [],
        }

        for key in conf[section]:
            if key == 'token':
                user[key] = conf[section][key]
            elif key == 'bots':
                user[key] = conf[section][key].split(',')
            else:
                raise TelNotConfigException('Found invalid key {} in {} section'.format(key, section))

        if not user['token']:
            raise TelNotConfigException('User "{}" configuration is not complete - token is missing')

        self.config['users'].append(user)

    def __getitem__(self, name):
        return self.config.get(name)
