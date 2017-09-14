#!/usr/bin/env python
from __future__ import unicode_literals

import os
import subprocess

from django.core.wsgi import get_wsgi_application

import sh

import tornado.httpserver
import tornado.ioloop
from tornado.process import Subprocess
import tornado.web
import tornado.wsgi

DEFAULT_PORT = 8080

command_manage = sh.Command('./manage.py')

"""
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
"""

from multiprocessing import Value

from tornado import gen
from tornado.ioloop import IOLoop
from tornado.locks import Lock, Semaphore

from tornado.queues import LifoQueue, QueueEmpty

lifo = LifoQueue()
lock = Lock()

workers = [
    {
        'name': 'fast',
        'queues': 'converter',
        'concurrency': None,
    },
    {
        'name': 'medium',
        'queues': 'checkouts_periodic,documents_periodic,indexing,metadata,sources,sources_periodic,uploads,documents',
        'concurrency': None,
    },
    {
        'name': 'slow',
        'queues': 'mailing,parsing,ocr,tools,statistics',
        'concurrency': '1',
        'nice': '19',
    },
]

#for worker in workers:
#    worker_semaphore = Semaphore(1)

#worker_instances = {}

processes = []


#@gen.coroutine
def launch_celery_workers():

    for worker in workers:
        args = []

        args.extend(['celery', 'worker', '-O', 'fair', '-l', 'INFO'])

        args.extend(['-n', 'mayan-worker-{}.%%h'.format(worker['name'])])

        if 'queues' in worker:
            args.extend(['-Q', worker['queues']])

        if worker.get('concurrency'):
            args.extend(['--concurrency', worker.get('concurrency')])

        print 'arguments: ', args

        #with (yield lock.acquire()):
            #try:
            #    worker_instances = lifo.get_nowait()
            #except QueueEmpty:
            #    worker_instances = {}

        #print 'worker_instances', worker_instances

        #worker_instances.setdefault(worker['name'], 0)
        #worker_instances[worker['name']] += 1

        #lifo.put(worker_instances)

        #print worker_instances[worker['name']]

        #processes.append(command_nice('-n', worker.get('nice', 0), command_manage(args, _bg=True)))
        processes.append(command_manage(args, _bg=True))
        #processes.append(
        #    subprocess.Popen(
        #        args, close_fds=True, stderr=subprocess.PIPE,
        #        stdout=subprocess.PIPE
        #    )
        #)

        #Subprocess(args)#, io_loop=global_ioloop)


class MayanTornado(object):
    #@gen.coroutine
    def start(self):
        print 'a'
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mayan.settings.production')
        print '2'
        option_port = DEFAULT_PORT
        #option_single_process = False
        option_fork = 3

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
            if option_fork == 1:
                http_server.listen(option_port)
                #ioloop = tornado.ioloop.IOLoop.instance()
                ioloop = tornado.ioloop.IOLoop.current()

                launch_workers()

                ioloop.start()
            elif option_fork == 2:
                http_server.bind(option_port)
                http_server.start(0)  # forks one process per cpu
                #global_ioloop = tornado.ioloop.IOLoop.instance()
                #ioloop = tornado.ioloop.IOLoop.current()

                launch_workers()

                #Subprocess(['./manage.py', 'celery', 'worker', '-O', 'fair', '-l', 'INFO'])
                #ioloop.start()
                #global_ioloop.start()
                tornado.ioloop.IOLoop.current().start()
            else:
                launch_celery_workers()
                sockets = tornado.netutil.bind_sockets(option_port)
                tornado.process.fork_processes(0)

                #print tornado.ioloop.IOLoop.instance()

                #server = HTTPServer(app)
                #server.add_sockets(sockets)
                http_server.add_sockets(sockets)
                tornado.ioloop.IOLoop.current().start()

        except KeyboardInterrupt:
            tornado.ioloop.IOLoop.instance().stop()
            for process in processes:
                try:
                    process.process.kill_group()
                except TypeError:
                    pass


if __name__ == '__main__':
    app = MayanTornado()
    app.start()
