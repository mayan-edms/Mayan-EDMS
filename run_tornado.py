import os
import sys

from django.core.wsgi import get_wsgi_application

import tornado.httpserver
import tornado.ioloop
from tornado.options import options, define, parse_command_line
import tornado.web
import tornado.wsgi

from tornado.process import Subprocess

DEFAULT_PORT = 52723


def main():
    define('port', type=int, default=DEFAULT_PORT)
    define('single-process', type=bool, default=False)

    parse_command_line()

    os.environ['DJANGO_SETTINGS_MODULE'] = 'mayan.settings.production'

    wsgi_application = get_wsgi_application()
    wsgi_container = tornado.wsgi.WSGIContainer(wsgi_application)

    tornado_application = tornado.web.Application(
        handlers=(
            (
                r'/static/(.*)', tornado.web.StaticFileHandler,
                {'path': 'mayan/media/static'},
            ),
            ('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_container)),
        )
    )

    http_server = tornado.httpserver.HTTPServer(tornado_application)

    try:
        if options.single_process:
            http_server.listen(options.port)
            ioloop = tornado.ioloop.IOLoop.instance()
            Subprocess(['./manage.py', 'celery', 'worker'])
            ioloop.start()
        else:
            http_server.bind(options.port)
            http_server.start(0)  # forks one process per cpu
            ioloop = tornado.ioloop.IOLoop.current()
            Subprocess(['./manage.py', 'celery', 'worker'])
            ioloop.start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.instance().stop()


if __name__ == '__main__':
    main()

