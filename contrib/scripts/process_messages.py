#!/usr/bin/env python

import os
import optparse
import sys

import sh

import django
from django.apps import apps
from django.conf import settings

LANGUAGE_MAPPING = {
    'de': 'de_DE',
    'ro': 'ro_RO',
    'tr': 'tr_TR',
    'zh-hans': 'zh_Hans',
}
VERSION = '1.0'


class MessageProcessor:
    @staticmethod
    def get_app_list():
        from mayan.apps.common.apps import MayanAppConfig

        return sorted(
            [
                name for name, app_config in apps.app_configs.items() if issubclass(type(app_config), MayanAppConfig)
            ]
        )

    @staticmethod
    def get_language_list():
        result = []

        for language in dict(settings.LANGUAGES).keys():
            language = LANGUAGE_MAPPING.get(language, language)
            if '-' in language:
                elements = language.split('-')
                language = '{}_{}' .format(elements[0], elements[1].upper())

            result.append(language)

        return result

    def __init__(self):
        sys.path.insert(1, os.path.abspath('.'))
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mayan.settings')

        self.parser = optparse.OptionParser(
            usage='%prog command [options]', version='%prog {}'.format(VERSION)
        )
        self.parser.add_option(
            '-a', '--app', help='specify which app to process', dest='app',
            action='store', metavar='appname'
        )
        self.parser.add_option(
            '-l', '--lang', help='specify which language to process', dest='lang',
            action='store', metavar='language'
        )
        (options, args) = self.parser.parse_args()

        if len(args) != 1:
            self.parser.error('command argument is missing')

        django.setup()

        if options.app:
            self.selected_apps = options.app.split(',')
        else:
            self.selected_apps = MessageProcessor.get_app_list()

        if options.lang:
            self.selected_languages = options.lang.split(',')
        else:
            self.selected_languages = MessageProcessor.get_language_list()

        command_manage = sh.Command('django-admin.py')
        self.command_makemessages = command_manage.bake('makemessages')
        self.command_compilemessages = command_manage.bake('compilemessages')

        command_transifex_client = sh.Command('tx')
        self.command_pull_translations = command_transifex_client.bake('pull')
        self.command_push_translations = command_transifex_client.bake('push')

        self.argument_method_map = {
            'compile': 'do_compilemessages',
            'make': 'do_makemessages',
            'pull': 'do_pull_translations',
            'push': 'do_push_translations'
        }

        self.call_command(command=args[0])

    def call_command(self, command):
        try:
            method = self.argument_method_map[command]
        except KeyError:
            self.parser.error('Unknown command "{}"'.format(command))

        return getattr(self, method)()

    def get_django_language_argument(self):
        command_argument_locales = []
        for language in self.selected_languages:
            command_argument_locales.append('--locale')
            command_argument_locales.append(language)

        return command_argument_locales

    def do_compilemessages(self):
        print('Compiling messages')

        for app in self.selected_apps:
            print('Processing app: %s...' % app)
            app_path = os.path.join(settings.BASE_DIR, 'apps', app)
            os.chdir(app_path)

            print(
                'Doing languages: {}'.format(
                    ', '.join(self.selected_languages)
                )
            )

            environment = os.environ.copy()
            environment.pop('DJANGO_SETTINGS_MODULE')

            self.command_compilemessages(
                _env=environment, *self.get_django_language_argument()
            )

    def do_makemessages(self):
        print('Making messages')

        for app in self.selected_apps:
            print('Processing app: %s...' % app)
            app_path = os.path.join(settings.BASE_DIR, 'apps', app)
            os.chdir(app_path)

            print(
                'Doing languages: {}'.format(
                    ', '.join(self.selected_languages)
                )
            )

            environment = os.environ.copy()
            environment.pop('DJANGO_SETTINGS_MODULE')

            self.command_makemessages(
                _env=environment, *self.get_django_language_argument()
            )

    def do_pull_translations(self):
        print('Pulling translations')

        for app in self.selected_apps:
            print('Processing app: %s...' % app)
            print(
                'Doing languages: {}'.format(
                    ', '.join(self.selected_languages)
                )
            )
            self.command_pull_translations(
                '-f', '-l', ','.join(self.selected_languages)
            )

    def do_push_translations(self):
        print('Push translations')

        for app in self.selected_apps:
            print('Processing app: %s...' % app)
            print(
                'Doing languages: {}'.format(
                    ', '.join(self.selected_languages)
                )
            )
            self.command_push_translations(
                '-s', '-l', ','.join(self.selected_languages)
            )


if __name__ == '__main__':
    message_processor = MessageProcessor()
