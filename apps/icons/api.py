from __future__ import absolute_import

from .conf import settings
from .sets import ICON_THEMES
from .literals import ERROR


def get_icon_name(icon):
    try:
        return ICON_THEMES[settings.ICON_SET][icon]
    except KeyError:
        return ICON_THEMES[settings.ICON_SET][ERROR]
    except AttributeError:
        pass

def get_sprite_name(sprite):
    try:
        return ICON_THEMES[settings.ICON_SET][sprite]
    except KeyError:
        return ICON_THEMES[settings.ICON_SET][ERROR]
    except AttributeError:
        pass
