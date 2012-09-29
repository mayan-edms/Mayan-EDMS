from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .icons import icon_navigation

name = 'navigation'
label = _(u'Navigation')
description = _(u'Handles UI navigation, menus and links.')
icon = icon_navigation
dependencies = ['app_registry', 'permissions']
