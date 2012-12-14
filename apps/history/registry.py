from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .icons import icon_history_list
from .links import history_list
from .cleanup import cleanup

label = _(u'History')
description = _(u'Handles the events registration and event logging.')
dependencies = ['app_registry', 'icons', 'navigation']
icon = icon_history_list
tool_links = [history_list]
cleanup_functions = [cleanup]
