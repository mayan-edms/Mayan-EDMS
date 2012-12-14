from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .icons import icon_folders
from .links import menu_link
from .cleanup import cleanup

label = _(u'Folders')
description = _(u'Allow manual grouping of documents.')
icon = icon_folders
dependencies = ['navigation', 'icons', 'permissions', 'acls', 'documents']
menu_links = [menu_link]
cleanup_functions = [cleanup]
