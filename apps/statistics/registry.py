from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .icons import icon_statistics
from .links import statistics_link

label = _(u'Statistics')
description = _(u'Central place to store and display app statistics.')
dependencies = ['app_registry', 'icons', 'navigation']
icon = icon_statistics
tool_links = [statistics_link]
