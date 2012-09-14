from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .icons import icon_maintenance_menu
from .links import maintenance_menu

label = _(u'Maintenance')
description = _(u'Central registration and execution of app maintenance code.')
icon = icon_maintenance_menu
dependencies = ['navigation', 'icons', 'permissions']
tool_links = [maintenance_menu]
