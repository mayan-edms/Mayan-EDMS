from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .icons import icon_icons_app

name = 'icons'
label = _(u'Icons')
description = _(u'Handles the registration and rendering of icons and sprites.')
dependencies = ['app_registry']
icon = icon_icons_app
