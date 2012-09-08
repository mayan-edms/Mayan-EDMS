from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .icons import icon_app
from .links import app_registry_tool_link

name = 'app_registry'
label = _(u'App registry')
description = _(u'Handles the registration of apps in a project.')
icon = icon_app
tool_links = [app_registry_tool_link]
dependencies = ['navigation']
