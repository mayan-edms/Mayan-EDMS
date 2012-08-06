from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import Link

maintenance_menu = Link(text=_(u'maintenance tools'), view='maintenance_menu', icon='rainbow.png', sprite='rainbow')
maintenance_execute = Link(text=_(u'execute'), view='maintenance_execute', args='object.id', sprite='lightning')
