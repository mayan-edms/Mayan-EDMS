from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import Link

from .permissions import PERMISSION_NODES_VIEW, PERMISSION_EDIT_CLUSTER_CONFIGURATION

tool_link = Link(text=_(u'clustering'), view='node_list', icon='server.png', permissions=[PERMISSION_NODES_VIEW])
node_list = Link(text=_(u'node list'), view='node_list', sprite='server', permissions=[PERMISSION_NODES_VIEW])
clustering_config_edit = Link(text=_(u'edit cluster configuration'), view='clustering_config_edit', sprite='server_edit', permissions=[PERMISSION_EDIT_CLUSTER_CONFIGURATION])
setup_link = Link(text=_(u'cluster configuration'), view='clustering_config_edit', icon='server.png', permissions=[PERMISSION_EDIT_CLUSTER_CONFIGURATION])
