import sys
import os

from twisted.application import internet, service
from twisted.web import server, resource, wsgi, static
from twisted.python import threadpool
from twisted.internet import reactor, protocol

#import twresource

PORT = 8000

class ThreadPoolService(service.Service):
    def __init__(self, pool):
        self.pool = pool

    def startService(self):
        service.Service.startService(self)
        self.pool.start()

    def stopService(self):
        service.Service.stopService(self)
        self.pool.stop()

# Environment setup for your Django project files:
sys.path.append("mayan")
os.environ['DJANGO_SETTINGS_MODULE'] = 'mayan.settings'
from django.core.handlers.wsgi import WSGIHandler

# Twisted Application Framework setup:
application = service.Application('twisted-django')


# WSGI container for Django, combine it with twisted.web.Resource:
# XXX this is the only 'ugly' part: see the 'getChild' method in twresource.Root 
# The MultiService allows to start Django and Twisted server as a daemon.

multi = service.MultiService()
pool = threadpool.ThreadPool()
tps = ThreadPoolService(pool)
tps.setServiceParent(multi)
resource = wsgi.WSGIResource(reactor, tps.pool, WSGIHandler())
#root = twresource.Root(resource)

# Servce Django media files off of /media:
mediasrc = static.File(os.path.join(os.path.abspath("."), "mydjangosite/media"))
staticsrc = static.File(os.path.join(os.path.abspath("."), "mydjangosite/static"))
root.putChild("media", mediasrc)
root.putChild("static", staticsrc)

# The cool part! Add in pure Twisted Web Resouce in the mix
# This 'pure twisted' code could be using twisted's XMPP functionality, etc:
#root.putChild("google", twresource.GoogleResource())

# Serve it up:
main_site = server.Site(root)
internet.TCPServer(PORT, main_site).setServiceParent(multi)
multi.setServiceParent(application)
