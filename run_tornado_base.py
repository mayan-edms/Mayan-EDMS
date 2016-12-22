import django.core.handlers.wsgi
import os
import tornado.httpserver
import tornado.ioloop
import tornado.wsgi

def main():
    os.environ["DJANGO_SETTINGS_MODULE"] = 'mayan.settings'
    application = django.core.handlers.wsgi.WSGIHandler()
    container = tornado.wsgi.WSGIContainer(application)
    http_server = tornado.httpserver.HTTPServer(container)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main() 
