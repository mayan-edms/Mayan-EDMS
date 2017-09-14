from __future__ import unicode_literals

import os

from django.core import management
from django.core.wsgi import get_wsgi_application

import tornado.httpserver
import tornado.ioloop
from tornado.process import Subprocess
import tornado.web
import tornado.wsgi

DEFAULT_PORT = 8080


class Command(management.BaseCommand):
    help = 'Launches a local Tornado server.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--single-process',
            action='store_true',
            dest='single-process',
            default=False,
            help='Forces only one server process.'
        )

        parser.add_argument(
            '--port',
            action='store',
            dest='port',
            default=DEFAULT_PORT,
            help='Port on which to bind the server.'
        )

    def handle(self, *args, **options):
        wsgi_application = get_wsgi_application()
        wsgi_container = tornado.wsgi.WSGIContainer(wsgi_application)

        tornado_application = tornado.web.Application(
            handlers=(
                (
                    r'/static/(.*)', tornado.web.StaticFileHandler,
                    {'path': 'mayan/media/static'},
                ),
                (
                    '.*', tornado.web.FallbackHandler,
                    dict(fallback=wsgi_container)
                ),
            )
        )

        http_server = tornado.httpserver.HTTPServer(tornado_application)

        try:
            if options['single-process']:
                http_server.listen(options['port'])
                ioloop = tornado.ioloop.IOLoop.instance()
                Subprocess(['./manage.py', 'celery', 'worker', '-O', 'fair'])
                ioloop.start()
            else:
                http_server.bind(options['port'])
                http_server.start(0)  # forks one process per cpu
                ioloop = tornado.ioloop.IOLoop.current()
                Subprocess(['./manage.py', 'celery', 'worker', '-O', 'fair'])
                ioloop.start()
        except KeyboardInterrupt:
            tornado.ioloop.IOLoop.instance().stop()
