from __future__ import absolute_import

import os

from django.utils.safestring import mark_safe
from django.conf import settings

from .settings import ICON_SET
from .sets import ICON_THEMES
from .literals import ERROR

SIZE_SMALL = '16x16'
SIZE_BIG = '32x32'


class Icon(object):
    _registry = {}

    def __init__(self, literal, icon_set=None):
        self.literal = literal
        self.icon_set = icon_set
        self.__class__._registry[literal] = self

    def get_file_name(self, size):
        # TODO: Move name + size resolution to sets to support size/name and
        # name_size filename conventions
        try:
            if self.icon_set:
                return '%s/%s/%s' % (ICON_THEMES[self.icon_set].PATH, size, ICON_THEMES[self.icon_set].DICTIONARY[self.literal])
            else:
                return '%s/%s/%s' % (ICON_THEMES[ICON_SET].PATH, size, ICON_THEMES[ICON_SET].DICTIONARY[self.literal])
        except KeyError:
            return '%s/%s/%s' % (ICON_THEMES[ICON_SET].PATH, size, ICON_THEMES[ICON_SET].DICTIONARY[ERROR])
        except AttributeError:
            pass

    def display(self, size): # TODO: move to widgets?
        return mark_safe(u'<img src="%s/icons/%s" />' % (settings.STATIC_URL, self.get_file_name(size)))

    def display_small(self):
        return self.display(SIZE_SMALL)

    def display_big(self):
        return self.display(SIZE_BIG)

    def get_filepath(self):
        if settings.DEVELOPMENT:
            return os.path.join(settings.PROJECT_ROOT, 'apps', 'icons', 'static', 'icons', self.get_file_name(SIZE_BIG))
        else:
            return os.path.join(settings.STATIC_ROOT, self.get_file_name(SIZE_BIG))
