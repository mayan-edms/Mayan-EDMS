from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .permissions import PERMISSION_NODES_VIEW, PERMISSION_EDIT_CLUSTER_CONFIGURATION
from .icons import icon_tool_link, icon_node_link

tool_link = Link(text=_(u'clustering'), view='node_list', icon=icon_tool_link, permissions=[PERMISSION_NODES_VIEW])
node_list = Link(text=_(u'node list'), view='node_list', icon=icon_node_link, permissions=[PERMISSION_NODES_VIEW])
