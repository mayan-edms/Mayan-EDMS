from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .icons import icon_tag_list

label = _(u'Tagging')
#description = _(u'Central place to store and display app statistics.')
dependencies = ['app_registry', 'icons', 'navigation']
icon = icon_tag_list
