from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .icons import icon_user
from .links import user_setup, group_setup

label = _(u'User management')
description = _(u'Handles user accounts and groups.')
icon = icon_user
dependencies = ['app_registry', 'icons', 'navigation', 'permissions']
setup_links = [user_setup, group_setup]
