from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .icons import icon_tick

name = 'common'
label = _(u'Common')
description = _(u'Contains many commonly used models, views and utilities.')
dependencies = ['app_registry']
icon = icon_tick
