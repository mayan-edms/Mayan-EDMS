from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .icons import icon_diagnostic
from .links import diagnostic_list

label = _(u'Diagnostics')
description = _(u'Central registration and execution of app diagnostics.')
icon = icon_diagnostic
dependencies = ['navigation', 'icons', 'permissions']
tool_links = [diagnostic_list]
