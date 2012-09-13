from __future__ import absolute_import

import os

from django.utils.safestring import mark_safe
from django.conf import settings

from .literals import ERROR, SIZE_SMALL, SIZE_BIG


class Icon(object):
    _registry = {}

    def __init__(self, id, icon_set=None):
        self.id = id
        self.icon_set = icon_set
        self.__class__._registry[id] = self

    def get_url(self, size):
        from .settings import ICON_SET
        return IconSetBase.get_by_name(self.icon_set or ICON_SET).get_url(self, size)

    def display(self, size): # TODO: move to widgets?
        return mark_safe(u'<img src="%s/icons/%s" />' % (settings.STATIC_URL, self.get_url(size)))

    def display_small(self):
        return self.display(SIZE_SMALL)

    def display_big(self):
        return self.display(SIZE_BIG)

    #def get_filepath(self):
    #    if settings.DEVELOPMENT:
    #        return os.path.join(settings.PROJECT_ROOT, 'apps', 'icons', 'static', 'icons', self.get_file_name(SIZE_BIG))
    #    else:
    #        return os.path.join(settings.STATIC_ROOT, self.get_file_name(SIZE_BIG))


class IconSetBase(object):
    _registry = {}
    
    @classmethod
    def get_all(cls):
        return cls._registry.values()
    
    @classmethod
    def get_by_name(cls, name):
        return cls._registry.get(name)

    def __init__(self):
        self.__class__._registry[self.name] = self
    
    def get_filename(self, icon, size):
        return os.path.join([self.path, size, self.dictionary.get(icon.id, ERROR)])
    
    def get_url(self, icon, size):
        return '%s/%s/%s' % (self.path, size, self.dictionary.get(icon.id, ERROR))
    
