from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .icons import icon_statistics

label = _(u'Statistics')
description = _(u'Central place to store and display app statistics.')
dependencies = ['app_registry', 'icons', 'navigation']
icon = icon_statistics
