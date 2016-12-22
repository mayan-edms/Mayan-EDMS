#/usr/bin/env python

# Run this with
# Original file: https://github.com/bdarnell/django-tornado-demo/blob/master/testsite/tornado_main.py
# PYTHONPATH=. DJANGO_SETTINGS_MODULE=testsite.settings testsite/tornado_main.py
# Serves by default at
# http://localhost:8080/hello-tornado and
# http://localhost:8080/hello-django

from tornado.options import options, define, parse_command_line
import django.core.handlers.wsgi
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
#import daemon
import os, sys


SITE_ROOT = os.path.dirname(os.getcwd()) 
PROJECT_NAME = 'mayan'#os.path.basename(os.getcwd())

sys.path.append( 'mayan' )
os.environ['DJANGO_SETTINGS_MODULE'] = PROJECT_NAME + '.settings'

define('port', type=int, default=8080)

class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello from tornado')

def main():
    tornado.options.parse_command_line()

    wsgi_app = tornado.wsgi.WSGIContainer(
        django.core.handlers.wsgi.WSGIHandler())

    tornado_app = tornado.web.Application(
        [
            ('/hello-tornado', HelloHandler),
            ('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
        ])

    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    #with daemon.DaemonContext():
    main()
