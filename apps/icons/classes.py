from __future__ import absolute_import

from django.utils.safestring import mark_safe
from django.conf import settings

from .settings import ICON_SET
from .sets import ICON_THEMES
from .literals import ERROR

SIZE_SMALL = '16x16'
SIZE_BIG = '32x32'


class Icon(object):
    _registry = {}

    def __init__(self, literal):
        self.literal = literal
        self.__class__._registry[literal] = self

    def get_file_name(self, size):
        # TODO: Move name + size resolution to sets to support size/name and
        # name_size filename conventions
        try:
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
