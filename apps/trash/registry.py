from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .icons import icon_trash_cans
from .links import trash_can_list

label = _(u'Trash manager')
description = _(u'Provides a generic and reusable trash bin.')
icon = icon_trash_cans
dependencies = ['app_registry', 'icons', 'documents', 'permissions', 'navigation', 'documents', 'tags', 'folders']
tool_links = [trash_can_list]
