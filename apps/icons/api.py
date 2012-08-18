from __future__ import absolute_import

from .conf import settings
from .sets import THEME_ICONSETS, DEFAULT_THEME
from .literals import ERROR


def get_icon_name(icon):
    try:
        return THEME_ICONSETS[settings.ICON_SET][icon]
    except KeyError:
        return THEME_ICONSETS[settings.ICON_SET][ERROR]


def get_sprite_name(icon):
    return THEME_ICONSETS[DEFAULT_THEME]['sprites'][icon]
