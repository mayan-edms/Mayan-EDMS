from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from smart_settings import LocalScope

from .icons import icon_setup

label = _(u'Project setup')
description = _(u'Handles project setup function registration.')
icon = icon_setup
dependencies = ['app_registry', 'icons', 'navigation']
