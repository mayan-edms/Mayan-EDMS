from __future__ import unicode_literals

from django.conf.urls import include, patterns, url
from django.conf import settings
from django.utils.module_loading import import_string

from rest_framework.reverse import reverse


class APIEndPoint(object):
    _registry = {}

    @classmethod
    def get_all(cls):
        return cls._registry.values()

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    def __unicode__(self):
        return unicode(self.app.name)

    def __init__(self, app, version_string, name=None):
        self.app = app
        self.endpoints = []
        self.name = name
        self.version_string = version_string
        try:
            api_urls = import_string(
                '{0}.urls.api_urls'.format(app.name)
            )
        except Exception:
            if settings.DEBUG:
                raise
            else:
                # Ignore import time errors
                pass
        else:
            self.register_urls(api_urls)

        self.__class__._registry[app.name] = self

    def get_absolute_url(self):
        return reverse('rest_api:api-version-1-app', args=(self.app.name,))

    @property
    def app_name(self):
        return self.app.name

    def register_urls(self, urlpatterns):
        from .urls import version_1_urlpatterns
        endpoint_urls = patterns(
            '',
            url(r'^%s/' % self.app.name, include(urlpatterns)),
        )
        version_1_urlpatterns += endpoint_urls


class APIVersion(object):
    def __init__(self):
        self.version_string = '1'
        self.url = reverse('rest_api:api-version-1')
