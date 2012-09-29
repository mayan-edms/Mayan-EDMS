from django.utils.translation import ugettext_lazy as _

from icons.literals import *
from icons.classes import IconSetBase


class IconSet(IconSetBase):
    path = 'custom'
    name = 'custom'
    label = _(u'Custom')
    directory = 'custom'
    dictionary = {
        FILE_EXTENSION_ERROR: 'file_extension_error.png',
        FILE_EXTENSION_UNKNOWN: 'file_extension_unknown.png'
    }
