from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import Link

from .permissions import (PERMISSION_NODES_VIEW)

tool_link = Link(text=_(u'clustering'), view='node_list', icon='server.png', permissions=[PERMISSION_NODES_VIEW])  # children_view_regex=[r'^index_setup', r'^template_node'])
node_list = Link(text=_(u'node list'), view='node_list', sprite='server', permissions=[PERMISSION_NODES_VIEW])
