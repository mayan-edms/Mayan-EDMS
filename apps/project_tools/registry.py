from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from smart_settings import LocalScope

from .icons import icon_tool

label = _(u'Project tools')
description = _(u'Handles project tools registration.')
icon = icon_tool
dependencies = ['app_registry', 'icons', 'navigation']
