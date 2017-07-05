from __future__ import unicode_literals

from django.conf.urls import include, url
from django.conf import settings
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.module_loading import import_string

from .exceptions import APIResourcePatternError


class APIResource(object):
    _registry = {}

    @classmethod
    def all(cls):
        return cls._registry.values()

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    def __unicode__(self):
        return unicode(self.name)

    def __init__(self, name, label, description=None):
        self.label = label
        self.name = name
        self.description = description
        self.__class__._registry[self.name] = self


@python_2_unicode_compatible
class APIEndPoint(object):
    _registry = {}
    _patterns = []

    @classmethod
    def get_all(cls):
        return cls._registry.values()

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    def __str__(self):
        return force_text(self.app.name)

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

    @property
    def app_name(self):
        return self.app.name

    def register_urls(self, urlpatterns):
        from .urls import urlpatterns as app_urls

        for url in urlpatterns:
            if url.regex.pattern not in self.__class__._patterns:
                app_urls.append(url)
                self.__class__._patterns.append(url.regex.pattern)
            else:
                raise APIResourcePatternError(
                    'App "{}" tried to register API URL pattern "{}", which '
                    'already exists'.format(self.app.label, url.regex.pattern)
                )
