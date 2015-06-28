from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .permissions import permission_installation_details

link_menu_link = Link(icon='fa fa-check-square-o', permissions=[permission_installation_details], text=_('installation details'), view='installation:namespace_list')
link_namespace_details = Link(permissions=[permission_installation_details], text=_('details'), view='installation:namespace_details', args='object.id')
link_namespace_list = Link(permissions=[permission_installation_details], text=_('installation property namespaces'), view='installation:namespace_list')
