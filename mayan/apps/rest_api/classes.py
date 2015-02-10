from __future__ import unicode_literals

from django.conf.urls import include, patterns, url
from django.conf import settings

from common.utils import load_backend


class APIEndPoint(object):
    _registry = {}

    @classmethod
    def get_all(cls):
        return cls._registry.values()

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    def __unicode__(self):
        return unicode(self.name)

    def __init__(self, name, app_name=None):
        self.name = name
        self.endpoints = []
        try:
            api_urls = load_backend('{0}.urls.api_urls'.format(app_name or name))
        except Exception:
            if settings.DEBUG:
                raise
            else:
                # Ignore import time errors
                pass
        else:
            self.register_urls(api_urls)

        self.__class__._registry[name] = self

    def register_urls(self, urlpatterns):
        from .urls import version_0_urlpatterns
        endpoint_urls = patterns('',
            url(r'^%s/' % self.name, include(urlpatterns)),
        )

        version_0_urlpatterns += endpoint_urls
