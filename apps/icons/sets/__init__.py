from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from icons.sets import fat_cow, famfamfam


SET_CHOICES = (
    (fat_cow.ID, fat_cow.LABEL),
    (famfamfam.ID, famfamfam.LABEL),
)

ICON_THEMES = {
    fat_cow.ID: fat_cow,
    famfamfam.ID: famfamfam,
}


"""
THEME_DEFAULT = 'default'

SET_CHOICES = (
    (fat_cow.ID, fat_cow.LABEL),
    (famfamfam.ID, famfamfam.LABEL),
)

THEME_ICONSETS = {
    THEME_DEFAULT: {
        'icons': fat_cow.DICTIONARY,
        'sprites': famfamfam.DICTIONARY
    }
}

THEMES_CHOICES = {
    THEME_DEFAULT: _(u'Default theme (using Fat cow for icons and FamFamFam for sprites)')
}

DEFAULT_THEME = THEME_DEFAULT
"""
