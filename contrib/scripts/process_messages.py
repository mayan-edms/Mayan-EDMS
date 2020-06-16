#!/usr/bin/env python

import os
import optparse
import sys

import sh

import django
from django.apps import apps

makemessages = sh.Command('./manage.py')
makemessages = makemessages.bake('makemessages')

compilemessages = sh.Command('./manage.py')
compilemessages = compilemessages.bake('compilemessages')

transifex_client = sh.Command('tx')
pull_translations = transifex_client.bake('pull')
push_translations = transifex_client.bake('push')

sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(1, os.path.abspath('.'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mayan.settings')
django.setup()

from mayan.apps.common.apps import MayanAppConfig
from mayan.settings import BASE_DIR, LANGUAGES


def process(command, app_list, language_list):
    if command == makemessages:
        print('Making messages')
    elif command == compilemessages:
        print('Compiling messages')
    elif command == pull_translations:
        print('Pulling translation files')
    elif command == push_translations:
        print('Pushing translation files')

    if command in [compilemessages, makemessages]:
        command_argument_locales = []
        for language in language_list:
            command_argument_locales.append('--locale')
            command_argument_locales.append(language)

        for app in app_list:
            print('Processing app: %s...' % app)
            app_path = os.path.join(BASE_DIR, 'apps', app)
            os.chdir(app_path)

            print('Doing languages: {}'.format(', '.join(language_list)))
            command(*command_argument_locales)
    elif command == pull_translations:
        for lang in language_list:
            print('Doing language: %s' % lang)
            command('-f', '-l', lang)
    elif command == push_translations:
        for lang in language_list:
            print('Doing language: %s' % lang)
            command('-s', '-l', lang)


if __name__ == '__main__':
    APP_LIST = sorted(
        [
            name for name, app_config in apps.app_configs.items() if issubclass(type(app_config), MayanAppConfig)
        ]
    )

    LANGUAGE_MAPPING = {
        'de': 'de_DE',
        'ro': 'ro_RO',
        'tr': 'tr_TR',
        'zh-hans': 'zh_Hans',
    }
    LANGUAGE_LIST = []

    for language in dict(LANGUAGES).keys():
        language = LANGUAGE_MAPPING.get(language, language)
        if '-' in language:
            elements = language.split('-')
            language = '{}_{}' .format(elements[0], elements[1].upper())

        LANGUAGE_LIST.append(language)

    parser = optparse.OptionParser()
    parser.add_option(
        '-m', '--make', help='create message sources file', dest='make',
        default=False, action='store_true'
    )
    parser.add_option(
        '-c', '--compile', help='compile message files', dest='compile',
        default=False, action='store_true'
    )
    parser.add_option(
        '-p', '--pull', help='pull translation files', dest='pull',
        default=False, action='store_true'
    )
    parser.add_option(
        '-u', '--push', help='push translation files', dest='push',
        default=False, action='store_true'
    )
    parser.add_option(
        '-a', '--app', help='specify which app to process', dest='app',
        action='store', metavar='appname'
    )
    parser.add_option(
        '-l', '--lang', help='specify which language to process', dest='lang',
        action='store', metavar='language'
    )
    (opts, args) = parser.parse_args()

    if not opts.make and not opts.compile:
        parser.print_help()

    if opts.app:
        app_list = [opts.app]
    else:
        app_list = APP_LIST

    if opts.lang:
        language_list = [opts.lang]
    else:
        language_list = LANGUAGE_LIST

    if opts.make:
        process(makemessages, app_list, language_list)
    elif opts.compile:
        process(compilemessages, app_list, language_list)
    elif opts.pull:
        process(pull_translations, app_list, language_list)
    elif opts.push:
        process(push_translations, app_list, language_list)
