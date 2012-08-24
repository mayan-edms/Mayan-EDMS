import os

from django.utils.translation import ugettext_lazy as _

from icons.literals import *

PATH = os.path.join('Fat Cow', '32x32')
ID = 'fat_cow'
LABEL = _(u'Fat cow')

DICTIONARY = {
    APP: 'plugin.png',
    BACKUPS: 'cd_burn.png',
    ERROR: 'error.png',
    ICONS: 'application_view_icons.png',
}
