from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .icons import icon_settings
from .links import link_settings

name = 'smart_settings'
label = _(u'Smart settings')
description = _(u'Handles the configuration settings of all apps')
icon = icon_settings
dependencies = ['app_registry']
setup_links = [link_settings]
