from __future__ import absolute_import

from django.conf.urls import include, patterns, url


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

    def __init__(self, name):
        self.name = name
        self.endpoints = []
        self.__class__._registry[name] = self

    def add_endpoint(self, view_name, description=None):
        self.endpoints.append(
            {
                'description': description,
                'view_name': view_name,
            }
        )

    def register_urls(self, urlpatterns):
        from .urls import version_0_urlpatterns
        endpoint_urls = patterns('',
            url(r'^%s/' % self.name, include(urlpatterns)),
        )

        version_0_urlpatterns += endpoint_urls
