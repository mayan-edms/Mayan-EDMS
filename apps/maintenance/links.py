from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .icons import icon_maintenance_menu, icon_maintenance_execute

maintenance_menu = Link(text=_(u'maintenance tools'), view='maintenance_menu', icon=icon_maintenance_menu)
maintenance_execute = Link(text=_(u'execute'), view='maintenance_execute', args='object.id', icon=icon_maintenance_execute)
