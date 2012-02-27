from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _


COLOR_RED = u'red'
COLOR_BLUE = u'blu'
COLOR_MAGENTA = u'mag'
COLOR_CYAN = u'cya'
COLOR_YELLOW = u'yel'
COLOR_GREENYELLOW = u'gry'
COLOR_CORAL = u'crl'
COLOR_KHAKI = u'kki'
COLOR_LIGHTGREY = u'lig'
COLOR_ORANGE = u'org'

COLOR_CHOICES = (
    (COLOR_BLUE, _(u'Blue')),
    (COLOR_CYAN, _(u'Cyan')),
    (COLOR_CORAL, _(u'Coral')),
    (COLOR_GREENYELLOW, _(u'Green-Yellow')),
    (COLOR_KHAKI, _(u'Khaki')),
    (COLOR_LIGHTGREY, _(u'LightGrey')),
    (COLOR_MAGENTA, _(u'Magenta')),
    (COLOR_RED, _(u'Red')),
    (COLOR_ORANGE, _(u'Orange')),
    (COLOR_YELLOW, _(u'Yellow'))
)

COLOR_CODES = (
    (COLOR_RED, u'red'),
    (COLOR_BLUE, u'blue'),
    (COLOR_MAGENTA, u'magenta'),
    (COLOR_CYAN, u'cyan'),
    (COLOR_YELLOW, u'yellow'),
    (COLOR_GREENYELLOW, u'greenyellow '),
    (COLOR_CORAL, u'coral'),
    (COLOR_KHAKI, u'khaki'),
    (COLOR_ORANGE, u'orange'),
    (COLOR_LIGHTGREY, u'lightgrey'),
)
