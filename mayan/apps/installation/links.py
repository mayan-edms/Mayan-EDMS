from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .permissions import PERMISSION_INSTALLATION_DETAILS

link_menu_link = Link(icon='fa fa-flag', permissions=[PERMISSION_INSTALLATION_DETAILS], text=_('Installation details'), view='installation:namespace_list')
link_namespace_details = Link(permissions=[PERMISSION_INSTALLATION_DETAILS], text=_('Details'), view='installation:namespace_details', args='object.id')
link_namespace_list = Link(permissions=[PERMISSION_INSTALLATION_DETAILS], text=_('Installation property namespaces'), view='installation:namespace_list')
