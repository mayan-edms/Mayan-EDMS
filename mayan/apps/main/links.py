from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Link


def is_superuser(context):
    return context['request'].user.is_staff or context['request'].user.is_superuser


link_admin_site = Link(condition=is_superuser, icon='fa fa-keyboard-o', text=_('Admin site'), view='admin:index')
link_maintenance_menu = Link(icon='fa fa-wrench', text=_('Maintenance'), view='main:maintenance_menu')
link_setup = Link(icon='fa fa-gear', text=_('Setup'), view='main:setup_list')
link_tools = Link(icon='fa fa-wrench', text=_('Tools'), view='main:tools_list')
