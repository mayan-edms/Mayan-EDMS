from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .icons import icon_user

name = 'user_management'
label = _(u'User management')
description = _(u'Handles the registration of apps in a project.')
icon = icon_user
dependencies = ['app_registry']
