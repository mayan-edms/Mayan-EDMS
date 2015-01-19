from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

COLOR_RED = 'red'
COLOR_BLUE = 'blu'
COLOR_MAGENTA = 'mag'
COLOR_CYAN = 'cya'
COLOR_YELLOW = 'yel'
COLOR_GREENYELLOW = 'gry'
COLOR_CORAL = 'crl'
COLOR_KHAKI = 'kki'
COLOR_LIGHTGREY = 'lig'
COLOR_ORANGE = 'org'

COLOR_CHOICES = (
    (COLOR_BLUE, _('Blue')),
    (COLOR_CYAN, _('Cyan')),
    (COLOR_CORAL, _('Coral')),
    (COLOR_GREENYELLOW, _('Green-Yellow')),
    (COLOR_KHAKI, _('Khaki')),
    (COLOR_LIGHTGREY, _('LightGrey')),
    (COLOR_MAGENTA, _('Magenta')),
    (COLOR_RED, _('Red')),
    (COLOR_ORANGE, _('Orange')),
    (COLOR_YELLOW, _('Yellow'))
)

COLOR_CODES = (
    (COLOR_RED, 'red'),
    (COLOR_BLUE, 'blue'),
    (COLOR_MAGENTA, 'magenta'),
    (COLOR_CYAN, 'cyan'),
    (COLOR_YELLOW, 'yellow'),
    (COLOR_GREENYELLOW, 'greenyellow '),
    (COLOR_CORAL, 'coral'),
    (COLOR_KHAKI, 'khaki'),
    (COLOR_ORANGE, 'orange'),
    (COLOR_LIGHTGREY, 'lightgrey'),
)
