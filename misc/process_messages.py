#!/usr/bin/env python
import sys
import os
import optparse

import pbs

APP_LIST = ('common', 'converter', 'documents', 'document_comments',
    'document_indexing', 'dynamic_search', 'folders', 'history',
    'linking', 'main', 'metadata', 'navigation', 'ocr', 'permissions',
    'project_setup', 'project_tools', 'smart_settings', 'sources',
    'tags', 'user_management', 'web_theme', 'django_gpg', 'document_signatures',
    'acls', 'installation', 'scheduler', 'bootstrap')
LANGUAGE_LIST = ('en', 'pt', 'pt_BR', 'ru', 'es', 'it', 'pl', 'de_DE')

makemessages = pbs.Command('django-admin.py')
makemessages = makemessages.bake('makemessages')

compilemessages = pbs.Command('django-admin.py')
compilemessages = compilemessages.bake('compilemessages')

if hasattr(sys, 'real_prefix'):
    # We are inside a virtual env
    BASE_DIR = os.path.join(os.environ['VIRTUAL_ENV'], 'mayan')
else:
    BASE_DIR = os.getcwd()


def process_all(command):
    if command == makemessages:
        print 'Making messages'
    elif command == compilemessages:
        print 'Compiling messages'

    for app in APP_LIST:
        print 'Processing app: %s...' % app
        app_path = os.path.join(BASE_DIR, 'apps', app)
        os.chdir(app_path)
        for lang in LANGUAGE_LIST:
            print 'Doing language: %s' % lang
            command(locale=lang)


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-m', '--make', help='create message sources file', dest='make', default=False, action='store_true')
    parser.add_option('-c', '--compile', help='compile message files', dest='compile', default=False, action='store_true')
    (opts, args) = parser.parse_args()
    
    if not opts.make and not opts.compile:
        parser.print_help()

    if opts.make:
        process_all(makemessages)
    elif opts.compile:
        process_all(compilemessages)
